"""Step 1 — prepare the inputs, whatever the user gave.

python tools/prepare.py projects/<slug> [--align] [--lang en]

Accepted inputs in projects/<slug>/input/ (any of these):
  - an .srt only                 -> the video is timed to the SRT (no narration in the mix; add the voice later)
  - a voice file only            -> the voice is transcribed to input/script.srt (faster-whisper); if input/script.txt
                                    exists (the text that was read), names and numbers are aligned to it
  - an .srt + a voice file       -> the SRT gives the words, the voice gives the sound
Any audio file name works (it is recorded in work/inputs.json); voice.wav is the usual name.

Writes:
  work/inputs.json   which files are used
  work/words.json    every narration word with start/end seconds (what card phrases are matched against)
  work/reading.md, work/cues.json, work/sentences.json, work/stats.json (from tools/srt_tool.py)
  understanding.md   copied from templates/ if missing — fill it in (playbook/02-understand.md)
--align: with an .srt + voice, re-time every word on the voice with faster-whisper (slower, more precise cuts).
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
PY = sys.executable
AUDIO = (".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg")


def words_from_srt(srt: Path):
    from srt_tool import parse_srt
    cues = parse_srt(srt.read_text(encoding="utf-8", errors="replace"))
    out = []
    for c in cues:
        ws = c["text"].split()
        if not ws:
            continue
        weights = [len(re.sub(r"[^\w]", "", w)) + 1.5 for w in ws]
        tot = sum(weights)
        span = max(0.2, c["end"] - c["start"])
        t = c["start"]
        for w, k in zip(ws, weights):
            d = span * k / tot
            out.append({"w": w, "start": round(t, 3), "end": round(t + d * 0.92, 3)})
            t += d
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    proj = Path(sys.argv[1]).resolve()
    align = "--align" in sys.argv
    lang = sys.argv[sys.argv.index("--lang") + 1] if "--lang" in sys.argv else None
    inp = proj / "input"
    (proj / "work").mkdir(parents=True, exist_ok=True)
    srts = sorted(inp.glob("*.srt"))
    voices = sorted([p for p in inp.iterdir() if p.suffix.lower() in AUDIO and not p.name.startswith("thumb_")]) if inp.exists() else []
    voice = next((v for v in voices if v.stem == "voice"), voices[0] if voices else None)
    srt = srts[0] if srts else None
    if not srt and not voice:
        sys.exit(f"Nothing in {inp}. Put the subtitles (.srt) and/or the narration audio there, then run again.")
    if len(srts) > 1:
        print(f"note: several .srt files; using {srt.name}")

    words_f = proj / "work" / "words.json"
    if voice and (not srt or align):
        script = inp / "script.txt"
        out_srt = inp / "script.srt" if not srt else proj / "work" / "aligned.srt"
        cmd = [PY, ROOT / "tools/transcribe.py", voice, out_srt]
        if srt and align:
            from srt_tool import parse_srt  # noqa
            txt = " ".join(c["text"] for c in parse_srt(srt.read_text(encoding="utf-8", errors="replace")))
            (proj / "work" / "script_from_srt.txt").write_text(txt, encoding="utf-8")
            cmd += ["--script", proj / "work" / "script_from_srt.txt"]
        elif script.exists():
            cmd += ["--script", script]
        if lang:
            cmd += ["--lang", lang]
        print("$", " ".join(str(c) for c in cmd))
        r = subprocess.run([str(c) for c in cmd], cwd=ROOT)
        if r.returncode:
            sys.exit("transcription failed (is faster-whisper installed? pip install faster-whisper)")
        wj = Path(str(out_srt).rsplit(".", 1)[0] + ".words.json")
        shutil.copy(wj, words_f)
        if not srt:
            srt = out_srt
    else:
        words = words_from_srt(srt)
        words_f.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")

    # srt_tool reads input/*.srt and input/voice.* — make sure it sees the right ones
    if voice and voice.stem != "voice":
        target = inp / f"voice{voice.suffix.lower()}"
        if not target.exists():
            shutil.copy(voice, target)
        voice = target
    r = subprocess.run([PY, str(ROOT / "tools/srt_tool.py"), str(proj)], cwd=ROOT)
    if r.returncode:
        sys.exit(r.returncode)
    (proj / "work" / "inputs.json").write_text(json.dumps({"srt": str(srt.relative_to(proj)) if srt else None,
                                                          "voice": str(voice.relative_to(proj)).replace("\\", "/") if voice else None,
                                                          "words": "work/words.json", "aligned": bool(align)}, indent=1), encoding="utf-8")
    und = proj / "understanding.md"
    if not und.exists():
        shutil.copy(ROOT / "templates" / "understanding.md", und)
    cards = proj / "cards"
    if not cards.exists():
        cards.mkdir()
        shutil.copy(ROOT / "templates" / "cards" / "_film.json", cards / "_film.json")
    n = len(json.loads(words_f.read_text(encoding="utf-8")))
    print(json.dumps({"srt": str(srt.name) if srt else None, "voice": voice.name if voice else None, "words": n,
                      "next": "read work/reading.md completely, then fill understanding.md (playbook/02-understand.md)"}, indent=1))


if __name__ == "__main__":
    main()
