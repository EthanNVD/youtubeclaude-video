"""People in places: decisions, news arriving, dialogue, meetings, quotes, speeches, phone calls, signings, arrivals."""
from __future__ import annotations

from shotlib import AID, K, L, PROP, SHOT  # noqa: F401

from .core import Param, recipe, stage

REACT = ["worried", "angry", "shocked", "determined", "sad", "smug", "panic", "happy", "nervous", "tired"]
OFFICE_SETS = ["office", "warroom", "tent", "bunker", "cabinet", "study", "conference", "radio", "codebreak", "hotel", "train_interior", "bridge"]
REACT_POSE = {"angry": "slam", "rage": "slam", "shocked": "head", "panic": "head", "worried": "chin", "sad": "face", "determined": "point",
              "smug": "hips", "happy": "cheer", "nervous": "rub", "tired": "wipe"}
HOLDS = {"telegram": "telegram", "paper": "paper", "folder": "folder", "photo": "photo", "book": "book", "none": None}


def _set(kind, flag=None, fg=True):
    st = {"kind": kind}
    if kind in ("office", "study", "cabinet", "conference", "home", "kitchen", "warroom", "bunker", "tent", "radio", "codebreak"):
        if fg:
            st["fg"] = "officedesk"
        if kind in ("office", "study", "cabinet", "conference", "home", "kitchen"):
            st["desk"] = False
    if flag and kind in ("office", "study", "bunker"):
        st["flag"] = flag
    return st


def _react_keys(t, react, then=None):
    k = [(t, {"pose": REACT_POSE.get(react, "chin"), "expr": react})]
    if then:
        k.append((t + 1.7, {"pose": then}))
    return k


# ------------------------------------------------------------------ decision
@recipe("decision", "talk",
        when="A leader learns something or decides something: 'X decided…', 'X ordered…', 'X realised…', 'X had a problem…'. "
             "Keep it 3-6 s, then follow with a card that SHOWS the consequence (command → field).",
        not_when="The narration describes what soldiers did (use an action recipe), or two people argue (use dialogue).",
        params={
            "who": Param("who", required=True, doc="cast id of the decision-maker"),
            "setting": Param("enum", "office", OFFICE_SETS, "where he is"),
            "reads": Param("enum", "telegram", list(HOLDS), "what he holds at the start"),
            "react": Param("enum", "determined", REACT, "his reaction on react_on"),
            "react_on": Param("phrase", doc="word(s) where he reacts (default: middle of the scene)"),
            "then": Param("enum", None, ["slam", "point", "pointL", "write", "phone", "chin", "cross", "fist", "explain"], "what he does after reacting"),
            "flag": Param("side", doc="side whose flag hangs on the wall (office/study/bunker)"),
            "aide": Param("who", doc="optional second person (an aide or officer) in the room"),
        },
        variants=("A", "B", "C"),
        shots="A: medium at his desk → close-up just before the reaction → medium. B: the aide's shoulder in the foreground "
              "(over-the-shoulder), then close on the leader. C: he walks into the room reading, stops, reacts (tracking), close.",
        example={"at": "By the end of 1915, the man", "recipe": "decision", "says": "Falkenhayn, Germany's top general, faced a war that could not be won by attacking.",
                 "who": "falkenhayn", "setting": "warroom", "react": "worried", "react_on": "had a problem", "then": "chin", "name_card": "falkenhayn"})
