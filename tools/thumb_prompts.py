"""Build detailed image-model prompts for the 3 YouTube thumbnails.

    python tools/thumb_prompts.py projects/<slug>

Input : projects/<slug>/youtube/thumb_prompts.json  (written by Claude, schema in
        .claude/skills/srt-history-video/references/thumbnails.md)
Output: projects/<slug>/out/youtube/thumb_prompts.md       (all prompts, ready to paste)
        projects/<slug>/out/youtube/prompts/thumb_N_<model>.txt
        projects/<slug>/work/thumb_refs.json             (characters to render as reference sheets)

Every prompt is assembled from the same blocks so nothing is forgotten:
STYLE (fixed, distilled from the reference channel's 32 thumbnails) · LAYOUT · CHARACTERS (appearance from the
engine presets + expression + pose + placement) · SCENE (background / midground / symbols / labels) ·
HEADLINE TEXT (exact words, colours, font, position) · LIGHT & COLOUR · AVOID.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- fixed style (from the 32 reference thumbnails)
STYLE = (
    "Bold, high-contrast cartoon illustration made for a YouTube thumbnail of a military-history channel. "
    "Polished digital comic art: thick clean black outlines, smooth cel shading with soft painted gradients and "
    "subtle texture, rich saturated colours, crisp detail, slight dark vignette at the corners. "
    "Characters are stylized chibi caricatures: very large round heads (about half of the body height) sitting "
    "directly on small bodies with no visible neck, simple dot or almond eyes, big readable expressions, "
    "recognisable by their hair, moustache, hat, glasses and uniform. Hands are cartoon hands with clear fingers. "
    "Everything must read in one second at phone size: one idea, few big shapes, strong silhouettes, "
    "faces large and unobstructed."
)
AVOID = [
    "swastikas or any Nazi/extremist insignia (use a plain red armband with no symbol)",
    "gore, blood, corpses",
    "photorealism or real photographs",
    "watermarks, logos, signatures, channel names, UI elements, borders or frames",
    "any text other than the headline and labels listed",
    "misspelled or garbled letters",
    "extra fingers or deformed hands",
    "cluttered small details in the headline area",
    "faces covered by text or objects",
]

NAT = {
    "GER": "German", "GERI": "Imperial German", "USSR": "Soviet", "RUS": "Russian", "USA": "American", "UK": "British",
    "JPN": "Japanese", "FRA": "French", "ITA": "Italian", "POL": "Polish", "CHN": "Chinese", "FIN": "Finnish",
    "ROM": "Romanian", "HUN": "Hungarian", "NED": "Dutch", "BEL": "Belgian", "AUS": "Austro-Hungarian", "OTT": "Ottoman",
    "VN": "Vietnamese", "SPQR": "Roman", "CARTH": "Carthaginian",
}
OUTFIT = {
    "tunic": "{nat}military tunic{col} with pockets, buttons and a belt",
    "navy": "dark navy-blue double-breasted naval uniform with gold buttons",
    "navywhite": "white naval dress uniform with gold buttons and shoulder boards",
    "suit": "three-piece suit{col} with a white shirt",
    "coat": "long {nat}military greatcoat{col}",
    "sailor": "sailor's jumper with a square navy collar",
    "civil": "plain civilian shirt and trousers{col}",
    "party": "brown party-style uniform jacket with a tie",
    "pilot": "leather flight jacket{col}",
    "robe": "dressing gown / smoking jacket{col}",
    "tweed": "brown tweed jacket over a mustard knitted vest, white shirt and blue tie",
    "armor": "ancient bronze armour",
    "dress": "1940s dress{col}",
}
HAT = {
    "peaked": "peaked officer's cap", "navy": "black naval peaked cap with a gold anchor badge",
    "navy_white": "white-topped naval peaked cap with a black band and gold badge", "garrison": "side cap",
    "helmet_de": "German-style steel helmet (no insignia)", "helmet_us": "US M1 steel helmet", "helmet_uk": "flat British Brodie helmet",
    "helmet_su": "Soviet steel helmet with a small red star", "helmet_jp": "Japanese army helmet with a small star",
    "beret": "beret", "bicorne": "black bicorne hat", "kepi": "French kepi", "ushanka": "fur ushanka hat", "fedora": "fedora",
    "tophat": "top hat", "pith": "pith helmet", "sailor": "white sailor cap", "pilot": "leather flying helmet with goggles",
    "roman": "Roman helmet with a red crest", "crown": "golden crown", "conical": "conical straw hat", "flatcap": "flat cap",
    "pith_vn": "olive pith helmet with a star",
}
HAIR = {
    "side": "dark hair with a heavy side-swept fringe", "back": "hair combed straight back", "bald": "completely bald head",
    "baldtop": "bald on top with tufts of hair at the sides", "short": "short hair", "part": "neatly side-parted hair",
    "curly": "curly hair", "bun": "hair in a bun", "long": "long hair", "messy": "messy spiky hair",
    "tousled": "tousled brown mop of hair with a cowlick",
}
FACIAL = {
    "toothbrush": "small square toothbrush moustache", "walrus": "big bushy walrus moustache", "pencil": "thin pencil moustache",
    "handlebar": "curled handlebar moustache", "beard": "full beard", "goatee": "goatee", "stubble": "stubble",
}
GLASSES = {"round": "round wire-rimmed glasses", "pince": "pince-nez glasses", "sun": "dark sunglasses"}
EXTRA = {
    "cigar": "a fat cigar in the mouth", "pipe": "a pipe", "medals": "a row of medals", "bowtie": "a bow tie",
    "scarf": "a long red scarf", "epaulettes": "gold epaulettes", "thickbrows": "thick bushy eyebrows", "jowls": "heavy jowls",
    "armband": "a plain red armband with no symbol", "monocle": "a monocle", "cigarette": "a cigarette",
}
EXPR = {
    "panic": "panicking — eyes wide open with tiny pupils, mouth open in a scream, big blue sweat drops flying off the head",
    "cry": "crying — eyes squeezed shut, streams of tears, wobbly open mouth, sweat drops",
    "sad": "sad — droopy eyes, downturned mouth, a single tear",
    "smug": "smug — half-closed eyes, one eyebrow raised, confident smirk",
    "angry": "furious — deeply furrowed brows, gritted teeth, red-tinted face, a little anger vein",
    "determined": "determined — narrowed eyes, firm straight mouth, chin forward",
    "worried": "worried — raised inner eyebrows, nervous side glance, one big sweat drop",
    "shocked": "shocked — huge round eyes, mouth wide open",
    "grin": "forcing a nervous grin with clenched teeth while sweating heavily",
    "happy": "beaming — closed happy eyes, big open smile",
    "thinking": "thinking — one eyebrow raised, eyes looking up and aside",
    "neutral": "calm, neutral",
    "tired": "exhausted — heavy eyelids, bags under the eyes",
}
POSE = {
    "head": "both hands clutching the sides of the head",
    "cross": "arms firmly folded across the chest",
    "point": "pointing a finger sideways toward {target}",
    "pointUp": "pointing up at {target}",
    "pointSelf": "pointing at himself",
    "show": "holding {prop} up beside the face toward the viewer",
    "hold": "holding {prop} in both hands in front of the chest",
    "holdUp": "raising {prop} high above the head",
    "chin": "hand on the chin, thinking",
    "shrug": "shrugging with both palms up",
    "salute": "saluting",
    "binoculars": "looking through binoculars",
    "fist": "both fists clenched in front of the chest",
    "cheer": "both fists raised in triumph",
    "present": "presenting {target} with an open palm",
    "wipe": "wiping sweat from the forehead",
    "face": "both hands over the cheeks in horror",
    "stop": "holding one palm out toward the viewer: stop",
    "idle": "arms relaxed",
}
COLORS = {
    "#2a3550": "dark navy", "#3b3a3f": "charcoal grey", "#2f3036": "dark charcoal", "#6e6a58": "field grey",
    "#8c8a66": "olive khaki", "#9aa3a8": "pale blue-grey", "#3a3a3a": "black", "#2a2a2a": "black", "#b7a77c": "light khaki",
    "#55575c": "slate grey", "#5a4636": "brown", "#3f5a4a": "dark green", "#8e2c2a": "dark red", "#7b5a3c": "brown tweed",
    "#eceee9": "white winter", "#f0f2ef": "white winter", "#7f97b8": "horizon blue", "#6b5a46": "brown", "#2d2d2d": "black",
}
LAYOUT = {
    "hero": ("Hero composition: ONE character as a huge bust (head and upper chest) on the {side} 40% of the frame, head about "
             "45–55% of the frame height, cut off by the bottom edge, body turned three-quarters toward the centre. "
             "The rest of the frame shows the story behind him: {background}."),
    "versus": ("Face-off composition: two characters as large busts at the far left and far right edges, cropped by the frame "
               "edges and the bottom, heads about 40–50% of the frame height, turned toward each other. Between them, in "
               "the centre: {middle}. Behind everything: {background}."),
    "split": ("Before/after split screen: two equal panels side by side separated by a clean vertical white line with a thin "
              "black edge. Each panel is its own scene (described below). The SAME character appears in both panels so the "
              "change is obvious."),
    "split_diagonal": ("Before/after split screen: two panels separated by a slightly diagonal white line with a thin black edge "
                       "(top of the line a little right of centre, bottom a little left). Each panel is its own scene (described below). "
                       "The SAME character appears in both panels so the change is obvious."),
    "triptych": ("Three equal vertical panels separated by white lines, one bust per panel, each panel with its own "
                 "saturated background colour and a big number at the top."),
    "center": ("Symmetric composition: the character centred as a large bust, framed on both sides by {middle}. "
               "Background: {background}."),
    "object": ("Object composition: a giant symbolic object dominates the frame ({middle}), with {background}. "
               "Characters, if any, react to it from the side."),
}
TEXT_POS = {
    "top": "across the top of the frame",
    "bottom": "across the bottom of the frame",
    "top-left": "in the top-left area",
    "top-right": "in the top-right area",
    "center": "across the middle of the frame",
}
ACC = {"yellow": "bright yellow (#FFD21F)", "red": "bright red (#E5322D)", "white": "white", "blue": "icy light blue (#8FD3FF)"}
FONT = {
    "condensed": "ultra-bold condensed sans-serif in capitals (like Anton / Impact)",
    "rounded": "chunky rounded heavy display font in capitals (like Luckiest Guy / Lilita One)",
}


def load_presets() -> dict[str, dict]:
    src = (ROOT / "src/char/presets.ts").read_text(encoding="utf-8")
    out: dict[str, dict] = {}
    for m in re.finditer(r"^\s{2}(\w+): \{(.*)\},?\s*(?://.*)?$", src, re.M):
        body = m.group(2)
        d: dict = {}
        for k, v in re.findall(r"(\w+):\s*('(?:[^']*)'|\[[^\]]*\]|[\d.]+|true|false)", body):
            if v.startswith("'"):
                d[k] = v.strip("'")
            elif v.startswith("["):
                d[k] = re.findall(r"'([^']*)'", v)
            elif v in ("true", "false"):
                d[k] = v == "true"
            else:
                d[k] = float(v)
        out[m.group(1)] = d
    return out


def color_name(hexv: str | None) -> str:
    if not hexv:
        return ""
    return COLORS.get(hexv.lower(), "")


def describe(spec: dict) -> str:
    nat = NAT.get(spec.get("nation", ""), "")
    natw = (nat + " ") if nat else ""
    cn = color_name(spec.get("color"))
    outfit = OUTFIT.get(spec.get("outfit", "tunic"), "{nat}uniform{col}").format(nat=natw, col=(" in " + cn) if cn else "")
    parts = [outfit]
    if spec.get("hat") and spec["hat"] != "none":
        parts.append(HAT.get(spec["hat"], spec["hat"]))
    if spec.get("hair") and spec["hair"] != "none" and not (spec.get("hat") and spec["hat"] not in ("none", "beret", "garrison")):
        parts.append(HAIR.get(spec["hair"], spec["hair"]))
    if spec.get("facial") and spec["facial"] != "none":
        parts.append(FACIAL.get(spec["facial"], spec["facial"]))
    if spec.get("glasses") and spec["glasses"] != "none":
        parts.append(GLASSES.get(spec["glasses"], spec["glasses"]))
    for x in spec.get("extra", []):
        if x in EXTRA:
            parts.append(EXTRA[x])
    age = spec.get("age", 0.4)
    agew = "young" if age < 0.3 else "middle-aged" if age < 0.62 else "elderly, grey-haired"
    b = spec.get("build", 1)
    build = " stout," if b > 1.12 else " thin," if b < 0.9 else ""
    return f"{agew},{build} wearing " + ", ".join(parts)


def char_block(c: dict, presets: dict, cast: dict) -> str:
    who = c.get("who", "")
    spec = {}
    if who in cast:
        base = presets.get(cast[who].get("preset", who), {})
        spec = {**base, **{k: v for k, v in cast[who].items() if k not in ("preset", "name")}}
    elif who in presets:
        spec = presets[who]
    name = c.get("name") or who.replace("_", " ").title()
    look = c.get("look") or (describe(spec) if spec else "")
    expr = EXPR.get(c.get("expr", ""), c.get("expr", ""))
    pose = POSE.get(c.get("pose", ""), c.get("pose", "")).format(prop=c.get("prop", "the object"), target=c.get("target", "the key element"))
    s = f"{name} (cartoon caricature): {look}." if look else f"{name} (cartoon caricature)."
    if c.get("position"):
        s += f" Placement: {c['position']}."
    if expr:
        s += f" Expression: {expr}."
    if pose:
        s += f" Pose: {pose}."
    if c.get("prop") and "{prop}" not in POSE.get(c.get("pose", ""), ""):
        s += f" Holding: {c['prop']}."
    if c.get("extra"):
        s += f" {c['extra']}"
    return s


def text_block(tb: dict) -> tuple[str, list[str]]:
    lines = tb.get("lines", [])
    pos = TEXT_POS.get(tb.get("position", "top"), tb.get("position", "top"))
    font = FONT.get(tb.get("font", "condensed"), tb.get("font"))
    exact: list[str] = []
    desc = []
    for i, ln in enumerate(lines):
        t = ln["text"]
        exact.append(t)
        acc = ln.get("accent", [])
        acol = ACC.get(ln.get("accentColor", "yellow"), ln.get("accentColor", "yellow"))
        base = ACC.get(ln.get("color", "white"), ln.get("color", "white"))
        colour = f"{base} letters" + (f", with the word(s) {', '.join(repr(a) for a in acc)} in {acol}" if acc else "")
        size = ln.get("size", "very large — cap height about 22–28% of the frame height" if i == 0 else "smaller, about 60% of the first line")
        desc.append(f'Line {i + 1}: "{t}" — {colour}; {size}.')
    s = (f"HEADLINE TEXT {pos}, spelled exactly as written (capital letters, keep punctuation): "
         + " ".join(desc)
         + f" Font: {font}. Every letter has a thick black outline (about 1/6 of the letter height) and a soft dark drop shadow; "
           "the headline spans about 80–95% of the frame width, slightly tilted (−2°) for energy, and never covers a face.")
    if tb.get("plate"):
        s += f" The headline sits on a {tb['plate']}."
    return s, exact


def build(thumb: dict, idx: int, presets: dict, cast: dict) -> dict:
    layout = thumb.get("layout", "hero")
    lay = LAYOUT.get(layout, layout).format(side=thumb.get("heroSide", "right"), background=thumb.get("background", "the story scene"),
                                            middle=thumb.get("middle", "the key symbol of the story"))
    chars = [char_block(c, presets, cast) for c in thumb.get("characters", [])]
    panels = []
    for j, p in enumerate(thumb.get("panels", [])):
        pc = [char_block(c, presets, cast) for c in p.get("characters", [])]
        side = ["LEFT", "RIGHT", "MIDDLE"][j] if len(thumb.get("panels", [])) < 3 else ["LEFT", "MIDDLE", "RIGHT"][j]
        tag = f' A black rectangular tag with bold white capital text "{p["tag"]}" in its top {"left" if j == 0 else "right"} corner.' if p.get("tag") else ""
        panels.append(f"{side} PANEL — {p.get('scene', '')}.{tag} " + " ".join(pc))
    scene = []
    if thumb.get("background") and layout not in ("hero", "versus", "center", "object"):
        scene.append(f"Background: {thumb['background']}.")
    if thumb.get("symbols"):
        scene.append("Story symbols (big and simple): " + "; ".join(thumb["symbols"]) + ".")
    if thumb.get("labels"):
        scene.append("Small labels (the only other text allowed): " + "; ".join(
            f'"{l["text"]}" as {l.get("style", "a white rounded box with bold black capital text and a black outline")}' + (f" {l['where']}" if l.get("where") else "")
            for l in thumb["labels"]) + ".")
    light = thumb.get("light", "dramatic light from the side, a soft glow behind the main character to separate it from the background")
    palette = thumb.get("palette", "saturated complementary colours (warm reds/oranges against blues), whites kept clean")
    tb, exact = text_block(thumb.get("text", {"lines": []}))
    avoid = AVOID + thumb.get("avoid", [])

    full = "\n\n".join(x for x in [
        f"16:9 YouTube thumbnail, 1280×720. {STYLE}",
        "LAYOUT: " + lay,
        ("CHARACTERS: " + " ".join(chars)) if chars else "",
        "\n".join(panels),
        "SCENE: " + " ".join(scene) if scene else "",
        tb,
        f"LIGHT & COLOUR: {light}. Palette: {palette}.",
        "AVOID: " + "; ".join(avoid) + ".",
    ] if x)
    clean = "\n\n".join(x for x in [
        f"16:9 YouTube thumbnail background art, 1280×720. {STYLE}",
        "LAYOUT: " + lay,
        ("CHARACTERS: " + " ".join(chars)) if chars else "",
        "\n".join(panels),
        "SCENE: " + " ".join(s for s in scene if not s.startswith("Small labels")) if scene else "",
        f"Keep the space {TEXT_POS.get(thumb.get('text', {}).get('position', 'top'), 'at the top')} (about 30% of the frame height) "
        "simple and uncluttered (sky, map or smooth background) — a headline will be added there later. "
        "Do NOT draw any text, letters, numbers or labels anywhere.",
        f"LIGHT & COLOUR: {light}. Palette: {palette}.",
        "AVOID: " + "; ".join(AVOID[:-3] + ["any text, letters or numbers"]) + ".",
    ] if x)
    # Midjourney: compact single paragraph + params (MJ draws text poorly: keep the words short, quoted)
    mj_chars = " ".join(chars)[:900]
    mj = (f"bold cartoon YouTube thumbnail, thick black outlines, cel shading, saturated colours, chibi caricatures with huge round heads, "
          f"{lay} {mj_chars} {' '.join(panels)[:600]} {' '.join(scene)[:400]} "
          f"big headline text \"{' / '.join(exact)}\" in heavy white capitals with black outline "
          f"--ar 16:9 --v 7 --style raw --s 150 --no swastika, gore, photo, watermark, logo, extra text")
    return {"full": full, "clean": clean, "midjourney": mj, "exact": exact}


def main():
    proj = Path(sys.argv[1]).resolve()
    src = proj / "youtube" / "thumb_prompts.json"
    if not src.exists():
        print(f"missing {src} — write it first (see references/thumbnails.md)")
        sys.exit(1)
    data = json.loads(src.read_text(encoding="utf-8"))
    presets = load_presets()
    cast = {}
    for name in ("plan.json", "plan/_meta.json"):
        f = proj / name
        if f.exists():
            cast = json.loads(f.read_text(encoding="utf-8")).get("cast", {})
            break
    thumbs = data.get("thumbs", [])
    warn = []
    if len(thumbs) != 3:
        warn.append(f"expected 3 thumbnails, got {len(thumbs)}")
    out = proj / "out" / "youtube"
    (out / "prompts").mkdir(parents=True, exist_ok=True)
    md = [f"# Thumbnail prompts — {proj.name}\n",
          "Paste a prompt into the image model. **ChatGPT / Gemini / Ideogram** render text well → use *Full prompt*. "
          "**Midjourney / Flux** often misspell → use *Clean plate*, then add the headline with "
          "`python tools/make.py projects/<slug> thumbs` (put the image in `input/thumb_N.png`).\n",
          "For consistent characters, attach the reference sheet `out/thumbs/ref_characters.png` to the model "
          "(\"use these characters' designs\").\n"]
    refs = set()
    for i, th in enumerate(thumbs, 1):
        r = build(th, i, presets, cast)
        words = sum(len(x.split()) for x in r["exact"])
        if words > 5:
            warn.append(f"thumb {i}: headline has {words} words (reference median 3, max 4–5)")
        if not r["exact"]:
            warn.append(f"thumb {i}: no headline text")
        for c in th.get("characters", []) + [c for p in th.get("panels", []) for c in p.get("characters", [])]:
            if c.get("who"):
                refs.add(c["who"])
        for k in ("full", "clean", "midjourney"):
            (out / "prompts" / f"thumb_{i}_{k}.txt").write_text(r[k], encoding="utf-8")
        md.append(f"\n---\n\n## Thumbnail {i} — {th.get('angle', '')}\n")
        md.append(f"- Title it goes with: **{th.get('title', '')}**\n- Layout: `{th.get('layout', 'hero')}` · Headline: **{' / '.join(r['exact'])}**\n")
        md.append(f"\n### Full prompt (ChatGPT · Gemini · Ideogram · Flux)\n\n```text\n{r['full']}\n```\n")
        md.append(f"\n### Clean plate (no text — headline added by `make.py thumbs`)\n\n```text\n{r['clean']}\n```\n")
        md.append(f"\n### Midjourney v7\n\n```text\n{r['midjourney']}\n```\n")
        if th.get("fix_tips"):
            md.append("\n**If the result is off:** " + " ".join(th["fix_tips"]) + "\n")
    md.append("\n---\n\n## Checklist before choosing\n\n"
              "1. Look at it at 25 % size (phone): emotion, headline and the one symbol readable in one second?\n"
              "2. Headline spelled exactly? Face not covered? No extra text / no hate symbols?\n"
              "3. Does the image add the twist the title does not say (title asks, thumbnail answers or provokes)?\n"
              "4. Three thumbnails = three different angles (not three versions of the same picture).\n")
    if warn:
        md.append("\n## Warnings\n\n" + "\n".join(f"- {w}" for w in warn) + "\n")
    (out / "thumb_prompts.md").write_text("\n".join(md), encoding="utf-8")
    (proj / "work").mkdir(exist_ok=True)
    (proj / "work" / "thumb_refs.json").write_text(json.dumps(sorted(refs)), encoding="utf-8")
    print(json.dumps({"prompts": str(out / "thumb_prompts.md"), "characters": sorted(refs), "warnings": warn}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
