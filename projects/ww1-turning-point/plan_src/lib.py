"""Film-specific builders for "What Was The REAL Turning Point of WW1".

Every builder returns one scene (and registers it). Acting scenes always carry `shots` (coverage inside the place);
people travel with the engine's walking profile; vehicles drive with `drive`. Times are seconds from the scene start.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools"))
sys.path.insert(0, HERE)
from shotlib import A, K, L, ST, NC, V, FX, DOC, HEAD, PROP, CITY, CNT, SHOT, AID, WOOD_DESK, Plan  # noqa: E402,F401
from timing import T, E, peek, END, LAST  # noqa: E402,F401

P = Plan(end=END)
SCENES = P.scenes


def sc(start, set_, els, shots=None, typ="stage", **kw):
    s = {"start": round(start, 2), "type": typ, "elements": [e for e in els if e]}
    if set_ is not None:
        s["set"] = set_ if isinstance(set_, dict) else {"kind": set_}
    if shots:
        s["shots"] = shots
    s.update({k: v for k, v in kw.items() if v is not None})
    s.setdefault("beat", LAST[0])
    return P.add(s)


def mv(*pairs):
    """keys from (t, dict) pairs"""
    return K(*pairs)


# ------------------------------------------------------------------ people & places
DESK = {"fg": "officedesk"}
HOST_SET = {"kind": "station"}  # the narrator is a stationmaster of history: platform, timetable, pocket watch


def host(start, pose="talk", expr="smug", keys=None, holds="stopwatch", turn=0.25, size="medium", label=None, aide=False, aide_keys=None,
         second=None, set_=None, **kw):
    """The host on the platform talking to camera; optional aide (Porter) beside him; `second` = (t, size, on) a cut."""
    els = [AID("host", "host", 760 if aide else 960, 960, 1.6, pose, expr, talk=True, holds=holds, holdsScale=0.42, turn=turn, keys=keys)]
    if aide:
        els.append(AID("aide", "aide", 1260, 975, 1.5, "idle", "neutral", turn=-0.5, keys=aide_keys or mv((1.8, {"pose": "chin"}))))
    if label:
        els.append(L(label, 960, 170, "tag", 42, at=0.6))
    shots = [SHOT(0, ["host", "aide"] if aide else "host", "medium" if not aide else "full", frameX=-0.1 if not aide else 0, push=0.04)]
    if second:
        t2, sz, on = second
        shots.append(SHOT(t2, on, sz, frameX=0.12 if on == "host" else -0.12, push=0.04))
    return sc(start, set_ or HOST_SET, els, shots, **kw)


def duo(start, turns, set_=None, holds=None, **kw):
    """Host <-> aide exchange in over-the-shoulder coverage. turns: [(t, 'host'|'aide', pose, expr)] — each turn is a cut
    to the speaker over the other's shoulder (or a close-up for short retorts: pose ends with '!')."""
    els = [
        AID("host", "host", 1240, 960, 1.6, "idle", "smug", turn=-0.5, holds=holds or "stopwatch", holdsScale=0.42),
        AID("aide", "aide", 680, 975, 1.5, "idle", "neutral", turn=0.5),
    ]
    hk, ak = [], []
    shots = []
    for t, who, pose, expr in turns:
        close = pose.endswith("!")
        pose = pose.rstrip("!")
        (hk if who == "host" else ak).append((t, {"pose": pose, "expr": expr, "talk": True}))
        (ak if who == "host" else hk).append((t, {"talk": False}))
        if close:
            shots.append(SHOT(t, who, "close", frameX=0.12 if who == "host" else -0.12, push=0.03))
        else:
            shots.append(SHOT(t, [who], "medium", frameX=0.18 if who == "host" else -0.18, push=0.04))
    els[0]["keys"] = mv(*hk) if hk else None
    els[1]["keys"] = mv(*ak) if ak else None
    return sc(start, set_ or HOST_SET, els, shots, **kw)


