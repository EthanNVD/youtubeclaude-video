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
    "ruins": "amb_fire", "trench": "amb_battle", "nomansland": "amb_battle", "jungle": "amb_jungle", "railway": "amb_wind", "station": "amb_wind",
    # detailed acting sets
    "deck": "amb_sea", "flightdeck": "amb_sea", "bridge": "amb_sea", "hangar": "amb_factory", "radio": "amb_basement",
    "tent": "amb_wind", "airfield": "amb_wind", "corridor": "amb_room", "garden": "amb_wind", "parliament": "amb_crowd",
    "cell": "amb_basement", "train_interior": "amb_engine", "cockpit": "amb_engine", "room": "amb_room", "town": "amb_wind",
    "archbridge": "amb_wind", "river": "amb_wind", "polder": "amb_wind", "cabin": "amb_engine", "heath": "amb_wind", "hotel": "amb_wind",
}
# extra loop layered on top of the bed for some sets (id, gain dB)
SET_LAYER = {"radio": ("radio_static", -30), "train_interior": ("train", -22), "hangar": ("metal_clank", -26)}
# gain (dB) per id family
GAIN = {"amb": -24, "explosion": -6, "explosion_big": -4, "artillery": -6, "stamp": -8, "pop": -16, "whoosh": -16,
        "whoosh_soft": -20, "whoosh_fast": -16, "paper": -14, "typewriter": -14, "chalk": -16, "pen": -18,
        "map_draw": -20, "clock_tick": -18, "tick": -18, "impact": -8, "riser": -16, "plane_flyby": -10,
        "plane_dive": -10, "machinegun": -10, "gunshot": -10, "cannon": -8, "boom_distant": -14, "heartbeat": -12,
        "footsteps": -17, "footsteps_snow": -17, "thud": -12, "tank_engine": -16, "truck": -16, "train": -16}
LOOP_IDS = {"footsteps", "footsteps_snow", "clock_tick", "typewriter", "chalk", "pen", "map_draw", "machinegun", "plane_engine", "tank_engine", "truck", "train", "morse", "radio_static"}

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


CHUNK = SR * 30


