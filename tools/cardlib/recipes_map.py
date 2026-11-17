"""Maps: movement arrows, front lines, routes, locating places. Places are given BY NAME (data/places.json, or
cards/_film.json "places"); the compiler computes coordinates, map centre and zoom, colours the countries of the sides
involved and adds the legend. Maps stay short (≤ 5 s in battle chapters, ≤ 8 s otherwise) — see playbook."""
from __future__ import annotations

import json
from pathlib import Path

from shotlib import K

from . import sides as SIDES
from .core import CardError, Param, _where, mapscene, recipe

PLACES = {k.lower(): v for k, v in json.loads((Path(__file__).resolve().parents[2] / "data" / "places.json").read_text(encoding="utf-8")).items() if not k.startswith("_")}

MAP_ERA = {"ww1": "1914", "ww2": "1938", "napoleonic": "1815", "ancient": "bc200", "vietnam": "1960", "modern": "1994"}

# countries (as named in that era's basemap) that belong to each side
COUNTRIES = {
    "1914": {"german": ["German Empire"], "british": ["United Kingdom of Great Britain and Ireland"], "french": ["France"],
             "russian": ["Russian Empire", "Grand Duchy of Finland"], "austrian": ["Austro-Hungarian Empire"], "ottoman": ["Ottoman Empire"],
             "italian": ["Kingdom of Italy"], "american": ["United States"], "belgian": ["Belgium"], "serbian": ["Serbia"], "romanian": ["Romania"],
             "bulgarian": ["Bulgaria"], "japanese": ["Empire of Japan"]},
    "1938": {"german": ["Germany"], "british": ["United Kingdom"], "french": ["France"], "soviet": ["USSR"], "italian": ["Italy"],
             "japanese": ["Empire of Japan"], "american": ["United States"], "polish": ["Poland"], "finnish": ["Finland"], "dutch": ["Netherlands"],
             "belgian": ["Belgium"], "chinese": ["Chinese warlords"], "romanian": ["Romania"], "hungarian": ["Hungary"]},
    "1945": {"german": ["Germany (France)", "Germany (Soviet)", "Germany (UK)", "Germany (USA)"], "british": ["United Kingdom"], "french": ["France"],
             "soviet": ["USSR"], "italian": ["Italy"], "japanese": ["Japan (USA)"], "american": ["United States"], "polish": ["Poland"], "chinese": ["China"]},
    "1960": {"vietnamese": ["Tonkin", "Annam"], "american": ["United States"], "french": ["France"], "chinese": ["China"], "soviet": ["USSR"]},
}
NEUTRAL_FILL = "#e3d3a8"


def place(c, name):
    if isinstance(name, (list, tuple)) and len(name) == 2 and all(isinstance(v, (int, float)) for v in name):
        return list(name)
    extra = {k.lower(): v for k, v in (c.film.get("places") or {}).items()}
    key = str(name).lower()
    if key in extra:
        return extra[key]
    if key in PLACES:
        return PLACES[key]
    import difflib
    near = difflib.get_close_matches(key, list(PLACES) + list(extra), n=3)
    raise CardError(f"{_where(c.raw)}: place \"{name}\" is not in data/places.json. Did you mean {near}? If not, add it to cards/_film.json "
                    f"\"places\": {{\"{name}\": [longitude, latitude]}} (look the coordinates up once).")


def _frame(points, min_span=2.2, pad=1.7):
    lons = [p[0] for p in points]
    lats = [p[1] for p in points]
    cx, cy = (min(lons) + max(lons)) / 2, (min(lats) + max(lats)) / 2
    span = max(min_span, (max(lons) - min(lons)) * pad, (max(lats) - min(lats)) * pad * 1.6)
    return [round(cx, 2), round(cy, 2)], round(span, 2)


def _map(c, center, span, sides_involved):
    era = c.film.get("map_era") or MAP_ERA.get(c.era, "1938")
    colors, legend = {}, []
    for sname in sides_involved:
        sd = SIDES.side(sname, c.era, c.film)
        for country in COUNTRIES.get(era, {}).get(sname, []):
            colors[country] = sd.nation
        if (sd.nation, sname) not in legend:
            legend.append((sd.nation, sname.capitalize()))
    m = {"era": era, "center": center, "span": span, "style": "paper", "colors": colors}
    if c.film.get("rivers"):
        m["rivers"] = c.film["rivers"]
    leg = {"kind": "legend", "x": 40, "y": 860, "hud": True, "in": 0, "enter": "fade", "items": [{"nation": n, "label": l} for n, l in legend]} if legend else None
    return m, leg


def _city(c, name, at, tag=False):
    return {"kind": "city", "name": str(name), "at": place(c, name), "in": at, "side": "right", "size": 28, **({"tag": True} if tag else {})}