def decision(c):
    who = c.person("who")
    react, then = c.p("react"), c.p("then")
    holds = HOLDS[c.p("reads")]
    tr = c.t(c.p("react_on"), 0.45, 1.2)
    flag = c.side("flag").nation if c.p("flag") else None
    st = _set(c.p("setting"), flag)
    aide = c.person("aide")
    v = c.variant
    if v == "C":
        walk = max(1.2, min(2.6, tr - 0.4))
        x0 = round(1050 + 190 * walk)        # a calm walk: ~190 px/s at this size
        keys = [(walk, {"x": 1050}), *_react_keys(tr, react, then)]
        els = [AID("p", who, x0, 1000, 1.6, "hold" if holds else "idle", "neutral", holds=holds, turn=-0.4, keys=K(*keys))]
        if holds:
            els[0]["keys"].append({"t": tr - 0.05, "holds": ""})
        shots = [SHOT(0, "p", "full", track=True, frameX=-0.08), SHOT(max(0.6, tr - 0.35), "p", "close", frameX=0.12, push=0.05)]
        if c.dur - tr > 3.2:
            shots.append(SHOT(tr + 1.9, "p", "medium", frameX=-0.1))
        st.pop("fg", None)
        return stage(c, st, els, shots)
    keys = _react_keys(tr, react, then)
    if holds:
        keys.insert(0, (max(0.2, tr - 0.1), {"holds": ""}))
    els = [AID("p", who, 1000 if v == "A" else 1180, 1000, 1.6, "hold" if holds else "chin", "neutral", holds=holds, turn=-0.3, keys=K(*keys))]
    if v == "B" or aide:
        els.append(AID("aide", aide or c.side().officer, 560, 1080 if v == "B" else 1000, 2.1 if v == "B" else 1.5, "idle", "worried",
                       view="back" if v == "B" else None, turn=0.4, keys=K((tr + 0.3, {"pose": "chin"}))))
    if v == "A":
        shots = [SHOT(0, "p", "medium", frameX=-0.1), SHOT(max(0.6, tr - 0.35), "p", "close", frameX=0.12, push=0.06)]
        if c.dur - tr > 3.2:
            shots.append(SHOT(tr + 1.9, "p", "medium", frameX=0.1))
    else:
        shots = [SHOT(0, ["aide", "p"], "full", push=0.03), SHOT(max(0.6, tr - 0.35), "p", "close", frameX=-0.14, push=0.05)]
        if c.dur - tr > 3.2:
            shots.append(SHOT(tr + 1.9, ["aide", "p"], "medium"))
    return stage(c, st, els, shots)


# ------------------------------------------------------------------ report (news arrives)
@recipe("report", "talk",
        when="News reaches someone: 'a telegram arrived', 'he was told…', 'word reached Berlin…', 'the report said…'.",
        not_when="Nobody receives anything (use decision); the content of the paper matters more than the reaction (use document, ≤ 4 s).",
        params={
            "who": Param("who", required=True, doc="cast id of the person who receives the news"),
            "messenger": Param("who", doc="who brings it (default: an officer of the receiver's side)"),
            "side": Param("side", doc="side of the messenger if not given"),
            "item": Param("enum", "telegram", ["telegram", "paper", "folder", "photo"], "what is handed over"),
            "react": Param("enum", "shocked", REACT, "reaction when he reads it"),
            "react_on": Param("phrase", doc="word(s) where he reacts"),
            "setting": Param("enum", "office", OFFICE_SETS, "where"),
        },
        variants=("A", "B"),
        shots="A: messenger walks in from the left, hands it over (full shot) → medium on the reader → close before the reaction. "
              "B: the reader at his desk in close-up first; the messenger's hand enters; cut wide to both; close on the reaction.",
        example={"at": "Word reached Berlin", "recipe": "report", "says": "The bad news from the front reached the Kaiser.", "who": "kaiser_wilhelm",
                 "react": "shocked", "react_on": "lost"})
def report(c):
    who = c.person("who")
    msg = c.person("messenger") or c.side().officer
    item, react = c.p("item"), c.p("react")
    tr = c.t(c.p("react_on"), 0.6, 2.4)
    walk = c.variant == "A"
    hand = min(1.8, tr - 0.8) if walk else 0.5
    gk = ([(0.0, {"x": -180}), (hand, {"x": 560}), (hand + 0.15, {"pose": "offer"}), (hand + 0.8, {"pose": "idle", "holds": ""})]
          if walk else [(0.3, {"pose": "offer"}), (1.0, {"pose": "idle", "holds": ""})])
    els = [AID("giver", msg, -180 if walk else 600, 1000, 1.5, "carry", "neutral", holds=item, keys=K(*gk)),
           AID("recv", who, 1060, 1000, 1.55, "write", "neutral", holds="pen", turn=-0.4,
               keys=K((hand + 0.1, {"pose": "reach", "holds": ""}), (hand + 0.6, {"pose": "hold", "holds": item, "turn": 0}),
                      (tr, {"expr": react}), (tr + 1.2, {"pose": REACT_POSE.get(react, "chin")})))]
    if walk:
        shots = [SHOT(0, ["giver", "recv"], "full", zoom=1.0, x=880, push=0.03), SHOT(max(hand + 0.7, tr - 1.4), "recv", "medium", frameX=0.12),
                 SHOT(max(hand + 1.2, tr - 0.4), "recv", "close", frameX=0.16, push=0.05)]
    else:
        shots = [SHOT(0, "recv", "mediumclose", frameX=0.12), SHOT(1.1, ["giver", "recv"], "full", push=0.03),
                 SHOT(max(1.8, tr - 0.4), "recv", "close", frameX=0.16, push=0.05)]
    shots = sorted({round(q["t"], 2): q for q in shots}.values(), key=lambda q: q["t"])
    return stage(c, _set(c.p("setting")), els, shots)


