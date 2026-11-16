"""Small helpers to write the Market Garden plan compactly. Every scene is still designed by hand in build.py."""
import json

SCENES = []
END = 2044.72


def K(*pairs):
    """K((t, {..}), ...) -> keys list"""
    out = []
    for t, d in pairs:
        x = {"t": t}
        x.update(d)
        out.append(x)
    return out


def A(who, x, y=900, s=1.45, pose="idle", expr="neutral", keys=None, **kw):
    d = {"kind": "actor", "who": who, "x": x, "y": y, "scale": s, "pose": pose, "expr": expr}
    if keys:
        d["keys"] = keys
    d.update(kw)
    return d


def L(text, x, y, style="tag", size=44, at=0.3, **kw):
    d = {"kind": "label", "text": text, "x": x, "y": y, "style": style, "size": size, "in": at}
    d.update(kw)
    return d


def ML(text, at_ll, style="map", size=34, at=0.3, **kw):
    d = {"kind": "label", "text": text, "at": at_ll, "style": style, "size": size, "in": at}
    d.update(kw)
    return d


def ST(text, x, y, at, size=90, color=None, tilt=-8, **kw):
    d = {"kind": "stamp", "text": text, "x": x, "y": y, "in": at, "enter": "stamp", "size": size, "tilt": tilt}
    if color:
        d["color"] = color
    d.update(kw)
    return d


def NC(name, role, at=0.6, out=None):
    d = {"kind": "namecard", "name": name, "role": role, "in": at}
    if out:
        d["out"] = out
    return d


def V(typ, x, y, s=0.6, nation=None, **kw):
    d = {"kind": "vehicle", "type": typ, "x": x, "y": y, "scale": s}
    if nation:
        d["nation"] = nation
    d.update(kw)
    return d


def FX(typ, x, y, **kw):
    d = {"kind": "fx", "type": typ, "x": x, "y": y}
    d.update(kw)
    return d


def CNT(frm, to, x, y, at=0.4, suffix="", prefix="", size=110, dur=1.5, **kw):
    d = {"kind": "counter", "from": frm, "to": to, "x": x, "y": y, "in": at, "suffix": suffix, "prefix": prefix, "size": size, "dur": dur}
    d.update(kw)
    return d


def DOC(style, title, lines, x=960, y=540, w=1000, h=560, at=0.3, size=None, speed=26, stamp=None, **kw):
    d = {"kind": "document", "style": style, "title": title, "lines": lines, "x": x, "y": y, "w": w, "h": h, "in": at, "speed": speed}
    if size:
        d["size"] = size
    if stamp:
        d["stamp"] = stamp
    d.update(kw)
    return d


def HEAD(text, x=960, y=540, size=120, at=0.3, accent=None, **kw):
    d = {"kind": "headline", "text": text, "x": x, "y": y, "size": size, "in": at}
    if accent:
        d["accent"] = accent
    d.update(kw)
    return d


def PROP(item, x, y, s=1.0, at=0.0, **kw):
    d = {"kind": "prop", "item": item, "x": x, "y": y, "scale": s, "in": at}
    d.update(kw)
    return d


def scene(start, set_=None, els=(), typ="stage", **kw):
    d = {"start": round(start, 2), "type": typ, "elements": list(els)}
    if set_ is not None:
        d["set"] = set_ if isinstance(set_, dict) else {"kind": set_}
    d.update(kw)
    SCENES.append(d)
    return d


# ---------------- maps ----------------
NL_COLORS = {"Germany": "#b9b3a2", "Netherlands": "#f0d29a", "Belgium": "#d9e6c4", "France": "#d9e6c4", "Luxembourg": "#d9e6c4", "United Kingdom": "#d9e6c4"}
RIVERS = {
    "waal": [[5.20, 51.84], [5.50, 51.855], [5.70, 51.86], [5.86, 51.85], [6.00, 51.87], [6.10, 51.85]],
    "rhine": [[5.30, 51.965], [5.60, 51.975], [5.78, 51.98], [5.90, 51.976], [5.98, 51.965], [6.08, 51.90], [6.12, 51.87]],
    "maas": [[5.30, 51.80], [5.55, 51.78], [5.74, 51.766], [5.90, 51.73], [6.05, 51.68]],
    "scheldt": [[3.50, 51.44], [3.75, 51.40], [4.05, 51.39], [4.25, 51.34], [4.40, 51.24]],
}
TOWNS = {
    "Neerpelt": [5.42, 51.23], "Eindhoven": [5.48, 51.44], "Son": [5.49, 51.51], "Veghel": [5.55, 51.62], "Grave": [5.74, 51.76],
    "Nijmegen": [5.86, 51.84], "Lent": [5.865, 51.862], "Elst": [5.85, 51.92], "Arnhem": [5.91, 51.98], "Oosterbeek": [5.84, 51.99],
    "Driel": [5.81, 51.955], "Antwerp": [4.40, 51.22], "Brussels": [4.35, 50.85], "Kleve": [6.14, 51.79], "Wesel": [6.62, 51.66],
    "Groesbeek": [5.93, 51.78],
}
ROUTE = [TOWNS[t] for t in ("Neerpelt", "Eindhoven", "Son", "Veghel", "Grave", "Nijmegen", "Lent", "Elst", "Arnhem")]