ARROW_P = {
    "side": Param("side", doc="whose movement (colour)"),
    "from": Param("str", required=True, doc="place name where it starts"),
    "to": Param("str", required=True, doc="place name where it ends"),
    "via": Param("list", doc="optional place names in between"),
    "label": Param("str", doc="1-3 word tag on the arrow"),
    "dashed": Param("bool", False, doc="a plan or intention (not a real move)"),
    "on": Param("phrase", doc="word(s) where the arrow starts drawing"),
    "others": Param("list", doc="more arrows: [{\"side\": ..., \"from\": ..., \"to\": ..., \"on\": ...}] (max 2)"),
    "show": Param("list", doc="extra place names to mark"),
    "highlight": Param("list", doc="countries to tint, e.g. [\"Romania\"] (as named on the era's map)"),
    "highlight_side": Param("side", doc="side whose colour the highlighted countries get"),
}


@recipe("map_move", "map",
        when="Where something moved: 'they advanced to…', 'the Germans pushed toward…', 'divisions were sent east', 'an attack at X'.",
        not_when="The movement itself is the story (show the men: march / convoy / wave). Keep maps short.",
        params=ARROW_P, variants=("A", "B"),
        shots="A: map framed on the move, arrow draws on the word, gentle push. B: starts wider, pushes in toward the arrow head.",
        example={"at": "The place he picked was Verdun", "recipe": "map_move", "says": "Falkenhayn chose Verdun, a fortress the French would never give up.",
                 "side": "german", "from": "Metz", "to": "Verdun", "label": "VERDUN", "show": ["Verdun"]})
def map_move(c):
    sd = c.side()
    arrows = [{"side": c.p("side") or sd.name, "from": c.p("from"), "to": c.p("to"), "via": c.p("via") or [], "on": c.p("on"),
               "label": c.p("label"), "dashed": c.p("dashed")}] + list(c.p("others") or [])[:2]
    pts, els, involved = [], [], []
    shown = set()
    for k, a in enumerate(arrows):
        s = SIDES.side(a.get("side") or sd.name, c.era, c.film)
        involved.append(s.name)
        path = [place(c, a["from"])] + [place(c, v) for v in a.get("via") or []] + [place(c, a["to"])]
        pts += path
        t = c.t(a.get("on"), 0.18 + 0.25 * k, 0.4)
        el = {"kind": "arrow", "path": path, "color": s.nation, "in": t, "dur": 1.8, "width": 26}
        if a.get("dashed"):
            el["dashed"] = True
        if a.get("label") and str(a["label"]).lower() != str(a["to"]).lower():
            el["label"] = a["label"]
        els.append(el)
        if str(a["to"]).lower() not in shown:
            shown.add(str(a["to"]).lower())
            els.append(_city(c, a["to"], max(0.2, t - 0.3), tag=k == 0))
    for n in c.p("show") or []:
        pts.append(place(c, n))
        if str(n).lower() not in shown:
            shown.add(str(n).lower())
            els.append(_city(c, n, 0.3, tag=True))
    center, span = _frame(pts)
    m, leg = _map(c, center, span, involved)
    for country in c.p("highlight") or []:
        m["colors"][country] = SIDES.side(c.p("highlight_side") or sd.name, c.era, c.film).nation
    els.append(leg)
    cam = None
    if c.variant == "B":
        end = pts[-1] if len(arrows) == 1 else center
        cam = [{"t": 0, "center": center, "span": round(span * 1.35, 2)}, {"t": c.dur, "center": [round((center[0] + end[0]) / 2, 2), round((center[1] + end[1]) / 2, 2)], "span": span}]
    return mapscene(c, m, els, camera=cam)


@recipe("map_front", "map",
        when="A front line forms or moves: 'the front settled…', 'the line ran from the sea to Switzerland', 'they were pushed back to…'.",
        not_when="A single attack (map_move).",
        params={
            "side": Param("side", doc="the side holding the line (colour of the line)"),
            "line": Param("list", required=True, doc="place names along the front, north to south (3-10 names)"),
            "to_line": Param("list", doc="place names of the later line — the front slides from line to to_line"),
            "move_on": Param("phrase", doc="word(s) where the line starts moving"),
            "show": Param("list", doc="extra place names to mark"),
            "enemy": Param("side", doc="the other side (its countries are coloured too)"),
        },
        variants=("A",),
        shots="A: the line draws itself, then (with to_line) slides to its new position.",
        example={"at": "By Christmas the front ran", "recipe": "map_front", "says": "A continuous trench line now ran from the Channel to Switzerland.",
                 "side": "german", "enemy": "french", "line": ["Nieuport", "Ypres", "Arras", "Soissons", "Reims", "Verdun", "Nancy", "Belfort"]})
