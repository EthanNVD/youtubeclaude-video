"""Ground action: marching, convoys, assaults, waves, men under fire, guns, machine guns, hits, stretchers, aftermath,
surrender, retreat, tank attacks, trench life, trains, river crossings, paratroops.

All of these build scenes with the depth model (`world`), so people, vehicles and shell bursts are sized and sorted by their
ground position. Bursts land where `shells` says; the camera jolts on them (scene.impacts). See references/action.md.
"""
from __future__ import annotations

from shotlib import (AID, FX, K, PROP, SHOT, WORLD, assault as _assault, fallen as _fallen, gun_crew as _gun_crew, hit_and_help,
                     man_path, mg_nest as _mg_nest, shells, stretcher_team)

from .core import Param, recipe, stage

W = dict(WORLD)
MOODS = ["determined", "tired", "worried", "shout", "panic", "sad", "happy", "nervous"]


def _bursts(c, n, ys=(660, 760), xs=(300, 1700), size=2.0, first=0.5, spacing=None):
    """n shell bursts spread over the scene (deterministic per card)."""
    if n <= 0:
        return [], []
    spacing = spacing or max(0.7, (c.dur - first - 0.6) / n)
    pts = []
    for k in range(n):
        t = round(first + k * spacing + c.rng.uniform(-0.15, 0.15), 2)
        x = int(c.rng.uniform(*xs))
        y = int(c.rng.uniform(*ys))
        pts.append((max(0.2, min(c.dur - 0.4, t)), x, y))
    return shells(pts, size=size)


def _hit_times(c, n, t_on, spread=2.6):
    """n fall times starting at t_on, never two in the same second."""
    return [round(min(c.dur - 0.5, t_on + k * (spread / max(1, n)) + c.rng.uniform(0, 0.25)), 2) for k in range(n)]


# ------------------------------------------------------------------ march
@recipe("march", "action",
        when="Troops move on foot to somewhere: 'the army marched…', 'reinforcements were sent…', 'they moved up to the front…'.",
        not_when="They attack (assault/wave) or travel by vehicle (convoy) or by rail (rail).",
        params={
            "side": Param("side", doc="whose troops (default: the film's first side)"),
            "mood": Param("enum", "determined", MOODS, "faces"),
            "setting": Param("enum", "countryside", ["countryside", "field", "steppe", "snow", "desert", "mud", "polder", "street", "nomansland", "jungle"], "landscape"),
            "direction": Param("enum", "right", ["right", "left"], "which way they march (keep one side's direction consistent in a chapter)"),
            "vehicles": Param("bool", False, doc="add trucks/tanks on the far road"),
        },
        variants=("A", "B", "C"),
        shots="A: side view in two files at different depths → close on one marching face. B: column comes down the road toward the camera "
              "(depth). C: three planes: vehicles far, a file mid, one soldier near watching them pass.",
        example={"at": "Reinforcements streamed toward the town", "recipe": "march", "says": "French reinforcements kept pouring toward Verdun.",
                 "side": "french", "mood": "tired", "vehicles": True, "time": "dusk"})
