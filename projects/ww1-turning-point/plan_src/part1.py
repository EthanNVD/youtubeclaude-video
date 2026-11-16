"""Cold open, the list, the hourglass rule, chapter 1 (the Marne). 0:00 - 7:23"""
from lib import *  # noqa: F401,F403
from lib import sc, host, duo, glass, hq, report, march_col, trench, battlefield, fleet, doc, quote, MAP, city, arrow, front, PL, \
    EUROPE, WEST, LEG_CP, LEG_W, WESTERN_FRONT, SPRING_1918, HINDENBURG, EAST_FRONT, mv  # noqa: E402


def r(start, phrase):
    """time of `phrase` relative to a scene start (does not move the cursor)"""
    return round(peek(phrase) - start, 2)


def build():
    # ================================================================ COLD OPEN — "Two Hours"
    s = T("On the 29th of September")
    sc(s, {"kind": "hotel", "drift": 0}, [
        {"id": "car", "kind": "vehicle", "type": "car", "nation": "GERI", "x": -300, "y": 930, "keys": mv((2.6, {"x": 700}))},
        AID("hin", "hindenburg", 760, 960, None, "idle", "neutral", out=None, **{"in": 2.8}, keys=mv((3.0, {"x": 760}), (5.6, {"x": 1180}))),
        AID("lud", "ludendorff", 640, 965, None, "idle", "determined", **{"in": 3.0}, keys=mv((3.2, {"x": 640}), (5.8, {"x": 1060}))),
    ], [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(3.4, ["hin", "lud"], "full", track=True)],
       world={"scale": 1.1, "y": 940}, date="29 SEPTEMBER 1918", place="SPA, BELGIUM", chapter="Two Hours", letterbox="DRAMATISED — SPA, 29 SEPTEMBER 1918")

    s = T("Field Marshal Paul von Hindenburg")
    hq(s, [("kaiser", "kaiser_wilhelm", "write", "neutral", mv((r(s, "told Kaiser Wilhelm"), {"pose": "idle", "expr": "neutral"}))),
           ("hin", "hindenburg", "idle", "worried", mv((1.5, {"pose": "chin"}))),
           ("lud", "ludendorff", "explain", "determined", mv((r(s, "could no longer"), {"pose": "talk2"})))],
       set_="cabinet", talk=2,
       cuts=[(r(s, "General Erich Ludendorff"), "lud", "mediumclose"), (r(s, "told Kaiser Wilhelm"), "kaiser", "mediumclose"),
             (r(s, "could no longer"), "lud", "close")],
       extra=None) if False else None
    sc(s, {"kind": "cabinet", "desk": False, "fg": "officedesk"}, [
        AID("kaiser", "kaiser_wilhelm", 1150, 1000, 1.55, "write", "neutral", holds="pen", turn=-0.4,
            keys=mv((r(s, "told Kaiser Wilhelm"), {"pose": "idle", "holds": "", "turn": -0.7}))),
        AID("hin", "hindenburg", 520, 1000, 1.55, "idle", "worried", turn=0.5, keys=mv((2.5, {"pose": "chin"}))),
        AID("lud", "ludendorff", 800, 1005, 1.5, "idle", "determined", turn=0.55, keys=mv((r(s, "General Erich"), {"pose": "explain", "talk": True}), (r(s, "could no longer"), {"pose": "talk2"}))),
        NC("Field Marshal Paul von Hindenburg", "Chief of the General Staff", at=0.4, out=r(s, "General Erich") - 0.2),
        NC("General Erich Ludendorff", "First Quartermaster-General", at=r(s, "General Erich") + 0.1),
    ], [SHOT(0, ["hin", "lud", "kaiser"], "full", push=0.03), SHOT(r(s, "General Erich"), "lud", "medium", frameX=-0.15),
        SHOT(r(s, "told Kaiser Wilhelm"), "kaiser", "mediumclose", frameX=0.15), SHOT(r(s, "could no longer"), "lud", "close", frameX=-0.15)],
       place="IMPERIAL HQ")

    s = T("Not for weeks")
    sc(s, {"kind": "cabinet", "desk": False}, [
        AID("lud", "ludendorff", 900, 1000, 1.55, "talk", "worried", talk=True, turn=0.4, keys=mv((r(s, "Not for days"), {"pose": "fist"}), (r(s, "For two hours"), {"pose": "count", "expr": "panic"}))),
        AID("kaiser", "kaiser_wilhelm", 1400, 1000, 1.55, "idle", "neutral", turn=-0.6, keys=mv((r(s, "For two hours") + 0.3, {"expr": "shocked", "pose": "head"}))),
        {**PROP("clock", 1500, 300, 1.2, value=17), "id": "clk"},
    ], [SHOT(0, "lud", "close", frameX=-0.1), SHOT(r(s, "For two hours") - 0.15, "kaiser", "close", frameX=0.12, push=0.08)], clock="2 HOURS")

    s = T("Germany needed an armistice")
    sc(s, {"kind": "cabinet", "desk": False, "fg": "officedesk"}, [
        AID("kaiser", "kaiser_wilhelm", 960, 1000, 1.6, "head", "shocked", turn=0, keys=mv((1.4, {"pose": "facepalm", "expr": "sad"}))),
        {**PROP("paper", 1180, 872, 0.7), "rotate": 80},
    ], [SHOT(0, "kaiser", "medium", push=0.06)])

    s = T("The Kaiser could hardly believe it")
    sc(s, {"kind": "cabinet", "desk": False}, [
        AID("kaiser", "kaiser_wilhelm", 960, 1000, 1.6, "facepalm", "sad", turn=0.3, keys=mv((r(s, "and you can see why"), {"pose": "idle", "turn": 0.6, "look": 1}))),
    ], [SHOT(0, "kaiser", "close", frameX=-0.1, push=0.04)])

    s = T("Six months earlier")
    battlefield(s, "ww1_german", n=5, direction=1, run=True, shells=((1.0, 1500, 760), (2.6, 1700, 820)), close=(2.2, "m1"), dur=7.0,
                date="SPRING 1918", tint="sepia")

    s = T("In early June")
    MAP(s, [2.9, 49.4], 5.2, [
        front(SPRING_1918, "#5a5a52"), city("Paris", tag=True, at=0.3), city("Château-Thierry", at=0.6, side="left"), city("Reims", at=0.8),
        {"kind": "line", "path": [PL["Château-Thierry"], PL["Paris"]], "color": "#7a2a22", "dashed": True, "in": 1.2, "enter": "draw", "dur": 1.2, "width": 5},
        L("56 KM", 1020, 520, "red", 44, at=r(s, "fifty-six") if False else 2.0),
    ], colors=WEST, legend=LEG_W, date="JUNE 1918")

    s = T("So how does an army go")
    MAP(s, [3.4, 49.6], 6.0, [front(SPRING_1918, "#5a5a52", path2=HINDENBURG, morph_dur=5.0), city("Paris", tag=True), city("Spa", at=1.0)],
        colors=WEST, legend=LEG_W, date="SUMMER 1918")

    s = T("Or had the war really been lost")
    glass(s, level=0.82, to=0.98, dur_fall=6.0, plaque="GERMANY")

    # ================================================================ THE LIST — a quick montage of candidates
    s = T("Ask around")
    host(s, "explain", "smug", label=None, keys=mv((1.4, {"pose": "count"})))
    s = T("The Marne, in 1914")
    battlefield(s, "ww1_french_1914", n=5, direction=-1, run=True, shells=((0.8, 600, 780),), dur=5.0, close=(2.6, "m1"), date="1914")
    s = T("The British blockade")
    fleet(s, ships=(("battleship", "UK", 520, 700, 1), ("cruiser", "UK", 1300, 640, 1)), dur=4.0)
    s = T("The bloodbath at Verdun")
    trench(s, "ww1_french", action="cower", shells=((0.3, 700, 300), (1.1, 1300, 260)), close=1.2, date="1916")
    s = T("A great sea battle")
    fleet(s, ships=(("battleship", "GERI", 1400, 640, -1), ("battleship", "UK", 520, 720, 1)), firing=((0.4, 1), (0.9, 0)), hits=((1.2, 1180, 660), (1.7, 760, 740)), dur=4.0)
    s = T("A decision taken at a castle")
    sc(s, {"kind": "conference", "desk": False, "fg": "officedesk"}, [
        AID("k", "kaiser_wilhelm", 960, 1000, 1.55, "write", "determined", holds="pen"),
        AID("hz", "holtzendorff", 1340, 1000, 1.5, "present", "smug", turn=-0.5),
        {**PROP("paper", 1000, 872, 0.7), "rotate": 80},
    ], [SHOT(0, ["k", "hz"], "full"), SHOT(2.4, "k", "mediumclose", frameX=-0.1)], date="JANUARY 1917", tint="sepia")
    s = T("A black day in August 1918")
    battlefield(s, "ww1_australian", n=4, tanks=("markiv", 2), surrender=3, dur=5.0, close=(2.4, "g0"), date="AUGUST 1918")
    s = T("And for twenty years after the war")
    doc(s, "newspaper", "1919-1933", ["\"IM FELDE UNBESIEGT\"", "UNDEFEATED IN THE FIELD"], speed=30)

    s = T("So, what was the real turning point")
    host(s, "explain", "neutral", label="THE REAL TURNING POINT?", keys=mv((1.6, {"pose": "chin", "expr": "smug"})))
    s = T("Sir, it ended in 1918")
    duo(s, [(0.0, "aide", "explain", "neutral"), (r(s, "That's when the train"), "host", "talk", "smug"), (r(s, "I want to know"), "host", "point!", "smug")])

    # ================================================================ THE RULE — the hourglass
    s = T("Eight moments, two alliances")
    glass(s, level=0.0, plaque="GERMANY", chapter="The Hourglass", cut_host=r(s, "Here's why an hourglass"))
    s = T("Every big German plan")
    sc(s, {"kind": "workshop"}, [{"kind": "timeline", "x": 960, "y": 560, "width": 1500, "items": [
        {"sub": "1914", "label": "Beat France before Russia is ready", "at": 0.17, "color": "GERI", "in": r(s, "In 1914")},
        {"sub": "1917", "label": "Starve Britain before America arrives", "at": 0.5, "color": "GERI", "in": r(s, "In 1917")},
        {"sub": "1918", "label": "Win before the Americans arrive", "at": 0.8, "color": "GERI", "in": r(s, "In 1918")}]},
        L("EVERY PLAN HAD A DEADLINE", 960, 150, "tag", 42, at=0.4)], [SHOT(0, None, None, zoom=1.0, push=0.05)])
    s = T("Germany was always racing a clock")
    glass(s, level=0.1, to=0.3, dur_fall=4.0, plaque="GERMANY")
    s = T("So here's the rule")
    host(s, "explain", "neutral", second=(r(s, "It's the day Germany"), "close", "host"), keys=mv((r(s, "It's the day Germany"), {"pose": "point", "expr": "determined"})))
    s = T("We'll go in order")
    glass(s, level=0.3, plaque="GERMANY", stamp="NOT YET", stamp_at=r(s, "Turned, or not yet") + 0.6, label=None) if False else \
        glass(s, level=0.3, plaque="GERMANY", stamp="NOT YET", stamp_at=r(s, "Turned, or not yet") + 0.6)
    s = T("And one of these moments")
    glass(s, level=0.6, to=0.62, flip_at=r(s, "It turns the hourglass") + 0.2, plaque="GERMANY")
    s = T("Glass is full")
    host(s, "count", "smug", keys=mv((r(s, "Timetable says"), {"pose": "explain"}), (r(s, "Let's see"), {"pose": "idle"})),
         second=(r(s, "Let's see") - 0.3, "close", "host"))

    # ================================================================ CHAPTER 1 — the Marne
    s = T("Start with the problem")
    MAP(s, [14.0, 51.0], 34, [city("Berlin", capital=True) if False else city("Berlin"), city("Paris", at=0.6), city("Petrograd", at=1.0)],
        colors=EUROPE, legend=LEG_CP, date="1914", chapter="Forty Days to Paris")
    s = T("A war with one meant")
    MAP(s, [14.0, 51.0], 34, [city("Berlin"), city("Paris"), arrow(["Berlin", [6.5, 49.5]], "GERI", at=0.3, dur=1.2, dashed=True),
                              arrow(["Berlin", [21.5, 53.5]], "GERI", at=0.9, dur=1.2, dashed=True), L("TWO FRONTS", 960, 160, "tag", 44, at=1.6)],
        colors=EUROPE, legend=LEG_CP)
    s = T("So the German General Staff")
    sc(s, {"kind": "warroom", "fg": "officedesk"}, [
        AID("m", "moltke", 760, 1000, 1.55, "explain", "determined", talk=False, turn=0.4, keys=mv((2.0, {"pose": "pointDown"}))),
        AID("o1", "falkenhayn", 1180, 1000, 1.5, "write", "neutral", holds="pen", turn=-0.4, keys=mv((3.0, {"pose": "chin", "holds": ""}))),
        {**PROP("stopwatch", 960, 820, 0.9), "front": True},
        {**PROP("paper", 1100, 872, 0.7), "rotate": 80},
    ], [SHOT(0, ["m", "o1"], "medium"), SHOT(1.8, None, None, zoom=2.2, x=960, y=760, push=0.04), SHOT(3.1, "m", "close", frameX=-0.12)])
    s = T("Defeat France fast")
    MAP(s, [12.0, 51.0], 30, [city("Paris", tag=True), arrow(["Berlin", [7.0, 49.8], [3.4, 49.2]], "GERI", at=0.3, dur=1.5, label="6 WEEKS"),
                              arrow([[6.0, 50.5], "Berlin", [21.0, 53.8]], "GERI", at=r(s, "then put the army on trains"), dur=1.8, dashed=True)],
        colors=EUROPE, legend=LEG_CP)

    WHEEL = [[6.8, 51.0], [5.6, 50.7], [4.0, 50.4], [2.6, 49.9], [1.8, 49.2], [2.0, 48.4], [3.0, 48.0], [4.6, 48.4]]
    s = T("The road to Paris ran through Belgium")
    MAP(s, [4.2, 49.6], 7.5, [city("Paris", tag=True), city("Brussels", at=0.3), city("Liège", at=0.5), arrow(WHEEL[:4], "GERI", at=0.6, dur=2.0, dashed=True)],
        colors=WEST, legend=LEG_W)
    s = T("The plan was first drawn up")
    sc(s, {"kind": "study", "desk": False, "fg": "officedesk"}, [
        AID("sch", "schlieffen", 900, 1000, 1.55, "write", "determined", holds="pen", turn=0.3),
        NC("Field Marshal Alfred von Schlieffen", "Chief of the General Staff to 1906", at=0.3, out=r(s, "then reworked") - 0.3),
    ], [SHOT(0, "sch", "medium", frameX=0.1, push=0.05)], tint="sepia")
    s = T("then reworked by his successor")
    sc(s, {"kind": "warroom", "fg": "officedesk"}, [
        AID("m", "moltke", 1000, 1000, 1.6, "pointDown", "neutral", turn=-0.3, keys=mv((2.0, {"pose": "chin"}))),
        NC("Colonel General Helmuth von Moltke", "Chief of the General Staff, 1906-1914", at=0.3),
    ], [SHOT(0, "m", "medium", frameX=-0.15, push=0.04)])
    s = T("It sent the German right wing")
    MAP(s, [4.2, 49.6], 7.5, [city("Paris", tag=True), arrow(WHEEL, "GERI", at=0.3, dur=4.0, dashed=True, label="RIGHT WING"),
                              arrow([[4.6, 48.4], [5.4, 48.7]], "GERI", at=r(s, "then trap") if False else 4.6, dur=1.0, dashed=True)],
        colors=WEST, legend=LEG_W)
    s = T("It was a plan that depended on speed")
    sc(s, {"kind": "railway", "drift": 0}, [
        {"id": "train", "kind": "vehicle", "type": "train", "nation": "GERI", "x": -900, "y": 900, "scale": 2.2, "keys": mv((5.0, {"x": 1100}))},
        AID("off", "ww1_german_1914", 1560, 1000, 1.6, "idle", "determined", holds="stopwatch", holdsScale=0.45, turn=-0.5, keys=mv((2.0, {"pose": "show"}))),
    ], [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(2.4, "off", "mediumclose", frameX=0.15)])

    s = T("And in August 1914, for a while")
    march_col(s, "ww1_german_1914", n=6, set_="countryside", direction=1, expr="determined", dur=9.0, close=4.0, date="AUGUST 1914", place="BELGIUM")
    s = T("The French had planned")
    MAP(s, [5.0, 49.0], 8, [city("Metz", at=0.3), city("Mulhouse", at=0.3), arrow([[5.4, 48.4], [6.4, 48.8]], "FRA", at=0.5, dur=1.2),
                            arrow([[6.6, 47.4], [7.3, 47.8]], "FRA", at=0.9, dur=1.0), L("FAILED", 1350, 640, "red", 40, at=r(s, "failed badly"))],
        colors=WEST, legend=LEG_W)
    s = T("Their commander, General Joseph Joffre")
    sc(s, {"kind": "warroom", "fg": "officedesk"}, [
        AID("joffre", "joffre", 1040, 1000, 1.6, "pointDown", "smug", turn=-0.3, keys=mv((r(s, "clung to that plan"), {"pose": "cross"}))),
        NC("General Joseph Joffre", "French Commander-in-Chief", at=0.4, out=r(s, "even as one") - 0.2),
        AID("lan", "lanrezac", -200, 1000, 1.5, "idle", "worried", **{"in": r(s, "even as one") - 1.0},
            keys=mv((r(s, "even as one") - 0.8, {"x": -200}), (r(s, "even as one") + 1.2, {"x": 560}), (r(s, "kept warning"), {"pose": "pointL", "talk": True}))),
        NC("General Charles Lanrezac", "French Fifth Army", at=r(s, "Charles Lanrezac")),
    ], [SHOT(0, "joffre", "medium", frameX=-0.12), SHOT(r(s, "even as one") - 0.2, ["lan", "joffre"], "full"),
        SHOT(r(s, "kept warning"), "lan", "close", frameX=0.12), SHOT(r(s, "the real German blow") + 0.6, "joffre", "close", frameX=-0.12)])
    s = T("On the 24th of August")
    sc(s, {"kind": "warroom", "fg": "officedesk"}, [
        AID("joffre", "joffre", 960, 1000, 1.6, "chin", "worried", turn=0.2, keys=mv((r(s, "admitted"), {"pose": "pointDown", "expr": "nervous"}))),
        {**PROP("paper", 900, 872, 0.7), "rotate": 80},
    ], [SHOT(0, "joffre", "mediumclose", frameX=0.1)], date="24 AUGUST 1914")
    s = T("By then, the French and British armies")
    march_col(s, "ww1_french_1914", n=6, set_="countryside", direction=-1, expr="tired", dur=7.0, close=2.6)
    s = T("It was a hot summer")
    march_col(s, "ww1_french_1914", n=4, set_="field", direction=-1, expr="sweat", dur=9.0, close=1.0)
    SCENES[-1]["shots"].append(SHOT(5.2, None, "wide", zoom=1.08, x=1100, push=0.03))
    SCENES[-1]["elements"].append(L("PACK ≈ 27 KG", 1500, 300, "tag", 40, at=r(s, "carrying packs"), hud=True))
    s = T("The Germans kept going because")
    march_col(s, "ww1_german_1914", n=5, set_="countryside", direction=1, expr="smile", dur=8.0, close=2.0)
    SCENES[-1]["elements"].append({**PROP("sign", 1700, 900, 0.9), "text": "PARIS"})

    s = T("But the German wheel")
    MAP(s, [5.0, 49.8], 9.0, [city("Paris"), arrow(WHEEL[:5], "GERI", at=0.1, dur=1.6, dashed=True)], colors=WEST, legend=LEG_W)
    s = T("Worried about the Russians")
    sc(s, {"kind": "warroom", "fg": "officedesk"}, [
        AID("m", "moltke", 960, 1000, 1.6, "chin", "worried", turn=0.3, keys=mv((r(s, "perhaps a little overconfident"), {"expr": "smug", "pose": "hips"}))),
    ], [SHOT(0, "m", "medium", frameX=0.1), SHOT(r(s, "perhaps a little overconfident"), "m", "close", frameX=-0.12)])
    s = T("pulled two whole army corps")
    MAP(s, [9.0, 51.0], 22, [city("Paris"), arrow([[5.2, 50.6], [13.4, 52.5], [20.5, 54.0]], "GERI", at=0.2, dur=2.4, label="2 CORPS EAST")],
        colors=EUROPE, legend=LEG_CP)
    s = T("Two more were left behind")
    MAP(s, [4.0, 50.4], 6.0, [city("Antwerp", at=0.3), city("Maubeuge", at=0.6), city("Paris", at=0.2),
                              {"kind": "unit", "type": "inf", "nation": "GERI", "at": [4.7, 51.1], "label": "SIEGE", "in": 0.5},
                              {"kind": "unit", "type": "inf", "nation": "GERI", "at": [4.2, 50.2], "label": "SIEGE", "in": 1.0},
                              CNT(0, 200000, 1240, 960, at=r(s, "two hundred thousand"), prefix="−", suffix=" MEN", size=80, dur=1.4, hud=True)],
        colors=WEST, legend=LEG_W)
    s = T("Moltke realised")
    MAP(s, [3.6, 49.3], 6.0, [city("Paris", tag=True), arrow([[4.6, 50.6], [3.6, 49.7], [3.1, 49.0], [3.3, 48.5]], "GERI", at=1.2, dur=3.0, dashed=True), L("EAST OF PARIS, NOT WEST", 1200, 900, "tag", 38, at=r(s, "pass east of the city"))],
        colors=WEST, legend=LEG_W)

    s = T("The commander of that right wing")
    sc(s, {"kind": "field", "drift": 0}, [
        AID("kluck", "kluck", 1260, 980, None, "binoculars", "smug", holds="binoculars", turn=-0.2, keys=mv((r(s, "read his orders broadly"), {"pose": "hips", "holds": ""}), (r(s, "or ignored them"), {"pose": "cross"}))),
        *[{**AID(f"c{i}", "ww1_german_1914", 200 - i * 240, 760, None, "shoulder", "tired", holds="rifle", keys=mv((9.0, {"x": 700 - i * 240, "ease": "linear"})))} for i in range(4)],
        NC("General Alexander von Kluck", "German First Army", at=0.5),
    ], [SHOT(0, None, "wide", zoom=1.0), SHOT(r(s, "read his orders broadly"), "kluck", "mediumclose", frameX=0.12)], world={"scale": 1.0, "y": 900})
    s = T("He turned southeast")
    MAP(s, [3.2, 48.9], 3.0, [city("Paris", tag=True, at=0.2), city("Meaux", at=0.4), city("Château-Thierry", at=0.4),
                              arrow([[3.4, 49.6], [3.1, 49.25], [3.25, 48.85]], "GERI", at=0.5, dur=2.4, label="FIRST ARMY")],
        colors=WEST, legend=LEG_W, rivers=["Marne", "Seine", "Oise"], date="3 SEPTEMBER 1914")
    s = T("Kluck didn't know")
    MAP(s, [3.0, 48.9], 3.0, [city("Paris", tag=True), {"kind": "unit", "type": "inf", "nation": "FRA", "at": [2.65, 49.05], "label": "6th ARMY", "in": 0.6},
                              {"kind": "unit", "type": "inf", "nation": "UK", "at": [2.75, 48.7], "label": "BEF", "in": r(s, "written off the British")},
                              arrow([[3.4, 49.5], [3.15, 49.1], [3.25, 48.85]], "GERI", at=0.0, dur=0.6)],
        colors=WEST, legend=LEG_W, rivers=["Marne", "Seine"])

    s = T("The military governor of Paris")
    sc(s, {"kind": "office", "desk": False, "fg": "officedesk"}, [
        AID("gal", "gallieni", 980, 1000, 1.55, "pointDown", "determined", turn=-0.2, keys=mv((r(s, "saw the opening"), {"pose": "point", "expr": "smug"}))),
        NC("General Joseph Gallieni", "Military Governor of Paris", at=0.4),
        {**PROP("paper", 900, 872, 0.7), "rotate": 80},
    ], [SHOT(0, "gal", "medium", frameX=0.1), SHOT(r(s, "saw the opening"), "gal", "close", frameX=-0.12)])
    s = T("Joffre, who for all his mistakes")
    sc(s, {"kind": "conference", "desk": False, "fg": "officedesk"}, [
        AID("joffre", "joffre", 960, 1000, 1.6, "drink", "smug", turn=0.2, keys=mv((r(s, "eight hours' sleep") if False else 4.0, {"pose": "rub", "expr": "happy"}), (r(s, "ordered the counterattack"), {"pose": "point", "expr": "determined"}))),
        {**PROP("candle", 760, 830, 1.2), "front": True},
    ], [SHOT(0, "joffre", "medium", push=0.04), SHOT(4.0, "joffre", "close", frameX=-0.14), SHOT(r(s, "ordered the counterattack"), "joffre", "mediumclose", frameX=0.12)], date="4 SEPTEMBER 1914")
    s = T("He had been shifting troops by rail")
    sc(s, {"kind": "railway", "drift": 0}, [
        {"id": "train", "kind": "vehicle", "type": "train", "nation": "FRA", "x": 2700, "y": 930, "scale": 2.2, "flip": True, "keys": mv((5.0, {"x": 900}))},
    ], [SHOT(0, None, "wide", zoom=1.0, panX=-120)])
    s = T("When the battle began")
    sc(s, {"kind": "workshop"}, [{"kind": "bars", "title": "AT THE MARNE", "x": 1020, "y": 400, "width": 760, "max": 1000000, "unit": "", "items": [
        {"label": "French", "value": 980000, "nation": "FRA", "in": r(s, "nine hundred and eighty")},
        {"label": "British", "value": 100000, "nation": "UK", "in": r(s, "a hundred thousand British")},
        {"label": "German", "value": 750000, "nation": "GERI", "in": r(s, "seven hundred and fifty")}]}], [SHOT(0, None, None, zoom=1.0, push=0.05)])

    s = T("For a week")
    battlefield(s, "ww1_french_1914", n=5, direction=1, run=True, shells=((0.6, 1300, 760), (2.0, 900, 840), (3.4, 1600, 800)), close=(2.8, "m1"), dur=8.0,
                date="6-9 SEPTEMBER 1914", place="THE MARNE")
    s = T("By the 9th of September")
    MAP(s, [3.5, 49.2], 3.6, [city("Paris"), city("Soissons", at=0.5), front([[2.7, 49.1], [3.2, 48.95], [3.8, 48.85], [4.6, 48.8]], "GERI",
                                                                        path2=[[2.9, 49.5], [3.3, 49.4], [3.9, 49.35], [4.6, 49.1]], morph_dur=4.0),
                              L("FALL BACK TO THE AISNE", 960, 170, "tag", 40, at=r(s, "fall back"))],
        colors=WEST, legend=LEG_W, rivers=["Marne", "Aisne"])
    s = T("The estimated casualties")
    sc(s, {"kind": "workshop"}, [{"kind": "bars", "title": "CASUALTIES (ESTIMATES)", "x": 1020, "y": 400, "width": 760, "max": 300000, "unit": "", "items": [
        {"label": "French", "value": 250000, "nation": "FRA", "in": r(s, "two hundred and fifty")},
        {"label": "German", "value": 300000, "nation": "GERI", "in": r(s, "nearly three hundred")},
        {"label": "British", "value": 13000, "nation": "UK", "in": r(s, "almost thirteen")}]}], [SHOT(0, None, None, zoom=1.0, push=0.05)])

    s = T("Moltke's health broke down")
    sc(s, {"kind": "warroom", "fg": "officedesk"}, [
        AID("m", "moltke", 960, 1000, 1.6, "head", "sad", turn=0.1, keys=mv((r(s, "he was replaced"), {"pose": "facepalm"}))),
    ], [SHOT(0, "m", "medium"), SHOT(r(s, "he was replaced") - 0.3, "m", "close", frameX=0.1)], date="14 SEPTEMBER 1914")
    s = T("And there's a famous line")
    sc(s, {"kind": "cabinet", "desk": False}, [
        AID("m", "moltke", 760, 1000, 1.55, "idle", "sad", turn=0.5), AID("k", "kaiser_wilhelm", 1220, 1000, 1.55, "idle", "neutral", turn=-0.5),
    ], [SHOT(0, ["m", "k"], "full", push=0.04)], tint="sepia")
    s = T("Your Majesty, we have lost the war")
    quote(s, "moltke", "\"Your Majesty, we have lost the war.\"", set_="cabinet", pose="talk", expr="sad", tag="REPORTED · UNPROVEN", tint="sepia")
    s = T("Sir, so he said it")
    duo(s, [(0.0, "aide", "explain", "happy"), (r(s, "Did he?"), "host", "chin!", "smug")])
    s = T("Here's the paperwork. Nobody")
    doc(s, "note", "THE SOURCE?", ["No document", "No witness who wrote it down", "Repeated — never proven"], stamp="UNPROVEN", speed=40)
    s = T("Keep the sentence in your pocket")
    host(s, "show", "smug", holds="paper", keys=mv((1.4, {"pose": "pockets", "holds": ""})), second=(1.3, "close", "host"))

    s = T("What we do know")
    MAP(s, [4.0, 49.8], 9, [arrow([[3.2, 49.6], [2.9, 50.3], [2.7, 51.0]], "FRA", at=r(s, "to the north") - 0.6, dur=2.0),
                            arrow([[3.6, 49.7], [3.3, 50.4], [3.0, 51.05]], "GERI", at=r(s, "to the north") - 0.3, dur=2.0),
                            front(WESTERN_FRONT, "#7a2a22", at=r(s, "From the North Sea") - 0.2), city("Paris")],
        colors=WEST, legend=LEG_W, date="AUTUMN 1914")
    s = T("The trenches had arrived")
    trench(s, "ww1_german", n=3, action="wait", expr="tired", close=1.6, date="LATE 1914")
    s = T("So, did the sand run out here?")
    glass(s, level=0.75, to=1.0, dur_fall=4.0, plaque="SHORT WAR", cut_host=r(s, "There would be no"))
    s = T("Germany was now stuck")
    MAP(s, [14.0, 51.0], 34, [front(WESTERN_FRONT, "#7a2a22"), front(EAST_FRONT, "#7a2a22", at=0.6), city("Berlin"),
                              L("TWO FRONTS · LONG WAR", 960, 160, "tag", 42, at=1.2)], colors=EUROPE, legend=LEG_CP)
    s = T("But it still held almost all of Belgium")
    MAP(s, [4.0, 49.8], 9, [front(WESTERN_FRONT, "#7a2a22"), city("Brussels"), city("Paris"),
                            {"kind": "region", "polygon": [[2.6, 51.4], [2.75, 51.13], [2.88, 50.85], [2.8, 50.35], [2.95, 49.65], [3.3, 49.42], [4.0, 49.3], [5.38, 49.22], [6.0, 49.5], [6.1, 50.2], [6.0, 51.0], [5.0, 51.5], [3.5, 51.45]],
                             "color": "GERI", "fillOpacity": 0.3, "in": 0.6},
                            L("NOBODY HAD BEATEN ITS ARMY", 960, 160, "tag", 40, at=r(s, "nobody had beaten"))],
        colors=WEST, legend=LEG_W)
    s = T("Small glass, empty")
    glass(s, level=1.0, flip_at=r(s, "I'm turning over") + 0.2, stamp="NOT YET", stamp_at=r(s, "Not yet.") + 0.15, plaque="1914")