# ------------------------------------------------------------------ dialogue
@recipe("dialogue", "talk",
        when="Two people argue, persuade or exchange views: 'X told Y…', 'Y refused…', 'they disagreed…'.",
        not_when="One person alone decides (decision); a crowd listens (speech).",
        params={
            "a": Param("who", required=True, doc="first speaker (cast id)"),
            "b": Param("who", required=True, doc="second speaker (cast id)"),
            "b_on": Param("phrase", doc="word(s) where B answers (cut to B)"),
            "a_mood": Param("enum", "determined", REACT, "A's expression"),
            "b_mood": Param("enum", "worried", REACT, "B's expression"),
            "setting": Param("enum", "office", OFFICE_SETS + ["garden", "corridor", "railway", "street", "deck"], "where"),
        },
        variants=("A", "B", "C"),
        shots="A: over-the-shoulder on A, then on B when B answers, then a two-shot. B: two-shot walking side by side (garden/corridor) "
              "then close-ups. C: A close, B close, two-shot (fast back-and-forth).",
        example={"at": "Ludendorff told the Kaiser", "recipe": "dialogue", "says": "Ludendorff admitted to the Kaiser that the army could not hold.",
                 "a": "ludendorff", "b": "kaiser_wilhelm", "b_on": "The Kaiser", "a_mood": "worried", "b_mood": "shocked"})
def dialogue(c):
    a, b = c.person("a"), c.person("b")
    tb = c.t(c.p("b_on"), 0.5, 1.5)
    am, bm = c.p("a_mood"), c.p("b_mood")
    place = c.p("setting")
    v = c.variant
    if v == "B":
        place = place if place in ("garden", "corridor", "railway", "street", "deck") else "corridor"
        els = [AID("a", a, 760, 1000, 1.45, "explain", am, talk=True, turn=0.4, keys=K((c.dur, {"x": 1060, "ease": "linear"}), (tb, {"talk": False, "pose": "idle"}))),
               AID("b", b, 1060, 1010, 1.45, "idle", "neutral", turn=-0.4, keys=K((c.dur, {"x": 1360, "ease": "linear"}), (tb, {"talk": True, "pose": "talk", "expr": bm})))]
        shots = [SHOT(0, ["a", "b"], "full", track=True), SHOT(max(0.8, tb - 0.2), "b", "mediumclose", track=True, frameX=-0.12)]
        if c.dur - tb > 3:
            shots.append(SHOT(tb + 2.2, "a", "mediumclose", track=True, frameX=0.12))
        return stage(c, {"kind": place}, els, shots)
    els = [AID("a", a, 640, 1060, 2.0, "explain", am, talk=True, turn=0.5, keys=K((tb, {"talk": False, "pose": "idle"}), (tb + 1.5, {"pose": "chin"}))),
           AID("b", b, 1280, 1000, 1.6, "idle", "neutral", turn=-0.5, keys=K((tb, {"talk": True, "pose": "talk", "expr": bm}), (tb + 1.8, {"pose": "shrug"})))]
    if v == "A":
        els[0]["view"] = "back"
        shots = [SHOT(0, ["a", "b"], "medium", frameX=0.1), SHOT(tb - 0.1, "b", "mediumclose", frameX=-0.18), SHOT(min(c.dur - 1.2, tb + 2.6), ["a", "b"], "full")]
    else:
        shots = [SHOT(0, "a", "mediumclose", frameX=0.15), SHOT(tb - 0.1, "b", "close", frameX=-0.15), SHOT(min(c.dur - 1.2, tb + 2.2), ["a", "b"], "medium")]
    shots = [q for q in shots if q["t"] < c.dur - 0.6] or shots[:1]
    return stage(c, _set(place if place in OFFICE_SETS else place, fg=False) if place in OFFICE_SETS else {"kind": place}, els, shots)


