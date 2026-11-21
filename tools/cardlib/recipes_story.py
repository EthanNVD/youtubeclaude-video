"""Story recipes: the documentary-film grammar measured on the reference channel (projects/ember-test/ANALYSIS.md).

A film is told through PEOPLE in PLACES. A place is introduced from outside (establish), we follow people into it
(approach), we find someone at work who is interrupted (interrupt), people clash (confront), someone is left alone with the
news (contemplate). At the front we watch what is coming (watch_front), see it through binoculars (binocular_view), stand on
a ridge looking at the goal (vista). Loss is shown by an empty place (absence). A teacher frames the debate (lecture).
Every recipe here is ACTED: somebody does something the narration says, in a real place, with a slow push and dissolves.
"""
from __future__ import annotations

from shotlib import AID, FX, K, PROP, SHOT, WORLD, man_path

from .core import CardError, Param, _where, recipe, stage

W = dict(WORLD)
MOOD = ["neutral", "worried", "determined", "sad", "shocked", "angry", "tired", "smug", "happy", "panic"]
ROOMS = ["office", "study", "warroom", "cabinet", "conference", "bunker", "tent", "radio", "codebreak", "hotel", "home", "kitchen", "train_interior", "bridge"]
OUTSIDE = ["hotel", "street", "city", "ruins", "railway", "station", "harbor", "dock", "countryside", "field", "snow", "desert", "airfield", "garden", "polder", "heath", "steppe", "nomansland", "jungle"]


def _people(c, key, lo=0, hi=4):
    lst = c.p(key) or []
    if not isinstance(lst, list) or not (lo <= len(lst) <= hi):
        raise CardError(f"{_where(c.raw)}: \"{key}\" needs a list of {lo}-{hi} cast ids, e.g. [\"hindenburg\", \"ludendorff\"].")
    for w in lst:
        c.raw["_tmp"] = w
        c.person("_tmp")
    c.raw.pop("_tmp", None)
    return lst


def _room(kind, flag=None, desk=True):
    st = {"kind": kind}
    if kind in ("office", "study", "cabinet", "conference", "home", "kitchen"):
        st["desk"] = False
        if desk:
            st["fg"] = "officedesk"
    elif desk and kind in ("warroom", "bunker", "tent", "radio", "codebreak"):
        st["fg"] = "officedesk"
    if flag and kind in ("office", "study", "bunker"):
        st["flag"] = flag
        st["portrait"] = True
    return st


# ------------------------------------------------------------------ establish
@recipe("establish", "action",
        when="The story arrives at a new place or a new day: 'On the 29th of September 1918…', 'In Berlin…', 'That morning at headquarters…'. "
             "The FIRST card of every new place. Put the place/time `tag` on it.",
        not_when="We are already in this place (go straight to the people: approach / interrupt / decision).",
        params={
            "setting": Param("enum", "street", OUTSIDE, "the outside of the place"),
            "arrive": Param("enum", "car", ["car", "walk", "none", "train", "ship"], "how people arrive (none = life goes on: passers-by)"),
            "who": Param("list", doc="0-3 cast ids who arrive (they get out of the car / walk in)"),
            "guard": Param("bool", True, doc="a sentry at the door who presents arms when they arrive"),
            "side": Param("side", doc="side of the sentry / vehicles / passers-by"),
        },
        variants=("A", "B"),
        shots="A: wide of the place with a slow push; the arrival happens in it; dissolve to a full shot following the arrivals. "
              "B: the arrivals walk from the foreground toward the building (depth), wide only.",
        example={"at": "On the 29th of September", "recipe": "establish", "says": "Germany's two top generals arrive at headquarters at dawn to see the Kaiser.",
                 "setting": "hotel", "arrive": "car", "who": ["hindenburg", "ludendorff"], "side": "german", "time": "dawn",
                 "place_id": "spa_hq", "tag": "Spa, Belgium · 29 September 1918", "tag_on": "1918"})
