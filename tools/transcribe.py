"""Voice -> SRT (when the user gives only the narration).

python tools/transcribe.py <voice.wav> <out.srt> [--script script.txt] [--model small] [--lang en]

1. faster-whisper (CPU, int8) transcribes with word timestamps (cached models: small, large-v3).
2. With --script (the text that was read), the recognised words are aligned to the script words
   (difflib), so names and numbers are spelled as written, and every script word gets a time
   (words the recogniser missed are interpolated between their aligned neighbours).
3. Cues: sentence-aware, ≤ 84 characters (2 lines of ≤ 42), ≤ 6.5 s, split at punctuation first.
Writes <out.srt> and <out>.words.json (every word with start/end).
"""
import argparse
import difflib
import json
import re
import sys
import time
from pathlib import Path


def norm(w):
    w = w.lower().replace("’", "'")
    w = re.sub(r"[^a-z0-9']", "", w)
    return w


def transcribe(path, model_name, lang):
    from faster_whisper import WhisperModel
    t0 = time.time()
    model = WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=0)
    segs, info = model.transcribe(str(path), language=lang, word_timestamps=True, vad_filter=True,
                                  beam_size=1, condition_on_previous_text=False)
    words = []
    last = 0
    for s in segs:
        for w in s.words or []:
            words.append({"w": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)})
        if s.end - last > 120:
            last = s.end
            print(f"  … {s.end / 60:.1f} min transcribed ({time.time() - t0:.0f}s)", flush=True)
    print(f"transcribed {len(words)} words in {time.time() - t0:.0f}s", flush=True)
    return words


def align(script_text, asr):
    """Give every script word the time of its matching recognised word; interpolate the rest."""
    toks = re.findall(r"\S+", script_text)
    a = [norm(t) for t in toks]
    b = [norm(w["w"]) for w in asr]
    times = [None] * len(toks)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    matched = 0
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            w = asr[blk.b + k]
            times[blk.a + k] = (w["start"], w["end"])
            matched += 1
    # replaced runs of equal length: take the recogniser's times one for one
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "replace" and (i2 - i1) == (j2 - j1):
            for k in range(i2 - i1):
                times[i1 + k] = (asr[j1 + k]["start"], asr[j1 + k]["end"])
    # interpolate gaps
    n = len(toks)
    i = 0
    while i < n:
        if times[i] is None:
            j = i
            while j < n and times[j] is None:
                j += 1
            t_prev = times[i - 1][1] if i > 0 else (times[j][0] if j < n else 0.0)
            t_next = times[j][0] if j < n else t_prev + 0.35 * (j - i)
            span = max(0.0, t_next - t_prev)
            for k in range(i, j):
                s = t_prev + span * (k - i) / (j - i)
                times[k] = (round(s, 3), round(s + span / (j - i), 3))
            i = j
        else:
            i += 1
    out = [{"w": t, "start": s, "end": e} for t, (s, e) in zip(toks, times)]
    print(f"aligned {matched}/{len(toks)} script words to the recognition ({100 * matched / max(1, len(toks)):.1f} %)")
    return out


def cues_from_words(words, max_chars=84, max_dur=6.5):
    cues, cur = [], []

    def flush():
        if cur:
            cues.append({"start": cur[0]["start"], "end": cur[-1]["end"], "text": " ".join(w["w"] for w in cur)})
            cur.clear()

    for i, w in enumerate(words):
        if cur:
            text = " ".join(x["w"] for x in cur)
            gap = w["start"] - cur[-1]["end"]
            ends_sentence = re.search(r"[.!?…][\"”’)]*$", cur[-1]["w"]) is not None
            soft = re.search(r"[,;:—–][\"”’)]*$", cur[-1]["w"]) is not None
            too_long = len(text) + 1 + len(w["w"]) > max_chars or (w["end"] - cur[0]["start"]) > max_dur
            if ends_sentence or gap > 0.8 or too_long or (soft and len(text) > max_chars * 0.55):
                flush()
        cur.append(w)
    flush()
    # no overlaps, tiny gaps closed
    for a, b in zip(cues, cues[1:]):
        if a["end"] > b["start"]:
            a["end"] = b["start"]
    return cues


def wrap(text, width=42):
    if len(text) <= width:
        return text
    words = text.split()
    best, best_d = text, 1e9
    for k in range(1, len(words)):
        l1, l2 = " ".join(words[:k]), " ".join(words[k:])
        d = abs(len(l1) - len(l2)) + (100 if max(len(l1), len(l2)) > width + 4 else 0)
        if d < best_d:
            best, best_d = l1 + "\n" + l2, d
    return best


def fmt(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("voice")
    ap.add_argument("out")
    ap.add_argument("--script")
    ap.add_argument("--model", default="small")
    ap.add_argument("--lang", default="en")
    a = ap.parse_args()
    out = Path(a.out)
    cache = out.with_suffix(".asr.json")
    if cache.exists():
        asr = json.loads(cache.read_text(encoding="utf8"))
        print(f"using cached recognition {cache}")
    else:
        asr = transcribe(a.voice, a.model, a.lang)
        cache.write_text(json.dumps(asr), encoding="utf8")
    words = align(Path(a.script).read_text(encoding="utf-8-sig"), asr) if a.script else asr
    out.with_suffix(".words.json").write_text(json.dumps(words, ensure_ascii=False), encoding="utf8")
    cues = cues_from_words(words)
    out.write_text("\n\n".join(f"{i}\n{fmt(c['start'])} --> {fmt(c['end'])}\n{wrap(c['text'])}" for i, c in enumerate(cues, 1)) + "\n", encoding="utf8")
    print(json.dumps({"srt": str(out), "cues": len(cues), "words": len(words), "end": cues[-1]["end"] if cues else 0}))


if __name__ == "__main__":
    sys.exit(main())