def rivers(*names, at=0.0):
    return [{"kind": "line", "path": RIVERS[n], "color": "#5b8fb0", "width": 10, "in": at, "enter": "none"} for n in names]


def towns(*names, at=0.2, side="right", size=36):
    return [{"kind": "city", "name": n, "at": TOWNS[n], "side": side, "in": at, "size": size} for n in names]


def MAP(start, center, span, els, style="war", colors=None, camera=None, **kw):
    m = {"era": "1938", "center": center, "span": span, "style": style, "colors": colors or NL_COLORS}
    return scene(start, None, els, typ="map", map=m, **({"camera": camera} if camera else {}), **kw)


# ---------------- the road device ----------------
ROAD_LEN = 6000
EXITS = {
    "A1": dict(at=0.02, label="Antwerp first", sub="Sept 1944 · Montgomery", side="down", painted="allied", num="A1", reveal=362.0, paint=382.54),
    "T": dict(at=0.07, label="Seven days to plan", sub="a toll either way", side="up", painted="none", reveal=470.3, paint=None),
    "A2": dict(at=0.11, label="Two lifts on day one", sub="England · Brereton", side="up", painted="allied", num="A2", reveal=636.1, paint=637.0),
    "A3": dict(at=0.15, label="Drop near the bridge", sub="England · the planners", side="down", painted="allied", num="A3", reveal=638.5, paint=642.0),
    "A4": dict(at=0.30, label="More strength at Arnhem", sub="mid-Sept · Bedell Smith", side="up", painted="allied", num="A4", reveal=1024.9, paint=1033.0),
    "G1": dict(at=0.52, label="Blow the Grave bridge", sub="17 Sept · Grave", side="down", painted="german", num="G1", reveal=1321.1, paint=1324.6),
    "A5": dict(at=0.62, label="Nijmegen bridge, day one", sub="17 Sept · Gavin", side="up", painted="allied", num="A5", reveal=1314.0, paint=1319.98),
    "G2": dict(at=0.66, label="Blow the Nijmegen bridge", sub="20 Sept · Model", side="down", painted="german", num="G2", reveal=1797.5, paint=1799.5),
    "L": dict(at=0.71, label="Lent", sub="20 Sept, night", side="up", painted="blank", reveal=1559.6, paint=1562.6),
}
TOWN_POS = [("Belgian border", 0.04), ("Eindhoven", 0.20), ("Son", 0.25), ("Veghel", 0.38), ("Grave", 0.49), ("Nijmegen", 0.64), ("Elst", 0.80), ("Arnhem", 0.93)]


def p_for(exit_id):
    """vehicle progress that puts the exit's sign a little right of the tank"""
    return EXITS[exit_id]["at"] - 440 / ROAD_LEN


def ROAD(start, p0, p1, move=(0.3, 4.0), y=600, extra=(), vehicles=1, set_=None, show_unknown=False, **kw):
    exits = []
    for k, e in EXITS.items():
        d = {"at": e["at"], "side": e["side"]}
        if start + 8 < e["reveal"]:
            if not show_unknown:
                continue
            d["label"] = "? ? ?"
        else:
            d["label"] = e["label"]
            d["sub"] = e["sub"]
            if e["paint"] is not None:
                d["painted"] = e["painted"]
                d["paintIn"] = round(e["paint"] - start, 2)
                if e.get("num"):
                    d["num"] = e["num"]
        exits.append(d)
    road = {"kind": "road", "x": 960, "y": y, "progress": p0, "length": ROAD_LEN, "vehicle": "tank", "nation": "UK", "polder": True,
            "exits": exits, "towns": [{"at": a, "label": n} for n, a in TOWN_POS], "vehicles": vehicles, "in": 0, "enter": "none",
            "keys": [{"t": move[0], "progress": p0}, {"t": move[1], "progress": p1, "ease": "inOut"}]}
    s = set_ or {"kind": "field", "road": False, "houses": False, "poles": False, "trees": "round"}
    return scene(start, s, [road, *extra], **kw)


def LEDGER(start, allied, german, extra=(), new_at=None, **kw):
    """allied/german: list of (label, absolute time it was written)"""
    cols = [
        {"title": "Allied exits", "nation": "UK", "entries": [{"label": l, "in": round(max(-1, t - start), 2)} for l, t in allied]},
        {"title": "German exits", "nation": "GERI", "entries": [{"label": l, "in": round(max(-1, t - start), 2)} for l, t in german]},
    ]
    return scene(start, {"kind": "study", "desk": False, "portrait": False, "shelf": True}, [{"kind": "ledger", "x": 960, "y": 520, "columns": cols, "scale": 0.95, "in": 0, "enter": "fade"}, *extra], **kw)


def finish(meta, cast, path):
    SCENES.sort(key=lambda s: s["start"])
    for i, s in enumerate(SCENES):
        s["id"] = f"s{i + 1:03d}"
        s["end"] = SCENES[i + 1]["start"] if i + 1 < len(SCENES) else END
    plan = {"meta": meta, "cast": cast, "scenes": SCENES}
    json.dump(plan, open(path, "w", encoding="utf8"), indent=1, ensure_ascii=False)
    print(len(SCENES), "scenes")
