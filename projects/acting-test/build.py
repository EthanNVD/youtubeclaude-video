"""Acting + camera test (1 min, Market Garden 15:29-16:28): coverage inside places, people doing things.
python projects/acting-test/build.py && python tools/make.py projects/acting-test validate"""
import sys

sys.path.insert(0, "tools")
from shotlib import Plan, A, K, L, ST, NC, V, FX, DOC, PROP  # noqa: E402

END = 59.4
P = Plan(end=END)
WOOD = {"kind": "panel", "x": 960, "y": 540, "w": 2600, "h": 1600, "color": "#8a5a33", "border": False, "enter": "none"}
GRAIN = [{"kind": "shape", "shape": "rect", "x": 960, "y": 120 + i * 210, "w": 2600, "h": 3, "fill": "#6f4626", "stroke": "#6f4626", "strokeWidth": 0, "enter": "none", "opacity": 0.5} for i in range(5)]


def sc(start, set_, els, shots=None, **kw):
    s = {"start": start, "type": "stage", "set": set_, "elements": els}
    if shots:
        s["shots"] = shots
    s.update(kw)
    return P.add(s)


def act(id_, who, x, y, s, pose="idle", expr="neutral", keys=None, **kw):
    d = A(who, x, y, s, pose, expr, keys=keys, **kw)
    if s is None:
        d.pop("scale")
    d["id"] = id_
    return d


def photo(x, y, s=1.0, rot=0, at=0.0, enter="slideR", **kw):
    return {"kind": "prop", "item": "photo", "x": x, "y": y, "scale": s, "rotate": rot, "in": at, "enter": enter, **kw}


# 0.00 "Then there were the photographs." — insert: prints land on a desk one by one, a hand squares them up
sc(0.0, {"kind": "paper", "dof": 0}, [WOOD, *GRAIN,
    photo(760, 560, 2.2, -8, 0.05, "drop"), photo(1180, 520, 2.2, 6, 0.35, "drop"), photo(960, 640, 2.3, -2, 0.7, "drop"),
    {"kind": "hand", "x": 2250, "y": 700, "flip": True, "scale": 1.4, "sleeve": "#6b6446", "in": 0.9, "enter": "none",
     "keys": K((0.9, {"x": 2250}), (1.5, {"x": 1700, "ease": "out"}))}],
   shots=[{"t": 0, "zoom": 1.0, "push": 0.06}], sfx=[{"t": 0.1, "id": "paper"}, {"t": 0.4, "id": "paper"}, {"t": 0.75, "id": "paper"}])

# 1.82 intelligence office: a clerk brings a slip, Urquhart reads it; name card on his name
clerk_keys = K((0.0, {"x": -160}), (2.0, {"x": 560, "ease": "inOut"}), (2.2, {"pose": "offer"}), (3.2, {"pose": "idle"}), (4.2, {"x": -200, "ease": "in"}))
sc(1.82, {"kind": "office", "flag": "UK", "portrait": False, "desk": False, "fg": "officedesk"}, [
    act("clerk", "british_soldier", -160, 905, 1.5, "carry", "neutral", holds="paper", keys=clerk_keys, out=6.5),
    act("urq", "brian_urquhart", 1040, 990, 1.55, "write", "neutral", holds="pen", turn=-0.35,
        keys=K((2.1, {"pose": "reach", "turn": -0.6, "holds": ""}), (2.6, {"pose": "hold", "holds": "telegram", "turn": 0, "expr": "worried"}),
               (5.6, {"pose": "shrug", "expr": "nervous"}), (6.4, {"pose": "hold", "expr": "worried"})),
        holdsKeys=None),
    {**PROP("paper", 760, 845, 0.7), "front": True, "rotate": -10},
    {**PROP("phone", 1380, 830, 0.9), "front": True},
    NC("Maj Brian Urquhart", "I Airborne Corps intelligence — no relation to the general", at=4.2),
], shots=[{"t": 0, "on": ["clerk", "urq"], "size": "full", "zoom": 1.0, "x": 900, "push": 0.03},
          {"t": 2.4, "on": "urq", "size": "medium", "frameX": 0.12, "push": 0.05},
          {"t": 4.3, "on": "urq", "size": "close", "frameX": 0.16, "push": 0.05}],
   sfx=[{"t": 0.3, "id": "footsteps"}, {"t": 2.2, "id": "paper"}])