def glass(start, level=0.0, to=None, flip_at=None, stamp=None, stamp_at=1.2, plaque=None, host_line=None, dur_fall=6.0, cut_host=None, **kw):
    """THE DEVICE — a big brass hourglass on the station-master's desk. level: share of the sand fallen (0 = full top).
    to: level reached over dur_fall s. flip_at: the host turns the glass over (rotation 0->180, then swap).
    stamp: ('NOT YET'|'TURNED'|...) slammed onto the log beside it at stamp_at."""
    g = {"kind": "prop", "item": "hourglass", "x": 720, "y": 545, "scale": 2.2, "value": level, "text": plaque, "front": True, "id": "glass", "enter": "none"}
    keys = []
    if to is not None:
        keys.append((min(dur_fall, 30), {"value": to, "ease": "linear"}))
    if flip_at is not None:
        lv = to if to is not None else level
        keys += [(flip_at, {"rotate": 0}), (flip_at + 1.1, {"rotate": 180, "ease": "smooth"}),
                 (flip_at + 1.12, {"rotate": 0, "value": 1 - lv, "ease": "step"})]
    if keys:
        g["keys"] = mv(*keys)
    els = [g,
           {**PROP("ledger", 1130, 868, 0.62), "front": True, "rotate": -3},
           AID("host", "host", 1480, 1000, 1.6, "idle", "neutral", holds="stopwatch", holdsScale=0.42, turn=-0.45,
               keys=mv(*([(max(0.1, flip_at - 0.5), {"pose": "reach", "holds": ""}), (flip_at + 1.3, {"pose": "idle", "holds": "stopwatch"})] if flip_at is not None else [])
                       + ([(stamp_at - 0.35, {"pose": "slam", "expr": "determined"}), (stamp_at + 0.8, {"pose": "idle"})] if stamp else []))) ]
    if stamp:
        col = "#2f6b3a" if stamp in ("NOT YET",) else None
        els.append({**ST(stamp, 1130, 850, stamp_at, size=46, color=col, tilt=-9), "front": True})
    shots = [SHOT(0, None, None, zoom=1.0, x=1000, push=0.04)]
    if to is not None or flip_at is not None:
        shots.append(SHOT(0.9 if flip_at is None else max(0.3, flip_at - 0.7), "glass", "full", zoom=2.0, push=0.05))
    if stamp:
        shots.append(SHOT(max(0.2, stamp_at - 0.5), None, None, zoom=2.1, x=1180, y=800, push=0.03))
    if cut_host:
        shots.append(SHOT(cut_host, "host", "close", frameX=0.12))
    shots.sort(key=lambda q: q["t"])
    return sc(start, {"kind": "workshop", "fg": "officedesk"}, els, shots, **kw)


def hq(start, people, set_="warroom", talk=0, react=None, cuts=None, map_table=True, desk=True, **kw):
    """Commanders around a map table. people: [(id, who, pose, expr, keys)] left->right. talk: index of the speaker.
    cuts: [(t, id|[ids], size)] after the opening wide."""
    n = len(people)
    xs = [960 + (i - (n - 1) / 2) * 330 for i in range(n)]
    els = []
    for i, (id_, who, pose, expr, keys) in enumerate(people):
        turn = -0.45 if xs[i] > 960 else 0.45
        els.append(AID(id_, who, xs[i], 1000 if desk else 960, 1.5, pose, expr, talk=(i == talk), turn=turn, keys=keys))
    if map_table and desk:
        els.append({**PROP("paper", 960, 872, 0.7), "rotate": 80})
    shots = [SHOT(0, [p[0] for p in people], "medium", push=0.03)]
    for t, on, size in cuts or []:
        shots.append(SHOT(t, on, size, frameX=0.1 if isinstance(on, str) else 0, push=0.04))
    st = {"kind": set_, **({"fg": "officedesk"} if desk else {})}
    if set_ in ("office", "study", "cabinet", "conference", "home", "kitchen"):
        st["desk"] = False
    return sc(start, st, els, shots, **kw)


