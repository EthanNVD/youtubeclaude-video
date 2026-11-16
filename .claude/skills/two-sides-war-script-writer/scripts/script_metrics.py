"""Report narration length and editing cues; never edits prose or verifies facts."""
import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

WORD = re.compile(r"\b\w+(?:['’-]\w+)*\b", re.UNICODE)

def measure(text, rate=160):
    logical = text.replace("\r\n", "\n").replace("\r", "\n")
    words = WORD.findall(logical)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", logical) if p.strip()]
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", logical) if s.strip()]
    repeated = Counter(re.sub(r"\s+", " ", p).casefold() for p in paragraphs)
    warnings = []
    for label, pattern in [
        ("url", r"https?://\S+"),
        ("markdown_heading", r"(?m)^\s*#{1,6}\s+"),
        ("list_or_stage_markup", r"(?m)^\s*(?:[-*]\s+|\d+[.)]\s+|>>\s*)"),
        ("stage_direction", r"\[(?:music|screaming|snorts|pause|sfx|cut|scene|camera)[^\]]*\]"),
        ("placeholder", r"\b(?:TODO|TBD|INSERT|PLACEHOLDER)\b|<[^>]+>"),
        ("working_claim_id", r"\b[CSB]\d{2,}\b"),
        ("timestamp", r"\b\d{2}:\d{2}:\d{2}[,.]\d{3}\b"),
    ]:
        hits = list(re.finditer(pattern, logical, re.I))
        if hits:
            warnings.append({"type": label, "count": len(hits), "examples": [m.group(0) for m in hits[:5]]})
    long_sentences = [{"words": len(WORD.findall(s)), "preview": s[:180]}
                      for s in sentences if len(WORD.findall(s)) > 30]
    duplicates = [{"occurrences": n, "preview": p[:180]} for p, n in repeated.items() if n > 1]
    return {
        "words": len(words),
        "characters_logical": len(logical),
        "characters_as_decoded": len(text),
        "paragraphs": len(paragraphs),
        "sentences_approximate": len(sentences),
        "reading_rate_wpm": rate,
        "estimated_minutes": round(len(words) / rate, 2),
        "long_sentences_review": long_sentences,
        "identical_paragraphs_review": duplicates,
        "mechanical_warnings": warnings,
        "method": "Unicode word tokens with internal apostrophes/hyphens; logical chars normalize CRLF/CR to LF; includes spaces/newlines; sentence splitting approximate",
        "limits": "No history/source/semantic repetition/TTS-quality verification; review warnings in context; duration is an estimate, not measured audio",
    }

TAG = re.compile(r"^\s*([^\W\d][\w .'’-]{0,40}?)(?:\s*\[(QUOTE|REPORTED|DRAMATIZED)\])?\s*:\s*(.*)$", re.S)


def check_tagged(clean, tagged):
    """Strip speaker prefixes from the tagged twin, compare word streams, count dialogue words."""
    norm = lambda s: s.replace("\r\n", "\n").replace("\r", "\n")
    paras = [p.strip() for p in re.split(r"\n\s*\n", norm(tagged)) if p.strip()]
    stripped, untagged, speakers, kinds = [], [], Counter(), Counter()
    dialogue_words = 0
    for p in paras:
        m = TAG.match(p)
        if m and m.group(1).strip() != m.group(1).strip().upper():
            m = None  # speaker tags are upper-case; "Sir: ..." in prose is not a tag
        if not m:
            untagged.append(p[:120])
            stripped.append(p)
            continue
        who, kind, body = m.group(1).strip(), m.group(2), m.group(3).strip()
        n = len(WORD.findall(body))
        speakers[who] += n
        if who != "NARRATOR":
            dialogue_words += n
            kinds[kind or "HOST/UNLABELLED"] += n
        stripped.append(body)
    a = [w.casefold() for w in WORD.findall(norm(clean))]
    b = [w.casefold() for w in WORD.findall("\n\n".join(stripped))]
    first_diff = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), None)
    if first_diff is None and len(a) != len(b):
        first_diff = min(len(a), len(b))
    total = max(len(b), 1)
    return {
        "matches_clean_text": first_diff is None,
        "first_mismatch_word_index": first_diff,
        "clean_context": " ".join(a[first_diff:first_diff + 12]) if first_diff is not None else None,
        "tagged_context": " ".join(b[first_diff:first_diff + 12]) if first_diff is not None else None,
        "untagged_paragraphs": untagged[:5],
        "words_by_speaker": dict(speakers),
        "dialogue_words_by_kind": dict(kinds),
        "dialogue_share": round(dialogue_words / total, 3),
        "dialogue_share_review": dialogue_words / total > 0.15,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    targets = parser.add_mutually_exclusive_group()
    targets.add_argument("--target-words", type=int)
    targets.add_argument("--target-characters", type=int)
    parser.add_argument("--tolerance", type=float, default=0.05)
    parser.add_argument("--rate", type=float, default=160)
    parser.add_argument("--json", type=Path)
    parser.add_argument("--tagged", type=Path,
                        help="speaker-tagged twin file; checks it matches the clean script and reports dialogue share")
    args = parser.parse_args()
    if args.rate <= 0 or not 0 <= args.tolerance < 1:
        parser.error("rate must be positive; tolerance must be in [0, 1)")
    target = args.target_words if args.target_words is not None else args.target_characters
    if target is not None and target <= 0:
        parser.error("target must be positive")
    raw = args.path.read_bytes()
    decoded = raw.decode("utf-8-sig")
    report = {"path": str(args.path.resolve()), "sha256": hashlib.sha256(raw).hexdigest(),
              "utf8_bytes": len(raw), **measure(decoded, args.rate)}
    if target is not None:
        unit = "words" if args.target_words is not None else "characters_logical"
        low = math.ceil(target * (1 - args.tolerance))
        high = math.floor(target * (1 + args.tolerance))
        report["length_contract"] = {"unit": unit, "target": target, "minimum": low,
                                     "maximum": high, "actual": report[unit],
                                     "pass": low <= report[unit] <= high}
    if args.tagged:
        report["tagged_check"] = check_tagged(decoded, args.tagged.read_bytes().decode("utf-8-sig"))
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 2 if report.get("length_contract", {}).get("pass") is False else 0

if __name__ == "__main__":
    sys.exit(main())
