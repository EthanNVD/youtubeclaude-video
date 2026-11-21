"""Documents, charts, photos, newspapers; the host; sea and air; home front; mood (silhouettes, memorials); chapter titles."""
from __future__ import annotations

import json

from shotlib import AID, DOC, FX, K, L, PROP, SHOT, WOOD_DESK, WORLD, man_path, shells, stretcher_team

from .core import CardError, Param, _where, recipe, stage

W = dict(WORLD)


# ================================================================== documents and numbers (keep short: ≤ 4 s documents, ≤ 7 s charts)
@recipe("document", "device",
        when="The words of a paper matter: an order, a telegram, a treaty clause, a memo, a diary line. ≤ 4 s, then cut to what it causes.",
        not_when="Who reads it matters more (report / decision).",
        params={
            "style": Param("enum", "telegram", ["telegram", "letter", "order", "newspaper", "note", "book"], "kind of paper"),
            "title": Param("str", required=True, doc="heading of the paper (CAPITALS for telegrams/orders)"),
            "lines": Param("list", required=True, doc="1-3 short lines of text (the narration's key words)"),
            "stamp": Param("str", doc="stamp after the text is typed: SECRET, APPROVED, REJECTED, URGENT"),
        },
        variants=("A", "B"),
        shots="A: top-down on a wooden desk, typed line by line, slow push. B: same paper held up in a hand, slight tilt.",
        example={"at": "According to the memoirs", "recipe": "document", "says": "After the war Falkenhayn wrote that he meant to bleed France, not break through.",
                 "style": "letter", "title": "FALKENHAYN — AS HE WROTE AFTER THE WAR", "lines": ["France can be beaten", "without a breakthrough —", "if the French army loses enough men."]})
def document(c):
    lines = c.p("lines") or []
    if not 1 <= len(lines) <= 4:
        raise CardError(f"{_where(c.raw)}: \"lines\" needs 1-3 short lines.")
    speed = max(24, min(60, sum(len(x) for x in lines) / max(1.0, c.dur * 0.6)))
    d = DOC(c.p("style"), c.p("title"), lines, x=960, y=540, w=1000, h=560, at=0.2, speed=round(speed), stamp=c.p("stamp"))
    if c.variant == "B":
        d["rotate"] = -3
    return stage(c, {"kind": "paper", "dof": 0}, list(WOOD_DESK) + [d], [SHOT(0, None, None, zoom=1.0, push=0.07)],
                 sfx=[{"t": 0.2, "id": "typewriter" if c.p("style") in ("telegram", "order") else "paper", "dur": 1.5}])


@recipe("newspaper", "device",
        when="Public reaction / news: 'the papers called it…', 'the headlines…', 'the public learned…'. ≤ 4 s.",
        not_when="",
        params={"headline": Param("str", required=True, doc="the headline (2-6 words)"), "accent": Param("str", doc="one word of the headline shown in yellow"),
                "paper": Param("str", "THE DAILY", doc="newspaper name")},
        variants=("A",), shots="A: the front page spins in and lands on the desk, push.",
        example={"at": "The newspapers called it", "recipe": "newspaper", "says": "British papers celebrated the tank as a war-winner.", "headline": "TANKS SMASH THROUGH", "accent": "TANKS"})
def newspaper(c):
    els = list(WOOD_DESK) + [DOC("newspaper", c.p("paper"), [" ", " ", " ", " "], x=960, y=540, w=1000, h=620, at=0.1, speed=60),
                             {"kind": "headline", "text": c.p("headline"), "accent": c.p("accent"), "x": 960, "y": 520, "size": 88, "in": 0.5}]
    return stage(c, {"kind": "paper", "dof": 0}, els, [SHOT(0, None, None, zoom=1.0, push=0.06)], sfx=[{"t": 0.1, "id": "paper"}])


@recipe("chart", "device",
        when="Two or more numbers must be COMPARED: 'X lost 377,000, Y lost 337,000', 'Britain built twice as many…'. ≤ 7 s.",
        not_when="A single number (put a counter on an action card instead).",
        params={"title": Param("str", required=True, doc="what is compared (CAPITALS)"),
                "items": Param("list", required=True, doc="[{\"label\": \"French\", \"value\": 377000, \"side\": \"french\", \"on\": \"phrase\"}] 2-5 items"),
                "unit": Param("str", "", doc="unit after the numbers")},
        variants=("A",), shots="A: glass tubes on a wooden plaque in the workroom fill one by one on their words.",
        example={"at": "One modern calculation", "recipe": "chart", "says": "Both armies lost over 300,000 men at Verdun.", "title": "VERDUN 1916 — CASUALTIES (ONE ESTIMATE)",
                 "items": [{"label": "French", "value": 377000, "side": "french", "on": "French casualties"}, {"label": "German", "value": 337000, "side": "german", "on": "German casualties"}]})