def map_front(c):
    sd = c.side()
    line = [place(c, n) for n in c.p("line")]
    to = [place(c, n) for n in c.p("to_line") or []]
    pts = line + to
    els = []
    f = {"kind": "front", "path": line, "color": "#7a2a22", "in": 0.0, "enter": "draw", "dur": 1.6}
    if to:
        tm = c.t(c.p("move_on"), 0.35, 1.2)
        f.update(enter="none", path2=to, morph=0, keys=K((tm, {"morph": 0}), (min(c.dur - 0.3, tm + 3.0), {"morph": 1})))
    els.append(f)
    for n in c.p("show") or []:
        pts.append(place(c, n))
        els.append(_city(c, n, 0.4, tag=True))
    center, span = _frame(pts, min_span=3.0, pad=1.4)
    involved = [sd.name] + ([c.p("enemy")] if c.p("enemy") else [])
    m, leg = _map(c, center, span, involved)
    m["hatch"] = [k for k, v in m["colors"].items() if v == sd.nation][:1]
    els.append(leg)
    return mapscene(c, m, els)


@recipe("map_route", "map",
        when="Ships, convoys, trains or armies travelling a long way: 'convoys crossed the Atlantic…', 'troops shipped to France…'.",
        not_when="Short moves (map_move).",
        params={
            "side": Param("side", doc="whose movers"),
            "route": Param("list", required=True, doc="place names along the route, in order"),
            "icon": Param("enum", "freighter", ["freighter", "warship", "truck", "tank", "train", "column", "crate"], "what travels"),
            "count": Param("int", 4, doc="how many icons follow each other"),
        },
        variants=("A",),
        shots="A: the dashed route draws with icons riding it; the camera follows the lead icon.",
        example={"at": "American troops crossed the Atlantic", "recipe": "map_route", "says": "Two million Americans were shipped to France.",
                 "side": "american", "route": ["New York", "Brest"], "icon": "freighter", "count": 5})
def map_route(c):
    sd = c.side()
    path = [place(c, n) for n in c.p("route")]
    if len(path) < 2:
        raise CardError(f"{_where(c.raw)}: \"route\" needs at least 2 place names.")
    center, span = _frame(path, min_span=3.0, pad=1.3)
    m, leg = _map(c, center, span, [sd.name])
    icon = c.p("icon")
    els = [{"kind": "route", "path": path, "color": "#3a6ea5" if icon in ("freighter", "warship") else sd.nation, "width": 5, "icon": icon,
            "trail": max(0, min(7, c.p("count") - 1)), "gap": 90, "iconSize": 1.3, "nation": sd.nation, "enter": "draw", "dur": max(2.0, c.dur - 0.8), "in": 0.3},
           _city(c, c.p("route")[0], 0.2), _city(c, c.p("route")[-1], 0.4, tag=True), leg]
    return mapscene(c, m, els)


@recipe("map_locate", "map",
        when="Where a place is or which countries are involved: 'a fortress town on the Meuse…', 'Romania joined the Allies…', 'in Silesia…'.",
        not_when="Something moves (map_move / map_route).",
        params={
            "places": Param("list", required=True, doc="place names to mark (the first is the key place, on a tag)"),
            "side": Param("side", doc="main side (coloured)"),
            "others": Param("list", doc="other sides to colour, e.g. [\"french\", \"british\"]"),
            "highlight": Param("list", doc="countries to tint with highlight_side's colour"),
            "highlight_side": Param("side", doc="colour for the highlighted countries"),
            "zoom": Param("enum", "region", ["city", "region", "country", "continent"], "how far out"),
        },
        variants=("A", "B"),
        shots="A: framed on the places, they appear one by one. B: starts on the continent and zooms in to the key place.",
        example={"at": "and Romania was encouraged", "recipe": "map_locate", "says": "Romania entered the war on the Allied side.",
                 "places": ["Bucharest"], "side": "german", "others": ["russian"], "highlight": ["Romania"], "highlight_side": "french", "zoom": "country",
                 "label": "ROMANIA JOINS THE ALLIES"})
def map_locate(c):
    sd = c.side()
    names = c.p("places")
    pts = [place(c, n) for n in names]
    span_min = {"city": 1.2, "region": 3.0, "country": 9.0, "continent": 30.0}[c.p("zoom")]
    center, span = _frame(pts, min_span=span_min)
    m, leg = _map(c, center, span, [sd.name] + list(c.p("others") or []))
    for country in c.p("highlight") or []:
        m["colors"][country] = SIDES.side(c.p("highlight_side") or sd.name, c.era, c.film).nation
    els = [_city(c, n, 0.3 + k * 0.5, tag=k == 0) for k, n in enumerate(names)] + [leg]
    cam = None
    if c.variant == "B":
        cam = [{"t": 0, "center": center, "span": max(span * 3, 20)}, {"t": min(c.dur, 3.0), "center": pts[0], "span": span}]
    return mapscene(c, m, els, camera=cam)
