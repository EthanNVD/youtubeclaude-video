"""DEV ONLY: build a robotic guide voice from the SRT with Windows SAPI so timing can be previewed
before the real narration exists. Never ship this voice.

python tools/guide_voice.py projects/<slug>   ->  input/voice.wav
"""
import subprocess, sys, tempfile, wave, json
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from srt_tool import parse_srt  # noqa: E402

SR = 22050


def say(text, path):
    ps = (
        "Add-Type -AssemblyName System.Speech;"
        "$s=New-Object System.Speech.Synthesis.SpeechSynthesizer;"
        "$s.SelectVoice('Microsoft David Desktop');$s.Rate=1;"
        f"$s.SetOutputToWaveFile('{path}');$s.Speak([IO.File]::ReadAllText('{path}.txt'));$s.Dispose()"
    )
    Path(str(path) + ".txt").write_text(text, encoding="utf-8")
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)


def main(proj):
    proj = Path(proj)
    srt = next((proj / "input").glob("*.srt"))
    cues = parse_srt(srt.read_text(encoding="utf-8-sig"))
    total = cues[-1]["end"] + 1.0
    mix = np.zeros(int(total * SR) + SR, dtype=np.float32)
    tmp = Path(tempfile.mkdtemp())
    for c in cues:
        p = tmp / f"c{c['i']}.wav"
        say(c["text"], p)
        with wave.open(str(p)) as w:
            sr = w.getframerate()
            a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        if sr != SR:
            a = np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a)
        room = int((c["end"] - c["start"]) * SR)
        if len(a) > room:  # squeeze slightly by resampling (dev only)
            a = np.interp(np.linspace(0, len(a) - 1, room), np.arange(len(a)), a)
        s = int(c["start"] * SR)
        mix[s:s + len(a)] += a[: len(mix) - s]
    out = proj / "input" / "voice.wav"
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
    print(json.dumps({"voice": str(out), "seconds": round(len(mix) / SR, 2)}))


if __name__ == "__main__":
    main(sys.argv[1])