def establish(c):
    sd = c.side()
    who = _people(c, "who", 0, 3)
    arrive = c.p("arrive")
    T = max(c.dur, 3.0)
    els, shots = [], [SHOT(0, None, None, zoom=1.0, push=0.05)]
    ta = min(3.2, T * 0.45)
    if arrive == "car":
        els.append({"id": "car", "kind": "vehicle", "type": "car", "nation": sd.nation, "x": -300, "y": 930, "keys": K((ta, {"x": 640}))})
    elif arrive == "train":
        els += [{"id": f"tc{i}", "kind": "vehicle", "type": "locomotive" if i == 0 else "traincar", "nation": sd.nation, "x": 2400 - i * 300, "y": 760,
                 "keys": K((ta, {"x": 1500 - i * 300}))} for i in range(4)]
    elif arrive == "ship":
        els.append({"id": "ship", "kind": "vehicle", "type": "cargo", "nation": sd.nation, "x": -200, "y": 640, "scale": 0.45, "keys": K((T, {"x": 700}))})
    if c.p("guard") and c.p("setting") not in ("countryside", "field", "steppe", "desert", "jungle", "nomansland", "heath", "polder", "snow"):
        els.append(AID("guard", sd.soldier, 1500, 905, None, "port", "neutral", holds="rifle", turn=-0.4,
                       keys=K((ta - 0.2, {"pose": "salute", "holds": ""}))))
    ids = []
    for i, w in enumerate(who):
        if arrive in ("car", "train", "ship"):
            x0 = 600 + i * 100 if arrive == "car" else 900 + i * 120
            els.append({**man_path(f"p{i}", w, [(ta + 0.4 + i * 0.3, x0, 940 + i * 8), (T, x0 + 460, 900 + i * 4)], pose="idle", expr="neutral", holds=""),
                        "in": ta + 0.2 + i * 0.3})
        else:
            x0 = 520 + i * 140
            els.append(man_path(f"p{i}", w, [(0, x0, 1160 + i * 10), (T, x0 + 280, 930 + i * 6)], pose="idle", expr="neutral", holds="", view="back"))
        ids.append(f"p{i}")
    if arrive == "none":
        els += [{**man_path(f"c{i}", ["civilian_man", "civilian_woman", "worker"][i % 3], [(0, -100 - i * 260, 930 + (i % 2) * 30), (T, 700 - i * 260 + 300, 930 + (i % 2) * 30)],
                            pose="idle", expr="neutral", holds="")} for i in range(3)]
    if ids and c.variant == "A" and T > ta + 1.6:
        shots.append(SHOT(ta + 0.8, ids + (["guard"] if any(e.get("id") == "guard" for e in els) else []), "full", track=True, push=0.03))
    return stage(c, {"kind": c.p("setting"), "drift": 0}, els, shots, world={"scale": 1.05, "y": 940})


# ------------------------------------------------------------------ approach
@recipe("approach", "action",
        when="People on their way to something important: 'the two men went to see the emperor', 'he was summoned', 'the delegates walked in'. "
             "Use it with name cards when important people first appear.",
        not_when="They have already arrived (interrupt / dialogue / meeting).",
        params={
            "who": Param("list", required=True, doc="1-3 cast ids walking toward the camera (first = left)"),
            "setting": Param("enum", "corridor", ["corridor", "street", "railway", "station", "garden", "hotel", "airfield", "dock", "field", "snow"], "where they walk"),
            "carry": Param("enum", "folder", ["folder", "telegram", "suitcase", "none"], "what the second person carries"),
            "bystander": Param("bool", True, doc="an officer / clerk at the side who salutes or steps aside as they pass"),
            "side": Param("side", doc="side of the bystander"),
            "mood": Param("enum", "determined", MOOD, "their faces"),
        },
        variants=("A", "B"),
        shots="A: one depth shot — they grow toward the lens (corridor/street), bystander salutes. B: start on their feet/faces close, dissolve to the depth shot.",
        example={"at": "Field Marshal Paul von Hindenburg", "recipe": "approach", "says": "The two generals stride toward the Kaiser's study with the bad news.",
                 "who": ["hindenburg", "ludendorff"], "setting": "corridor", "carry": "folder", "name_card": "hindenburg", "place_id": "spa_hq"})
