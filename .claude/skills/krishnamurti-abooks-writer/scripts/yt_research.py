#!/usr/bin/env python3
"""Lay tin hieu YouTube cho viec de xuat chu de (chi doc, khong tai video, khong dang gi).

  python -I yt_research.py channel [--filter krishna] [--url URL ...]
      -> danh sach video cua kenh (mac dinh ABooks va BBooks): luot xem, thoi luong, tieu de
  python -I yt_research.py search "krishnamurti so hai" [--n 20]
      -> ket qua tim kiem YouTube: luot xem, thoi luong, kenh, tieu de
  python -I yt_research.py meta VIDEO_ID_OR_URL [--out DIR]
      -> tieu de, mo ta, tag, chuong cua mot video (va phu de tieng Viet neu co --out)

Can yt-dlp (tren PATH hoac `python -m yt_dlp`). File tai ve la du lieu tham khao,
dat trong thu muc scratch, khong dua vao skill.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

CHANNELS = {
    "ABooks": "https://www.youtube.com/@ABookschannel/videos",
    "BBooks": "https://www.youtube.com/channel/UCyrA3QpNXjodnElVqfaVtzg/videos",
}


def ytdlp():
    exe = shutil.which("yt-dlp")
    return [exe] if exe else [sys.executable, "-m", "yt_dlp"]


def run(args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    r = subprocess.run(ytdlp() + ["--no-update", "--encoding", "utf-8"] + args, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=env)
    return r.stdout


def views(v):
    return int(v) if v and v.isdigit() else -1


def cmd_channel(a):
    urls = a.url or list(CHANNELS.values())
    fmt = "%(view_count)s\t%(duration_string)s\t%(id)s\t%(title)s"
    for u in urls:
        rows = [ln.split("\t", 3) for ln in run(["--flat-playlist", "--print", fmt, u]).splitlines()]
        rows = [r for r in rows if len(r) == 4]
        if a.filter:
            rows = [r for r in rows if a.filter.lower() in r[3].lower()]
        rows.sort(key=lambda r: -views(r[0]))
        print(f"\n## {u}  ({len(rows)} video{' khop ' + repr(a.filter) if a.filter else ''})")
        for v, d, i, t in rows[: a.top]:
            print(f"{v:>9}\t{d:>8}\t{i}\t{t}")


def cmd_search(a):
    # khong dung --flat-playlist: ket qua tim kiem phang khong co luot xem
    fmt = "%(view_count)s\t%(duration_string)s\t%(upload_date)s\t%(channel)s\t%(id)s\t%(title)s"
    out = run(["--skip-download", "--ignore-errors", "--print", fmt, f"ytsearch{a.n}:{a.query}"])
    rows = [ln.split("\t", 5) for ln in out.splitlines() if ln.count("\t") >= 5]
    rows.sort(key=lambda r: -views(r[0]))
    print(f"## ytsearch{a.n}: {a.query}  ({len(rows)} ket qua; luot xem, thoi luong, ngay dang, kenh)")
    for v, d, up, ch, i, t in rows:
        print(f"{v:>9}\t{d:>8}\t{up}\t{ch[:24]:<24}\t{i}\t{t}")


def cmd_meta(a):
    url = a.video if a.video.startswith("http") else f"https://www.youtube.com/watch?v={a.video}"
    args = ["--skip-download", "--dump-single-json", url]
    j = json.loads(run(args) or "{}")
    if not j:
        print("Khong lay duoc metadata")
        return
    print("TIEU DE:", j.get("title"), f"({len(j.get('title') or '')} ky tu)")
    print("KENH:", j.get("channel"), "| xem:", j.get("view_count"), "| thoi luong:", j.get("duration_string"),
          "| ngay:", j.get("upload_date"))
    print("TAG:", j.get("tags"))
    print("CHUONG:", [(c["start_time"], c["title"]) for c in (j.get("chapters") or [])])
    print("MO TA:\n" + (j.get("description") or ""))
    if a.out:
        os.makedirs(a.out, exist_ok=True)
        run(["--skip-download", "--write-auto-subs", "--write-subs", "--sub-langs", "vi.*,vi", "--sub-format", "vtt",
             "-o", os.path.join(a.out, "%(id)s.%(ext)s"), url])
        print("Phu de (neu co) luu o:", a.out)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("channel")
    c.add_argument("--url", action="append")
    c.add_argument("--filter")
    c.add_argument("--top", type=int, default=40)
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--n", type=int, default=20)
    m = sub.add_parser("meta")
    m.add_argument("video")
    m.add_argument("--out")
    a = ap.parse_args()
    {"channel": cmd_channel, "search": cmd_search, "meta": cmd_meta}[a.cmd](a)


if __name__ == "__main__":
    main()
