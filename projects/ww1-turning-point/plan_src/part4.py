"""Armistice, the stab-in-the-back myth, the verdict, the close. 26:44 - 32:23"""
from lib import *  # noqa: F401,F403
from lib import sc, host, duo, glass, hq, report, march_col, trench, battlefield, fleet, doc, quote, MAP, city, arrow, front, PL, \
    EUROPE, WEST, LEG_CP, LEG_W, HINDENBURG, NOV_1918, mv  # noqa: E402


def r(start, phrase):
    return round(peek(phrase) - start, 2)


def build():
    s = T("In early October, Germany's government")
    doc(s, "telegram", "BERLIN TO WASHINGTON · OCTOBER 1918", ["REQUEST: PEACE TALKS", "ON THE BASIS OF THE FOURTEEN POINTS"], speed=40, date="OCTOBER 1918")
    s = T("Ludendorff was forced out")
    sc(s, {"kind": "corridor"}, [AID("lud", "ludendorff", 960, 1150, None, "idle", "sad", view="back", keys=mv((3.0, {"y": 700, "ease": "linear"})))],
       [SHOT(0, None, None, zoom=1.0, push=0.03)], world={"horizon": 500, "y": 900, "scale": 1.3}, date="26 OCTOBER 1918")
    s = T("Sailors mutinied")
    sc(s, {"kind": "harbor", "drift": 0}, [
        {"kind": "vehicle", "type": "battleship", "nation": "GERI", "x": 1200, "y": 640, "scale": 0.5},
        *[AID(f"s{i}", "ww1_sailor_de", 300 + i * 300, 1000 - (i % 2) * 30, 1.35, ["fist", "cheer", "shout" if False else "raise", "fist"][i], "angry", keys=mv((0.6 + i * 0.4, {"pose": "cheer"}))) for i in range(4)],
        {"kind": "flag", "nation": "NEUTRAL", "out": 0, "x": 1650, "y": 420, "w": 160, "h": 100}],
       [SHOT(0, ["s0", "s3"], "full"), SHOT(2.0, "s1", "close", frameX=0.1)], place="KIEL, NOVEMBER 1918")
    s = T("on the 9th of November the Kaiser's abdication")
    doc(s, "newspaper", "BERLIN · 9 NOVEMBER 1918", ["THE KAISER ABDICATES"], speed=30)
    s = T("Two days later, at five in the morning")
    sc(s, {"kind": "train_interior", "time": "night", "fg": "officedesk"}, [
        AID("foch", "foch", 640, 1000, 1.5, "idle", "determined", turn=0.5, keys=mv((2.4, {"pose": "cross"}))),
        AID("ger", "civilian_man", 1260, 1000, 1.5, "write", "sad", holds="pen", turn=-0.4, look_={"outfit": "suit", "color": "#3b3a3f", "facial": "walrus", "age": 0.6}),
        {**PROP("paper", 1200, 872, 0.7), "rotate": 80}],
       [SHOT(0, ["foch", "ger"], "medium"), SHOT(2.0, "ger", "close", frameX=0.12), SHOT(4.0, None, None, zoom=2.0, x=1200, y=820)],
       clock="5:00 AM", date="11 NOVEMBER 1918", place="COMPIÈGNE", letterbox="DRAMATISED — COMPIÈGNE, 11 NOVEMBER 1918")
    s = T("It came into force at eleven o'clock")
    trench(s, "ww1_british", n=3, action="wait", expr="tired", close=None)
    SCENES[-1].pop("date", None)
    SCENES[-1]["clock"] = "11:00 AM"
    s = T("Two thousand seven hundred and thirty-eight")
    sc(s, {"kind": "memorial", "drift": 0}, [{**PROP("candle", 960, 700, 2.0)}, CNT(0, 2738, 960, 300, at=0.3, suffix=" DIED THAT LAST MORNING", size=60, dur=1.6, color="#efe6d2")],
       [SHOT(0, None, None, zoom=1.0, push=0.06)], tint="grey", ambience=None)

    # ================================================================ THE MYTH
    s = T("Which brings us to the last myth")
    host(s, "explain", "neutral", label="THE LAST MYTH", keys=mv((2.0, {"pose": "chin"})), chapter="The Last Myth")
    s = T("Within months of the armistice")
    hq(s, [("o1", "bauer", "talk", "angry", mv((2.0, {"pose": "fist"}))), ("o2", "clerk_de", "idle", "smug", None)], set_="office", talk=0, desk=False,
       cuts=[(r(s, "Colonel Max Bauer"), "o1", "mediumclose")], date="1919")
    SCENES[-1]["elements"].append(NC("Colonel Max Bauer", "adviser to Ludendorff", at=r(s, "Colonel Max Bauer")))
    s = T("The war was lost only and exclusively")
    doc(s, "book", "BAUER · SPRING 1919", ["\"The war was lost only and exclusively", "through the failure of the homeland.\""], speed=36)
    s = T("The army, so the story went")
    sc(s, {"kind": "street", "drift": 0, "weather": "rain"}, [
        AID("v", "ww1_german", 760, 1000, 1.55, "idle", "sad", turn=0.4, keys=mv((2.0, {"pose": "head"}))),
        AID("p", "civilian_man", 1240, 1000, 1.55, "talk", "angry", talk=True, turn=-0.5, look_={"outfit": "suit", "color": "#3b3a3f"}, keys=mv((1.6, {"pose": "point"})))],
       [SHOT(0, ["v", "p"], "medium"), SHOT(r(s, "Ludendorff became"), "p", "close", frameX=0.12)], tint="sepia", date="1920s")
    SCENES[-1]["elements"].append(L("\"STABBED IN THE BACK\"", 960, 160, "tag", 40, at=0.8, hud=True))
    s = T("Later, the Nazis made it part")
    doc(s, "book", "1930s", ["THE MYTH BECOMES", "OFFICIAL HISTORY"], stamp="MYTH", speed=30, tint="sepia")
    s = T("Sir, is that one true?")
    duo(s, [(0.0, "aide", "explain", "worried"), (r(s, "Look at the timetable"), "host", "talk", "neutral"), (r(s, "Who asked for the armistice first"), "host", "point!", "determined")])
    s = T("Here's the paperwork. On the 29th of September")
    sc(s, {"kind": "workshop"}, [{"kind": "timeline", "x": 960, "y": 560, "width": 1400, "items": [
        {"sub": "29 SEPT", "label": "Army asks for an armistice", "at": 0.15, "color": "GERI", "in": 0.4},
        {"sub": "3 NOV", "label": "Revolt begins (Kiel)", "at": 0.55, "color": "#7a2a22", "in": r(s, "before the revolution began")},
        {"sub": "11 NOV", "label": "Armistice", "at": 0.85, "color": "#2f6b3a", "in": r(s, "before the revolution began") + 0.6}]}],
       [SHOT(0, None, None, zoom=1.0, push=0.05)])
    s = T("To be fair to the myth's strongest version")
    MAP(s, [4.6, 50.0], 7.0, [front(HINDENBURG, "#5a5a52", path2=NOV_1918, morph_dur=6.0), city("Brussels"), city("Spa"),
                              L("RETREATING · NOT DESTROYED", 960, 160, "tag", 40, at=r(s, "had not been destroyed"))], colors=WEST, legend=LEG_W, date="NOVEMBER 1918")
    s = T("But an army that is retreating every week")
    battlefield(s, "ww1_german", n=4, direction=-1, surrender=3, dur=6.0, close=(2.0, "g1"))
    s = T("That's why Foch's terms were so hard")
    doc(s, "order", "ARMISTICE TERMS", ["Evacuate everything west of the Rhine", "Allied troops on the Rhine", "Hand over warships, aircraft, weapons"], speed=46)
    s = T("Historians accept that hunger and unrest")
    host(s, "explain", "neutral", keys=mv((r(s, "They reject the myth"), {"pose": "stop", "expr": "determined"}), (r(s, "It was a weapon"), {"pose": "point"})),
         second=(r(s, "They reject the myth"), "close", "host"))
    SCENES[-1]["elements"].append({**ST("MYTH", 1500, 300, r(s, "They reject the myth") + 0.3, size=90), "hud": True})

    # ================================================================ THE VERDICT
    s = T("So, let's read the timetable back")
    glass(s, level=1.0, plaque="1918", chapter="The Verdict", cut_host=0.2)
    s = T("Marne, 1914. The short war, finished")
    sc(s, {"kind": "workshop"}, [{"kind": "timeline", "x": 960, "y": 560, "width": 1440, "items": [
        {"sub": "1914", "label": "Marne", "at": 0.06, "color": "#2f6b3a", "in": 0.2},
        {"sub": "1914-18", "label": "Blockade", "at": 0.22, "color": "#2f6b3a", "in": r(s, "Blockade")},
        {"sub": "1916", "label": "Verdun, Somme", "at": 0.38, "color": "#2f6b3a", "in": r(s, "Verdun and the Somme")},
        {"sub": "1916", "label": "Jutland", "at": 0.53, "color": "#2f6b3a", "in": r(s, "Jutland")},
        {"sub": "1918", "label": "Brest: turned back", "at": 0.68, "color": "GERI", "in": r(s, "Brest-Litovsk")},
        {"sub": "18 JULY", "label": "Sand out", "at": 0.81, "color": "#7a2a22", "in": r(s, "The 18th of July")},
        {"sub": "8 AUG", "label": "Amiens", "at": 0.94, "color": "#7a2a22", "in": r(s, "And Amiens")}]}],
       [SHOT(0, None, None, zoom=1.0, push=0.04)])
    s = T("And one stamp is still in the stationmaster's pocket")
    glass(s, level=1.0, plaque="PLESS", stamp="PLESS", stamp_at=r(s, "Pless") + 0.3, cut_host=0.3)
    s = T("Here's our verdict")
    host(s, "explain", "determined", label="THE VERDICT", keys=mv((r(s, "Pless decided"), {"pose": "point"})), second=(r(s, "Pless decided"), "close", "host"))
    s = T("On the 9th of January, 1917, Germany's leaders")
    sc(s, {"kind": "conference", "desk": False, "fg": "officedesk"}, [
        AID("k", "kaiser_wilhelm", 960, 1000, 1.55, "write", "determined", holds="pen"), AID("hz", "holtzendorff", 1360, 1000, 1.5, "present", "smug", turn=-0.5),
        AID("hin", "hindenburg", 560, 1000, 1.5, "idle", "determined", turn=0.5)],
       [SHOT(0, ["hin", "k", "hz"], "medium"), SHOT(r(s, "in exchange for a promise"), "hz", "close", frameX=0.12)], tint="sepia")
    s = T("Britain didn't starve")
    fleet(s, ships=(("cargo", "USA", 500, 700, 1), ("cargo", "USA", 1100, 660, 1), ("destroyer", "USA", 1600, 630, 1)), dur=6)
    s = T("From that day on, every German chance")
    glass(s, level=0.3, to=1.0, dur_fall=10.0, plaque="PLESS", cut_host=r(s, "Brest-Litovsk turned the glass"))
    s = T("And Moltke's sentence from 1914")
    quote(s, "moltke", "\"Your Majesty, we have lost the war.\"", set_="cabinet", pose="talk", expr="sad", tag="1914 · WRONG", tint="sepia")
    s = T("Germany had more than two years of chances left")
    host(s, "count", "neutral", keys=mv((r(s, "By the evening"), {"pose": "explain"})))
    s = T("By the evening of the 9th of January, 1917")
    sc(s, {"kind": "conference", "desk": False, "time": "night"}, [AID("k", "kaiser_wilhelm", 960, 1000, 1.6, "idle", "neutral", turn=0.3, keys=mv((3.0, {"expr": "sad", "pose": "chin"}))),
                                                                  {**PROP("candle", 600, 820, 1.4)}],
       [SHOT(0, "k", "medium"), SHOT(3.0, "k", "close", frameX=-0.12)], tint="sepia", date="9 JANUARY 1917, EVENING")
    s = T("Now, to be fair, historians")
    host(s, "shrug", "neutral", keys=mv((r(s, "Many still point to the Marne"), {"pose": "count"})))
    s = T("Many still point to the Marne")
    battlefield(s, "ww1_french_1914", n=4, direction=1, run=True, dur=6.0, close=(2.0, "m1"), date="1914", tint="sepia")
    s = T("Others put the weight on the blockade")
    kitchen(s)
    s = T("And others say the war was decided")
    battlefield(s, "ww1_australian", n=3, tanks=("markiv", 1), dur=7.0, close=(2.6, "t0"))
    s = T("The strongest case against our stamp")
    MAP(s, [2.9, 49.4], 5.2, [front(SPRING_1918, "#5a5a52"), city("Paris", tag=True), city("Amiens", tag=False),
                              {"kind": "line", "path": [PL["Château-Thierry"], PL["Paris"]], "color": "#7a2a22", "dashed": True, "in": 0.6, "enter": "draw", "dur": 1.0, "width": 5},
                              L("56 KM", 1020, 520, "red", 44, at=1.0)], colors=WEST, legend=LEG_W)
    s = T("It's a fair question")
    host(s, "chin", "neutral", keys=mv((1.4, {"pose": "explain"})))
    s = T("They never had a clear goal")
    MAP(s, [2.4, 50.0], 4.5, [front(SPRING_1918, "#5a5a52"), city("Amiens", tag=True),
                              *[{"kind": "unit", "type": "inf", "nation": n, "at": a, "in": 0.6 + i * 0.3} for i, (n, a) in enumerate([("UK", [2.15, 49.95]), ("FRA", [2.25, 49.8]), ("UK", [2.05, 49.85]), ("FRA", [2.35, 49.7])])],
                              L("RESERVES PILE UP", 960, 160, "tag", 40, at=r(s, "piled up their reserves"))], colors=WEST, legend=LEG_W)
    s = T("And by the summer, every week")
    sc(s, {"kind": "dock", "drift": 0}, [
        {"kind": "vehicle", "type": "cargo", "nation": "USA", "x": 1300, "y": 640, "scale": 0.75},
        *[{**AID(f"u{i}", "ww1_american", 1050 - i * 230, 980, 1.35, "shoulder", "determined", holds="rifle", keys=mv((7.0, {"x": 1050 - i * 230 - 600, "ease": "linear"}))), "flip": True} for i in range(5)],
        CNT(0, 70000, 1450, 230, at=r(s, "as many as seventy thousand"), suffix=" A WEEK", size=64, dur=1.2, hud=True)],
       [SHOT(0, None, None, zoom=1.0, push=0.03), SHOT(3.0, "u1", "mediumclose", track=True, frameX=0.1)])
    s = T("All of these historians are describing")
    glass(s, level=0.5, to=0.6, dur_fall=4.0, plaque="GERMANY", cut_host=1.6)
    s = T("The price of that clock")
    sc(s, {"kind": "memorial", "drift": 0}, [*[{**PROP("cross", 300 + i * 220, 760 + (i % 3) * 70, 0.8 + (i % 3) * 0.2)} for i in range(7)],
                                            CNT(0, 9, 960, 220, at=r(s, "between nine and eleven million"), suffix="-11 MILLION SOLDIERS", size=60, dur=1.0),
                                            CNT(0, 15, 960, 330, at=r(s, "fifteen to twenty-two million"), suffix="-22 MILLION IN ALL", size=48, dur=1.0, color="#c8352b")],
       [SHOT(0, None, None, zoom=1.0, push=0.05)], tint="grey", ambience="wind")
    s = T("Millions more came home wounded")
    sc(s, {"kind": "station", "drift": 0}, [AID("w", "ww1_british", 960, 1000, 1.55, "idle", "sad", turn=0.2, keys=mv((2.0, {"pose": "head"})))],
       [SHOT(0, "w", "full"), SHOT(1.6, "w", "close", frameX=0.1)], tint="grey")
    s = T("That's our reading of the hourglass")
    host(s, "explain", "neutral", aide=True, keys=mv((r(s, "Tell us in the comments"), {"pose": "point"}), (r(s, "subscribe"), {"pose": "thumbsup", "expr": "smug"})),
         aide_keys=mv((r(s, "subscribe") + 0.3, {"pose": "cheer", "expr": "happy"})), second=(r(s, "Would you stamp"), "close", "host"))
    s = T("It's the only timetable")
    duo(s, [(0.0, "host", "show!", "smug"), (1.4, "aide", "laugh", "laugh")]) if False else host(s, "show", "smug", aide=True, aide_keys=mv((0.8, {"pose": "rub", "expr": "laugh"})))
    s = T("The war that began with railway timetables")
    sc(s, {"kind": "countryside", "time": "dawn", "drift": 0, "weather": None}, [
        {"id": "car", "kind": "vehicle", "type": "traincar", "nation": "FRA", "x": 960, "y": 900, "scale": 1.6}],
       [SHOT(0, None, "wide", zoom=1.0, push=0.05), SHOT(r(s, "Germany had spent four years"), "car", "full", push=0.04)], place="COMPIÈGNE", tint="warm")
    s = T("In the end, it never caught a single train")
    glass(s, level=1.0, plaque="GERMANY", cut_host=0.4)
    s = T("Last train in")
    host(s, "salute", "smug", holds="stopwatch", keys=mv((r(s, "Stamp the log"), {"pose": "slam"})))
    SCENES[-1]["elements"].append(ST("END OF THE LINE", 1400, 300, r(s, "Stamp the log") + 0.3, size=70))