def approach(c):
    who = _people(c, "who", 1, 3)
    T = max(c.dur, 2.6)
    hz = 500 if c.p("setting") == "corridor" else 640 if c.p("setting") in ("railway", "station") else 600
    els = []
    for i, w in enumerate(who):
        x0 = 900 + (i - (len(who) - 1) / 2) * 140
        holds = None if c.p("carry") == "none" or i != min(1, len(who) - 1) else c.p("carry")
        els.append(man_path(f"p{i}", w, [(0, x0, hz + 140), (T * 0.95, x0 + (i - (len(who) - 1) / 2) * 90, 1015 + i * 6)],
                            pose="hold" if holds else "idle", expr=c.p("mood"), holds=holds or ""))
    if c.p("bystander"):
        els.append(AID("by", c.side().officer, 1430, hz + 260, None, "idle", "nervous", turn=-0.5, keys=K((T * 0.3, {"pose": "salute"}))))
    shots = [SHOT(0, None, None, zoom=1.0, push=0.05)]
    if c.variant == "B" and T > 3:
        shots = [SHOT(0, "p0", "mediumclose", frameX=0.1), SHOT(min(1.4, T * 0.4), None, None, zoom=1.0, push=0.05)]
    return stage(c, {"kind": c.p("setting"), "doors": ["", ""]} if c.p("setting") == "corridor" else {"kind": c.p("setting")}, els, shots,
                 world={"scale": 1.3, "y": 900, "horizon": hz}, sfx=[{"t": 0.1, "id": "footsteps", "dur": min(4.0, T)}])


# ------------------------------------------------------------------ interrupt
@recipe("interrupt", "talk",
        when="Someone is told / receives the news while doing his work: 'they told the Kaiser…', 'the report reached Churchill at his desk…'. "
             "The listener's BUSINESS (writing, reading, phoning) stops on the words that hit him.",
        not_when="Nobody is working when the news comes (dialogue), or the message is a telegram handed over (report).",
        params={
            "who": Param("who", required=True, doc="the person at work (the listener)"),
            "speakers": Param("list", required=True, doc="1-2 cast ids who bring the news (they stand on the left)"),
            "business": Param("enum", "write", ["write", "read", "phone", "map", "typing"], "what he is doing when they come in"),
            "look_up_on": Param("phrase", doc="word(s) where he stops and looks up (default: his name / early)"),
            "react_on": Param("phrase", doc="word(s) where the news hits him (close-up)"),
            "react": Param("enum", "shocked", MOOD, "his reaction"),
            "setting": Param("enum", "office", ROOMS, "the room"),
            "flag": Param("side", doc="flag and portrait on the wall"),
        },
        variants=("A", "B"),
        shots="A: full shot of the room (speakers left, worker at the desk right) → dissolve to a medium-close of the worker on react_on. "
              "B: medium on the worker at his business first, the speakers enter frame, then the close-up.",
        example={"at": "told Kaiser Wilhelm", "recipe": "interrupt", "says": "The generals tell the Kaiser the front cannot hold; he stops writing, stunned.",
                 "who": "kaiser_wilhelm", "speakers": ["ludendorff", "hindenburg"], "business": "write", "look_up_on": "Kaiser Wilhelm",
                 "react_on": "could no longer", "react": "shocked", "setting": "office", "flag": "german", "name_card": "kaiser_wilhelm"})
def interrupt(c):
    who = c.person("who")
    sp = _people(c, "speakers", 1, 2)
    tu = c.t(c.p("look_up_on"), 0.2, 0.6)
    tr = c.t(c.p("react_on"), 0.55, 1.4)
    bus = c.p("business")
    pose, holds = {"write": ("write", "pen"), "read": ("hold", "paper"), "phone": ("phone", "phone"), "map": ("pointDown", None), "typing": ("typing", None)}[bus]
    react = c.p("react")
    els = [AID("w", who, 1250, 1000, 1.6, pose, "neutral", holds=holds, turn=-0.3,
               keys=K((tu, {"pose": "idle", "holds": "", "turn": -0.6}), (tr + 0.2, {"expr": react, "pose": "head" if react in ("shocked", "panic") else "chin"})))]
    for i, s_ in enumerate(sp):
        els.append(AID(f"s{i}", s_, 640 - i * 260, 1000 + i * 8, 1.6 - i * 0.05, "explain" if i == 0 else "idle", "worried", talk=i == 0, turn=0.5,
                       keys=K((tr - 0.4, {"pose": "talk2"})) if i == 0 else K((1.4, {"pose": "chin"}))))
    flag = c.side("flag").nation if c.p("flag") else None
    if c.variant == "A":
        shots = [SHOT(0, ["s0", "w"], "full", push=0.03), SHOT(max(0.8, tr - 0.25), "w", "mediumclose", frameX=0.12, push=0.05)]
    else:
        for e in els[1:]:
            e["keys"] = (e.get("keys") or []) + [{"t": 0.0, "x": e["x"] - 500}, {"t": min(1.6, tu + 0.6), "x": e["x"], "ease": "arrive"}]
            e["x"] = e["x"] - 500
        shots = [SHOT(0, "w", "medium", frameX=0.1), SHOT(min(1.8, tu + 0.7), ["s0", "w"], "full"), SHOT(max(2.2, tr - 0.25), "w", "mediumclose", frameX=0.12)]
    return stage(c, _room(c.p("setting"), flag), els, [q for q in shots if q["t"] < c.dur - 0.4])