def report(start, giver, receiver, item="telegram", set_="cabinet", react="shocked", react_at=2.6, name=None, role="", walk_in=True,
           receiver_pose="write", text=None, close_at=None, **kw):
    """A messenger walks in and hands over news; the receiver reads, then reacts (cut to close before the reaction)."""
    gk = [(0.0, {"x": -180}), (1.8, {"x": 560}), (1.95, {"pose": "offer"}), (2.6, {"pose": "idle", "holds": ""})] if walk_in else [(0.4, {"pose": "offer"}), (1.2, {"pose": "idle", "holds": ""})]
    els = [AID("giver", giver, -180 if walk_in else 560, 1000, 1.5, "carry", "neutral", holds=item, holdsText=text, keys=mv(*gk)),
           AID("recv", receiver, 1060, 1000, 1.55, receiver_pose, "neutral", holds="pen" if receiver_pose == "write" else None, turn=-0.4,
               keys=mv((1.9 if walk_in else 0.5, {"pose": "reach", "holds": ""}), (2.4 if walk_in else 1.0, {"pose": "show", "holds": item, "holdsText": text, "turn": 0}),
                       (react_at, {"expr": react}), (react_at + 1.2, {"pose": "head" if react in ("panic", "shocked") else "chin"})))]
    if name:
        els.append(NC(name, role, at=0.8))
    st = {"kind": set_, "fg": "officedesk"}
    if set_ in ("office", "study", "cabinet", "conference", "home"):
        st["desk"] = False
    c = close_at if close_at is not None else max(0.6, react_at - 0.5)
    shots = [SHOT(0, ["giver", "recv"], "full", zoom=1.0, x=880, push=0.03), SHOT(min(2.2, c - 0.6) if c > 1.4 else c, "recv", "medium", frameX=0.12),
             SHOT(c, "recv", "close", frameX=0.16, push=0.05)]
    shots = sorted({q["t"]: q for q in shots}.values(), key=lambda q: q["t"])
    return sc(start, st, els, shots, **kw)


def march_col(start, who="ww1_german_1914", n=5, set_="countryside", direction=1, expr="tired", dur=8.0, close=None, heat=False, **kw):
    """A column marching through the countryside in depth (world model): a far file, a near file, one face close."""
    els = []
    for i in range(n):
        x0 = (300 - i * 260) if direction > 0 else (1620 + i * 260)
        els.append({**AID(f"m{i}", who, x0, 860 + (i % 2) * 22, None, "shoulder", expr, holds="rifle", keys=mv((dur, {"x": x0 + direction * 420, "ease": "linear"}))),
                    "flip": direction < 0})
    x1 = 760 if direction > 0 else 1160
    els.append({**AID("near", who, x1, 1150, None, "shoulder", expr, holds="rifle", keys=mv((dur, {"x": x1 + direction * 520, "ease": "linear"}))), "flip": direction < 0})
    shots = [SHOT(0, None, "wide", zoom=1.0, push=0.03)]
    if close is not None:
        shots.append(SHOT(close, "near", "mediumclose", track=True, frameX=0.1 * direction))
    return sc(start, {"kind": set_, "drift": 0}, els, shots, world={"scale": 0.95, "y": 900}, **kw)