def march(c):
    sd = c.side()
    d = 1 if c.p("direction") == "right" else -1
    mood = c.p("mood")
    els, v = [], c.variant
    dur = max(c.dur, 3.0)
    if v == "B":
        for i in range(6):
            x = 860 + (i % 2) * 200 - (i // 2) * 30
            els.append(man_path(f"m{i}", sd.soldier, [(0, x, 640 + (i // 2) * 30), (dur, x + (i % 2 - 0.5) * 120, 960 + (i // 2) * 90)], pose="shoulder", expr=mood))
        shots = [SHOT(0, None, None, zoom=1.0, push=0.04), SHOT(dur * 0.6, "m4", "mediumclose", track=True, frameX=0.1)]
    else:
        for i in range(5):
            x0 = (300 - i * 260) if d > 0 else (1620 + i * 260)
            els.append({**man_path(f"m{i}", sd.soldier, [(0, x0, 860 + (i % 2) * 22), (dur, x0 + d * 420 * dur / 8, 860 + (i % 2) * 22)], pose="shoulder", expr=mood),
                        "flip": d < 0})
        x1 = 760 if d > 0 else 1160
        els.append({**man_path("near", sd.soldier, [(0, x1, 1150), (dur, x1 + d * 520 * dur / 8, 1150)], pose="shoulder", expr=mood), "flip": d < 0})
        shots = [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(min(dur * 0.55, 4.0), "near", "mediumclose", track=True, frameX=0.1 * d)]
        if v == "C":
            els[-1] = AID("near", sd.soldier, 1640 if d > 0 else 280, 1110, None, "idle", "worried", look=-0.8 * d, keys=K((dur * 0.5, {"pose": "chin"})))
            shots = [SHOT(0, None, None, zoom=1.0, push=0.04), SHOT(dur * 0.55, "near", "close", frameX=-0.12 * d)]
    if c.p("vehicles") and sd.get("tank") is not None:
        for i in range(3):
            x0 = (380 - i * 330) if d > 0 else (1540 + i * 330)
            els.append({"id": f"v{i}", "kind": "vehicle", "type": "truck", "nation": sd.nation, "x": x0, "y": 700, "flip": d < 0,
                        "keys": K((dur, {"x": x0 + d * 520})), "moving": True})
    return stage(c, {"kind": c.p("setting"), "drift": 0}, els, [q for q in shots if q["t"] < c.dur - 0.4], world=W,
                 sfx=[{"t": 0.1, "id": "footsteps", "dur": min(5.0, dur)}])


# ------------------------------------------------------------------ convoy
@recipe("convoy", "action",
        when="Vehicles move: 'the tanks rolled…', 'supplies were trucked…', 'the panzers raced to the coast…'.",
        not_when="A single vehicle arrives somewhere (use vehicle in a scene), aircraft (air_battle/bombing), ships (naval_battle).",
        params={
            "side": Param("side", doc="whose vehicles"),
            "vehicle": Param("enum", "tank", ["tank", "tank_heavy", "truck", "halftrack", "jeep", "car", "artillery", "horse", "cart"], "which vehicle (tank = the side's usual tank for the era)"),
            "count": Param("int", 3, doc="2-4 vehicles"),
            "setting": Param("enum", "polder", ["polder", "field", "countryside", "steppe", "snow", "desert", "mud", "street", "ruins", "nomansland"], "landscape"),
            "direction": Param("enum", "right", ["right", "left"], "which way"),
            "infantry": Param("bool", True, doc="soldiers walking beside / sitting on the vehicles"),
        },
        variants=("A", "B", "C"),
        shots="A: column on the middle road, wide, then a closer pass. B: a close pass that fills half the frame (low, slight shake) with infantry far behind. "
              "C: three planes — column far, infantry mid, one soldier near.",
        example={"at": "The panzers raced west", "recipe": "convoy", "says": "German tank columns drove fast toward the Channel coast.",
                 "side": "german", "vehicle": "tank", "count": 3, "setting": "countryside"})
def convoy(c):
    sd = c.side()
    vt = c.p("vehicle")
    vt = sd.get("tank", "tank") if vt == "tank" else sd.get("tank_heavy", sd.get("tank", "tank")) if vt == "tank_heavy" else vt
    d = 1 if c.p("direction") == "right" else -1
    n = max(1, min(4, c.p("count")))
    dur = max(c.dur, 3.0)
    els = []
    v = c.variant
    if v == "B":
        els.append({"id": "v0", "kind": "vehicle", "type": vt, "nation": sd.nation, "x": 260 if d > 0 else 1660, "y": 1010, "flip": d < 0,
                    "keys": K((dur, {"x": 1350 if d > 0 else 570})), "moving": True})
        if c.p("infantry"):
            els += [AID(f"i{i}", sd.soldier, 1250 + i * 140, 690, None, "shoulder", "neutral", holds="rifle") for i in range(3)]
        shots = [SHOT(0, None, None, zoom=1.0, push=0.03, shake=0.6)]
        return stage(c, {"kind": c.p("setting"), "drift": 0}, els, shots, world={"scale": 0.62, "y": 880})
    for i in range(n):
        x0 = (380 - i * 360) if d > 0 else (1540 + i * 360)
        els.append({"id": f"v{i}", "kind": "vehicle", "type": vt, "nation": sd.nation, "x": x0, "y": 720 if v == "C" else 820, "flip": d < 0,
                    "keys": K((dur, {"x": x0 + d * 600})), "moving": True, "crew": i == 0})
    if c.p("infantry"):
        for i in range(3):
            x0 = (1500 - i * 150) if d > 0 else (420 + i * 150)
            els.append({**man_path(f"i{i}", sd.soldier, [(0, x0, 900 if v == "C" else 940), (dur, x0 + d * 300, 900 if v == "C" else 940)], pose="shoulder", expr="tired"), "flip": d < 0})
    if v == "C":
        els.append(AID("near", sd.soldier, 1640 if d > 0 else 280, 1110, None, "idle", "worried", look=-0.8 * d))
        shots = [SHOT(0, None, None, zoom=1.0, push=0.04), SHOT(dur * 0.6, "near", "close", frameX=-0.12 * d)]
    else:
        shots = [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(dur * 0.55, "v0", "full", track=True)]
    return stage(c, {"kind": c.p("setting"), "drift": 0, "road": v != "C"}, els, [q for q in shots if q["t"] < c.dur - 0.4], world={"scale": 0.8, "y": 900})


# ------------------------------------------------------------------ assault (over the top)
@recipe("assault", "action",
        when="An attack on foot: 'they went over the top…', 'the infantry attacked…', 'the assault began…', 'attacks gained nothing and cost many men'.",
        not_when="A running charge across the frame (wave), defenders pinned down (under_fire), tanks leading (tank_attack).",
        params={
            "side": Param("side", doc="who attacks"),
            "falls": Param("int", 2, doc="how many men are hit (0-5)"),
            "hit_on": Param("phrase", doc="word(s) where the first man falls (e.g. 'cost', 'killed')"),
            "climb": Param("bool", True, doc="the near row climbs out of the trench at the start"),
            "shells": Param("int", 3, doc="shell bursts among them (0-6)"),
            "mg": Param("bool", True, doc="machine-gun tracers from the enemy line"),
        },
        variants=("A", "B"),
        shots="A: from behind the parapet: rows walk away into the smoke, wide → full on the group where men fall. "
              "B: the same from a lower angle with a close on one man before he goes, then the wide.",
        example={"at": "Attacks on the Western Front gained", "recipe": "assault", "says": "Attacks across no man's land won little ground and killed many men.",
                 "side": "british", "falls": 3, "hit_on": "cost enormous"})
def assault(c):
    sd = c.side()
    th = c.t(c.p("hit_on"), 0.5, 1.6)
    nf = max(0, min(5, c.p("falls")))
    climb = c.p("climb")
    T = max(c.dur, 4.0)
    rows = [(1130, 800, [330, 960, 1590], 0.2, T), (900, 720, [150, 640, 1280, 1780], 0, T), (760, 660, [420, 1100, 1500], 0, T)]
    order = [3, 5, 1, 8, 6]
    falls = dict(zip(order[:nf], _hit_times(c, nf, th)))
    men = _assault("m", sd.soldier, rows, falls, climb=climb)
    bur, imp = _bursts(c, max(0, min(6, c.p("shells"))), ys=(650, 740))
    els = men + bur
    if c.p("mg"):
        els += [FX("tracer", 1990, 640, dir=172, **{"in": 0.8}), FX("tracer", 1990, 610, dir=176, **{"in": 1.4})]
    if c.variant == "A":
        shots = [SHOT(0, None, None, zoom=1.0, push=0.04), SHOT(max(1.0, th - 0.3), ["m3", "m4", "m5"], "full", push=0.05)]
    else:
        men[1]["id"] = "lead"
        shots = [SHOT(0, "lead", "mediumclose", frameX=0.1), SHOT(1.2, None, None, zoom=1.0, push=0.04), SHOT(max(1.8, th - 0.2), ["m3", "m4", "m5"], "full")]
    return stage(c, {"kind": "nomansland", "fg": "sandbags" if climb else None}, els, [q for q in shots if q["t"] < c.dur - 0.4], world=W, impacts=imp,
                 sfx=[{"t": 0.8, "id": "machinegun", "dur": min(5.0, c.dur - 1)}] if c.p("mg") else None)


# ------------------------------------------------------------------ wave (side charge)
@recipe("wave", "action",
        when="A fast charge or counter-attack across open ground: 'they stormed…', 'the attack began…', 'the Russians smashed through…'.",
        not_when="A slow walk into machine guns (assault).",
        params={
            "side": Param("side", doc="who charges"),
            "direction": Param("enum", "right", ["right", "left"], "which way they run"),
            "count": Param("int", 6, doc="4-8 men"),
            "falls": Param("int", 1, doc="0-3 men hit"),
            "hit_on": Param("phrase", doc="word(s) for the first fall"),
            "shells": Param("int", 3, doc="bursts ahead of them"),
            "setting": Param("enum", "nomansland", ["nomansland", "steppe", "field", "snow", "desert", "mud", "ruins"], "terrain"),
            "enemy": Param("side", doc="optional: defenders on the far side who fire, then break"),
        },
        variants=("A", "B"),
        shots="A: wide as the wave crosses → full shot tracking the leader. B: start on the leader's face (shout), then the wide.",
        example={"at": "The attack began in February 1916", "recipe": "wave", "says": "German storm troops rushed the French lines at Verdun.",
                 "side": "german", "date": "21 FEBRUARY 1916", "setting": "nomansland", "weather": "snow", "time": "dawn"})
def wave(c):
    sd = c.side()
    d = 1 if c.p("direction") == "right" else -1
    n = max(4, min(8, c.p("count")))
    T = max(c.dur, 3.0)
    th = c.t(c.p("hit_on"), 0.55, 1.2)
    nf = max(0, min(3, c.p("falls")))
    falls = dict(zip([2, 5, 1][:nf], _hit_times(c, nf, th)))
    els = []
    for i in range(n):
        y = 705 + (i % 4) * 48
        x0 = (-160 - i * 150) if d > 0 else (2080 + i * 150)
        x1 = x0 + d * 1460
        els.append({**man_path(f"w{i}", sd.soldier, [(0, x0, y), (T, x1, y)], pose="charge", expr="shout", fall=falls.get(i), fall_dir=-d, run=True), "flip": d < 0})
    bx = (1200, 1750) if d > 0 else (170, 720)
    bur, imp = _bursts(c, max(0, min(6, c.p("shells"))), ys=(700, 880), xs=bx)
    els += bur
    en = c.p("enemy")
    if en:
        es = c.side("enemy")
        tb = c.t(None, 0.7)
        for i in range(3):
            x = (1500 + i * 150) if d > 0 else (420 - i * 150)
            els.append({**AID(f"e{i}", es.soldier, x, 800 + i * 50, None, "aim", "nervous", holds="rifle", fireAt=[0.4 + i * 0.3, 1.3 + i * 0.3],
                              keys=K((tb + i * 0.2, {"pose": "surrender" if i % 2 == 0 else "charge", "holds": "" if i % 2 == 0 else "rifle", "expr": "panic"}))), "flip": d > 0})
    if c.variant == "A":
        shots = [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(min(1.8, T * 0.45), ["w0", "w1", "w2"], "full", track=True)]
    else:
        shots = [SHOT(0, ["w0", "w1"], "full", track=True), SHOT(min(1.6, T * 0.4), None, "wide", zoom=1.0, push=0.03)]
    return stage(c, {"kind": c.p("setting"), "drift": 0, "road": False, "houses": False, "poles": False}, els, [q for q in shots if q["t"] < c.dur - 0.4], world=W, impacts=imp)


# ------------------------------------------------------------------ under fire
@recipe("under_fire", "action",
        when="Men endure shelling or hold a position: 'the battle lasted 300 days…', 'they held the line…', 'the bombardment went on…'.",
        not_when="They attack (assault/wave).",
        params={
            "side": Param("side", doc="who is under fire"),
            "setting": Param("enum", "shellhole", ["shellhole", "trench"], "a shell hole in the open, or a trench"),
            "runner": Param("bool", True, doc="a runner dashes across behind them"),
            "shells": Param("int", 4, doc="bursts walking closer (2-6)"),
            "fire_back": Param("bool", False, doc="one man fires back over the parapet"),
        },
        variants=("A", "B"),
        shots="A: wide over the men pressed down → medium-close on the most scared face. B: close first, then the wide with the runner.",
        example={"at": "It became the longest battle", "recipe": "under_fire", "says": "Verdun turned into a battle of endurance that lasted about 300 days.",
                 "side": "french", "label": {"text": "≈ 300 DAYS", "on": "three hundred days"}})
def under_fire(c):
    sd = c.side()
    T = max(c.dur, 3.0)
    n = max(2, min(6, c.p("shells")))
    if c.p("setting") == "trench":
        els = []
        for i, x in enumerate([520, 960, 1400]):
            p0, p1 = [("cower", "head"), ("head", "cower"), ("port", "cower")][i]
            els.append(AID(f"s{i}", sd.soldier, x + (i - 1) * 40, 1000 + (i % 2) * 18, 1.45 - (i % 2) * 0.08, p0, "panic" if i != 2 else "shocked",
                           holds="rifle" if p0 == "port" else None, turn=[0.4, -0.2, -0.5][i], keys=K((1.0 + i * 0.55, {"pose": p1, "holds": ""}))))
        pts = [(round(0.3 + k * (T - 0.8) / n, 2), [1300, 500, 1000, 700, 1500, 800][k], 400) for k in range(n)]
        bur, imp = shells(pts, size=1.2)
        for b in bur:
            b["depth"] = False
        shots = [SHOT(0, ["s0", "s1", "s2"], "full", push=0.04), SHOT(T * 0.5, "s1", "close", frameX=0.12, shake=3)]
        return stage(c, {"kind": "trench"}, els + bur, [q for q in shots if q["t"] < c.dur - 0.4], impacts=imp)
    els = [AID("p1", sd.soldier, 560, 1060, 1.7, "cower", "panic", turn=0.4, keys=K((T * 0.35, {"pose": "head"}), (T * 0.7, {"pose": "port", "holds": "rifle", "expr": "determined"}))),
           AID("p2", sd.soldier, 1300, 1080, 1.8, "head", "shocked", turn=-0.4, keys=K((T * 0.5, {"pose": "cower", "expr": "panic"})))]
    if c.p("fire_back"):
        els[0]["fireAt"] = [T * 0.75, T * 0.75 + 0.6]
    if c.p("runner"):
        els.append({**man_path("run", sd.soldier, [(0.8, 2050, 820), (min(T, 4.2), -150, 800)], pose="charge", expr="determined", run=True), "flip": True})
    pts = [(round(0.4 + k * (T - 0.9) / n, 2), [1500, 400, 1200, 760, 1650, 600][k], [660, 700, 760, 720, 690, 740][k]) for k in range(n)]
    bur, imp = shells(pts, size=2.0)
    shots = ([SHOT(0, None, None, zoom=1.0, push=0.04), SHOT(T * 0.48, "p1", "mediumclose", frameX=-0.15, push=0.05)] if c.variant == "A" else
             [SHOT(0, "p2", "mediumclose", frameX=0.15), SHOT(1.4, None, None, zoom=1.0, push=0.04), SHOT(T * 0.7, "p1", "mediumclose", frameX=-0.15)])
    return stage(c, {"kind": "nomansland", "fg": "sandbags"}, els + bur, [q for q in shots if q["t"] < c.dur - 0.4], world=W, impacts=imp)


# ------------------------------------------------------------------ gun crew
@recipe("gun_crew", "action",
        when="Artillery fires: 'the guns opened fire…', 'a bombardment…', 'let the heavy guns do the killing…', 'the barrage began…'.",
        not_when="Shells landing on men (under_fire / assault with shells).",
        params={
            "side": Param("side", doc="whose guns"),
            "heavy": Param("bool", True, doc="heavy howitzers (bigger guns)"),
            "fire_on": Param("phrase", doc="word(s) for the main shot (the second gun fires on other beats)"),
            "time": Param("enum", "dusk", ["day", "dusk", "dawn", "night"], "dusk/night make the flashes read best"),
        },
        variants=("A", "B"),
        shots="A: wide of the battery → medium-close on the layer covering his ears as the gun fires → wide again on the smoke. "
              "B: start on the loader carrying the shell (medium), then the battery wide.",
        example={"at": "and let German heavy guns", "recipe": "gun_crew", "says": "Falkenhayn wanted artillery, not infantry, to do the killing.",
                 "side": "german", "fire_on": "heavy guns", "time": "dusk"})
def gun_crew(c):
    sd = c.side()
    T = max(c.dur, 3.0)
    f2 = c.t(c.p("fire_on"), 0.65, 1.8)
    f1 = round(min(1.1, f2 - 1.2), 2) if f2 > 2.2 else None
    fire = [t for t in (f1, f2) if t is not None]
    els = _gun_crew("g", sd.soldier, 760, 1000, fire, sd.nation, loader_from=120, heavy=1.9 if c.p("heavy") else 1.0)
    els.append({"id": "g2", "kind": "vehicle", "type": "artillery", "nation": sd.nation, "x": 1460, "y": 760, "fireAt": [0.4, round(T * 0.45, 2), round(min(T - 0.4, f2 + 0.7), 2)],
                **({"depthScale": 1.9} if c.p("heavy") else {})})
    els.append(AID("c2", sd.soldier, 1700, 800, None, "idle", "neutral", keys=K((0.2, {"pose": "head"}), (1.3, {"pose": "idle"}), (T * 0.45 - 0.2, {"pose": "head"}))))
    if c.variant == "A":
        shots = [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(max(0.8, f2 - 1.5), "gc", "mediumclose", frameX=-0.12, push=0.05),
                 SHOT(f2 + 0.35, None, "wide", zoom=1.12, x=900, y=620, push=0.03)]
    else:
        shots = [SHOT(0, "gld", "medium", track=True, frameX=0.12), SHOT(max(1.0, f2 - 0.8), None, "wide", zoom=1.0, push=0.03)]
    return stage(c, {"kind": "nomansland", "wire": False, "horizon": 600}, els, [q for q in shots if q["t"] < c.dur - 0.4],
                 world={**W, "vehicles": 1.0}, impacts=fire)


# ------------------------------------------------------------------ machine-gun nest
@recipe("mg_nest", "action",
        when="Defenders mow down an attack: 'machine guns cut them down…', '19,240 killed…', 'the defenders opened fire…'.",
        not_when="",
        params={
            "side": Param("side", doc="who mans the guns (the defenders)"),
            "direction": Param("enum", "left", ["left", "right"], "which way they fire (toward the attackers' side of the screen)"),
            "spotter": Param("bool", True, doc="a man with binoculars beside them"),
        },
        variants=("A", "B"),
        shots="A: medium over the sandbags → medium-close on the gunner (flashes, small shake). B: close on the gunner first, then the group.",
        example={"at": "including nineteen thousand", "recipe": "mg_nest", "says": "German machine guns killed nearly twenty thousand British soldiers that day.",
                 "side": "german", "counter": {"to": 19240, "suffix": " KILLED", "on": "nineteen thousand", "color": "#f08070"}})
def mg_nest(c):
    sd = c.side()
    flip = c.p("direction") == "left"
    els = _mg_nest("mg", sd.soldier, [380, 860] if flip else [1540, 1060], 1170, 1.9, fire=(0.0, c.dur), flip=flip, spotter=c.p("spotter"))
    ids = [e["id"] for e in els]
    shots = ([SHOT(0, ids, "medium", push=0.04, shake=2), SHOT(c.dur * 0.5, "mg0", "mediumclose", frameX=-0.2 if flip else 0.2, shake=3)] if c.variant == "A" else
             [SHOT(0, "mg0", "close", frameX=-0.2 if flip else 0.2, shake=3), SHOT(c.dur * 0.45, ids, "medium", shake=2)])
    return stage(c, {"kind": "nomansland", "fg": "sandbags"}, els, [q for q in shots if q["t"] < c.dur - 0.4],
                 sfx=[{"t": 0.0, "id": "machinegun", "dur": max(1.0, c.dur - 0.3)}])


# ------------------------------------------------------------------ hit
@recipe("hit", "action",
        when="One man's death or wound stands for many: 'the army that was supposed to bleed was the German army too', 'he was killed…'.",
        not_when="Many fall at once (assault with falls).",
        params={
            "side": Param("side", doc="the man who is hit"),
            "hit_on": Param("phrase", doc="word(s) where he is hit"),
            "burst": Param("bool", True, doc="a shell bursts behind him at that moment"),
        },
        variants=("A",),
        shots="A: full shot tracking him advancing → he falls → his comrade runs in and kneels → close-up of the comrade crying.",
        example={"at": "The army that was supposed to bleed", "recipe": "hit", "says": "German soldiers died at Verdun as fast as the French.", "side": "german", "hit_on": "German army"})
def hit(c):
    sd = c.side()
    T = max(c.dur, 3.4)
    th = c.t(c.p("hit_on"), 0.4, 1.2)
    els = hit_and_help("x", sd.soldier, 380, 1100, 960, th, max(th + 1.0, T * 0.8), helper_from=-150)
    imp = []
    if c.p("burst"):
        b, imp = shells([(round(th - 0.05, 2), 1500, 740)])
        els += b
    shots = [SHOT(0, "xh", "full", track=True, frameX=0.1), SHOT(min(c.dur - 1.0, th + 1.35), "xk", "close", frameX=0.15, push=0.05)]
    return stage(c, {"kind": "nomansland"}, els, shots, world=W, impacts=imp)


# ------------------------------------------------------------------ stretcher
@recipe("stretcher", "action",
        when="The wounded, the cost carried back: 'casualties mounted…', '337,000 German casualties…', 'the wounded…'. A number can run on top (counter).",
        not_when="Grief / the dead at dusk (silhouette).",
        params={
            "side": Param("side", doc="whose wounded"),
            "setting": Param("enum", "trench", ["trench", "nomansland", "ruins", "snow"], "where they are carried"),
            "direction": Param("enum", "right", ["right", "left"], "which way they walk"),
        },
        variants=("A", "B"),
        shots="A: bearers walk through the trench past a man sitting with his head in his hands (one set-up with a pan). "
              "B: in the open: two teams in depth, then a medium on the near team.",
        example={"at": "and German casualties", "recipe": "stretcher", "says": "The attackers lost almost as many men as the French.", "side": "german",
                 "counter": {"to": 337000, "prefix": "≈ ", "suffix": " GERMAN CASUALTIES", "on": "three hundred and thirty-seven"}})
def stretcher(c):
    sd = c.side()
    T = max(c.dur, 3.0)
    d = 1 if c.p("direction") == "right" else -1
    place = c.p("setting")
    if place == "trench" or c.variant == "A":
        x0, x1 = (1225, 2125) if d > 0 else (700, -200)
        els = stretcher_team("st", sd.soldier, x0, x1, 1000, T * 0.85, scale=1.5)
        if d < 0:
            for e in els:
                e["flip"] = True
        els.append(AID("sd", sd.soldier, 420 if d > 0 else 1500, 1000, 1.55, "cower", "sad", turn=0.4))
        return stage(c, {"kind": "trench" if place == "trench" else place}, els, [SHOT(0, None, None, zoom=1.0, push=0.04, panX=80 * d)])
    els = stretcher_team("a", sd.soldier, 500, 1300, 960, T) + stretcher_team("b", sd.soldier, -300, 500, 760, T)
    shots = [SHOT(0, None, None, zoom=1.0, push=0.03), SHOT(T * 0.5, ["ar", "af"], "full", track=True)]
    return stage(c, {"kind": place}, els, [q for q in shots if q["t"] < c.dur - 0.4], world=W)


# ------------------------------------------------------------------ aftermath
@recipe("aftermath", "action",
        when="After the battle: 'it was the worst day…', 'the field was covered with dead…', 'by nightfall…'. Quiet, grey.",
        not_when="",
        params={
            "side": Param("side", doc="whose dead"),
            "survivor": Param("bool", True, doc="a survivor walks back through them"),
        },
        variants=("A", "B"),
        shots="A: wide of the field (grey) → medium on the survivor. B: close on a helmet on the ground, then the wide.",
        example={"at": "It's still the worst day", "recipe": "aftermath", "says": "The first day of the Somme remains the British Army's worst day.",
                 "side": "british", "label": "WORST DAY IN BRITISH ARMY HISTORY", "tint": "grey", "time": "dusk"})
def aftermath(c):
    sd = c.side()
    T = max(c.dur, 3.0)
    els = _fallen("d", sd.soldier, [(260 + i * 330, 820 + (i % 3) * 90) for i in range(5)])
    if c.p("survivor"):
        els.append({**man_path("sv", sd.soldier, [(0, 1500, 1000), (T * 0.9, 700, 1080)], pose="idle", expr="cry", holds=""), "flip": True})
    shots = ([SHOT(0, None, None, zoom=1.0, push=0.05), SHOT(T * 0.5, "sv", "medium", frameX=0.12)] if c.variant == "A" else
             [SHOT(0, None, None, zoom=2.4, x=420, y=900, push=0.03), SHOT(min(2.0, T * 0.4), None, None, zoom=1.0, push=0.04)])
    s = stage(c, {"kind": "nomansland", "time": "dusk"}, els, [q for q in shots if q["t"] < c.dur - 0.4], world=W)
    s.setdefault("tint", "grey")
    return s


# ------------------------------------------------------------------ surrender
@recipe("surrender", "action",
        when="Soldiers give up: 'thousands surrendered…', 'the army collapsed…', 'prisoners were taken…'.",
        not_when="Leaders sign a surrender (signing).",
        params={
            "side": Param("side", doc="who surrenders"),
            "captors": Param("side", doc="who takes them prisoner"),
            "count": Param("int", 4, doc="3-6 men surrendering"),
        },
        variants=("A", "B"),
        shots="A: wide: hands go up one after another as the captors walk in → close on one face. B: a file of prisoners walking past the camera.",
        example={"at": "and smashed the Austro-Hungarian armies", "recipe": "surrender", "says": "The Austro-Hungarian army broke and its men surrendered in masses.",
                 "side": "austrian", "captors": "russian"})
def surrender(c):
    sd, cap = c.side(), c.side("captors")
    T = max(c.dur, 3.0)
    n = max(3, min(6, c.p("count")))
    els = []
    if c.variant == "B":
        for i in range(n):
            els.append({**man_path(f"p{i}", sd.soldier, [(0, 2000 + i * 200, 900 + (i % 2) * 60), (T, 600 + i * 200, 900 + (i % 2) * 60)], pose="surrender", expr=["sad", "tired", "worried"][i % 3], holds=""), "flip": True})
        els.append(AID("g", cap.soldier, 400, 1000, None, "port", "determined", holds="rifle"))
        shots = [SHOT(0, None, None, zoom=1.0, push=0.03), SHOT(T * 0.55, "p1", "mediumclose", track=True, frameX=-0.1)]
        return stage(c, {"kind": "field", "road": True, "poles": False}, els, [q for q in shots if q["t"] < c.dur - 0.4], world=W)
    for i in range(n):
        els.append({**AID(f"p{i}", sd.soldier, 1100 + i * 170, 820 + (i % 3) * 60, None, ["aim", "port", "head", "cower"][i % 4], ["nervous", "worried", "panic", "sad"][i % 4],
                          holds="rifle" if i % 4 < 2 else None, keys=K((0.6 + i * 0.45, {"pose": "surrender", "holds": "", "expr": ["sad", "worried", "cry", "tired"][i % 4]}))), "flip": True})
    for i in range(3):
        els.append(man_path(f"c{i}", cap.soldier, [(0, -200 - i * 180, 860 + i * 60), (T * 0.8, 500 - i * 120, 860 + i * 60)], pose="port", expr="determined"))
    shots = [SHOT(0, None, None, zoom=1.0, push=0.04), SHOT(T * 0.6, "p2", "close", frameX=-0.12)]
    return stage(c, {"kind": "steppe" if sd.era == "ww1" else "field", "road": False, "poles": False, "houses": False}, els, [q for q in shots if q["t"] < c.dur - 0.4], world=W)


# ------------------------------------------------------------------ retreat
@recipe("retreat", "action",
        when="An army falls back: 'they retreated…', 'the front collapsed…', 'they fled…', 'the defenders ran'.",
        not_when="Orderly withdrawal by road with vehicles (convoy, direction away).",
        params={
            "side": Param("side", doc="who retreats"),
            "direction": Param("enum", "left", ["left", "right"], "which way they run"),
            "shells": Param("int", 2, doc="bursts behind them"),
        },
        variants=("A", "B"),
        shots="A: wide, men running past, looking back → close on a frightened face. B: back view running away into depth.",
        example={"at": "The front gave way", "recipe": "retreat", "says": "The defending line broke and the men ran.", "side": "italian"})
def retreat(c):
    sd = c.side()
    T = max(c.dur, 3.0)
    d = 1 if c.p("direction") == "right" else -1
    els = []
    if c.variant == "B":
        for i in range(6):
            x = 300 + i * 260
            els.append(man_path(f"r{i}", sd.soldier, [(0, x, 1060 - (i % 3) * 60), (T, x + (960 - x) * 0.2, 700 - (i % 3) * 20)], pose="charge", expr="panic", holds="", view="back", run=True))
        shots = [SHOT(0, None, None, zoom=1.0, push=0.04)]
    else:
        for i in range(6):
            y = 780 + (i % 3) * 90
            x0 = (1900 + i * 160) if d < 0 else (20 - i * 160)
            els.append({**man_path(f"r{i}", sd.soldier, [(0, x0, y), (T, x0 + d * 1500, y)], pose="charge", expr="panic", holds="" if i % 2 else "rifle", run=True, look=-d), "flip": d < 0})
        shots = [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(T * 0.5, ["r1", "r2"], "full", track=True)]
    bur, imp = _bursts(c, max(0, min(5, c.p("shells"))), ys=(700, 800), xs=(1300, 1800) if d < 0 else (120, 620))
    return stage(c, {"kind": "nomansland"}, els + bur, [q for q in shots if q["t"] < c.dur - 0.4], world=W, impacts=imp)


# ------------------------------------------------------------------ tank attack
@recipe("tank_attack", "action",
        when="Tanks break in: 'the first tanks…', 'the tanks broke through…', 'armour led the attack…'.",
        not_when="Tanks just driving somewhere (convoy).",
        params={
            "side": Param("side", doc="whose tanks"),
            "enemy": Param("side", doc="the defenders who flee"),
            "count": Param("int", 1, doc="1-3 tanks"),
            "shock_on": Param("phrase", doc="word(s) where the defender's face is shown"),
            "infantry": Param("bool", True, doc="infantry following the tanks"),
        },
        variants=("A", "B"),
        shots="A: wide ≥ 3 s as the tank crawls in and fires, defenders run → medium-close on the shocked defender. "
              "B: the defender's face first (he hears it), then the wide reveal.",
        example={"at": "In September, the first tanks", "recipe": "tank_attack", "says": "The British used tanks for the first time and the Germans fled.",
                 "side": "british", "enemy": "german", "date": "SEPTEMBER 1916"})
def tank_attack(c):
    sd, en = c.side(), c.side("enemy")
    T = max(c.dur, 3.4)
    ts = c.t(c.p("shock_on"), 0.65, 1.6)
    n = max(1, min(3, c.p("count")))
    tk = sd.get("tank", "tank")
    els = []
    for i in range(n):
        els.append({"id": f"tk{i}", "kind": "vehicle", "type": tk, "nation": sd.nation, "x": 120 - i * 520, "y": 880 - i * 70,
                    "keys": K((c.dur, {"x": 720 - i * 520})), "fireAt": [round(1.6 + i * 0.9, 2)], "moving": True})
    if c.p("infantry"):
        for i in range(3):
            els.append(man_path(f"i{i}", sd.soldier, [(0, -120 - i * 200, 960 + (i % 2) * 50), (T, 380 - i * 200, 960 + (i % 2) * 50)], pose="port", expr="determined"))
    for i in range(3):
        els.append({**man_path(f"f{i}", en.soldier, [(0.6 + i * 0.25, 1350 + i * 160, 860 + (i % 2) * 70), (T, 2300 + i * 160, 860 + (i % 2) * 70)],
                               pose="charge", expr="panic", holds="", run=True)})
    els.append({**AID("st", en.soldier, 1500, 1060, None, "aim", "shocked", holds="rifle", fireAt=[0.7, 1.4, 2.2], keys=K((ts + 0.3, {"pose": "cower", "holds": "", "expr": "panic"}))), "flip": True})
    els.append(FX("dust", 300, 900, size=1.2))
    if c.variant == "A":
        shots = [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(max(2.8, ts), "st", "mediumclose", frameX=-0.12, push=0.05)]
    else:
        shots = [SHOT(0, "st", "mediumclose", frameX=-0.12), SHOT(1.2, None, "wide", zoom=1.0, push=0.03)]
    return stage(c, {"kind": "nomansland"}, els, [q for q in shots if q["t"] < c.dur - 0.4], world=W, impacts=[1.6],
                 sfx=[{"t": 0, "id": "tank_engine", "dur": T}])


# ------------------------------------------------------------------ trench life
@recipe("trench_wait", "action",
        when="Waiting, endurance, routine in the line: 'months of stalemate…', 'the war settled into the trenches…', 'the men waited…'.",
        not_when="Shelling (under_fire).",
        params={
            "side": Param("side", doc="whose trench"),
            "business": Param("enum", "mixed", ["mixed", "letters", "lookout", "rain", "eating"], "what they do"),
        },
        variants=("A", "B"),
        shots="A: three men doing small things (one watches through binoculars, one writes, one smokes) → close on one. B: rain, a man trudging past the others.",
        example={"at": "The war settled into the trenches", "recipe": "trench_wait", "says": "Both armies dug in and the front froze for years.", "side": "british", "weather": "rain"})
def trench_wait(c):
    sd = c.side()
    b = c.p("business")
    T = max(c.dur, 3.0)
    p = {"mixed": ["binoculars", "write", "smoke"], "letters": ["write", "write", "chin"], "lookout": ["binoculars", "port", "binoculars"],
         "rain": ["head", "idle", "chin"], "eating": ["drink", "chin", "drink"]}[b]
    holds = {"write": "paper", "binoculars": "binoculars", "port": "rifle"}
    els = [AID(f"s{i}", sd.soldier, x, 1000, 1.5, p[i], ["tired", "neutral", "sad"][i], holds=holds.get(p[i]), turn=[0.4, 0.1, -0.4][i],
               keys=K((T * (0.4 + i * 0.15), {"pose": ["chin", "idle", "smoke"][i]}))) for i, x in enumerate([480, 960, 1440])]
    if c.variant == "B":
        els.append({**man_path("walk", sd.soldier, [(0, 2060, 1030), (T, 900, 1030)], pose="shoulder", expr="tired"), "flip": True, "front": False})
    shots = [SHOT(0, ["s0", "s1", "s2"], "full", push=0.03), SHOT(T * 0.5, "s1" if c.variant == "A" else "walk", "mediumclose", frameX=0.1, track=c.variant == "B")]
    s = stage(c, {"kind": "trench"}, els, [q for q in shots if q["t"] < c.dur - 0.4])
    if b == "rain":
        s["set"]["weather"] = "rain"
    return s


# ------------------------------------------------------------------ rail
@recipe("rail", "action",
        when="Troops or supplies go by train: 'divisions were sent east…', 'by rail…', 'trains carried…'.",
        not_when="",
        params={"side": Param("side", doc="whose train")},
        variants=("A", "B"),
        shots="A: soldiers walk toward the train as it pulls out, an officer waves them on. B: the train passes close, faces at the windows (wide, shake).",
        example={"at": "Germany had to send divisions east", "recipe": "rail", "says": "Germany had to move whole divisions east by train to rescue Austria.", "side": "german"})
def rail(c):
    sd = c.side()
    T = max(c.dur, 3.0)
    els = []
    y = 740 if c.variant == "A" else 900
    for i in range(5):
        els.append({"id": f"tc{i}", "kind": "vehicle", "type": "locomotive" if i == 0 else "traincar", "nation": sd.nation, "x": 1500 - i * 300, "y": y,
                    "keys": K((0.8, {"x": 1500 - i * 300}), (T, {"x": 2300 - i * 300 + (400 if c.variant == "B" else 0), "ease": "smooth"}))})
    els.append({**FX("smoke", 1560, y - 100, size=0.6), "keys": K((0.8, {"x": 1560}), (T, {"x": 2360 + (400 if c.variant == "B" else 0), "ease": "smooth"}))})
    if c.variant == "A":
        els += [man_path(f"s{i}", sd.soldier, [(0, -150 - i * 210, 1000 + (i % 2) * 50), (T, 700 - i * 210, 800 + (i % 2) * 20)], pose="shoulder", expr="tired") for i in range(5)]
        els.append(AID("of", sd.officer, 1450, 1040, None, "wave", "determined", turn=-0.4, keys=K((T * 0.45, {"pose": "point"}))))
    shots = [SHOT(0, None, "wide", zoom=1.0, push=0.03, panX=120, shake=0.4 if c.variant == "B" else 0)]
    return stage(c, {"kind": "railway"}, els, shots, world=W, sfx=[{"t": 0.6, "id": "train", "dur": T}])


# ------------------------------------------------------------------ river crossing
@recipe("river_crossing", "action",
        when="An assault across water: 'they crossed the river under fire…', 'boats paddled across…'.",
        not_when="",
        params={"side": Param("side", doc="who crosses"), "boats": Param("int", 3, doc="2-4 boats")},
        variants=("A",),
        shots="A: wide of the boats crossing with splashes and tracer from the far bank → closer on the lead boat.",
        example={"at": "the paratroopers crossed the Waal", "recipe": "river_crossing", "says": "American paratroopers rowed across the river under heavy fire.", "side": "american"})
def river_crossing(c):
    sd = c.side()
    T = max(c.dur, 3.0)
    n = max(2, min(4, c.p("boats")))
    els = [{"id": f"b{i}", "kind": "vehicle", "type": "assaultboat", "nation": sd.nation, "x": 260 + i * 330, "y": 730 - i * 45, "scale": round(0.8 - i * 0.08, 2),
            "keys": K((T, {"x": 560 + i * 330}))} for i in range(n)]
    els += [FX("splash", 700 + i * 260, 640 + (i % 2) * 50, **{"in": round(0.8 + i * (T - 1.2) / 4, 2)}) for i in range(4)]
    els += [FX("tracer", 1500, 520, dir=200, **{"in": 0.6})]
    shots = [SHOT(0, None, None, zoom=1.0, push=0.03), SHOT(T * 0.55, None, None, zoom=1.6, x=520, y=690, push=0.04)]
    return stage(c, {"kind": "river"}, els, [q for q in shots if q["t"] < c.dur - 0.4], sfx=[{"t": 0.6, "id": "machinegun", "dur": min(4.0, T - 1)}])


# ------------------------------------------------------------------ paratroops
@recipe("para_drop", "action",
        when="Airborne landings: 'paratroopers dropped…', 'gliders landed…'.",
        not_when="",
        params={"side": Param("side", doc="whose aircraft")},
        variants=("A", "B"),
        shots="A: transports cross the sky and canopies bloom (wide). B: inside the cabin at the green light, then the sky.",
        example={"at": "the first lift dropped", "recipe": "para_drop", "says": "British paratroopers landed far from the bridge.", "side": "british"})
def para_drop(c):
    sd = c.side()
    T = max(c.dur, 3.0)
    if c.variant == "B" and T > 4:
        who = sd.get("para", sd.soldier)
        els = [AID(f"p{i}", who, 500 + i * 300, 1000, 1.5, "idle", ["nervous", "determined", "worried"][i % 3], turn=0.3 - i * 0.2,
                   keys=K((T * 0.5, {"pose": "fist"}))) for i in range(3)]
        return stage(c, {"kind": "cabin", "jumplight": "green"}, els, [SHOT(0, ["p0", "p1", "p2"], "medium"), SHOT(T * 0.5, "p1", "close")])
    els = [{"id": f"d{i}", "kind": "vehicle", "type": "dakota", "nation": sd.nation, "x": -300 - i * 380, "y": 170 + i * 70, "scale": 0.42,
            "keys": K((T + 2, {"x": 1500 - i * 380, "ease": "linear"}))} for i in range(3)]
    els.append({"kind": "paras", "x": 960, "y": 460, "count": 14, "spread": 1500, "fall": 640, "pdur": 6, "in": 1.0})
    return stage(c, {"kind": "heath"}, els, [SHOT(0, None, None, zoom=1.0, push=0.04)], sfx=[{"t": 0, "id": "plane_engine", "dur": T}])
