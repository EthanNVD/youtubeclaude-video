from lib import *
from part1 import STUDY, tanks, UK, US, GE

NIGHT_POLDER = {"kind": "polder", "time": "night"}


def build():
    # =============== CH9 SUNDAY, 1 O'CLOCK ===============
    scene(1035.23, {"kind": "warroom"}, [
        A("brereton", 960, 900, 1.6, "chin", "neutral", keys=K((4.6, {"pose": "fist", "expr": "determined"}))),
        DOC("note", "WEATHER — 17 SEPT", ["FORECAST: GOOD"], x=1500, y=380, w=560, h=300, at=0.6, size=44, speed=24),
        ST("GO", 500, 320, 5.6, size=160, color="green"),
    ], chapter="Sunday, 1 O'Clock", date="16 SEPTEMBER 1944", clock="EVENING", beat="evening of 16 Sept, forecast good, the final decision: go")
    scene(1043.28, {"kind": "polder"}, [
        *[V("bomber", -200 - i * 330, 160 + (i % 3) * 130, 0.42, US, keys=K((8.0, {"x": 2500 - i * 330, "ease": "linear"}))) for i in range(6)],
        *[{"kind": "burst", "x": 400 + i * 380, "y": 300 + (i % 2) * 220, "in": 1.0 + i * 1.1, "size": 0.35} for i in range(5)],
        L("1,000+ BOMBERS AND FIGHTERS vs FLAK", 960, 110, "tag", 42, at=0.6),
    ], sfx=[{"t": 0, "id": "plane_engine", "dur": 8}], beat="well over a thousand Allied bombers and fighters hammered flak and airfields")
    scene(1051.36, {"kind": "airfield", "nation": "GERI", "planes": 0}, [
        *[V("fighter", 400 + i * 600, 830, 0.55, "GER") for i in range(3)],
        *[{"kind": "burst", "x": 300 + i * 450, "y": 900, "in": 0.4 + i * 0.6, "size": 0.7} for i in range(4)],
        *[FX("smoke", 300 + i * 450, 860, **{"in": 1.0 + i * 0.6}) for i in range(4)],
        L("ME 262 JET BASE", 960, 110, "tag", 44, at=0.3),
        L("NONE COULD TAKE OFF", 960, 210, "red", 44, at=5.0),
    ], camera=[{"t": 0, "zoom": 1.0, "shake": 4}, {"t": 3, "zoom": 1.05, "shake": 0}], beat="one raid cratered an Me 262 base so none could take off")
    scene(1060.58, STUDY, [
        A("host", 960, 900, 1.7, "show", "determined", holds="stopwatch"),
        HEAD("THE CLOCK STARTS NOW", 960, 270, 96, at=2.6, accent="NOW"),
    ], clock="SUN 17 SEP · 13:00", sfx=[{"t": 2.6, "id": "tick"}, {"t": 2.8, "id": "clock_tick", "dur": 1.6}], beat="Sunday 17 September, one o'clock: the clock starts now")
    scene(1065.04, {"kind": "airfield", "nation": UK, "planes": 0}, [
        *[V("dakota", 300 + i * 700, 780, 0.6, US, keys=K((3.0 + i, {"x": 2500, "y": 300, "rotate": -10}))) for i in range(3)],
        V("glider", 500, 860, 0.5, UK, keys=K((6.0, {"x": 2200, "y": 500, "rotate": -8}))),
        CNT(0, 1500, 640, 220, 0.8, prefix="~", suffix=" TRANSPORTS", size=70, dur=2.0),
        CNT(0, 500, 1340, 220, 2.0, prefix="~", suffix=" GLIDERS", size=70, dur=2.0),
        L("TWO DOZEN AIRFIELDS IN ENGLAND", 960, 340, "tag", 40, at=4.2),
    ], clock="SUN 17 SEP · 13:00", sfx=[{"t": 0.3, "id": "plane_flyby"}, {"t": 3.0, "id": "plane_flyby"}], beat="about 1,500 transports and nearly 500 gliders took off")
    scene(1073.92, {"kind": "polder"}, [
        *[V("dakota", -200 - i * 380, 140 + (i % 3) * 110, 0.36, US, keys=K((7.3, {"x": 2400 - i * 380, "ease": "linear"}))) for i in range(5)],
        {"kind": "bars", "title": "TRANSPORTS & GLIDERS LOST", "x": 1060, "y": 700, "max": 32, "width": 900,
         "items": [{"label": "PLANNERS EXPECTED: UP TO 30%", "value": 30, "in": 2.4, "color": "red"}, {"label": "ACTUAL: UNDER 3%", "value": 3, "in": 5.4, "color": "green"}]},
        L("WEATHER: CLOSE TO PERFECT", 960, 110, "tag", 42, at=0.3),
    ], beat="weather close to perfect; ready to lose 30%, they lost under three")
    scene(1081.22, {"kind": "heath"}, [
        {"kind": "paras", "x": 960, "y": 340, "count": 26, "spread": 1800, "fall": 520, "pdur": 7, "in": 0.0},
        *[V("glider", -300 - i * 500, 640 - i * 60, 0.5, UK, rotate=6, keys=K((6 + i, {"x": 600 + i * 600, "y": 820, "rotate": 0}))) for i in range(2)],
        CNT(0, 20000, 960, 160, 2.0, prefix="~", suffix=" MEN", size=90, dur=2.4),
        L("IN ABOUT 80 MINUTES · MOSTLY ON THEIR MARKS", 960, 270, "tag", 38, at=5.0),
    ], clock="SUN 17 SEP · 13:00–14:20", beat="about 20,000 British and American soldiers landed in 80 minutes")
    scene(1092.56, {"kind": "heath", "panels": False}, [
        A("british_para", 600, 920, 1.5, "cheer", "happy"),
        A("us_para", 1000, 920, 1.5, "thumbsup", "happy"),
        A("aide", 1400, 920, 1.5, "show", "happy", holds="radio"),
        L("\"THE BEST DROP WE EVER MADE\"", 960, 160, "plain", 56, at=0.6),
    ], beat="all three divisions called it the best drop they had ever made")
    scene(1097.36, {"kind": "hotel", "name": "Hotel Tafelberg"}, [
        {"kind": "paras", "x": 1400, "y": 160, "count": 10, "spread": 900, "fall": 260, "pdur": 6, "in": 0.0},
        A("model", 700, 930, 1.5, "idle", "neutral", keys=K((2.0, {"pose": "pointUp", "expr": "shocked"}))),
        L("A SHORT DRIVE FROM HIS HQ", 960, 110, "red", 44, at=4.6),
    ], place="OOSTERBEEK", beat="a few kilometres from the landing zones, at the hotel, Model")
    scene(1106.16, {"kind": "hotel", "name": "Hotel Tafelberg"}, [
        V("car", 1500, 940, 0.8, "GER"),
        A("model", 400, 930, 1.5, "hold", "panic", holds="folder", run=True, keys=K((3.0, {"x": 1250}))),
        A("german_officer", 100, 930, 1.3, "carry", "sweat", holds="crate", keys=K((3.6, {"x": 900}))),
        L("\"PACK EVERYTHING, WE LEAVE NOW.\"", 960, 130, "plain", 52, at=8.6),
    ], beat="Model and his staff packed up and left in a hurry: his own narrow escape struck him first")
    MAP(1116.92, [6.0, 51.97], 1.3, [
        *rivers("waal", "rhine"), *towns("Arnhem", "Nijmegen", at=0.0),
        {"kind": "arrow", "path": [[6.15, 52.15], [6.0, 52.05], [5.92, 51.985]], "color": "GER", "in": 0.8, "dur": 2.2},
        {"kind": "arrow", "path": [[6.25, 52.1], [6.1, 51.95], [5.88, 51.85]], "color": "GER", "in": 2.0, "dur": 2.6},
        ML("SS UNITS", [6.25, 52.15], style="tag", at=0.6),
        ML("MODEL + BITTRICH", [6.3, 52.0], style="dark", at=4.6),
    ], beat="within hours Model and Bittrich sent the SS toward Arnhem and Nijmegen")
    MAP(1126.72, [5.80, 51.99], 0.4, [
        *rivers("rhine"), *towns("Oosterbeek", "Arnhem", at=0.0),
        *[{"kind": "ring", "at": c, "r": 50, "color": "UK", "enter": "none", "dashed": False} for c in [[5.74, 52.0], [5.76, 51.99]]],
        ML("DROP ZONES", [5.745, 52.012], style="tag", at=0.2),
        ML("MODEL'S HQ", [5.84, 52.022], style="red", at=1.0),
        L("LANDED NEXT TO THE ONE MAN BEST PLACED TO STOP THEM", 960, 980, "tag", 36, at=1.8, hud=True),
    ], beat="they had landed next to the one man best placed to stop them")
    scene(1130.92, {"kind": "heath", "panels": False, "fg": "sandbags"}, [
        A("krafft", 700, 900, 1.6, "pointL", "determined", flip=True, talk=True),
        {"kind": "crowd", "who": ["ss_soldier"], "count": 3, "spacing": 260, "x": 1350, "y": 900, "scale": 1.1, "pose": "hold", "expr": "determined"},
        NC("Maj Sepp Krafft", "SS training battalion", at=0.6),
        L("CAMPED IN THE WOODS RIGHT BESIDE THE LANDING ZONES", 960, 110, "tag", 36, at=2.0),
    ], beat="an SS training battalion under Sepp Krafft happened to be camped beside the landing zones")
    scene(1139.28, {"kind": "heath", "panels": False}, [
        {"kind": "crowd", "who": ["british_para", "british_para_helmet"], "count": 5, "spacing": 180, "x": 200, "y": 940, "scale": 1.0, "walk": True, "expr": "determined", "keys": K((2.4, {"x": 800}))},
        *[FX("muzzle", 1600 + i * 120, 760 - i * 40, **{"in": 2.6 + i * 0.4}) for i in range(3)],
        FX("tracer", 1600, 760, dir=190, **{"in": 2.8}),
        L("A THIN BLOCKING LINE", 1500, 300, "red", 44, at=3.0),
        L("2 OF 3 BATTALIONS RAN STRAIGHT INTO IT", 960, 110, "tag", 40, at=4.2),
    ], sfx=[{"t": 2.6, "id": "machinegun", "dur": 3}], beat="two of the three British battalions ran straight into it")
    scene(1145.98, {"kind": "heath", "panels": False}, [
        A("aide", 960, 900, 1.7, "show", "worried", holds="radio", keys=K((2.4, {"pose": "rub", "expr": "panic"}))),
        L("NO SIGNAL", 1450, 300, "red", 60, at=1.0),
        L("SWALLOWED BY THE TREES AND THE DISTANCES", 960, 110, "tag", 38, at=2.6),
    ], sfx=[{"t": 0.2, "id": "radio_static", "dur": 4.5}], beat="the radios gave out almost at once")
    scene(1150.88, {"kind": "city", "time": "day"}, [
        A("roy_urquhart", 200, 920, 1.5, "idle", "worried", keys=K((4.0, {"x": 900}), (4.3, {"pose": "binoculars"}))),
        L("COULDN'T REACH HIS BRIGADES — WENT TO FIND THEM", 960, 110, "tag", 38, at=1.0),
    ], beat="Urquhart couldn't reach his brigades, so he went forward himself")
    scene(1157.4, {"kind": "city", "ruined": True, "time": "night"}, [
        A("roy_urquhart", 600, 900, 1.6, "cower", "worried"),
        {"kind": "crowd", "who": ["ss_soldier"], "count": 3, "spacing": 200, "x": 2200, "y": 930, "scale": 1.0, "walk": True, "dir": -1, "expr": "neutral", "keys": K((8.0, {"x": 900}))},
        CNT(0, 2, 1450, 250, 3.0, suffix=" DAYS CUT OFF FROM HIS HQ", size=60, dur=1.0),
    ], beat="caught in street fighting, hid from patrols, couldn't get back for two days")
    scene(1166.64, {"kind": "river", "bridges": True}, [
        {"kind": "crowd", "who": ["frost", "british_para", "british_para", "aide"], "count": 4, "spacing": 170, "x": 100, "y": 940, "scale": 1.05, "walk": True, "expr": "determined", "keys": K((3.6, {"x": 900}))},
        NC("Lt Col John Frost", "2nd Parachute Battalion", at=0.4),
    ], sfx=[{"t": 0, "id": "footsteps", "dur": 3.6}], beat="the third battalion under John Frost took a quiet road along the river")
    MAP(1170.0, [5.84, 51.983], 0.35, [
        *rivers("rhine"), *towns("Oosterbeek", "Arnhem", at=0.0),
        {"kind": "route", "path": [[5.76, 51.99], [5.82, 51.98], [5.88, 51.978], [5.912, 51.977]], "color": "UK", "in": 0.2, "dur": 3.0},
        ML("SLIPPED PAST", [5.84, 51.97], style="green", at=2.6),
    ], beat="and slipped past")
    scene(1173.93, {"kind": "archbridge", "time": "dusk"}, [
        *[V("halftrack", -200 - i * 230, 528, 0.22, "GER", moving=True, keys=K((11, {"x": 2300 - i * 230}))) for i in range(4)],
        A("british_para", 300, 920, 1.4, "binoculars", "determined"),
        A("frost", 1650, 920, 1.5, "pointUp", "determined"),
        CNT(0, 740, 960, 960, 0.6, prefix="~", suffix=" MEN AT THE NORTH END", size=60, dur=1.6),
    ], clock="SUN 17 SEP · DUSK", beat="about 740 men reached the north end; at dusk a German armoured column drove south across it")
    scene(1185.41, {"kind": "polder", "time": "dusk"}, [
        *[V("halftrack", 2200 + i * 260, 588, 0.36, "GER", flip=True, moving=True, keys=K((7.9, {"x": 400 + i * 260}))) for i in range(4)],
        A("grabner", 1500, 920, 1.5, "pointL", "smug"),
        NC("Hauptsturmführer Viktor Gräbner", "9th SS Reconnaissance Battalion", at=0.6),
        L("HEADING FOR NIJMEGEN · REMEMBER THAT COLUMN", 960, 110, "tag", 38, at=3.0),
    ], sfx=[{"t": 0, "id": "tank_engine", "dur": 7}], beat="Gräbner's reconnaissance battalion heading for Nijmegen; remember that column")
    scene(1193.41, {"kind": "river", "bridges": False}, [
        {"kind": "shape", "shape": "rect", "x": 960, "y": 560, "w": 900, "h": 30, "fill": "#7a868a", "in": 0, "keys": K((4.3, {"opacity": 1}), (4.5, {"opacity": 0}))},
        {"kind": "burst", "x": 960, "y": 560, "in": 4.4, "size": 1.0},
        FX("smoke", 960, 520, **{"in": 4.8}),
        {"kind": "crowd", "who": ["us_para"], "count": 3, "spacing": 160, "x": 200, "y": 940, "scale": 1.05, "run": True, "expr": "determined", "keys": K((4.0, {"x": 700}))},
        L("SON · WILHELMINA CANAL", 960, 110, "tag", 42, at=0.4),
    ], camera=[{"t": 0, "zoom": 1.0}, {"t": 4.4, "zoom": 1.0, "shake": 8}, {"t": 5.4, "zoom": 1.0, "shake": 0}], beat="as the 101st reached the canal bridge at Son, the Germans blew it")
    scene(1199.4, {"kind": "river", "bridges": False}, [
        {"kind": "crowd", "who": ["us_para"], "count": 3, "spacing": 200, "x": 700, "y": 940, "scale": 1.15, "pose": "head", "expr": "shocked"},
        FX("smoke", 960, 520), L("ALMOST IN THEIR FACES", 960, 140, "red", 46, at=0.6),
        L("FURTHER SOUTH: BEHIND SCHEDULE", 960, 240, "tag", 40, at=2.4),
    ], beat="almost in their faces")
    scene(1205.22, {"kind": "river", "time": "night", "bridges": False}, [
        {"kind": "shape", "shape": "rect", "x": 960, "y": 560, "w": 900, "h": 30, "fill": "#8a8478", "in": 2.0, "enter": "fade"},
        A("british_soldier", 500, 930, 1.3, "carry", "tired", holds="crate"),
        A("british_soldier", 900, 930, 1.3, "carry", "determined", holds="crate"),
        L("A BAILEY BRIDGE, BUILT OVERNIGHT", 960, 110, "tag", 42, at=0.4),
        V("tank", -300, 520, 0.3, UK, moving=True, **{"in": 5.0}, keys=K((8.8, {"x": 2200}))),
        L("TANKS ACROSS: MORNING OF THE 19TH", 960, 220, "red", 40, at=5.4),
    ], sfx=[{"t": 0.4, "id": "metal_clank"}, {"t": 2.0, "id": "metal_clank"}], beat="engineers put up a Bailey bridge; tanks only across early on the 19th")
    scene(1214.1, {"kind": "river", "bridges": True}, [
        {"kind": "crowd", "who": ["us_para"], "count": 4, "spacing": 160, "x": 100, "y": 940, "scale": 1.05, "run": True, "expr": "determined", "keys": K((3.0, {"x": 1000}))},
        L("GRAVE · BRIDGE OVER THE MAAS", 960, 110, "tag", 42, at=0.3),
        ST("TAKEN INTACT", 1450, 300, 3.4, size=80, color="green"),
    ], beat="the 82nd had a better afternoon: at Grave a platoon took the great bridge over the Maas intact")
    scene(1221.98, {"kind": "river", "bridges": True}, [
        PROP("crate", 900, 860, 0.9, text="CHARGES"),
        A("us_para", 1300, 930, 1.5, "shrug", "worried", talk=True),
        L("PREPARED FOR DEMOLITION · NEVER BLOWN", 960, 120, "tag", 40, at=0.4),
        FX("question", 1300, 500, **{"in": 3.0}),
    ], beat="it had been prepared for demolition; nobody knew why it was never blown")
    scene(1228.9, {"kind": "tent", "desk": False}, [
        A("gavin", 960, 900, 1.6, "chin", "worried", keys=K((2.2, {"pose": "pointL"}))),
        L("BUT AT NIJMEGEN THE PLAN WENT SIDEWAYS", 960, 110, "tag", 42, at=0.2),
    ], beat="but at Nijmegen the plan went sideways")
    MAP(1231.08, [5.95, 51.78], 0.6, [
        *rivers("waal", "maas"), *towns("Nijmegen", "Groesbeek", "Grave", at=0.0),
        {"kind": "region", "polygon": [[5.9, 51.81], [5.98, 51.81], [5.98, 51.75], [5.9, 51.75]], "color": "#4f7a3a", "in": 0.6, "fillOpacity": 0.4},
        ML("WOODED HIGH GROUND", [5.94, 51.78], style="map", at=1.0),
        {"kind": "region", "polygon": [[6.0, 51.80], [6.12, 51.80], [6.12, 51.72], [6.0, 51.72]], "color": "#2f5a2a", "in": 3.0, "fillOpacity": 0.5},
        ML("REICHSWALD", [6.06, 51.76], style="map", at=3.2),
        {"kind": "unit", "type": "armor", "nation": "GER", "label": "ARMOUR?", "at": [6.06, 51.74], "in": 5.4},
        ML("GERMANY", [6.15, 51.70], style="red", at=2.0),
    ], beat="Gavin's first worry: the high ground by the border; reports of armour massing in the Reichswald")
    scene(1242.78, {"kind": "field", "road": True, "houses": True, "trees": "round"}, [
        A("dutch_civilian", 700, 900, 1.5, "shrug", "smile", talk=True),
        A("gavin", 1250, 900, 1.5, "idle", "shocked", keys=K((2.2, {"pose": "facepalm"}))),
        ST("FALSE", 960, 300, 1.4, size=100),
    ], beat="those reports were false, Dutch civilians soon told the Americans")
    scene(1247.32, {"kind": "studio", "color": "#d9cdb0"}, [
        {"kind": "panel", "x": 480, "y": 540, "w": 960, "h": 1080, "color": "#c9d6c0", "in": 0},
        {"kind": "panel", "x": 1440, "y": 540, "w": 960, "h": 1080, "color": "#d9c4a8", "in": 0},
        A("gavin", 480, 960, 1.5, "point", "determined", talk=True),
        L("GAVIN REMEMBERED:\n\"A BATTALION FOR THE BRIDGE\nWITHOUT DELAY\"", 480, 160, "plain", 38, at=1.6),
        A("lindquist", 1440, 960, 1.5, "explain", "neutral", talk=True, **{"in": 9.0}),
        NC("Col Roy Lindquist", "508th Parachute Infantry", at=9.2, out=14),
        L("LINDQUIST REMEMBERED:\n\"SECURE YOUR OTHER\nOBJECTIVES FIRST\"", 1440, 160, "plain", 38, at=13.6),
    ], beat="Gavin's orders remembered two ways: bridge without delay vs other objectives first")
    scene(1265.42, {"kind": "field", "time": "night", "road": False, "houses": False}, [
        A("gavin", 700, 900, 1.6, "point", "angry", talk=True, **{"in": 1.6}),
        {"kind": "crowd", "who": ["us_para"], "count": 3, "spacing": 160, "x": 1100, "y": 940, "scale": 1.0, "run": True, "expr": "determined", "in": 5.2, "keys": K((7.4, {"x": 2100}))},
        L("THE BATTALION WENT TO THE OTHER OBJECTIVES", 960, 110, "tag", 38, at=0.2),
        L("\"DELAY NOT A SECOND LONGER\"", 960, 220, "red", 46, at=4.2),
    ], beat="only as darkness came did Gavin order: delay not a second longer")
    scene(1272.8, {"kind": "archbridge", "time": "dusk"}, [
        {"kind": "crowd", "who": ["german_soldier"], "count": 6, "spacing": 60, "x": 960, "y": 530, "scale": 0.25, "pose": "idle", "expr": "neutral"},
        CNT(0, 12, 960, 260, 0.6, prefix="~", suffix=" GUARDS — HOURS EARLIER", size=60, dur=1.0),
        *[V("halftrack", 2300 + i * 220, 528, 0.22, "GER", flip=True, moving=True, **{"in": 5.6}, keys=K((9.0, {"x": 1300 + i * 220}))) for i in range(3)],
        L("SS REINFORCEMENTS FROM THE NORTH", 960, 360, "red", 40, at=7.0),
        ST("ATTACK FAILED", 960, 900, 12.2, size=90),
    ], beat="hours earlier only a dozen guards; then SS reinforcements arriving from the north; the attack failed")
    scene(1285.94, {"kind": "polder"}, [
        *[V("halftrack", -300 - i * 260, 588, 0.36, "GER", moving=True, keys=K((8.0, {"x": 1700 - i * 260}))) for i in range(4)],
        A("grabner", 400, 920, 1.4, "pointUp", "determined", keys=K((1.0, {"pose": "point"}))),
        L("GRÄBNER TURNS BACK NORTH — TO CLEAR THE BRIDGE", 1100, 160, "tag", 38, at=0.6),
    ], date="MONDAY 18 SEPTEMBER", sfx=[{"t": 0, "id": "tank_engine", "dur": 8}], beat="Monday morning Gräbner drove back north to clear Frost's men off the bridge")
    scene(1294.44, {"kind": "archbridge", "time": "day", "burning": True}, [
        *[V("halftrack", 1500 - i * 260, 930, 0.6, "GER", flip=True, damaged=i < 2) for i in range(3)],
        *[{"kind": "burst", "x": 1500 - i * 260, "y": 860, "in": 1.0 + i * 1.6, "size": 0.7} for i in range(3)],
        *[FX("smoke", 1500 - i * 260, 820, **{"in": 1.6 + i * 1.6}) for i in range(3)],
        *[FX("muzzle", x, y, **{"in": 0.4 + i * 0.7}) for i, (x, y) in enumerate([(240, 560), (360, 640), (1800, 600), (1700, 520)])],
        CNT(0, 12, 960, 160, 6.0, suffix=" OF 22 VEHICLES KNOCKED OUT", size=60, dur=1.4),
        L("GRÄBNER AMONG 70+ GERMANS KILLED", 960, 270, "dark", 40, at=9.4),
    ], camera=[{"t": 0, "zoom": 1.0, "shake": 3}, {"t": 12.8, "zoom": 1.08, "shake": 2}], sfx=[{"t": 0.4, "id": "machinegun", "dur": 6}], beat="the paratroopers waited in the houses: 12 of 22 vehicles knocked out, Gräbner killed")
    scene(1307.32, {"kind": "airfield", "nation": UK, "planes": 0, "time": "storm"}, [
        *[V("dakota", 300 + i * 650, 780, 0.6, US) for i in range(3)],
        {"kind": "crowd", "who": ["british_para", "polish_para"], "count": 5, "spacing": 150, "x": 960, "y": 960, "scale": 0.95, "pose": "pockets", "expr": "tired"},
        L("SECOND LIFT: HOURS LATE", 960, 120, "red", 46, at=0.4),
    ], clock="MON 18 SEP", beat="in England the second lift was running hours late")

    # =============== CH10 MONDAY NIGHT ===============
    ROAD(1311.34, p_for("A5") - 0.05, p_for("G1") + 0.06, move=(0.3, 13.0), extra=[
        A("host", 1700, 1010, 1.25, "explain", "determined", talk=True, keys=K((8.6, {"pose": "pointL"}), (13.0, {"pose": "present", "expr": "smug"}))),
        L("ALLIED: NIJMEGEN BRIDGE ON DAY ONE", 960, 92, "tag", 40, at=2.6),
        L("GERMAN: GRAVE, READY TO BLOW, LEFT STANDING", 960, 180, "dark", 38, at=9.8),
    ], chapter="Monday Night", beat="exits: Nijmegen bridge day one (five); Grave left standing (German one)")
    ROAD(1325.6, 0.20 - 440 / ROAD_LEN, 0.21 - 440 / ROAD_LEN, move=(0.2, 9.0), extra=[
        A("host", 1700, 1010, 1.25, "show", "worried", holds="stopwatch", talk=True),
        L("PLAN: WELL ON THE WAY TO ARNHEM", 960, 92, "tag", 40, at=0.6),
        L("ACTUAL: JUST PAST EINDHOVEN", 960, 180, "red", 40, at=3.4),
    ], clock="MON 18 SEP · NIGHT", beat="Monday night: the tanks only just past Eindhoven, running late")

    # =============== CH11 BOATS ACROSS THE WAAL ===============
    scene(1335.24, {"kind": "field", "road": True, "houses": True, "trees": "round"}, [
        V("tank", -300, 900, 0.75, UK, moving=True, keys=K((4.0, {"x": 800}))),
        A("us_para", 1450, 920, 1.5, "wave", "happy", talk=True),
        A("guards_tanker", 1100, 920, 1.4, "salute", "happy", **{"in": 4.2}),
        L("GRENADIER GUARDS MEET THE 82ND AT GRAVE", 960, 160, "tag", 38, at=0.6),
    ], chapter="Boats Across the Waal", date="TUESDAY 19 SEPTEMBER", clock="08:20", sfx=[{"t": 0, "id": "tank_engine", "dur": 4}], beat="8:20 Tuesday the Guards meet the paratroopers at Grave")
    scene(1343.28, {"kind": "archbridge", "time": "day"}, [
        V("tank", 400, 960, 0.9, UK),
        A("guards_tanker", 900, 930, 1.4, "binoculars", "worried"),
        L("NIJMEGEN · THE BIGGEST BRIDGE ON THE ROAD", 960, 80, "tag", 40, at=0.4),
        *[{"kind": "burst", "x": 700 + i * 250, "y": 560, "in": 8.2 + i * 0.6, "size": 0.4} for i in range(3)],
        L("ATTACK AFTER ATTACK FAILED", 1450, 330, "red", 40, at=8.4),
    ], camera=[{"t": 0, "zoom": 1.0}, {"t": 8, "zoom": 1.1, "y": 480}], beat="by afternoon in Nijmegen staring at the huge steel arch; attacks on the south end failed")
    scene(1354.36, {"kind": "field", "road": False, "houses": True, "fg": "sandbags"}, [
        {"kind": "crowd", "who": ["ss_soldier", "german_soldier"], "count": 5, "spacing": 300, "x": 960, "y": 900, "scale": 1.1, "pose": "hold", "expr": "determined"},
        CNT(0, 500, 960, 230, 0.4, prefix="~", suffix=" GOOD SS TROOPS", size=80, dur=1.6),
        L("DUG IN AROUND THE BRIDGE", 960, 350, "tag", 40, at=2.4),
    ], beat="about 500 good SS troops dug in")
    MAP(1359.65, [5.95, 51.91], 0.9, [
        *rivers("waal", "rhine"), *towns("Arnhem", "Nijmegen", at=0.0),
        L("A DETAIL THAT TIES THE WHOLE ROAD TOGETHER", 960, 110, "tag", 40, at=0.4, hud=True),
        {"kind": "shape", "shape": "cross", "at": [5.912, 51.977], "in": 7.6, "scale": 0.6},
        ML("FROST HOLDS THE NORTH END", [5.912, 51.995], style="tag", at=8.0),
        {"kind": "route", "path": [[5.96, 52.02], [6.06, 51.9], [6.0, 51.86], [5.87, 51.845]], "color": "GER", "in": 12.0, "dur": 3.4},
        ML("FERRY", [6.07, 51.885], style="red", at=13.4),
    ], beat="Nijmegen reinforced from Arnhem, but not over the bridge Frost held: by ferry further east")
    scene(1378.07, {"kind": "archbridge", "time": "dusk", "burning": True}, [
        A("frost", 960, 920, 1.7, "binoculars", "determined"),
        L("EVERY HOUR FROST HELD = AN HOUR NIJMEGEN DIDN'T GET", 960, 110, "tag", 36, at=0.4),
    ], sfx=[{"t": 0.2, "id": "clock_tick", "dur": 4.6}], beat="every hour Frost held on was an hour the Germans at Nijmegen didn't get")
    scene(1383.21, {"kind": "tent", "desk": False}, [
        A("gavin", 960, 900, 1.6, "explain", "determined", talk=True, keys=K((2.4, {"pose": "talk2"}))),
        L("A PLAN THAT SOUNDED MAD", 960, 110, "red", 46, at=0.4),
    ], beat="so Gavin came up with a plan that sounded mad")
    MAP(1386.43, [5.85, 51.852], 0.2, [
        *rivers("waal"), *towns("Nijmegen", at=0.0),
        {"kind": "city", "name": "Road bridge", "at": [5.865, 51.851], "side": "right", "in": 0.2},
        {"kind": "arrow", "path": [[5.83, 51.840], [5.832, 51.862]], "color": "USA", "in": 3.4, "dur": 1.6, "width": 18},
        ML("504TH: BOATS, DOWNSTREAM, IN DAYLIGHT", [5.80, 51.835], style="tag", size=28, at=3.6),
        {"kind": "arrow", "path": [[5.835, 51.865], [5.86, 51.860]], "color": "USA", "in": 7.6, "dur": 1.2, "width": 18},
        ML("HIT THE NORTH END", [5.86, 51.868], style="tag", size=28, at=8.4),
        {"kind": "arrow", "path": [[5.865, 51.835], [5.865, 51.846]], "color": "UK", "in": 11.0, "dur": 1.2, "width": 18},
        ML("GUARDS + PARAS HIT THE SOUTH", [5.90, 51.833], style="tag", size=28, at=11.4),
        L("TAKE IT FROM BOTH ENDS", 960, 110, "red", 48, at=1.2, hud=True),
    ], beat="take the bridge from both ends: the 504th crosses in boats and hits the north end")
    ROAD(1403.25, p_for("A5") - 0.08, p_for("A5") - 0.075, move=(0.2, 7.0), vehicles=4, extra=[
        A("aide", 1350, 1010, 1.25, "shrug", "worried", holds="radio", talk=True),
        A("host", 1700, 1010, 1.25, "idle", "neutral", keys=K((2.4, {"pose": "pointL", "talk": True}), (6.6, {"pose": "write", "talk": False}))),
        L("THE BOATS: BEHIND THE TANKS, BEHIND THE TRAFFIC", 960, 92, "tag", 38, at=2.6),
    ], beat="AIDE: what boats? HOST: coming up the road behind the tanks, behind the traffic. Noted")
    scene(1411.24, {"kind": "river", "bridges": True}, [
        V("truck", -300, 930, 0.7, UK, moving=True, keys=K((3.0, {"x": 500}))),
        V("assaultboat", 1250, 920, 0.9, **{"in": 3.0, "enter": "drop"}),
        {"kind": "crowd", "who": ["us_para"], "count": 3, "spacing": 140, "x": 1600, "y": 960, "scale": 1.0, "pose": "carry", "expr": "worried"},
        L("CANVAS + PLYWOOD · ~6 M LONG", 1250, 700, "tag", 38, at=4.6),
    ], date="WEDNESDAY 20 SEPTEMBER", clock="EARLY AFTERNOON", beat="the boats arrived early Wednesday afternoon: small, flat, canvas and plywood")
    scene(1420.55, {"kind": "river", "bridges": True}, [
        *[V("assaultboat", 260 + i * 460, 900, 0.9, keys=K((1.0, {"y": 900}), (8.6, {"y": 720, "scale": 0.65}))) for i in range(4)],
        A("julian_cook", 1750, 960, 1.3, "point", "determined", flip=True, talk=True),
        NC("Maj Julian Cook", "3rd Bn, 504th Parachute Infantry", at=0.6),
        L("SEVERAL HUNDRED METRES OF FAST RIVER", 960, 110, "tag", 38, at=4.4),
    ], clock="15:00", beat="about three o'clock the first wave of Cook's battalion pushed off")
    scene(1429.2, {"kind": "river", "bridges": True}, [
        *[V("assaultboat", 260 + i * 460, 760 - (i % 2) * 60, 0.7, keys=K((10.8, {"y": 560 + (i % 2) * 20, "scale": 0.45}))) for i in range(4)],
        *[FX("splash", 300 + i * 300, 700 - (i % 3) * 60, **{"in": 0.6 + i * 0.7}) for i in range(6)],
        FX("tracer", 1300, 450, dir=225, **{"in": 0.3}), FX("tracer", 700, 450, dir=250, **{"in": 1.6}), FX("tracer", 1600, 450, dir=210, **{"in": 3.0}),
        L("FIRE FROM THE FAR BANK", 960, 110, "red", 42, at=0.4),
        L("ONLY ~HALF THE BOATS MADE IT BACK", 960, 980, "dark", 40, at=7.6),
    ], camera=[{"t": 0, "zoom": 1.05, "shake": 3}, {"t": 11, "zoom": 1.12, "shake": 3}], sfx=[{"t": 0.3, "id": "machinegun", "dur": 8}], beat="the Germans opened fire; bullets ripped through the canvas; half the boats came back")
    scene(1440.2, {"kind": "polder", "dyke": 560}, [
        {"kind": "crowd", "who": ["us_para", "julian_cook"], "count": 5, "spacing": 170, "x": 100, "y": 940, "scale": 1.05, "run": True, "expr": "determined", "keys": K((6.5, {"x": 1500}))},
        *[FX("muzzle", 1700 + i * 90, 560 - i * 20, **{"in": 1.0 + i * 1.3}) for i in range(3)],
        L("ACROSS OPEN GROUND TO THE NORTH ENDS OF BOTH BRIDGES", 960, 110, "tag", 36, at=1.0),
    ], beat="the men who reached the north bank fought across open ground to the north ends")
    scene(1447.32, {"kind": "archbridge", "time": "dusk"}, [
        *tanks(-200, 1500, 528, 0.2, 6.0, n=4, gap=120),
        L("HELD AT BOTH ENDS", 960, 640, "green", 40, at=0.6),
    ], clock="19:10", camera=[{"t": 0, "zoom": 1.0}, {"t": 6, "zoom": 1.08, "x": 1000, "y": 520}], beat="at ten past seven British tanks drove across")
    scene(1453.81, {"kind": "office", "portrait": False, "desk": False, "map": "WAAL · RHINE"}, [
        A("model", 960, 900, 1.6, "stop", "determined", talk=True),
        DOC("order", "MODEL — ORDER", ["BRIDGES OVER THE WAAL AND", "THE RHINE NOT TO BE DESTROYED"], x=1490, y=400, w=740, h=340, at=3.4, size=34, speed=26),
        L("IT NEVER WENT UP — PART OF THE REASON:", 960, 110, "tag", 38, at=0.2),
        L("HE WANTED THEM FOR HIS OWN COUNTER-ATTACK", 1440, 640, "plain", 32, at=8.8),
    ], beat="it never went up: Model had ordered the bridges not destroyed")
    scene(1464.08, {"kind": "office", "portrait": False, "desk": False, "time": "night", "clockTime": "11:50"}, [
        A("model", 960, 900, 1.6, "facepalm", "angry"),
        L("CHANGED HIS MIND CLOSE TO MIDNIGHT", 960, 110, "tag", 40, at=0.6),
        ST("TOO LATE", 1450, 360, 3.6, size=90),
    ], beat="he only changed his mind close to midnight, after the Americans held it")
    scene(1472.01, {"kind": "archbridge", "time": "night"}, [
        {"kind": "crowd", "who": ["dutch_civilian"], "count": 3, "spacing": 220, "x": 600, "y": 920, "scale": 1.2, "pose": "hold", "expr": "determined"},
        *[FX("muzzle", 500 + i * 220, 760, **{"in": 1.0 + i * 0.8}) for i in range(3)],
        L("GAVIN: ATTACK FROM BOTH ENDS AT ONCE", 1300, 200, "tag", 36, at=0.2),
        L("+ DUTCH RESISTANCE KEPT THE DEMOLITION PARTIES UNDER FIRE", 960, 980, "green", 32, at=2.6),
    ], beat="Gavin added two reasons: both ends at once, and the Dutch resistance")
    scene(1480.77, STUDY, [
        A("host", 960, 900, 1.7, "show", "worried", holds="stopwatch", talk=True),
        CNT(0, 35, 960, 200, 2.0, prefix="~", suffix=" HOURS AT NIJMEGEN", size=80, dur=2.0),
        L("PLAN: 2–3 DAYS TO REACH ARNHEM", 960, 330, "red", 42, at=8.4),
    ], beat="almost 35 hours at Nijmegen, on a plan with two to three days to reach Arnhem")

    # =============== CH12 LENT ===============
    scene(1494.44, NIGHT_POLDER, [
        *tanks(-300, 1400, 600, 0.42, 3.4, n=4, gap=200),
        L("LENT", 1750, 520, "tag", 52, at=0.3),
        L("ONE KILOMETRE NORTH OF THE BRIDGE", 960, 110, "tag", 38, at=1.0),
    ], chapter="Lent", sfx=[{"t": 0, "id": "tank_engine", "dur": 3.4}], beat="the four tanks reached Lent and stopped")
    scene(1499.72, NIGHT_POLDER, [
        A("guards_tanker", 500, 920, 1.5, "scratch", "worried"),
        A("guards_tanker", 860, 920, 1.4, "shrug", "nervous", look_={"hat": "helmet_uk"}),
        FX("question", 680, 420, **{"in": 1.0}),
        A("ss_soldier", 1600, 900, 1.1, "hold", "worried", **{"in": 6.2}),
        FX("question", 1600, 560, **{"in": 7.4}),
        L("DARK · CHAOTIC · NOBODY KNEW WHAT WAS AHEAD", 960, 110, "tag", 38, at=0.4),
        L("NOT EVEN THE GERMANS", 1500, 300, "red", 38, at=7.0),
    ], beat="dark, chaotic, nobody knew what waited; not even the Germans knew how thin their line was")
    scene(1510.62, {"kind": "polder", "time": "dusk", "dyke": 600}, [
        V("tank", 960, 578, 0.5, UK),
        {"kind": "glow", "x": 960, "y": 520, "r": 320, "color": "#fff3c0", "strength": 0.4},
        L("BEYOND LENT: THE ROAD ON TOP OF A DYKE", 960, 110, "tag", 38, at=0.4),
        L("A TANK STANDS OUT AGAINST THE SKY", 960, 780, "red", 40, at=3.2),
    ], beat="beyond Lent the road ran on a dyke where a tank stands out against the sky")
    scene(1516.06, {"kind": "archbridge", "time": "night", "burning": True}, [
        A("frost", 960, 920, 1.6, "idle", "tired", kneel=True),
        {"kind": "burst", "x": 1400, "y": 820, "in": 3.6, "size": 0.6},
        L("11 KM AWAY · FROST'S LAST DAY", 960, 110, "tag", 40, at=0.4),
        L("BADLY WOUNDED BY A MORTAR BOMB", 960, 210, "dark", 38, at=4.4),
    ], beat="eleven kilometres away Frost's men were finishing their last day; Frost badly wounded")
    scene(1525.15, {"kind": "city", "ruined": True, "time": "night"}, [
        FX("fire", 400, 640), FX("fire", 1500, 600), FX("smoke", 420, 520), FX("smoke", 1500, 480),
        A("british_para", 700, 920, 1.3, "carry", "sad"),
        A("british_para_helmet", 1000, 920, 1.3, "carry", "sad"),
        A("ss_soldier", 1500, 920, 1.3, "idle", "neutral", **{"in": 4.2}),
        L("BRIEF TRUCE · THE WOUNDED CARRIED OUT INTO CAPTIVITY", 960, 110, "tag", 34, at=4.4),
    ], tint="grey", ambience="fire", beat="buildings burning with the wounded inside; under a truce they were carried into captivity")
    scene(1535.23, {"kind": "archbridge", "time": "night", "burning": True}, [
        *[FX("muzzle", 300 + i * 140, 700 + (i % 2) * 40, **{"in": 0.4 + i * 1.2}) for i in range(3)],
        L("FOUGHT ON UNTIL ~10 PM · A FEW HELD INTO THE EARLY HOURS", 960, 110, "tag", 34, at=0.4),
        *[V("halftrack", 2100 + i * 220, 528, 0.22, "GER", flip=True, moving=True, **{"in": 6.2}, keys=K((10.0, {"x": 900 + i * 220}))) for i in range(4)],
        ST("BRIDGE LOST", 960, 820, 6.4, size=100),
    ], beat="from that night the Germans had the Arnhem bridge")
    MAP(1545.33, [5.88, 51.92], 0.55, [
        *rivers("waal", "rhine"), *towns("Nijmegen", "Lent", "Elst", "Arnhem", at=0.0),
        {"kind": "arrow", "path": [[5.912, 51.98], [5.88, 51.95], [5.86, 51.925]], "color": "GER", "in": 0.4, "dur": 2.4},
        {"kind": "front", "path": [[5.80, 51.905], [5.86, 51.90], [5.93, 51.905]], "color": "GER", "in": 4.0, "enter": "draw", "dur": 2.0, "width": 12},
        ML("THE SCREEN", [5.95, 51.895], style="red", at=5.6),
    ], beat="they poured tanks and men south and built the screen between Lent and Arnhem")
    scene(1554.81, {"kind": "paper"}, [
        DOC("book", "US ARMY OFFICIAL HISTORY", ["THAT SCREEN:", "\"THE GREATEST DELAY OF ALL\""], x=960, y=540, w=1100, h=520, at=0.2, size=56, speed=28),
    ], beat="the official history calls that screen the greatest delay of all")
    ROAD(1559.55, p_for("L") - 0.01, p_for("L"), move=(0.2, 2.6), extra=[
        A("aide", 1350, 1010, 1.25, "hold", "worried", holds="radio", talk=True),
        A("host", 1700, 1010, 1.25, "pointL", "neutral", keys=K((2.4, {"talk": True}))),
        L("THE SIGN WE PROMISED NOT TO PAINT", 960, 92, "tag", 40, at=3.2),
    ], beat="AIDE: should they have kept going from Lent? HOST: the sign we wouldn't paint")
    scene(1565.47, {"kind": "studio", "color": "#d9cdb0"}, [
        {"kind": "scale", "x": 960, "y": 640, "left": "KEEP GOING", "right": "HOLD", "leftNation": "UK", "rightNation": "UK", "title": "LENT, 20 SEPT, NIGHT",
         "items": [
             {"side": "L", "label": "GERMAN GENERAL: 'ALL OVER'", "value": 1, "in": 0.4},
             {"side": "L", "label": "HIS MAP: ALMOST NOTHING", "value": 1, "in": 3.4},
             {"side": "L", "label": "BRIDGE HELD ~2½ MORE HRS", "value": 1, "in": 6.4},
             {"side": "R", "label": "FOUR TANKS, AT NIGHT", "value": 1, "in": 12.2},
             {"side": "R", "label": "RAISED ROAD", "value": 1, "in": 15.0},
             {"side": "R", "label": "ENEMY OF UNKNOWN STRENGTH", "value": 1, "in": 17.0}]},
        L("THE CASE FOR GOING ON IS STRONG", 960, 90, "green", 40, at=0.2, out=11.4),
        L("THE CASE AGAINST IS STRONG TOO", 960, 90, "red", 40, at=11.6),
    ], beat="the case for going on vs the case against")
    ROAD(1588.03, p_for("L"), p_for("L"), move=(0.2, 0.4), extra=[
        A("host", 1700, 1010, 1.25, "offer", "smile", talk=True),
        L("PAINT IT IN THE COMMENTS", 960, 92, "tag", 46, at=4.8),
    ], beat="a bridge that was falling as they drove: we'll leave that sign blank; paint it in the comments")

    # =============== CH13 HELL'S HIGHWAY ===============
    scene(1595.35, {"kind": "polder", "dyke": 600}, [
        *tanks(-200, 900, 578, 0.4, 5.0, n=3, gap=240),
        {"kind": "burst", "x": 900, "y": 560, "in": 5.4, "size": 0.6}, FX("smoke", 900, 520, **{"in": 5.8}),
        L("ELST", 1700, 520, "tag", 46, at=0.4),
        L("STALLED ON THE RAISED HIGHWAY", 960, 160, "red", 42, at=6.4),
    ], chapter="Hell's Highway", date="THURSDAY 21 SEPTEMBER", beat="Thursday the Guards tried the road in daylight; stalled short of Elst")
    MAP(1605.7, [5.62, 51.64], 1.6, [
        *rivers("maas", "waal"), *towns("Eindhoven", "Veghel", "Grave", "Nijmegen", at=0.0),
        {"kind": "line", "path": ROUTE[:6], "color": "#6a5a4a", "width": 8, "enter": "none"},
        {"kind": "arrow", "path": [[5.85, 51.65], [5.6, 51.62]], "color": "GER", "in": 2.6, "dur": 1.6},
        {"kind": "arrow", "path": [[5.3, 51.6], [5.52, 51.62]], "color": "GER", "in": 3.4, "dur": 1.6},
        {"kind": "shape", "shape": "cross", "at": [5.55, 51.62], "in": 5.0, "scale": 0.6},
        ML("CORRIDOR CUT", [5.55, 51.57], style="red", at=5.2),
        {"kind": "arrow", "path": [[5.8, 51.82], [5.62, 51.68]], "color": "UK", "dashed": True, "in": 8.0, "dur": 1.6},
        ML("TANKS TURN BACK", [5.85, 51.72], style="tag", at=8.6),
        L("HELL'S HIGHWAY", 960, 110, "red", 56, at=12.4, hud=True),
    ], beat="German attacks cut the corridor to the south; tanks turned back; Hell's Highway")
    scene(1622.86, {"kind": "polder"}, [
        *[V("dakota", -400 - i * 400, 160 + (i % 2) * 90, 0.4, US, keys=K((8.0, {"x": 2300 - i * 400, "ease": "linear"}))) for i in range(3)],
        {"kind": "paras", "x": 960, "y": 360, "count": 16, "spread": 1600, "fall": 360, "pdur": 7, "in": 0.6, "color": "#d9d4bf"},
        A("sosabowski", 1650, 960, 1.4, "binoculars", "determined"),
        NC("Maj Gen Stanisław Sosabowski", "1st Polish Independent Parachute Brigade", at=0.6),
        L("TWO DAYS LATE · NOT WHERE PLANNED", 700, 110, "tag", 38, at=5.4),
    ], beat="Thursday the Polish brigade finally jumped, two days late, not where it had planned")
    MAP(1634.64, [5.83, 51.97], 0.32, [
        *rivers("rhine"), *towns("Oosterbeek", "Driel", at=0.0),
        {"kind": "ring", "at": [5.81, 51.955], "r": 60, "color": "POL", "in": 0.4, "enter": "grow", "dashed": False},
        ML("SOUTH BANK — OPPOSITE THE BRITISH", [5.81, 51.94], style="tag", at=1.2),
    ], beat="landing zone changed to the polder near Driel on the south bank")
    scene(1641.94, {"kind": "studio", "color": "#d9cdb0"}, [
        CNT(0, 114, 960, 300, 0.2, suffix=" SET OUT", size=80, dur=1.0),
        CNT(0, 41, 960, 460, 2.6, suffix=" TURNED BACK", size=80, dur=0.8, color="red"),
        CNT(0, 1000, 960, 620, 4.6, prefix="~", suffix=" POLES LANDED", size=70, dur=1.0),
        *[V("dakota", 300, 860, 0.3, US)],
    ], beat="114 transports set out, 41 turned back, about a thousand Poles landed")
    scene(1648.92, {"kind": "river", "bridges": False}, [
        V("boat", 900, 700, 0.8, rotate=-14, damaged=True),
        A("sosabowski", 1500, 960, 1.5, "hips", "angry"),
        L("THE FERRY: OUT OF ACTION", 900, 140, "red", 46, at=0.6),
    ], beat="the ferry they were to use was out of action")
    scene(1653.27, {"kind": "river", "time": "night", "bridges": False}, [
        L("HOW DO YOU TELL THE POLES WHAT'S HAPPENING?", 960, 110, "tag", 38, at=0.2),
        L("NOT BY RADIO", 960, 200, "red", 44, at=1.0),
        A("ernest_archer", 400, 760, 1.2, "idle", "determined", keys=K((13.0, {"x": 1500, "y": 600, "scale": 0.8}))),
        {"kind": "shape", "shape": "rect", "x": 960, "y": 900, "w": 2600, "h": 380, "fill": "#14263d", "opacity": 0.92},
        FX("splash", 400, 740, **{"in": 6.0}),
        NC("Pte Ernest Archer", "swam the Rhine with a message", at=9.6),
    ], beat="not by radio: Private Ernest Archer swam the Rhine with a message")
    scene(1667.21, STUDY, [
        A("aide", 700, 900, 1.6, "show", "sad", holds="radio", talk=True),
        A("host", 1250, 900, 1.6, "idle", "smug", keys=K((2.8, {"pose": "explain", "talk": True}))),
        L("THE MOST RELIABLE RADIO: A MAN WHO COULD SWIM", 960, 120, "tag", 40, at=3.8),
    ], beat="AIDE: further than my set reaches too. HOST: the most reliable radio was a man who could swim")
    MAP(1674.78, [5.84, 51.988], 0.25, [
        *rivers("rhine"), *towns("Oosterbeek", at=0.0),
        {"kind": "pocket", "polygon": [[5.82, 51.99], [5.85, 51.995], [5.855, 51.985], [5.84, 51.977], [5.82, 51.98]], "in": 0.4, "color": "UK"},
        ML("THE OOSTERBEEK POCKET", [5.84, 52.005], style="tag", at=1.0),
        ML("MODEL'S OLD HOTEL", [5.84, 51.996], style="red", size=26, at=5.4),
    ], beat="the British squeezed into a pocket around Oosterbeek, the same village as Model's hotel")
    scene(1683.97, {"kind": "home"}, [
        A("british_para", 600, 900, 1.4, "idle", "tired", seated=True),
        A("british_para_helmet", 960, 900, 1.4, "idle", "sad", kneel=True),
        A("civilian_woman", 1350, 900, 1.4, "carry", "worried", holds="crate"),
        L("AID POSTS IN THE FRONT LINE", 960, 110, "tag", 42, at=0.4),
        L("HOUSES CHANGED HANDS MORE THAN ONCE", 960, 200, "plain", 38, at=2.4),
    ], tint="grey", beat="aid posts sat in the front line in houses that changed hands")
    scene(1689.6, {"kind": "heath", "panels": False}, [
        *[V("dakota", -400 - i * 450, 180 + (i % 2) * 80, 0.42, UK, keys=K((6.0, {"x": 2300 - i * 450, "ease": "linear"}))) for i in range(2)],
        {"kind": "paras", "x": 960, "y": 360, "count": 10, "spread": 1400, "fall": 380, "pdur": 6, "in": 0.4, "color": "#e86a3a"},
        {"kind": "crowd", "who": ["ss_soldier"], "count": 3, "spacing": 260, "x": 1300, "y": 950, "scale": 1.0, "pose": "pointUp", "expr": "happy"},
        L("SUPPLIES ONTO ZONES THE GERMANS NOW HELD", 960, 110, "red", 38, at=1.6),
    ], beat="resupply planes kept dropping onto landing zones the Germans now held")
    scene(1696.12, {"kind": "river", "time": "night", "bridges": False}, [
        *[V("assaultboat", 300 + i * 500, 880, 0.75, keys=K((10, {"y": 620, "scale": 0.5}))) for i in range(3)],
        FX("tracer", 1200, 440, dir=230, **{"in": 2.0}), FX("splash", 800, 700, **{"in": 3.0}),
        L("NIGHT OF THE 24TH · THE DORSETS CROSS", 960, 110, "tag", 40, at=0.4),
        CNT(0, 315, 600, 980, 4.0, suffix=" SET OUT", size=60, dur=0.8),
        CNT(0, 200, 1300, 980, 8.0, prefix="~", suffix=" CAPTURED", size=60, dur=0.8, color="red"),
    ], beat="the Dorsets tried to cross: of 315, about 200 ended up prisoners, a handful got through")
    scene(1711.1, {"kind": "tent", "desk": False}, [
        A("horrocks", 650, 900, 1.5, "idle", "sad", headMove="nod"),
        A("browning", 1300, 900, 1.5, "idle", "sad", headMove="nod"),
        L("BRING THE SURVIVORS BACK", 960, 140, "tag", 46, at=1.4),
    ], date="25 SEPTEMBER", clock="09:30", beat="Horrocks and Browning agreed to bring the survivors back")
    scene(1717.42, {"kind": "heath", "panels": False, "time": "night", "weather": "rain"}, [
        {"kind": "crowd", "who": ["british_para", "british_para_helmet", "aide"], "count": 6, "spacing": 170, "x": 100, "y": 940, "scale": 1.0, "walk": True, "expr": "tired", "keys": K((8.0, {"x": 1300}))},
        L("HEAVY RAIN · BOOTS MUFFLED WITH CLOTH", 960, 110, "tag", 40, at=0.6),
    ], sfx=[{"t": 0, "id": "footsteps", "dur": 8}], ambience="rain", beat="that night, in heavy rain, boots muffled, they slipped down to the river")
    scene(1725.9, {"kind": "river", "time": "night", "bridges": False, "weather": "rain"}, [
        *[V("assaultboat", 200 + i * 600, 640, 0.6, keys=K((5.4, {"y": 860, "scale": 0.9}))) for i in range(3)],
        L("FERRIED ACROSS UNTIL DAYLIGHT", 960, 110, "tag", 40, at=0.4),
    ], ambience="rain", beat="engineers ferried them across until daylight")
    scene(1731.34, {"kind": "studio", "color": "#2c2a28"}, [
        CNT(0, 2400, 480, 440, 0.2, prefix="~", suffix=" CAME BACK", size=70, dur=1.4, color="green"),
        CNT(0, 300, 1440, 440, 3.0, prefix="~", suffix=" LEFT BEHIND", size=70, dur=1.0),
        CNT(0, 100, 960, 700, 6.0, prefix="~", suffix=" KILLED IN THE CROSSING", size=60, dur=1.0, color="red"),
    ], tint="grey", ambience=None, beat="about 2,400 came back; roughly 300 left; nearly 100 killed during the crossing")
    scene(1740.69, {"kind": "river", "time": "dawn", "bridges": False}, [
        A("roy_urquhart", 960, 920, 1.7, "idle", "tired"),
        L("\"WE HAVE NO REGRETS.\"", 960, 150, "plain", 60, at=3.6),
    ], ambience="wind", beat="Urquhart, speaking for his men: we have no regrets")
    scene(1746.19, STUDY, [
        A("host", 960, 900, 1.7, "shrug", "sad", talk=True),
        L("SOMEONE HAD TO BE BLAMED", 960, 130, "tag", 44, at=0.3),
        L("NOT THE PLANNERS", 960, 230, "red", 44, at=2.0),
    ], beat="someone had to be blamed, and it wasn't going to be the planners")
    scene(1750.59, {"kind": "office", "flag": UK, "portrait": False, "desk": False}, [
        A("montgomery", 700, 900, 1.5, "talk", "angry", talk=True),
        A("diplomat", 1300, 900, 1.4, "idle", "neutral", look_={"outfit": "tunic", "hat": "peaked"}),
        L("\"THE POLES FOUGHT VERY BADLY\"", 960, 140, "red", 46, at=2.0),
    ], date="OCTOBER 1944", beat="Montgomery told the head of the British Army the Poles had fought very badly")
    scene(1757.05, {"kind": "office", "flag": UK, "portrait": False, "desk": False, "fg": "officedesk"}, [
        A("browning", 700, 900, 1.6, "write", "smug"),
        DOC("letter", "BROWNING ON SOSABOWSKI", ["\"DIFFICULT\"", "\"UNWILLING\""], x=1350, y=420, w=640, h=380, at=0.6, size=48, speed=14),
    ], beat="Browning wrote a long letter attacking Sosabowski")
    scene(1761.65, {"kind": "corridor", "doors": ["POLISH GOV'T", "IN EXILE"]}, [
        A("sosabowski", 960, 900, 1.6, "idle", "sad"),
        ST("REMOVED FROM COMMAND", 960, 300, 2.4, size=70),
        L("MANY HISTORIANS: A DISGRACE", 960, 980, "plain", 44, at=6.0),
    ], date="DECEMBER 1944", tint="grey", beat="under British pressure he was removed from command; many call it a disgrace")
    scene(1770.61, {"kind": "rally", "flag": "NED"}, [
        PROP("medal", 960, 520, 2.4),
        L("HIGHEST MILITARY HONOUR FOR GALLANTRY", 960, 160, "tag", 40, at=0.6),
        L("THE POLISH BRIGADE", 960, 250, "plain", 40, at=1.0),
        L("+ SOSABOWSKI, LONG AFTER HIS DEATH", 960, 800, "green", 40, at=4.6),
    ], date="2006", beat="in 2006 the Netherlands honoured the Polish brigade and Sosabowski")

    # =============== CH14 READING THE ROAD ===============
    ROAD(1780.95, -0.10, 0.70, move=(1.0, 21.0), extra=[
        A("host", 1720, 1010, 1.2, "explain", "neutral", talk=True, keys=K((12.0, {"pose": "pointL"}), (20.6, {"pose": "idle"}))),
        L("READ THE ROAD BACK, ONE SIGN AT A TIME", 960, 92, "tag", 40, at=0.4),
    ], chapter="Reading the Road", beat="read the road back: Antwerp, seven days, one lift, drop zones, Bedell Smith, Nijmegen, Grave, Nijmegen standing, Lent")
    LEDGER(1803.37, [("A1 Antwerp first", 0), ("A2 Two lifts on day one", 0), ("A3 Drop near the bridge", 0), ("A4 More strength at Arnhem", 0), ("A5 Nijmegen bridge, day one", 0)],
           [("G1 Grave left standing", 0), ("G2 Nijmegen left standing", 0)],
           extra=[L("+ 1 BLANK: LENT", 960, 1000, "dark", 40, at=3.0)], beat="five Allied, two German, one nobody can settle")
    scene(1808.23, STUDY, [
        A("host", 960, 900, 1.7, "idle", "determined", talk=True),
        HEAD("HERE'S OUR VERDICT", 960, 180, 100, at=2.6, accent="VERDICT"),
    ], beat="was Market Garden completely avoidable? here's our verdict")
    scene(1812.53, {"kind": "studio", "color": "#d9cdb0"}, [
        HEAD("AVOIDABLE", 960, 180, 120, at=0.2, accent="AVOIDABLE"),
        L("— BUT NOT BY ONE HEROIC DECISION", 960, 290, "plain", 44, at=1.6),
        L("EVERY BRIDGE", 480, 520, "tag", 50, at=4.2), L("EVERY DAY", 960, 520, "tag", 50, at=5.0), L("EVERY RADIO", 1440, 520, "tag", 50, at=5.8),
        ST("NO SPARE TIME", 960, 780, 8.0, size=90),
    ], beat="the defeat was avoidable but not by one heroic decision; no spare time built in")
    ROAD(1825.9, p_for("A2") - 0.02, p_for("A5"), move=(0.3, 14.0), extra=[
        A("host", 1720, 1010, 1.2, "explain", "determined", talk=True),
        L("ANY ONE OF THESE MIGHT HAVE BEEN ENOUGH", 960, 92, "tag", 40, at=11.0),
    ], beat="two lifts, closer drop zones, Bedell Smith's advice, Nijmegen bridge the first evening")
    scene(1840.61, STUDY, [
        A("host", 960, 900, 1.7, "count", "determined", talk=True, keys=K((3.6, {"pose": "stop", "expr": "sad"}))),
        L("THE ALLIES NEEDED ONLY ONE", 960, 140, "tag", 46, at=1.8),
        ST("THEY TOOK NONE", 960, 300, 4.4, size=90),
    ], beat="the Allies needed only one; they took none")

    # =============== CH15 LUCK, BLAME AND THE BILL ===============
    scene(1846.15, {"kind": "paper"}, [
        {"kind": "timeline", "x": 960, "y": 600, "width": 1500, "items": [{"label": "SS sent to Arnhem", "sub": "3 SEPT", "at": 0.05, "in": 0.6, "color": "GER"}, {"label": "Plan approved", "sub": "10 SEPT", "at": 0.5, "in": 1.4, "color": "UK"}]},
        HEAD("NOBODY'S FAULT: THE LUCK", 960, 200, 80, at=0.2, accent="LUCK"),
        L("NO TRAITOR PUT THEM THERE", 960, 900, "red", 44, at=6.8),
    ], chapter="Luck, Blame and the Bill", beat="what wasn't anyone's fault was the luck; no traitor put them there")
    scene(1854.89, {"kind": "archbridge", "time": "day"}, [
        A("ss_soldier", 1400, 920, 1.5, "shrug", "nervous"),
        L("THE GERMANS MADE MISTAKES TOO", 960, 110, "tag", 42, at=0.4),
        L("TWO GREAT BRIDGES LEFT STANDING", 960, 200, "dark", 42, at=3.0),
    ], beat="the Germans too made mistakes: two great bridges left standing")
    scene(1863.11, STUDY, [
        A("host", 960, 900, 1.7, "shrug", "neutral", talk=True),
        L("HISTORIANS DON'T AGREE ON WHERE THE WEIGHT LIES", 960, 130, "tag", 40, at=0.4),
    ], beat="to be fair, historians don't agree on where the weight lies")
    scene(1867.52, {"kind": "paper"}, [
        DOC("book", "US ARMY OFFICIAL HISTORY (1963)", ["THE PLAN DREW LITTLE CRITICISM.", "ITS HANDICAPS COULD HAVE BEEN", "OVERCOME — IF THE GROUND COLUMN", "HAD MOVED AS FAST AS HORROCKS HOPED."], x=960, y=540, w=1350, h=640, at=0.2, size=44, speed=30),
    ], beat="the 1963 American official history: the plan drew little criticism; the ground column was too slow")
    scene(1881.46, {"kind": "studio", "color": "#d9cdb0"}, [
        L("MANY LATER WRITERS: THE PLAN", 960, 120, "tag", 44, at=0.2),
        PROP("crate", 480, 560, 1.2, at=2.0, text="DROP ZONES 13 KM"), L("DISTANT DROP ZONES", 480, 760, "tag", 34, at=2.0),
        PROP("clock", 960, 560, 1.4, at=3.6), L("ONE LIFT A DAY", 960, 760, "tag", 34, at=3.6),
        PROP("radio", 1440, 560, 1.6, at=5.2), L("THE RADIOS", 1440, 760, "tag", 34, at=5.2),
    ], beat="many later writers blame the plan: the drop zones, the single lift, the radios")
    scene(1888.84, {"kind": "field", "road": False, "houses": False, "trees": "pine", "fg": "sandbags"}, [
        {"kind": "crowd", "who": ["german_soldier", "german_pilot", "uboat_captain", "ss_soldier"], "count": 6, "spacing": 260, "x": 960, "y": 900, "scale": 1.1, "pose": "hold", "expr": "determined"},
        L("OTHERS: HOW FAST THE GERMANS RECOVERED", 960, 110, "tag", 40, at=0.4),
        L("\"A CRUST\" — STRAGGLERS AND TRAINING BATTALIONS", 960, 210, "plain", 40, at=4.6),
        L("IN LESS THAN TWO WEEKS", 960, 300, "red", 40, at=8.0),
    ], beat="others stress the German recovery: a crust of stragglers and training battalions in under two weeks")
    scene(1898.76, {"kind": "podium", "flag": "UK"}, [
        A("montgomery", 960, 900, 1.6, "show", "smug", holds="sign", holdsText="90%", holdsScale=0.9, keys=K((4.0, {"pose": "idle", "expr": "sad"}))),
        L("LATER, SOMETHING CLOSER TO THE TRUTH", 960, 120, "tag", 40, at=4.6),
    ], beat="Montgomery, who called it 90% successful, later admitted something closer to the truth")
    scene(1906.86, {"kind": "paper"}, [
        DOC("book", "MONTGOMERY, MEMOIRS", ["\"IT WAS A BAD MISTAKE ON MY PART.", "I UNDERESTIMATED THE DIFFICULTIES", "OF OPENING UP THE APPROACHES", "TO ANTWERP.\""], x=960, y=540, w=1350, h=620, at=0.1, size=48, speed=30),
    ], beat="it was a bad mistake on my part; I underestimated the difficulties of opening Antwerp")
    scene(1913.52, {"kind": "office", "flag": UK, "portrait": False, "desk": False}, [
        A("browning", 700, 900, 1.5, "talk", "worried", talk=True),
        A("montgomery", 1300, 900, 1.5, "cross", "neutral"),
        L("\"A BRIDGE TOO FAR?\"", 960, 140, "plain", 60, at=0.6),
        L("USUALLY CREDITED TO BROWNING", 960, 250, "tag", 38, at=2.4),
    ], tint="sepia", beat="that famous line, a bridge too far, usually credited to Browning")
    scene(1921.0, {"kind": "field", "road": True, "houses": False}, [
        V("jeep", 760, 900, 1.0, UK),
        A("host", 1350, 900, 1.6, "hold", "neutral", holds="paper", talk=True, keys=K((4.0, {"x": 980}), (4.6, {"pose": "idle"}))),
        L("NOTHING WRITTEN DOWN AT THE TIME", 960, 120, "tag", 40, at=0.4),
        ST("GLOVEBOX · UNSIGNED", 960, 280, 5.6, size=70, color="#5a5048"),
    ], beat="we couldn't pin it down, so it stays in the glovebox, unsigned")
    scene(1928.64, {"kind": "memorial"}, [
        PROP("candle", 760, 760, 1.6), PROP("candle", 1160, 760, 1.6),
        L("THE BILL", 960, 140, "plain", 70, at=0.2, color="white"),
        CNT(0, 12000, 960, 360, 1.6, prefix="~", suffix=" AIRBORNE CASUALTIES", size=70, dur=2.0, color="white"),
        CNT(0, 7000, 960, 500, 7.4, prefix="> ", suffix=" BRITISH AIRBORNE", size=56, dur=1.6, color="white"),
        L("+ THOUSANDS MORE IN THE GROUND CORPS", 960, 980, "plain", 40, at=14.0, color="white"),
    ], tint="grey", ambience=None, beat="the bill: ~12,000 airborne casualties; British airborne > 7,000; thousands more")
    scene(1946.46, {"kind": "memorial"}, [
        PROP("candle", 960, 760, 1.6),
        CNT(0, 3300, 960, 400, 0.4, prefix="~", suffix=" GERMAN CASUALTIES AROUND ARNHEM", size=56, dur=1.6, color="white"),
        L("AND THE DUTCH PAID", 960, 980, "plain", 46, at=7.6, color="white"),
    ], tint="grey", ambience=None, beat="a German signal reported ~3,300 casualties; and the Dutch paid")
    scene(1954.62, {"kind": "city", "ruined": True, "time": "night"}, [
        FX("fire", 600, 640), FX("smoke", 620, 520), FX("fire", 1400, 600), FX("smoke", 1400, 480),
        L("EINDHOVEN · BOMBED BY THE LUFTWAFFE", 960, 120, "tag", 40, at=0.4),
        CNT(0, 200, 960, 260, 1.6, prefix="> ", suffix=" KILLED", size=70, dur=1.2),
    ], tint="grey", beat="Eindhoven was bombed during the battle; more than 200 killed")
    scene(1961.6, {"kind": "railway"}, [
        V("train", 600, 900, 0.8, "NED"),
        A("dutch_civilian", 1300, 920, 1.5, "cross", "determined"),
        L("DUTCH RAILWAY WORKERS STRIKE", 960, 120, "tag", 42, at=0.4),
        ST("FOOD SHIPMENTS STOPPED", 960, 300, 4.4, size=60),
    ], beat="Dutch railway workers struck; the occupiers stopped food shipments")
    scene(1969.0, {"kind": "city", "time": "dawn", "weather": "snow"}, [
        {"kind": "crowd", "who": ["dutch_civilian", "dutch_woman", "civilian_man"], "count": 5, "spacing": 200, "x": 960, "y": 930, "scale": 1.1, "pose": "idle", "expr": "sad"},
        L("THE HUNGER WINTER", 960, 120, "plain", 64, at=0.4),
        CNT(0, 20000, 960, 320, 2.4, prefix="> ", suffix=" STARVED TO DEATH", size=70, dur=2.0),
    ], tint="grey", ambience="wind_cold", beat="in the hunger winter more than 20,000 Dutch civilians starved")
    scene(1977.74, {"kind": "harbor"}, [
        V("freighter", -500, 760, 0.6, UK, keys=K((6.4, {"x": 900}))),
        L("ANTWERP · FIRST CONVOY", 960, 120, "tag", 42, at=0.4),
        L("THE PORT THAT COULD HAVE OPENED IN SEPTEMBER", 960, 220, "plain", 38, at=1.6),
    ], date="28 NOVEMBER 1944", sfx=[{"t": 4.0, "id": "ship_horn"}], beat="Antwerp received its first convoy on 28 November")
    scene(1984.29, {"kind": "office", "flag": "NED", "portrait": False, "desk": False}, [
        A("bernhard", 960, 900, 1.6, "idle", "sad", talk=True),
        NC("Prince Bernhard of the Netherlands", "reported remark", at=0.4),
        L("\"MY COUNTRY CAN NEVER AGAIN AFFORD THE\nLUXURY OF ANOTHER MONTGOMERY SUCCESS\"", 960, 150, "plain", 42, at=1.6),
    ], beat="Prince Bernhard: his country could never again afford another Montgomery success")
    ROAD(1994.41, p_for("L"), p_for("L"), move=(0.2, 0.4), extra=[
        A("host", 1700, 1010, 1.25, "offer", "neutral", talk=True, keys=K((6.0, {"pose": "chin"}))),
        L("AT LENT, 20 SEPT, NIGHT:", 960, 100, "tag", 40, at=2.8),
        L("SEND THE FOUR TANKS ON — OR HOLD UNTIL MORNING?", 960, 180, "red", 38, at=4.0),
    ], beat="that's our reading of the road; what's yours? at Lent would you have sent the tanks on?")
    scene(2005.78, STUDY, [
        A("aide", 700, 900, 1.6, "thumbsup", "happy"),
        A("host", 1250, 900, 1.6, "present", "smile", talk=True, keys=K((6.0, {"pose": "thumbsup"}))),
        L("WHICH SIGN WOULD YOU HAVE PAINTED?", 960, 120, "tag", 42, at=0.6),
        L("SUBSCRIBE — ONE LIFT, NO WAITING FOR DAY TWO", 960, 220, "green", 36, at=7.4),
    ], beat="tell us in the comments, and subscribe: it's one lift, no waiting for the second day")
    scene(2017.64, {"kind": "archbridge", "time": "day"}, [
        *[V("bomber", -400 - i * 400, 160 + i * 60, 0.35, US, keys=K((6.0, {"x": 2300 - i * 400, "ease": "linear"}))) for i in range(3)],
        *[{"kind": "burst", "x": 700 + i * 300, "y": 540, "in": 4.0 + i * 0.6, "size": 0.8} for i in range(3)],
        L("THE ARNHEM BRIDGE DIDN'T SURVIVE THE WAR", 960, 980, "tag", 40, at=0.4),
    ], date="7 OCTOBER 1944", camera=[{"t": 0, "zoom": 1.0}, {"t": 4.0, "zoom": 1.0, "shake": 6}, {"t": 6.0, "zoom": 1.02, "shake": 0}], beat="7 Oct 1944 American bombers destroyed it")
    scene(2027.12, {"kind": "archbridge", "time": "dawn", "label": "John Frost Bridge"}, [
        L("REBUILT AFTER THE WAR", 960, 980, "tag", 40, at=0.4),
        L("NAMED SINCE 1977", 960, 900, "plain", 40, at=4.2),
    ], camera=[{"t": 0, "zoom": 1.0}, {"t": 9, "zoom": 1.08}], ambience="wind", beat="since 1977 it carries the name of the man who held it: the John Frost Bridge")
    scene(2037.2, {"kind": "study", "desk": False, "portrait": False, "shelf": True, "lamp": True, "fg": "officedesk"}, [
        A("host", 560, 900, 1.7, "write", "neutral"),
        DOC("note", "DISPATCHER'S LOG — FINAL ENTRY", ["PLANNED ARRIVAL AT ARNHEM: DAY 2 OR 3", "ACTUAL ARRIVAL: NEVER", "CLOSE THE LOG."], x=1330, y=400, w=1000, h=440, at=0.2, size=40, speed=22),
    ], transition="fade", beat="final entry: planned arrival day two or three; actual arrival never; close the log")
