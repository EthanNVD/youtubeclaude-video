"""Merge + validate a plan before rendering.

python tools/validate_plan.py projects/<slug>
  input:  plan.json            (single file)  OR
          plan/_meta.json      ({meta, cast})  +  plan/ch*.json  ([scenes] or {scenes:[...]}) in name order
  output: work/plan.merged.json  (always written; render/mix read this)
  exit 1 on errors. Vocabulary (set kinds, props, vehicles, fx, presets, element kinds) is read from src/ so
  it never drifts from the engine.
"""
import json, re, sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"


def cases(path, fn=None):
    s = (SRC / path).read_text(encoding="utf-8")
    if fn:
        i = s.index(fn)
        s = s[i:]
    return set(re.findall(r"case '([\w-]+)'", s))


def vocab():
    v = {
        "sets": cases("sets/Sets.tsx", "const BaseSet") | cases("sets/Rich.tsx", "export const RichSet"),
        "fg": cases("sets/Rich.tsx", "export const Foreground"),
        "props": cases("props/Props.tsx", "export const Prop:"),
        "vehicles": cases("props/Vehicles.tsx", "export const Vehicle:"),
        "fx": cases("fx/Fx.tsx"),
        "kinds": cases("scene/Elements.tsx", "export const ElementView") | {"date", "namecard"},
        "presets": set(re.findall(r"^\s{2}(\w+): \{", (SRC / "char/presets.ts").read_text(encoding="utf-8"), re.M)),
        "poses": set(re.findall(r"^\s{2}(\w+): \{ r:", (SRC / "char/Character.tsx").read_text(encoding="utf-8"), re.M)),
        "eras": {p.stem.replace("world_", "") for p in (ROOT / "public/maps").glob("world_*.json")},
        "nations": set(re.findall(r"^\s{2}(\w+): \{ name:", (SRC / "theme.ts").read_text(encoding="utf-8"), re.M)),
    }
    return v


EXPRS = {"grin", "neutral", "happy", "smile", "laugh", "angry", "rage", "determined", "smug", "worried", "sad", "cry", "panic", "nervous",
         "sweat", "shocked", "shout", "tired"}


def merge(proj):
    if (proj / "plan.json").exists() and not (proj / "plan").is_dir():
        return json.loads((proj / "plan.json").read_text(encoding="utf-8"))
    d = proj / "plan"
    base = json.loads((d / "_meta.json").read_text(encoding="utf-8"))
    scenes = []
    for f in sorted(d.glob("ch*.json")):
        part = json.loads(f.read_text(encoding="utf-8"))
        scenes += part["scenes"] if isinstance(part, dict) else part
    base["scenes"] = scenes
    return base


SHOT_SIZES = ("wide", "full", "medium", "mediumclose", "close", "ecu")
COVER = {"setups": 0, "close": 0, "acting_s": 0.0}


