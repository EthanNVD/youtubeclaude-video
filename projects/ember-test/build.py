"""Ember-style storytelling test: the first 60 s of the WW1 film, told the way Ember History tells a story.

python projects/ember-test/build.py  ->  projects/ember-test/plan.json

Grammar applied (from the frame-by-frame study of two Ember History films, see ANALYSIS.md):
- every clause gets ONE concrete picture; the picture changes when the idea changes (~2.5-6 s)
- the story enters through PEOPLE in PLACES (an anecdote): establishing exterior -> corridor -> the room -> the face
- inside a place the framing changes by 0.6 s dissolves (shotDissolve), between scenes 0.6 s cross-dissolves; hard cuts are rare
- a slow push-in on almost every shot (~1.5 %/s), sometimes a slow pan
- place/time tag top-left (wooden plank) that slides in on the date and persists while we stay there
- reveals land ~0.25 s after the word that names them (map fills, notes, stats)
- the film's questions as kinetic captions, word by word, key words in amber
- numbers as engraved stat cards over a mood picture; quotes as paper notes typed in
- time passing = the SAME place re-lit (dusk -> night) with a dissolve; absence (an empty helmet) for loss
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from shotlib import AID, FX, K, PROP, SHOT, man_path  # noqa: E402

WORDS = json.loads((ROOT / "projects/ww1-turning-point/work/transcript.words.json").read_text(encoding="utf8"))
END = 60.6


def word_t(phrase, after=0.0):
    toks = phrase.lower().split()
    norm = lambda w: "".join(ch for ch in w.lower() if ch.isalnum())
    ws = [norm(w["w"]) for w in WORDS]
    for i in range(len(WORDS)):
        if WORDS[i]["start"] >= after and ws[i:i + len(toks)] == [norm(t) for t in toks]:
            return WORDS[i]["start"]
    raise KeyError(phrase)


def cap_words(first, last, start, accents=()):
    """kinetic caption words from the narration between two phrases, times relative to a scene start"""
    a = word_t(first)
    b = word_t(last, a)
    out = []
    for w in WORDS:
        if a - 0.01 <= w["start"] <= b + 0.01:
            clean = w["w"].strip()
            out.append({"w": clean, "t": round(w["start"] + 0.05 - start, 2), "accent": any(x.lower() in clean.lower() for x in accents)})
    return out


scenes = []


def scene(start, set_, els, shots, **kw):
    s = {"start": round(start, 2), "type": "stage", "set": set_, "elements": els, "shots": shots, "shotDissolve": True, "transition": "fade"}
    s.update(kw)
    scenes.append(s)
    return s


TAG_SPA = "Spa, Belgium · 29 September 1918"
W = {"scale": 1.0, "y": 900}

# 1 ── establishing (acting): dawn at the HQ hotel; a staff car pulls up, a sentry presents arms, the two generals get out
s = 0.0
scene(s, {"kind": "hotel", "time": "dawn", "drift": 0}, [
    {"id": "car", "kind": "vehicle", "type": "car", "nation": "GERI", "x": -300, "y": 930, "keys": K((3.2, {"x": 640}))},
    AID("sentry", "ww1_german", 1500, 905, None, "port", "neutral", holds="rifle", turn=-0.4, keys=K((3.0, {"pose": "salute", "holds": ""}))),
    {**man_path("hin", "hindenburg", [(3.6, 600, 940), (6.9, 1060, 900)], pose="idle", expr="neutral", holds=""), "in": 3.4},
    {**man_path("lud", "ludendorff", [(3.9, 700, 950), (6.9, 1180, 905)], pose="hold", expr="determined", holds="folder"), "in": 3.7},
], [SHOT(0, None, None, zoom=1.0, push=0.05), SHOT(4.2, ["hin", "lud", "sentry"], "full", track=True, push=0.03)],
    world={"scale": 1.05, "y": 940}, tag=TAG_SPA, tagIn=word_t("1918,") + 0.25 - s, transition="cut")

# 2 ── the corridor (acting): they stride toward us; a staff officer stands aside and salutes
s = word_t("Field Marshal Paul")
scene(s, {"kind": "corridor", "doors": ["", ""]}, [
    man_path("hin", "hindenburg", [(0, 900, 640), (4.0, 840, 1010)], pose="idle", expr="neutral", holds=""),
    man_path("lud", "ludendorff", [(0, 1040, 650), (4.0, 1110, 1020)], pose="hold", expr="determined", holds="folder"),
    AID("aide", "ww1_german@officer", 1420, 760, None, "idle", "nervous", turn=-0.5, keys=K((1.2, {"pose": "salute"}))),
    {"kind": "namecard", "name": "Paul von Hindenburg", "role": "Field Marshal, Chief of the General Staff", "in": 0.4, "out": word_t("and General Erich") - s - 0.1},
    {"kind": "namecard", "name": "Erich Ludendorff", "role": "General, First Quartermaster-General", "in": word_t("General Erich") - s + 0.2},
], [SHOT(0, None, None, zoom=1.0, push=0.05)], world={"scale": 1.3, "y": 900, "horizon": 500}, tag=TAG_SPA, tagIn=-1)

# 3 ── the study (acting): the Kaiser is writing; he looks up as they come in, the pen stops; push to his face
s = word_t("told Kaiser Wilhelm")
tk = word_t("Kaiser Wilhelm") - s
tn = word_t("could no longer") - s
scene(s, {"kind": "office", "flag": "GERI", "portrait": True, "fg": "officedesk", "desk": False}, [
    AID("kaiser", "kaiser_wilhelm", 1250, 1000, 1.6, "write", "neutral", holds="pen", turn=-0.3,
        keys=K((tk + 0.3, {"pose": "idle", "holds": "", "turn": -0.6, "expr": "neutral"}), (tn + 0.4, {"expr": "shocked", "pose": "hold", "holds": "pen"}))),
    AID("lud", "ludendorff", 640, 1000, 1.6, "explain", "worried", talk=True, turn=0.5, keys=K((word_t("guarantee") - s, {"pose": "talk2"}))),
    AID("hin", "hindenburg", 380, 1010, 1.55, "idle", "sad", turn=0.5, keys=K((1.4, {"pose": "chin"}))),
    {"kind": "namecard", "name": "Kaiser Wilhelm II", "role": "German Emperor", "in": tk + 0.5},
], [SHOT(0, ["lud", "kaiser"], "full", push=0.03), SHOT(tn - 0.2, "kaiser", "mediumclose", frameX=0.12, push=0.05)], tag=TAG_SPA, tagIn=-1)

# 4 ── "Not for weeks. Not for days. For two hours." (acting): at the front, an officer checks his watch as tanks crawl out of the mist
s = word_t("Not for weeks.")
t2 = word_t("For two hours.") - s
scene(s, {"kind": "nomansland", "time": "dawn", "fg": "sandbags"}, [
    *[{"id": f"tk{i}", "kind": "vehicle", "type": "markiv", "nation": "UK", "x": 500 + i * 520, "y": 640 + i * 18, "keys": K((3.4, {"x": 560 + i * 520})), "moving": True} for i in range(3)],
    AID("off", "ww1_german@officer", 760, 1150, 2.0, "hold", "worried", holds="stopwatch", holdsScale=0.22, turn=0.4,
        keys=K((t2, {"expr": "panic", "pose": "head", "holds": ""}))),
    AID("sold", "ww1_german", 1380, 1170, 1.95, "aim", "nervous", holds="rifle", turn=-0.2, fireAt=[0.9, 2.2]),
    FX("shellburst", 1200, 700, size=1.6, **{"in": 1.4}),
], [SHOT(0, ["off", "sold"], "medium", push=0.04), SHOT(t2 - 0.3, "off", "close", frameX=-0.12, push=0.05)],
    world=W, impacts=[1.4], tag="The Western Front · 29 September 1918", tagIn=0.3, sfx=[{"t": 0, "id": "tank_engine", "dur": 3.0}])

# 5 ── the demand (acting): back in the study, Ludendorff brings his fist down on the desk; the Kaiser recoils
s = word_t("Germany needed an armistice,")
ti = word_t("immediately.") - s
scene(s, {"kind": "office", "flag": "GERI", "portrait": True, "fg": "officedesk", "desk": False}, [
    AID("lud", "ludendorff", 760, 1000, 1.6, "explain", "determined", talk=True, turn=0.4, keys=K((ti - 0.2, {"pose": "slam", "expr": "angry"}))),
    AID("kaiser", "kaiser_wilhelm", 1250, 1000, 1.6, "idle", "worried", turn=-0.5, keys=K((ti + 0.2, {"pose": "stop", "expr": "shocked"}))),
], [SHOT(0, ["lud", "kaiser"], "full", push=0.04), SHOT(ti - 0.4, "lud", "mediumclose", frameX=-0.12)],
    tag=TAG_SPA, tagIn=-1, sfx=[{"t": ti - 0.05, "id": "thud"}])

# 6 ── disbelief (acting): the Kaiser walks to the window and stands with his back to the room; rain outside
s = word_t("The Kaiser could hardly")
scene(s, {"kind": "office", "flag": "GERI", "portrait": True, "desk": False, "time": "dusk"}, [
    {**AID("kaiser", "kaiser_wilhelm", 900, 1000, 1.6, "idle", "sad"), "keys": K((1.6, {"x": 1250, "y": 990}), (1.75, {"view": "back", "pose": "behind"}))},
], [SHOT(0, "kaiser", "full", track=True, push=0.04)], tag=TAG_SPA, tagIn=-1, tint="cold")

# 7 ── six months earlier (acting): spring 1918, storm troops pour through the smoke
s = word_t("Six months earlier,")
waveA = [man_path(f"w{i}", "ww1_german", [(0.2 + (i % 3) * 0.2, -160 - i * 170, 700 + (i % 4) * 45), (6.2, 1400 - i * 170, 700 + (i % 4) * 45)], pose="charge", expr="shout", run=True) for i in range(7)]
scene(s, {"kind": "nomansland", "time": "dawn"}, waveA + [
    *[FX("smoke", x, y, size=1.4) for x, y in ((400, 720), (1100, 680), (1700, 740))],
    *[FX("shellburst", x, y, size=2.0, **{"in": t}) for t, x, y in ((0.6, 1600, 700), (2.0, 1300, 780), (3.3, 1750, 860))],
], [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(2.6, ["w1", "w2", "w3"], "full", track=True)], world=W, impacts=[0.6, 2.0, 3.3],
    tag="The Western Front · March 1918", tagIn=0.4)

# 7b ── the map, briefly: the front bulges forward
s = word_t("on the Western Front since")
WF = [[2.75, 51.13], [2.88, 50.85], [2.8, 50.35], [2.95, 49.65], [3.3, 49.42], [4.0, 49.3], [5.38, 49.22], [5.65, 48.9], [6.5, 48.6], [7.1, 47.6]]
SP = [[2.75, 51.13], [2.75, 50.75], [2.6, 50.3], [2.45, 49.85], [2.57, 49.62], [3.0, 49.4], [3.4, 49.05], [3.95, 49.1], [4.1, 49.25], [5.38, 49.22], [5.65, 48.9], [6.5, 48.6], [7.1, 47.6]]
scenes.append({"start": round(s, 2), "type": "map", "transition": "fade",
               "map": {"era": "1914", "center": [3.8, 49.7], "span": 7.5, "style": "paper",
                       "colors": {"German Empire": "GERI", "France": "#93ab6e", "Belgium": "#cfa264"}, "hatch": ["German Empire"], "rivers": ["Marne"]},
               "camera": [{"t": 0, "center": [4.3, 50.0], "span": 8.5}, {"t": 3.5, "center": [3.3, 49.4], "span": 6.0}],
               "elements": [{"kind": "front", "path": WF, "path2": SP, "morph": 0, "keys": K((0.2, {"morph": 0}), (1.8, {"morph": 1})), "color": "#7a2a22", "enter": "none", "width": 10},
                            {"kind": "city", "name": "Paris", "at": [2.35, 48.86], "in": 0.3, "tag": True, "side": "right"}],
               "tag": "The Western Front · Spring 1918", "tagIn": -1})

# 8 ── early June (acting): on a ridge at dusk an officer raises his binoculars...
s = word_t("In early June,")
ridge = {"kind": "nomansland", "time": "dusk", "wire": False, "horizon": 860}
scene(s, ridge, [
    {"kind": "glow", "x": 1500, "y": 840, "r": 260, "color": "#ffd9a0", "strength": 0.55},
    *[{**AID(f"g{i}", "ww1_german", 520 + i * 120, 866 + (i % 2) * 4, 0.62 - (i % 2) * 0.05, "port" if i % 2 else "idle", "neutral", view="back", holds="rifle" if i % 2 else ""), "silhouette": True}
      for i in range(4)],
    AID("off", "ww1_german@officer", 1250, 1080, 1.9, "idle", "determined", turn=0.3, keys=K((1.0, {"pose": "binoculars", "holds": "binoculars"}))),
], [SHOT(0, None, None, zoom=1.0, push=0.04, panX=60), SHOT(1.6, "off", "mediumclose", frameX=-0.15)], tag="The Marne · June 1918", tagIn=0.5, tint="warm")

# 8b ── ...and through them: Paris at dusk
s = word_t("about fifty-six")
scene(s, {"kind": "city", "time": "dusk"}, [{"kind": "binoculars", "in": 0}],
      [SHOT(0, None, None, zoom=1.15, x=960, y=500, push=0.04, panX=-40)], tag="The Marne · June 1918", tagIn=-1, tint="warm")

# 9 ── the question (acting): the same ridge — the men turn and trudge back as the light goes
s = word_t("So how does an army")
q1 = cap_words("So how does", "summer?", s, accents=("Paris", "collapse"))
scene(s, ridge, [
    {"kind": "glow", "x": 1500, "y": 840, "r": 260, "color": "#ffd9a0", "strength": 0.35},
    *[{**man_path(f"g{i}", "ww1_german", [(0.6 + i * 0.3, 520 + i * 120, 866 + (i % 2) * 4), (6.2, 60 + i * 90, 866 + (i % 2) * 4)], pose="port" if i % 2 else "idle",
                  expr="tired", holds="rifle" if i % 2 else ""), "silhouette": True, "flip": True, "scale": round(0.62 - (i % 2) * 0.05, 2)} for i in range(4)],
    {"kind": "caption", "words": q1},
], [SHOT(0, None, None, zoom=1.04, push=0.04)], tag="The Marne · June 1918", tagIn=-1, tint="warm")

# 10 ── (acting) weeks later: the same men fall back through rain and mud; the question goes on
s = word_t("Or had the war")
back = [{**man_path(f"r{i}", "ww1_german", [(0, 1500 + i * 170, 900 + (i % 3) * 60), (5.0, 700 + i * 170, 900 + (i % 3) * 60)], pose="shoulder" if i % 2 else "idle",
                    expr="tired", holds="rifle" if i % 2 else ""), "flip": True} for i in range(5)]
scene(s, {"kind": "nomansland", "time": "day", "weather": "rain", "wire": False}, back + [
    {"kind": "caption", "words": cap_words("Or had the war", "even started?", s, accents=("lost",))},
], [SHOT(0, None, None, zoom=1.0, push=0.04), SHOT(2.4, "r1", "medium", track=True)], world=W, tag="The Western Front · Summer 1918", tagIn=0.4, tint="cold")

# 11 ── "Ask around and you'll get a list" (acting): a historian at a blackboard chalks up the candidates
s = word_t("Ask around and")
scene(s, {"kind": "classroom", "desk": False}, [
    AID("prof", "civilian_man", 1250, 1000, 1.55, "reach", "smile", view="back", look_={"age": 0.8, "glasses": "round"},
        keys=K((1.4, {"view": "front", "pose": "pointL", "turn": -0.4, "talk": True}))),
    *[{"kind": "label", "text": t, "x": 760 + (i % 2) * 330, "y": 480 + (i // 2) * 100, "style": "chalk", "size": 58, "in": 0.3 + i * 0.45} for i, t in enumerate(["1914?", "1916?", "1917?", "1918?"])],
], [SHOT(0, "prof", "full", push=0.04)], tag="Today", tagIn=0.3, sfx=[{"t": 0.3, "id": "chalk", "dur": 1.8}])

# 12 ── candidate one, the Marne 1914 (acting): French infantry counter-attack across the stubble; an officer waves them on
s = word_t("The Marne, in 1914,")
scene(s, {"kind": "field", "time": "day", "poles": False, "houses": True, "road": False}, [
    *[man_path(f"f{i}", "ww1_french_1914", [(0, 260 - i * 150, 780 + (i % 4) * 70), (7.0, 1500 - i * 150, 780 + (i % 4) * 70)], pose="charge", expr="shout", run=True) for i in range(6)],
    AID("cap", "ww1_french_1914@officer", 1500, 1040, None, "wave", "shout", turn=-0.3, keys=K((1.2, {"pose": "pointL"}), (2.6, {"pose": "wave"}))),
    *[FX("shellburst", x, y, size=2.0, **{"in": t}) for t, x, y in ((0.6, 1500, 720), (1.9, 1200, 800), (3.4, 1650, 860))],
], [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(2.8, "cap", "medium", frameX=0.12), SHOT(4.6, ["f1", "f2", "f3"], "full", track=True)], world=W,
    impacts=[0.6, 1.9, 3.4], tag="The Marne · September 1914", tagIn=0.4)

# assemble
scenes.sort(key=lambda q: q["start"])
for i, q in enumerate(scenes):
    q["id"] = f"s{i + 1:03d}"
    q["end"] = scenes[i + 1]["start"] if i + 1 < len(scenes) else END
CAST = {n: {"preset": n} for n in ("kaiser_wilhelm", "hindenburg", "ludendorff", "ww1_german", "ww1_french_1914", "civilian_man")}
for q in scenes:
    for e in q["elements"]:
        w = e.get("who")
        if isinstance(w, str) and "@" in w:
            base = w.split("@")[0]
            cid = base + "__officer"
            CAST[cid] = {"preset": base, "hat": "peaked"}
            e["who"] = cid
plan = {"meta": {"title": "Ember-style test — WW1 cold open", "lang": "en", "fps": 24, "duration": END, "voice": "input/voice.wav", "grain": 0.5},
        "cast": CAST, "scenes": scenes}
(ROOT / "projects/ember-test/plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False), encoding="utf8")
print(len(scenes), "scenes")
