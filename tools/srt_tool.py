"""SRT analysis for planning.

python tools/srt_tool.py projects/<slug>
  reads   input/*.srt (+ input/voice.* if present)
  writes  work/cues.json      every cue {i,start,end,text}
          work/sentences.json cues merged into sentences/clauses with times
          work/reading.md     the full script in ~20 s blocks with timestamps (read this before planning)
          work/stats.json     duration, words, wpm, voice duration/offset, overlaps, language guess
"""
import json, re, subprocess, sys
from pathlib import Path

TS = re.compile(r"(\d+):(\d+):(\d+)[,.](\d+)")


def ts(s):
    h, m, sec, ms = TS.match(s.strip()).groups()
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms.ljust(3, "0")[:3]) / 1000


def fmt(t):
    m, s = divmod(t, 60)
    h, m = divmod(int(m), 60)
    return f"{h}:{m:02d}:{s:05.2f}" if h else f"{m}:{s:05.2f}"


def parse_srt(text):
    text = text.replace("﻿", "").replace("\r", "")
    cues = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [l for l in block.split("\n") if l.strip()]
        k = next((i for i, l in enumerate(lines) if "-->" in l), None)
        if k is None:
            continue
        a, b = lines[k].split("-->")
        body = " ".join(lines[k + 1:]).strip()
        body = re.sub(r"<[^>]+>", "", body)
        if body:
            cues.append({"i": len(cues) + 1, "start": round(ts(a), 3), "end": round(ts(b.split()[0]), 3), "text": body})
    return cues


def sentences(cues):
    out, cur = [], None
    for c in cues:
        if cur is None:
            cur = {"start": c["start"], "end": c["end"], "text": c["text"], "cues": [c["i"]]}
        else:
            cur["end"] = c["end"]
            cur["text"] += " " + c["text"]
            cur["cues"].append(c["i"])
        if re.search(r"[.!?…:;][\"'”’)]?$", c["text"]) or cur["end"] - cur["start"] > 14:
            out.append(cur)
            cur = None
    if cur:
        out.append(cur)
    return out


def probe(path):
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)], capture_output=True, text=True)
        return float(json.loads(r.stdout)["format"]["duration"])
    except Exception:
        return None


def first_sound(path):
    """seconds of leading silence in the voice file"""
    try:
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "silencedetect=n=-40dB:d=0.2", "-t", "30", "-f", "null", "-"], capture_output=True, text=True)
        m = re.search(r"silence_start: 0(?:\.0+)?\s.*?silence_end: ([\d.]+)", r.stderr, re.S)
        return float(m.group(1)) if m else 0.0
    except Exception:
        return None


def main(proj):
    proj = Path(proj)
    inp = proj / "input"
    srt = next(iter(sorted(inp.glob("*.srt"))), None)
    if not srt:
        sys.exit(f"no .srt in {inp}")
    voice = next((p for p in sorted(inp.glob("voice.*"))), None) or next((p for p in inp.iterdir() if p.suffix.lower() in (".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg")), None)
    cues = parse_srt(srt.read_text(encoding="utf-8-sig", errors="replace"))
    sents = sentences(cues)
    words = sum(len(c["text"].split()) for c in cues)
    dur = cues[-1]["end"] if cues else 0
    overlaps = [c["i"] for p, c in zip(cues, cues[1:]) if c["start"] < p["end"] - 0.05]
    vi = len(re.findall(r"[ăâđêôơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ]", " ".join(c["text"].lower() for c in cues)))
    lang = "vi" if vi > 20 else "en"
    vdur = probe(voice) if voice else None
    stats = {
        "srt": srt.name, "cues": len(cues), "sentences": len(sents), "words": words, "srt_end": dur,
        "wpm": round(words / max(1e-6, dur / 60), 1), "lang_guess": lang, "overlapping_cues": overlaps[:50],
        "voice": voice.name if voice else None, "voice_duration": vdur, "voice_leading_silence": first_sound(voice) if voice else None,
        "video_duration": round(max(dur, vdur or 0) + 1.5, 2),
    }
    work = proj / "work"
    work.mkdir(exist_ok=True)
    (work / "cues.json").write_text(json.dumps(cues, ensure_ascii=False, indent=0), encoding="utf-8")
    (work / "sentences.json").write_text(json.dumps(sents, ensure_ascii=False, indent=1), encoding="utf-8")
    lines, block_start, buf = [f"# {srt.name} — {len(cues)} cues, {words} words, {fmt(dur)}\n"], None, []
    for s in sents:
        if block_start is None:
            block_start = s["start"]
        buf.append(f"[{fmt(s['start'])}–{fmt(s['end'])}] {s['text']}")
        if s["end"] - block_start >= 20:
            lines.append("\n".join(buf) + "\n")
            buf, block_start = [], None
    if buf:
        lines.append("\n".join(buf) + "\n")
    (work / "reading.md").write_text("\n".join(lines), encoding="utf-8")
    (work / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