# 8.60 "kept hearing from the Dutch resistance" — night attic, a man taps out a message
sc(8.6, {"kind": "home", "time": "night", "fg": "officedesk"}, [
    act("dutch", "dutch_civilian", 960, 1010, 1.6, "typing", "worried", turn=0.35, keys=K((1.6, {"expr": "nervous", "look": 0.8}))),
    {**PROP("radio", 1010, 880, 1.05), "front": True},
    {**PROP("candle", 600, 830, 1.4), "front": True},
    {"kind": "glow", "x": 600, "y": 760, "r": 420, "color": "#ffd28a", "strength": 0.5, "enter": "none", "front": True},
], shots=[{"t": 0, "on": "dutch", "size": "medium", "frameX": -0.08, "push": 0.04},
          {"t": 1.7, "on": "dutch", "size": "close", "frameX": 0.15, "push": 0.05}],
   sfx=[{"t": 0.2, "id": "morse"}], tint="night")

# 11.90 "German armour around Arnhem" — panzers parked under trees, crews resting
sc(11.9, {"kind": "field", "drift": 0}, [
    {"id": "tank1", "kind": "vehicle", "type": "panzer4", "nation": "GER", "x": 1220, "y": 840, "parked": True},
    {"id": "tank2", "kind": "vehicle", "type": "panther", "nation": "GER", "x": -420, "y": 730, "keys": K((2.35, {"x": 430}))},
    act("ss1", "ss_soldier", 1580, 860, None, "smoke", "neutral", keys=K((1.5, {"pose": "chin"}))),
    act("ss2", "ss_soldier", 760, 870, None, "idle", "smile", look=-0.6, keys=K((0.6, {"x": 760}), (2.2, {"x": 930}), (2.4, {"pose": "pockets"}))),
], world={"scale": 0.95, "y": 870},
   shots=[{"t": 0, "size": "wide", "zoom": 1.05, "x": 900, "y": 600, "panX": -60},
          {"t": 2.45, "on": ["ss2", "tank1"], "size": "full", "push": 0.03}],
   date="SEPTEMBER 1944", place="ARNHEM", ambience="wind")

# 14.91 "He asked for reconnaissance flights." — on the phone, pointing at the map
sc(14.91, {"kind": "office", "flag": "UK", "portrait": False, "desk": False, "fg": "officedesk"}, [
    act("urq", "brian_urquhart", 1040, 990, 1.55, "phone", "determined", holds="phone", talk=True, turn=0.4,
        keys=K((1.4, {"expr": "angry", "turn": -0.3, "headMove": "nod"}))),
], shots=[{"t": 0, "on": "urq", "size": "mediumclose", "frameX": 0.1, "push": 0.06}], sfx=[{"t": 0.0, "id": "phone_ring"}])

# 17.79 "On the 12th of September, a photo reconnaissance Spitfire" — low pass over the polder, camera pans with it
sc(17.79, {"kind": "polder", "drift": 0}, [
    {"id": "spit", "kind": "vehicle", "type": "fighter", "nation": "UK", "x": -700, "y": 470, "scale": 3.3, "rotate": -3,
     "keys": K((2.3, {"x": 2700, "y": 400, "ease": "linear"}))},
], shots=[{"t": 0, "size": "wide", "x": 820, "zoom": 1.12, "panX": 300, "shake": 2}],
   date="12 SEPTEMBER 1944", sfx=[{"t": 0.0, "id": "plane_flyby"}])

# 20.10 what its camera saw: shutter, shutter, shutter
sc(20.1, {"kind": "paper", "dof": 0}, [
    photo(960, 560, 8.6, 0, 0, "none"),
    {"kind": "viewfinder", "hud": True, "label": "ARNHEM", "shots": [0.25, 0.7, 1.15], "start": 41, "enter": "none"},
], shots=[{"t": 0, "x": 900, "y": 560, "zoom": 1.0, "panX": 160, "push": 0.05}], sfx=[{"t": 0.25, "id": "tick"}, {"t": 0.7, "id": "tick"}, {"t": 1.15, "id": "tick"}])