def trench(start, who="ww1_british", n=3, action="wait", expr="worried", shells=(), close=None, enemy=None, **kw):
    """Soldiers in a trench. action: wait | over (climb out and run) | cower (shelling) | aim."""
    els = []
    xs = [520, 960, 1400][:n] if n <= 3 else [400 + i * 280 for i in range(n)]
    for i, x in enumerate(xs):
        if action == "over":
            k = mv((0.6 + i * 0.25, {"pose": "charge", "expr": "shout"}), (1.2 + i * 0.25, {"y": 760}), (3.2 + i * 0.25, {"x": x + 500, "y": 700}))
            els.append(AID(f"s{i}", who, x, 1000, 1.45, "port", expr, holds="rifle", keys=k))
        elif action == "cower":
            p0, p1 = [("cower", "head"), ("head", "cower"), ("port", "cower")][i % 3]
            els.append(AID(f"s{i}", who, x + (i - 1) * 40, 1000 + (i % 2) * 18, 1.45 - (i % 2) * 0.08, p0, "panic" if i != 2 else "shocked",
                           holds="rifle" if p0 == "port" else None, turn=[0.4, -0.2, -0.5][i % 3], keys=mv((1.0 + i * 0.55, {"pose": p1, "holds": ""}))))
        elif action == "aim":
            els.append(AID(f"s{i}", who, x, 1000, 1.45, "aim", "determined", holds="rifle"))
        else:
            els.append(AID(f"s{i}", who, x, 1000, 1.45, ["port", "idle", "smoke"][i % 3], expr, holds="rifle" if i % 3 == 0 else None, turn=0.3 - 0.3 * i,
                           keys=mv((2.2 + i * 0.5, {"pose": "chin" if i % 2 else "port"}))))
    for t, x, y in shells:
        els.append(FX("explosion", x, y, **{"in": t}))
        els.append(FX("dust", x, y + 60, **{"in": t + 0.05}))
    shots = [SHOT(0, None, None, zoom=1.0, push=0.04)] if action == "over" else [SHOT(0, [e["id"] for e in els if e.get("kind") == "actor"], "full", push=0.04, shake=0)]
    if close is not None:
        shots.append(SHOT(close, "s1" if n > 1 else "s0", "close", frameX=0.12, push=0.05, shake=3 if shells else 0))
    return sc(start, "trench", els, shots, sfx=[{"t": t, "id": "explosion"} for t, _, _ in shells] or None, **kw)


def battlefield(start, who="ww1_german", n=4, direction=1, set_="mud", shells=(), tanks=None, tank_nation="UK", run=False,
                close=None, surrender=None, dur=6.0, **kw):
    """Men advancing across a shell-torn field in depth; optional tanks (markiv/renault) leading, explosions, surrender."""
    els = []
    if tanks:
        for i in range(tanks[1]):
            x0 = (250 - i * 560) if direction > 0 else (1670 + i * 560)
            els.append({"id": f"t{i}", "kind": "vehicle", "type": tanks[0], "nation": tank_nation, "x": x0, "y": 760 + i * 40, "flip": direction < 0,
                        "keys": mv((dur, {"x": x0 + direction * 600}))})
    for i in range(n):
        x0 = (200 + i * 230) if direction > 0 else (1720 - i * 230)
        yy = 800 + (i % 3) * 70
        els.append({**AID(f"m{i}", who, x0, yy, None, "charge" if run else "port", "shout" if run else "determined", holds="rifle",
                          keys=mv((dur, {"x": x0 + direction * (900 if run else 420), "ease": "linear"}))), "flip": direction < 0, "run": bool(run)})
    if surrender:
        for i in range(surrender):
            els.append({**AID(f"g{i}", "ww1_german", 1320 + i * 170, 820 + i * 30, None, ["surrender", "head", "surrender", "cower", "surrender"][i % 5],
                                  ["worried", "sad", "nervous", "cry", "tired"][i % 5], keys=mv((0.8 + i * 0.45, {"pose": "surrender"}))), "flip": direction > 0})
    for t, x, y in shells:
        els.append(FX("explosion", x, y, **{"in": t}))
    shots = [SHOT(0, None, "wide", zoom=1.0, push=0.03)]
    if close is not None:
        target = close[1] if isinstance(close, tuple) else "m1"
        t0 = close[0] if isinstance(close, tuple) else close
        shots.append(SHOT(t0, target, "medium", track=True, frameX=0.1 * direction))
    return sc(start, {"kind": set_, "drift": 0}, els, shots, world={"scale": 0.95, "y": 900},
              sfx=[{"t": t, "id": "explosion"} for t, _, _ in shells] or None, **kw)