def chart(c):
    items = c.p("items") or []
    if not 1 <= len(items) <= 5:
        raise CardError(f"{_where(c.raw)}: \"items\" needs 2-5 entries like {{\"label\": \"French\", \"value\": 377000, \"side\": \"french\"}}.")
    its = []
    for k, it in enumerate(items):
        from . import sides as S
        nat = S.side(it["side"], c.era, c.film).nation if it.get("side") else None
        its.append({"label": it["label"], "value": it["value"], **({"nation": nat} if nat else {"color": it.get("color", "#8a6a4a")}),
                    "in": c.t(it.get("on"), 0.15 + k * 0.25, 0.3)})
    el = {"kind": "bars", "title": c.p("title"), "x": 1020, "y": 400, "width": 760, "items": its, "max": max(i["value"] for i in items) * 1.06, "unit": c.p("unit")}
    return stage(c, {"kind": "workshop", "ground": 1000}, [el], [SHOT(0, None, None, zoom=1.0, push=0.05)], ambience="battle")


@recipe("photo_evidence", "device",
        when="Evidence on a desk: a reconnaissance photo, a map with circles, a captured paper being examined.",
        not_when="",
        params={"caption": Param("str", "", doc="caption on the photo"), "ring_on": Param("phrase", doc="word(s) where a red ring circles the key spot")},
        variants=("A",), shots="A: top-down desk, the photo under a magnifier, a red ring drawn on the word.",
        example={"at": "The photographs showed tanks", "recipe": "photo_evidence", "says": "Air photos proved there were German tanks near Arnhem.", "caption": "ARNHEM, 12 SEPT", "ring_on": "tanks"})
def photo_evidence(c):
    tr = c.t(c.p("ring_on"), 0.5, 1.0)
    els = list(WOOD_DESK) + [{**PROP("photo", 960, 540, 4.2), "text": c.p("caption"), "value": 3, "rotate": -3},
                             {**PROP("magnifier", 1260, 640, 2.2), "keys": K((tr - 0.6, {"x": 1180, "y": 600}))},
                             {"kind": "shape", "shape": "ring", "x": 1100, "y": 560, "w": 220, "h": 160, "color": "#c0392b", "strokeWidth": 8, "in": tr, "enter": "draw"}]
    return stage(c, {"kind": "paper", "dof": 0}, els, [SHOT(0, None, None, zoom=1.0, push=0.05), SHOT(max(0.8, tr - 0.3), None, None, zoom=1.6, x=1100, y=560)])


# ================================================================== the host
@recipe("host", "host",
        when="The channel's narrator speaks to the viewer: the opening hook, chapter transitions, the verdict, rhetorical questions ('So, was this the turning point?').",
        not_when="Inside a battle or a historical scene.",
        params={"aide": Param("bool", False, doc="the aide stands beside him and reacts"),
                "mood": Param("enum", "smug", ["smug", "neutral", "determined", "sad", "worried", "happy"], "expression"),
                "close_on": Param("phrase", doc="word(s) where the camera cuts to a close-up (the key line)"),
                "holds": Param("enum", "none", ["none", "stopwatch", "telegram", "paper", "book", "photo", "medal"], "prop in his hand"),
                "setting": Param("str", None, doc="host set (default from cards/_film.json \"host_set\", else study)"),
                "label": Param("str", doc="1-5 word tag at the top")},
        variants=("A", "B"),
        shots="A: medium, he gestures; close-up on the key line. B: full shot with the aide, then a close-up.",
        example={"at": "So, did the sand run out here?", "recipe": "host", "says": "The narrator asks whether this was the decisive moment.", "mood": "smug", "close_on": "Not yet"})
def host(c):
    aide = c.p("aide") or c.variant == "B"
    holds = None if c.p("holds") == "none" else c.p("holds")
    tc = c.t(c.p("close_on"), 0.55, 1.2)
    els = [AID("host", "host", 760 if aide else 960, 960, 1.6, "talk", c.p("mood"), talk=True, holds=holds, holdsScale=0.42, turn=0.25,
               keys=K((tc * 0.6, {"pose": "explain"}), (tc + 0.2, {"pose": "point"})))]
    if aide:
        els.append(AID("aide", "aide", 1260, 975, 1.5, "idle", "neutral", turn=-0.5, keys=K((tc, {"pose": "chin"}))))
    if c.p("label"):
        els.append(L(c.p("label"), 960, 170, "tag", 42, at=0.6, hud=True))
    shots = [SHOT(0, ["host", "aide"] if aide else "host", "full" if aide else "medium", frameX=0 if aide else -0.1, push=0.04)]
    if c.dur > 2.5:
        shots.append(SHOT(tc, "host", "close", frameX=0.12, push=0.04))
    hs = c.p("setting") or c.film.get("host_set") or "study"
    return stage(c, {"kind": hs} if isinstance(hs, str) else hs, els, [q for q in shots if q["t"] < c.dur - 0.5] or shots[:1])