def main(proj):
    proj = Path(proj)
    plan = merge(proj)
    V = vocab()
    err, warn = [], []
    meta = plan.get("meta", {})
    scenes = sorted(plan.get("scenes", []), key=lambda s: s["start"])
    plan["scenes"] = scenes
    cast = plan.get("cast", {})
    if not scenes:
        err.append("no scenes")
    stats = proj / "work" / "stats.json"
    vdur = json.loads(stats.read_text())["voice_duration"] if stats.exists() else None
    if vdur and meta.get("duration", 0) < vdur:
        warn.append(f"meta.duration {meta.get('duration')} < voice {vdur:.2f}; extended")
        meta["duration"] = round(vdur + 1.0, 2)
    ids = set()
    for i, s in enumerate(scenes):
        sid = s.get("id", f"#{i}")
        if sid in ids:
            err.append(f"{sid}: duplicate id")
        ids.add(sid)
        if i == 0 and s["start"] > 0.01:
            err.append(f"{sid}: first scene must start at 0")
        if i > 0 and abs(s["start"] - scenes[i - 1]["end"]) > 0.05:
            err.append(f"{sid}: gap/overlap with previous ({scenes[i-1]['end']} -> {s['start']})")
        dur = s["end"] - s["start"]
        if dur <= 0:
            err.append(f"{sid}: end <= start")
        if dur < 1.0:
            warn.append(f"{sid}: very short shot ({dur:.2f}s)")
        if dur > 20 and s.get("type") != "chapter":
            warn.append(f"{sid}: long shot ({dur:.1f}s) — add a cut, camera move or new event")
        t = s.get("type")
        if t not in ("stage", "map", "title", "chapter"):
            err.append(f"{sid}: bad type {t}")
        if t == "stage":
            k = (s.get("set") or {}).get("kind")
            if k and k not in V["sets"]:
                err.append(f"{sid}: unknown set '{k}' (have: {', '.join(sorted(V['sets']))})")
            fg = (s.get("set") or {}).get("fg")
            if fg and fg not in V["fg"]:
                err.append(f"{sid}: unknown foreground '{fg}' (have: {', '.join(sorted(V['fg']))})")
            # coverage: shots inside the scene (see references/acting-camera.md)
            els = s.get("elements", [])
            ids = {e.get("id") for e in els if e.get("id")}
            shots = s.get("shots") or []
            for q in shots:
                refs = q.get("on")
                refs = [] if refs is None else refs if isinstance(refs, list) else [refs]
                for r in refs:
                    if isinstance(r, int) and not 0 <= r < len(els):
                        err.append(f"{sid}: shot t={q.get('t')} frames element #{r}, which does not exist")
                    elif isinstance(r, str) and r not in ids:
                        err.append(f"{sid}: shot t={q.get('t')} frames '{r}' — no element has that id")
                if q.get("size") and q["size"] not in SHOT_SIZES:
                    err.append(f"{sid}: shot size '{q['size']}' (have {', '.join(SHOT_SIZES)})")
                if q.get("t", 0) > dur + 0.01:
                    warn.append(f"{sid}: shot at t={q['t']} is after the scene end")
            starts = sorted({0.0} | {float(q.get("t", 0)) for q in shots})
            longest = max([b - a for a, b in zip(starts, starts[1:] + [dur])] or [dur])
            has_people = any(e.get("kind") in ("actor", "crowd") for e in els)
            if has_people and not s.get("camera") and longest > 6.5:
                warn.append(f"{sid}: one set-up for {longest:.1f}s — add a cut inside the place (scene.shots: wide → medium → close/insert)")
            COVER["setups"] += max(1, len(shots))
            COVER["acting_s"] += dur if has_people else 0
            for q in shots:
                if q.get("size") in ("close", "ecu", "mediumclose"):
                    COVER["close"] += 1
            # people do not sprint across rooms: a walk is ~60-140 px/s at scale 1, a run up to ~330
            for j2, e2 in enumerate(els):
                if e2.get("kind") != "actor" or e2.get("run"):
                    continue
                keys = sorted([k for k in (e2.get("keys") or []) if "x" in k], key=lambda k: k["t"])
                t0, x0 = 0.0, e2.get("x")
                for k in keys:
                    if x0 is not None and k["t"] > t0:
                        sc = e2.get("scale") or 1.0
                        v = abs(k["x"] - x0) / (k["t"] - t0) / max(0.2, sc)
                        if v > 420:
                            warn.append(f"{sid}.e{j2}(actor {e2.get('who')}): crosses {abs(k['x'] - x0):.0f}px in {k['t'] - t0:.2f}s ({v:.0f} px/s at scale 1) — that is a sprint; give the walk more time")
                    t0, x0 = k["t"], k["x"]
        if t == "map":
            m = s.get("map") or {}
            if "center" not in m or "span" not in m:
                err.append(f"{sid}: map needs center + span")
            if str(m.get("era", "1938")) not in V["eras"]:
                err.append(f"{sid}: unknown map era {m.get('era')} (have {sorted(V['eras'])})")
        for j, el in enumerate(s.get("elements", [])):
            k = el.get("kind")
            tag = f"{sid}.e{j}({k})"
            if k not in V["kinds"]:
                err.append(f"{tag}: unknown element kind")
                continue
            if el.get("in", 0) > dur + 0.01:
                warn.append(f"{tag}: appears after scene end ({el.get('in')} > {dur:.2f})")
            for key in el.get("keys", []) or []:
                if key.get("t", 0) > dur + 0.5:
                    warn.append(f"{tag}: key t={key['t']} beyond scene ({dur:.2f})")
            if k == "actor":
                who = el.get("who", "")
                if who not in cast and who not in V["presets"]:
                    err.append(f"{tag}: who '{who}' not in cast/presets")
                for st in [el] + (el.get("keys") or []):
                    if st.get("pose") and st["pose"] not in V["poses"]:
                        err.append(f"{tag}: unknown pose '{st['pose']}' (have {sorted(V['poses'])})")
                    if st.get("expr") and st["expr"] not in EXPRS:
                        warn.append(f"{tag}: unknown expr '{st['expr']}'")
            if k == "prop" and el.get("item") not in V["props"]:
                warn.append(f"{tag}: unknown prop '{el.get('item')}' (placeholder box will render)")
            if k == "vehicle" and el.get("type") not in V["vehicles"]:
                err.append(f"{tag}: unknown vehicle '{el.get('type')}'")
            if k == "fx" and el.get("type") not in V["fx"]:
                err.append(f"{tag}: unknown fx '{el.get('type')}'")
            if k in ("label", "bubble") and len(str(el.get("text", ""))) > 48:
                warn.append(f"{tag}: long on-screen text ({len(str(el.get('text')))} chars) — labels are 1–5 words")
            if el.get("at") and t != "map":
                warn.append(f"{tag}: 'at' only works in map scenes")
            n = el.get("nation")
            if n and n.upper() not in V["nations"]:
                warn.append(f"{tag}: unknown nation '{n}'")
    # layout + motion checks (text never on text / badges / faces; vehicles at believable speeds)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import layout_check
    layout = []
    for s in scenes:
        if s.get("type") == "stage":
            layout += layout_check.overlaps(s)
            layout += layout_check.speeds(s)
            layout += layout_check.proportions(s)
        elif s.get("type") == "map":
            layout += [w for w in layout_check.overlaps(s)]
    warn += layout
    for name, c in cast.items():
        if c.get("preset") and c["preset"] not in V["presets"]:
            err.append(f"cast.{name}: unknown preset '{c['preset']}'")
    if scenes and vdur and scenes[-1]["end"] < vdur - 0.1:
        err.append(f"last scene ends {scenes[-1]['end']} before voice ends {vdur:.2f}")
    out = proj / "work" / "plan.merged.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    chapters = [(s["start"], s.get("chapter") or s.get("title")) for s in scenes if s.get("chapter") or s.get("type") == "chapter"]
    total = scenes[-1]["end"] if scenes else 0
    coverage = {"setups": COVER["setups"] + sum(1 for s in scenes if s.get("type") != "stage"),
                "avg_setup_s": round(total / max(1, COVER["setups"] + sum(1 for s in scenes if s.get("type") != "stage")), 2),
                "close_shots": COVER["close"], "acting_share": round(COVER["acting_s"] / max(1e-6, total), 2)}
    print(json.dumps({"scenes": len(scenes), "duration": total, "chapters": len(chapters), "coverage": coverage,
                      "errors": err, "warnings": warn[:150], "warnings_total": len(warn), "merged": str(out)}, ensure_ascii=False, indent=1))
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main(sys.argv[1])
