from lib import *

US, UK, GE = "USA", "UK", "GERI"
STUDY = {"kind": "study", "desk": False, "portrait": False, "shelf": True, "lamp": True, "fg": "plant", "fgSide": "left"}
NIGHT_POLDER = {"kind": "polder", "time": "night"}


def tanks(x0, x1, y, s, t1, n=4, gap=260, nation=UK, ease="out", **kw):
    return [V("tank", x0 - i * gap, y, s, nation, moving=True, keys=K((t1, {"x": x1 - i * gap, "ease": ease})), **kw) for i in range(n)]


def build():
    # =============== CH1 THE LAST FOUR TANKS ===============
    scene(0.0, {"kind": "archbridge", "time": "dusk"}, [
        *tanks(-200, 1500, 528, 0.2, 5.6, n=4, gap=120),
        L("NIJMEGEN ROAD BRIDGE", 960, 640, "map", 34, at=1.2),
    ], date="20 SEPTEMBER 1944", clock="7:10 PM", camera=[{"t": 0, "zoom": 1.0}, {"t": 5.7, "zoom": 1.08, "x": 1000, "y": 520}],
        chapter="The Last Four Tanks", beat="A little after seven on 20 Sept 1944, four British tanks cross the Nijmegen road bridge")
    scene(5.68, {"kind": "archbridge", "time": "dusk"}, [
        V("tank", -300, 960, 1.15, UK, moving=True, keys=K((5.5, {"x": 1500}))),
        A("guards_tanker", 1650, 930, 1.3, "salute", "determined"),
    ], place="NIJMEGEN · THE NETHERLANDS", sfx=[{"t": 0, "id": "tank_engine", "dur": 5.5}], beat="tanks roll north across the bridge")
    scene(11.18, {"kind": "river", "bridges": True}, [
        *[V("assaultboat", 300 + i * 520, 860, 0.85, keys=K((4.7, {"y": 620, "scale": 0.55}))) for i in range(3)],
        FX("splash", 600, 700, **{"in": 1.0}), FX("splash", 1250, 650, **{"in": 2.2}), FX("splash", 900, 740, **{"in": 3.4}),
        FX("tracer", 1200, 470, dir=200, **{"in": 0.6}),
        L("A FEW HOURS EARLIER", 960, 120, "dark", 40, at=0.2),
    ], clock="3:00 PM", beat="earlier: American paratroopers rowing across the Waal in canvas boats")
    scene(15.9, {"kind": "river"}, [
        V("assaultboat", 700, 780, 1.6, keys=K((4.8, {"x": 980, "y": 720}))),
        FX("splash", 500, 700, **{"in": 0.4}), FX("splash", 1400, 760, **{"in": 1.4}), FX("splash", 1100, 640, **{"in": 2.8}),
        FX("tracer", 1500, 430, dir=210, **{"in": 0.2}), FX("tracer", 900, 430, dir=230, **{"in": 1.8}),
        L("RIVER WAAL · IN BROAD DAYLIGHT", 960, 110, "tag", 42, at=0.6),
    ], camera=[{"t": 0, "zoom": 1.0, "shake": 2}, {"t": 4.8, "zoom": 1.1, "shake": 2}], sfx=[{"t": 0.5, "id": "machinegun", "dur": 3.5, "vol": -6}], beat="under fire in broad daylight")
    scene(20.7, {"kind": "archbridge", "time": "dusk", "burning": True}, [
        A("british_para", 380, 920, 1.35, "hold", "determined", holds="rifle"),
        A("frost", 1350, 920, 1.5, "binoculars", "neutral", keys=K((5.9, {"pose": "idle", "expr": "tired"}))),
        A("british_para_helmet", 1700, 940, 1.3, "idle", "tired"),
        L("ARNHEM · 11 KM NORTH", 960, 110, "dark", 40, at=0.3),
    ], camera=[{"t": 0, "zoom": 1.0}, {"t": 9, "zoom": 1.12, "x": 1100}], beat="11 km up the road at Arnhem a few hundred British paratroopers still holding")
    scene(29.94, {"kind": "city", "ruined": True, "time": "night"}, [
        FX("fire", 300, 700), FX("smoke", 320, 600),
        A("frost", 1050, 920, 1.6, "pointL", "worried", talk=True),
        CNT(0, 3, 1500, 300, 0.3, suffix=" DAYS", size=100, dur=1.0),
        L("WAITING FOR THE TANKS", 960, 110, "tag", 44, at=2.4),
    ], beat="holding for three days, waiting for exactly these tanks")
    scene(35.22, NIGHT_POLDER, [
        *tanks(-300, 1400, 600, 0.42, 3.0, n=4, gap=200),
        L("LENT", 1750, 520, "tag", 52, at=0.3),
        FX("question", 1300, 420, **{"in": 3.4}),
    ], camera=[{"t": 0, "zoom": 1.0}, {"t": 4.9, "zoom": 1.15, "x": 1150, "y": 560}], beat="the tanks stopped in the next village, Lent")
    scene(40.14, {"kind": "archbridge", "time": "night", "burning": True}, [
        *[V("halftrack", 2100 + i * 220, 528, 0.22, GE, flip=True, moving=True, keys=K((2.1, {"x": 900 + i * 220}))) for i in range(3)],
        ST("BRIDGE LOST", 960, 820, 0.8, size=100),
    ], beat="that night the men at Arnhem lost their bridge")
    scene(42.24, {"kind": "office", "desk": False, "portrait": False, "shelf": True, "time": "day"}, [
        A("harmel_old", 1150, 900, 1.5, "idle", "neutral", seated=False),
        A("reporter", 600, 900, 1.4, "hold", "neutral", holds="microphone", talk=True),
        L("DECADES LATER", 960, 110, "dark", 40, at=0.2),
        L("THE GERMAN GENERAL FACING THOSE TANKS", 1150, 320, "plain", 36, at=1.5),
    ], tint="sepia", beat="decades later the German general who had faced the four tanks was asked")
    scene(48.66, {"kind": "office", "desk": False, "portrait": False, "shelf": True}, [
        A("harmel_old", 1100, 900, 1.6, "explain", "neutral", talk=True, keys=K((3.2, {"pose": "shrug"}))),
        L("\"THE FOUR TANKS MADE A MISTAKE\nWHEN THEY STAYED IN LENT.\"", 960, 120, "plain", 46, at=0.2),
        L("\"IF THEY HAD CARRIED ON, IT WOULD\nHAVE BEEN ALL OVER FOR US.\"", 960, 260, "plain", 46, at=3.1, color="red"),
    ], tint="sepia", camera=[{"t": 0, "zoom": 1.0}, {"t": 7, "zoom": 1.15, "x": 1060}], beat="his quote: it would have been all over for us")
    scene(55.66, STUDY, [
        A("host", 980, 900, 1.65, "chin", "smug", headMove="tilt"),
        NC("The Dispatcher", "your guide on this road", at=0.2),
    ], beat="HOST: that's an old man remembering")
    MAP(57.8, [5.88, 51.91], 0.8, [
        *rivers("waal", "rhine"), *towns("Nijmegen", "Lent", "Elst", "Arnhem", at=0.1),
        {"kind": "unit", "type": "inf", "nation": "GER", "at": [5.86, 51.895], "in": 2.8, "size": 0.7},
        {"kind": "unit", "type": "inf", "nation": "GER", "at": [5.885, 51.94], "in": 3.2, "size": 0.7},
        {"kind": "ring", "at": [5.865, 51.915], "km": 4, "in": 4.5, "color": "red", "enter": "grow"},
        L("HIS OWN ARTILLERY MAP", 960, 110, "tag", 44, at=0.3, hud=True),
        L("A FEW PICKETS\nWITH RIFLES", 1500, 500, "red", 40, at=5.4, hud=True),
    ], style="sepia", tint="sepia", camera=[{"t": 0, "zoom": 1.0}, {"t": 9.8, "zoom": 1.15}], beat="his artillery map shows almost nothing between Lent and Arnhem")
    scene(67.6, {"kind": "cabinet"}, [
        A("montgomery", 360, 900, 1.35, "pointUp", "angry"),
        A("brereton", 760, 900, 1.35, "point", "angry"),
        A("pinto", 1160, 900, 1.35, "pointL", "smug"),
        A("browning", 1560, 900, 1.35, "cross", "smug"),
        L("EVERYBODY HAD AN EXPLANATION", 960, 110, "tag", 44, at=0.5),
    ], beat="everybody who survived had an explanation")
    scene(73.08, {"kind": "field", "weather": "rain", "time": "storm", "road": False, "houses": False}, [
        A("montgomery", 960, 900, 1.6, "pointUp", "angry", talk=True),
        NC("Field Marshal Bernard Montgomery", "21st Army Group", at=0.2),
        L("THE WEATHER", 1450, 300, "red", 54, at=0.6),
    ], beat="Montgomery blamed the weather")
    scene(75.06, {"kind": "polder"}, [
        V("tank", 1300, 590, 0.38, UK, moving=True, keys=K((6.2, {"x": 1360}))),
        A("brereton", 600, 900, 1.6, "point", "angry", talk=True, keys=K((3.5, {"pose": "hips"}))),
        NC("Lt Gen Lewis Brereton", "First Allied Airborne Army", at=0.4),
        L("THE SLOW BRITISH TANKS", 1350, 300, "red", 48, at=4.4),
    ], beat="Brereton blamed the slow British tanks")
    scene(81.3, {"kind": "dark"}, [
        A("lindemans", 560, 900, 1.6, "behind", "smug"),
        L("A TRAITOR?", 560, 220, "red", 54, at=0.4),
        PROP("folder", 1350, 620, 1.6, at=2.4, text="RECON PHOTOS"),
        L("PHOTOS NOBODY\nWANTED TO SEE", 1350, 260, "tag", 46, at=2.8),
    ], beat="others blamed a traitor, or photographs nobody wanted to look at")
    scene(86.32, {"kind": "city", "ruined": True}, [
        {"kind": "crowd", "who": ["ss_soldier", "german_soldier"], "count": 7, "spacing": 200, "x": 960, "y": 920, "scale": 1.05, "pose": "idle", "expr": "determined", "in": 1.0, "enter": "rise"},
        ST("FINISHED", 960, 300, 0.2, size=120),
        {"kind": "shape", "shape": "cross", "x": 960, "y": 300, "in": 2.6, "scale": 2.4},
    ], beat="a German army that was supposed to be finished and somehow wasn't")
    scene(90.72, {"kind": "podium", "flag": "UK"}, [
        A("montgomery", 960, 900, 1.6, "show", "smug", holds="sign", holdsText="90%", holdsScale=0.9, talk=True),
        CNT(0, 90, 1550, 320, 1.4, suffix="% SUCCESSFUL", size=90, dur=2.2),
    ], beat="Montgomery called the operation 90% successful")

    # =============== CH2 ONE ROAD, FIVE BRIDGES ===============
    scene(96.68, STUDY, [
        A("host", 300, 900, 1.6, "idle", "neutral", keys=K((1.8, {"x": 800}), (2.0, {"pose": "present"}))),
        HEAD("WAS MARKET GARDEN COMPLETELY AVOIDABLE?", 1060, 220, 70, at=2.3, accent="COMPLETELY"),
    ], chapter="One Road, Five Bridges", sfx=[{"t": 0.1, "id": "footsteps", "dur": 1.7}], beat="HOST: here's tonight's question")
    MAP(101.54, [4.0, 50.6], 9.5, [
        {"kind": "arrow", "path": [[-0.3, 49.2], [2.3, 49.9], [4.3, 50.8], [5.6, 51.6]], "color": "UK", "in": 0.2, "dur": 2.0},
        L("THE WAR IN THE WEST", 600, 300, "tag", 40, at=0.4, hud=True),
        L("THE ADVANCE INTO HOLLAND", 1350, 300, "tag", 40, at=1.6, hud=True),
        {"kind": "shape", "shape": "cross", "x": 600, "y": 330, "in": 1.2, "scale": 1.2, "hud": True},
        {"kind": "shape", "shape": "cross", "x": 1350, "y": 330, "in": 2.6, "scale": 1.2, "hud": True},
    ], beat="not the war in the West, not the advance into Holland")
    scene(104.98, {"kind": "archbridge", "time": "dusk", "burning": True, "label": "Arnhem"}, [
        HEAD("THE DEFEAT AT THE LAST BRIDGE", 960, 900, 84, at=0.4, accent="LAST"),
    ], camera=[{"t": 0, "zoom": 1.15, "y": 460}, {"t": 2.6, "zoom": 1.0}], beat="the defeat at the last bridge")
    ROAD(107.6, -0.12, -0.08, move=(0.2, 4.0), extra=[
        A("aide", 1350, 1010, 1.25, "hold", "worried", holds="radio", talk=True, keys=K((3.2, {"talk": False}))),
        A("host", 1700, 1010, 1.25, "idle", "neutral", keys=K((3.2, {"pose": "explain", "expr": "smug", "talk": True}))),
        NC("The Aide", "signaller, 1st Airborne", at=0.4, out=3.0),
    ], beat="AIDE: Sir, it's one road. How many ways can you get lost? HOST: on this road?")
    ROAD(111.82, -0.08, 0.10, move=(0.2, 5.2), show_unknown=True, extra=[
        HEAD("5 BRIDGES · 2 ARMIES · 1 ROAD", 960, 170, 80, at=2.0, accent="1 ROAD"),
    ], beat="let's count: every turn-off gets assigned; five bridges, two armies, one road")
    scene(117.1, STUDY, [
        A("host", 1450, 900, 1.6, "pointL", "neutral", talk=True, keys=K((5.0, {"pose": "stop", "expr": "determined"}))),
        DOC("note", "THE RULES", ["EVERY EXIT GETS:", "1. A DATE", "2. A PLACE", "3. A PERSON WHO COULD TAKE IT", "HINDSIGHT DOESN'T COUNT"], x=700, y=520, w=900, h=640, at=0.6, size=44, speed=18),
    ], beat="rules: date, place, person; hindsight doesn't count")
    LEDGER(126.77, [], [], extra=[A("host", 1720, 1000, 1.2, "present", "neutral", talk=True)], beat="the Allies get a column, so do the Germans")
    scene(132.41, STUDY, [
        A("host", 960, 900, 1.7, "show", "neutral", holds="stopwatch", talk=True),
        L("THE PLAN RAN ON A TIMETABLE", 960, 110, "tag", 44, at=0.4),
    ], camera=[{"t": 0, "zoom": 1.0}, {"t": 5, "zoom": 1.2, "y": 480}], beat="the dispatcher keeps the clock")
    scene(137.78, {"kind": "paper"}, [
        DOC("order", "TIMETABLE — XXX CORPS", ["START: SUNDAY", "ARNHEM: DAY 2 TO 3"], x=960, y=520, w=1100, h=520, at=0.2, size=64, speed=22),
    ], beat="timetable says tanks reach Arnhem in two to three days")
    ROAD(140.84, 0.62, 0.66, move=(0.2, 5.5), extra=[
        A("host", 1700, 1010, 1.25, "idle", "smug", talk=True, keys=K((4.6, {"pose": "chin", "headMove": "tilt"}))),
        FX("question", 1180, 300, **{"in": 3.0}),
    ], beat="clock starts on a Sunday; one sign we won't paint at all")

    # =============== CH3 THE SUMMER THAT MADE IT LOOK EASY ===============
    scene(147.16, {"kind": "corridor", "doors": ["MAPS", "HQ"]}, [
        A("host", 300, 900, 1.5, "idle", "neutral", talk=True, keys=K((4.5, {"x": 1300}), (4.8, {"pose": "explain"}))),
    ], chapter="The Summer That Made It Look Easy", transition="dip", beat="start with the summer that made it look easy")
    scene(152.84, {"kind": "field", "road": True, "houses": True, "trees": "round"}, [
        V("truck", 1500, 900, 0.7, "GER", damaged=True, rotate=-6),
        FX("smoke", 1500, 780),
        {"kind": "crowd", "who": ["german_soldier", "german_soldier", "german_officer"], "count": 6, "spacing": 170, "x": 1700, "y": 920, "scale": 1.0, "expr": "tired", "walk": True, "dir": -1,
         "keys": K((4.6, {"x": 600}))},
    ], date="AUGUST 1944", place="FRANCE", beat="August 1944 the German army in France fell apart")
    MAP(157.44, [2.0, 49.9], 8.5, [
        {"kind": "pocket", "polygon": [[-0.6, 48.75], [0.1, 48.7], [0.2, 48.95], [-0.4, 49.05]], "in": 0.6, "color": "GER"},
        ML("FALAISE", [-0.2, 48.6], at=0.8),
        {"kind": "arrow", "path": [[-0.4, 49.1], [1.5, 49.4], [3.0, 50.2], [4.3, 50.85]], "color": "UK", "in": 2.0, "dur": 2.6},
        {"kind": "arrow", "path": [[0.0, 48.5], [2.3, 48.9], [4.4, 49.6], [5.6, 50.3]], "color": "USA", "in": 2.6, "dur": 2.6},
        L("FASTER THAN THEIR OWN MAPS", 960, 980, "tag", 44, at=5.0, hud=True),
    ], beat="breakout from Normandy, Falaise pocket, chase across France and Belgium")
    scene(166.28, {"kind": "field", "road": True, "houses": False}, [
        {"kind": "crowd", "who": ["german_soldier", "german_soldier", "ss_soldier"], "count": 7, "spacing": 170, "x": 900, "y": 920, "scale": 1.0, "pose": "surrender", "expr": "sad"},
        A("american_soldier", 1750, 930, 1.3, "hold", "determined", holds="rifle"),
        CNT(0, 200000, 960, 260, 1.2, prefix="~", size=110, dur=2.4),
        L("MISSING OR CAPTURED · JUNE–AUG 1944", 960, 380, "tag", 40, at=3.0),
    ], beat="nearly 200,000 missing or captured")
    scene(176.62, {"kind": "harbor"}, [
        *tanks(-200, 1100, 900, 0.75, 4.0, n=2, gap=420),
        {"kind": "crowd", "who": ["dutch_civilian", "dutch_woman", "civilian_man"], "count": 5, "spacing": 150, "x": 1620, "y": 940, "scale": 0.95, "pose": "cheer", "expr": "happy"},
        L("DOCKS ALMOST INTACT", 960, 140, "green", 46, at=5.0),
    ], date="4 SEPTEMBER 1944", place="ANTWERP", sfx=[{"t": 0.5, "id": "cheer", "dur": 3}], beat="British tanks roll into Antwerp, docks almost intact")
    scene(185.12, {"kind": "cabinet"}, [
        A("eisenhower", 600, 900, 1.4, "cheer", "happy"),
        A("bedell_smith", 1000, 900, 1.4, "talk2", "happy", talk=True),
        A("montgomery", 1400, 900, 1.4, "hips", "smug"),
        L("ALLIED HQ: SOMETHING CLOSE TO A FEVER", 960, 110, "tag", 42, at=0.5),
    ], beat="the mood was something close to a fever")
    scene(189.52, {"kind": "warroom"}, [
        A("shaef_officer", 380, 900, 1.45, "present", "happy", talk=True),
        {"kind": "bars", "title": "GERMAN DIVISIONS IN THE WEST", "x": 1300, "y": 380, "max": 50, "width": 620,
         "items": [{"label": "ON PAPER", "nation": "GERI", "value": 48, "in": 0.6}, {"label": "WORTH ~20 INF + 4 ARMD", "nation": "GERI", "value": 24, "in": 4.0}]},
    ], beat="SHAEF counted 48 divisions worth about 20 infantry and 4 armoured")
    MAP(200.96, [5.4, 52.1], 5.0, [
        L("NETHERLANDS", 960, 520, "map", 50, at=0.2, hud=True),
        CNT(0, 100, 960, 380, 1.0, suffix=" TANKS", prefix="50–", size=110, dur=1.6, hud=True),
        L("BRITISH AIRBORNE STAFF ESTIMATE", 960, 140, "tag", 42, at=0.4, hud=True),
    ], beat="British airborne staff: the whole Netherlands held no more than 50–100 tanks")
    scene(208.88, {"kind": "paper"}, [
        DOC("book", "1ST AIRBORNE DIVISION — AFTER-ACTION REPORT", ["WE ASSUMED:", "AN ENEMY STILL DISORGANIZED", "AFTER A LONG, HASTY RETREAT,", "SCATTERED IN SMALL GROUPS,", "NOT CAPABLE OF MUCH", "ORGANIZED RESISTANCE."], x=960, y=540, w=1300, h=760, at=0.3, size=48, speed=20),
    ], beat="the British airborne division admitted what it had assumed")
    scene(222.12, STUDY, [
        A("host", 960, 900, 1.7, "show", "worried", holds="barrel", holdsScale=0.5, talk=True),
        ST("FUEL", 1450, 360, 2.6, size=120),
    ], beat="one problem, the oldest one in war: fuel")
    scene(227.95, {"kind": "beach"}, [
        *[PROP("barrel", 200 + (i % 6) * 100, 880 - (i // 6) * 70, 0.45) for i in range(18)],
        V("truck", 1200, 900, 0.75, US, moving=True, keys=K((7.2, {"x": 1900}))),
        L("NORMANDY", 400, 140, "map", 48, at=0.2),
        L("HUNDREDS OF KM FROM THE FRONT", 1250, 300, "tag", 44, at=2.0),
        L("NOT ENOUGH TRUCKS", 1250, 400, "red", 44, at=4.6),
    ], beat="the petrol was in Normandy and there weren't enough trucks")
    MAP(235.3, [4.0, 51.38], 1.7, [
        *rivers("scheldt"),
        {"kind": "region", "polygon": [[3.4, 51.42], [4.1, 51.42], [4.1, 51.55], [3.4, 51.6]], "color": "GER", "in": 3.6},
        {"kind": "region", "polygon": [[3.4, 51.25], [4.0, 51.25], [4.0, 51.37], [3.4, 51.38]], "color": "GER", "in": 4.2},
        *towns("Antwerp", at=0.2),
        ML("DOCKS: ALLIED", [4.40, 51.17], style="green", at=1.6),
        ML("THE SCHELDT", [3.85, 51.395], at=2.6),
        L("GERMANS ON BOTH BANKS", 960, 980, "red", 46, at=5.0, hud=True),
    ], camera=[{"t": 0, "zoom": 1.0, "center": [4.25, 51.3]}, {"t": 6, "zoom": 1.0, "center": [3.95, 51.4]}], beat="the Scheldt estuary was still held by the Germans on both banks")
    scene(246.12, {"kind": "harbor"}, [
        V("jeep", 700, 900, 0.8, US), V("truck", 1150, 900, 0.7, US),
        A("host", 1650, 920, 1.4, "shrug", "smug", talk=True),
        L("A VERY LARGE CAR PARK", 900, 220, "tag", 52, at=0.8),
    ], beat="a port you can't sail into is a very large car park")
    scene(249.9, {"kind": "office", "flag": "UK", "portrait": False, "desk": False, "shelf": True}, [
        A("cunningham", 1000, 900, 1.6, "stop", "angry", talk=True, keys=K((5.0, {"pose": "explain"}))),
        NC("Admiral Sir Andrew Cunningham", "First Sea Lord", at=1.2),
        L("\"ABOUT AS MUCH USE\nAS TIMBUKTU\"", 960, 130, "plain", 54, at=6.6),
    ], beat="Cunningham warned Antwerp would be as much use as Timbuktu")
    MAP(259.56, [4.6, 51.5], 3.2, [
        *rivers("scheldt"), *towns("Antwerp", at=0.1),
        {"kind": "arrow", "path": [[4.6, 51.1], [5.4, 51.3], [6.2, 51.4]], "color": "UK", "in": 0.4, "dur": 1.6},
        {"kind": "unit", "type": "inf", "nation": "GER", "label": "15TH ARMY", "at": [3.6, 51.25], "in": 2.2, "keys": K((9.0, {"at": [3.62, 51.52]}))},
        {"kind": "route", "path": [[3.6, 51.3], [3.6, 51.45], [3.7, 51.6], [4.3, 51.8]], "color": "GER", "in": 3.0, "dur": 4.5},
        L("BEHIND THEIR BACKS", 960, 980, "red", 46, at=5.2, hud=True),
    ], beat="the German 15th Army was quietly escaping across the estuary behind them")
    scene(268.81, {"kind": "river", "time": "dusk", "bridges": False}, [
        *[V("boat", -200 - i * 500, 640 + (i % 2) * 90, 0.55, keys=K((10, {"x": 1700 - i * 500}))) for i in range(3)],
        V("cargo", -900, 720, 0.4, keys=K((10, {"x": 900}))),
        {"kind": "crowd", "who": ["german_soldier"], "count": 5, "spacing": 120, "x": 1200, "y": 930, "scale": 0.9, "expr": "tired", "walk": True, "dir": -1},
        CNT(0, 65000, 960, 220, 0.6, prefix="~", suffix=" MEN", size=100, dur=2.4),
        L("5–21 SEPT · GUNS AND TRUCKS · ANYTHING THAT FLOATED", 960, 340, "tag", 36, at=3.2),
    ], date="SEPTEMBER 1944", place="THE SCHELDT", beat="65,000 men got across with hundreds of guns and trucks")
    scene(278.81, {"kind": "field", "road": True, "houses": False, "trees": "pine"}, [
        A("chill", 1350, 900, 1.6, "stop", "determined", talk=True),
        PROP("sign", 1700, 800, 1.1, text="RALLY POINT"),
        {"kind": "crowd", "who": ["german_soldier", "german_pilot"], "count": 4, "spacing": 160, "x": 200, "y": 920, "scale": 1.0, "expr": "tired", "walk": True, "keys": K((6, {"x": 750}))},
        NC("Lt Gen Kurt Chill", "remnants of three divisions", at=1.0),
        L("ALBERT CANAL · BELGIUM", 960, 110, "tag", 40, at=0.2),
    ], beat="on the Albert Canal Kurt Chill simply stopped")
    scene(289.69, {"kind": "field", "road": True, "houses": False, "trees": "pine"}, [
        A("chill", 300, 900, 1.45, "pointL", "determined", flip=True, keys=K((4.0, {"pose": "point"}))),
        A("german_pilot", 700, 920, 1.25, "idle", "tired"),
        A("uboat_captain", 980, 920, 1.25, "idle", "worried"),
        A("diplomat", 1260, 920, 1.25, "idle", "nervous"),
        A("german_soldier", 1540, 920, 1.25, "salute", "tired"),
        L("SAILORS · AIRMEN · OFFICIALS", 960, 130, "tag", 46, at=1.4),
    ], beat="he grabbed every straggler: sailors, airmen, occupation officials")
    scene(298.69, {"kind": "field", "road": False, "houses": False, "trees": "pine", "fg": "sandbags"}, [
        {"kind": "crowd", "who": ["german_soldier", "german_pilot", "uboat_captain", "ss_soldier"], "count": 6, "spacing": 260, "x": 960, "y": 900, "scale": 1.1, "pose": "hold", "expr": "determined"},
        L("IT WASN'T PRETTY", 500, 200, "plain", 50, at=4.6),
        L("IT ONLY NEEDED TO EXIST", 1350, 300, "red", 50, at=6.2),
        L("A FRONT LINE", 960, 110, "tag", 46, at=0.4),
    ], beat="within hours something like a front line; it only needed to exist")
    scene(306.15, {"kind": "tent"}, [
        A("eisenhower", 600, 900, 1.5, "talk2", "neutral", talk=True),
        A("montgomery", 1350, 900, 1.5, "cross", "angry", keys=K((4.0, {"pose": "point", "talk": True}))),
        PROP("barrel", 960, 830, 0.5),
        L("THE LAST OF THE PETROL", 960, 110, "tag", 44, at=0.5),
    ], beat="the Allied argument: where to spend the last of the petrol")
    MAP(314.71, [5.6, 51.0], 6.5, [
        *[{"kind": "arrow", "path": p, "color": "USA", "in": 0.4 + i * 0.4, "dur": 1.4, "width": 18} for i, p in enumerate([[[4.0, 50.6], [5.5, 50.5]], [[4.6, 49.8], [6.0, 49.9]], [[4.2, 49.2], [6.2, 49.2]]])],
        L("EISENHOWER: BROAD FRONT", 600, 980, "tag", 42, at=0.6, hud=True),
        {"kind": "front", "path": [[6.0, 51.85], [6.2, 51.2], [6.1, 50.6], [6.4, 49.9], [6.8, 49.2]], "color": "GER", "in": 4.8, "width": 8},
        ML("WEST WALL", [6.45, 50.4], at=5.2),
        {"kind": "arrow", "path": [[5.0, 50.9], [5.5, 51.5], [5.9, 52.0], [6.8, 51.9], [7.2, 51.5]], "color": "UK", "in": 6.0, "dur": 3.0, "width": 30},
        ML("RUHR", [7.2, 51.45], style="red", at=8.8),
        L("MONTGOMERY: ONE THRUST IN THE NORTH", 1300, 110, "red", 40, at=5.0, hud=True),
    ], camera=[{"t": 0, "zoom": 1.0}, {"t": 13, "zoom": 1.1, "center": [6.2, 51.4]}], beat="broad front vs one thrust through Holland round the West Wall into the Ruhr")
    scene(328.29, {"kind": "airfield", "nation": UK, "planes": 0}, [
        *[V("dakota", 250 + i * 560, 760, 0.6, UK) for i in range(3)],
        *[V("glider", 520 + i * 560, 860, 0.45, UK) for i in range(2)],
        {"kind": "crowd", "who": ["british_para", "us_para"], "count": 5, "spacing": 150, "x": 1400, "y": 960, "scale": 0.95, "pose": "pockets", "expr": "tired"},
        L("ENGLAND · UNUSED", 960, 110, "tag", 44, at=0.4),
        CNT(0, 18, 960, 260, 5.4, suffix=" OPERATIONS PLANNED", size=80, dur=1.6),
    ], beat="sitting in England, unused, the perfect tool; 18 different airborne operations")
    scene(339.48, {"kind": "warroom"}, [
        A("brereton", 1600, 900, 1.4, "facepalm", "sad"),
        DOC("order", "OPERATION LINNET", ["DROP AT TOURNAI"], x=520, y=380, w=620, h=300, at=0.2, size=44, speed=30, stamp="CANCELLED"),
        DOC("order", "OPERATION COMET", ["ARNHEM · NIJMEGEN · GRAVE"], x=1150, y=640, w=620, h=300, at=1.6, size=40, speed=30, stamp="CANCELLED"),
        L("GROUND TROOPS GOT THERE FIRST", 960, 980, "tag", 44, at=4.4),
    ], beat="every one cancelled; ground troops overran the objective")
    scene(347.82, {"kind": "office", "flag": US, "portrait": False, "map": "DEEP BEHIND ENEMY LINES", "desk": False}, [
        A("diplomat", 1250, 900, 1.5, "pointL", "determined", talk=True),
        L("WASHINGTON", 1450, 260, "tag", 48, at=0.3),
    ], beat="Washington wanted to see what a big airborne army could do")
    scene(352.88, {"kind": "airfield", "nation": US}, [
        A("us_para", 700, 920, 1.5, "fist", "determined"),
        A("british_para", 1200, 920, 1.5, "cheer", "angry"),
    ], beat="the paratroopers wanted to fight")
    scene(355.22, STUDY, [
        A("host", 960, 900, 1.7, "explain", "smug", talk=True),
        L("A TOOL LOOKING FOR A JOB", 960, 140, "tag", 54, at=0.3),
    ], beat="the tool was looking for a job")

    # =============== CH4 THE ROAD NOBODY TOOK ===============
    ROAD(357.28, -0.16, -0.16, move=(0.2, 0.4), extra=[
        A("aide", 1350, 1010, 1.25, "hold", "worried", holds="radio", talk=True),
        A("host", 1700, 1010, 1.25, "idle", "neutral"),
    ], chapter="The Road Nobody Took", beat="AIDE: why does Antwerp get a sign? we haven't started driving")
    ROAD(362.0, -0.16, p_for("A1") - 0.01, move=(2.0, 7.0), extra=[
        A("host", 1700, 1010, 1.25, "explain", "determined", talk=True, keys=K((4.5, {"pose": "pointL"}))),
        A("aide", 1400, 1010, 1.25, "hold", "neutral", holds="radio"),
        L("THE ROAD NOBODY TOOK", 960, 92, "tag", 46, at=4.0),
    ], beat="HOST: the cheapest way to lose at Arnhem is to go to Arnhem; first exit isn't on the road")
    ROAD(369.6, p_for("A1") - 0.01, p_for("A1"), move=(0.2, 8.0), extra=[
        A("host", 1700, 1010, 1.25, "idle", "neutral", talk=True, keys=K((4.2, {"pose": "pointL", "expr": "determined"}), (10.0, {"pose": "present", "expr": "smug"}))),
        L("CLEAR THE SCHELDT IN SEPTEMBER", 960, 92, "tag", 44, at=4.6),
        L("PEOPLE SAID SO AT THE TIME", 960, 180, "plain", 40, at=11.2),
    ], beat="which exit? Antwerp first: clear the Scheldt in September and there's no Market Garden. That's one")
    LEDGER(383.44, [("A1 Antwerp first", 383.6)], [], beat="Allied column")