@recipe("device", "device",
        when="The film's recurring scored device is updated (hourglass, scale, scoreboard, meter, ranking, timeline, ledger) — usually at a chapter end.",
        not_when="",
        params={"element": Param("dict", required=True, doc="the device element exactly as in references/plan-schema.md §Storytelling devices (kind + fields)"),
                "host": Param("bool", True, doc="the host stands beside it"),
                "stamp": Param("dict", doc="{\"text\": \"NOT YET\", \"on\": \"phrase\"} stamped beside it")},
        variants=("A",), shots="A: device wide with the host → close on the device as it changes → (stamp).",
        example={"at": "So, did the sand run out", "recipe": "device", "says": "The device shows the war is not yet lost for Germany.",
                 "element": {"kind": "meter", "value": -0.2, "left": "LOST", "right": "WON", "title": "GERMANY'S CHANCES"}})
def device(c):
    el = dict(c.p("element"))
    el.setdefault("x", 760 if c.p("host") else 960)
    el.setdefault("y", 500)
    el["id"] = "dev"
    els = [el]
    if c.p("host"):
        els.append(AID("host", "host", 1500, 1000, 1.55, "point", "neutral", turn=-0.45, talk=True))
    shots = [SHOT(0, None, None, zoom=1.0, push=0.04)]
    if c.dur > 3:
        shots.append(SHOT(c.dur * 0.35, None, None, zoom=1.5, x=el["x"], y=el["y"], push=0.04))
    return stage(c, {"kind": "workshop", "ground": 1000}, els, shots)


@recipe("chapter_title", "device",
        when="A chapter opens with its title card (only if the film uses title cards; usually the date badge on the first scene is enough).",
        not_when="",
        params={"title": Param("str", required=True, doc="chapter title"), "subtitle": Param("str", "", doc="date or place")},
        variants=("A",), shots="A: title card.",
        example={"at": "Chapter three", "recipe": "chapter_title", "says": "A new chapter about Verdun begins here.", "title": "BLEEDING", "subtitle": "1916"})
def chapter_title(c):
    return {"start": round(c.start, 2), "type": "chapter", "title": c.p("title"), "subtitle": c.p("subtitle"), "elements": []}


# ================================================================== sea
@recipe("naval_battle", "action",
        when="Fleets fight: 'the fleets met…', 'the battlecruisers exchanged fire…', 'the guns of the fleet…'.",
        not_when="One ship sinking (sinking); submarines (submarine_attack).",
        params={"side": Param("side", doc="first fleet"), "enemy": Param("side", doc="second fleet"), "hit_on": Param("phrase", doc="word(s) where a ship is hit"),
                "time": Param("enum", "day", ["day", "dusk", "night"], "time")},
        variants=("A", "B"),
        shots="A: line of ships firing (wide) → splashes around the enemy → closer on the hit ship. B: on the deck/bridge first (the gun fires), then the wide.",
        example={"at": "the two fleets met off Jutland", "recipe": "naval_battle", "says": "The British and German fleets fought the war's only great sea battle.", "side": "british", "enemy": "german"})
def naval_battle(c):
    sd, en = c.side(), c.side("enemy")
    T = max(c.dur, 3.0)
    th = c.t(c.p("hit_on"), 0.6, 1.5)
    els = []
    for i in range(3):
        x, y = 260 + i * 260, 640 + i * 40
        els.append({"id": f"a{i}", "kind": "vehicle", "type": sd.ship if i == 0 else "cruiser", "nation": sd.nation, "x": x, "y": y, "scale": round(0.36 + i * 0.05, 2),
                    "keys": K((T, {"x": x + 90 * T / 7, "ease": "linear"})), "fireAt": [round(0.5 + i * 0.6, 2), round(T * 0.55 + i * 0.4, 2)]})
    els.append({"id": "e0", "kind": "vehicle", "type": en.ship, "nation": en.nation, "x": 1560, "y": 600, "scale": 0.3, "flip": True,
                "keys": K((T, {"x": 1480, "ease": "linear"})), "fireAt": [1.2, round(T * 0.7, 2)]})
    els += [FX("splash", 1480 + k * 70, 610 + (k % 2) * 20, **{"in": round(1.0 + k * 0.7, 2)}) for k in range(3)]
    els.append({**FX("explosion", 1560, 570, size=0.6), "in": th})
    els.append({**FX("smoke", 1560, 560, size=0.7), "in": th + 0.2})
    if c.variant == "B" and T > 4:
        # on the bridge of the flagship: the officer watches through binoculars, the shell lands, he shouts the order
        crew = [AID("o", sd.officer, 1100, 1000, 1.6, "binoculars", "determined", turn=-0.3, keys=K((th, {"pose": "point", "expr": "shout"}))),
                AID("s", sd.sailor, 620, 1010, 1.5, "idle", "worried", turn=0.4, keys=K((th + 0.3, {"pose": "head", "expr": "shocked"})))]
        return stage(c, {"kind": "bridge", "nation": sd.nation}, crew, [SHOT(0, ["o", "s"], "medium"), SHOT(max(1.0, th - 0.3), "o", "close", frameX=0.12)],
                     impacts=[th], sfx=[{"t": th, "id": "cannon"}])
    shots = [SHOT(0, None, None, zoom=1.0, push=0.03), SHOT(max(1.0, th - 0.3), None, None, zoom=1.8, x=1540, y=580, push=0.04)]
    return stage(c, {"kind": "sea", "time": c.p("time")}, els, [q for q in shots if q["t"] < c.dur - 0.4], impacts=[th])


