from lib import *
from part1 import STUDY, tanks, UK, US, GE


def build():
    # =============== CH5 SEVEN DAYS TO PLAN ===============
    scene(384.64, {"kind": "airfield", "nation": UK, "planes": 0}, [
        V("dakota", 1250, 820, 0.95, US),
        A("montgomery", 100, 920, 1.4, "idle", "determined", holds="folder", keys=K((5.0, {"x": 800}))),
    ], chapter="Seven Days to Plan", date="10 SEPTEMBER 1944", place="BRUSSELS AIRPORT", transition="dip",
        sfx=[{"t": 0.2, "id": "footsteps", "dur": 4.6}], beat="10 Sept Montgomery meets Eisenhower inside the Supreme Commander's plane")
    scene(391.92, {"kind": "cabin"}, [
        A("eisenhower", 1400, 900, 1.5, "cross", "worried"),
        A("montgomery", 600, 900, 1.5, "hold", "angry", holds="paper", talk=True,
          keys=K((2.4, {"pose": "slam", "expr": "rage"}), (5.0, {"pose": "point"}), (8.6, {"pose": "idle", "expr": "angry", "talk": False}))),
        FX("sparks", 700, 600, **{"in": 2.6, "color": "#fbf8f0"}),
        L("NOT A CALM MEETING", 960, 110, "tag", 44, at=0.4),
    ], sfx=[{"t": 2.6, "id": "paper"}, {"t": 2.9, "id": "paper"}],
        beat="Montgomery tore up Eisenhower's messages and demanded priority")
    scene(400.0, {"kind": "cabin"}, [
        A("eisenhower", 1200, 900, 1.6, "stop", "angry", talk=True),
        A("montgomery", 600, 900, 1.5, "point", "angry", keys=K((1.8, {"pose": "cross", "expr": "smug"}))),
    ], camera=[{"t": 0, "zoom": 1.1, "x": 1100}, {"t": 4, "zoom": 1.15, "x": 1100}], beat="so fierce Eisenhower had to stop him")
    scene(404.16, {"kind": "cabin"}, [
        A("eisenhower", 1200, 900, 1.5, "idle", "neutral", headMove="nod"),
        A("montgomery", 600, 900, 1.5, "hips", "smug"),
        ST("APPROVED", 960, 350, 1.2, size=110, color="green"),
    ], beat="by the end Eisenhower had approved the plan")
    scene(407.92, {"kind": "paper"}, [
        DOC("order", "OPERATION COMET", ["1 BRITISH DIVISION + POLES", "ARNHEM · NIJMEGEN · GRAVE"], x=560, y=480, w=760, h=380, at=0.2, size=40, speed=34, stamp="CANCELLED", out=3.0),
        DOC("order", "OPERATION MARKET GARDEN", ["3½ AIRBORNE DIVISIONS", "+ XXX CORPS"], x=1300, y=600, w=900, h=460, at=3.2, size=48, speed=30, enter="grow"),
        L("BIGGER · BOLDER · NEW NAME", 1300, 160, "tag", 44, at=5.6),
    ], date="10 SEPTEMBER 1944", beat="Comet cancelled the same day, reborn bigger with a new name")
    scene(416.46, {"kind": "polder"}, [
        *[V("dakota", -500 - i * 450, 140 + i * 70, 0.42, US, keys=K((6.0, {"x": 2300 - i * 450, "ease": "linear"}))) for i in range(3)],
        {"kind": "paras", "x": 900, "y": 320, "count": 14, "spread": 1300, "fall": 300, "pdur": 6, "in": 0.6},
        L("MARKET = AIRBORNE", 520, 380, "tag", 52, at=0.4),
        *tanks(-300, 1300, 588, 0.38, 6.0, n=3, gap=240),
        L("GARDEN = TANKS", 1400, 760, "green", 52, at=2.0),
    ], beat="Market for the airborne part, Garden for the tanks")
    scene(422.56, {"kind": "office", "flag": US, "portrait": False, "desk": False}, [
        A("eisenhower", 960, 900, 1.6, "explain", "neutral", talk=True),
        ST("PRIORITY — LIMITED", 1450, 330, 1.8, size=70),
    ], beat="priority, but only limited priority")
    scene(426.82, {"kind": "tent", "desk": False, "fg": "officedesk"}, [
        A("montgomery", 960, 900, 1.6, "write", "angry"),
        DOC("letter", "TO EISENHOWER — 11 SEPT", ["WITHOUT FULL PRIORITY:", "NOT BEFORE THE 23RD,", "MAYBE THE 26TH."], x=1460, y=380, w=700, h=420, at=1.0, size=40, speed=22),
    ], beat="Montgomery wrote back: without full priority not before the 23rd, maybe the 26th")
    scene(434.96, {"kind": "paper"}, [
        DOC("letter", "MONTGOMERY, 11 SEPTEMBER 1944", ["\"THIS DELAY WILL GIVE THE ENEMY TIME", "TO ORGANIZE BETTER DEFENSIVE", "ARRANGEMENTS, AND WE MUST EXPECT", "HEAVIER RESISTANCE AND SLOWER", "PROGRESS.\""], x=960, y=540, w=1400, h=700, at=0.1, size=50, speed=26),
        L("A SENTENCE WORTH KEEPING", 960, 70, "red", 40, at=0.1),
    ], beat="the sentence worth keeping")
    scene(443.04, {"kind": "tent"}, [
        A("bedell_smith", 650, 900, 1.5, "offer", "happy", talk=True),
        A("montgomery", 1300, 900, 1.5, "chin", "neutral", keys=K((6.0, {"pose": "cheer", "expr": "happy"}))),
        NC("Lt Gen Walter Bedell Smith", "Eisenhower's Chief of Staff", at=0.4, out=5.0),
        CNT(0, 1000, 960, 230, 1.4, suffix=" TONS A DAY", size=90, dur=1.8),
        L("BY PLANE + AMERICAN TRUCK", 960, 340, "tag", 40, at=3.4),
    ], beat="Eisenhower's chief of staff promises 1,000 tons a day; Montgomery delighted")
    scene(451.16, {"kind": "paper"}, [
        DOC("note", "D-DAY", ["23RD?  26TH?"], x=640, y=520, w=640, h=360, at=0.1, size=60, speed=30),
        {"kind": "shape", "shape": "cross", "x": 640, "y": 560, "in": 1.4, "scale": 1.6},
        HEAD("SUNDAY 17 SEPTEMBER", 1400, 560, 84, at=2.6, accent="17"),
        {"kind": "arrow", "screen": True, "path": [[900, 560], [1020, 560]], "color": "red", "in": 2.2, "dur": 0.5, "width": 20},
    ], beat="pulled the date forward to Sunday the 17th")
    scene(456.7, {"kind": "warroom"}, [
        A("brereton", 500, 900, 1.4, "pointL", "worried", talk=True),
        A("browning", 900, 900, 1.35, "write", "neutral"),
        A("shaef_officer", 1300, 900, 1.35, "typing", "sweat"),
        CNT(7, 0, 1620, 260, 0.4, suffix=" DAYS", size=110, dur=8.0),
        L("LARGEST AIRBORNE OPERATION IN HISTORY", 960, 110, "tag", 42, at=1.0),
        L("EARLIER ONES: WEEKS, MONTHS", 1350, 420, "plain", 40, at=6.4),
    ], sfx=[{"t": 0.5, "id": "typewriter", "dur": 3}, {"t": 0.2, "id": "clock_tick", "dur": 9}], beat="seven days to plan the largest airborne operation; earlier ones took weeks")
    ROAD(466.81, p_for("T") - 0.03, p_for("T"), move=(0.2, 3.4), extra=[
        A("aide", 1350, 1010, 1.25, "hold", "neutral", holds="radio", talk=True),
        A("host", 1700, 1010, 1.25, "think", "neutral", keys=K((3.0, {"pose": "scratch"}))),
    ], beat="AIDE: is that an exit, sir? take more time? HOST: hmm")
    scene(470.3, {"kind": "field", "road": False, "houses": False, "trees": "pine", "fg": "sandbags"}, [
        {"kind": "crowd", "who": ["german_soldier", "ss_soldier"], "count": 5, "spacing": 300, "x": 960, "y": 900, "scale": 1.1, "pose": "carry", "expr": "determined"},
        L("EVERY DAY YOU PLAN = A DAY THEY DIG", 960, 120, "tag", 44, at=0.3),
    ], beat="every day spent planning is a day the Germans spend digging")
    ROAD(473.28, p_for("T"), p_for("T"), move=(0.2, 0.4), extra=[
        A("host", 1700, 1010, 1.25, "shrug", "smug", talk=True),
        ST("NO SIGN", 1100, 300, 2.6, size=90, color="#5a5048"),
        L("A TOLL EITHER WAY", 1100, 140, "tag", 44, at=0.6),
    ], beat="that's a toll either way; no sign")

    # =============== CH6 CARPET OF PARATROOPERS ===============
    MAP(477.32, [5.68, 51.62], 2.8, [
        *rivers("maas", "waal", "rhine"),
        {"kind": "line", "path": ROUTE, "color": "#6a5a4a", "width": 8, "in": 0.2, "enter": "draw", "dur": 2.4},
        *towns("Neerpelt", "Eindhoven", "Grave", "Nijmegen", "Arnhem", at=0.6),
        L("ONE ROAD NORTH FROM THE BELGIAN BORDER", 960, 980, "tag", 42, at=3.0, hud=True),
        HEAD("3½ AIRBORNE DIVISIONS", 960, 130, 80, at=5.2, hud=True),
    ], chapter="Carpet of Paratroopers", beat="three and a half airborne divisions along a single road")
    MAP(486.7, [5.68, 51.62], 2.8, [
        *rivers("maas", "waal", "rhine"), {"kind": "line", "path": ROUTE, "color": "#6a5a4a", "width": 8, "enter": "none"},
        *towns("Eindhoven", "Son", "Veghel", "Grave", "Nijmegen", "Arnhem", at=0.0),
        {"kind": "ring", "at": [5.50, 51.52], "km": 9, "color": "USA", "in": 0.3, "enter": "grow"},
        ML("101ST AIRBORNE (US)", [5.25, 51.52], style="tag", at=0.6),
        {"kind": "ring", "at": [5.84, 51.79], "km": 9, "color": "USA", "in": 4.2, "enter": "grow"},
        ML("82ND AIRBORNE (US)", [6.15, 51.74], style="tag", at=4.4),
        ML("HIGH GROUND", [5.95, 51.77], style="map", at=8.6),
        {"kind": "ring", "at": [5.84, 51.99], "km": 8, "color": "UK", "in": 11.4, "enter": "grow"},
        ML("1ST AIRBORNE (UK)\n+ POLISH BRIGADE", [5.55, 52.04], style="tag", at=11.8),
        ML("THE FARTHEST", [5.91, 52.06], style="red", at=17.6),
    ], camera=[{"t": 0, "zoom": 1.3, "center": [5.55, 51.55]}, {"t": 4, "zoom": 1.3, "center": [5.55, 51.55]}, {"t": 5, "zoom": 1.3, "center": [5.8, 51.8]}, {"t": 11, "zoom": 1.3, "center": [5.8, 51.8]}, {"t": 12, "zoom": 1.3, "center": [5.85, 51.95]}],
        beat="101st at Eindhoven, 82nd at Grave and Nijmegen, British 1st + Poles at Arnhem")
    MAP(508.11, [5.68, 51.62], 2.8, [
        *rivers("maas", "waal", "rhine"), *towns("Neerpelt", "Eindhoven", "Grave", "Nijmegen", "Arnhem", at=0.0),
        *[{"kind": "ring", "at": c, "km": 8, "color": "USA" if i < 2 else "UK", "enter": "none", "dashed": False} for i, c in enumerate([[5.50, 51.52], [5.84, 51.79], [5.84, 51.99]])],
        {"kind": "arrow", "path": ROUTE + [[5.95, 52.12]], "color": "UK", "width": 30, "in": 1.0, "dur": 8.0},
        ML("XXX CORPS", [5.25, 51.30], style="tag", at=0.6),
        L("ACROSS A CARPET OF PARATROOPERS", 960, 980, "tag", 42, at=5.0, hud=True),
    ], beat="then XXX Corps' tanks drive up that road across the carpet, cross the Rhine, keep going")
    scene(519.41, {"kind": "polder", "dyke": 600}, [
        *tanks(-300, 1100, 578, 0.36, 9.0, n=3, gap=260, ease="linear"),
        V("tank", 1500, 760, 0.6, UK, rotate=-10, keys=K((5.0, {"y": 800, "rotate": -16}))),
        FX("splash", 1500, 780, **{"in": 1.0}),
        L("POLDER", 480, 220, "map", 54, at=0.4),
        L("THE ROAD: RAISED LIKE A CAUSEWAY", 1200, 160, "tag", 42, at=3.2),
        L("TANKS THAT LEFT IT SANK", 1500, 980, "red", 44, at=8.6),
    ], beat="it really was one road: polder, ditches, dykes; tanks that left it sank")
    scene(529.96, {"kind": "tent", "desk": False}, [
        A("horrocks", 600, 900, 1.6, "pointL", "determined", talk=True, keys=K((4.0, {"pose": "explain"}))),
        {"kind": "crowd", "who": ["guards_tanker", "british_soldier"], "count": 3, "spacing": 200, "x": 1450, "y": 930, "scale": 1.1, "pose": "idle", "expr": "neutral"},
        NC("Lt Gen Brian Horrocks", "XXX Corps", at=0.4),
        CNT(0, 20000, 1350, 250, 2.6, suffix=" VEHICLES", size=84, dur=1.6),
        L("IN 60 HOURS", 1350, 360, "red", 50, at=4.6),
    ], beat="Horrocks: 20,000 vehicles up that road in 60 hours")
    scene(537.92, {"kind": "corridor", "doors": ["XXX CORPS", "LIAISON"]}, [
        A("horrocks", 700, 900, 1.6, "chin", "worried", talk=True, keys=K((5.6, {"pose": "think"}))),
        A("us_para", 1350, 900, 1.4, "write", "neutral", holds="paper"),
        L("AN AMERICAN LIAISON OFFICER HEARD:", 960, 110, "plain", 40, at=0.4),
        L("\"HOW MANY DAYS' RATIONS\nWILL THEY JUMP WITH?\"", 700, 260, "plain", 44, at=5.4),
        L("\"HOW LONG CAN\nTHEY HOLD OUT?\"", 1250, 320, "plain", 44, at=8.0),
    ], beat="in private Horrocks asked how many days' rations, how long can they hold")
    scene(548.24, {"kind": "airfield", "nation": UK, "planes": 0}, [
        *[V("dakota", 300 + i * 600, 760, 0.6, US) for i in range(3)],
        {"kind": "crowd", "who": ["british_para", "us_para"], "count": 4, "spacing": 130, "x": 520, "y": 960, "scale": 0.95, "pose": "idle", "expr": "determined", "walk": True, "keys": K((6, {"x": 900}))},
        {"kind": "crowd", "who": ["british_para", "us_para"], "count": 4, "spacing": 130, "x": 1550, "y": 960, "scale": 0.95, "pose": "pockets", "expr": "sad"},
        L("FLIES TODAY", 700, 330, "green", 44, at=1.4), L("WAITS", 1550, 330, "dark", 44, at=2.2),
        L("PLANES FOR ONLY HALF AT ONCE", 960, 110, "tag", 44, at=0.4),
    ], beat="only enough planes to carry about half the airborne troops at once")
    scene(555.34, {"kind": "warroom"}, [
        A("gavin", 600, 900, 1.45, "talk2", "determined", talk=True),
        A("roy_urquhart", 1000, 900, 1.45, "point", "determined"),
        A("brereton", 1500, 900, 1.45, "cross", "neutral"),
        L("DIVISION COMMANDERS: 2 LIFTS ON DAY ONE", 960, 110, "tag", 42, at=0.6),
    ], beat="division commanders asked for two flights on the first day")
    scene(563.12, {"kind": "airfield", "nation": UK, "planes": 0}, [
        V("dakota", 900, 780, 0.9, US),
        A("worker", 600, 930, 1.3, "rub", "tired"),
        A("american_pilot", 1450, 930, 1.4, "stop", "tired", talk=True),
        L("TROOP CARRIER COMMANDERS: REFUSED", 960, 110, "red", 42, at=0.4),
        L("NO TIME FOR REPAIRS", 600, 330, "tag", 40, at=2.6), L("EXHAUSTED CREWS", 1450, 330, "tag", 40, at=4.6),
    ], beat="troop carrier commanders refused: no time for repairs, exhausted crews")
    scene(569.9, {"kind": "office", "flag": US, "portrait": False, "desk": False, "fg": "officedesk"}, [
        A("brereton", 960, 900, 1.6, "slam", "determined", talk=True),
        ST("ONE LIFT A DAY", 1500, 330, 1.0, size=80),
        CNT(0, 4, 960, 230, 2.4, suffix=" DAYS TO DELIVER EVERYBODY", size=64, dur=1.2),
    ], beat="Brereton sided with the airmen: one lift a day, four days")
    MAP(575.9, [5.86, 51.98], 0.55, [
        *rivers("rhine"), *towns("Arnhem", "Oosterbeek", at=0.2),
        {"kind": "city", "name": "Road bridge", "at": [5.912, 51.976], "side": "bottom", "in": 1.0},
        L("FOR ARNHEM: MULTIPLIED BY GEOGRAPHY", 960, 110, "tag", 42, at=1.0, hud=True),
    ], beat="for the British at Arnhem the decision was multiplied by geography")
    scene(580.52, {"kind": "tent", "desk": False}, [
        A("roy_urquhart", 960, 900, 1.65, "pointUp", "determined", talk=True, keys=K((3.6, {"pose": "explain"}))),
        NC("Maj Gen Roy Urquhart", "1st British Airborne Division", at=0.4),
        L("LAND CLOSE TO THE BRIDGE", 960, 130, "tag", 48, at=2.6),
    ], beat="Urquhart wanted landing zones close to the bridge")
    MAP(586.1, [5.88, 51.97], 0.4, [
        *rivers("rhine"), *towns("Arnhem", at=0.0),
        *[ML("FLAK", c, style="red", size=30, at=0.3 + i * 0.4) for i, c in enumerate([[5.90, 51.99], [5.93, 51.985], [5.92, 52.0], [5.88, 51.995]])],
        {"kind": "region", "polygon": [[5.84, 51.96], [5.96, 51.965], [5.96, 51.94], [5.84, 51.94]], "color": "#7f9a52", "in": 3.6},
        ML("SOUTH BANK: TOO SOFT,\nCUT UP BY DYKES", [5.90, 51.945], style="tag", at=4.0),
    ], beat="the city full of AA guns; south bank too soft and cut up by dykes")
    MAP(593.92, [5.83, 51.985], 0.5, [
        *rivers("rhine"), *towns("Arnhem", "Oosterbeek", at=0.0),
        *[{"kind": "ring", "at": c, "r": 50, "color": "UK", "in": 0.2 + i * 0.4, "enter": "grow", "dashed": False} for i, c in enumerate([[5.74, 52.0], [5.76, 51.99], [5.73, 51.995]])],
        ML("HEATHLAND DROP ZONES", [5.74, 52.02], style="tag", at=1.0),
        {"kind": "route", "path": [[5.75, 51.99], [5.82, 51.985], [5.912, 51.976]], "color": "UK", "in": 2.6, "dur": 1.8},
        ML("UP TO 13 KM", [5.83, 51.975], style="red", at=4.2),
    ], beat="the drop zones went in heathland west of Arnhem, up to 13 km from the bridge")
    scene(600.08, {"kind": "heath"}, [
        *[V("glider", 300 + i * 700, 760, 0.5, UK) for i in range(3)],
        {"kind": "crowd", "who": ["british_para", "british_para_helmet"], "count": 4, "spacing": 200, "x": 600, "y": 930, "scale": 1.05, "pose": "hold", "expr": "determined"},
        L("STAY: GUARD THE FIELDS", 600, 330, "dark", 40, at=1.6),
        {"kind": "crowd", "who": ["british_para"], "count": 3, "spacing": 140, "x": 1350, "y": 940, "scale": 1.0, "walk": True, "expr": "determined", "keys": K((9, {"x": 2100}))},
        L("FOR THE SECOND LIFT", 600, 420, "tag", 36, at=5.4),
    ], beat="half the half that landed first had to stay and guard the fields")
    scene(609.54, {"kind": "heath", "panels": False}, [
        {"kind": "crowd", "who": ["british_para", "british_para_helmet", "frost"], "count": 6, "spacing": 170, "x": 200, "y": 940, "scale": 1.0, "walk": True, "expr": "determined", "keys": K((3.4, {"x": 1100}))},
        L("DAY ONE: ONE BRIGADE WALKS TO THE BRIDGE", 960, 120, "tag", 42, at=0.2),
    ], sfx=[{"t": 0, "id": "footsteps", "dur": 3.4}], beat="on day one, one brigade would walk to the bridge")
    ROAD(612.99, p_for("A3") - 0.06, p_for("A3") - 0.05, move=(0.2, 6.0), extra=[
        A("aide", 1350, 1010, 1.25, "show", "worried", holds="radio", talk=True),
        A("host", 1700, 1010, 1.25, "write", "neutral", holds="paper", keys=K((5.0, {"headMove": "nod"}))),
        L("\"MY SET REACHES ~5 KM.\nTHE BRIDGE IS 13 AWAY.\"", 1100, 130, "plain", 44, at=0.6),
    ], beat="AIDE: my set reaches about 5 km, the bridge is 13 away. HOST: noted")
    MAP(620.43, [5.83, 51.985], 0.5, [
        *rivers("rhine"), *towns("Arnhem", "Oosterbeek", at=0.0),
        {"kind": "ring", "at": [5.75, 51.995], "km": 5, "color": "#2f7a3a", "in": 0.6, "enter": "grow", "dashed": False},
        ML("TYPE 22 SET: ~5 KM", [5.75, 52.04], style="green", at=1.2),
        {"kind": "city", "name": "Bridge", "at": [5.912, 51.976], "side": "right", "in": 0.2},
        {"kind": "shape", "shape": "cross", "x": 1500, "y": 640, "in": 4.0, "scale": 0.8, "hud": True},
        L("OUT OF RANGE", 1500, 760, "red", 40, at=4.4, hud=True),
    ], beat="the Type 22 set: effective range about 5 km")
    scene(627.93, STUDY, [
        A("aide", 760, 900, 1.6, "show", "neutral", holds="radio"),
        A("host", 1200, 900, 1.6, "pointL", "smug", talk=True),
        L("REMEMBER THAT RADIO", 960, 130, "tag", 50, at=0.4),
    ], beat="remember that radio, it keeps coming back")
    ROAD(630.89, p_for("A2") - 0.03, p_for("A3") + 0.02, move=(0.4, 11.0), extra=[
        A("host", 1700, 1010, 1.25, "explain", "determined", talk=True, keys=K((4.0, {"pose": "pointL"}), (9.6, {"pose": "present", "expr": "smug"}))),
        L("TWO EXITS — BOTH IN ENGLAND", 960, 92, "tag", 44, at=3.2),
    ], beat="which exits? two, both in England: one lift a day, distant drop zones. That's three")
    LEDGER(645.49, [("A1 Antwerp first", 383.6), ("A2 Two lifts on day one", 646.0), ("A3 Drop near the bridge", 646.6)], [], beat="Allied column: three")

    # =============== CH7 THE GERMANS NEXT DOOR ===============
    ROAD(647.69, p_for("A3"), p_for("A3"), move=(0.2, 0.4), extra=[
        A("host", 1750, 1010, 1.25, "idle", "determined", talk=True, keys=K((3.8, {"x": 300}))),
        L("THE GERMANS WERE MAKING PLANS TOO", 960, 92, "tag", 44, at=1.0),
    ], chapter="The Germans Next Door", sfx=[{"t": 0.1, "id": "footsteps", "dur": 3.6}], beat="cross to the other side of the road")
    scene(655.61, {"kind": "office", "portrait": False, "desk": False, "fg": "officedesk", "map": "WEST"}, [
        A("model", 960, 900, 1.6, "write", "neutral"),
        NC("Field Marshal Walter Model", "Army Group B", at=0.6),
        L("A ROUTINE DECISION", 960, 110, "tag", 44, at=4.6),
    ], date="3 SEPTEMBER 1944", beat="3 Sept, a week before Market Garden existed, Model makes a routine decision")
    MAP(665.13, [5.4, 51.5], 3.6, [
        *rivers("waal", "rhine"), *towns("Arnhem", at=0.0),
        {"kind": "arrow", "path": [[4.0, 50.5], [5.0, 51.2], [5.85, 52.05]], "color": "GER", "in": 0.6, "dur": 2.4},
        {"kind": "arrow", "path": [[4.6, 50.3], [5.6, 51.2], [6.05, 52.0]], "color": "GER", "in": 1.2, "dur": 2.4},
        {"kind": "unit", "type": "armor", "nation": "GER", "label": "9TH SS PZ", "at": [5.8, 52.1], "in": 3.4},
        {"kind": "unit", "type": "armor", "nation": "GER", "label": "10TH SS PZ", "at": [6.15, 52.06], "in": 3.8},
        L("BATTERED · SENT TO REST AND REFIT", 960, 980, "tag", 42, at=5.0, hud=True),
    ], beat="two battered SS panzer divisions sent near Arnhem to rest and refit")
    scene(675.89, {"kind": "field", "road": True, "houses": True, "trees": "round"}, [
        V("car", -200, 900, 0.8, "GER", moving=True, keys=K((3.2, {"x": 700}))),
        A("bittrich", 1300, 900, 1.6, "hips", "determined", **{"in": 3.0, "enter": "fade"}),
        NC("Gen Wilhelm Bittrich", "II SS Panzer Corps", at=3.2),
    ], date="5 SEPTEMBER 1944", beat="two days later the corps HQ under Bittrich joins them")
    scene(681.72, {"kind": "studio", "color": "#2c2a28"}, [
        L("HOHENSTAUFEN", 600, 200, "dark", 60, at=0.2), L("FRUNDSBERG", 1350, 200, "dark", 60, at=1.0),
        {"kind": "crowd", "who": ["ss_soldier", "german_soldier"], "count": 5, "spacing": 260, "x": 960, "y": 930, "scale": 1.1, "pose": "idle", "expr": "tired", "in": 3.4, "enter": "fade"},
        L("SHADOWS OF THEMSELVES AFTER NORMANDY", 960, 400, "plain", 44, at=4.2, color="white"),
    ], tint="grey", beat="famous names, shadows of themselves")
    scene(688.8, {"kind": "field", "road": False, "houses": False, "trees": "pine"}, [
        {"kind": "crowd", "who": ["ss_soldier"], "count": 4, "spacing": 180, "x": 960, "y": 930, "scale": 1.1, "pose": "idle", "expr": "tired"},
        CNT(0, 7000, 960, 240, 0.6, prefix="~6,000–", suffix=" MEN", size=90, dur=1.6),
        L("THE WHOLE CORPS · A FRACTION OF PROPER STRENGTH", 960, 360, "tag", 38, at=3.4),
    ], beat="the whole corps perhaps six or seven thousand men")
    scene(696.77, {"kind": "railway"}, [
        V("train", 300, 900, 0.8, "GER"),
        A("ss_soldier", 1100, 930, 1.3, "carry", "tired", holds="crate", keys=K((4.0, {"x": 800}))),
        A("german_soldier", 1500, 930, 1.3, "carry", "neutral", holds="crate", keys=K((4.0, {"x": 1150}))),
        L("PACKING FOR GERMANY", 960, 120, "tag", 46, at=0.6),
    ], beat="some units already packing to leave for Germany")
    scene(705.0, {"kind": "hotel", "name": "Hotel Tafelberg"}, [
        A("model", 300, 930, 1.3, "idle", "smug", keys=K((3.0, {"x": 900}))),
        {"kind": "ring", "x": 960, "y": 520, "r": 520, "color": "red", "in": 3.4, "enter": "grow", "dashed": False},
        L("KEEP AN EYE ON THAT HOTEL", 1150, 170, "red", 46, at=3.6),
    ], place="OOSTERBEEK · WEST OF ARNHEM", sfx=[{"t": 0.1, "id": "footsteps", "dur": 3}], beat="Model set up his HQ in a pleasant hotel in Oosterbeek")
    scene(710.07, {"kind": "office", "portrait": False, "desk": False}, [
        A("german_officer", 600, 900, 1.5, "hold", "worried", holds="folder", talk=True, look_={"glasses": "round"}),
        A("model", 1450, 900, 1.5, "cross", "neutral"),
        DOC("order", "INTELLIGENCE — DAILY", ["9–14 SEPT: BRITISH OFFENSIVE COMING", "→ NIJMEGEN · ARNHEM · WESEL", "PRIZE: THE RUHR"], x=1000, y=270, w=900, h=330, at=2.4, size=36, speed=26),
    ], beat="Model's intelligence officer warned every day of a British offensive")
    MAP(724.71, [6.1, 51.8], 3.2, [
        *rivers("waal", "rhine"), *towns("Nijmegen", "Arnhem", "Wesel", at=0.0),
        {"kind": "arrow", "path": [[5.4, 51.2], [5.8, 51.7], [6.5, 51.6], [7.1, 51.45]], "color": "UK", "dashed": True, "in": 0.2, "dur": 1.6},
        {"kind": "shape", "shape": "check", "x": 700, "y": 300, "in": 1.8, "scale": 0.8, "hud": True},
        L("ON THE GROUND: ALMOST EXACTLY RIGHT", 700, 140, "green", 38, at=1.8, hud=True),
        ML("PARATROOPERS?", [7.3, 52.05], style="red", at=4.4),
        {"kind": "shape", "shape": "cross", "x": 1500, "y": 300, "in": 5.6, "scale": 0.8, "hud": True},
        L("AIRBORNE: WRONG PLACE (EAST OF THE RHINE)", 1300, 980, "red", 36, at=6.0, hud=True),
    ], beat="right about the ground attack, wrong about the airborne army")
    scene(732.88, {"kind": "beach"}, [
        A("model", 960, 900, 1.6, "binoculars", "worried", keys=K((6.0, {"pose": "chin"}))),
        {"kind": "bubble", "text": "LANDING CRAFT?", "x": 1200, "y": 520, "thought": True, "in": 2.4},
        L("A SEABORNE INVASION OF NORTHERN HOLLAND?", 960, 120, "tag", 40, at=7.0),
    ], beat="Model became convinced a seaborne invasion of northern Holland was coming")
    scene(745.3, {"kind": "sky", "below": "sea"}, [
        *[V("dakota", -400 - i * 350, 300 + (i % 3) * 140, 0.4, US, keys=K((4.4, {"x": 2300 - i * 350, "ease": "linear"}))) for i in range(6)],
    ], date="17 SEPTEMBER 1944", sfx=[{"t": 0, "id": "plane_engine", "dur": 4.4}], beat="even as the transport planes were in the air on the 17th")
    scene(749.7, {"kind": "warroom"}, [
        A("german_officer", 960, 900, 1.6, "pointUp", "neutral", talk=True),
        ST("STUDY: LANDINGS ON THE DUTCH COAST", 960, 300, 1.6, size=56, color="#5a5048", tilt=-4),
    ], beat="the German C-in-C West was ordering a study of possible landings on the Dutch coast")
    scene(754.64, STUDY, [
        A("host", 960, 900, 1.7, "idle", "determined", talk=True),
        ST("MYTH #1", 1450, 330, 1.4, size=100),
    ], beat="which brings us to the first myth on this road")
    scene(758.12, {"kind": "office", "flag": UK, "portrait": False, "desk": False, "shelf": True}, [
        A("pinto", 960, 900, 1.6, "show", "smug", holds="book", talk=True),
        NC("Lt Col Oreste Pinto", "counter-intelligence officer", at=0.6),
        L("\"MARKET GARDEN WAS BETRAYED\"", 960, 120, "plain", 52, at=3.6),
    ], beat="after the war Oreste Pinto claimed Market Garden had been betrayed")
    scene(765.61, {"kind": "city", "time": "night"}, [
        A("lindemans", 700, 900, 1.6, "talk", "smug", talk=True),
        A("german_officer", 1250, 900, 1.4, "write", "neutral", holds="paper"),
        NC("Christiaan Lindemans", "\"King Kong\" — Dutch resistance", at=0.6),
        L("TOLD THE GERMANS THE PLAN?", 960, 120, "red", 44, at=5.4),
    ], tint="sepia", beat="Lindemans, 'King Kong', supposedly told the Germans the plan")
    scene(776.39, STUDY, [
        A("aide", 700, 900, 1.6, "hold", "worried", holds="radio", talk=True),
        A("host", 1250, 900, 1.6, "idle", "neutral", keys=K((2.0, {"pose": "explain", "talk": True}), (5.4, {"pose": "show", "talk": False})), holds="folder"),
        L("THE TRAITOR MIGHT BE REAL", 960, 110, "tag", 42, at=2.4),
        L("THE BETRAYAL DOESN'T FIT THE TIMETABLE", 960, 200, "red", 40, at=4.0),
    ], beat="AIDE: a traitor? HOST: the traitor might be real; the betrayal doesn't fit the timetable")
    scene(783.51, {"kind": "cell"}, [
        A("lindemans", 960, 900, 1.6, "behind", "sad"),
        L("ARRESTED OCTOBER 1944 · DIED IN HIS CELL 1946", 960, 120, "tag", 40, at=0.6),
        L("A FRENCH HISTORIAN:", 1400, 330, "plain", 38, at=6.2),
        ST("DOUBLE AGENT", 1400, 480, 7.6, size=70),
    ], tint="grey", beat="Lindemans arrested 1944, killed himself 1946; a historian concluded he was a double agent")
    scene(796.39, {"kind": "paper"}, [
        {"kind": "timeline", "x": 960, "y": 560, "width": 1500, "start": "", "end": "",
         "items": [{"label": "SS sent to Arnhem", "sub": "3 SEPT", "at": 0.05, "in": 0.6, "color": "GER"}, {"label": "Plan approved", "sub": "10 SEPT", "at": 0.5, "in": 3.2, "color": "UK"}, {"label": "Landings", "sub": "17 SEPT", "at": 0.95, "in": 4.4, "color": "USA"}]},
        L("A WEEK BEFORE THE PLAN EXISTED", 960, 200, "red", 48, at=4.8),
    ], beat="the SS divisions were ordered to Arnhem a week before the plan existed")
    scene(803.58, {"kind": "warroom"}, [
        A("german_officer", 700, 900, 1.5, "pointUp", "neutral", keys=K((2.6, {"pose": "head", "expr": "shocked"}))),
        PROP("phone", 1300, 820, 1.2, on=True, **{"in": 2.2}),
        L("THE GERMANS WERE SURPRISED", 960, 120, "tag", 44, at=3.0),
    ], sfx=[{"t": 2.2, "id": "phone_ring", "dur": 2}], beat="the Germans were surprised; that morning they were looking at the coast")
    scene(810.66, {"kind": "parliament"}, [
        A("pinto", 960, 900, 1.6, "idle", "nervous", keys=K((3.2, {"pose": "shrug", "expr": "sweat"}))),
        L("DUTCH PARLIAMENTARY COMMISSION · UNDER OATH", 960, 120, "tag", 40, at=0.6),
        L("COULDN'T BACK UP HIS STORY", 960, 260, "red", 46, at=4.0),
    ], beat="a Dutch commission questioned Pinto under oath; he couldn't back it up")
    scene(816.76, {"kind": "paper"}, [
        DOC("book", "US ARMY OFFICIAL HISTORY", ["THE BETRAYAL THEORY:"], x=960, y=520, w=1000, h=520, at=0.2, size=54, speed=26, stamp="BASELESS"),
    ], beat="the American official history calls the betrayal theory baseless")
    scene(821.26, STUDY, [
        A("host", 960, 900, 1.7, "explain", "neutral", talk=True, keys=K((3.0, {"pose": "shrug"}))),
        L("NOT A LEAK", 600, 200, "red", 54, at=0.4),
        L("BAD LUCK + GOOD GERMAN HOUSEKEEPING", 1150, 330, "tag", 42, at=2.6),
    ], beat="the panzers at Arnhem weren't a leak; bad luck and good German housekeeping")
    scene(827.95, STUDY, [
        A("aide", 760, 900, 1.6, "show", "happy", holds="radio"),
        A("host", 1200, 900, 1.6, "thumbsup", "smile", talk=True),
        L("A LIKE ACTUALLY REACHES SOMEBODY", 960, 130, "tag", 44, at=3.0),
    ], beat="if you're enjoying the drive, a like helps; unlike the British radios it reaches somebody")

    # =============== CH8 THE WARNINGS ===============
    scene(835.6, {"kind": "corridor", "doors": ["INTELLIGENCE", "SECRET"]}, [
        A("host", 960, 900, 1.6, "stop", "determined", talk=True),
        ST("THE ALLIES WERE WARNED", 960, 280, 4.4, size=70),
    ], chapter="The Warnings", beat="bad luck somebody warns you about is another; the Allies were warned")
    scene(842.44, {"kind": "radio", "desk": False, "fg": "officedesk", "time": "night"}, [
        A("dutch_civilian", 700, 900, 1.5, "typing", "determined"),
        DOC("telegram", "DUTCH RESISTANCE → LONDON", ["BATTERED PANZER FORMATIONS", "SENT INTO HOLLAND TO REFIT"], x=1350, y=380, w=780, h=380, at=1.6, size=36, speed=24),
        L("10 SEPTEMBER — THE DAY THE PLAN WAS APPROVED", 960, 110, "tag", 38, at=0.4),
    ], sfx=[{"t": 0.2, "id": "morse", "dur": 4}], beat="by the 10th British intelligence passed on Dutch resistance reports of panzers refitting")
    MAP(856.04, [5.98, 51.9], 1.4, [
        *rivers("waal", "rhine"), *towns("Arnhem", "Nijmegen", "Kleve", at=0.0),
        {"kind": "unit", "type": "armor", "nation": "GER", "label": "9TH SS PZ", "at": [5.95, 52.07], "in": 1.4},
        {"kind": "unit", "type": "armor", "nation": "GER", "label": "10TH SS PZ?", "at": [6.14, 51.84], "in": 4.4},
        L("SHAEF INTELLIGENCE NAMES THEM", 960, 110, "tag", 42, at=0.4, hud=True),
        L("A SHORT DRIVE FROM ARNHEM", 960, 980, "red", 42, at=9.4, hud=True),
    ], beat="SHAEF named the 9th SS and probably the 10th, refitting near Kleve")
    scene(869.82, {"kind": "office", "flag": US, "portrait": False, "desk": False}, [
        A("bedell_smith", 800, 900, 1.6, "hold", "worried", holds="telegram", keys=K((4.0, {"pose": "idle", "x": 1600}))),
        L("PERMISSION TO WARN MONTGOMERY", 960, 120, "tag", 42, at=3.0),
    ], sfx=[{"t": 4.2, "id": "footsteps", "dur": 2.6}], beat="it worried Bedell Smith enough to go to Montgomery with a warning")
    scene(878.6, {"kind": "tent"}, [
        A("bedell_smith", 650, 900, 1.5, "explain", "worried", talk=True, keys=K((4.6, {"pose": "talk2"}))),
        A("montgomery", 1350, 900, 1.5, "cross", "neutral"),
        L("DROP A 2ND DIVISION AT ARNHEM", 960, 120, "tag", 42, at=0.6),
        L("OR MOVE A US DIVISION NORTH", 960, 220, "tag", 42, at=4.8),
    ], beat="drop the equivalent of a second division at Arnhem, or move an American division north")
    scene(887.1, {"kind": "tent"}, [
        A("bedell_smith", 650, 900, 1.5, "face", "sad"),
        A("montgomery", 1350, 900, 1.5, "wave", "laugh", talk=True),
        L("\"MONTGOMERY RIDICULED THE IDEA\nAND WAVED MY OBJECTIONS ASIDE\"", 960, 150, "plain", 44, at=2.6),
        L("— BEDELL SMITH, AFTER THE WAR", 1300, 300, "plain", 34, at=4.0),
    ], beat="Montgomery ridiculed the idea and waved his objections aside")
    scene(894.88, {"kind": "tent", "desk": False}, [
        A("us_para", 600, 900, 1.5, "hold", "worried", holds="folder", look_={"glasses": "round"}),
        DOC("order", "CAPTURED GERMAN DOCUMENT", ["COLLECTING STRAGGLERS", "INTO NEW BATTLE GROUPS"], x=1250, y=420, w=820, h=380, at=1.0, size=38, speed=26),
        L("82ND AIRBORNE INTELLIGENCE", 960, 110, "tag", 40, at=0.4),
    ], beat="the 82nd's intelligence officer noted a captured document on gathering stragglers")
    scene(908.76, {"kind": "paper"}, [
        DOC("letter", "82ND AIRBORNE — INTELLIGENCE NOTE", ["\"THE FIGHTING CAPACITY OF THE NEW", "BATTLE GROUPS FORMED FROM THE", "REMNANTS OF BATTERED DIVISIONS", "SEEMS UNIMPAIRED.\""], x=960, y=540, w=1350, h=620, at=0.1, size=48, speed=30),
    ], beat="fighting capacity seems unimpaired")
    scene(914.0, {"kind": "tent", "time": "night", "desk": False, "fg": "officedesk"}, [
        A("gavin", 960, 900, 1.6, "write", "worried"),
        NC("Brig Gen James Gavin", "82nd Airborne Division", at=0.4),
        DOC("note", "GAVIN'S DIARY", ["\"IT LOOKS VERY ROUGH.", "IF I GET THROUGH THIS ONE,", "I WILL BE VERY LUCKY.\""], x=1450, y=380, w=720, h=420, at=4.0, size=38, speed=20),
    ], beat="Gavin's diary: it looks very rough; if I get through this one I will be very lucky")
    scene(929.0, {"kind": "office", "flag": UK, "portrait": False, "desk": False}, [
        A("brian_urquhart", 700, 900, 1.6, "hold", "worried", holds="telegram", keys=K((8.0, {"pose": "phone", "expr": "determined", "talk": True}))),
        NC("Maj Brian Urquhart", "I Airborne Corps intelligence — no relation to the general", at=0.6),
        L("DUTCH RESISTANCE: ARMOUR AROUND ARNHEM", 1300, 260, "tag", 38, at=3.4),
        L("REQUEST: RECONNAISSANCE FLIGHTS", 1300, 380, "green", 38, at=10.2),
    ], beat="Major Brian Urquhart kept hearing of German armour; asked for recon flights")
    scene(943.91, {"kind": "polder"}, [
        V("fighter", -300, 420, 0.9, UK, keys=K((6.0, {"x": 2300, "ease": "linear"}))),
        FX("flash", 900, 520, **{"in": 3.0}),
        L("PHOTO-RECONNAISSANCE SPITFIRE", 960, 120, "tag", 42, at=0.6),
    ], date="12 SEPTEMBER 1944", sfx=[{"t": 0.4, "id": "plane_flyby"}], beat="12 Sept a photo-recon Spitfire came back with pictures of tanks")
    scene(949.91, {"kind": "paper"}, [
        PROP("folder", 960, 560, 3.0, text="ARNHEM · 12 SEPT"),
        V("tank", 1400, 520, 0.35, "GER", **{"in": 1.0}), V("tank", 1550, 640, 0.3, "GER", **{"in": 1.4}),
        L("TANKS IN THE ARNHEM AREA", 960, 120, "red", 46, at=1.8),
    ], beat="pictures that showed tanks near Arnhem")
    scene(954.17, {"kind": "office", "flag": UK, "portrait": False, "desk": False, "fg": "officedesk"}, [
        A("browning", 1300, 900, 1.6, "idle", "neutral"),
        A("brian_urquhart", 300, 900, 1.5, "show", "worried", holds="folder", keys=K((2.4, {"x": 760}))),
        NC("Lt Gen Frederick Browning", "I Airborne Corps", at=2.8),
    ], beat="Urquhart took them to his commander, Browning")
    scene(959.39, {"kind": "office", "flag": UK, "portrait": False, "desk": False, "fg": "officedesk"}, [
        A("browning", 1300, 900, 1.6, "wave", "smug", talk=True),
        A("brian_urquhart", 760, 900, 1.5, "show", "sad", holds="folder", keys=K((4.0, {"pose": "idle"}), (5.6, {"x": 100}))),
        ST("SICK LEAVE", 960, 330, 6.6, size=90),
    ], beat="Browning was dismissive; Urquhart was sent home on sick leave")
    scene(968.63, STUDY, [
        A("host", 960, 900, 1.7, "show", "neutral", holds="folder", talk=True),
        L("THE PHOTOGRAPHS THAT WERE IGNORED", 960, 130, "tag", 44, at=0.6),
        ST("MYTH #2?", 1450, 380, 4.6, size=90),
    ], beat="the story everyone knows; let's check the second myth")
    scene(976.06, STUDY, [
        A("aide", 700, 900, 1.6, "show", "worried", holds="folder", talk=True),
        A("host", 1250, 900, 1.6, "idle", "neutral", keys=K((2.6, {"pose": "count", "talk": True}))),
        L("WERE THERE REALLY TANKS WAITING?", 960, 120, "tag", 44, at=0.2),
        L("PICTURES DO. COUNT WHAT COULD DRIVE.", 960, 220, "plain", 40, at=5.2),
    ], beat="AIDE: the pictures had tanks. HOST: pictures do; let's count what could drive")
    scene(982.1, {"kind": "studio", "color": "#d9cdb0"}, [
        HEAD("BARELY ANY", 960, 160, 110, at=2.0, accent="BARELY"),
        {"kind": "bars", "title": "WORKING TANKS (ONE ESTIMATE)", "x": 960, "y": 470, "max": 16, "width": 900,
         "items": [{"label": "9TH SS: PANTHERS", "nation": "GERI", "value": 2, "in": 6.6}, {"label": "10TH SS: PANZER IV (5–14)", "nation": "GERI", "value": 14, "in": 9.6}]},
        L("MOST SS ARMOUR WAS LEFT IN NORMANDY", 960, 940, "tag", 40, at=3.6),
    ], beat="barely any: two working Panthers, 5–14 Panzer IVs")
    scene(996.34, {"kind": "heath", "panels": False}, [
        CNT(0, 0, 960, 320, 0.4, suffix=" GERMAN TANKS IN ACTION", size=80, dur=0.4),
        L("DAY ONE · AGAINST THE BRITISH", 960, 440, "tag", 42, at=1.2),
    ], beat="on the first day not one German tank went into action against the British")
    scene(1002.12, STUDY, [
        A("host", 960, 900, 1.7, "explain", "neutral", talk=True, keys=K((2.4, {"pose": "pointUp"}))),
        L("EVIDENCE: WEAK", 600, 260, "red", 50, at=0.3),
        L("CONCLUSION: RIGHT", 1350, 260, "green", 50, at=2.4),
    ], beat="the photographs were weak evidence; the conclusion was right")
    scene(1006.68, {"kind": "heath", "panels": False}, [
        *[V("halftrack", 300 + i * 520, 830 + (i % 2) * 40, 0.5, "GER") for i in range(3)],
        V("artillery", 1700, 870, 0.5, "GER"),
        {"kind": "crowd", "who": ["ss_soldier", "german_soldier", "german_officer"], "count": 6, "spacing": 230, "x": 960, "y": 960, "scale": 1.0, "pose": "hold", "expr": "determined"},
        L("THOUSANDS OF EXPERIENCED SS SOLDIERS", 960, 110, "tag", 42, at=1.2),
        L("A SHORT MARCH FROM THE DROP ZONES", 960, 210, "red", 42, at=6.0),
    ], camera=[{"t": 0, "zoom": 1.0}, {"t": 15, "zoom": 1.1}], beat="the danger was thousands of experienced SS soldiers a short march from the drop zones")
    ROAD(1022.12, p_for("A4") - 0.05, p_for("A4"), move=(0.4, 8.0), extra=[
        A("host", 1700, 1010, 1.25, "explain", "determined", talk=True, keys=K((6.0, {"pose": "pointL"}), (10.4, {"pose": "present", "expr": "smug"}))),
        L("BEDELL SMITH'S: PUT MORE STRENGTH AT ARNHEM", 960, 92, "tag", 40, at=2.8),
        L("IT WAS WAVED AWAY", 960, 180, "red", 40, at=8.4),
    ], beat="which exit? Bedell Smith's: more strength at Arnhem, waved away. That's four")
