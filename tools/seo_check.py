"""Check + export the YouTube package written by the skill.

python tools/seo_check.py projects/<slug>
input  youtube/package.json:
{
  "language": "en",
  "titles": [ {"angle": "...", "title": "...", "thumb": 1, "hook": "first line spoken/seen", "why": "..."}, x3 ],
  "recommended": 1,
  "description": "... {{CHAPTERS}} ...",          # chapters are filled from the plan (scene.chapter) unless given
  "chapters": "auto" | [{"t": 0, "title": "..."}],
  "hashtags": ["#history", "#ww2", "#midway"],
  "tags": ["...", ...]
}
output out/youtube/{titles.txt, description.txt, tags.txt, hashtags.txt, chapters.txt, report.md}
"""
import json, re, sys
from pathlib import Path


def fmt(t):
    t = int(t)
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def main(proj):
    proj = Path(proj)
    pkg = json.loads((proj / "youtube" / "package.json").read_text(encoding="utf-8"))
    err, warn = [], []
    titles = pkg.get("titles", [])
    if len(titles) != 3:
        err.append(f"need exactly 3 titles, got {len(titles)}")
    for i, t in enumerate(titles, 1):
        s = t.get("title", "")
        if len(s) > 100:
            err.append(f"title {i} > 100 chars")
        elif len(s) > 70:
            warn.append(f"title {i} is {len(s)} chars — may truncate on mobile (aim 40–65)")
        if re.search(r"[<>]", s):
            err.append(f"title {i} contains < or > (YouTube rejects them)")
        caps = [w for w in re.findall(r"[A-ZÀ-Ỹ]{3,}", s) if w not in ("WW2", "WWII", "WWI", "USSR", "USA", "UK", "NATO")]
        if len(caps) > 2:
            warn.append(f"title {i}: {len(caps)} ALL-CAPS words — channel style uses one")
    # chapters
    ch = pkg.get("chapters", "auto")
    if ch == "auto":
        plan = json.loads((proj / "work" / "plan.merged.json").read_text(encoding="utf-8"))
        ch = [{"t": s["start"], "title": s.get("chapter") or s.get("title")} for s in plan["scenes"] if s.get("chapter") or s.get("type") == "chapter"]
        if ch and ch[0]["t"] > 0.5:
            first = plan["scenes"][0]
            ch.insert(0, {"t": 0, "title": pkg.get("introChapter") or titles[pkg.get("recommended", 1) - 1]["title"]})
    if ch:
        ch[0]["t"] = 0
        for a, b in zip(ch, ch[1:]):
            if b["t"] - a["t"] < 10:
                err.append(f"chapter '{a['title']}' shorter than 10 s (YouTube ignores all chapters)")
        if len(ch) < 3:
            warn.append("fewer than 3 chapters: YouTube will not show chapters")
    chapters_txt = "\n".join(f"{fmt(c['t'])} {c['title']}" for c in ch)
    desc = pkg.get("description", "").replace("{{CHAPTERS}}", chapters_txt)
    if len(desc) > 5000:
        err.append(f"description {len(desc)} chars > 5000")
    if re.search(r"[<>]", desc):
        err.append("description contains < or > (YouTube rejects them)")
    tags = [t.strip() for t in pkg.get("tags", []) if t.strip()]
    tag_chars = sum(len(t) + (2 if " " in t else 0) for t in tags) + max(0, len(tags) - 1)
    if tag_chars > 500:
        err.append(f"tags use {tag_chars}/500 characters — drop the weakest")
    if len(tags) < 10:
        warn.append(f"only {len(tags)} tags (channel uses 20–29)")
    hs = pkg.get("hashtags", [])
    if not 2 <= len(hs) <= 5:
        warn.append(f"{len(hs)} hashtags (use 3–4; >15 makes YouTube ignore all)")
    for h in hs:
        if not re.fullmatch(r"#[\wÀ-ỹ]+", h):
            err.append(f"bad hashtag '{h}' (no spaces/punctuation)")
    if hs and not all(h in desc for h in hs):
        desc = desc.rstrip() + "\n\n" + " ".join(hs)
    out = proj / "out" / "youtube"
    out.mkdir(parents=True, exist_ok=True)
    rec = pkg.get("recommended", 1)
    (out / "titles.txt").write_text("\n".join(f"{'★ ' if i == rec else '  '}{i}. {t['title']}   [thumb {t.get('thumb', i)}]" for i, t in enumerate(titles, 1)), encoding="utf-8")
    (out / "description.txt").write_text(desc, encoding="utf-8")
    (out / "tags.txt").write_text(", ".join(tags), encoding="utf-8")
    (out / "hashtags.txt").write_text(" ".join(hs), encoding="utf-8")
    (out / "chapters.txt").write_text(chapters_txt, encoding="utf-8")
    rep = [f"# YouTube package — {proj.name}\n", "## 3 titles (angle → thumbnail)\n"]
    for i, t in enumerate(titles, 1):
        rep.append(f"{i}. {'**(recommended)** ' if i == rec else ''}**{t['title']}** — {len(t['title'])} chars  \n   angle: {t.get('angle','')}  \n   thumbnail: out/thumbs/thumb_{t.get('thumb', i)}.jpg  \n   hook: {t.get('hook','')}  \n   why: {t.get('why','')}\n")
    rep += ["\n## Description\n", "```\n" + desc + "\n```\n", f"\n## Tags ({len(tags)}, {tag_chars}/500 chars)\n", ", ".join(tags), "\n\n## Hashtags\n", " ".join(hs)]
    if err or warn:
        rep += ["\n\n## Checks\n"] + [f"- ERROR {e}" for e in err] + [f"- warn {w}" for w in warn]
    (out / "report.md").write_text("\n".join(rep), encoding="utf-8")
    print(json.dumps({"errors": err, "warnings": warn, "chapters": len(ch), "tags": len(tags), "tag_chars": tag_chars, "out": str(out)}, ensure_ascii=False, indent=1))
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main(sys.argv[1])