# ------------------------------------------------------------------ meeting
@recipe("meeting", "talk",
        when="A council, conference or staff meeting decides something: 'the generals met…', 'at the conference…', 'the cabinet agreed…'.",
        not_when="Only one or two people matter (decision / dialogue).",
        params={
            "people": Param("list", required=True, doc="2-5 cast ids around the table, left to right"),
            "speaker": Param("int", 0, doc="index (0 = first) of the one who talks"),
            "slam_on": Param("phrase", doc="word(s) where the speaker slams the table / points (the decision lands)"),
            "mood": Param("enum", "worried", REACT, "the others' expression"),
            "setting": Param("enum", "conference", ["conference", "cabinet", "warroom", "tent", "bunker", "parliament"], "where"),
        },
        variants=("A", "B"),
        shots="A: the table wide → speaker medium → the others reacting (group medium) → speaker close on the slam. "
              "B: speaker close first, then the room, then a listener's close-up.",
        example={"at": "On the 9th of January", "recipe": "meeting", "says": "The Kaiser's council approved unrestricted submarine war.",
                 "people": ["holtzendorff", "kaiser_wilhelm", "hindenburg"], "speaker": 0, "slam_on": "approved"})
def meeting(c):
    people = c.p("people") or []
    if not 2 <= len(people) <= 5:
        from .core import CardError, _where
        raise CardError(f"{_where(c.raw)}: \"people\" needs 2 to 5 cast ids, e.g. [\"foch\", \"haig\", \"petain\"].")
    for p in people:
        c.raw["_tmp"] = p
        c.person("_tmp")
    c.raw.pop("_tmp", None)
    n = len(people)
    sp = min(max(0, c.p("speaker")), n - 1)
    ts = c.t(c.p("slam_on"), 0.6, 1.5)
    xs = [960 + (i - (n - 1) / 2) * 330 for i in range(n)]
    els = []
    for i, who in enumerate(people):
        turn = -0.45 if xs[i] > 960 else 0.45
        if i == sp:
            keys = K((max(0.3, ts - 1.6), {"pose": "explain"}), (ts, {"pose": "slam", "expr": "determined"}), (ts + 1.4, {"pose": "point"}))
            els.append(AID(f"p{i}", who, xs[i], 1000, 1.5, "talk", "determined", talk=True, turn=turn, keys=keys))
        else:
            mood = c.p("mood")
            els.append(AID(f"p{i}", who, xs[i], 1000, 1.5, ["chin", "cross", "idle", "think"][i % 4], "neutral", turn=turn,
                           keys=K((ts + 0.25 + i * 0.12, {"expr": mood, "pose": ["head", "chin", "rub", "cross"][i % 4]}))))
    els.append({**PROP("paper", 960, 872, 0.7), "rotate": 80})
    others = [f"p{i}" for i in range(n) if i != sp]
    if c.variant == "A":
        shots = [SHOT(0, [f"p{i}" for i in range(n)], "medium", push=0.03), SHOT(min(1.6, ts * 0.4), f"p{sp}", "medium", frameX=0.1),
                 SHOT(max(1.0, ts - 0.4), f"p{sp}", "close", frameX=0.12, push=0.05), SHOT(ts + 1.0, others, "medium")]
    else:
        shots = [SHOT(0, f"p{sp}", "mediumclose", frameX=0.12), SHOT(min(1.8, ts * 0.5), [f"p{i}" for i in range(n)], "medium"),
                 SHOT(ts + 0.2, others[0], "close", frameX=-0.12)]
    shots = sorted({round(q["t"], 1): q for q in shots if q["t"] < c.dur - 0.5}.values(), key=lambda q: q["t"])
    return stage(c, _set(c.p("setting")), els, shots)


