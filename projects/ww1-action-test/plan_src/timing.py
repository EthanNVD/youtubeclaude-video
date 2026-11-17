"""Phrase -> time lookup on the aligned words (work/transcript.words.json).

T("phrase")  start of the first occurrence at/after the cursor (the cursor then moves there)
E("phrase")  end of that occurrence (cursor moves to its end)
peek(...)    same without moving the cursor
Write scenes in narration order so repeated phrases ("So, did the sand run out here?") resolve to the right one.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORDS = json.loads((ROOT / "work" / "transcript.words.json").read_text(encoding="utf8"))
NORM = [re.sub(r"[^a-z0-9']", "", w["w"].lower().replace("’", "'")) for w in WORDS]
_cur = [0]
LAST = [""]


def _find(phrase, start_idx):
    toks = [re.sub(r"[^a-z0-9']", "", t.lower().replace("’", "'")) for t in phrase.split()]
    toks = [t for t in toks if t]
    n = len(toks)
    for i in range(start_idx, len(NORM) - n + 1):
        if NORM[i:i + n] == toks:
            return i, i + n - 1
    raise KeyError(f"phrase not found after word {start_idx}: {phrase!r}")


def T(phrase, move=True):
    i, j = _find(phrase, _cur[0])
    if move:
        _cur[0] = i
        LAST[0] = " ".join(w["w"] for w in WORDS[i:i + 14])
    return round(WORDS[i]["start"], 2)


def E(phrase, move=True):
    i, j = _find(phrase, _cur[0])
    if move:
        _cur[0] = j
    return round(WORDS[j]["end"], 2)


def peek(phrase):
    return T(phrase, move=False)


def reset(t=0.0):
    _cur[0] = next((k for k, w in enumerate(WORDS) if w["start"] >= t), 0)


END = round(WORDS[-1]["end"] + 1.2, 2)