def write(path, x, scale=1.0):
    """write a mono (or stereo) float array as 16-bit stereo WAV in 30 s chunks (long films stay within RAM)"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        for a in range(0, len(x), CHUNK):
            c = np.clip(x[a:a + CHUNK] * scale, -1, 1)
            if c.ndim == 1:
                c = np.repeat(c[:, None], 2, axis=1)
            w.writeframes((c * 32767).astype(np.int16).tobytes())


def _actor_cues(scene, el, tin):
    """Acting sounds: footsteps while an actor moves, typing/writing hands, a slam, paper on pose changes."""
    cues = []
    dur_scene = float(scene["end"]) - float(scene["start"])
    snowy = (scene.get("set") or {}).get("kind") in ("snow",) or (scene.get("set") or {}).get("weather") == "snow"
    step = "footsteps_snow" if snowy else "footsteps"
    keys = sorted(el.get("keys") or [], key=lambda k: k.get("t", 0))
    prev_t, prev_pos = tin, (el.get("x"), el.get("at"))
    for k in keys:
        pos = (k.get("x", prev_pos[0]), k.get("at", prev_pos[1]))
        if ("x" in k or "at" in k) and pos != prev_pos and k["t"] - prev_t > 0.2:
            cues.append((prev_t, step, round(k["t"] - prev_t, 2), 0))
        if "x" in k or "at" in k:
            prev_t, prev_pos = k["t"], pos
    if el.get("walk") is True or el.get("run") is True:
        cues.append((tin, step, round(dur_scene - tin, 2), 0))
    poses = [(tin, el.get("pose", "idle"))] + [(k["t"], k["pose"]) for k in keys if isinstance(k.get("pose"), str)]
    for i, (t, pose) in enumerate(poses):
        end = poses[i + 1][0] if i + 1 < len(poses) else dur_scene
        if pose == "typing":
            cues.append((t, "typewriter", round(min(6.0, end - t), 2), -5))
        elif pose == "write":
            cues.append((t, "pen", round(min(4.0, end - t), 2), -2))
        elif pose == "slam" and i > 0:
            cues.append((t + 0.15, "thud", 0, 0))
        elif i > 0 and el.get("holds") in ("paper", "telegram", "folder", "book", "letter", "ledger"):
            cues.append((t, "paper", 0, -2))
    return cues


def auto_cues(scene):
    """SFX implied by elements (only where the picture shows a contact/event)."""
    cues = []
    for el in scene.get("elements", []):
        k, tin = el.get("kind"), float(el.get("in", 0) or 0)
        if k == "actor":
            cues.extend(_actor_cues(scene, el, tin))
            continue
        if k == "vehicle" and el.get("fireAt"):
            # guns that fire on screen: artillery boom for field guns, cannon crack for tanks and ships
            sid = "artillery" if el.get("type") in ("artillery", "gun") else "cannon"
            cues.extend((float(q), sid, 0) for q in el["fireAt"])
        if k == "vehicle" and el.get("keys") and el.get("type") in ("tank", "markiv", "renault", "truck", "car", "jeep", "train", "locomotive"):
            sid = "tank_engine" if el.get("type") in ("tank", "markiv", "renault") else "train" if el.get("type") in ("train", "locomotive") else "truck"
            last = max(kk.get("t", 0) for kk in el["keys"])
            cues.append((tin, sid, round(max(0.5, last - tin), 2), 0))
            continue
        if k == "stamp":
            cues.append((tin + 0.15, "stamp", 0))
        elif k == "burst":
            cues.append((tin, "explosion_big" if (el.get("size") or 0.5) >= 0.8 else "explosion", 0))
        elif k == "fx" and el.get("type") in ("explosion", "impact", "shellburst"):
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
    return [c if len(c) == 4 else (c[0], c[1], c[2], 0) for c in cues]


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
    BLK = SR // 100  # 10 ms blocks
    nb = N // BLK
    pw = (voice[: nb * BLK].reshape(nb, BLK).astype(np.float64) ** 2).mean(1)
    env_b = np.sqrt(signal.sosfiltfilt(signal.butter(2, 3 / 50, output="sos"), pw).clip(0))
    spk_b = signal.sosfiltfilt(signal.butter(1, 1.5 / 50, output="sos"), (env_b > 0.01).astype(np.float64)).clip(0, 1).astype(np.float32)

    def speaking_at(a, b):
        """speech-presence envelope (0..1) for samples a..b, expanded from the 10 ms blocks"""
        ia = np.minimum(np.arange(a, b) // BLK, nb - 1)
        return spk_b[ia]

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
    for s in scenes:
        if s.get("type") != "stage" or s.get("ambience", "__default__") is None:
            continue
        lay = SET_LAYER.get((s.get("set") or {}).get("kind", ""))
        if not lay:
            continue
        x = load(lay[0])
        if x is None:
            continue
        a, b = int(s["start"] * SR), int(s["end"] * SR)
        seg = x[np.arange(a, b) % len(x)] * db(lay[1])
        f = min(fade, (b - a) // 2)
        w = np.ones(b - a, dtype=np.float32)
        w[:f] = np.linspace(0, 1, f)
        w[-f:] = np.linspace(1, 0, f)
        amb[a:b] += seg * w
    for a0 in range(0, N, CHUNK):  # duck beds ~5 dB under narration
        b0 = min(N, a0 + CHUNK)
        amb[a0:b0] *= 1 - 0.45 * speaking_at(a0, b0)

    # ---- SFX cues ----
    for s in scenes:
        explicit = [(float(c["t"]), c["id"], float(c.get("dur", 0) or 0), float(c.get("vol", 0) or 0), "plan") for c in s.get("sfx", [])]
        autos = [(t, i, d, float(v), "auto") for (t, i, d, v) in auto_cues(s) if not any((abs(t - e[0]) < 0.25 and (e[1] == i or e[1].split("_")[0] == i.split("_")[0])) or (e[1] == i and d > 0 and e[0] < t + d and t < e[0] + max(e[2], 0.5)) for e in explicit)]
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
    mask = spk_b > 0.5
    if mask.any():
        rms = float(np.sqrt(np.mean(env_b[mask] ** 2)))
        vg *= np.float32(0.1 / max(rms, 1e-5))
    write(out / "stems" / "voice.wav", vg)
    write(out / "stems" / "ambience.wav", amb)
    write(out / "stems" / "sfx.wav", sfx)
    sfx *= np.float32(0.9)
    peak = 0.0
    for a0 in range(0, N, CHUNK):
        peak = max(peak, float(np.max(np.abs(vg[a0:a0 + CHUNK] + amb[a0:a0 + CHUNK] + sfx[a0:a0 + CHUNK]))))
    vg += amb
    del amb
    vg += sfx
    del sfx
    raw = out / "mix_raw.wav"
    write(raw, vg, scale=1 / max(1.0, peak * 1.05))
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
    # ---- coverage report: scenes that ended up silent (no bed and no cue) or whose set has no default bed ----
    QUIET_OK = {"studio", "paper", "void", "dark", "memorial"}
    report = []
    cue_scenes = {l["scene"] for l in log}
    for s in scenes:
        kind = (s.get("set") or {}).get("kind", "")
        amb_id = s.get("ambience", "__default__")
        has_bed = (amb_id not in (None, "__default__")) or (amb_id == "__default__" and s.get("type") == "stage" and kind in SET_AMB)
        if s.get("type") == "stage" and amb_id == "__default__" and kind and kind not in SET_AMB and kind not in QUIET_OK:
            report.append(f"{s['id']}: set '{kind}' has no default ambience - add scene.ambience or map it in SET_AMB")
        if not has_bed and s["id"] not in cue_scenes and s.get("type") == "stage" and kind not in QUIET_OK and amb_id is not None:
            report.append(f"{s['id']}: silent scene ({kind or s.get('type')}) - add ambience or sfx for what is visible")
    print(json.dumps({"mix": str(final), "seconds": round(N / SR, 2), "sfx_cues": len(log), "auto": sum(1 for l in log if l["source"] == "auto"), "sound_warnings": report}, ensure_ascii=False))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[a.index("--plan") + 1] if "--plan" in a else None)