def fleet(start, ships=(("battleship", "UK", 420, 650, 1),), firing=(), hits=(), set_="sea", dur=7.0, close=None, **kw):
    """Ships at sea in depth. ships: (type, nation, x, y, dir). firing: [(t, ship_index)] muzzle flash+smoke; hits: [(t, x, y)] splashes."""
    els = []
    for i, (typ, nat, x, y, d) in enumerate(ships):
        s = 0.34 + (y - 600) / 900
        els.append({"id": f"sh{i}", "kind": "vehicle", "type": typ, "nation": nat, "x": x, "y": y, "scale": round(s, 2), "flip": d < 0,
                    "keys": mv((dur, {"x": x + d * 90 * dur / 7, "ease": "linear"}))})
    for t, i in firing:
        typ, nat, x, y, d = ships[i]
        els.append(FX("muzzle", x + d * 120, y - 70, **{"in": t}))
        els.append(FX("smoke", x + d * 140, y - 80, **{"in": t + 0.05}))
    for t, x, y in hits:
        els.append(FX("splash", x, y, **{"in": t}))
    shots = [SHOT(0, None, "wide", zoom=1.0, push=0.03)]
    if close is not None:
        i0 = int(str(close[1]).replace("sh", "") or 0)
        shots.append(SHOT(close[0], None, None, zoom=1.7, x=ships[i0][2], y=ships[i0][3] - 60, push=0.04))
    return sc(start, {"kind": set_, "drift": 0}, els, shots, sfx=[{"t": t, "id": "cannon"} for t, _ in firing] or None, **kw)


# ------------------------------------------------------------------ inserts, documents, device
def doc(start, style, title, lines, stamp=None, speed=34, **kw):
    """A document typed on the desk insert (top-down wood)."""
    return sc(start, {"kind": "paper", "dof": 0}, list(WOOD_DESK) + [DOC(style, title, lines, x=960, y=540, w=1000, h=600, at=0.2, speed=speed, stamp=stamp)],
              [SHOT(0, None, None, zoom=1.0, push=0.06)], sfx=[{"t": 0.2, "id": "typewriter", "dur": 1.5}], **kw)


def quote(start, who, text, set_="cabinet", pose="talk", expr="angry", tag=None, x=1080, **kw):
    """A quoted line: close on the speaker with a speech bubble (QUOTE / REPORTED tag under it)."""
    els = [AID("q", who, x, 1000, 1.6, pose, expr, talk=True, turn=-0.3),
           {"kind": "bubble", "text": text, "x": 700, "y": 300, "side": 1, "size": 34, "in": 0.35, "hud": True}]
    if tag:
        els.append(L(tag, 360, 140, "dark", 30, at=0.2, hud=True))
    st = {"kind": set_}
    if set_ in ("office", "study", "cabinet", "conference", "home"):
        st["desk"] = False
    return sc(start, st, els, [SHOT(0, "q", "mediumclose", frameX=0.2, push=0.05)], **kw)


def kitchen(start, beats="turnip", **kw):
    """Turnip Winter: a mother sets a turnip on the plate; the child's face falls."""
    els = [AID("mother", "civilian_woman", 1180, 1060, 1.95, "carry", "sad", holds="turnip", holdsScale=0.6, turn=-0.4,
               keys=mv((1.0, {"pose": "offer"}), (1.6, {"pose": "idle", "holds": ""}), (2.6, {"pose": "chin"}))),
           AID("child", "civilian_man", 720, 1060, 1.6, "idle", "neutral", turn=0.4, look_={"age": 0.0, "build": 0.85}, keys=mv((1.9, {"expr": "sad"}), (3.2, {"pose": "chin"}))),
           {**PROP("turnip", 950, 845, 0.55), "front": True, "in": 1.5}]
    shots = [SHOT(0, ["mother", "child"], "full", push=0.03), SHOT(1.7, "child", "close", frameX=-0.12)]
    return sc(start, {"kind": "kitchen", "desk": False, "fg": "officedesk", "time": "dusk"}, els, shots, tint="cold", **kw)


# ------------------------------------------------------------------ maps (1914 basemap)
EUROPE = {"German Empire": "GERI", "Austro-Hungarian Empire": "#9b9a8c", "France": "#93ab6e", "Russian Empire": "#c98a6a",
          "United Kingdom of Great Britain and Ireland": "#d99a8c", "Belgium": "#cfa264", "Serbia": "#93ab6e"}