@recipe("sinking", "action",
        when="A ship is sunk: 'the Lusitania went down…', 'three battlecruisers blew up…', 'the ship sank in minutes'.",
        not_when="",
        params={"side": Param("side", doc="whose ship sinks"), "ship": Param("enum", None, ["battleship", "cruiser", "destroyer", "cargo", "freighter", "carrier"], "ship type (default: the side's capital ship)"),
                "hit_on": Param("phrase", doc="word(s) where it is hit"), "time": Param("enum", "day", ["day", "dusk", "night"], "time")},
        variants=("A",),
        shots="A: the ship is hit (flash, fire), lists and slides under, smoke; splashes of men in the water; slow push. Symbolic: debris stays.",
        example={"at": "The Lusitania sank in eighteen minutes", "recipe": "sinking", "says": "A German submarine sank a liner full of civilians.", "side": "british", "ship": "cargo"})
def sinking(c):
    sd = c.side()
    T = max(c.dur, 3.0)
    th = c.t(c.p("hit_on"), 0.2, 0.5)
    typ = c.p("ship") or sd.ship
    ship = {"id": "s", "kind": "vehicle", "type": typ, "nation": sd.nation, "x": 900, "y": 640, "scale": 0.5, "rotate": 0,
            "keys": K((th, {"rotate": 0}), (th + 0.3, {"burning": True, "damaged": True}), (T, {"rotate": 12, "y": 760, "ease": "in"}))}
    els = [ship, {**FX("explosion", 960, 600, size=0.9), "in": th}, {**FX("smoke", 960, 560, size=1.0), "in": th + 0.3},
           {**FX("fire", 880, 600, size=0.6), "in": th + 0.4}]
    els += [FX("splash", 700 + k * 120, 690 + (k % 2) * 20, **{"in": round(th + 1.0 + k * 0.5, 2)}) for k in range(4)]
    els.append({"kind": "shape", "shape": "rect", "x": 960, "y": 1000, "w": 2400, "h": 300, "fill": "#3e5f7a", "stroke": "#3e5f7a", "opacity": 0.0, "enter": "none"})
    return stage(c, {"kind": "sea", "time": c.p("time")}, els, [SHOT(0, None, None, zoom=1.0, push=0.05)], impacts=[th])


@recipe("submarine_attack", "action",
        when="Submarine warfare: 'U-boats sank…', 'a torpedo struck…', 'unrestricted submarine warfare…'.",
        not_when="",
        params={"side": Param("side", doc="whose submarine"), "target": Param("side", doc="whose ship is hit"), "hit_on": Param("phrase", doc="word(s) of the torpedo hit")},
        variants=("A", "B"),
        shots="A: the U-boat surfaces/runs in the foreground, a torpedo wake runs to the freighter, the hit, smoke. B: the captain at the periscope (close), then the hit.",
        example={"at": "U-boats sank", "recipe": "submarine_attack", "says": "German submarines began sinking merchant ships without warning.", "side": "german", "target": "british"})
def submarine_attack(c):
    sd, tg = c.side(), c.side("target")
    T = max(c.dur, 3.0)
    th = c.t(c.p("hit_on"), 0.6, 1.5)
    if c.variant == "B" and T > 4:
        cap = "uboat_captain" if sd.name == "german" else sd.officer
        els = [AID("cap", cap, 960, 1000, 1.7, "binoculars", "determined", turn=-0.2, keys=K((th, {"expr": "smug", "pose": "fist"})))]
        return stage(c, {"kind": "radio" if sd.era == "ww1" else "bunker"}, els, [SHOT(0, "cap", "mediumclose"), SHOT(th, "cap", "close")])
    els = [{"id": "u", "kind": "vehicle", "type": sd.sub, "nation": sd.nation, "x": 420, "y": 760, "scale": 0.55, "keys": K((T, {"x": 560, "ease": "linear"}))},
           {"id": "f", "kind": "vehicle", "type": "cargo", "nation": tg.nation, "x": 1450, "y": 620, "scale": 0.32, "flip": True,
            "keys": K((th + 0.3, {"burning": True, "damaged": True}), (T, {"y": 660, "rotate": 6, "ease": "in"}))},
           {"kind": "line", "path": [[600, 760], [1420, 640]], "color": "#e8f2f6", "width": 4, "dashed": True, "screen": True, "in": max(0.2, th - 1.5), "dur": 1.4, "enter": "draw"},
           {**FX("explosion", 1450, 600, size=0.7), "in": th}, {**FX("smoke", 1450, 580, size=0.8), "in": th + 0.3}]
    return stage(c, {"kind": "sea"}, els, [SHOT(0, None, None, zoom=1.0, push=0.04), SHOT(th + 0.4, None, None, zoom=1.8, x=1430, y=600)], impacts=[th])


