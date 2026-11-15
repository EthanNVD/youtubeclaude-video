"""One entry point for the whole pipeline.

python tools/make.py <project> analyze     SRT + voice -> work/reading.md, stats.json (read before planning)
python tools/make.py <project> validate    merge plan -> work/plan.merged.json, check vocabulary/timing
python tools/make.py <project> review      stills of every scene -> review/sheet_*.jpg (look at them!)
python tools/make.py <project> audio       voice + ambience + SFX -> out/audio/mix.wav (+ stems)
python tools/make.py <project> video       render picture (muted) -> out/picture.mp4
python tools/make.py <project> mux         picture + mix -> out/<slug>.mp4
python tools/make.py <project> thumbs      thumbs.json -> out/thumbs/thumb_1..3.png
python tools/make.py <project> package     youtube/package.json -> out/youtube/ (checks + publish.txt)
python tools/make.py <project> all         validate, audio, video, mux, thumbs, package
options: --from S --to S (partial video), --scenes s1,s2 (review subset)
"""
import json, subprocess, sys, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable


def run(cmd, **kw):
    print("$", " ".join(str(c) for c in cmd))
    r = subprocess.run([str(c) for c in cmd], cwd=ROOT, **kw)
    if r.returncode:
        sys.exit(r.returncode)


def node(*a):
    run(["node", ROOT / "tools" / "render.mjs", *a])


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    proj = Path(sys.argv[1]).resolve()
    step = sys.argv[2]
    rest = sys.argv[3:]
    opt = lambda k: rest[rest.index("--" + k) + 1] if "--" + k in rest else None
    merged = proj / "work" / "plan.merged.json"
    slug = proj.name

    def analyze():
        run([PY, ROOT / "tools/srt_tool.py", proj])

    def validate():
        run([PY, ROOT / "tools/validate_plan.py", proj])

    def review():
        validate()
        d = proj / "review"
        if d.exists() and not opt("scenes"):
            shutil.rmtree(d)
        args = ["stills", merged, d, "--scale", "0.5", "--at", opt("at") or "mid"]
        if opt("scenes"):
            args += ["--scenes", opt("scenes")]
        node(*args)
        run([PY, ROOT / "tools/contact_sheet.py", d, "--per", "12"])

    def audio():
        validate()
        run([PY, ROOT / "tools/mix_audio.py", proj, "--plan", merged])

    def video():
        validate()
        (proj / "out").mkdir(exist_ok=True)
        args = ["video", merged, proj / "out" / "picture.mp4"]
        if opt("from"):
            args += ["--from", opt("from"), "--to", opt("to") or str(float(opt("from")) + 20)]
        if opt("concurrency"):
            args += ["--concurrency", opt("concurrency")]
        node(*args)

    def mux():
        pic, mix = proj / "out" / "picture.mp4", proj / "out" / "audio" / "mix.wav"
        out = proj / "out" / f"{slug}.mp4"
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", pic, "-i", mix, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart"]
        if opt("from"):
            cmd += ["-ss", "0"]
        cmd += ["-shortest", out]
        run(cmd)
        print(json.dumps({"video": str(out)}))

    def thumbs():
        src = proj / "thumbs.json"
        if not src.exists():
            print("no thumbs.json — skipped")
            return
        data = json.loads(src.read_text(encoding="utf-8"))
        if "cast" not in data and merged.exists():
            data["cast"] = json.loads(merged.read_text(encoding="utf-8")).get("cast", {})
            tmp = proj / "work" / "thumbs.merged.json"
            tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            src = tmp
        node("thumb", src, proj / "out" / "thumbs")
        # YouTube limit: < 2 MB -> also write high-quality JPGs
        for p in sorted((proj / "out" / "thumbs").glob("thumb_*.png")):
            run(["ffmpeg", "-v", "error", "-y", "-i", p, "-q:v", "2", p.with_suffix(".jpg")])

    def package():
        run([PY, ROOT / "tools/seo_check.py", proj])

    steps = {"analyze": [analyze], "validate": [validate], "review": [review], "audio": [audio], "video": [video], "mux": [mux],
             "thumbs": [thumbs], "package": [package], "all": [audio, video, mux, thumbs, package]}
    if step not in steps:
        sys.exit(__doc__)
    for f in steps[step]:
        f()


if __name__ == "__main__":
    main()