WEST = {"German Empire": "GERI", "France": "#93ab6e", "Belgium": "#cfa264", "United Kingdom of Great Britain and Ireland": "#d99a8c", "Luxembourg": "#cfa264"}
LEG_CP = [("GERI", "Central Powers"), ("FRA", "France"), ("UK", "Britain"), ("RUS", "Russia")]
LEG_W = [("GERI", "Germany"), ("FRA", "France"), ("UK", "Britain"), ("BEL", "Belgium")]
PL = {  # places (lon, lat)
    "Paris": [2.35, 48.86], "Berlin": [13.4, 52.52], "Brussels": [4.35, 50.85], "Antwerp": [4.4, 51.22], "Maubeuge": [3.97, 50.28],
    "Liège": [5.57, 50.63], "Verdun": [5.38, 49.16], "Amiens": [2.3, 49.9], "Reims": [4.03, 49.26], "Soissons": [3.32, 49.38],
    "Meaux": [2.88, 48.96], "Château-Thierry": [3.4, 49.05], "St Quentin": [3.29, 49.85], "Compiègne": [2.83, 49.42], "Metz": [6.18, 49.12],
    "Mulhouse": [7.34, 47.75], "Albert": [2.65, 50.0], "Nieuport": [2.75, 51.13], "Ypres": [2.88, 50.85], "Spa": [5.86, 50.49],
    "Scapa Flow": [-3.1, 58.9], "Shetland": [-1.2, 60.3], "Bergen": [5.3, 60.4], "Dover": [1.3, 51.13], "Wilhelmshaven": [8.1, 53.5],
    "Pless": [18.95, 49.98], "Brest-Litovsk": [23.7, 52.1], "Petrograd": [30.3, 59.9], "Zurich": [8.5, 47.4], "Kiev": [30.5, 50.45],
    "Vienna": [16.37, 48.2], "Washington": [-77.0, 38.9], "Mexico City": [-99.1, 19.4], "New York": [-74.0, 40.7], "Brest": [-4.5, 48.4],
    "Kinsale": [-8.5, 51.6], "London": [-0.12, 51.5], "Hamel": [2.57, 49.9], "Warsaw": [21.0, 52.23], "Lutsk": [25.3, 50.75],
}
WESTERN_FRONT = [[2.75, 51.13], [2.88, 50.85], [2.8, 50.35], [2.95, 49.65], [3.3, 49.42], [4.0, 49.3], [5.38, 49.22], [5.65, 48.9], [6.5, 48.6], [7.1, 47.6]]
SPRING_1918 = [[2.75, 51.13], [2.75, 50.75], [2.6, 50.3], [2.45, 49.85], [2.57, 49.62], [3.0, 49.4], [3.4, 49.05], [3.95, 49.1], [4.1, 49.25], [5.38, 49.22], [5.65, 48.9], [6.5, 48.6], [7.1, 47.6]]
HINDENBURG = [[2.9, 51.0], [3.0, 50.45], [3.2, 50.1], [3.29, 49.85], [3.45, 49.6], [3.8, 49.45], [4.2, 49.35], [5.38, 49.22], [5.65, 48.9], [6.5, 48.6], [7.1, 47.6]]
NOV_1918 = [[3.7, 51.1], [3.9, 50.7], [4.2, 50.35], [4.6, 50.0], [5.0, 49.7], [5.4, 49.4], [5.65, 48.9], [6.5, 48.6], [7.1, 47.6]]
EAST_FRONT = [[21.3, 57.2], [24.2, 56.6], [26.2, 55.3], [26.6, 53.5], [25.8, 51.6], [25.3, 50.0], [25.9, 48.3], [26.4, 47.8]]
BREST_LOSS = [[21.0, 55.8], [21.2, 57.6], [23.5, 59.4], [28.2, 59.5], [28.4, 57.0], [31.5, 55.6], [32.0, 52.3], [38.5, 51.2], [40.0, 49.0],
              [38.0, 47.0], [35.0, 46.2], [31.0, 46.4], [29.6, 45.4], [28.3, 46.4], [27.0, 48.2], [24.0, 48.6], [22.6, 49.4], [21.5, 50.4],
              [19.0, 50.1], [18.8, 52.0], [19.5, 53.8], [21.0, 54.5]]