# ------------------------------------------------------------------ confront
@recipe("confront", "action",
        when="A demand, an order, an argument that lands hard: 'Germany needed an armistice, immediately', 'he demanded…', 'he refused'. "
             "One person forces the point physically (fist on the desk, steps forward); the other recoils.",
        not_when="A calm exchange (dialogue).",
        params={
            "a": Param("who", required=True, doc="the one who forces the point"),
            "b": Param("who", required=True, doc="the one who receives it"),
            "hit_on": Param("phrase", doc="word(s) where the fist comes down / he steps in"),
            "gesture": Param("enum", "slam", ["slam", "point", "fist", "stop"], "the forcing gesture"),
            "setting": Param("enum", "office", ROOMS, "the room"),
            "flag": Param("side", doc="flag on the wall"),
        },
        variants=("A", "B"),
        shots="A: two-shot across the desk → dissolve to a medium-close of A as the gesture lands. B: close on B first, A's gesture lands off-centre, then the two-shot.",
        example={"at": "Germany needed an armistice,", "recipe": "confront", "says": "Ludendorff insists Germany must ask for an armistice at once.",
                 "a": "ludendorff", "b": "kaiser_wilhelm", "hit_on": "immediately", "setting": "office", "flag": "german", "place_id": "kaiser_study"})
def confront(c):
    a, b = c.person("a"), c.person("b")
    th = c.t(c.p("hit_on"), 0.6, 1.0)
    g = c.p("gesture")
    els = [AID("a", a, 760, 1000, 1.6, "explain", "determined", talk=True, turn=0.4, keys=K((th - 0.2, {"pose": g, "expr": "angry"}))),
           AID("b", b, 1250, 1000, 1.6, "idle", "worried", turn=-0.5, keys=K((th + 0.2, {"pose": "stop" if g != "stop" else "head", "expr": "shocked"})))]
    flag = c.side("flag").nation if c.p("flag") else None
    shots = ([SHOT(0, ["a", "b"], "full", push=0.04), SHOT(max(0.6, th - 0.4), "a", "mediumclose", frameX=-0.12)] if c.variant == "A" else
             [SHOT(0, "b", "mediumclose", frameX=0.12), SHOT(max(0.6, th - 0.3), ["a", "b"], "full")])
    return stage(c, _room(c.p("setting"), flag), els, [q for q in shots if q["t"] < c.dur - 0.3], sfx=[{"t": th - 0.05, "id": "thud"}] if g == "slam" else None)


# ------------------------------------------------------------------ contemplate
@recipe("contemplate", "action",
        when="Someone left alone with the news / the weight of a decision: 'he could hardly believe it', 'he knew it was over', 'he never recovered'. "
             "Show the body: walking to the window, sitting down slowly, staring out.",
        not_when="He reacts in front of others (interrupt / confront).",
        params={
            "who": Param("who", required=True, doc="the person"),
            "action": Param("enum", "window", ["window", "sit", "stare", "walk_away"], "what he does"),
            "setting": Param("enum", "office", ROOMS + ["deck", "railway", "garden", "nomansland"], "where"),
            "mood": Param("enum", "sad", MOOD, "his face before he turns away"),
        },
        variants=("A", "B"),
        shots="A: full shot, he crosses to the window and stands with his back to us; slow push. B: close on his face first, dissolve to the wide of him alone in the room.",
        example={"at": "The Kaiser could hardly", "recipe": "contemplate", "says": "The Kaiser is left stunned by the news that the war is lost.",
                 "who": "kaiser_wilhelm", "action": "window", "setting": "office", "time": "dusk", "tint": "cold", "place_id": "kaiser_study"})
