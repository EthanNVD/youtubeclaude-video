"""Chapter 5 (Pless, the U-boats, America), chapter 6 (Brest-Litovsk), chapter 7 (spring 1918, second Marne), chapter 8 (Amiens).
15:26 - 27:15"""
from lib import *  # noqa: F401,F403
from lib import sc, host, duo, glass, hq, report, march_col, trench, battlefield, fleet, doc, quote, MAP, city, arrow, front, PL, \
    EUROPE, WEST, LEG_CP, LEG_W, WESTERN_FRONT, SPRING_1918, HINDENBURG, EAST_FRONT, BREST_LOSS, mv  # noqa: E402


def r(start, phrase):
    return round(peek(phrase) - start, 2)


ATL = {"German Empire": "GERI", "United Kingdom of Great Britain and Ireland": "#d99a8c", "France": "#93ab6e", "United States": "#c49a6c", "Mexico": "#e3d3a8"}
LEG_ATL = [("GERI", "Germany"), ("UK", "Britain"), ("FRA", "France"), ("USA", "United States")]


def bars(start, title, items, mx, unit="", **kw):
    return sc(start, {"kind": "workshop"}, [{"kind": "bars", "title": title, "x": 1020, "y": 400, "width": 760, "max": mx, "unit": unit,
                                             "items": [{"label": l, "value": v, ("nation" if len(c) <= 5 else "color"): c, "in": t} for l, v, c, t in items]}],
              [SHOT(0, None, None, zoom=1.0, push=0.05)], **kw)


def sinking(start, ship="cargo", nation="NEUTRAL", hit=1.2, sink=True, **kw):
    """A U-boat's periscope and torpedo track, the ship hit, listing and going down."""
    els = [{"id": "ship", "kind": "vehicle", "type": ship, "nation": nation, "x": 1150, "y": 640, "scale": 0.62,
            "keys": mv((hit, {"x": 1180}), (hit + 4.5, {"rotate": 8, "y": 700, "ease": "in"}) if sink else (hit + 0.1, {"x": 1180}))},
           {"kind": "line", "path": [[200, 820], [1120, 660]], "screen": True, "color": "#e9eef0", "width": 5, "dashed": True, "enter": "draw", "dur": hit, "in": 0.0},
           FX("explosion", 1120, 600, **{"in": hit}), FX("splash", 1140, 650, **{"in": hit + 0.05}), FX("smoke", 1160, 560, **{"in": hit + 0.2})]
    return sc(start, {"kind": "sea", "drift": 0}, els, [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(hit + 0.6, None, None, zoom=1.6, x=1150, y=600, push=0.05)],
              sfx=[{"t": hit, "id": "explosion"}], **kw)


