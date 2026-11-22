"""Re-render only the scenes that changed since the last full render, and splice them into the video.

    python tools/make.py projects/<slug> cards       # after fixing the wrong cards
    python tools/make.py projects/<slug> patch       # renders the changed time ranges only, splices, rebuilds the sound, muxes

How it works: `make.py video` (a full render) saves the plan it rendered as out/plan.rendered.json. `patch` compares the
current work/plan.merged.json with it scene by scene (ignoring ids, card numbers and narration text). A scene that changed
is re-rendered from its start to its end + 0.7 s (the dissolve into the next scene), neighbouring ranges are merged, and
the new pieces replace the old frames in out/picture.mp4 (the previous picture is kept as out/picture.prev.mp4).
Changes to the cast re-render the scenes where that person appears; a change of look/grade/size needs a full `video`.
`patch` compares PLANS: it cannot see a change in the engine (src/: how arms, sets or props are drawn). After an engine
change, render the whole film again with `video`.

    --dry      only print what would be re-rendered
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FPS = 24
IGNORE = {"id", "card", "beat", "sfx", "ambience", "chapter"}


def _norm(s):
    return json.dumps({k: v for k, v in s.items() if k not in IGNORE}, sort_keys=True, ensure_ascii=False)


def _who(s):
    out = set()
    for e in s.get("elements", []):
        w = e.get("who")
        if isinstance(w, str):
            out.add(w)
        elif isinstance(w, list):
            out |= set(w)
    return out


def changed_ranges(old, new):
    if {k: v for k, v in old["meta"].items() if k not in ("duration", "voice")} != {k: v for k, v in new["meta"].items() if k not in ("duration", "voice")}:
        return None, ["the film's meta (look, grade, size) changed"]
    cast_changed = {cid for cid in set(old.get("cast", {})) | set(new.get("cast", {})) if old.get("cast", {}).get(cid) != new.get("cast", {}).get(cid)}
    old_set = {_norm(s) for s in old["scenes"]}
    ranges, why = [], []
    for s in new["scenes"]:
        reason = None
        if _norm(s) not in old_set:
            reason = "changed"
        elif _who(s) & cast_changed:
            reason = f"cast changed ({', '.join(sorted(_who(s) & cast_changed))})"
        if reason:
            ranges.append([max(0.0, s["start"]), min(new["meta"]["duration"], s["end"] + 0.7)])
            why.append(f"{s['id']} {s['start']:.2f}-{s['end']:.2f} {reason}: {s.get('beat', '')[:60]}")
    ranges.sort()
    merged = []
    for a, b in ranges:
        if merged and a <= merged[-1][1] + 0.5:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    # whole frames
    return [[round(a * FPS) / FPS, round(b * FPS) / FPS] for a, b in merged], why


def run(cmd):
    print("$", " ".join(str(c) for c in cmd))
    r = subprocess.run([str(c) for c in cmd], cwd=ROOT)
    if r.returncode:
        sys.exit(r.returncode)


def main():
    proj = Path(sys.argv[1]).resolve()
    dry = "--dry" in sys.argv
    merged = proj / "work" / "plan.merged.json"
    rendered = proj / "out" / "plan.rendered.json"
    pic = proj / "out" / "picture.mp4"
    if not rendered.exists() or not pic.exists():
        sys.exit("no previous full render (out/picture.mp4 + out/plan.rendered.json): run `python tools/make.py <proj> video` once first")
    old = json.loads(rendered.read_text(encoding="utf-8"))
    new = json.loads(merged.read_text(encoding="utf-8"))
    ranges, why = changed_ranges(old, new)
    if ranges is None:
        sys.exit(f"{why[0]}: run a full `python tools/make.py {proj} video` instead")
    if abs(old["meta"]["duration"] - new["meta"]["duration"]) > 0.05:
        ranges.append([round(min(old["meta"]["duration"], new["meta"]["duration"]) * FPS) / FPS - 1.0, new["meta"]["duration"]])
    print(json.dumps({"changed": why, "ranges": ranges}, indent=1, ensure_ascii=False))
    if not ranges:
        print("nothing changed in the picture; rebuilding the sound only")
    if dry:
        return
    parts = []
    for k, (a, b) in enumerate(ranges):
        out = proj / "out" / f"patch_{k}.mp4"
        run(["node", ROOT / "tools" / "render.mjs", "video", merged, out, "--from", f"{a:.3f}", "--to", f"{b:.3f}"])
        parts.append((a, b, out))
    if parts:
        prev = proj / "out" / "picture.prev.mp4"
        shutil.copyfile(pic, prev)
        total = round(new["meta"]["duration"] * FPS)
        inputs = ["-i", prev]
        chains, labels, cur = [], [], 0
        # frame-exact splice: render.mjs renders frames [round(a*FPS), round(b*FPS) - 1] for a range
        for k, (a, b, f) in enumerate(parts):
            fa, fb = round(a * FPS), round(b * FPS)
            inputs += ["-i", f]
            if fa > cur:
                chains.append(f"[0:v]trim=start_frame={cur}:end_frame={fa},setpts=PTS-STARTPTS[o{k}]")
                labels.append(f"[o{k}]")
            chains.append(f"[{k + 1}:v]trim=end_frame={fb - fa},setpts=PTS-STARTPTS[n{k}]")
            labels.append(f"[n{k}]")
            cur = fb
        if cur < total:
            chains.append(f"[0:v]trim=start_frame={cur}:end_frame={total},setpts=PTS-STARTPTS[tail]")
            labels.append("[tail]")
        fc = ";".join(chains) + ";" + "".join(labels) + f"concat=n={len(labels)}:v=1:a=0[v]"
        run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
             "-pix_fmt", "yuv420p", pic])
        for _, _, f in parts:
            f.unlink(missing_ok=True)
    run([sys.executable, ROOT / "tools" / "mix_audio.py", proj, "--plan", merged])
    slug = proj.name
    final = proj / "out" / f"{slug}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", pic, "-i", proj / "out" / "audio" / "mix.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", final])
    shutil.copyfile(merged, rendered)
    print(json.dumps({"video": str(final), "re_rendered_s": round(sum(b - a for a, b, _ in parts), 2)}))


if __name__ == "__main__":
    main()