def contemplate(c):
    who = c.person("who")
    T = max(c.dur, 2.4)
    act = c.p("action")
    walk = min(1.8, T * 0.6)
    if act == "window":
        el = {**AID("p", who, 880, 1000, 1.6, "idle", c.p("mood")), "keys": K((walk, {"x": 1250, "y": 990}), (walk + 0.15, {"view": "back", "pose": "behind"}))}
    elif act == "sit":
        el = AID("p", who, 1000, 1000, 1.6, "idle", c.p("mood"), keys=K((walk * 0.6, {"pose": "face"}), (walk, {"seated": True, "pose": "head"})))
    elif act == "walk_away":
        el = man_path("p", who, [(0, 960, 1080), (T, 1020, 760)], pose="idle", expr=c.p("mood"), holds="", view="back")
    else:
        el = AID("p", who, 1000, 1000, 1.6, "chin", c.p("mood"), turn=0.3, keys=K((T * 0.5, {"pose": "behind", "turn": 0.6})))
    st = _room(c.p("setting"), desk=False) if c.p("setting") in ROOMS else {"kind": c.p("setting")}
    shots = [SHOT(0, "p", "full", track=act != "stare", push=0.04)] if c.variant == "A" else [SHOT(0, "p", "close", frameX=0.1), SHOT(min(1.4, T * 0.45), None, None, zoom=1.0, push=0.05)]
    return stage(c, st, [el], shots, world={"scale": 1.3, "y": 900, "horizon": 560} if act == "walk_away" else None)


# ------------------------------------------------------------------ watch_front
@recipe("watch_front", "action",
        when="Soldiers at the front see what is coming or check the time / their chances: 'they could not hold for two hours', 'the enemy massed for the attack', "
             "'by now the line was collapsing'. A face in front, the threat behind.",
        not_when="The attack itself (wave / assault / tank_attack).",
        params={
            "side": Param("side", doc="who is watching (in the foreground, behind sandbags)"),
            "enemy": Param("side", doc="who is coming"),
            "threat": Param("enum", "tanks", ["tanks", "infantry", "planes", "ships", "smoke"], "what is coming on the horizon"),
            "business": Param("enum", "watch", ["watch", "binoculars", "aim", "wait"], "what the man in front does (watch = checks his pocket watch)"),
            "react_on": Param("phrase", doc="word(s) where he gives up / panics (close-up)"),
            "react": Param("enum", "panic", MOOD, "his reaction"),
        },
        variants=("A", "B"),
        shots="A: medium on the two men behind the sandbags, the threat moving behind them → dissolve to a close-up on react_on. "
              "B: wide of the threat first, then the men.",
        example={"at": "Not for weeks.", "recipe": "watch_front", "says": "The front could collapse within hours as enemy tanks roll forward.",
                 "side": "german", "enemy": "british", "threat": "tanks", "business": "watch", "react_on": "For two hours", "time": "dawn",
                 "tag": "The Western Front · 29 September 1918"})