# 21.60 "came back with pictures that showed tanks" — magnifier over the print, red pencil ring
sc(21.6, {"kind": "paper", "dof": 0}, [WOOD, *GRAIN,
    photo(960, 540, 4.2, -3, 0, "none"),
    {"kind": "prop", "item": "magnifier", "x": 1500, "y": 760, "scale": 1.6, "enter": "none",
     "keys": K((1.0, {"x": 770, "y": 380, "ease": "inOut"}), (2.2, {"x": 790, "y": 360}), (2.8, {"x": 1600, "y": 800, "ease": "in"}))},
    {"kind": "shape", "shape": "ring", "x": 712, "y": 345, "r": 90, "in": 1.6, "enter": "draw", "strokeWidth": 9},
    {"kind": "shape", "shape": "ring", "x": 1180, "y": 520, "r": 80, "in": 2.4, "enter": "draw", "strokeWidth": 9},
], shots=[{"t": 0, "zoom": 1.0, "push": 0.08}])

# 25.17 "Urquhart took them to his commander." — walks down the corridor toward the camera, folder under his arm
sc(25.17, {"kind": "corridor"}, [
    act("urq", "brian_urquhart", 960, 600, None, "carry", "determined", holds="folder", keys=K((2.85, {"y": 1180, "ease": "linear"}))),
], world={"horizon": 500, "y": 900, "scale": 1.3},
   shots=[{"t": 0, "zoom": 1.0, "push": 0.05}], sfx=[{"t": 0.1, "id": "footsteps"}])

# 28.05 "Lieutenant General Frederick Browning." — he enters; Browning writing, looks up
SET_B = {"kind": "cabinet", "fg": "officedesk", "flag": "UK"}
sc(28.05, SET_B, [
    act("brow", "browning", 1080, 995, 1.6, "write", "neutral", holds="pen", turn=-0.2, keys=K((1.4, {"pose": "idle", "expr": "smug", "turn": -0.55}))),
    act("urq", "brian_urquhart", -150, 1000, 1.62, "idle", "worried", holds="folder", holdsScale=0.45, keys=K((1.2, {"x": 330, "ease": "out"}))),
    {**PROP("paper", 1180, 845, 0.8), "front": True, "rotate": 6},
    NC("Lt Gen Frederick Browning", "commander, I Airborne Corps", at=0.5),
], shots=[{"t": 0, "on": ["brow"], "size": "full", "zoom": 1.0, "x": 860, "push": 0.03},
          {"t": 1.25, "on": "brow", "size": "mediumclose", "frameX": 0.1, "push": 0.05}],
   sfx=[{"t": 0.2, "id": "thud", "vol": 0.5}])

# 30.39 "Browning was dismissive." — over Urquhart's shoulder: the prints on the desk, a glance, a wave of the hand
sc(30.39, SET_B, [
    act("brow", "browning", 1180, 995, 1.6, "idle", "smug", turn=-0.45, keys=K((0.5, {"pose": "wave", "headMove": "shake"}), (1.4, {"pose": "cross"}))),
    {**photo(1010, 862, 0.75, -4, 0.0, "slideL"), "front": True},
    {**photo(1150, 868, 0.75, 7, 0.15, "slideL"), "front": True},
    act("urq", "brian_urquhart", 430, 1330, 3.0, "idle", "worried", view="back", fixedLayer=True, front=True),
], shots=[{"t": 0, "zoom": 1.0, "x": 960, "y": 540, "push": 0.04},
          {"t": 1.1, "on": "brow", "size": "close", "frameX": 0.08, "push": 0.05}])

