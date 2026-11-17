"""Build the recipe catalog (recipes/*.md) and, with --previews, a preview still of every recipe variant.

python tools/catalog.py            write recipes/CATALOG.md, recipes/<id>.md, recipes/PEOPLE.md (no rendering)
python tools/catalog.py --previews also render recipes/img/<id>_<variant>.jpg (≈ 5 min; one render at a time!)

The recipe code (tools/cardlib/recipes_*.py) is the single source of truth: parameters, defaults, allowed values, when to use,
example cards. Run this after changing a recipe.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from cardlib import RECIPES  # noqa: E402
from cardlib.core import COMMON  # noqa: E402
from cardlib import sides as SIDES  # noqa: E402

OUT = ROOT / "recipes"
CLASS_ORDER = [("action", "Action — people and machines DOING something (most of the film)"), ("talk", "Talk — people in a place, with business (keep short)"),
               ("map", "Maps — where (≤ 5 s in battle chapters)"), ("device", "Documents, numbers, devices, titles (≤ 4-7 s)"), ("host", "The host")]
ERA_OF = {"convoy": "ww2", "bombing": "ww2", "air_battle": "ww2", "airfield": "ww2", "para_drop": "ww2", "river_crossing": "ww2"}


def phrases_in(card):
    out = []
    for k, v in card.items():
        if k == "at":
            continue
        if isinstance(v, str) and (k.endswith("_on") or k == "on"):
            out.append(v)
        elif isinstance(v, dict) and isinstance(v.get("on"), str):
            out.append(v["on"])
        elif isinstance(v, list):
            for it in v:
                if isinstance(it, dict) and isinstance(it.get("on"), str):
                    out.append(it["on"])
    return out


def preview_project():
    proj = ROOT / "projects" / "_recipes"
    if proj.exists():
        shutil.rmtree(proj)
    (proj / "cards").mkdir(parents=True)
    (proj / "work").mkdir()
    cards, words, t = [], [], 0.0
    names = []
    for rid, r in sorted(RECIPES.items()):
        for v in r.variants:
            ex = json.loads(json.dumps(r.example))
            if not ex:
                continue
            ex["variant"] = v
            ex["era"] = ex.get("era") or ERA_OF.get(rid, "ww1")
            text = f"{ex['at']} " + " ".join(phrases_in(ex)) + " and so the story went on for a while longer here"
            toks = text.split()
            # unique start: prefix with a marker word so phrases never collide between cards
            marker = f"zz{len(cards)}"
            toks = [marker] + toks
            ex["at"] = marker + " " + ex["at"]
            step = max(0.2, 6.5 / len(toks))
            for w in toks:
                words.append({"w": w, "start": round(t, 3), "end": round(t + step * 0.9, 3)})
                t += step
            t += 0.3
            cards.append(ex)
            names.append((rid, v))
    film = {"title": "Recipe previews", "lang": "en", "era": "ww1", "sides": ["german", "british"], "host_set": "station", "cast": {}}
    (proj / "cards" / "_film.json").write_text(json.dumps(film, indent=1), encoding="utf-8")
    (proj / "cards" / "ch01.json").write_text(json.dumps({"cards": cards}, indent=1, ensure_ascii=False), encoding="utf-8")
    (proj / "work" / "words.json").write_text(json.dumps(words), encoding="utf-8")
    return proj, names


def render_previews():
    proj, names = preview_project()
    r = subprocess.run([sys.executable, str(ROOT / "tools/cards.py"), str(proj)], capture_output=True, text=True, encoding="utf-8")
    rep = json.loads(r.stdout[r.stdout.index("{"):])
    if rep.get("errors"):
        print(json.dumps(rep["errors"], indent=1, ensure_ascii=False))
        sys.exit("preview cards failed — fix the recipe examples above")
    subprocess.run([sys.executable, str(ROOT / "tools/make.py"), str(proj), "review", "--at", "mid"], check=True)
    plan = json.loads((proj / "plan.json").read_text(encoding="utf-8"))
    img = OUT / "img"
    img.mkdir(parents=True, exist_ok=True)
    stills = sorted((proj / "review").glob("s*_*.jpg"))
    by_id = {}
    for f in stills:
        by_id.setdefault(f.name.split("_")[0], f)
    for s, (rid, v) in zip(plan["scenes"], names):
        f = by_id.get(s["id"])
        if f:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-vf", "scale=480:-1", str(img / f"{rid}_{v}.jpg")], check=True)
    print(f"{len(names)} previews -> {img}")


def md_param(name, p):
    t = p.type
    vals = f"one of `{'`, `'.join(str(v) for v in p.values)}`" if p.values else {"phrase": "words copied from this card's narration", "who": "cast id",
                                                                                  "side": "side name", "list": "list", "dict": "object", "bool": "true / false",
                                                                                  "int": "whole number"}.get(t, "text")
    d = "" if p.default is None else f"`{json.dumps(p.default)}`"
    return f"| `{name}` | {'**yes**' if p.required else 'no'} | {vals} | {d} | {p.doc} |"


def write_docs():
    OUT.mkdir(exist_ok=True)
    lines = ["# Recipe catalog", "",
             "Every card uses exactly one recipe. Choose the recipe from what the narration SAYS: look the sentence up in "
             "`playbook/narration-to-picture.md` first, then open the recipe's page here for its fields.", "",
             "This file is generated by `python tools/catalog.py` from the code. Do not edit it by hand.", ""]
    for cls, title in CLASS_ORDER:
        rs = [r for r in sorted(RECIPES.values(), key=lambda r: r.id) if r.cls == cls]
        if not rs:
            continue
        lines += [f"## {title}", "", "| recipe | use it when | do NOT use it when | preview |", "|---|---|---|---|"]
        for r in rs:
            pv = f"![]({'img/' + r.id + '_' + r.variants[0] + '.jpg'})" if (OUT / "img" / f"{r.id}_{r.variants[0]}.jpg").exists() else ""
            lines.append(f"| [`{r.id}`]({r.id}.md) | {r.when} | {r.not_when or '—'} | {pv} |")
        lines.append("")
    lines += ["## Fields every card can have", "", "| field | required | value | default | meaning |", "|---|---|---|---|---|"]
    lines += [md_param(k, p) for k, p in COMMON.items()]
    (OUT / "CATALOG.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    for r in RECIPES.values():
        L = [f"# `{r.id}` ({r.cls})", "", f"**Use it when:** {r.when}", "", f"**Do NOT use it when:** {r.not_when or '—'}", "",
             f"**Camera (what the compiler does, per variant):** {r.shots_doc}", "", "## Fields", "",
             "| field | required | value | default | meaning |", "|---|---|---|---|---|"]
        L += [md_param(k, p) for k, p in r.params.items()]
        L += ["", "Plus the common fields (`at`, `recipe`, `says`, `variant`, `date`, `place`, `name_card`, `label`, `counter`, `stamp`, `time`, "
              "`weather`, `tint`, …) — see [CATALOG.md](CATALOG.md#fields-every-card-can-have).", "",
              f"Variants: {', '.join(r.variants)} (leave `variant` out: the compiler rotates them so the film never repeats a composition).", "",
              "## Example card", "", "```json", json.dumps(r.example, ensure_ascii=False, indent=1), "```", ""]
        pv = [v for v in r.variants if (OUT / "img" / f"{r.id}_{v}.jpg").exists()]
        if pv:
            L += ["## Previews (middle frame of the example, each variant)", ""] + [f"Variant {v}: ![]({'img/' + r.id + '_' + v + '.jpg'})" for v in pv] + [""]
        (OUT / f"{r.id}.md").write_text("\n".join(L), encoding="utf-8")
    write_people()
    print(f"{len(RECIPES)} recipes -> {OUT}")


def write_people():
    L = ["# People: sides, uniforms, presets", "", "Generated by `python tools/catalog.py`.", "",
         "## Soldiers come from `side` + the film's `era`", "", "You never pick a uniform. A card says `\"side\": \"german\"`, and the film's era decides the rest.", ""]
    for era, t in SIDES.TABLE.items():
        if era == "modern":
            continue
        L += [f"### era `{era}`", "", "| side | soldier | officer | flag | tank | ship |", "|---|---|---|---|---|---|"]
        for s, row in t.items():
            L.append(f"| `{s}` | {row.get('soldier')} | {row.get('officer')} | {row.get('nation')} | {row.get('tank') or '—'} | {row.get('ship') or '—'} |")
        L.append("")
    L += ["## Named people (`cast` in cards/_film.json)", "",
          "Give every named person a cast id with a `preset` from this list. If someone is missing, pick the closest preset and change it, e.g. "
          "`{\"preset\": \"german_officer\", \"facial\": \"walrus\", \"glasses\": \"round\", \"age\": 0.7}`. See references/cast.md for all the look fields.", ""]
    groups = {}
    for p in sorted(SIDES.PRESETS):
        key = "WW1" if p.startswith("ww1_") or p in ("kaiser_wilhelm", "hindenburg", "ludendorff", "moltke", "schlieffen", "kluck", "falkenhayn", "scheer", "holtzendorff",
                                                      "zimmermann", "bauer", "joffre", "lanrezac", "gallieni", "foch", "jellicoe", "brusilov", "wilson", "lenin", "monash", "currie", "kaiser") else \
            "Host" if p.startswith("host") or p in ("aide", "narrator_archivist", "narrator_accountant") else \
            "Civilians" if p in ("civilian_man", "civilian_woman", "worker", "diplomat", "reporter", "dutch_civilian", "dutch_woman", "vn_peasant") else \
            "Older eras" if p in ("napoleon", "wellington", "kutuzov", "hannibal", "roman_legionary", "caesar") else "WW2 and later"
        groups.setdefault(key, []).append(p)
    for k in ("WW1", "WW2 and later", "Older eras", "Civilians", "Host"):
        L += [f"### {k}", "", ", ".join(f"`{p}`" for p in groups.get(k, [])), ""]
    (OUT / "PEOPLE.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--previews" in sys.argv:
        render_previews()
    write_docs()
