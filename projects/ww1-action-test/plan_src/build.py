"""Sample ACTION chapter (WW1 film 599.4-722.7 s: Falkenhayn, Verdun, Brusilov, the Somme, the first tanks).

python projects/ww1-action-test/plan_src/build.py  ->  projects/ww1-action-test/plan.json

Target mix for a battle chapter: action >= 55-60 %, talk <= 10 %, maps ~10 %, devices/docs <= 10 %.
Action recipes used here (each scene notes which one):
  OVER_TOP    men climb out and advance into depth, some fall at staggered times, shells burst among them, camera jolts
  GUN_CREW    a gun crew loop: loader carries a shell in, the gun fires (recoil, flash, smoke), crew cover their ears
  WAVE        a line runs across a battlefield in depth, shells ahead, one man falls, close tracking shot on the leader
  UNDER_FIRE  men pinned in a shell hole while bursts walk closer; a runner dashes across
  HIT         one man is hit, a comrade runs to him and kneels (no gore: he tips over)
  SILHOUETTE  dusk ridge: stretcher bearers / columns as black cut-outs against the sky; crosses appear one by one
  RAIL        troops board, the train pulls out
  MG_NEST     a machine-gun crew behind sandbags, looping muzzle flash + tracers
  AFTERMATH   the field after: fallen men, a lone survivor walks back
  TANK        a tank crawls over a trench, defenders flee, one shocked close-up
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import timing  # noqa: E402,F401  (this project's words; the WW1 lib below reuses this module)

sys.path.insert(1, os.path.join(HERE, "..", "..", "ww1-turning-point", "plan_src"))
import lib  # noqa: E402
from shotlib import man_path as path_man, assault, shells, stretcher_team, hit_and_help, mg_nest, fallen  # noqa: E402
from lib import (sc, mv, MAP, city, arrow, front, PL, EUROPE, WEST, LEG_W, LEG_CP, EAST_FRONT, trench,  # noqa: E402
                 AID, SHOT, NC, L, FX, PROP, CNT, DOC, WOOD_DESK, T, peek, END)


def r(start, phrase):
    return round(peek(phrase) - start, 2)


# ------------------------------------------------------------------ action helpers
def adv(id_, who, x0, y0, x1, y1, t1, t0=0.0, pose="port", expr="determined", fall=None, fall_dir=-1, holds="rifle", **kw):
    """A man moving from (x0, y0) to (x1, y1) between t0 and t1 at a steady pace; `fall` = time he is hit (he stops there and tips over)."""
    keys = []
    if t0 > 0:
        keys.append((t0, {"x": x0, "y": y0}))
    if fall is not None and fall < t1:
        k = max(0.0, (fall - t0) / max(0.01, t1 - t0))
        keys.append((round(fall, 2), {"x": round(x0 + (x1 - x0) * k), "y": round(y0 + (y1 - y0) * k), "ease": "linear", "expr": "shocked"}))
    else:
        keys.append((t1, {"x": x1, "y": y1, "ease": "linear"}))
    d = AID(id_, who, x0, y0, None, pose, expr, keys=mv(*keys), holds=holds, **kw)
    if fall is not None:
        d["fallAt"] = round(fall, 2)
        d["fallDir"] = fall_dir
    return d


def bursts(times_xy, size=1.0, kind="shellburst"):
    """old local helper kept for the world-less sentry shot; world scenes use shotlib.shells (depth-sized)"""
    return [FX(kind, x, y, size=size, **{"in": t}) for t, x, y in times_xy]


def B(times_xy):
    return shells(times_xy, size=2.0)[0]


def bars(start, title, items, mx, **kw):
    return sc(start, {"kind": "workshop"}, [{"kind": "bars", "title": title, "x": 1020, "y": 400, "width": 760, "max": mx,
                                             "items": [{"label": l, "value": v, "nation": c, "in": t} for l, v, c, t in items]}],
              [SHOT(0, None, None, zoom=1.0, push=0.05)], **kw)


W = {"scale": 1.0, "y": 900}  # world: a man at y 900 is scale 1.0; the horizon (560) is scale 0


def build():
    # 1 ── UNDER_FIRE (establish): a dawn sentry line, shells bursting out in no man's land ─────────────── action
    s = 0.0
    bt = [(0.5, 1250, 700), (1.7, 520, 760), (3.0, 1500, 820)]
    sc(s, {"kind": "nomansland", "time": "dawn", "fg": "sandbags"}, [
        AID("a", "ww1_british", 640, 1130, 1.9, "aim", "worried", holds="rifle", view="back", keys=mv((1.75, {"pose": "cower", "holds": ""}), (3.2, {"pose": "aim", "holds": "rifle"}))),
        AID("b", "ww1_british", 1380, 1150, 2.0, "port", "nervous", holds="rifle", view="back", keys=mv((0.6, {"pose": "head", "holds": ""}), (2.4, {"pose": "port", "holds": "rifle"}))),
        *bursts(bt, 0.8)],
       [SHOT(0, None, None, zoom=1.0, push=0.05)], impacts=[t for t, _, _ in bt], date="END OF 1915", chapter="Bleeding")
    # Falkenhayn: reads the casualty returns, then the problem lands
    s = T("General Erich von Falkenhayn")
    sc(s, {"kind": "warroom", "fg": "officedesk"}, [
        AID("f", "falkenhayn", 1000, 1000, 1.6, "hold", "neutral", holds="telegram", turn=-0.3,
            keys=mv((r(s, "had a problem"), {"pose": "head", "holds": "", "expr": "worried"}), (r(s, "no obvious answer"), {"pose": "chin"}))),
        NC("General Erich von Falkenhayn", "Chief of the German General Staff", at=0.3)],
       [SHOT(0, "f", "medium", frameX=-0.1), SHOT(r(s, "had a problem"), "f", "close", frameX=0.12, push=0.06)])

    # 2 ── OVER_TOP: men climb out and walk into the guns; three fall ─────────────────────────────────── action
    s = T("Attacks on the Western Front gained")
    c = r(s, "cost enormous")
    men = assault("m", "ww1_british", [
        (1130, 800, [330, 960, 1590], 0.2, 5.8),          # front row climbs over the parapet
        (900, 720, [150, 640, 1280, 1780], 0, 5.8),       # middle row already out
        (760, 660, [420, 1100, 1500], 0, 5.8)],           # far row
        {3: c + 0.2, 5: c + 0.9, 1: c + 1.6, 8: c + 0.5}, climb=True)
    bt = [(1.2, 1300, 650), (2.3, 700, 690), (c + 0.1, 1000, 720), (c + 1.2, 1500, 700)]
    sc(s, {"kind": "nomansland", "fg": "sandbags"}, men + B(bt) + [FX("tracer", 1990, 640, dir=172, **{"in": 1.0}), FX("tracer", 1990, 610, dir=176, **{"in": 1.6})],
       [SHOT(0, None, None, zoom=1.0, push=0.04), SHOT(c - 0.3, ["m3", "m4", "m5"], "full", push=0.05)], world=W,
       impacts=[t for t, _, _ in bt], sfx=[{"t": 1.0, "id": "machinegun", "dur": 4.0}])

    # 3 ── his idea: Falkenhayn writes at night, then the memoir line ──────────────────────── talk / document
    s = T("So he went looking")
    sc(s, {"kind": "warroom", "fg": "officedesk", "time": "night"}, [
        AID("f", "falkenhayn", 900, 1000, 1.6, "write", "determined", holds="pen", turn=0.3),
        {**PROP("candle", 1240, 880, 0.9), "front": True}],
       [SHOT(0, "f", "medium", frameX=0.1, push=0.05)], sfx=[{"t": 0.3, "id": "pen", "dur": 2.2}])
    s = T("According to the memoirs")
    sc(s, {"kind": "paper", "dof": 0}, list(WOOD_DESK) + [
        DOC("letter", "FALKENHAYN — AS HE WROTE AFTER THE WAR", ["France can be beaten", "without a breakthrough —", "if the French army loses enough men."], x=960, y=540, w=1000, h=560, at=0.2, speed=30)],
       [SHOT(0, None, None, zoom=1.0, push=0.07)])

    # 4 ── the French reinforcements stream toward the smoke (dusk road, trucks + column) ──────────────── action
    s = T("his idea was that France")
    trench(s, "ww1_french", n=3, action="aim", shells=((0.8, 1300, 400), (2.6, 600, 380)), close=2.2)
    lib.SCENES[-1]["impacts"] = [0.8, 2.6]
    for e in lib.SCENES[-1]["elements"]:
        if e.get("kind") == "actor":
            e["fireAt"] = [0.5 + len(e["id"]) * 0.1 + (int(e["id"][1:]) * 0.6), 2.0 + int(e["id"][1:]) * 0.5, 3.6]
    lib.SCENES[-1]["elements"].append(L("THE LINE HOLDS", 960, 170, "tag", 42, at=r(s, "without a breakthrough"), hud=True))
    s = T("if the French army could")
    col = [adv(f"c{i}", "ww1_french", -120 - i * 190, 930 + (i % 2) * 24, 900 - i * 190, 930 + (i % 2) * 24, 3.6, pose="shoulder", expr="tired") for i in range(6)]
    sc(s, {"kind": "mud", "time": "dusk", "poles": False}, col + [
        {"id": "tr", "kind": "vehicle", "type": "truck", "nation": "FRA", "x": 200, "y": 700, "keys": mv((3.6, {"x": 1200}))},
        {"id": "tr2", "kind": "vehicle", "type": "truck", "nation": "FRA", "x": -500, "y": 700, "keys": mv((3.6, {"x": 600}))},
        FX("smoke", 1700, 640, size=1.3), FX("smoke", 1880, 660, size=1.0)],
       [SHOT(0, None, "wide", zoom=1.0, panX=80, push=0.03)], world=W)

    # 5 ── GUN_CREW: German heavy guns at dusk ──────────────────────────────────────────────────────────── action
    s = T("Pick a place")
    f1, f2 = 1.1, r(s, "let German heavy guns")
    g2 = [0.4, 2.3, f2 + 0.7]
    sc(s, {"kind": "nomansland", "time": "dusk", "wire": False, "horizon": 600}, [
        {"id": "g1", "kind": "vehicle", "type": "artillery", "nation": "GERI", "x": 760, "y": 1000, "fireAt": [f1, f2]},
        {"id": "g2", "kind": "vehicle", "type": "artillery", "nation": "GERI", "x": 1460, "y": 760, "fireAt": g2},
        AID("ld", "ww1_german", 120, 1010, None, "carry", "determined", holds="shell", holdsScale=0.8,
            keys=mv((2.2, {"x": 420}), (2.7, {"pose": "reach"}), (3.2, {"holds": "", "pose": "idle"}), (f2 - 0.15, {"pose": "head"}))),
        AID("c1", "ww1_german", 1100, 1030, None, "idle", "determined", turn=-0.4,
            keys=mv((f1 - 0.25, {"pose": "head"}), (f1 + 0.9, {"pose": "point"}), (f2 - 0.25, {"pose": "head", "expr": "tired"}))),
        AID("c2", "ww1_german", 1700, 800, None, "idle", "neutral", keys=mv((0.2, {"pose": "head"}), (1.3, {"pose": "idle"}), (2.1, {"pose": "head"}), (3.2, {"pose": "idle"})))],
       [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(2.1, "c1", "mediumclose", frameX=-0.12, push=0.05), SHOT(f2 + 0.35, None, "wide", zoom=1.12, x=900, y=620, push=0.03)],
       world={**W, "vehicles": 1.9},
       impacts=[f1, f2])

    # 6 ── where: Verdun (one short map) ───────────────────────────────────────────────────────────────────── map
    s = T("The place he picked was Verdun")
    MAP(s, [5.4, 49.2], 2.4, [city("Verdun", tag=True), arrow([[5.75, 49.45], [5.45, 49.25]], "GERI", at=1.0, dur=2.0),
                              front([[5.1, 49.4], [5.6, 49.3], [5.7, 49.1]], "#7a2a22")],
        colors=WEST, legend=LEG_W, rivers=["Meuse"])

    # 7 ── WAVE: German storm troops across the snow at dawn ─────────────────────────────────────────────── action
    s = T("The attack began in February")
    wave = [adv(f"w{i}", "ww1_german", -160 - i * 150, 760 + (i % 4) * 70, 1300 - i * 150, 760 + (i % 4) * 70, 2.6, pose="charge", expr="shout",
                fall=1.7 if i == 2 else None, run=True) for i in range(6)]
    bt = [(0.3, 1500, 720), (1.4, 1200, 800), (2.2, 1650, 860)]
    sc(s, {"kind": "nomansland", "time": "dawn", "weather": "snow"}, wave + B(bt) + [FX("snow", 960, 540)],
       [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(1.2, "w0", "full", track=True, frameX=0.12)], world=W,
       impacts=[t for t, _, _ in bt], date="21 FEBRUARY 1916", place="VERDUN")

    # 8 ── UNDER_FIRE: French pinned in a shell hole, bursts walk closer, a runner dashes across ──────────── action
    s = T("It became the longest battle")
    bt = [(0.4, 1500, 660), (1.5, 400, 700), (2.7, 1200, 760), (3.6, 760, 720)]
    sc(s, {"kind": "nomansland", "fg": "sandbags"}, [
        AID("p1", "ww1_french", 560, 1060, 1.7, "cower", "panic", turn=0.4, keys=mv((1.9, {"pose": "head"}), (3.4, {"pose": "port", "holds": "rifle", "expr": "determined"}))),
        AID("p2", "ww1_french", 1300, 1080, 1.8, "head", "shocked", turn=-0.4, keys=mv((2.75, {"pose": "cower", "expr": "panic"}))),
        adv("run", "ww1_french", 2050, 820, -150, 800, 3.4, t0=0.8, pose="charge", expr="determined", run=True, flip=True),
        *B(bt),
        L("≈ 300 DAYS", 1560, 170, "tag", 44, at=r(s, "about three hundred days"), hud=True)],
       [SHOT(0, None, None, zoom=1.0, push=0.04), SHOT(2.5, "p1", "mediumclose", frameX=-0.15, push=0.05)], world=W,
       impacts=[t for t, _, _ in bt])

    # 9 ── WAVE (reverse): the Germans bleed too — an assault in the mud, two fall ───────────────────────────── action
    s = T("And the arithmetic never worked")
    g = [adv(f"g{i}", "ww1_german", 2080 + i * 170, 780 + (i % 3) * 80, 500 + i * 170, 780 + (i % 3) * 80, 3.8, pose="port", expr="determined",
             fall={1: 1.5, 3: 2.4}.get(i), fall_dir=1, flip=True) for i in range(5)]
    bt = [(0.9, 900, 760), (2.2, 1400, 860)]
    sc(s, {"kind": "nomansland", "time": "day"}, g + B(bt) + [FX("tracer", -60, 700, dir=-6, **{"in": 0.5})],
       [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(2.2, ["g2", "g3"], "full", push=0.05)], world=W, impacts=[t for t, _, _ in bt],
       sfx=[{"t": 0.5, "id": "machinegun", "dur": 2.5}])

    # 10 ── the numbers (one estimate) ─────────────────────────────────────────────────────────────────────── chart
    s = T("One modern calculation")
    bars(s, "VERDUN 1916 — FRENCH CASUALTIES (ONE ESTIMATE)", [("French", 377000, "FRA", r(s, "French casualties"))], 400000, ambience="amb_battle")
    # the German number lands on German stretcher bearers in their own trench (the other side bleeds too)
    s = T("and German casualties")
    sc(s, {"kind": "trench", "time": "day"}, [
        *stretcher_team("st", "ww1_german", 1225, 2125, 1000, 4.0, scale=1.5),
        AID("sd", "ww1_german", 420, 1000, 1.55, "cower", "sad", turn=0.4),
        CNT(0, 337000, 960, 150, at=r(s, "three hundred and thirty-seven"), prefix="≈ ", suffix=" GERMAN CASUALTIES", size=60, dur=1.4, hud=True)],
       [SHOT(0, None, None, zoom=1.0, push=0.04, panX=80)])

    # 11 ── SILHOUETTE: stretcher bearers on the ridge at dusk, crosses appear one by one ────────────────────── action
    s = T("That's roughly seventy thousand")
    dur = 5.6
    group = stretcher_team("b0", "ww1_french", 330, 1230, 900, dur, scale=1.3, silhouette=True) +         stretcher_team("b1", "ww1_french", -470, 380, 905, dur, scale=1.1, silhouette=True)
    relief = [adv(f"r{i}", "ww1_french", 2000 + i * 120, 880, 1300 + i * 120, 880, dur, pose="shoulder", expr="tired", flip=True, silhouette=True, scale=0.7) for i in range(4)]
    for e in relief:
        e["scale"] = 0.72
    crosses = [{**PROP("cross", 180 + i * 260, 1090 + (i % 2) * 30, 1.1), "in": 0.4 + i * 0.7, "enter": "place", "silhouette": True} for i in range(7)]
    sc(s, {"kind": "nomansland", "time": "dusk", "wire": False, "horizon": 880}, group + relief + crosses + [
        L("≈ 70,000 MEN A MONTH", 960, 160, "tag", 46, at=r(s, "seventy thousand"), hud=True)],
       [SHOT(0, None, None, zoom=1.0, push=0.04, panX=-60)], tint="warm")

    # 12 ── HIT: a German soldier is hit, his comrade runs to him and kneels ─────────────────────────────────── action
    s = T("The army that was supposed to bleed")
    sc(s, {"kind": "nomansland", "time": "day"}, [
        *hit_and_help("x", "ww1_german", 380, 1100, 960, 1.6, 3.0, helper_from=-150),
        *B([(1.55, 1500, 740)])],
       [SHOT(0, "xh", "full", track=True, frameX=0.1), SHOT(2.95, "xk", "close", frameX=0.15, push=0.05)], world=W, impacts=[1.55])

    # 13 ── where: two more doors (map, 3.5 s) ───────────────────────────────────────────────────────────────── map
    s = T("And while Verdun went on")
    MAP(s, [13.5, 50.3], 31, [front(EAST_FRONT, "#7a2a22"), arrow([[26.2, 50.6], [24.0, 50.0]], "RUS", at=0.6, dur=1.4, label="BRUSILOV"),
                              arrow([[1.6, 49.9], [2.9, 50.0]], "UK", at=1.6, dur=1.2, label="SOMME")],
        colors=EUROPE, legend=LEG_CP, date="SUMMER 1916")

    # 14 ── Brusilov orders, the Russian wave hits, the Austro-Hungarians break ─────────────────────────────── action
    s = T("In June, the Russian general")
    sc(s, {"kind": "tent"}, [
        AID("b", "brusilov", 1150, 1000, 1.7, "point", "determined", turn=-0.3, keys=mv((1.6, {"pose": "fist"}), (2.9, {"pose": "point"}))),
        NC("General Aleksei Brusilov", "Russian South-Western Front", at=0.4)],
       [SHOT(0, "b", "mediumclose", frameX=0.12, push=0.05)], date="JUNE 1916")
    s = T("attacked on a wide front")
    a0 = 0.0
    sm = r(s, "smashed the")
    ru = [adv(f"r{i}", "ww1_russian", -220 - i * 170, 760 + (i % 4) * 80, 1050 - i * 170, 760 + (i % 4) * 80, sm + 2.2, t0=a0, pose="charge", expr="shout", run=True) for i in range(7)]
    au = [AID(f"a{i}", "ww1_austrian", 1450 + i * 150, 780 + (i % 3) * 90, None, "aim", "nervous", holds="rifle", fireAt=[a0 + 0.3 + i * 0.35, a0 + 1.4 + i * 0.3],
              keys=mv((sm + 0.2 + i * 0.25, {"pose": ["surrender", "port", "surrender", "head"][i % 4], "holds": "" if i % 2 == 0 else "rifle", "expr": ["shocked", "panic", "sad", "panic"][i % 4]}),
                      *([(sm + 0.9 + i * 0.2, {"flip": False, "pose": "charge", "run": True}), (sm + 3.2 + i * 0.2, {"x": 2300 + i * 150, "ease": "linear"})] if i % 2 else [])),
              flip=True) for i in range(4)]
    bt = [(a0 + 0.4, 1500, 760), (a0 + 1.3, 1750, 840), (sm - 0.3, 1600, 900)]
    sc(s, {"kind": "steppe", "poles": False, "houses": False, "road": False}, ru + au + B(bt),
       [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(sm + 0.6, ["a0", "a1", "a2"], "full", push=0.05)], world=W, impacts=[t for t, _, _ in bt])

    # 15 ── RAIL: German divisions board and the train pulls out east ─────────────────────────────────────────── action
    s = T("Germany had to send divisions east")
    tr = [{"id": f"tc{i}", "kind": "vehicle", "type": "locomotive" if i == 0 else "traincar", "nation": "GERI", "x": 1500 - i * 300, "y": 740,
           "keys": mv((0.8, {"x": 1500 - i * 300}), (3.7, {"x": 2300 - i * 300, "ease": "smooth"}))} for i in range(5)]
    smoke = {**FX("smoke", 1560, 640, size=0.6), "keys": mv((0.8, {"x": 1560}), (3.7, {"x": 2360, "ease": "smooth"}))}
    sol = [path_man(f"s{i}", "ww1_german", [(0, -150 - i * 210, 1000 + (i % 2) * 50), (3.6, 700 - i * 210, 800 + (i % 2) * 20)], pose="shoulder", expr="tired")
           for i in range(5)]
    sc(s, {"kind": "railway"}, tr + [smoke] + sol + [AID("of", "ww1_german", 1450, 1040, None, "wave", "determined", turn=-0.4, keys=mv((1.6, {"pose": "point"})))],
       [SHOT(0, None, "wide", zoom=1.0, push=0.03, panX=120)], world=W, sfx=[{"t": 0.8, "id": "train", "dur": 3.0}])
    s = T("and Romania was")
    MAP(s, [20.0, 47.5], 18, [{"kind": "region", "polygon": [[22.4, 48.2], [26.6, 48.2], [29.6, 45.2], [28.6, 43.8], [22.7, 44.0], [21.0, 46.0]],
                               "color": "#93ab6e", "fillOpacity": 0.6, "in": 0.4},
                              L("ROMANIA JOINS THE ALLIES", 1300, 860, "tag", 34, at=0.9)], colors=EUROPE, legend=LEG_CP)

    # 16 ── OVER_TOP (the Somme): officer's whistle, men up the ladders ─────────────────────────────────────── action
    s = T("Then, on the 1st of July")
    up = assault("u", "ww1_british", [(1120, 820, [300, 760, 1200], 1.3, 3.4), (900, 760, [520, 980], 0, 3.4)], {}, climb=True)
    for e in up[3:]:
        e["in"] = 1.3
    sc(s, {"kind": "nomansland", "time": "dawn", "fg": "sandbags"}, [
        {**AID("of", "ww1_british", 1560, 1080, 2.1, "pointUp", "shout", turn=-0.4, keys=mv((1.0, {"pose": "charge", "expr": "determined"}))), "front": True},
        *up],
       [SHOT(0, "of", "mediumclose", frameX=0.1, push=0.05), SHOT(1.25, None, None, zoom=1.0, push=0.04)], world=W,
       date="1 JULY 1916", place="THE SOMME", sfx=[{"t": 0.4, "id": "bell"}])

    # 17 ── OVER_TOP (walking into the guns) with the counter running, then the MG nest, then the field after ─── action
    s = T("On its first day")
    k = r(s, "fifty-seven thousand")
    line = assault("l", "ww1_british", [
        (1090, 880, [300, 960, 1600], 0, 7.0),
        (900, 760, [130, 620, 1240, 1760], 0, 7.0),
        (760, 680, [380, 860, 1120, 1480], 0, 7.0)],
        {4: 1.4, 1: 3.1, 6: 2.2, 8: 4.0, 3: 2.8, 9: 4.6, 0: 5.4})
    sc(s, {"kind": "nomansland", "time": "day"}, line + [
        FX("tracer", 1990, 640, dir=172, **{"in": 0.6}), FX("tracer", 1990, 600, dir=178, **{"in": 1.1}), FX("tracer", -60, 620, dir=4, **{"in": 1.5}),
        *B([(0.8, 1400, 680), (2.6, 600, 700)]),
        CNT(0, 57470, 960, 150, at=k, suffix=" CASUALTIES", size=70, dur=2.4, hud=True)],
       [SHOT(0, None, None, zoom=1.0, push=0.05), SHOT(3.3, ["l0", "l1", "l2"], "full", push=0.05)], world=W, impacts=[0.8, 2.6], sfx=[{"t": 0.5, "id": "machinegun", "dur": 6.0}])
    s = T("including nineteen thousand")
    mg = mg_nest("mg", "ww1_german", [380, 860], 1170, 1.9, fire=(0.0, 6.0))
    sc(s, {"kind": "nomansland", "fg": "sandbags", "time": "day"}, mg + [
        CNT(0, 19240, 960, 150, at=0.3, suffix=" KILLED", size=70, dur=1.6, color="#f08070", hud=True)],
       [SHOT(0, ["mg0", "mg1", "mgsp"], "medium", push=0.04, shake=2), SHOT(2.3, "mg0", "mediumclose", frameX=-0.2, shake=3)],
       sfx=[{"t": 0.0, "id": "machinegun", "dur": 4.0}])
    s = T("It's still the worst day")
    down = fallen("d", "ww1_british", [(260 + i * 330, 820 + (i % 3) * 90) for i in range(5)])
    sc(s, {"kind": "nomansland", "time": "dusk"}, down + [
        adv("sv", "ww1_british", 1500, 1000, 700, 1080, 3.3, pose="idle", expr="cry", holds="", flip=True),
        L("WORST DAY IN BRITISH ARMY HISTORY", 960, 170, "tag", 40, at=0.5, hud=True)],
       [SHOT(0, None, None, zoom=1.0, push=0.05), SHOT(1.9, "sv", "medium", frameX=0.12)], world=W, tint="grey")

    # 18 ── the battle goes on: rain, men trudging in mud; then Germans under the barrage ─────────────────────── action
    s = T("But the battle went on")
    mud = [adv(f"t{i}", "ww1_british", 200 + i * 300, 900 + (i % 2) * 70, 360 + i * 300, 900 + (i % 2) * 70, 3.0, pose="shoulder", expr="tired") for i in range(5)]
    sc(s, {"kind": "nomansland", "time": "day", "wire": False}, mud + [FX("rain", 960, 540),
                                                                     L("141 DAYS", 1560, 170, "tag", 44, at=r(s, "a hundred and forty-one"), hud=True)],
       [SHOT(0, None, None, zoom=1.0, push=0.04), SHOT(1.6, "t2", "medium", track=True)], world=W, sfx=[{"t": 0, "id": "amb_rain", "dur": 3.0}])
    s = T("and the Germans facing it")
    trench(s, "ww1_german", n=3, action="cower", shells=((0.3, 1300, 400), (1.2, 500, 380), (2.0, 1000, 420)), close=1.5)
    lib.SCENES[-1]["impacts"] = [0.3, 1.2, 2.0]

    # 19 ── TANK: the first tanks crawl over the trench; the defenders run ───────────────────────────────────── action
    s = T("In September, the first tanks")
    sc(s, {"kind": "nomansland", "time": "day"}, [
        {"id": "tk", "kind": "vehicle", "type": "markiv", "nation": "UK", "x": 120, "y": 880, "keys": mv((5.0, {"x": 720})), "fireAt": [1.8]},
        *[adv(f"f{i}", "ww1_german", 1350 + i * 160, 860 + (i % 2) * 70, 2300 + i * 160, 860 + (i % 2) * 70, 3.4, t0=0.6 + i * 0.25, pose="charge", expr="panic", holds="", run=True)
          for i in range(3)],
        AID("st", "ww1_german", 1500, 1060, None, "aim", "shocked", holds="rifle", flip=True, fireAt=[0.7, 1.4, 2.2, 2.9], keys=mv((3.6, {"pose": "cower", "holds": "", "expr": "panic"}))),
        FX("dust", 300, 900, size=1.2)],
       [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(3.3, "st", "mediumclose", frameX=-0.12, push=0.05)], world=W,
       date="SEPTEMBER 1916", impacts=[1.8])


build()
CAST = {n: {"preset": n} for n in ["falkenhayn", "brusilov", "ww1_german", "ww1_french", "ww1_british", "ww1_russian", "ww1_austrian"]}
META = {"title": "WW1 — sample action chapter (Verdun to the first tanks)", "lang": "en", "fps": 24, "duration": END, "voice": "input/voice.wav", "grain": 0.5}
lib.finish(META, CAST, os.path.join(HERE, "..", "plan.json"))
