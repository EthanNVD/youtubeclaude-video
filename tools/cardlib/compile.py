"""Compile cards/*.json -> plan.json (+ checks written as instructions)."""
from __future__ import annotations

import difflib
import json
from pathlib import Path

from . import sides as SIDES
from .core import (RECIPES, Card, CardError, _where, apply_common, auto_coverage, check_card, load_cards, load_words)

TARGET = {"action": 0.40, "battle_action": 0.55, "talk": 0.15, "map": 0.15, "device": 0.15, "host": 0.08}


def _voice_file(proj: Path):
    inp = proj / "work" / "inputs.json"
    if inp.exists():
        v = json.loads(inp.read_text(encoding="utf-8")).get("voice")
        if v and (proj / v).exists():
            return v
    for ext in ("wav", "mp3", "m4a", "aac", "flac", "ogg"):
        f = proj / "input" / f"voice.{ext}"
        if f.exists():
            return f"input/voice.{ext}"
    return None


def _pick_variant(rid, history, wanted):
    vs = RECIPES[rid].variants
    if wanted and wanted != "auto":
        if wanted not in vs:
            return vs[0], f"variant \"{wanted}\" does not exist for '{rid}' (has {list(vs)}); used {vs[0]}"
        return wanted, None
    used = history.setdefault(rid, [])
    counts = {v: used.count(v) for v in vs}
    last = used[-1] if used else None
    best = sorted(vs, key=lambda v: (counts[v], v == last, vs.index(v)))[0]
    return best, None