# ------------------------------------------------------------------ quote
@recipe("quote", "talk",
        when="The narration quotes someone's words: 'he said…', 'he wrote…', 'in his words…'. The line appears in a speech bubble.",
        not_when="Long speeches (use speech with a crowd); quotes longer than ~15 words (shorten the bubble text).",
        params={
            "who": Param("who", required=True, doc="who said it"),
            "text": Param("str", required=True, doc="the quoted words for the bubble (≤ 15 words, exactly as narrated or shortened)"),
            "tag": Param("str", doc="small tag under the bubble, e.g. 'QUOTE' or 'REPORTED · UNPROVEN'"),
            "mood": Param("enum", "determined", REACT, "expression"),
            "setting": Param("enum", "office", OFFICE_SETS + ["podium", "street", "trench", "deck"], "where"),
        },
        variants=("A", "B"),
        shots="A: medium-close on the speaker, bubble on the left. B: a slow push from medium to close, bubble on the right.",
        example={"at": "I have been hit", "recipe": "quote", "says": "The general admitted the attack had failed, in his own words.", "who": "foch",
                 "text": "We have been hit hard.", "tag": "QUOTE"})
def quote(c):
    who = c.person("who")
    right = c.variant == "B"
    els = [AID("q", who, 760 if right else 1080, 1000, 1.6, "talk", c.p("mood"), talk=True, turn=0.3 if right else -0.3,
               keys=K((c.dur * 0.55, {"pose": "explain"}))),
           {"kind": "bubble", "text": c.p("text"), "x": 1260 if right else 700, "y": 300, "side": -1 if right else 1, "size": 34, "in": 0.35, "hud": True}]
    if c.p("tag"):
        els.append(L(c.p("tag"), 1560 if right else 360, 140, "dark", 30, at=0.2, hud=True))
    st = {"kind": c.p("setting")}
    if st["kind"] in ("office", "study", "cabinet", "conference", "home"):
        st["desk"] = False
    shots = [SHOT(0, "q", "mediumclose", frameX=-0.2 if right else 0.2, push=0.05)] if not right else \
        [SHOT(0, "q", "medium", frameX=-0.2, push=0.03), SHOT(min(c.dur * 0.5, 3.0), "q", "close", frameX=-0.2, push=0.04)]
    return stage(c, st, els, shots)


# ------------------------------------------------------------------ speech
@recipe("speech", "talk",
        when="A leader addresses a crowd, parliament or troops: 'he told the nation…', 'he declared war…', 'in a speech…'.",
        not_when="A private conversation (dialogue).",
        params={
            "who": Param("who", required=True, doc="the speaker"),
            "audience": Param("enum", "crowd", ["crowd", "parliament", "troops", "radio"], "who listens"),
            "side": Param("side", doc="side of the audience/flag"),
            "cheer_on": Param("phrase", doc="word(s) where the audience cheers or reacts"),
            "mood": Param("enum", "determined", REACT, "speaker's expression"),
            "audience_mood": Param("enum", "happy", REACT + ["cheer"], "audience reaction"),
        },
        variants=("A", "B"),
        shots="A: speaker at the podium (low angle medium) → audience wide → speaker close. B: audience first (backs of heads), then the speaker.",
        example={"at": "On the 2nd of April, Wilson", "recipe": "speech", "says": "President Wilson asked Congress to declare war on Germany.",
                 "who": "wilson", "audience": "parliament", "side": "american", "cheer_on": "declare war"})
def speech(c):
    who = c.person("who")
    sd = c.side()
    aud = c.p("audience")
    tc = c.t(c.p("cheer_on"), 0.6, 1.5)
    am = c.p("audience_mood")
    if aud == "radio":
        els = [AID("sp", who, 1000, 1000, 1.6, "talk", c.p("mood"), talk=True, turn=-0.2, keys=K((tc, {"pose": "fist"}))),
               {**PROP("microphone", 1180, 860, 1.2), "front": True}]
        return stage(c, {"kind": "studio" if c.variant == "A" else "radio", "fg": "officedesk"}, els,
                     [SHOT(0, "sp", "medium", frameX=-0.1), SHOT(tc - 0.3, "sp", "close", frameX=0.1)])
    set_kind = {"crowd": "rally", "parliament": "parliament", "troops": "field"}[aud]
    listener = {"crowd": "civilian_man", "parliament": "diplomat", "troops": sd.soldier}[aud]
    els = [AID("sp", who, 960, 760 if aud != "troops" else 900, 1.45, "talk", c.p("mood"), talk=True,
               keys=K((max(0.5, tc - 1.4), {"pose": "raise"}), (tc, {"pose": "fist"})))]
    for i in range(6):
        x = 220 + i * 300
        pose = "cheer" if am == "cheer" or am == "happy" else "idle"
        els.append(AID(f"l{i}", listener if i % 2 == 0 else ("civilian_woman" if aud == "crowd" else listener), x, 1150 + (i % 2) * 30, 1.7,
                       "idle" if aud != "troops" else "port", "neutral", view="back", holds="rifle" if aud == "troops" else None,
                       keys=K((tc + 0.1 + (i % 3) * 0.15, {"pose": pose if aud != "troops" else "salute"}))))
    shots = ([SHOT(0, "sp", "medium", frameY=0.05), SHOT(min(tc, c.dur * 0.45), None, None, zoom=1.0, push=0.04), SHOT(tc + 1.4, "sp", "close")]
             if c.variant == "A" else
             [SHOT(0, None, None, zoom=1.0, push=0.04), SHOT(min(1.8, tc - 0.5), "sp", "medium"), SHOT(tc + 0.8, ["l2", "l3"], "medium")])
    shots = [q for q in shots if q["t"] < c.dur - 0.5]
    st = {"kind": set_kind, "flag": sd.nation} if set_kind == "rally" else {"kind": set_kind}
    return stage(c, st, els, shots)