def watch_front(c):
    sd, en = c.side(), c.side("enemy")
    T = max(c.dur, 2.6)
    tr = c.t(c.p("react_on"), 0.7, 1.2)
    th = c.p("threat")
    els = []
    if th == "tanks":
        els += [{"id": f"t{i}", "kind": "vehicle", "type": en.get("tank", "tank"), "nation": en.nation, "x": 500 + i * 520, "y": 640 + i * 18,
                 "keys": K((T, {"x": 560 + i * 520})), "moving": True} for i in range(3)]
    elif th == "infantry":
        els += [man_path(f"e{i}", en.soldier, [(0, 300 + i * 220, 650 + (i % 2) * 12), (T, 380 + i * 220, 670 + (i % 2) * 12)], pose="port", expr="determined") for i in range(6)]
    elif th == "planes":
        els += [{"id": f"pl{i}", "kind": "vehicle", "type": en.get("bomber", "bomber"), "nation": en.nation, "x": -300 - i * 300, "y": 180 + i * 50, "scale": 0.3,
                 "keys": K((T + 2, {"x": 1400 - i * 300, "ease": "linear"}))} for i in range(3)]
    elif th == "ships":
        els += [{"id": f"sh{i}", "kind": "vehicle", "type": en.get("ship", "battleship"), "nation": en.nation, "x": 400 + i * 500, "y": 600, "scale": 0.22,
                 "keys": K((T, {"x": 460 + i * 500, "ease": "linear"}))} for i in range(3)]
    else:
        els += [FX("smoke", x, 640, size=1.6) for x in (400, 1000, 1600)]
    bus = c.p("business")
    pose, holds = {"watch": ("hold", "stopwatch"), "binoculars": ("binoculars", "binoculars"), "aim": ("aim", "rifle"), "wait": ("port", "rifle")}[bus]
    els.append(AID("m", sd.officer, 760, 1150, 2.0, pose, "worried", holds=holds, holdsScale=0.22 if holds == "stopwatch" else None, turn=0.4,
                   keys=K((tr, {"expr": c.p("react"), "pose": "head" if c.p("react") in ("panic", "shocked") else "chin", "holds": ""}))))
    els.append(AID("s", sd.soldier, 1380, 1170, 1.95, "aim", "nervous", holds="rifle", turn=-0.2, fireAt=[round(T * 0.3, 2), round(T * 0.65, 2)]))
    els.append(FX("shellburst", 1200, 700, size=1.6, **{"in": round(T * 0.4, 2)}))
    shots = ([SHOT(0, ["m", "s"], "medium", push=0.04), SHOT(max(0.8, tr - 0.3), "m", "close", frameX=-0.12, push=0.05)] if c.variant == "A" else
             [SHOT(0, None, None, zoom=1.15, x=960, y=600, push=0.04), SHOT(min(1.6, T * 0.4), ["m", "s"], "medium"), SHOT(max(2.0, tr - 0.3), "m", "close", frameX=-0.12)])
    return stage(c, {"kind": "nomansland", "fg": "sandbags"}, els, [q for q in shots if q["t"] < c.dur - 0.3], world=W, impacts=[round(T * 0.4, 2)],
                 sfx=[{"t": 0, "id": "tank_engine" if th == "tanks" else "boom_distant", "dur": T}])


# ------------------------------------------------------------------ binocular_view
@recipe("binocular_view", "action",
        when="What someone sees in the distance — right after a card where he raises binoculars (vista / watch_front / decision): "
             "'they were 56 km from Paris', 'the enemy fleet was in sight'.",
        not_when="Nobody is looking (use a normal scene of the place).",
        params={
            "setting": Param("enum", "city", ["city", "street", "ruins", "harbor", "sea", "field", "nomansland", "snow", "desert", "airfield"], "what is seen"),
            "movers": Param("enum", "none", ["none", "tanks", "infantry", "ships", "trucks"], "what moves in the view"),
            "side": Param("side", doc="side of the movers"),
        },
        variants=("A",),
        shots="A: the view inside two round lenses, swaying slightly, slow drift across the place.",
        example={"at": "about fifty-six kilometres", "recipe": "binocular_view", "says": "Through the binoculars the Germans could see the roofs of Paris.",
                 "setting": "city", "time": "dusk"})
def binocular_view(c):
    sd = c.side()
    T = max(c.dur, 2.0)
    els = [{"kind": "binoculars", "in": 0}]
    mv = c.p("movers")
    if mv == "tanks":
        els += [{"kind": "vehicle", "type": sd.get("tank", "tank"), "nation": sd.nation, "x": 500 + i * 400, "y": 760 + i * 20, "keys": K((T, {"x": 620 + i * 400})), "moving": True} for i in range(3)]
    elif mv == "ships":
        els += [{"kind": "vehicle", "type": sd.get("ship", "battleship"), "nation": sd.nation, "x": 600 + i * 400, "y": 620, "scale": 0.3, "keys": K((T, {"x": 680 + i * 400}))} for i in range(2)]
    elif mv == "infantry":
        els += [man_path(f"i{i}", sd.soldier, [(0, 500 + i * 180, 780), (T, 600 + i * 180, 780)], pose="shoulder", expr="neutral") for i in range(5)]
    elif mv == "trucks":
        els += [{"kind": "vehicle", "type": "truck", "nation": sd.nation, "x": 400 + i * 360, "y": 760, "keys": K((T, {"x": 560 + i * 360})), "moving": True} for i in range(3)]
    return stage(c, {"kind": c.p("setting")}, els, [SHOT(0, None, None, zoom=1.15, x=960, y=520, push=0.04, panX=-40)], world=W if mv in ("tanks", "infantry", "trucks") else None)