# ================================================================== air
@recipe("air_battle", "action",
        when="Aircraft fight: 'the RAF fought off…', 'dogfights over…', 'fighters attacked the bombers'.",
        not_when="Bombs falling on a city (bombing).",
        params={"side": Param("side", doc="first side's fighters"), "enemy": Param("side", doc="the enemy aircraft"), "hit_on": Param("phrase", doc="word(s) where one is hit")},
        variants=("A", "B"),
        shots="A: fighters cross the sky with tracers, one enemy trails smoke and falls. B: the pilot in the cockpit first (close), then the sky.",
        example={"at": "Fighters rose to meet them", "recipe": "air_battle", "says": "British fighters attacked the German bomber formations.", "side": "british", "enemy": "german"})
def air_battle(c):
    sd, en = c.side(), c.side("enemy")
    T = max(c.dur, 3.0)
    th = c.t(c.p("hit_on"), 0.55, 1.2)
    if c.variant == "B" and T > 4 and sd.get("pilot"):
        els = [AID("pl", sd.pilot, 960, 1000, 1.8, "aim", "determined", turn=0.2, keys=K((th, {"expr": "shout", "pose": "fist"})))]
        return stage(c, {"kind": "cockpit", "bank": 8}, els, [SHOT(0, "pl", "mediumclose"), SHOT(th, "pl", "close")], sfx=[{"t": 0, "id": "plane_engine", "dur": T}])
    els = [{"id": f"f{i}", "kind": "vehicle", "type": "fighter", "nation": sd.nation, "x": -200 - i * 260, "y": 380 + i * 110, "scale": 0.5,
            "keys": K((T, {"x": 1500 - i * 260, "ease": "linear"}))} for i in range(2)]
    els += [{"id": f"e{i}", "kind": "vehicle", "type": en.bomber if i == 0 else en.plane, "nation": en.nation, "x": 1700 - i * 300, "y": 260 + i * 160, "scale": 0.45, "flip": True,
             "keys": K((th, {"x": 1700 - i * 300 - 420 * th / T}), (T, {"x": 900 - i * 300, "y": 260 + i * 160 + (420 if i == 0 else 0), "rotate": -22 if i == 0 else 0, "ease": "in"}))} for i in range(2)]
    els += [FX("tracer", 240, 420, dir=-6, **{"in": 0.5}), {**FX("smoke", 1500, 270, size=0.6), "in": th}, {**FX("explosion", 1480, 260, size=0.4), "in": th}]
    return stage(c, {"kind": "sky", "below": "sea"}, els, [SHOT(0, None, None, zoom=1.0, push=0.03)], sfx=[{"t": 0, "id": "plane_flyby"}, {"t": 0.5, "id": "machinegun", "dur": 1.5}])


@recipe("bombing", "action",
        when="Bombs on a city, port or factory: 'the Blitz…', 'Dresden was bombed…', 'bombers struck…'.",
        not_when="",
        params={"side": Param("side", doc="whose bombers"), "time": Param("enum", "night", ["day", "dusk", "night"], "time"), "civilians": Param("bool", True, doc="civilians running for shelter")},
        variants=("A", "B"),
        shots="A: bombers overhead, bombs falling, bursts in the street, fires (wide) → civilians running. B: civilians look up first (close), then the bursts.",
        example={"at": "Night after night the bombers came", "recipe": "bombing", "says": "German bombers hit London for months during the Blitz.", "side": "german"})
