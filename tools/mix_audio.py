"""Build the soundtrack: user's voice + ambience beds + action SFX (no music).

python tools/mix_audio.py projects/<slug> [--plan work/plan.merged.json]
writes out/audio/mix.wav (loudness-normalised, -14 LUFS / -1.5 dBTP)
       out/audio/stems/{voice,ambience,sfx}.wav   (same clock, start = 0)
       work/sfx_cues.json  (every cue actually placed: scene, time, id, source=plan|auto)
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np
from scipy import signal

ROOT = Path(__file__).resolve().parent.parent
SFX = ROOT / "assets" / "sfx"
SR = 48000

# default ambience per set kind (scene.ambience overrides; null = silence)
SET_AMB = {
    "sea": "amb_sea", "ocean": "amb_sea", "beach": "amb_sea", "harbor": "amb_sea", "dock": "amb_sea",
    "field": "amb_wind", "countryside": "amb_wind", "steppe": "amb_wind", "desert": "amb_wind", "mud": "amb_rain",
    "snow": "amb_wind_cold", "sky": "amb_engine", "air": "amb_engine", "office": "amb_office", "study": "amb_office",
    "cabinet": "amb_room", "conference": "amb_room", "warroom": "amb_room", "bunker": "amb_basement",
    "codebreak": "amb_basement", "classroom": "amb_room", "kitchen": "amb_room", "home": "amb_room",
    "factory": "amb_factory", "rally": "amb_crowd", "podium": "amb_crowd", "city": "amb_wind", "street": "amb_wind",
    "ruins": "amb_fire", "trench": "amb_battle", "jungle": "amb_jungle", "railway": "amb_wind", "station": "amb_wind",
}
# gain (dB) per id family
GAIN = {"amb": -24, "explosion": -6, "explosion_big": -4, "artillery": -6, "stamp": -8, "pop": -16, "whoosh": -16,
        "whoosh_soft": -20, "whoosh_fast": -16, "paper": -14, "typewriter": -14, "chalk": -16, "pen": -18,
        "map_draw": -20, "clock_tick": -18, "tick": -18, "impact": -8, "riser": -16, "plane_flyby": -10,
        "plane_dive": -10, "machinegun": -10, "gunshot": -10, "cannon": -8, "boom_distant": -14, "heartbeat": -12}
LOOP_IDS = {"clock_tick", "typewriter", "chalk", "pen", "map_draw", "machinegun", "plane_engine", "tank_engine", "truck", "train", "morse", "radio_static"}

_cache = {}


def load(name):
    if name in _cache:
        return _cache[name]
    p = SFX / f"{name}.wav"
    if not p.exists():
        print(f"  ! missing sfx '{name}' (add assets/sfx/{name}.wav or tools/sfx_synth.py)")
        _cache[name] = None
        return None
    with wave.open(str(p)) as w:
        sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
        x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
    if ch == 2:
        x = x.reshape(-1, 2).mean(1)
    if sr != SR:
        x = signal.resample_poly(x, SR, sr).astype(np.float32)
    _cache[name] = x
    return x


def db(g):
    return 10 ** (g / 20)


def read_any(path):
    """decode any audio file to mono float32 @48k via ffmpeg"""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
    if r.returncode:
        sys.exit(r.stderr.decode())
    return np.frombuffer(r.stdout, dtype=np.float32).copy()


def write(path, x):
    path.parent.mkdir(parents=True, exist_ok=True)
    x = np.clip(x, -1, 1)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def auto_cues(scene):
    """SFX implied by elements (only where the picture shows a contact/event)."""
    cues = []
    for el in scene.get("elements", []):
        k, tin = el.get("kind"), float(el.get("in", 0) or 0)
        if k == "stamp":
            cues.append((tin + 0.15, "stamp", 0))
        elif k == "burst":
            cues.append((tin, "explosion_big" if (el.get("size") or 0.5) >= 0.8 else "explosion", 0))
        elif k == "fx" and el.get("type") in ("explosion", "impact"):
            cues.append((tin, "explosion", 0))
        elif k == "fx" and el.get("type") == "splash":
            cues.append((tin, "splash", 0))
        elif k == "document":
            n = sum(len(l) for l in el.get("lines", []))
            dur = min(6.0, n / float(el.get("speed", 28) or 28))
            style = el.get("style", "letter")
            sid = "typewriter" if style in ("telegram", "order") else "chalk" if style == "blackboard" else "pen" if style in ("letter", "note") else "paper"
            cues.append((tin, sid, dur))
        elif k == "arrow" and scene.get("type") == "map":
            cues.append((tin, "map_draw", float(el.get("dur", 1.4))))
        elif k in ("headline", "text"):
            cues.append((tin, "whoosh_soft", 0))
        elif k == "counter":
            cues.append((tin + float(el.get("dur", 1.5)), "pop", 0))
        elif k == "vehicle" and el.get("type") in ("fighter", "plane", "bomber", "divebomber") and el.get("keys"):
            cues.append((tin, "plane_flyby", 0))
    if scene.get("transition") == "flash":
        cues.append((0.0, "impact", 0))
    return cues


def main(proj, plan_path=None):
    proj = Path(proj)
    plan_path = Path(plan_path) if plan_path else (proj / "work" / "plan.merged.json" if (proj / "work" / "plan.merged.json").exists() else proj / "plan.json")
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    scenes = plan["scenes"]
    total = max(plan["meta"]["duration"], scenes[-1]["end"])
    N = int(total * SR) + SR
    voice = np.zeros(N, dtype=np.float32)
    vpath = plan["meta"].get("voice")
    if vpath:
        v = read_any(proj / vpath)
        off = float(plan["meta"].get("voiceOffset", 0))
        place = int(off * SR)
        voice[place:place + len(v)] = v[: N - place]
    # voice envelope for ducking (smoothed RMS)
    env = np.sqrt(signal.sosfiltfilt(signal.butter(2, 3 / (SR / 2), output="sos"), voice.astype(np.float64) ** 2).clip(0))
    speaking = (env > 0.01).astype(np.float32)
    speaking = signal.sosfiltfilt(signal.butter(1, 1.5 / (SR / 2), output="sos"), speaking).clip(0, 1).astype(np.float32)

    amb = np.zeros(N, dtype=np.float32)
    sfx = np.zeros(N, dtype=np.float32)
    log = []
    # ---- ambience beds: phase follows absolute time so cuts inside one space don't restart the loop ----
    fade = int(0.35 * SR)
    for s in scenes:
        aid = s.get("ambience", "__default__")
        if aid == "__default__":
            aid = SET_AMB.get((s.get("set") or {}).get("kind", ""), None) if s.get("type") == "stage" else None
        if not aid:
            continue
        if not aid.startswith("amb_"):
            aid = "amb_" + aid
        bed = load(aid)
        if bed is None:
            continue
        a, b = int(s["start"] * SR), int(s["end"] * SR)
        idx = (np.arange(a, b) % len(bed))
        seg = bed[idx] * db(GAIN["amb"] + float(s.get("ambienceGain", 0)))
        w = np.ones(b - a, dtype=np.float32)
        f = min(fade, (b - a) // 2)
        w[:f] = np.linspace(0, 1, f)
        w[-f:] = np.linspace(1, 0, f)
        amb[a:b] += seg * w
    amb *= 1 - 0.45 * speaking  # duck beds ~5 dB under narration

    # ---- SFX cues ----
    for s in scenes:
        explicit = [(float(c["t"]), c["id"], float(c.get("dur", 0) or 0), float(c.get("vol", 0) or 0), "plan") for c in s.get("sfx", [])]
        autos = [(t, i, d, 0.0, "auto") for (t, i, d) in auto_cues(s) if not any(abs(t - e[0]) < 0.25 and (e[1] == i or e[1].split("_")[0] == i.split("_")[0]) for e in explicit)]
        if s.get("autoSfx") is False:
            autos = []
        dedup = []
        for c in autos:  # one auto cue per id per 1.5 s inside a scene
            if not any(c[1] == d[1] and abs(c[0] - d[0]) < 1.5 for d in dedup):
                dedup.append(c)
        autos = dedup
        for (t, sid, dur, vol, src) in explicit + autos:
            x = load(sid)
            if x is None:
                continue
            if dur > 0:
                n = int(dur * SR)
                if sid in LOOP_IDS and n > len(x):
                    x = np.tile(x, n // len(x) + 1)
                x = x[:n].copy()
                r = min(len(x), int(0.15 * SR))
                x[-r:] *= np.linspace(1, 0, r)
            g = db(GAIN.get(sid, -12) + vol)
            at = int((s["start"] + t) * SR)
            n = min(len(x), N - at)
            if n > 0:
                sfx[at:at + n] += x[:n] * g
                log.append({"scene": s["id"], "t": round(s["start"] + t, 3), "id": sid, "dur": dur, "source": src})

    out = proj / "out" / "audio"
    vg = voice
    # normalise voice to a consistent speech level before mixing (~ -16 LUFS approx via RMS of voiced parts)
    voiced = vg[speaking > 0.5]
    if len(voiced):
        rms = np.sqrt(np.mean(voiced ** 2))
        vg = vg * (0.1 / max(rms, 1e-5))
    mix = vg + amb + sfx * 0.9
    write(out / "stems" / "voice.wav", vg)
    write(out / "stems" / "ambience.wav", amb)
    write(out / "stems" / "sfx.wav", sfx)
    raw = out / "mix_raw.wav"
    write(raw, mix / max(1.0, np.max(np.abs(mix)) * 1.05))
    final = out / "mix.wav"
    # gain + true-peak limiter, iterated until integrated loudness is -14 LUFS (+-0.3), peaks <= -1.5 dBTP
    gain = 0.0
    for _ in range(4):
        chain = f"volume={gain:.2f}dB,alimiter=limit=0.84:level=disabled:attack=2:release=60"
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(raw), "-af", chain + ",ebur128", "-f", "null", "-"], capture_output=True, text=True)
        meas = float(r.stderr.rsplit("I:", 1)[1].split("LUFS")[0])
        if abs(meas + 14) < 0.3:
            break
        gain += -14 - meas
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", chain, "-ar", str(SR), str(final)], check=True)
    raw.unlink()
    (proj / "work").mkdir(exist_ok=True)
    (proj / "work" / "sfx_cues.json").write_text(json.dumps(log, indent=0), encoding="utf-8")
    print(json.dumps({"mix": str(final), "seconds": round(N / SR, 2), "sfx_cues": len(log), "auto": sum(1 for l in log if l["source"] == "auto")}))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[a.index("--plan") + 1] if "--plan" in a else None)
