"""Reusable building blocks for plan builders (projects/<slug>/plan_src/build.py).

Two layers:
1. Element builders — A (actor), L (label), ML (map label), ST (stamp), NC (name card), V (vehicle), FX, CNT (counter),
   DOC (document), HEAD (headline), PROP, K (keys).
2. Shot templates — proven compositions that already respect the style guide (depth, slow camera, believable vehicle
   speeds, one text block per zone, reserved badge corners). Each returns ONE scene dict (start time + content; the
   end is filled in by Plan.finish()). Pass `extra=[...]` to add elements, and override anything afterwards.

    from shotlib import Plan, office_decision, convoy, map_convoy
    P = Plan(end=1834.2)
    P.add(office_decision(12.4, who="montgomery", reads="telegram", title="FROM SHAEF", react="angry"))
    P.add(convoy(18.0, "sherman", "UK", n=4, set_="polder"))
    P.finish(meta, cast, "projects/<slug>/plan.json")

Every template is a starting point: read the narration, then adjust timings to the cue words (`at=` values are
seconds from the scene start). Templates never place text in the badge corners (date/place top-left, clock
top-right, name card bottom-left).
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import layout_check  # noqa: E402


# ------------------------------------------------------------------ element builders
def K(*pairs):
    """K((t, {..}), ...) -> keys list"""
    out = []
    for t, d in pairs:
        x = {"t": t}
        x.update(d)
        out.append(x)
    return out


def _kw(d, kw):
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


def A(who, x, y=900, s=1.45, pose="idle", expr="neutral", keys=None, **kw):
    d = {"kind": "actor", "who": who, "x": x, "y": y, "scale": s, "pose": pose, "expr": expr}
    if keys:
        d["keys"] = keys
    return _kw(d, kw)


def L(text, x, y, style="tag", size=44, at=0.3, **kw):
    return _kw({"kind": "label", "text": text, "x": x, "y": y, "style": style, "size": size, "in": at}, kw)


def ML(text, at_ll, style="map", size=34, at=0.3, **kw):
    return _kw({"kind": "label", "text": text, "at": at_ll, "style": style, "size": size, "in": at}, kw)


def ST(text, x, y, at, size=90, color=None, tilt=-8, **kw):
    return _kw({"kind": "stamp", "text": text, "x": x, "y": y, "in": at, "enter": "stamp", "size": size, "tilt": tilt, "color": color}, kw)


def NC(name, role, at=0.6, out=None):
    return _kw({"kind": "namecard", "name": name, "role": role, "in": at}, {"out": out})


def V(typ, x, y, s=0.6, nation=None, **kw):
    return _kw({"kind": "vehicle", "type": typ, "x": x, "y": y, "scale": s, "nation": nation}, kw)


def FX(typ, x, y, **kw):
    return _kw({"kind": "fx", "type": typ, "x": x, "y": y}, kw)


def CNT(frm, to, x, y, at=0.4, suffix="", prefix="", size=110, dur=1.5, **kw):
    return _kw({"kind": "counter", "from": frm, "to": to, "x": x, "y": y, "in": at, "suffix": suffix, "prefix": prefix, "size": size, "dur": dur}, kw)


def DOC(style, title, lines, x=960, y=540, w=1000, h=560, at=0.3, size=None, speed=26, stamp=None, **kw):
    return _kw({"kind": "document", "style": style, "title": title, "lines": lines, "x": x, "y": y, "w": w, "h": h, "in": at, "speed": speed, "size": size, "stamp": stamp}, kw)


def HEAD(text, x=960, y=540, size=120, at=0.3, accent=None, **kw):
    return _kw({"kind": "headline", "text": text, "x": x, "y": y, "size": size, "in": at, "accent": accent}, kw)


def PROP(item, x, y, s=1.0, at=0.0, **kw):
    return _kw({"kind": "prop", "item": item, "x": x, "y": y, "scale": s, "in": at}, kw)


def CITY(name, ll, at=0.2, side="right", size=28, tag=False):
    return {"kind": "city", "name": name, "at": ll, "side": side, "in": at, "size": size, "tag": tag}


def LEGEND(items, x=40, y=860):
    """items: [(nation_key, label), ...] -> the standard bottom-left map key"""
    return {"kind": "legend", "x": x, "y": y, "hud": True, "in": 0, "enter": "fade", "items": [{"nation": n, "label": l} for n, l in items]}


def _scene(start, set_, els, typ="stage", extra=(), **kw):
    d = {"start": round(start, 2), "type": typ, "elements": list(els) + list(extra)}
    if set_ is not None:
        d["set"] = set_ if isinstance(set_, dict) else {"kind": set_}
    return _kw(d, kw)


# ------------------------------------------------------------------ shot templates (acting)
def host_talk(start, line_label=None, set_="study", aide=False, expr="smile", extra=(), **kw):
    """The narrator in his study, talking to camera; optional aide reacting. Hooks, transitions, verdicts."""
    els = [A("host", 760 if aide else 900, 930, 1.7, "talk", expr, talk=True, keys=K((2.4, {"pose": "explain"}), (4.6, {"pose": "talk2"})))]
    if aide:
        els.append(A("aide", 1250, 930, 1.55, "idle", "worried", look=-0.6, keys=K((2.0, {"pose": "chin", "expr": "neutral"}))))
    if line_label:
        els.append(L(line_label, 960, 150, "tag", 44, at=1.0))
    return _scene(start, set_, els, extra=extra, **kw)


def office_decision(start, who, reads="telegram", title=None, react="angry", set_="office", desk_text=None, stamp=None, extra=(), **kw):
    """A leader at a desk reads a message (prop in hand), then reacts on the key word (~2.6 s) and slams/points."""
    els = [
        A(who, 820, 930, 1.6, "hold", "neutral", holds=reads, holdsText=title,
          keys=K((2.6, {"pose": "slam" if react in ("angry", "rage") else "head", "expr": react}), (4.4, {"pose": "point", "expr": react}))),
    ]
    if desk_text:
        els.append(L(desk_text, 1380, 260, "tag", 40, at=1.2))
    if stamp:
        els.append(ST(stamp, 1380, 520, at=3.0))
    return _scene(start, {"kind": set_, "fg": "officedesk", "desk": False} if set_ in ("office", "study") else set_, els, extra=extra, **kw)


def two_shot(start, a, b, set_="tent", a_expr="determined", b_expr="worried", speaker="a", extra=(), **kw):
    """Conversation: A over-the-shoulder (back view, left, big) facing B (right). The speaker talks; the other reacts."""
    els = [
        A(b, 1250, 930, 1.6, "talk" if speaker == "b" else "idle", b_expr, talk=speaker == "b", keys=K((3.0, {"pose": "shrug"}))),
        A(a, 520, 1080, 2.4, "talk" if speaker == "a" else "idle", a_expr, view="back", talk=speaker == "a"),
    ]
    return _scene(start, set_, els, extra=extra, **kw)


def march(start, nation_who="british_soldier", n=4, set_="field", direction=1, extra=(), **kw):
    """A section marching with rifles shouldered across the frame (slow, believable walking speed)."""
    x0 = 200 if direction > 0 else 1720
    els = [A(nation_who, x0 - direction * i * 230, 930, 1.25, "shoulder", "determined", holds="rifle",
             keys=K((6.0, {"x": x0 - direction * i * 230 + direction * 520}))) for i in range(n)]
    return _scene(start, set_, els, extra=extra, **kw)


def convoy(start, vtype="sherman", nation="UK", n=3, set_="polder", y=700, s=0.42, direction=1, dur=6.0, crew=True, extra=(), **kw):
    """A column drives through: enters already in frame (no zip-and-stop), drive easing, spacing ~ one vehicle length.
    Distances respect VMAX; Plan.finish() also runs fix_speeds()."""
    vmax = layout_check.VMAX.get(vtype, 400) * 0.8
    travel = min(900, vmax * dur * s * 0.75)
    els = []
    for i in range(n):
        x0 = (300 - i * 260) if direction > 0 else (1620 + i * 260)
        els.append(V(vtype, x0, y, s, nation, moving=True, crew=crew and i == 0, flip=direction < 0,
                     keys=K((dur, {"x": x0 + direction * travel}))))
    return _scene(start, set_, els, extra=extra, **kw)


def river_crossing(start, nation="USA", boats=3, set_="river", fire=True, extra=(), **kw):
    """Assault boats paddled across under fire: splashes, tracer from the far bank, one boat hit late."""
    # the river set's water runs from the far bank (~y 470) to the near bank (~y 760): boats sit on it
    els = [V("assaultboat", 260 + i * 330, 730 - i * 45, 0.8 - i * 0.08, nation, keys=K((7.0, {"x": 560 + i * 330}))) for i in range(boats)]
    if fire:
        els += [FX("splash", 700 + i * 260, 640 + (i % 2) * 50, **{"in": 1.0 + i * 1.3}) for i in range(4)]
        els += [FX("tracer", 1500, 520, dir=200, **{"in": 0.6})]
    return _scene(start, {"kind": set_, "time": kw.pop("time", "day")}, els, extra=extra, **kw)


def air_drop(start, nation="UK", planes=3, set_="heath", extra=(), **kw):
    """Dakotas cross the sky (linear, slow at that height), paratroopers drift down under canopies."""
    els = [V("dakota", -300 - i * 380, 170 + i * 70, 0.42, nation, keys=K((8.0, {"x": 1500 - i * 380, "ease": "linear"}))) for i in range(planes)]
    els.append({"kind": "paras", "x": 960, "y": 460, "count": 14, "spread": 1500, "fall": 640, "pdur": 6, "in": 1.2})
    return _scene(start, set_, els, extra=extra, **kw)


# ------------------------------------------------------------------ shot templates (maps)
def map_advance(start, center, span, path, nation, towns=(), colors=None, legend=None, dur=2.4, label=None, extra=(), **kw):
    """One arrow grows along an axis of advance; towns appear before it reaches them; standard legend."""
    els = [CITY(n, ll, at=0.2) for n, ll in towns]
    els.append({"kind": "arrow", "path": path, "color": nation, "in": 0.6, "dur": dur, "width": 26})
    if label:
        els.append(ML(label, path[len(path) // 2], style="tag", at=0.6 + dur * 0.6))
    if legend:
        els.append(LEGEND(legend))
    m = {"era": kw.pop("era", "1938"), "center": center, "span": span, "style": "paper", "colors": colors or {}}
    return _scene(start, None, els, typ="map", extra=extra, map=m, **kw)


def map_convoy(start, center, span, path, icon="freighter", trail=5, nation=None, colors=None, dur=7.0, follow=True, legend=None, extra=(), **kw):
    """Movers along a dashed route (ships, crates, trucks, tanks) with the camera riding along (reference: Atlantic convoys)."""
    els = [{"kind": "route", "path": path, "color": "#3a6ea5" if icon in ("freighter", "warship") else (nation or "#4a4a4a"), "width": 5,
            "icon": icon, "trail": trail, "gap": 90, "iconSize": 1.3, "nation": nation, "enter": "draw", "dur": dur, "in": 0.3}]
    if legend:
        els.append(LEGEND(legend))
    m = {"era": kw.pop("era", "1938"), "center": center, "span": span, "style": "paper", "colors": colors or {}}
    if follow:
        m["follow"] = 0
    return _scene(start, None, els, typ="map", extra=extra, map=m, **kw)


def front_shift(start, center, span, line_from, line_to, nation, colors=None, dur=4.0, pocket=None, legend=None, extra=(), **kw):
    """A front line slides from one position to another over `dur`; optional pocket that shrinks."""
    els = [{"kind": "front", "path": line_from, "path2": line_to, "morph": 0, "keys": K((dur, {"morph": 1})), "color": nation, "enter": "none", "in": 0}]
    if pocket:
        els.append({"kind": "pocket", "polygon": pocket, "color": "red", "keys": K((dur, {"shrink": 0.6})), "enter": "fade"})
    if legend:
        els.append(LEGEND(legend))
    m = {"era": kw.pop("era", "1938"), "center": center, "span": span, "style": "paper", "colors": colors or {}, "hatch": kw.pop("hatch", None)}
    return _scene(start, None, els, typ="map", extra=extra, map={k: v for k, v in m.items() if v is not None}, **kw)


# ------------------------------------------------------------------ shot templates (devices / evidence)
def tubes(start, title, items, max_=None, unit="", extra=(), **kw):
    """Comparison as glass tubes on a wooden plaque in the workroom. items: [(label, value, nation_or_color, in_s)]"""
    its = [{"label": l, "value": v, ("nation" if len(str(c)) <= 5 and str(c).isupper() else "color"): c, "in": t} for l, v, c, t in items]
    el = {"kind": "bars", "title": title, "x": 1020, "y": 400, "width": 760, "items": its, "max": max_ or max(v for _, v, _, _ in items), "unit": unit}
    return _scene(start, {"kind": "workshop", "ground": 1000}, [el], extra=extra, **kw)


def corkboard(start, items, title=None, extra=(), **kw):
    """Timeline as pinned cards on a corkboard. items: [(date, label, at 0..1, nation_or_color, in_s)]"""
    els = [{"kind": "timeline", "x": 960, "y": 560, "width": 1500, "items": [{"sub": d, "label": l, "at": a, "color": c, "in": t} for d, l, a, c, t in items]}]
    if title:
        els.append(L(title, 960, 120, "red", 46, at=0.2))
    return _scene(start, {"kind": "workshop", "ground": 1000}, els, extra=extra, **kw)


def document_insert(start, style, title, lines, stamp=None, set_="paper", extra=(), **kw):
    """Close-up of evidence: a telegram/order/newspaper typed line by line, stamped at the end."""
    return _scene(start, set_, [DOC(style, title, lines, stamp=stamp, at=0.3)], extra=extra, **kw)


TEMPLATES = {
    "host_talk": host_talk, "office_decision": office_decision, "two_shot": two_shot, "march": march, "convoy": convoy,
    "river_crossing": river_crossing, "air_drop": air_drop, "map_advance": map_advance, "map_convoy": map_convoy,
    "front_shift": front_shift, "tubes": tubes, "corkboard": corkboard, "document_insert": document_insert,
}


# ------------------------------------------------------------------ plan assembly
class Plan:
    """Collect scenes (any order), then finish(): sort, tile the timeline, number ids, fix vehicle speeds, write JSON."""

    def __init__(self, end: float):
        self.end = end
        self.scenes: list[dict] = []

    def add(self, sc: dict) -> dict:
        self.scenes.append(sc)
        return sc

    def finish(self, meta: dict, cast: dict, path: str, letterbox: dict | None = None) -> dict:
        self.scenes.sort(key=lambda s: s["start"])
        for i, s in enumerate(self.scenes):
            s["id"] = f"s{i + 1:03d}"
            s["end"] = self.scenes[i + 1]["start"] if i + 1 < len(self.scenes) else self.end
            if letterbox and s["id"] in letterbox:
                s["letterbox"] = letterbox[s["id"]]
        plan = {"meta": meta, "cast": cast, "scenes": self.scenes}
        n = layout_check.fix_speeds(plan)
        with open(path, "w", encoding="utf8") as f:
            json.dump(plan, f, indent=1, ensure_ascii=False)
        print(f"{len(self.scenes)} scenes, {n} speed fixes -> {path}")
        return plan