# ------------------------------------------------------------------ vista
@recipe("vista", "action",
        when="Men look toward a goal or a threat far away — the city they want, the land they lost, the fires on the horizon: "
             "'they were within sight of Paris', 'they looked back at the burning city'. Dusk/dawn silhouettes on a ridge.",
        not_when="Fighting (assault / wave).",
        params={
            "side": Param("side", doc="who stands on the ridge"),
            "goal": Param("str", "", doc="1-2 words written small over the glow on the horizon, e.g. \"PARIS\" (optional)"),
            "goal_on": Param("phrase", doc="word(s) where the goal's name appears"),
            "action": Param("enum", "look", ["look", "binoculars", "turn_back", "march_past"], "look = they stand and stare; binoculars = an officer in front raises binoculars; "
                                                                                              "turn_back = they turn and trudge away (failure); march_past = a column passes along the ridge"),
            "count": Param("int", 4, doc="men on the ridge (2-7)"),
        },
        variants=("A", "B"),
        shots="A: one wide of the ridge against the sky, slow push and drift. B (binoculars): the wide, then dissolve to a medium-close of the officer raising his binoculars.",
        example={"at": "In early June,", "recipe": "vista", "says": "In June German troops came within sight of Paris.",
                 "side": "german", "goal": "PARIS", "goal_on": "Paris", "action": "binoculars", "time": "dusk", "tint": "warm",
                 "place_id": "marne_ridge", "tag": "The Marne · June 1918"})
def vista(c):
    sd = c.side()
    T = max(c.dur, 2.6)
    n = max(2, min(7, c.p("count")))
    act = c.p("action")
    els = [{"kind": "glow", "x": 1500, "y": 840, "r": 260, "color": "#ffd9a0", "strength": 0.5}]
    for i in range(n):
        base = {"silhouette": True, "scale": round(0.62 - (i % 2) * 0.05, 2)}
        x0 = 520 + i * 120
        if act == "turn_back":
            els.append({**man_path(f"g{i}", sd.soldier, [(0.5 + i * 0.25, x0, 866 + (i % 2) * 4), (T, 60 + i * 90, 866 + (i % 2) * 4)], pose="port" if i % 2 else "idle",
                                   expr="tired", holds="rifle" if i % 2 else ""), "flip": True, **base})
        elif act == "march_past":
            els.append({**man_path(f"g{i}", sd.soldier, [(0, -200 - i * 160, 866), (T, 900 - i * 160, 866)], pose="shoulder", expr="tired", holds="rifle"), **base})
        else:
            els.append({**AID(f"g{i}", sd.soldier, x0, 866 + (i % 2) * 4, None, "port" if i % 2 else "idle", "neutral", view="back", holds="rifle" if i % 2 else ""), **base})
    if c.p("goal"):
        els.append({"kind": "label", "text": c.p("goal"), "x": 1500, "y": 760, "style": "chalk", "size": 36, "in": c.t(c.p("goal_on"), 0.3) + 0.25, "color": "#fff3d6"})
    shots = [SHOT(0, None, None, zoom=1.0, push=0.04, panX=60)]
    if act == "binoculars":
        els.append(AID("off", sd.officer, 1250, 1080, 1.9, "idle", "determined", turn=0.3, keys=K((min(1.0, T * 0.3), {"pose": "binoculars", "holds": "binoculars"}))))
        shots.append(SHOT(min(1.6, T * 0.45), "off", "mediumclose", frameX=-0.15))
    return stage(c, {"kind": "nomansland", "wire": False, "horizon": 860}, els, [q for q in shots if q["t"] < c.dur - 0.3])


# ------------------------------------------------------------------ lecture
@recipe("lecture", "talk",
        when="The debate itself: 'historians disagree', 'ask around and you'll get a list', 'there are three explanations'. "
             "A historian chalks the options on a blackboard as they are named.",
        not_when="The options are events you can show (show the events instead, one card each).",
        params={
            "items": Param("list", required=True, doc="2-6 very short items written on the board, e.g. [\"1914?\", \"1916?\", \"1917?\"]"),
            "items_on": Param("list", doc="optional: for each item the word(s) where it is written"),
            "who": Param("who", "civilian_man", doc="the historian (default: an old scholar with glasses)"),
        },
        variants=("A", "B"),
        shots="A: full shot — he writes with his back to us, then turns and points at the board. B: medium on the board first, then him turning.",
        example={"at": "Ask around and", "recipe": "lecture", "says": "Historians propose several different turning points.",
                 "items": ["1914?", "1916?", "1917?", "1918?"], "tag": "Today"})