# ------------------------------------------------------------------ phone
@recipe("phone", "talk",
        when="An urgent call or radio message: 'he phoned…', 'the order came by radio…', 'the line went dead…'.",
        not_when="A written message (report).",
        params={
            "who": Param("who", required=True, doc="who is on the phone"),
            "other": Param("who", doc="optional person on the other end (cut between both)"),
            "react": Param("enum", "worried", REACT, "reaction"),
            "react_on": Param("phrase", doc="word(s) where he reacts"),
            "setting": Param("enum", "office", OFFICE_SETS, "where"),
        },
        variants=("A", "B"),
        shots="A: medium → close on the reaction. B: cross-cut caller / receiver (needs other).",
        example={"at": "He called Paris", "recipe": "phone", "says": "The general phoned Paris to ask for every reserve.", "who": "joffre", "react": "determined"})
def phone(c):
    who = c.person("who")
    other = c.person("other")
    tr = c.t(c.p("react_on"), 0.55, 1.2)
    react = c.p("react")
    els = [AID("p", who, 980, 1000, 1.6, "phone", "neutral", holds="phone", turn=-0.3, keys=K((tr, {"expr": react}), (tr + 1.5, {"pose": "slam", "holds": ""}) if react in ("angry", "rage") else (tr + 1.5, {"headMove": "nod"})))]
    shots = [SHOT(0, "p", "medium", frameX=-0.1), SHOT(max(0.5, tr - 0.3), "p", "close", frameX=0.12)]
    if other and c.variant == "B":
        els.append(AID("o", other, 1500, 1000, 1.5, "phone", "determined", holds="phone", turn=-0.4, talk=True))
        shots = [SHOT(0, "p", "mediumclose", frameX=-0.15), SHOT(max(0.6, tr * 0.5), "o", "mediumclose", frameX=0.15), SHOT(max(1.2, tr - 0.2), "p", "close", frameX=0.12)]
        els[0]["x"] = 520
    st = _set(c.p("setting"))
    st["phone"] = True
    return stage(c, st, els, shots, sfx=[{"t": 0.1, "id": "phone_ring", "dur": 1.2}])


# ------------------------------------------------------------------ signing
@recipe("signing", "talk",
        when="A treaty, armistice, order or surrender is signed: 'they signed…', 'the armistice was signed…', 'he signed the order…'.",
        not_when="The text of the document matters more (document).",
        params={
            "who": Param("who", required=True, doc="who signs"),
            "witnesses": Param("list", doc="0-3 cast ids standing behind"),
            "sign_on": Param("phrase", doc="word(s) where the pen touches the paper"),
            "setting": Param("enum", "conference", ["conference", "train_interior", "cabinet", "tent", "office"], "where (armistice in a railway carriage: train_interior)"),
            "mood": Param("enum", "sad", REACT, "signer's expression"),
        },
        variants=("A", "B"),
        shots="A: wide of the table → the pen in close-up (insert) → the witnesses' faces. B: over the witness's shoulder → signer close → paper.",
        example={"at": "At 5 a.m. on the 11th of November", "recipe": "signing", "says": "Germany's delegates signed the armistice in Foch's railway carriage.",
                 "who": "zimmermann", "witnesses": ["foch"], "setting": "train_interior", "mood": "sad"})