def compile_project(proj: Path, write=True):
    proj = Path(proj)
    film, cards, chapters = load_cards(proj)
    W = load_words(proj)
    errors, warns = [], []
    for raw in cards:
        errors += check_card(raw)
    if errors:
        return {"ok": False, "errors": errors, "warnings": warns}

    # 1. resolve every card's start on the voice (in order)
    starts = []
    cursor = 0
    for k, raw in enumerate(cards):
        try:
            i, j, score = W.find(raw["at"], cursor)
        except KeyError:
            ahead = W.text(cursor, cursor + 40)
            errors.append(f"{_where(raw)}: \"at\" = \"{raw['at']}\" was not found in the narration after the previous card. "
                          f"The narration continues: \"{ahead} …\". Copy the first 3-6 words of this scene from it exactly.")
            starts.append((cursor, cursor))
            continue
        if score < 1.0:
            warns.append(f"{_where(raw)}: \"at\" matched approximately (\"{W.text(i, j + 1)}\"). Copy the words exactly to be safe.")
        if k > 0 and i <= starts[-1][0]:
            errors.append(f"{_where(raw)}: starts at or before the previous card. Cards must follow the narration in order.")
        starts.append((i, j))
        cursor = i + 1
    if errors:
        return {"ok": False, "errors": errors, "warnings": warns}
    end_time = round(W.words[-1]["end"] + 1.5, 2)
    stats = proj / "work" / "stats.json"
    if stats.exists():
        vd = json.loads(stats.read_text(encoding="utf-8")).get("voice_duration")
        if vd:
            end_time = max(end_time, round(vd + 0.6, 2))
    t_start = []
    for k, (i, _) in enumerate(starts):
        t = 0.0 if k == 0 else max(0.0, W.words[i]["start"] - 0.12)
        if k and t < t_start[-1] + 0.8:
            t = t_start[-1] + 0.8
        t_start.append(round(t, 2))

    # 2. build scenes
    history, scenes = {}, []
    cast = json.loads(json.dumps(film.get("cast", {})))
    for k, raw in enumerate(cards):
        i0 = starts[k][0]
        i1 = starts[k + 1][0] if k + 1 < len(cards) else len(W.words)
        end = t_start[k + 1] if k + 1 < len(cards) else end_time
        variant, note = _pick_variant(raw["recipe"], history, raw.get("variant"))
        if note:
            warns.append(f"{_where(raw)}: {note}")
        history.setdefault(raw["recipe"], []).append(variant)
        c = Card(raw, film, W, i0, i1, t_start[k], end, variant, k)
        try:
            s = RECIPES[raw["recipe"]].fn(c)
            s = apply_common(c, s)
        except CardError as e:
            errors.append(str(e))
            continue
        except Exception as e:  # a bug in a recipe: report it plainly
            errors.append(f"{_where(raw)}: recipe '{raw['recipe']}' failed with {type(e).__name__}: {e}. "
                          f"Check the parameter values against recipes/{raw['recipe']}.md; if they are right, report this card.")
            continue
        if raw.get("_chapter"):
            s["chapter"] = raw["_chapter"]
        s["_cls"] = raw.get("class", "action") if raw["recipe"] == "raw" else RECIPES[raw["recipe"]].cls
        s["_raw"] = raw
        scenes.append(s)
    if errors:
        return {"ok": False, "errors": errors, "warnings": warns}

    # 3. people: derived looks ("preset@variant") become cast entries; presets used directly are fine
    for s in scenes:
        for e in s.get("elements", []):
            if e.get("kind") in ("actor", "crowd") and isinstance(e.get("who"), str):
                e["who"] = SIDES.resolve_who(e["who"], cast)
    clean_cast = {cid: {k: v for k, v in spec.items() if k not in ("name", "role", "note")} for cid, spec in cast.items()}
    for cid, spec in clean_cast.items():
        if not spec.get("preset") and not spec.get("outfit"):
            errors.append(f"cards/_film.json cast \"{cid}\": add \"preset\" (a look from recipes/PEOPLE.md), e.g. \"preset\": \"german_officer\".")
        elif spec.get("preset") and spec["preset"] not in SIDES.PRESETS:
            near = difflib.get_close_matches(spec["preset"], SIDES.PRESETS, n=3)
            errors.append(f"cards/_film.json cast \"{cid}\": preset \"{spec['preset']}\" does not exist. Did you mean {near}? (recipes/PEOPLE.md)")
    if errors:
        return {"ok": False, "errors": errors, "warnings": warns}

    # 4. tile, ids, coverage safety net
    for k, s in enumerate(scenes):
        s["id"] = f"s{k + 1:03d}"
        s["end"] = scenes[k + 1]["start"] if k + 1 < len(scenes) else end_time
    auto_coverage(scenes, end_time)

    # 5. checks that need the whole film
    warns += film_checks(scenes)

    meta = {"title": film.get("title", proj.name), "lang": film.get("lang", "en"), "fps": 24, "duration": end_time, "grain": 0.5}
    v = _voice_file(proj)
    if v:
        meta["voice"] = v
    else:
        warns.append("No input/voice.*: the video will have ambience and SFX only (add the narration later in editing, or drop the voice in input/ and re-run).")
    mix = mix_of(scenes)
    for s in scenes:
        s.pop("_cls", None)
        s.pop("_raw", None)
    plan = {"meta": meta, "cast": clean_cast, "scenes": scenes}
    import layout_check  # noqa: E402
    layout_check.fix_speeds(plan)
    if write:
        (proj / "plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False), encoding="utf-8")
    return {"ok": True, "errors": [], "warnings": warns, "scenes": len(scenes), "duration": end_time, "mix": mix}


def mix_of(scenes):
    tot = {}
    T = 0.0
    for s in scenes:
        d = s["end"] - s["start"]
        tot[s["_cls"]] = tot.get(s["_cls"], 0) + d
        T += d
    return {k: round(v / max(1e-6, T), 2) for k, v in sorted(tot.items())}


def film_checks(scenes):
    w = []
    chap = []
    cur = None
    for s in scenes:
        if cur is None or s.get("chapter"):
            cur = {"title": s.get("chapter") or "(opening)", "scenes": []}
            chap.append(cur)
        cur["scenes"].append(s)
    for k in range(1, len(scenes)):
        a, b = scenes[k - 1]["_raw"], scenes[k]["_raw"]
        if a["recipe"] == b["recipe"] and RECIPES[a["recipe"]].cls != "map":
            w.append(f"{_where(b)}: same recipe '{b['recipe']}' as the card before. Two scenes in a row that look alike feel like a loop: "
                     f"show the NEXT thing (the consequence, the other side, a close detail). See playbook/narration-to-picture.md.")
    for c in chap:
        n = len(c["scenes"])
        dur = sum(s["end"] - s["start"] for s in c["scenes"])
        counts = {}
        for s in c["scenes"]:
            counts[s["_raw"]["recipe"]] = counts.get(s["_raw"]["recipe"], 0) + 1
        for rid, m in counts.items():
            if n >= 6 and m / n > 0.3 and RECIPES[rid].cls != "map":
                w.append(f"chapter '{c['title']}': recipe '{rid}' is used {m} times in {n} cards. Use at most ~30 % per recipe; pick other recipes for some of them.")
        shares = mix_of(c["scenes"])
        battle = sum(1 for s in c["scenes"] if s["_raw"]["recipe"] in BATTLE) >= max(2, n // 4)
        need = TARGET["battle_action"] if battle else TARGET["action"]
        if dur >= 45 and shares.get("action", 0) < need - 0.05:
            w.append(f"chapter '{c['title']}': action is {shares.get('action', 0):.0%} of the time (target ≥ {need:.0%}{', battle chapter' if battle else ''}). "
                     f"Turn talk/document/chart/map cards into action recipes (playbook/narration-to-picture.md §More action).")
        for cls in ("talk", "map", "device"):
            if dur >= 45 and shares.get(cls, 0) > TARGET[cls] + 0.07:
                w.append(f"chapter '{c['title']}': {cls} is {shares[cls]:.0%} of the time (keep ≤ {TARGET[cls]:.0%}).")
    for s in scenes:
        raw = s["_raw"]
        d = s["end"] - s["start"]
        if d < 1.8:
            w.append(f"{_where(raw)}: only {d:.1f} s long. Merge it with the card before or after (scenes under 2 s flash by).")
        if d > 12 and RECIPES[raw["recipe"]].cls != "host":
            w.append(f"{_where(raw)}: {d:.1f} s long. Split it into 2-3 cards at sentence starts (one idea per card, 3-10 s).")
        says = raw.get("says", "")
        if says and difflib.SequenceMatcher(None, says.lower(), s["beat"].lower()[:len(says) + 20]).ratio() > 0.8:
            w.append(f"{_where(raw)}: \"says\" copies the narration. Write what it MEANS (who does what, why it matters) in your own words.")
    return w


BATTLE = {"assault", "wave", "under_fire", "gun_crew", "mg_nest", "hit", "stretcher", "aftermath", "tank_attack", "retreat", "surrender",
          "naval_battle", "sinking", "air_battle", "bombing", "submarine_attack", "river_crossing", "para_drop"}
