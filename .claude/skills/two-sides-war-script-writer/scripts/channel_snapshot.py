"""Snapshot a YouTube channel's video list (views, duration, date) and optionally
pull English auto-subtitles of the top-N videos as timestamped plain text.

Research helper only: it never writes narration, never uploads, and its output
(transcripts) is reference material that must stay in scratch, not in the skill.

Usage:
  python scripts/channel_snapshot.py --out <scratch-dir>                 # list only
  python scripts/channel_snapshot.py --out <scratch-dir> --top 10 --subs # + transcripts
  python scripts/channel_snapshot.py --channel https://www.youtube.com/@Other/videos --out ...
Requires yt-dlp on PATH (or `python -m yt_dlp`).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

DEFAULT_CHANNEL = "https://www.youtube.com/@TwoSidesOfWar/videos"
WORD = re.compile(r"\b\w+(?:['’-]\w+)*\b", re.UNICODE)


def ytdlp_cmd():
    exe = shutil.which("yt-dlp")
    return [exe] if exe else [sys.executable, "-m", "yt_dlp"]


def run(args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    res = subprocess.run(ytdlp_cmd() + ["--no-update", "--encoding", "utf-8"] + args, capture_output=True,
                         text=True, encoding="utf-8", errors="replace", env=env)
    return res.stdout


def list_videos(channel):
    fmt = "%(id)s\t%(view_count)s\t%(duration)s\t%(upload_date)s\t%(title)s"
    out = run(["--flat-playlist", "--extractor-args", "youtubetab:approximate_date", "--print", fmt, channel])
    rows = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) != 5:
            continue
        vid, views, dur, up, title = parts
        rows.append({"id": vid, "views": int(views) if views.isdigit() else None,
                     "duration_s": int(float(dur)) if dur not in ("NA", "") else None,
                     "upload_date_approx": up if up != "NA" else None, "title": title})
    for r in rows:  # flat listing sometimes omits views; fetch those individually
        if r["views"] is None:
            one = run(["--skip-download", "--print", "%(view_count)s\t%(upload_date)s",
                       f"https://www.youtube.com/watch?v={r['id']}"]).strip().split("\t")
            if one and one[0].isdigit():
                r["views"] = int(one[0])
                if len(one) > 1 and one[1] != "NA":
                    r["upload_date_approx"] = one[1]
    return rows


def json3_to_text(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    words = []
    for ev in data.get("events", []):
        t0 = ev.get("tStartMs", 0)
        for seg in ev.get("segs") or []:
            txt = seg.get("utf8", "").replace("\n", " ")
            if txt:
                words.append((t0 + seg.get("tOffsetMs", 0), txt))
    lines, cur, start = [], [], None
    for t, w in words:
        start = t if start is None else start
        cur.append(w)
        if (t - start > 20000 and w.rstrip().endswith((".", "?", "!"))) or t - start > 35000:
            lines.append((start, "".join(cur)))
            cur, start = [], None
    if cur:
        lines.append((start, "".join(cur)))
    body = "\n".join(f"[{s // 60000:02d}:{(s // 1000) % 60:02d}] {re.sub(r'\s+', ' ', x).strip()}"
                     for s, x in lines)
    return body, len(WORD.findall(" ".join(w for _, w in words)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--channel", default=DEFAULT_CHANNEL)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--subs", action="store_true", help="download + convert subtitles of the top N")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    a.out.mkdir(parents=True, exist_ok=True)

    rows = list_videos(a.channel)
    if not rows:
        sys.exit("No videos listed (yt-dlp missing, offline, or channel URL wrong).")
    ranked = sorted(rows, key=lambda r: r["views"] or 0, reverse=True)
    snap = {"channel": a.channel, "snapshot_date": date.today().isoformat(),
            "note": "views are public counts at snapshot time; upload dates from flat listing are approximate",
            "videos": ranked}
    (a.out / "channel_snapshot.json").write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{len(rows)} videos - top {a.top} by views:")
    for i, r in enumerate(ranked[:a.top], 1):
        d = r["duration_s"] or 0
        print(f"{i:2}. {r['views'] or 0:>9,}  {d // 60:02d}:{d % 60:02d}  {r['upload_date_approx'] or '?'}  {r['title']}  [{r['id']}]")

    if a.subs:
        sub_dir, txt_dir = a.out / "subs", a.out / "txt"
        sub_dir.mkdir(exist_ok=True)
        txt_dir.mkdir(exist_ok=True)
        for r in ranked[:a.top]:
            run(["--skip-download", "--write-subs", "--write-auto-subs", "--sub-langs", "en-orig,en",
                 "--sub-format", "json3", "-o", str(sub_dir / "%(id)s.%(ext)s"),
                 f"https://www.youtube.com/watch?v={r['id']}"])
            cands = sorted(sub_dir.glob(f"{r['id']}.en-orig.json3")) or sorted(sub_dir.glob(f"{r['id']}.en*.json3"))
            if not cands:
                print(f"   no English subtitles for {r['id']}")
                continue
            body, n = json3_to_text(cands[0])
            (txt_dir / f"{r['id']}.txt").write_text(body, encoding="utf-8")
            wpm = n / (r["duration_s"] / 60) if r["duration_s"] else 0
            print(f"   {r['id']}: {n} words (ASR), ~{wpm:.0f} wpm -> txt/{r['id']}.txt")


if __name__ == "__main__":
    main()