def bombing(c):
    sd = c.side()
    T = max(c.dur, 3.0)
    els = [{"id": f"b{i}", "kind": "vehicle", "type": sd.bomber, "nation": sd.nation, "x": -300 - i * 380, "y": 150 + i * 60, "scale": 0.38,
            "keys": K((T + 2, {"x": 1600 - i * 380, "ease": "linear"}))} for i in range(3)]
    pts = [(round(0.8 + k * (T - 1.2) / 4, 2), 500 + k * 280, 860 + (k % 2) * 40) for k in range(4)]
    b, imp = shells(pts, size=1.4, kind="explosion")
    els += b + [{**FX("fire", 700, 860, size=0.8), "in": pts[0][0] + 0.3}, {**FX("searchlight", 400, 900), "in": 0} if c.p("time") == "night" else None]
    if c.p("civilians"):
        els += [{**man_path(f"c{i}", ["civilian_man", "civilian_woman"][i % 2], [(0.3, 1700 + i * 150, 980 + (i % 2) * 40), (T, 300 + i * 150, 980 + (i % 2) * 40)],
                            pose="head", expr="panic", holds="", run=True), "flip": True} for i in range(3)]
    shots = ([SHOT(0, None, None, zoom=1.0, push=0.03), SHOT(T * 0.6, "b0", "medium", track=True)] if not c.p("civilians") else
             [SHOT(0, None, None, zoom=1.0, push=0.03), SHOT(T * 0.6, "c0", "mediumclose", track=True)] if c.variant == "A" else
             [SHOT(0, "c0", "mediumclose"), SHOT(1.2, None, None, zoom=1.0, push=0.03)])
    return stage(c, {"kind": "city", "ruined": True}, [e for e in els if e], [q for q in shots if q["t"] < c.dur - 0.4], world={"scale": 0.9, "y": 900, "horizon": 700},
                 impacts=imp, sfx=[{"t": 0, "id": "plane_engine", "dur": T}])


@recipe("airfield", "action",
        when="Pilots and planes on the ground: 'the squadrons were scrambled…', 'pilots waited…', 'the raid took off'.",
        not_when="",
        params={"side": Param("side", doc="whose airfield"), "scramble": Param("bool", True, doc="pilots run to the planes")},
        variants=("A",), shots="A: pilots run past a parked fighter, a plane starts its engine.",
        example={"at": "The squadrons were scrambled", "recipe": "airfield", "says": "RAF pilots ran to their fighters as radar spotted the raid.", "side": "british"})
def airfield(c):
    sd = c.side()
    T = max(c.dur, 3.0)
    pilot = sd.get("pilot", sd.soldier)
    els = [{"kind": "vehicle", "type": "fighter", "nation": sd.nation, "x": 640, "y": 890, "parked": True},
           {"kind": "vehicle", "type": "fighter", "nation": sd.nation, "x": 1500, "y": 760, "parked": True}]
    els += [{**man_path(f"p{i}", pilot, [(0, 1900 + i * 160, 960 + i * 40), (T, 900 + i * 160, 960 + i * 40)], pose="idle", expr="determined", holds="",
                        run=bool(c.p("scramble"))), "flip": True} for i in range(3)]
    return stage(c, {"kind": "airfield", "nation": sd.nation, "planes": 0}, els, [SHOT(0, None, None, zoom=1.0, push=0.03), SHOT(T * 0.55, "p0", "mediumclose", track=True)],
                 world={"scale": 0.62, "y": 880})


# ================================================================== home front
@recipe("home_front", "action",
        when="Civilians at home: hunger, rationing, waiting for news, a death telegram: 'the Turnip Winter…', 'families went hungry…', 'the telegram every mother feared'.",
        not_when="",
        params={"beat": Param("enum", "hunger", ["hunger", "telegram", "queue", "letter"], "which home-front moment"),
                "side": Param("side", doc="whose home (flag/uniform in the photo)")},
        variants=("A", "B"),
        shots="hunger: a mother puts a turnip on the plate, the child's face falls. telegram: a woman opens the door to a messenger, reads, covers her face. "
              "queue: a line of women in the street waiting for bread. letter: a soldier's family reads a letter by candlelight.",
        example={"at": "That winter, Germans ate turnips", "recipe": "home_front", "says": "The blockade left German families with almost nothing but turnips.", "beat": "hunger", "side": "german"})