def lecture(c):
    items = c.p("items") or []
    if not 2 <= len(items) <= 6:
        raise CardError(f"{_where(c.raw)}: \"items\" needs 2-6 short strings (≤ 12 characters each).")
    ons = c.p("items_on") or []
    T = max(c.dur, 2.4)
    who = c.person("who")
    turn = min(T * 0.55, 0.3 + len(items) * 0.45 + 0.2)
    els = [AID("prof", who, 1480, 1000, 1.55, "reach", "smile", view="back", look_={"age": 0.8, "glasses": "round"} if who == "civilian_man" else None,
               keys=K((turn, {"view": "front", "pose": "pointL", "turn": -0.4, "talk": True})))]
    for i, t in enumerate(items):
        at = c.t(ons[i], 0.2) if i < len(ons) else round(0.3 + i * 0.45, 2)
        els.append({"kind": "label", "text": t, "x": 640 + (i % 2) * 320, "y": 470 + (i // 2) * 95, "style": "chalk", "size": 58, "in": at})
    shots = ([SHOT(0, None, None, zoom=1.0, push=0.04), SHOT(max(1.0, turn - 0.2), "prof", "full", frameX=0.1)] if c.variant == "A" else
             [SHOT(0, None, None, zoom=1.5, x=820, y=540, push=0.03), SHOT(max(1.0, turn - 0.2), None, None, zoom=1.0, push=0.03)])
    return stage(c, {"kind": "classroom", "desk": False}, els, shots, sfx=[{"t": 0.3, "id": "chalk", "dur": min(2.0, turn)}])


# ------------------------------------------------------------------ absence
@recipe("absence", "action",
        when="Loss, death, the end of someone — shown by what is left behind: 'he died believing he had failed', 'none of them came back', "
             "'a whole generation was gone'. An empty place, one object, quiet light.",
        not_when="The narration describes the fighting (show the fighting) or mourning crowds (crowd mood=mourn).",
        params={
            "setting": Param("enum", "nomansland", ["nomansland", "office", "study", "home", "kitchen", "garden", "trench", "street", "ruins", "field"], "the empty place"),
            "object": Param("enum", "helmet_rifle", ["helmet_rifle", "empty_chair", "candle", "cross", "letter", "boots"], "what is left"),
        },
        variants=("A", "B"),
        shots="A: wide of the empty place, slow push toward the object. B: start close on the object, pull back by dissolve to the empty place.",
        example={"at": "none of them came back", "recipe": "absence", "says": "The men who left never returned.",
                 "setting": "home", "object": "empty_chair", "time": "dusk", "tint": "grey"})
def absence(c):
    o = c.p("object")
    stg = c.p("setting")
    outdoors = stg in ("nomansland", "garden", "trench", "street", "ruins", "field")
    gy = 870 if outdoors else 960
    obj = {"helmet_rifle": [{**PROP("rifle", 1000, gy - 60, 1.1), "rotate": -84}, PROP("helmet", 990, gy - 110, 0.9)],
           "empty_chair": [PROP("chair", 980, gy, 1.3)],
           "candle": [{**PROP("candle", 980, gy - 20, 1.6), "on": True}],
           "cross": [PROP("cross", 980, gy, 1.4)],
           "letter": [{**PROP("telegram", 980, gy - 40, 1.2), "rotate": 80}],
           "boots": [PROP("helmet", 940, gy, 0.8), PROP("rifle", 1060, gy, 0.8)]}[o]
    st = {"kind": stg, "wire": False} if stg == "nomansland" else _room(stg, desk=False) if stg in ROOMS else {"kind": stg}
    shots = ([SHOT(0, None, None, zoom=1.0, push=0.05), SHOT(max(1.2, c.dur * 0.5), None, None, zoom=1.8, x=980, y=gy - 80, push=0.04)] if c.variant == "A" else
             [SHOT(0, None, None, zoom=2.0, x=980, y=gy - 80, push=0.03), SHOT(max(1.2, c.dur * 0.45), None, None, zoom=1.0, push=0.04)])
    s = stage(c, st, obj, [q for q in shots if q["t"] < c.dur - 0.3], ambience="wind")
    return s