def build():
    # ================================================================ CHAPTER 5 — Pless
    s = T("Germany had tried submarine warfare")
    fleet(s, ships=(("uboat", "GERI", 700, 740, 1),), dur=8, chapter="Six Months to London", date="FEBRUARY 1915")
    s = T("In May that year, a U-boat torpedoed")
    sinking(s, ship="cargo", nation="UK", hit=1.4, date="7 MAY 1915", place="OFF IRELAND")
    SCENES[-1]["elements"].append(L("LUSITANIA", 960, 985, "tag", 36, at=0.6, hud=True))
    s = T("Of nearly two thousand people on board")
    sc(s, {"kind": "memorial", "drift": 0}, [
        CNT(0, 1960, 960, 360, at=0.2, prefix="≈", suffix=" ON BOARD", size=72, dur=1.0),
        CNT(0, 760, 960, 520, at=r(s, "fewer than eight hundred"), prefix="< ", suffix=" SURVIVED", size=72, dur=1.0, color="#a8d0a0"),
        CNT(0, 128, 960, 680, at=r(s, "About a hundred and twenty-eight"), prefix="≈", suffix=" AMERICANS DEAD", size=60, dur=1.0, color="#f08070")],
       [SHOT(0, None, None, zoom=1.0, push=0.05)], tint="grey")
    s = T("You'll often hear that the Lusitania")
    doc(s, "newspaper", "NEW YORK, MAY 1915", ["LUSITANIA SUNK", "AMERICANS AMONG THE DEAD", "WASHINGTON PROTESTS"], stamp="NOT WAR — YET", speed=36)
    s = T("America protested, threatened, and stayed out")
    sc(s, {"kind": "podium", "drift": 0}, [
        AID("w", "wilson", 960, 960, 1.55, "talk", "determined", talk=True, keys=mv((2.2, {"pose": "stop"}), (4.0, {"pose": "explain"}))),
        NC("President Woodrow Wilson", "United States", at=0.4),
        L("\"HE KEPT US OUT OF WAR\" · 1916", 960, 160, "tag", 40, at=r(s, "on the slogan"))],
       [SHOT(0, "w", "medium", frameX=-0.1), SHOT(r(s, "won re-election"), "w", "close", frameX=0.12)])
    s = T("The Lusitania made Americans angry")
    host(s, "explain", "neutral", keys=mv((r(s, "Something else made them fight"), {"pose": "point", "expr": "smug"})), second=(r(s, "Something else"), "close", "host"))

    s = T("In April 1916, Germany stopped sinking")
    fleet(s, ships=(("uboat", "GERI", 900, 740, -1),), dur=6, date="APRIL 1916")
    s = T("But by the end of that year")
    sc(s, {"kind": "workshop"}, [{"kind": "timeline", "x": 960, "y": 560, "width": 1400, "items": [
        {"sub": "1916", "label": "Verdun", "at": 0.12, "color": "GERI", "in": r(s, "after Verdun")},
        {"sub": "1916", "label": "The Somme", "at": 0.37, "color": "GERI", "in": r(s, "the Somme")},
        {"sub": "1916", "label": "Jutland", "at": 0.62, "color": "GERI", "in": r(s, "Jutland")},
        {"sub": "1916-17", "label": "Turnip Winter", "at": 0.86, "color": "GERI", "in": r(s, "the Turnip Winter")}]}],
       [SHOT(0, None, None, zoom=1.0, push=0.05)])
    s = T("In December 1916, the head of the Admiralty staff")
    report(s, "clerk_de", "holtzendorff", item="folder", text="MEMORANDUM", set_="cabinet", react="smug", react_at=4.5, receiver_pose="idle",
           name="Admiral Henning von Holtzendorff", role="Chief of the Admiralty Staff", date="DECEMBER 1916")
    s = T("The odd thing is that Holtzendorff")
    sc(s, {"kind": "cabinet", "desk": False}, [
        AID("hz", "holtzendorff", 960, 1000, 1.6, "chin", "neutral", turn=0.3, keys=mv((r(s, "pushed into retirement"), {"pose": "shrug", "expr": "sad"}), (r(s, "Now he was"), {"pose": "fist", "expr": "determined"})))],
       [SHOT(0, "hz", "medium"), SHOT(r(s, "Now he was"), "hz", "close", frameX=-0.12)], tint="sepia")
    s = T("His argument was simple")
    MAP(s, [-10, 52], 40, [{"kind": "route", "path": [[-40, 45], [-15, 48.5], [-5, 50.2]], "color": "#3a6ea5", "width": 5, "icon": "freighter", "trail": 3, "gap": 80, "iconSize": 1.1, "enter": "draw", "dur": 3.0, "in": 0.2},
                           {"kind": "burst", "at": [-12, 49.5], "size": 0.6, "in": 1.8}, {"kind": "burst", "at": [-7, 51], "size": 0.6, "in": 2.6},
                           city("London", tag=True), L("6 MONTHS", 1400, 300, "red", 48, at=r(s, "within six months"))],
        colors=ATL, legend=LEG_ATL)
    s = T("Within six months, England will be forced")
    quote(s, "holtzendorff", "\"Within six months, England will be forced to sue for peace.\"", set_="cabinet", pose="explain", expr="smug", tag="MEMORANDUM · DEC 1916")
    s = T("The generals agreed")
    hq(s, [("hin", "hindenburg", "idle", "determined", mv((1.2, {"pose": "cross"}))), ("lud", "ludendorff", "explain", "smug", mv((r(s, "They simply calculated"), {"pose": "shrug"})))],
       set_="warroom", talk=1, cuts=[(r(s, "They knew perfectly well"), "hin", "close"), (r(s, "They simply calculated"), "lud", "close")])
    s = T("And it was not a crazy calculation")
    march_col(s, "ww1_american", n=3, set_="countryside", direction=1, expr="neutral", dur=6.0, close=None, date="1916")
    SCENES[-1]["elements"].append(CNT(0, 100000, 1400, 220, at=r(s, "a little over a hundred thousand"), prefix="≈", suffix=" REGULARS", size=70, dur=1.2, hud=True))

    s = T("On the 9th of January, 1917")
    sc(s, {"kind": "conference", "desk": False, "fg": "officedesk"}, [
        AID("k", "kaiser_wilhelm", 960, 1000, 1.55, "idle", "neutral", turn=0, keys=mv((r(s, "the Kaiser approved it"), {"pose": "write", "holds": "pen", "expr": "determined"}))),
        AID("hin", "hindenburg", 560, 1000, 1.5, "idle", "determined", turn=0.5), AID("hz", "holtzendorff", 1360, 1000, 1.5, "present", "smug", turn=-0.5),
        {**PROP("paper", 980, 872, 0.7), "rotate": 80}],
       [SHOT(0, ["hin", "k", "hz"], "medium"), SHOT(r(s, "the Kaiser approved it") - 0.3, "k", "close", frameX=-0.1)],
       date="9 JANUARY 1917", place="PLESS CASTLE, SILESIA", letterbox="DRAMATISED — PLESS, 9 JANUARY 1917")
    s = T("From the 1st of February")
    doc(s, "order", "FROM 1 FEBRUARY 1917", ["Unrestricted submarine warfare", "around Britain.", "Without warning. Neutral or not."], speed=40)
    s = T("New timetable")
    glass(s, level=0.0, plaque="SIX MONTHS")

    s = T("A week after Pless")
    sc(s, {"kind": "office", "desk": False, "fg": "officedesk", "flag": "GERI"}, [
        AID("z", "zimmermann", 980, 1000, 1.6, "write", "smug", holds="pen", turn=-0.2, keys=mv((r(s, "If America entered"), {"pose": "explain", "holds": "", "talk": True}))),
        NC("Arthur Zimmermann", "German Foreign Secretary", at=0.5)],
       [SHOT(0, "z", "medium", frameX=0.1), SHOT(r(s, "If America entered"), "z", "close", frameX=-0.12)], date="JANUARY 1917")
    s = T("If America entered the war")
    MAP(s, [-95, 30], 40, [city("Washington", at=0.2), city("Mexico City", at=0.2),
                           arrow(["Mexico City", [-104.0, 31.5]], "#c8352b", at=r(s, "the return of Texas"), dur=1.4, dashed=True),
                           L("TEXAS · NEW MEXICO · ARIZONA?", 760, 260, "tag", 36, at=r(s, "the return of Texas") + 0.3)],
        colors=ATL, legend=[("USA", "United States"), ("NEUTRAL", "Mexico")], hatch=())
    s = T("The employment of ruthless submarine warfare")
    doc(s, "telegram", "ZIMMERMANN TELEGRAM · 16 JAN 1917", ["THE EMPLOYMENT OF RUTHLESS", "SUBMARINE WARFARE NOW PROMISES", "TO COMPEL ENGLAND TO MAKE", "PEACE IN A FEW MONTHS."], speed=40)
    s = T("British intelligence intercepted it")
    sc(s, {"kind": "codebreak", "fg": "officedesk"}, [
        AID("c1", "civilian_man", 860, 1000, 1.55, "write", "neutral", holds="pen", turn=0.3, look_={"glasses": "round"}, keys=mv((2.0, {"pose": "pointUp", "expr": "happy", "holds": ""}))),
        AID("c2", "ww1_british", 1300, 1000, 1.5, "idle", "neutral", turn=-0.4, keys=mv((2.4, {"expr": "shocked", "pose": "head"})))],
       [SHOT(0, ["c1", "c2"], "medium"), SHOT(1.8, "c1", "close", frameX=-0.12)], place="ROOM 40, LONDON")
    s = T("Americans were furious")
    doc(s, "newspaper", "MARCH 1917", ["GERMANY SEEKS ALLIANCE WITH MEXICO", "ZIMMERMANN ADMITS IT"], speed=40)
    s = T("Mexico's own generals")
    sc(s, {"kind": "tent", "fg": "officedesk"}, [
        AID("g1", "civilian_man", 760, 1000, 1.5, "chin", "neutral", look_={"hat": "fedora", "hatColor": "#b59a64", "facial": "walrus", "outfit": "tunic", "color": "#7a7a58"}, keys=mv((2.0, {"pose": "shrug", "expr": "smug"}))),
        AID("g2", "civilian_man", 1200, 1000, 1.5, "cross", "smug", look_={"hat": "kepi", "hatColor": "#5a5a48", "facial": "handlebar", "outfit": "tunic", "color": "#7a7a58"}, keys=mv((2.4, {"headMove": "shake"})))],
       [SHOT(0, ["g1", "g2"], "medium"), SHOT(2.2, "g2", "close", frameX=0.1)], tint="warm")
    SCENES[-1]["elements"].append(ST("HOPELESS", 960, 300, r(s, "hopeless"), size=80))

    s = T("On the 2nd of April, Woodrow Wilson")
    sc(s, {"kind": "parliament", "drift": 0}, [
        AID("w", "wilson", 960, 1000, 1.5, "talk", "determined", talk=True, keys=mv((2.0, {"pose": "fist"}))),
        *[AID(f"c{i}", "congressman", 300 + i * 440, 1130, 1.5, "idle", "neutral", view="back", fixedLayer=True) for i in range(4)]],
       [SHOT(0, None, None, zoom=1.0, push=0.04), SHOT(r(s, "asked for a declaration"), "w", "mediumclose", frameX=0.1)], date="2 APRIL 1917", place="CONGRESS, WASHINGTON")
    s = T("The world must be made safe")
    quote(s, "wilson", "\"The world must be made safe for democracy.\"", set_="parliament", pose="fist", expr="determined", tag="QUOTE · 2 APRIL 1917")
    s = T("On the 6th of April, 1917")
    sc(s, {"kind": "parliament", "drift": 0}, [
        *[AID(f"c{i}", "congressman", 380 + i * 380, 1000, 1.45, ["cheer", "fist", "raise", "wave"][i], ["happy", "determined", "smile", "laugh"][i],
              look_={"age": [0.6, 0.4, 0.75, 0.5][i], "glasses": ["none", "round", "pince", "none"][i], "facial": ["walrus", "none", "beard", "pencil"][i]},
              keys=mv((0.4 + i * 0.35, {"pose": ["raise", "cheer", "fist", "cheer"][i]}))) for i in range(4)],
        {"kind": "flag", "nation": "USA", "x": 960, "y": 300, "w": 300, "h": 190}],
       [SHOT(0, ["c0", "c3"], "full"), SHOT(2.0, "c1", "close", frameX=0.1)], date="6 APRIL 1917")
    s = T("For a while, it looked as though")
    sinking(s, ship="cargo", nation="UK", hit=1.0)
    SCENES[-1]["elements"].append(CNT(0, 6000000, 1500, 220, at=r(s, "more than six million tons"), prefix="> ", suffix=" TONS", size=60, dur=1.2, hud=True))
    s = T("But the British began sailing")
    MAP(s, [-15, 50], 40, [{"kind": "route", "path": [[-60, 42], [-30, 47], [-10, 50], [-4, 51]], "color": "#3a6ea5", "width": 5, "icon": "freighter", "trail": 6, "gap": 55, "iconSize": 1.0, "enter": "draw", "dur": 4.0, "in": 0.2},
                           {"kind": "route", "path": [[-60, 41], [-30, 46.2], [-10, 49.2], [-4, 50.3]], "color": "#2b4d7a", "width": 3, "icon": "warship", "trail": 2, "gap": 160, "iconSize": 0.9, "nation": "UK", "enter": "draw", "dur": 4.0, "in": 0.4},
                           L("CONVOYS", 960, 160, "tag", 44, at=0.8)], colors=ATL, legend=LEG_ATL, date="1917")
    s = T("Britain did not ask for peace")
    glass(s, level=0.0, to=1.0, dur_fall=5.0, plaque="SIX MONTHS", cut_host=r(s, "It didn't ask at all"))
    s = T("Sir, so this is the one?")
    duo(s, [(0.0, "aide", "explain", "neutral"), (r(s, "Maybe"), "host", "chin", "neutral"), (r(s, "I'm putting this stamp"), "host", "show!", "smug"),
            (r(s, "Because there's one moment"), "host", "point", "determined")], holds="paper")

    # ================================================================ CHAPTER 6 — Brest-Litovsk
    s = T("While America was declaring war")
    sc(s, {"kind": "street", "weather": "snow", "drift": 0}, [
        *[{**AID(f"r{i}", "ww1_russian" if i % 2 else "worker", 300 - i * 230, 980 - (i % 2) * 40, None, "cheer" if i % 2 else "fist", "shout", keys=mv((6.0, {"x": 900 - i * 230, "ease": "linear"})))} for i in range(5)],
        {"kind": "flag", "nation": "NEUTRAL", "out": 0, "x": 1500, "y": 420, "w": 220, "h": 140}],
       [SHOT(0, None, "wide", zoom=1.0, panX=100), SHOT(3.0, "r0", "mediumclose", track=True)], world={"scale": 1.2, "y": 960},
       chapter="The Glass Turns", date="1917", place="PETROGRAD", tint="cold")
    s = T("The German high command even helped")
    sc(s, {"kind": "railway", "drift": 0}, [
        {"id": "tr", "kind": "vehicle", "type": "train", "nation": "GERI", "x": -700, "y": 900, "scale": 2.0, "keys": mv((7.0, {"x": 1200}))},
        AID("len", "lenin", 1550, 1000, 1.6, "idle", "smug", turn=-0.5, **{"in": 0.0}, keys=mv((r(s, "Lenin's Bolsheviks") + 0.3, {"pose": "hips"})))],
       [SHOT(0, None, "wide", zoom=1.0), SHOT(r(s, "Lenin's Bolsheviks"), "len", "mediumclose", frameX=0.14)], place="SWITZERLAND → RUSSIA")
    SCENES[-1]["elements"].append(NC("Vladimir Lenin", "Bolshevik leader", at=r(s, "Lenin's Bolsheviks") + 0.2))
    s = T("In November, the Bolsheviks seized power")
    sc(s, {"kind": "podium", "drift": 0}, [
        AID("len", "lenin", 960, 960, 1.6, "point", "determined", talk=True, keys=mv((r(s, "Lenin's first act"), {"pose": "fist"}))),
        {"kind": "flag", "nation": "NEUTRAL", "out": 0, "x": 1500, "y": 380, "w": 220, "h": 140}],
       [SHOT(0, "len", "medium", frameX=-0.1), SHOT(r(s, "a decree calling for peace"), "len", "close", frameX=0.12)], date="NOVEMBER 1917")
    s = T("By December, the guns had stopped")
    trench(s, "ww1_russian", n=3, action="wait", expr="tired", close=1.2, date="DECEMBER 1917", tint="cold")
    s = T("The peace talks dragged")
    MAP(s, [26, 53], 26, [front(EAST_FRONT, "#7a2a22", path2=[[24.5, 59.0], [28.5, 57.0], [31.0, 54.5], [31.5, 52.0], [32.5, 50.0], [33.5, 48.0], [34.0, 46.5]], morph_dur=5.0),
                          arrow([[24, 54], [29, 54.5]], "GERI", at=1.0, dur=1.6), arrow([[25, 50], [31, 50.4]], "GERI", at=1.4, dur=1.6)],
        colors=EUROPE, legend=LEG_CP, date="FEBRUARY 1918")
    s = T("On the 3rd of March, 1918")
    sc(s, {"kind": "conference", "desk": False, "fg": "officedesk"}, [
        AID("ru", "civilian_man", 700, 1000, 1.5, "write", "sad", holds="pen", turn=0.4, look_={"facial": "beard", "glasses": "pince"}),
        AID("de", "clerk_de", 1260, 1000, 1.5, "cross", "smug", turn=-0.5, keys=mv((2.6, {"pose": "hips"}))),
        {**PROP("paper", 760, 872, 0.7), "rotate": 80}],
       [SHOT(0, ["ru", "de"], "medium"), SHOT(2.0, "ru", "close", frameX=-0.12), SHOT(4.0, "de", "close", frameX=0.12)],
       date="3 MARCH 1918", place="BREST-LITOVSK")
    s = T("Russia gave up Poland")
    MAP(s, [28, 53], 30, [{"kind": "region", "polygon": BREST_LOSS, "color": "GERI", "fillOpacity": 0.45, "in": 0.4, "dashed": True},
                          city("Brest-Litovsk", tag=True, at=0.2), city("Kiev", at=1.0), city("Warsaw", at=0.6)],
        colors=EUROPE, legend=LEG_CP)
    s = T("Measured against the old Russian Empire")
    bars(s, "WHAT RUSSIA LOST (SHARE OF THE OLD EMPIRE)", [("Population", 33, "RUS", r(s, "a third of its population")), ("Industrial land", 55, "RUS", r(s, "more than half")),
                                                          ("Coalfields", 90, "RUS", r(s, "nine-tenths"))], 100, unit="%")
    s = T("A later agreement that summer")
    sc(s, {"kind": "paper", "dof": 0}, list(WOOD_DESK) + [{**PROP("coins", 960, 600, 2.2), "value": 9}, CNT(0, 6, 960, 300, at=0.4, suffix=" BILLION MARKS", size=90, dur=1.0)],
       [SHOT(0, None, None, zoom=1.0, push=0.05)])
    s = T("For Germany, this was everything")
    hq(s, [("hin", "hindenburg", "cheer", "happy", None), ("lud", "ludendorff", "fist", "smug", mv((2.0, {"pose": "rub"})))], set_="warroom", talk=1,
       cuts=[(2.4, "lud", "close")])
    s = T("The grain fields of Ukraine")
    sc(s, {"kind": "field", "drift": 0}, [
        {"id": "cart", "kind": "vehicle", "type": "cart", "nation": "GERI", "x": -300, "y": 860, "keys": mv((7.0, {"x": 900}))},
        AID("p", "civilian_man", 1400, 980, None, "carry", "tired", holds="crate", holdsText="GRAIN", keys=mv((6.0, {"x": 1000})))],
       [SHOT(0, None, "wide", zoom=1.0, panX=80), SHOT(3.0, "p", "mediumclose", frameX=0.1)], world={"scale": 1.2, "y": 960}, place="UKRAINE")
    s = T("Remember the turnip")
    host(s, "show", "smug", holds="turnip", keys=mv((1.6, {"pose": "explain", "holds": ""})), second=(r(s, "This was the turnip's answer"), "close", "host"))
    s = T("And around fifty German divisions")
    sc(s, {"kind": "railway", "drift": 0}, [
        {"id": "tr", "kind": "vehicle", "type": "train", "nation": "GERI", "x": 2600, "y": 900, "scale": 2.0, "flip": True, "keys": mv((6.0, {"x": 400}))},
        *[AID(f"s{i}", "ww1_german", 400 + i * 260, 1060, None, "shoulder", "determined", holds="rifle", keys=mv((6.0, {"x": 800 + i * 260, "ease": "linear"}))) for i in range(3)]],
       [SHOT(0, None, "wide", zoom=1.0), SHOT(2.6, "s1", "mediumclose", track=True)], world={"scale": 1.2, "y": 960})
    SCENES[-1]["elements"].append(L("≈ 50 DIVISIONS → WEST", 960, 985, "tag", 40, at=0.6, hud=True))
    s = T("Porter, give me a hand")
    glass(s, level=0.92, flip_at=r(s, "Germany's way") - 0.4, plaque="1918", cut_host=0.1)
    s = T("So, did the sand run out here? No.")
    glass(s, level=0.08, to=0.25, dur_fall=10, plaque="1918", stamp="TURNED BACK", stamp_at=r(s, "Here, it ran back") + 0.4, cut_host=r(s, "But this glass was smaller"))
    s = T("The Americans were coming")
    march_col(s, "ww1_american", n=6, set_="countryside", direction=1, expr="determined", dur=6.0, close=1.0)

    # ================================================================ CHAPTER 7 — spring 1918, the second Marne
    s = T("Ludendorff had decided on a great offensive")
    sc(s, {"kind": "warroom", "fg": "officedesk"}, [
        AID("lud", "ludendorff", 960, 1000, 1.6, "pointDown", "determined", turn=0.2, keys=mv((r(s, "He was not sure"), {"pose": "chin", "expr": "worried"}), (r(s, "He was sure he could not wait"), {"pose": "slam", "expr": "angry"})))],
       [SHOT(0, "lud", "medium", frameX=0.1), SHOT(r(s, "He was not sure"), "lud", "close", frameX=-0.12), SHOT(r(s, "He was sure he could not wait"), "lud", "mediumclose", frameX=0.1)],
       chapter="The Last Window", date="NOVEMBER 1917")
    s = T("On the 21st of March, 1918")
    trench(s, "ww1_british", n=3, action="cower", shells=((0.3, 700, 300), (0.9, 1300, 260), (1.6, 1000, 320)), close=1.4, date="21 MARCH 1918", place="THE SOMME")
    s = T("The Germans had found a new way to attack")
    battlefield(s, "ww1_german", n=5, direction=1, run=True, shells=((1.0, 1500, 800),), close=(r(s, "small groups"), "m1"), dur=9.0, tint=None)
    SCENES[-1]["elements"].append(L("STORMTROOPERS", 1560, 170, "tag", 40, at=r(s, "stormtroopers"), hud=True))
    s = T("It worked.")
    MAP(s, [2.9, 49.9], 5.6, [front(WESTERN_FRONT, "#7a2a22", path2=SPRING_1918, morph_dur=8.0), city("Paris", tag=True),
                              arrow([[3.4, 50.0], [2.6, 49.85]], "GERI", at=r(s, "codenamed Michael"), dur=1.6), L("MICHAEL", 1250, 470, "tag", 36, at=r(s, "codenamed Michael") + 0.8)],
        colors=WEST, legend=LEG_W, date="MARCH 1918")
    s = T("roll the British army back")
    march_col(s, "ww1_british", n=5, set_="mud", direction=-1, expr="worried", dur=6.0, close=1.6)
    s = T("When Michael slowed")
    MAP(s, [2.9, 49.9], 5.6, [front(SPRING_1918, "#5a5a52"), city("Paris", tag=True), city("Amiens"),
                              arrow([[3.0, 50.7], [2.7, 50.6]], "GERI", at=r(s, "in Flanders") - 0.2, dur=1.0),
                              arrow([[3.6, 49.45], [3.45, 49.1]], "GERI", at=r(s, "the river Aisne") - 0.2, dur=1.2),
                              arrow([[3.1, 49.6], [2.85, 49.5]], "GERI", at=r(s, "then another.") , dur=1.0),
                              L("FIVE OFFENSIVES · MARCH-JULY", 960, 160, "tag", 40, at=r(s, "Five in all"))],
        colors=WEST, legend=LEG_W, camera=[{"t": 0, "center": [2.9, 49.9], "zoom": 1.0}, {"t": r(s, "in Flanders") + 0.8, "center": [2.9, 50.4], "zoom": 1.25, "ease": "smooth"},
                                           {"t": r(s, "the river Aisne") + 0.8, "center": [3.3, 49.3], "zoom": 1.25, "ease": "smooth"},
                                           {"t": r(s, "Five in all") + 0.4, "center": [2.9, 49.9], "zoom": 1.0, "ease": "smooth"}])
    s = T("Together, they made the deepest advances")
    MAP(s, [2.9, 49.4], 5.2, [front(SPRING_1918, "#5a5a52"), city("Paris", tag=True), city("Château-Thierry", side="left"),
                              {"kind": "line", "path": [PL["Château-Thierry"], PL["Paris"]], "color": "#7a2a22", "dashed": True, "in": r(s, "By the 3rd of June"), "enter": "draw", "dur": 1.2, "width": 5},
                              L("56 KM", 1020, 520, "red", 44, at=r(s, "fifty-six kilometres"))], colors=WEST, legend=LEG_W, date="3 JUNE 1918")
    s = T("And yet.")
    host(s, "stop", "neutral", keys=mv((1.2, {"pose": "explain"})))
    s = T("The offensive had no clear strategic aim")
    sc(s, {"kind": "warroom", "fg": "officedesk"}, [
        AID("lud", "ludendorff", 960, 1000, 1.6, "pointDown", "worried", turn=0.0, keys=mv((2.0, {"pose": "pointL"}), (3.6, {"pose": "point"}), (5.2, {"pose": "chin"}))),
        L("TARGET OF THE WEEK", 960, 160, "tag", 40, at=1.0)],
       [SHOT(0, "lud", "medium"), SHOT(3.4, "lud", "close", frameX=-0.12)])
    s = T("Capturing a really decisive objective")
    MAP(s, [2.4, 50.2], 4.5, [front(SPRING_1918, "#5a5a52"), city("Amiens", tag=True, at=0.6), {"kind": "ring", "at": PL["Amiens"], "r": 60, "in": 1.0}],
        colors=WEST, legend=LEG_W)
    s = T("The stormtroopers were the best men")
    battlefield(s, "ww1_german", n=4, direction=1, shells=((0.6, 900, 800), (1.8, 1300, 840)), close=(1.4, "m0"), dur=6.0, tint="grey")
    s = T("Supplies couldn't keep up")
    sc(s, {"kind": "mud", "drift": 0}, [
        {"id": "cart", "kind": "vehicle", "type": "cart", "nation": "GERI", "x": 700, "y": 880, "moving": False},
        AID("d", "ww1_german", 1080, 960, None, "beg", "tired", turn=-0.4, keys=mv((2.2, {"pose": "head"}))),
        AID("d2", "ww1_german", 1380, 940, None, "idle", "sad", turn=-0.6)],
       [SHOT(0, None, "wide", zoom=1.0), SHOT(2.0, "d", "close", frameX=0.1)], world={"scale": 1.2, "y": 960})
    SCENES[-1]["elements"].append(L("≈130,000 LOST EACH SIDE (ONE PHASE)", 960, 160, "tag", 36, at=r(s, "each side lost"), hud=True))

    s = T("Germany could not afford that trade")
    bars(s, "GERMAN MANPOWER, PER MONTH", [("Needed", 200000, "GERI", r(s, "two hundred thousand")), ("Recovered wounded", 75000, "#8a8f8c", r(s, "seventy or eighty")),
                                           ("Class of 18-year-olds (a year)", 300000, "#b9b2a6", r(s, "three hundred thousand"))], 300000)
    s = T("Ludendorff admitted in private")
    sc(s, {"kind": "warroom", "fg": "officedesk"}, [
        AID("lud", "ludendorff", 960, 1000, 1.6, "head", "worried", turn=0.2, keys=mv((r(s, "He still wouldn't give up"), {"pose": "slam", "expr": "angry"})))],
       [SHOT(0, "lud", "close", frameX=0.1), SHOT(r(s, "He still wouldn't give up"), "lud", "medium", frameX=-0.1)])
    s = T("Now remember Admiral Holtzendorff's six months")
    glass(s, level=1.0, plaque="SIX MONTHS", cut_host=1.2)
    s = T("In June 1917, six months after Pless")
    sc(s, {"kind": "dock", "drift": 0}, [
        {"id": "ship", "kind": "vehicle", "type": "cargo", "nation": "USA", "x": 1300, "y": 640, "scale": 0.75},
        *[{**AID(f"u{i}", "ww1_american", 1050 - i * 230, 980, 1.35, "shoulder", "determined", holds="rifle", keys=mv((9.0, {"x": 1050 - i * 230 - 700, "ease": "linear"}))), "flip": True} for i in range(6)],
        CNT(14000, 1000000, 1450, 230, at=r(s, "By May 1918"), suffix=" IN FRANCE", size=64, dur=2.0, hud=True)],
       [SHOT(0, None, None, zoom=1.0, push=0.03), SHOT(r(s, "By May 1918") + 0.5, "u1", "mediumclose", frameX=0.1, track=True)], place="SAINT-NAZAIRE, FRANCE")
    SCENES[-1]["elements"].append(L("14,000", 960, 985, "tag", 44, at=r(s, "only fourteen thousand"), out=r(s, "By May 1918") - 0.1, hud=True))
    s = T("By June, they were arriving at the rate")
    MAP(s, [-35, 45], 70, [{"kind": "route", "path": [[-74, 40.7], [-45, 44], [-20, 46.5], [-4.5, 48.4]], "color": "#3a6ea5", "width": 5, "icon": "freighter", "trail": 8, "gap": 45, "iconSize": 1.0, "nation": "USA", "enter": "draw", "dur": 5.0, "in": 0.2},
                           city("New York", at=0.2), city("Brest", at=0.4, side="left"), L("10,000 A DAY", 960, 160, "red", 48, at=0.6)], colors=ATL, legend=LEG_ATL, hatch=())
    s = T("In 1916, the whole American army")
    bars(s, "AMERICAN SOLDIERS", [("Regular army, 1916", 100000, "#8aa3c4", 0.4), ("Crossed the Atlantic by 1918", 2000000, "USA", r(s, "two million"))], 2000000)
    s = T("The submarines hadn't starved Britain")
    fleet(s, ships=(("cargo", "USA", 500, 700, 1), ("destroyer", "USA", 1350, 640, 1)), dur=6)
    s = T("By July, Germany's lead")
    bars(s, "DIVISIONS ON THE WESTERN FRONT, JULY 1918", [("Germany", 207, "GERI", r(s, "two hundred and seven")), ("Allies", 203, "FRA", r(s, "two hundred and three"))], 210)
    s = T("Sir, ten thousand a day")
    duo(s, [(0.0, "aide", "explain", "shocked"), (r(s, "More than one, Porter"), "host", "talk", "smug"), (r(s, "And all of them on time"), "host", "show!", "smug")])

    s = T("On the 15th of July, 1918")
    battlefield(s, "ww1_german", n=5, direction=1, run=True, shells=((1.2, 1300, 800), (2.4, 800, 860)), close=(2.4, "m1"), dur=6.0, date="15 JULY 1918", place="REIMS")
    s = T("On the 18th of July, the new Allied supreme commander")
    sc(s, {"kind": "warroom", "fg": "officedesk"}, [
        AID("foch", "foch", 980, 1000, 1.6, "pointDown", "determined", turn=-0.2, keys=mv((r(s, "hit back"), {"pose": "fist", "expr": "angry"}))),
        NC("General Ferdinand Foch", "Allied Supreme Commander", at=0.4)],
       [SHOT(0, "foch", "medium", frameX=0.1), SHOT(r(s, "hit back") - 0.2, "foch", "close", frameX=-0.12)], date="18 JULY 1918")
    s = T("Two dozen French divisions")
    battlefield(s, "ww1_french", n=4, direction=-1, tanks=("renault", 3), tank_nation="FRA", close=(r(s, "broke into the German flank"), "t0"), dur=9.0)
    s = T("The Germans had to retreat")
    MAP(s, [3.4, 49.2], 3.6, [front([[2.9, 49.5], [3.1, 49.25], [3.4, 49.05], [3.95, 49.1], [4.1, 49.25]], "#5a5a52",
                                    path2=[[2.95, 49.55], [3.3, 49.4], [3.7, 49.3], [4.0, 49.25], [4.1, 49.3]], morph_dur=4.0),
                              arrow([[3.0, 49.0], [3.4, 49.25]], "FRA", at=0.5, dur=1.6), city("Château-Thierry", side="left"), city("Soissons"), city("Reims")],
        colors=WEST, legend=LEG_W, rivers=["Marne", "Aisne"])
    s = T("Almost four years after the first battle")
    host(s, "explain", "neutral", label="THE MARNE · 1914 / 1918", keys=mv((2.0, {"pose": "chin"})))
    s = T("So, did the sand run out here? Yes.")
    glass(s, level=0.82, to=1.0, dur_fall=3.0, plaque="1918", stamp="TURNED", stamp_at=r(s, "Yes.") + 0.4, cut_host=r(s, "It never attacked"))
    s = T("From here on, the only question")
    trench(s, "ww1_german", n=3, action="wait", expr="tired", close=2.0, tint="grey")

    # ================================================================ CHAPTER 8 — Amiens
    s = T("They didn't have to wait long")
    sc(s, {"kind": "field", "time": "dawn", "drift": 0, "weather": None}, [
        *[{"id": f"t{i}", "kind": "vehicle", "type": "markiv", "nation": "UK", "x": -300 - i * 600, "y": 760 + i * 50, "keys": mv((9.0, {"x": 500 - i * 600}))} for i in range(3)],
        *[AID(f"a{i}", "ww1_australian" if i % 2 else "ww1_canadian", 200 - i * 200, 900 + (i % 2) * 60, None, "port", "determined", holds="rifle", keys=mv((9.0, {"x": 820 - i * 200, "ease": "linear"}))) for i in range(4)]],
       [SHOT(0, None, "wide", zoom=1.0, push=0.03), SHOT(r(s, "the British Fourth Army attacked") + 1.0, "t0", "full", track=True)],
       world={"scale": 1.0, "y": 900}, chapter="The Black Day", date="8 AUGUST 1918", place="AMIENS")
    s = T("with the Australian Corps under General John Monash")
    hq(s, [("mon", "monash", "pointDown", "determined", mv((1.8, {"pose": "explain"}))), ("cur", "currie", "idle", "smug", mv((r(s, "Arthur Currie"), {"pose": "cross"})))],
       set_="tent", talk=0, cuts=[(0.6, "mon", "mediumclose"), (r(s, "Arthur Currie"), "cur", "mediumclose")])
    SCENES[-1]["elements"] += [NC("General John Monash", "Australian Corps", at=0.4, out=r(s, "Arthur Currie") - 0.2), NC("General Arthur Currie", "Canadian Corps", at=r(s, "Arthur Currie") + 0.1)]
    s = T("The plan was built largely by Monash")
    sc(s, {"kind": "workshop"}, [{"kind": "timeline", "x": 960, "y": 560, "width": 1400, "items": [
        {"sub": "TANKS", "label": "go with the infantry", "at": 0.15, "color": "UK", "in": r(s, "tanks")},
        {"sub": "AIRCRAFT", "label": "overhead", "at": 0.5, "color": "UK", "in": r(s, "aircraft")},
        {"sub": "ARTILLERY", "label": "timed, no warning", "at": 0.85, "color": "UK", "in": r(s, "carefully timed artillery")}]},
        L("TRIED AT HAMEL, JULY 1918", 960, 160, "tag", 38, at=r(s, "at Hamel"))], [SHOT(0, None, None, zoom=1.0, push=0.05)])
    s = T("This time there was no long bombardment")
    battlefield(s, "ww1_australian", n=4, direction=1, tanks=("markiv", 2), shells=((r(s, "The guns opened up"), 1500, 760), (r(s, "The guns opened up") + 0.4, 1700, 820)),
                close=(r(s, "around six hundred tanks"), "t0"), dur=9.0)
    s = T("On the first day, the Allies advanced")
    MAP(s, [2.6, 49.85], 2.4, [front([[2.45, 50.1], [2.5, 49.85], [2.55, 49.65]], "#5a5a52", path2=[[2.65, 50.1], [2.72, 49.85], [2.68, 49.65]], morph_dur=4.0),
                               city("Amiens", tag=True), arrow([[2.45, 49.85], [2.62, 49.86]], "UK", at=0.5, dur=2.0), L("≈ 11 KM IN ONE DAY", 960, 260, "tag", 38, at=1.6)], colors=WEST, legend=LEG_W)
    s = T("Whole groups of German soldiers simply gave up")
    battlefield(s, "ww1_canadian", n=3, direction=1, surrender=4, dur=6.0, close=(1.6, "g0"))
    s = T("Ludendorff later gave the day a name")
    sc(s, {"kind": "warroom", "fg": "officedesk"}, [AID("lud", "ludendorff", 960, 1000, 1.6, "head", "shocked", turn=0.1, keys=mv((1.5, {"pose": "facepalm", "expr": "sad"})))],
       [SHOT(0, "lud", "medium"), SHOT(1.2, "lud", "close")])
    s = T("The black day of the German Army")
    quote(s, "ludendorff", "\"The black day of the German Army.\"", set_="warroom", pose="head", expr="sad", tag="QUOTE · LUDENDORFF")
    s = T("It wasn't the ground lost that frightened him")
    battlefield(s, "ww1_german", n=0, surrender=5, dur=6.0, close=(1.2, "g1"), tint="grey")
    s = T("Over the following weeks")
    MAP(s, [3.4, 50.0], 6.0, [front(SPRING_1918, "#5a5a52", path2=HINDENBURG, morph_dur=6.0), city("St Quentin", tag=True), city("Amiens"),
                              {"kind": "burst", "at": PL["St Quentin"], "size": 0.6, "in": r(s, "broke through it")}],
        colors=WEST, legend=LEG_W, date="AUGUST-SEPTEMBER 1918")
    s = T("And that was the same day Hindenburg and Ludendorff")
    sc(s, {"kind": "cabinet", "desk": False, "fg": "officedesk"}, [
        AID("kaiser", "kaiser_wilhelm", 1150, 1000, 1.55, "idle", "neutral", turn=-0.5, keys=mv((r(s, "two hours"), {"expr": "shocked", "pose": "head"}))),
        AID("hin", "hindenburg", 520, 1000, 1.55, "idle", "sad", turn=0.5), AID("lud", "ludendorff", 800, 1005, 1.5, "talk", "worried", talk=True, turn=0.55)],
       [SHOT(0, ["hin", "lud", "kaiser"], "full"), SHOT(r(s, "two hours") - 0.3, "kaiser", "close", frameX=0.12)], clock="2 HOURS", date="29 SEPTEMBER 1918", tint="sepia")
    s = T("That's the moment we started with")
    host(s, "point", "neutral", keys=mv((1.6, {"pose": "explain"})))