def home_front(c):
    T = max(c.dur, 3.0)
    b = c.p("beat")
    if b == "hunger":
        els = [AID("mother", "civilian_woman", 1180, 1060, 1.95, "carry", "sad", holds="turnip", holdsScale=0.6, turn=-0.4,
                   keys=K((T * 0.25, {"pose": "offer"}), (T * 0.4, {"pose": "idle", "holds": ""}), (T * 0.65, {"pose": "chin"}))),
               AID("child", "civilian_man", 720, 1060, 1.6, "idle", "neutral", turn=0.4, look_={"age": 0.0, "build": 0.85}, keys=K((T * 0.45, {"expr": "sad"}), (T * 0.8, {"pose": "chin"}))),
               {**PROP("turnip", 950, 845, 0.55), "front": True, "in": T * 0.38}]
        return stage(c, {"kind": "kitchen", "desk": False, "fg": "officedesk", "time": "dusk"}, els,
                     [SHOT(0, ["mother", "child"], "full", push=0.03), SHOT(T * 0.42, "child", "close", frameX=-0.12)], tint="cold")
    if b == "telegram":
        els = [AID("m", c.side().officer, 1400, 1000, 1.55, "offer", "sad", holds="telegram", turn=-0.4, keys=K((T * 0.25, {"pose": "idle", "holds": ""}))),
               AID("w", "civilian_woman", 800, 1000, 1.6, "idle", "worried", turn=0.4, keys=K((T * 0.25, {"pose": "show", "holds": "telegram"}), (T * 0.55, {"pose": "face", "expr": "cry", "holds": ""})))]
        return stage(c, {"kind": "street"}, els, [SHOT(0, ["m", "w"], "full"), SHOT(T * 0.5, "w", "close", frameX=0.12)], tint="grey")
    if b == "queue":
        els = [AID(f"q{i}", ["civilian_woman", "civilian_man"][i % 3 == 2], 300 + i * 260, 980 + (i % 2) * 20, 1.4, ["idle", "chin", "cross", "pockets"][i % 4],
                   ["tired", "sad", "worried"][i % 3], turn=0.5, keys=K((T * (0.3 + i * 0.07), {"pose": "chin"}))) for i in range(6)]
        return stage(c, {"kind": "street", "weather": "snow"}, els, [SHOT(0, None, None, zoom=1.0, push=0.04), SHOT(T * 0.55, "q2", "close", frameX=0.12)], tint="cold")
    els = [AID("w", "civilian_woman", 760, 1000, 1.6, "hold", "sad", holds="paper", turn=0.3), AID("o", "civilian_man", 1200, 1000, 1.5, "chin", "worried", turn=-0.4, look_={"age": 0.8}),
           {**PROP("candle", 980, 870, 0.9), "front": True}]
    return stage(c, {"kind": "home", "desk": False, "fg": "officedesk", "time": "night"}, els, [SHOT(0, ["w", "o"], "medium"), SHOT(T * 0.5, "w", "close")])


@recipe("factory", "action",
        when="War production: 'factories turned out shells…', 'women took the men's jobs…', 'production doubled'.",
        not_when="",
        params={"product": Param("enum", "shells", ["shells", "tanks", "planes"], "what is made"), "side": Param("side", doc="whose factory")},
        variants=("A",), shots="A: workers carry and stack shells along the line (wide) → close on a tired worker.",
        example={"at": "factories worked day and night", "recipe": "factory", "says": "Britain's factories produced shells around the clock.", "product": "shells", "side": "british"})
def factory(c):
    T = max(c.dur, 3.0)
    els = [AID("w1", "worker", 560, 1000, 1.5, "typing", "tired", turn=0.3), AID("w2", "civilian_woman", 1000, 1000, 1.5, "carry", "tired", holds="shell",
                                                                                    keys=K((T * 0.5, {"x": 1200}), (T * 0.7, {"pose": "reach", "holds": ""}))),
           AID("w3", "worker", 1440, 1000, 1.45, "typing", "sad", turn=-0.3, look_={"age": 0.05}), {**PROP("crate", 1350, 960, 1.2), "text": "SHELLS"}]
    return stage(c, {"kind": "factory"}, els, [SHOT(0, ["w1", "w3"], "full"), SHOT(T * 0.5, "w2", "close", frameX=0.1)], ambience="factory")


@recipe("crowd", "action",
        when="Crowds: celebration ('the armistice was celebrated…'), protest or strikes ('workers went on strike…'), volunteers ('men rushed to enlist…').",
        not_when="A leader's speech (speech).",
        params={"mood": Param("enum", "celebrate", ["celebrate", "protest", "enlist", "mourn"], "what the crowd does"), "side": Param("side", doc="whose country (flags)")},
        variants=("A",), shots="A: wide street full of people with the action, then a close face.",
        example={"at": "In London, crowds filled", "recipe": "crowd", "says": "Londoners poured into the streets to celebrate the armistice.", "mood": "celebrate", "side": "british"})
def crowd(c):
    T = max(c.dur, 3.0)
    mood = c.p("mood")
    pose, expr = {"celebrate": ("cheer", "happy"), "protest": ("fist", "angry"), "enlist": ("salute", "determined"), "mourn": ("face", "sad")}[mood]
    els = [AID(f"c{i}", ["civilian_man", "civilian_woman", "worker"][i % 3], 200 + i * 220, 960 + (i % 3) * 50, None, "idle", "neutral", turn=0.3 - (i % 3) * 0.3,
               keys=K((0.3 + (i % 4) * 0.25, {"pose": pose, "expr": expr}))) for i in range(8)]
    if mood == "celebrate":
        els.append({**FX("fireworks", 960, 300), "in": 0.5})
    st = {"kind": "street"}
    if mood in ("celebrate", "enlist"):
        st = {"kind": "rally", "flag": c.side().nation}
    return stage(c, st, els, [SHOT(0, None, None, zoom=1.0, push=0.04), SHOT(T * 0.55, "c3", "close")], world={"scale": 1.2, "y": 900, "horizon": 700},
                 ambience="crowd", sfx=[{"t": 0.4, "id": "cheer"}] if mood == "celebrate" else None)