def signing(c):
    who = c.person("who")
    wit = c.p("witnesses") or []
    ts = c.t(c.p("sign_on"), 0.45, 1.2)
    els = [AID("s", who, 900, 1000, 1.55, "write", c.p("mood"), holds="pen", turn=0.2, keys=K((max(0.2, ts - 1.0), {"pose": "idle", "holds": ""}), (ts, {"pose": "write", "holds": "pen"}), (ts + 1.6, {"pose": "idle", "holds": ""})))]
    for i, w in enumerate(wit[:3]):
        c.raw["_tmp"] = w
        c.person("_tmp")
        els.append(AID(f"w{i}", w, 1300 + i * 260, 990, 1.5, ["cross", "hips", "idle"][i % 3], "neutral", turn=-0.4, keys=K((ts + 0.4, {"expr": "determined"}))))
    c.raw.pop("_tmp", None)
    els.append({**PROP("paper", 880, 875, 0.8), "rotate": 82, "front": True, "id": "doc"})
    if c.variant == "A":
        shots = [SHOT(0, None, None, zoom=1.0, push=0.03), SHOT(max(0.6, ts - 0.2), "doc", "close", zoom=2.4, x=880, y=860), SHOT(ts + 1.4, [f"w{i}" for i in range(len(wit[:3]))] or "s", "medium")]
    else:
        shots = [SHOT(0, "s", "medium", frameX=-0.1), SHOT(max(0.6, ts - 0.2), "s", "close", frameX=0.1), SHOT(ts + 1.2, None, None, zoom=2.4, x=880, y=860)]
    shots = [q for q in shots if q["t"] < c.dur - 0.5]
    return stage(c, _set(c.p("setting")), els, shots, sfx=[{"t": ts, "id": "pen", "dur": 1.2}])


# ------------------------------------------------------------------ arrival / departure
@recipe("arrival", "action",
        when="Someone arrives or leaves: 'he arrived at…', 'he took command…', 'he was dismissed and left…', 'he went home'.",
        not_when="A crowd or an army moves (march / convoy).",
        params={
            "who": Param("who", required=True, doc="who walks"),
            "direction": Param("enum", "toward", ["toward", "away"], "toward the camera (arrives) or away (leaves)"),
            "setting": Param("enum", "corridor", ["corridor", "railway", "station", "street", "hotel", "garden", "airfield", "dock", "snow", "field"], "where"),
            "holds": Param("enum", "folder", ["folder", "suitcase", "none", "telegram"], "what he carries"),
            "mood": Param("enum", "determined", REACT, "expression"),
        },
        variants=("A", "B"),
        shots="A: one depth shot, he grows toward the lens (or shrinks away). B: wide of the place then a close tracking shot of his face.",
        example={"at": "By the end of August, Falkenhayn was gone", "recipe": "arrival", "says": "Falkenhayn was dismissed and left headquarters.",
                 "who": "falkenhayn", "direction": "away", "setting": "corridor", "holds": "suitcase", "mood": "sad"})
def arrival(c):
    who = c.person("who")
    holds = None if c.p("holds") == "none" else c.p("holds")
    place = c.p("setting")
    hz = 500 if place == "corridor" else 640 if place in ("railway", "station") else 600
    toward = c.p("direction") == "toward"
    d = min(c.dur - 0.3, max(2.4, c.dur * 0.8))
    if toward:
        a = AID("w", who, 960, hz + 100, None, "carry" if holds else "idle", c.p("mood"), holds=holds, keys=K((d, {"y": 1180, "ease": "linear"})))
    else:
        a = AID("w", who, 1060, 1120, None, "idle", c.p("mood"), view="back", holds=holds, holdsScale=0.5, keys=K((d, {"y": hz + 220, "ease": "linear"})))
    shots = [SHOT(0, None, None, zoom=1.0, push=0.05)]
    if c.variant == "B" and c.dur > 4:
        shots.append(SHOT(c.dur * 0.55, "w", "mediumclose", track=True, frameX=0.1))
    return stage(c, {"kind": place, "drift": 0}, [a], shots, world={"scale": 1.3 if toward else 1.45, "y": 900, "horizon": hz},
                 sfx=[{"t": 0.1, "id": "footsteps", "dur": min(4.0, d)}])
