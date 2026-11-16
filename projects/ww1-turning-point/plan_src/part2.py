"""Chapter 2 (blockade), chapter 3 (Verdun, Brusilov, the Somme), CTA, chapter 4 (Jutland). 7:23 - 15:26"""
from lib import *  # noqa: F401,F403
from lib import sc, host, duo, glass, hq, report, march_col, trench, battlefield, fleet, doc, quote, kitchen, MAP, city, arrow, front, PL, \
    EUROPE, WEST, LEG_CP, LEG_W, WESTERN_FRONT, EAST_FRONT, mv  # noqa: E402


def r(start, phrase):
    return round(peek(phrase) - start, 2)


NORTH_SEA = {"German Empire": "GERI", "United Kingdom of Great Britain and Ireland": "#d99a8c", "France": "#93ab6e",
             "Netherlands": "#e3d3a8", "Denmark": "#e3d3a8", "Norway": "#e3d3a8", "Sweden": "#e3d3a8"}
LEG_SEA = [("GERI", "Germany"), ("UK", "Britain"), ("NEUTRAL", "Neutrals")]


def bars(start, title, items, mx, unit="", **kw):
    return sc(start, {"kind": "workshop"}, [{"kind": "bars", "title": title, "x": 1020, "y": 400, "width": 760, "max": mx, "unit": unit,
                                             "items": [{"label": l, "value": v, ("nation" if len(c) <= 5 else "color"): c, "in": t} for l, v, c, t in items]}],
              [SHOT(0, None, None, zoom=1.0, push=0.05)], **kw)