# ================================================================== mood
@recipe("silhouette", "action",
        when="A grief or endurance beat over a big number or a long time: '70,000 men a month…', 'for most of a year…', 'a whole generation'.",
        not_when="",
        params={"side": Param("side", doc="whose men"), "what": Param("enum", "stretcher", ["stretcher", "column", "crosses"], "what crosses the ridge")},
        variants=("A",), shots="A: one dusk wide: black figures on the ridge against the sun, crosses appearing one by one in the foreground.",
        example={"at": "That's roughly seventy thousand men", "recipe": "silhouette", "says": "Verdun consumed about seventy thousand men every month.",
                 "side": "french", "label": {"text": "≈ 70,000 MEN A MONTH", "on": "seventy thousand"}})
def silhouette(c):
    sd = c.side()
    T = max(c.dur, 3.0)
    what = c.p("what")
    els = []
    if what == "stretcher":
        els += stretcher_team("b0", sd.soldier, 330, 1230, 900, T, scale=1.3, silhouette=True) + stretcher_team("b1", sd.soldier, -470, 380, 905, T, scale=1.1, silhouette=True)
    if what in ("stretcher", "column"):
        for i in range(4 if what == "stretcher" else 7):
            e = man_path(f"r{i}", sd.soldier, [(0, 2000 + i * 130, 880), (T, 1300 + i * 130 - (500 if what == "column" else 0), 880)], pose="shoulder", expr="tired", flip=True, silhouette=True)
            e["scale"] = 0.72 if what == "stretcher" else 1.0
            els.append(e)
    n = 7 if what != "crosses" else 9
    els += [{**PROP("cross", 180 + i * (1600 // (n - 1)), 1090 + (i % 2) * 30, 1.1), "in": round(0.4 + i * (T - 1.0) / n, 2), "enter": "place", "silhouette": True} for i in range(n)]
    return stage(c, {"kind": "nomansland", "time": "dusk", "wire": False, "horizon": 880}, els, [SHOT(0, None, None, zoom=1.0, push=0.04, panX=-60)], tint="warm")


@recipe("memorial", "device",
        when="A quiet, serious hold: the dead remembered, the verdict's human cost, the end of a war. 6-12 s, no hurry.",
        not_when="",
        params={"what": Param("enum", "crosses", ["crosses", "candle", "helmet"], "the image")},
        variants=("A",), shots="A: grey/dark, slow push on the image.",
        example={"at": "In memory of", "recipe": "memorial", "says": "The film pauses for the millions who died.", "what": "candle"})
def memorial(c):
    w = c.p("what")
    if w == "candle":
        els = [{**PROP("candle", 960, 760, 2.4), "on": True}]
        st = {"kind": "dark"}
    elif w == "helmet":
        els = [PROP("helmet", 960, 900, 2.2), {**PROP("cross", 960, 860, 2.0), "rotate": 0}]
        st = {"kind": "nomansland", "time": "dusk", "wire": False}
    else:
        els = [{**PROP("cross", 200 + i * 190, 900 + (i % 2) * 50, 1.3), "in": 0.2 + i * 0.25, "enter": "place"} for i in range(9)]
        st = {"kind": "memorial"}
    s = stage(c, st, els, [SHOT(0, None, None, zoom=1.0, push=0.06)], ambience="wind")
    s["tint"] = "grey"
    return s


# ================================================================== escape hatch
@recipe("raw", "action",
        when="ONLY when no recipe can show the moment and you know the engine schema (playbook/08-advanced.md). Strong models only.",
        not_when="Any recipe fits — recipes are tested; raw scenes are not.",
        params={"scene": Param("dict", required=True, doc="an engine scene without start/end/id: {\"type\": \"stage\", \"set\": {...}, \"elements\": [...], \"shots\": [...], \"world\": {...}} (references/plan-schema.md)"),
                "class": Param("enum", "action", ["action", "talk", "map", "device", "host"], "what it counts as in the screen-time mix")},
        variants=("A",), shots="Whatever the scene says.",
        example={"at": "and so the story", "recipe": "raw", "says": "A custom scene built by hand for a moment no recipe covers.",
                 "scene": {"type": "stage", "set": {"kind": "harbor", "time": "dusk"}, "elements": [{"kind": "vehicle", "type": "cargo", "nation": "UK", "x": 900, "y": 640, "scale": 0.5}],
                           "shots": [{"t": 0, "zoom": 1.0, "push": 0.04}]}})
def raw(c):
    s = json.loads(json.dumps(c.p("scene")))
    for k in ("start", "end", "id"):
        s.pop(k, None)
    s["start"] = round(c.start, 2)
    s.setdefault("type", "stage")
    s.setdefault("elements", [])
    return s