# 32.41 "the corps medical officer was sent to see Major Urquhart"
sc(32.41, {"kind": "office", "flag": "UK", "portrait": False, "desk": False, "fg": "officedesk"}, [
    act("urq", "brian_urquhart", 860, 990, 1.55, "write", "worried", holds="pen", turn=0.3,
        keys=K((1.3, {"pose": "idle", "holds": "", "turn": 0.7, "look": 1}), (2.5, {"expr": "shocked", "pose": "pointSelf"}))),
    act("doc", "medic", 2150, 960, 1.6, "idle", "neutral", keys=K((1.6, {"x": 1480, "ease": "out"}), (1.9, {"pose": "offer", "expr": "smile", "turn": -0.5}))),
    NC("Corps medical officer", "", at=1.4),
], shots=[{"t": 0, "on": ["urq"], "size": "full", "zoom": 1.0, "x": 1100, "push": 0.03},
          {"t": 2.45, "on": "urq", "size": "close", "frameX": -0.1, "push": 0.06}], sfx=[{"t": 0.3, "id": "thud", "vol": 0.5}])

# 36.20 "and Urquhart was sent home on sick leave" — the form is stamped
sc(36.2, {"kind": "paper", "dof": 0}, [WOOD, *GRAIN,
    DOC("form", "MEDICAL BOARD", ["MAJ. B. URQUHART", "EXHAUSTION", "LEAVE: IMMEDIATE"], x=960, y=540, w=900, h=640, at=0.0, speed=60, stamp="SICK LEAVE"),
], shots=[{"t": 0, "zoom": 1.0, "push": 0.05}], sfx=[{"t": 0.7, "id": "stamp"}])

# 37.90 walking away with a suitcase in the rain, getting small
sc(37.9, {"kind": "railway", "weather": "rain"}, [
    act("urq", "brian_urquhart", 1060, 1120, None, "idle", "sad", view="back", holds="suitcase", holdsScale=0.5, keys=K((1.7, {"y": 880, "ease": "linear"}))),
], world={"scale": 1.45, "y": 900},
   shots=[{"t": 0, "zoom": 1.0, "push": 0.03}], tint="cold", ambience="rain")

# 39.63 host: "That's the story everyone knows, the photographs that were ignored."
sc(39.63, {"kind": "study", "desk": False}, [
    act("host", "host", 900, 905, 1.55, "show", "neutral", holds="photo", holdsScale=0.5, talk=True, turn=0.3,
        keys=K((1.6, {"pose": "idle", "expr": "smug", "turn": -0.2}), (2.8, {"pose": "shrug", "holds": ""}))),
], shots=[{"t": 0, "on": "host", "size": "medium", "frameX": -0.12, "push": 0.05},
          {"t": 2.2, "on": "host", "size": "close", "frameX": 0.1, "push": 0.05}])

# 44.06 "So let's check the second myth on the road." — walks to the wall (camera tracks him) and pins the print up
sc(44.06, {"kind": "study", "desk": False}, [
    {**PROP("photo", 1560, 560, 0.7), "rotate": 3, "in": 2.0, "enter": "pop", "id": "pin"},
    L("MYTH 2", 1560, 430, "tag", 40, at=2.2),
    act("host", "host", 520, 905, 1.55, "idle", "neutral", holds="photo", holdsScale=0.45, talk=True,
        keys=K((1.8, {"x": 1330, "ease": "inOut"}), (1.9, {"pose": "reach", "turn": 0.6, "holds": ""}), (2.4, {"pose": "point", "turn": -0.3, "expr": "smug"}))),
], shots=[{"t": 0, "on": "host", "size": "full", "track": True, "zoom": 1.45, "dy": 40},
          {"t": 2.0, "on": ["host", "pin"], "size": "full", "zoom": 1.3, "push": 0.04}])

# 47.06 "Were there really tanks waiting at Arnhem?" — over the aide's shoulder onto the host
TWO = {"kind": "study", "desk": False}
sc(47.06, TWO, [
    act("host", "host", 1220, 905, 1.6, "explain", "neutral", talk=True, turn=-0.5, keys=K((1.2, {"pose": "chin", "expr": "neutral"}))),
    act("aide", "aide", 420, 1300, 2.9, "idle", "neutral", view="back", fixedLayer=True),
], shots=[{"t": 0, "zoom": 1.0, "x": 960, "push": 0.05}])

