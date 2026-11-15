"""Combine review stills into labelled contact sheets for visual QA.

python tools/contact_sheet.py <review_dir> [--cols 3] [--per 9]
reads <review_dir>/index.json (from tools/render.mjs stills) -> <review_dir>/sheet_01.jpg ...
"""
import json, sys, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def font(size):
    for f in ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            pass
    return ImageFont.load_default()


def main(d, cols=3, per=9):
    d = Path(d)
    items = json.loads((d / "index.json").read_text(encoding="utf-8"))
    tw = 640
    sheets = []
    for si in range(0, len(items), per):
        chunk = items[si:si + per]
        rows = (len(chunk) + cols - 1) // cols
        th = 360
        cap = 54
        sheet = Image.new("RGB", (cols * tw, rows * (th + cap)), (24, 24, 24))
        dr = ImageDraw.Draw(sheet)
        f1, f2 = font(20), font(16)
        for i, it in enumerate(chunk):
            im = Image.open(it["file"]).convert("RGB").resize((tw, th))
            x, y = (i % cols) * tw, (i // cols) * (th + cap)
            sheet.paste(im, (x, y))
            m, s = divmod(it["t"], 60)
            dr.text((x + 8, y + th + 4), f"{it['scene']}  {int(m)}:{s:05.2f}", fill=(255, 220, 120), font=f1)
            dr.text((x + 8, y + th + 28), textwrap.shorten(it.get("beat", ""), 70), fill=(220, 220, 220), font=f2)
        out = d / f"sheet_{si // per + 1:02d}.jpg"
        sheet.save(out, quality=85)
        sheets.append(str(out))
    print("\n".join(sheets))


if __name__ == "__main__":
    a = sys.argv[1:]
    cols = int(a[a.index("--cols") + 1]) if "--cols" in a else 3
    per = int(a[a.index("--per") + 1]) if "--per" in a else 9
    main(a[0], cols, per)