def MAP(start, center, span, els, colors=None, legend=None, camera=None, follow=None, hatch=("German Empire",), rivers=None, **kw):
    m = {"era": "1914", "center": center, "span": span, "style": "paper", "colors": colors or EUROPE, "hatch": list(hatch)}
    if rivers:
        m["rivers"] = rivers
    if follow is not None:
        m["follow"] = follow
    els = list(els)
    if legend:
        els.append({"kind": "legend", "x": 40, "y": 860, "hud": True, "in": 0, "enter": "fade", "items": [{"nation": n, "label": l} for n, l in legend]})
    return sc(start, None, els, typ="map", map=m, camera=camera, **kw)


def city(name, at=0.2, side="right", tag=False, size=28):
    return CITY(name, PL[name], at=at, side=side, size=size, tag=tag)


def arrow(path, nation, at=0.5, dur=2.2, width=24, dashed=False, label=None):
    a = {"kind": "arrow", "path": [PL[p] if isinstance(p, str) else p for p in path], "color": nation, "in": at, "dur": dur, "width": width}
    if dashed:
        a["dashed"] = True
    if label:
        a["label"] = label
    return a


def front(path, nation="#7a2a22", path2=None, morph_dur=4.0, at=0.0, width=None):
    f = {"kind": "front", "path": path, "color": nation, "in": at, "enter": "draw" if not path2 else "none", "dur": 1.6}
    if path2:
        f.update(path2=path2, morph=0, keys=K((morph_dur, {"morph": 1})))
    if width:
        f["width"] = width
    return f


def _auto_coverage(scenes, max_gap=6.0):
    """Safety net for the coverage rule: in a scene with people, a set-up held longer than `max_gap` s gets an extra cut
    at its middle — alternately a close-up on the most active actor and a medium of the group (never on a map)."""
    added = 0
    for i, s in enumerate(scenes):
        if s.get("type") != "stage":
            continue
        end = scenes[i + 1]["start"] if i + 1 < len(scenes) else END
        dur = end - s["start"]
        actors = [e for e in s.get("elements", []) if e.get("kind") == "actor" and e.get("view") != "back"]
        if not actors:
            continue
        for k, e in enumerate(actors):
            e.setdefault("id", f"a{k}")
        def x_at(e, t):
            ks = sorted([k for k in (e.get("keys") or []) if "x" in k], key=lambda k: k["t"])
            x, t0 = e.get("x", 960), 0.0
            for k in ks:
                if t <= k["t"]:
                    return x + (k["x"] - x) * max(0.0, min(1.0, (t - t0) / max(1e-6, k["t"] - t0)))
                x, t0 = k["x"], k["t"]
            return x
        # prefer the speaker, then the nearest (biggest) person, then the busiest
        active = sorted(actors, key=lambda e: (-int(bool(e.get("talk"))), -(e.get("scale") or e.get("y", 900) / 700), -len(e.get("keys") or [])))
        shots = s.get("shots") or [SHOT(0, None, None, zoom=1.0, push=0.03)]
        changed = True
        while changed:
            changed = False
            ts = sorted(q["t"] for q in shots)
            bounds = ts + [dur]
            for a0, b0 in zip(bounds, bounds[1:]):
                if b0 - a0 > max_gap:
                    t = round(a0 + (b0 - a0) / 2, 2)
                    prev = max((q for q in shots if q["t"] <= a0), key=lambda q: q["t"])
                    if prev.get("size") in ("close", "mediumclose", "ecu"):
                        new = SHOT(t, [e["id"] for e in actors[:3]], "medium" if len(actors) > 1 else "full", push=0.03)
                    else:
                        vis = [e for e in active if -60 < x_at(e, t) < 1980] or active
                        tgt = vis[(len(shots)) % len(vis)]
                        new = SHOT(t, tgt["id"], "close" if prev.get("size") != "medium" else "mediumclose", frameX=0.14 if tgt.get("x", 960) < 960 else -0.14, push=0.04)
                    shots.append(new)
                    added += 1
                    changed = True
                    break
        s["shots"] = sorted(shots, key=lambda q: q["t"])
    return added


def finish(meta, cast, path):
    P.scenes.sort(key=lambda s: s["start"])
    print("auto coverage cuts:", _auto_coverage(P.scenes))
    return P.finish(meta, cast, path)