def build():
    # ================================================================ CHAPTER 2 — the blockade
    s = T("And the big glass had a crack")
    glass(s, level=0.0, to=0.08, dur_fall=6, plaque="LONG WAR", chapter="The Crack in the Glass", cut_host=r(s, "Germany fed its people"))

    s = T("Before the war, more than half")
    els = [{"id": "ship", "kind": "vehicle", "type": "cargo", "nation": "NEUTRAL", "x": 1500, "y": 640, "scale": 0.7},
           AID("w1", "worker", 300, 1000, 1.5, "carry", "tired", holds="crate", holdsScale=0.42, keys=mv((5.0, {"x": 1100}))),
           AID("w2", "worker", 1500, 990, 1.45, "carry", "neutral", holds="crate", holdsScale=0.42, keys=mv((1.0, {"x": 1500}), (6.0, {"x": 820})))]
    goods = [("cotton", "COTTON"), ("wool", "WOOL"), ("hides", "HIDES"), ("copper", "COPPER"), ("oil,", "OIL"), ("rubber", "RUBBER"), ("saltpetre", "SALTPETRE")]
    for i, (w, lab) in enumerate(goods):
        els.append({**PROP("crate", 260 + i * 210, 900 - (i % 2) * 40, 0.9), "text": lab, "in": r(s, w), "front": True})
    sc(s, {"kind": "dock", "drift": 0}, els, [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(r(s, "cotton"), None, None, zoom=1.35, x=900, y=760, panX=160, push=0.03)],
       date="1913", place="HAMBURG")
    s = T("Much of its food came from abroad")
    sc(s, {"kind": "dock", "drift": 0}, [AID("w", "worker", 960, 1000, 1.6, "carry", "neutral", holds="crate", holdsText="GRAIN", turn=0.3, keys=mv((2.0, {"x": 1300})))],
       [SHOT(0, "w", "medium", track=True, frameX=-0.1)])
    s = T("And most of the world's sea lanes")
    MAP(s, [-12, 52], 60, [{"kind": "route", "path": p, "color": "#3a6ea5", "width": 5, "icon": "freighter", "trail": 2, "gap": 90, "iconSize": 1.0, "enter": "draw", "dur": 4.0, "in": 0.2 + i * 0.4}
                           for i, p in enumerate([[[-60, 38], [-30, 45], [-8, 49], [2, 51.2], [7.5, 54.0]], [[-40, 20], [-20, 40], [-6, 48.5], [1.5, 51.0], [8, 53.6]],
                                                  [[-50, 58], [-20, 60], [-2, 59.5], [5, 57.5], [8.5, 55.0]]])],
        colors=NORTH_SEA, legend=LEG_SEA)

    s = T("The British had decided")
    hq(s, [("j", "jellicoe", "pointDown", "determined", mv((2.0, {"pose": "explain"}))), ("o", "ww1_british", "idle", "neutral", None)],
       set_="warroom", talk=0, cuts=[(r(s, "distant blockade") - 0.4, "j", "close")], place="THE ADMIRALTY, LONDON")
    s = T("The Royal Navy didn't need")
    fleet(s, ships=(("cruiser", "UK", 400, 680, 1), ("destroyer", "UK", 1300, 630, 1)), dur=8.0, close=(r(s, "It simply closed the doors"), "sh0"))
    s = T("Ships patrolled the narrow")
    MAP(s, [2.0, 55.8], 34, [city("Dover", at=0.3), city("Scapa Flow", at=r(s, "Grand Fleet waiting") if False else 3.5, tag=True),
                             {"kind": "line", "path": [[1.0, 51.4], [1.9, 50.9]], "color": "#2b4d7a", "width": 9, "in": 0.6, "enter": "draw", "dur": 0.8},
                             {"kind": "line", "path": [PL["Shetland"], PL["Bergen"]], "color": "#2b4d7a", "width": 9, "in": r(s, "the Northern Patrol"), "enter": "draw", "dur": 1.2},
                             L("≈250 KM", 1250, 260, "tag", 36, at=r(s, "two hundred and fifty"))],
        colors=NORTH_SEA, legend=LEG_SEA, hatch=())
    s = T("On the 2nd of November, 1914")
    doc(s, "order", "ADMIRALTY · 2 NOVEMBER 1914", ["The whole of the North Sea", "is declared a military area."], speed=36)
    s = T("From March 1915")
    fleet(s, ships=(("cruiser", "UK", 600, 700, 1), ("cargo", "NEUTRAL", 1350, 640, -1)), dur=6.0, close=(2.2, "sh1"), date="1915")

    s = T("It leaked, at first")
    MAP(s, [6.0, 55.0], 24, [arrow([[-30, 50], [4.5, 52.3], [8.5, 52.0]], "#3a6ea5", at=r(s, "importing a lot more"), dur=1.6, dashed=True),
                             arrow([[-20, 58], [10.5, 56.0], [11, 54.0]], "#3a6ea5", at=r(s, "importing a lot more") + 0.4, dur=1.6, dashed=True),
                             arrow([[4.8, 52.3], [7.5, 52.3]], "GERI", at=r(s, "selling a lot more"), dur=0.8, width=16),
                             arrow([[9.8, 56.0], [10.0, 54.3]], "GERI", at=r(s, "selling a lot more") + 0.3, dur=0.8, width=16)],
        colors=NORTH_SEA, legend=LEG_SEA, hatch=())
    s = T("But by 1915, Germany's imports")
    bars(s, "GERMAN IMPORTS", [("1913", 100, "#8a8f8c", 0.3), ("1915", 45, "GERI", r(s, "fallen by more than half"))], 100, unit="%")

    s = T("Then came a bad harvest")
    sc(s, {"kind": "countryside", "weather": "rain", "drift": 0}, [
        AID("f", "civilian_man", 960, 1000, None, "pointDown", "sad", turn=0.3, keys=mv((2.2, {"pose": "head", "expr": "cry"}))),
    ], [SHOT(0, None, "wide", zoom=1.0), SHOT(2.0, "f", "close", frameX=0.1)], world={"scale": 1.3, "y": 960}, date="WINTER 1916-17", tint="cold", ambience="rain")
    s = T("They still call it the Turnip Winter")
    kitchen(s)
    SCENES[-1]["elements"].append(L("THE TURNIP WINTER", 960, 985, "tag", 44, at=0.4, hud=True))
    s = T("By 1917, official rations")
    els = [AID(f"q{i}", ["civilian_woman", "civilian_man", "worker", "civilian_woman", "civilian_man"][i], 420 + i * 260, 980 - (i % 2) * 30, 1.35,
               ["idle", "rub", "chin", "pockets", "idle"][i], ["sad", "tired", "worried", "sad", "tired"][i], turn=-0.6, keys=mv((2.0 + i * 0.4, {"pose": "rub"})))
           for i in range(5)]
    els.append(CNT(0, 1000, 960, 985, at=r(s, "a thousand calories"), prefix="≈", suffix=" KCAL / DAY", size=56, dur=1.2, hud=True))
    sc(s, {"kind": "street", "weather": "snow", "drift": 0}, els, [SHOT(0, ["q0", "q4"], "full"), SHOT(r(s, "a third of what"), "q1", "close", frameX=0.12)],
       tint="cold", ambience="wind_cold")
    s = T("In December 1918, German officials claimed")
    bars(s, "CIVILIAN DEATHS FROM THE BLOCKADE", [("German claim, 1918", 763000, "#8a8f8c", r(s, "seven hundred and sixty-three")),
                                                  ("Study, 1928", 424000, "GERI", r(s, "four hundred and twenty-four"))], 800000)
    s = T("and later historians are more cautious")
    host(s, "shrug", "neutral", label="ESTIMATES · THE 1918 FLU IS MIXED IN", keys=mv((1.8, {"pose": "explain"})))
    s = T("Sir, that's not a moment")
    duo(s, [(0.0, "aide", "explain", "worried"), (r(s, "That's what makes it hard"), "host", "talk", "neutral"), (r(s, "It's the speed"), "host", "point!", "determined")])
    s = T("So, did the sand run out here? Not yet. The blockade")
    glass(s, level=0.1, to=0.3, dur_fall=6, plaque="LONG WAR", stamp="NOT YET", stamp_at=r(s, "Not yet.") + 0.5, cut_host=r(s, "But from now on"))
    s = T("Keep a turnip in mind")
    host(s, "show", "smug", holds="turnip", keys=mv((1.6, {"pose": "idle"})), second=(1.0, "close", "host"))

    # ================================================================ CHAPTER 3 — bleeding
    s = T("By the end of 1915, the man")
    sc(s, {"kind": "warroom", "fg": "officedesk"}, [
        AID("f", "falkenhayn", 1000, 1000, 1.6, "chin", "worried", turn=-0.3, keys=mv((r(s, "had a problem"), {"pose": "head"}))),
        NC("General Erich von Falkenhayn", "Chief of the General Staff, 1914-16", at=0.5)],
       [SHOT(0, "f", "medium", frameX=-0.1), SHOT(r(s, "had a problem"), "f", "close", frameX=0.12)], chapter="Bleeding", date="END OF 1915")
    s = T("Attacks on the Western Front gained")
    trench(s, "ww1_british", action="over", shells=((1.6, 1300, 520), (2.4, 600, 480)), close=None)
    s = T("So he went looking")
    sc(s, {"kind": "warroom", "fg": "officedesk"}, [
        AID("f", "falkenhayn", 900, 1000, 1.6, "write", "determined", holds="pen", turn=0.3, keys=mv((r(s, "if the French army"), {"pose": "explain", "holds": "", "talk": True})))],
       [SHOT(0, "f", "medium", frameX=0.1), SHOT(r(s, "if the French army"), "f", "close", frameX=-0.12)])
    s = T("Pick a place the French")
    sc(s, {"kind": "field", "drift": 0}, [
        {"id": "g1", "kind": "vehicle", "type": "artillery", "nation": "GERI", "x": 700, "y": 900},
        {"id": "g2", "kind": "vehicle", "type": "artillery", "nation": "GERI", "x": 1350, "y": 780},
        AID("c", "ww1_german", 470, 960, None, "cower", "determined"),
        FX("muzzle", 940, 760, **{"in": 1.0}), FX("smoke", 960, 760, **{"in": 1.05}), FX("muzzle", 1500, 690, **{"in": 1.8}), FX("smoke", 1510, 690, **{"in": 1.85})],
       [SHOT(0, None, "wide", zoom=1.0), SHOT(2.4, "g1", "full", shake=4)], world={"scale": 1.2, "y": 960}, sfx=[{"t": 1.0, "id": "cannon"}, {"t": 1.8, "id": "cannon"}])

    s = T("The place he picked was Verdun")
    MAP(s, [5.4, 49.2], 2.4, [city("Verdun", tag=True), arrow([[5.75, 49.45], [5.45, 49.25]], "GERI", at=1.0, dur=2.0), front([[5.1, 49.4], [5.6, 49.3], [5.7, 49.1]], "#7a2a22")],
        colors=WEST, legend=LEG_W, rivers=["Meuse"], date="FEBRUARY 1916")
    s = T("It became the longest battle")
    battlefield(s, "ww1_french", n=4, direction=1, run=True, shells=((0.5, 900, 760), (1.6, 1500, 820), (3.0, 600, 860)), close=(2.4, "m1"), dur=6.0)
    SCENES[-1]["elements"].append(L("≈ 300 DAYS", 1560, 170, "tag", 44, at=r(s, "about three hundred days"), hud=True))
    s = T("And the arithmetic never worked")
    bars(s, "VERDUN, 1916 — CASUALTIES (ONE ESTIMATE)", [("French", 377000, "FRA", r(s, "three hundred and seventy-seven")), ("German", 337000, "GERI", r(s, "three hundred and thirty-seven"))], 400000)
    s = T("That's roughly seventy thousand men a month")
    sc(s, {"kind": "mud", "drift": 0}, [
        *[{**PROP("cross", 400 + i * 230, 760 + (i % 3) * 60, 0.7 + (i % 3) * 0.2)} for i in range(6)],
        AID("g", "ww1_german", 1300, 1060, None, "head", "sad", keys=mv((r(s, "The army that was supposed") + 0.5, {"pose": "cower"})))],
       [SHOT(0, None, "wide", zoom=1.0, push=0.04), SHOT(r(s, "The army that was supposed"), "g", "close", frameX=0.12)], world={"scale": 1.2, "y": 960}, tint="grey")

    s = T("And while Verdun went on")
    MAP(s, [20.0, 50.5], 26, [front(EAST_FRONT, "#7a2a22"), city("Lutsk", at=0.6), arrow([[25.9, 50.4], [24.0, 50.0]], "RUS", at=1.0, dur=1.6)],
        colors=EUROPE, legend=LEG_CP, date="JUNE 1916")
    s = T("In June, the Russian general")
    sc(s, {"kind": "field", "drift": 0}, [
        AID("b", "brusilov", 1300, 1000, None, "point", "determined", turn=-0.3),
        *[{**AID(f"r{i}", "ww1_russian", 200 - i * 230, 820 + (i % 2) * 40, None, "charge", "shout", holds="rifle", keys=mv((5.0, {"x": 900 - i * 230, "ease": "linear"}))), "run": True} for i in range(4)],
        NC("General Aleksei Brusilov", "Russian South-Western Front", at=0.4)],
       [SHOT(0, "b", "mediumclose", frameX=0.12), SHOT(r(s, "smashed the Austro-Hungarian"), None, "wide", zoom=1.0, panX=120)], world={"scale": 1.0, "y": 900})
    s = T("Germany had to send divisions east")
    MAP(s, [16.0, 49.0], 30, [arrow([[8.0, 50.5], [14.0, 51.0], [22.5, 50.6]], "GERI", at=0.3, dur=2.0, label="DIVISIONS EAST"),
                              {"kind": "region", "polygon": [[22.4, 48.2], [26.6, 48.2], [29.6, 45.2], [28.6, 43.8], [22.7, 44.0], [21.0, 46.0]], "color": "#93ab6e", "fillOpacity": 0.6, "in": r(s, "Romania")},
                              L("ROMANIA JOINS THE ALLIES", 1300, 860, "tag", 34, at=r(s, "Romania") + 0.2)],
        colors=EUROPE, legend=LEG_CP)

    s = T("Then, on the 1st of July")
    trench(s, "ww1_british", n=3, action="over", shells=((1.2, 900, 460), (2.0, 1500, 500)), close=None, date="1 JULY 1916", place="THE SOMME")
    s = T("On its first day")
    sc(s, {"kind": "memorial", "drift": 0}, [
        CNT(0, 57470, 960, 420, at=0.3, suffix=" CASUALTIES", size=96, dur=1.6),
        CNT(0, 19240, 960, 600, at=r(s, "including nineteen thousand"), suffix=" KILLED", size=72, dur=1.2, color="#f08070"),
        L("WORST DAY IN BRITISH ARMY HISTORY", 960, 820, "tag", 38, at=r(s, "It's still the worst day"))], [SHOT(0, None, None, zoom=1.0, push=0.05)], tint="grey")
    s = T("But the battle went on")
    battlefield(s, "ww1_german", n=4, direction=-1, shells=((0.8, 800, 780), (2.2, 1300, 840)), close=(2.4, "m1"), dur=6.0)
    SCENES[-1]["elements"].append(L("141 DAYS", 1560, 170, "tag", 44, at=r(s, "a hundred and forty-one"), hud=True))
    s = T("In September, the first tanks")
    battlefield(s, "ww1_british", n=3, direction=1, tanks=("markiv", 1), shells=((2.0, 1500, 800),), close=(2.6, "t0"), dur=8.0, date="SEPTEMBER 1916")

    s = T("By the end of August, Falkenhayn")
    sc(s, {"kind": "warroom", "fg": "officedesk"}, [
        AID("f", "falkenhayn", 1000, 1000, 1.55, "idle", "sad", keys=mv((0.4, {"x": 1000}), (3.9, {"x": 2200, "ease": "in"}))),
        AID("h", "hindenburg", -260, 1000, 1.55, "idle", "determined", keys=mv((r(s, "Hindenburg and Ludendorff"), {"x": -260}), (r(s, "Hindenburg and Ludendorff") + 3.0, {"x": 760}))),
        AID("l", "ludendorff", -200, 1005, 1.5, "idle", "smug", keys=mv((r(s, "Hindenburg and Ludendorff") + 0.3, {"x": -200}), (r(s, "Hindenburg and Ludendorff") + 3.6, {"x": 1160}), (r(s, "military dictatorship"), {"pose": "slam"})))],
       [SHOT(0, None, None, zoom=1.0, push=0.03), SHOT(r(s, "military dictatorship") - 0.4, ["h", "l"], "medium")], date="AUGUST 1916")
    s = T("They tried to squeeze more")
    sc(s, {"kind": "factory", "drift": 0}, [
        AID("w1", "worker", 560, 1000, 1.5, "typing", "tired", turn=0.3), AID("w2", "civilian_man", 1000, 1000, 1.5, "carry", "tired", holds="shell", look_={"age": 0.85}),
        AID("w3", "worker", 1440, 1000, 1.45, "typing", "sad", turn=-0.3, look_={"age": 0.05}),
        L("WAR SERVICE: AGES 17-60", 960, 160, "tag", 40, at=r(s, "seventeen to sixty"))],
       [SHOT(0, ["w1", "w3"], "full"), SHOT(r(s, "It never came close"), "w2", "close", frameX=0.1)])
    s = T("On the other side of the wire")
    doc(s, "order", "MILITARY SERVICE ACT · JANUARY 1916", ["Every unmarried man aged 18-41", "is deemed to have enlisted."], speed=40)
    s = T("The Allies were not going to run out")
    march_col(s, "ww1_british", n=6, set_="countryside", direction=1, expr="determined", dur=6.0, close=None)
    s = T("Sir, a million casualties")
    duo(s, [(0.0, "aide", "explain", "sad"), (r(s, "Terrible, Porter"), "host", "talk", "sad"), (r(s, "The sand's falling"), "host", "point!", "neutral")])
    s = T("So, did the sand run out here? Not yet. 1916")
    glass(s, level=0.3, to=0.42, dur_fall=6, plaque="LONG WAR", stamp="NOT YET", stamp_at=r(s, "Not yet.") + 0.4, cut_host=r(s, "It did not prove"))
    s = T("Quick one before the next train")
    host(s, "thumbsup", "happy", aide=True, aide_keys=mv((r(s, "unlike a Western Front"), {"pose": "cheer", "expr": "laugh"})),
         second=(r(s, "unlike a Western Front"), "close", "host"))

    # ================================================================ CHAPTER 4 — Jutland
    s = T("If Germany couldn't break the blockade")
    fleet(s, ships=(("uboat", "GERI", 600, 700, 1), ("battleship", "GERI", 1300, 640, 1)), set_="sea", dur=6, chapter="Who Held the Door")
    s = T("Germany's battle fleet, the High Seas Fleet")
    sc(s, {"kind": "harbor", "drift": 0}, [
        {"id": "b1", "kind": "vehicle", "type": "battleship", "nation": "GERI", "x": 760, "y": 660, "scale": 0.55},
        AID("s1", "ww1_sailor_de", 1240, 1000, 1.5, "smoke", "tired", turn=-0.4), AID("s2", "ww1_sailor_de", 1560, 1000, 1.5, "chin", "neutral", turn=-0.6, keys=mv((2.0, {"pose": "pockets"})))],
       [SHOT(0, None, "wide", zoom=1.0), SHOT(r(s, "spent most of it in port"), ["s1", "s2"], "medium")], place="WILHELMSHAVEN")
    s = T("So the new German commander")
    sc(s, {"kind": "cabin", "fg": "officedesk"}, [
        AID("sch", "scheer", 980, 1000, 1.6, "pointDown", "determined", turn=-0.2, keys=mv((r(s, "Lure out part"), {"pose": "explain", "talk": True}), (r(s, "even the odds"), {"pose": "fist", "expr": "smug"}))),
        NC("Admiral Reinhard Scheer", "High Seas Fleet", at=0.5), {**PROP("paper", 940, 872, 0.7), "rotate": 80}],
       [SHOT(0, "sch", "medium", frameX=0.1), SHOT(r(s, "even the odds") - 0.4, "sch", "close", frameX=-0.12)])
    s = T("The British had been reading")
    sc(s, {"kind": "codebreak", "fg": "officedesk"}, [
        AID("c1", "civilian_man", 760, 1000, 1.55, "write", "neutral", holds="pen", turn=0.3, look_={"glasses": "round"}, keys=mv((r(s, "a big operation"), {"pose": "pointUp", "expr": "shocked", "holds": ""}))),
        AID("c2", "ww1_british", 1220, 1000, 1.5, "chin", "neutral", turn=-0.4, keys=mv((r(s, "a big operation") + 0.4, {"expr": "worried"})))],
       [SHOT(0, ["c1", "c2"], "medium"), SHOT(r(s, "a big operation") - 0.2, "c1", "close", frameX=-0.12)], place="ROOM 40, LONDON")
    s = T("On the 30th of May")
    sc(s, {"kind": "cabin", "drift": 0}, [AID("j", "jellicoe", 960, 1000, 1.6, "binoculars", "determined", holds="binoculars", turn=0.1),
                                          NC("Admiral Sir John Jellicoe", "Grand Fleet", at=0.4)],
       [SHOT(0, "j", "mediumclose", push=0.05)], date="30 MAY 1916")
    s = T("put to sea")
    fleet(s, ships=(("battleship", "UK", 300, 720, 1), ("battleship", "UK", 900, 670, 1), ("cruiser", "UK", 1500, 630, 1)), dur=6)
    s = T("The next afternoon")
    MAP(s, [5.5, 56.5], 14, [city("Wilhelmshaven", at=0.2), city("Scapa Flow", at=0.2),
                             {"kind": "route", "path": [[8.1, 53.8], [7.0, 55.5], [6.3, 56.8]], "color": "GERI", "width": 5, "icon": "warship", "trail": 2, "gap": 70, "iconSize": 1.0, "nation": "GERI", "enter": "draw", "dur": 3.0, "in": 0.2},
                             {"kind": "route", "path": [[-2.9, 58.7], [2.0, 57.6], [5.4, 57.0]], "color": "#3a6ea5", "width": 5, "icon": "warship", "trail": 3, "gap": 70, "iconSize": 1.0, "nation": "UK", "enter": "draw", "dur": 3.0, "in": 0.4},
                             {"kind": "burst", "at": [6.0, 56.9], "size": 0.7, "in": 3.4}, L("JUTLAND", 1180, 300, "tag", 40, at=r(s, "off the coast of Jutland"))],
        colors=NORTH_SEA, legend=LEG_SEA, hatch=(), date="31 MAY 1916")
    s = T("It was the only full-scale clash")
    fleet(s, ships=(("battleship", "GERI", 1450, 640, -1), ("battleship", "UK", 480, 720, 1)), firing=((0.4, 0), (1.0, 1), (2.4, 0)),
          hits=((1.3, 700, 760), (2.8, 1200, 680)), dur=6, close=(3.0, "sh1"))
    s = T("On paper, the Germans won it")
    bars(s, "TONNAGE SUNK AT JUTLAND", [("British ships lost", 115000, "UK", r(s, "a hundred and fifteen thousand tons")),
                                        ("German ships lost", 62000, "GERI", r(s, "sixty-two thousand tons"))], 120000, unit=" t")
    SCENES[-1]["elements"] += [L("99 GERMAN SHIPS", 600, 960, "tag", 32, at=r(s, "ninety-nine ships")), L("151 BRITISH SHIPS", 1320, 960, "tag", 32, at=r(s, "a hundred and fifty-one"))]
    s = T("More than twice as many British sailors")
    fleet(s, ships=(("battleship", "UK", 900, 700, 1),), dur=6)
    SCENES[-1]["elements"] += [FX("explosion", 900, 560, **{"in": 0.4}), FX("smoke", 900, 520, **{"in": 0.5}), FX("fire", 860, 600, **{"in": 0.6})]
    SCENES[-1]["tint"] = "grey"
    s = T("In Germany, schoolchildren")
    sc(s, {"kind": "street", "drift": 0}, [
        *[AID(f"k{i}", ["civilian_man", "civilian_woman"][i % 2], 500 + i * 300, 1000, 1.05, ["cheer", "wave", "raise", "cheer"][i], ["laugh", "happy", "smile", "laugh"][i],
              look_={"age": 0.0, "build": 0.85}, keys=mv((0.5 + i * 0.37, {"pose": ["wave", "cheer", "cheer", "raise"][i]}))) for i in range(4)],
        {"kind": "flag", "nation": "GERI", "x": 1640, "y": 420, "w": 200, "h": 130}],
       [SHOT(0, ["k0", "k3"], "full"), SHOT(r(s, "and the Kaiser announced"), None, None, zoom=1.0)], date="JUNE 1916")
    SCENES[-1]["elements"].append(L("THE KAISER: \"A NEW CHAPTER IN WORLD HISTORY\"", 960, 985, "tag", 32, at=r(s, "and the Kaiser announced") + 0.2, hud=True))
    s = T("So Germany won, sir?")
    duo(s, [(0.0, "aide", "explain", "happy"), (r(s, "Germany won the afternoon"), "host", "talk", "smug"), (r(s, "Check who was still"), "host", "point!", "smug")])
    s = T("Here's the paperwork, on the German side")
    sc(s, {"kind": "cabin", "fg": "officedesk"}, [
        AID("sch", "scheer", 980, 1000, 1.6, "write", "worried", holds="pen", turn=0.2, keys=mv((r(s, "wear out his fleet"), {"pose": "chin", "holds": ""})))],
       [SHOT(0, "sch", "medium", frameX=0.1), SHOT(r(s, "wear out his fleet") - 0.3, "sch", "close", frameX=-0.12)])
    s = T("In August, another sortie")
    MAP(s, [3.0, 55.0], 14, [{"kind": "route", "path": [[8.1, 53.8], [4.5, 54.6], [8.0, 54.0]], "color": "GERI", "width": 5, "icon": "warship", "trail": 1, "gap": 70, "nation": "GERI", "enter": "draw", "dur": 3.0, "in": 0.2},
                             arrow([[-2.0, 57.5], [2.0, 55.4]], "UK", at=1.0, dur=1.6, dashed=True), L("NEARLY CAUGHT", 960, 160, "tag", 40, at=r(s, "nearly caught"))],
        colors=NORTH_SEA, legend=LEG_SEA, hatch=(), date="AUGUST 1916")
    s = T("After that, the High Seas Fleet")
    sc(s, {"kind": "harbor", "drift": 0}, [
        {"kind": "vehicle", "type": "battleship", "nation": "GERI", "x": 900, "y": 660, "scale": 0.55},
        AID("s1", "ww1_sailor_de", 1400, 1000, 1.5, "chin", "tired", turn=-0.5, keys=mv((2.4, {"pose": "smoke"})))],
       [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(2.2, "s1", "mediumclose", frameX=0.12)], tint="cold")
    s = T("The blockade stayed exactly")
    MAP(s, [2.0, 55.8], 34, [{"kind": "line", "path": [[1.0, 51.4], [1.9, 50.9]], "color": "#2b4d7a", "width": 9, "in": 0.2, "enter": "draw", "dur": 0.6},
                             {"kind": "line", "path": [PL["Shetland"], PL["Bergen"]], "color": "#2b4d7a", "width": 9, "in": 0.5, "enter": "draw", "dur": 0.8},
                             L("BLOCKADE: UNCHANGED", 960, 160, "tag", 40, at=0.8)], colors=NORTH_SEA, legend=LEG_SEA, hatch=())
    s = T("Historians still argue")
    host(s, "shrug", "neutral", keys=mv((r(s, "much less argument"), {"pose": "explain", "expr": "smug"})), second=(r(s, "By the end of 1916"), "close", "host"))
    s = T("That left it with only one weapon")
    fleet(s, ships=(("uboat", "GERI", 600, 760, 1),), dur=6, close=(r(s, "The submarine") - 0.2, "sh0"))
    SCENES[-1]["tint"] = "cold"
    s = T("So, did the sand run out here? Not yet. But Jutland")
    glass(s, level=0.42, to=0.5, dur_fall=6, plaque="LONG WAR", stamp="NOT YET", stamp_at=r(s, "Not yet.") + 0.4)