# 49.58 "Sir, the pictures had tanks in them." — reverse: the aide holds the print up
sc(49.58, TWO, [
    act("aide", "aide", 700, 905, 1.6, "holdUp", "worried", holds="photo", holdsScale=0.75, talk=True, turn=0.5),
    act("host", "host", 1520, 1300, 2.9, "idle", "neutral", view="back", fixedLayer=True),
], shots=[{"t": 0, "zoom": 1.0, "x": 960, "push": 0.05}])

# 52.18 "Pictures do." — close on the host, dry
sc(52.18, TWO, [
    act("host", "host", 1180, 905, 1.6, "idle", "smug", talk=True, turn=-0.4, headMove="nod"),
], shots=[{"t": 0, "on": "host", "size": "close", "frameX": 0.1, "push": 0.03}])

# 53.10 "Let's count what could actually drive." — two-shot, he takes the print and taps it
sc(53.1, TWO, [
    act("aide", "aide", 760, 905, 1.55, "show", "worried", holds="photo", holdsScale=0.6, turn=0.45, keys=K((0.6, {"pose": "idle", "expr": "neutral"}))),
    act("host", "host", 1180, 905, 1.6, "reach", "neutral", turn=-0.5, talk=True, keys=K((0.5, {"pose": "pointL", "expr": "determined"}))),
], shots=[{"t": 0, "on": ["aide", "host"], "size": "medium", "push": 0.04}])

# 55.10 "barely any." — the print, the tanks crossed out one by one
sc(55.1, {"kind": "paper", "dof": 0}, [WOOD, *GRAIN,
    photo(960, 540, 4.2, -3, 0, "none"),
    {"kind": "shape", "shape": "cross", "x": 712, "y": 345, "scale": 0.62, "in": 0.15, "enter": "pop"},
    {"kind": "shape", "shape": "cross", "x": 1180, "y": 520, "scale": 0.62, "in": 0.45, "enter": "pop"},
    {"kind": "shape", "shape": "cross", "x": 607, "y": 632, "scale": 0.62, "in": 0.75, "enter": "pop"},
], shots=[{"t": 0, "zoom": 1.0, "push": 0.05}], sfx=[{"t": 0.15, "id": "pen"}, {"t": 0.45, "id": "pen"}, {"t": 0.75, "id": "pen"}])

# 56.74 "Most of the SS armour had been left in Normandy." — burnt-out panzers along a Normandy lane, slow track
sc(56.74, {"kind": "field", "drift": 0}, [
    {"kind": "vehicle", "type": "panther", "nation": "GER", "x": 820, "y": 705, "burning": True, "rotate": -3},
    {"kind": "vehicle", "type": "tiger", "nation": "GER", "x": 1420, "y": 790, "damaged": True, "rotate": 4},
    {"kind": "vehicle", "type": "panzer4", "nation": "GER", "x": 60, "y": 1080, "damaged": True},
    FX("smoke", 820, 600), FX("smoke", 1430, 650),
], world={"scale": 0.95, "y": 870},
   shots=[{"t": 0, "zoom": 1.1, "x": 900, "y": 560, "panX": 140, "push": 0.03}],
   date="AUGUST 1944", place="NORMANDY", tint="warm")

META = {"title": "Acting test — the photographs", "lang": "en", "fps": 24, "width": 1920, "height": 1080, "duration": END,
        "voice": "input/voice.wav", "grain": 0.5}
CAST = {
    "host": {"preset": "host"}, "aide": {"preset": "aide"},
    "brian_urquhart": {"preset": "brian_urquhart"}, "browning": {"preset": "browning"},
    "dutch_civilian": {"preset": "dutch_civilian"}, "ss_soldier": {"preset": "ss_soldier"},
    "british_soldier": {"preset": "british_soldier"},
    "medic": {"preset": "browning", "facial": "none", "glasses": "round", "hairColor": "#7a6a58", "age": 0.6, "extra": ["armband"]},
}
P.finish(META, CAST, "projects/acting-test/plan.json")
