"""Layout + motion checks used by validate_plan.py.

overlaps(scene)  -> list of warnings: on-screen text boxes that collide with each other, with the
                    reserved badge zones (date/place top-left, clock top-right, name card bottom-left)
                    or with an actor's face.
speeds(scene)    -> list of warnings: vehicles moving faster than their type plausibly can.

Boxes are estimates from the same formulas the components use (Label, Stamp, Headline, Counter,
Document, NameCard, DateBadge). Map-anchored items (`at`) are skipped (they need the projection).
"""
from __future__ import annotations

COND = 0.52   # Oswald condensed width per char (Label)
HEAVY = 0.5   # Anton width per char (Headline/Counter)


def _box_label(el):
    text = str(el.get("text", ""))
    lines = text.split("\n")
    size = el.get("size", 40)
    w = max(len(l) for l in lines) * size * (0.5 if el.get("style") in ("plain", "map") else COND) + 36
    h = len(lines) * size * 1.12 + 22
    x, y = el.get("x", 960), el.get("y", 540)
    return (x - w / 2, y, x + w / 2, y + h)


def _box_center(el, w, h):
    x, y = el.get("x", 960), el.get("y", 540)
    return (x - w / 2, y - h / 2, x + w / 2, y + h / 2)


def _scale(el):
    return float(el.get("scale", 1) or 1)


def box(el):
    k = el.get("kind")
    s = _scale(el)
    if k == "label":
        b = _box_label(el)
        if s != 1:
            x, y = el.get("x", 960), el.get("y", 540)
            b = (x + (b[0] - x) * s, y + (b[1] - y) * s, x + (b[2] - x) * s, y + (b[3] - y) * s)
        return b
    if k == "stamp":
        size = el.get("size", 90)
        return _box_center(el, len(str(el.get("text", ""))) * size * 0.6 + 60, size * 1.25)
    if k in ("headline", "text"):
        size = el.get("size", 130)
        w = len(str(el.get("text", ""))) * size * HEAVY
        x, y = el.get("x", 960), el.get("y", 540)
        return (x - w / 2, y - size * 0.85, x + w / 2, y + size * 0.15)
    if k == "counter":
        size = el.get("size", 110)
        txt = f"{el.get('prefix', '')}{el.get('to', 0):,}{el.get('suffix', '')}"
        w = len(txt) * size * 0.45
        x, y = el.get("x", 960), el.get("y", 540)
        return (x - w / 2, y - size * 0.85, x + w / 2, y + size * 0.15)
    if k == "document":
        return _box_center(el, el.get("w", 760) * s, el.get("h", 520) * s)
    if k == "namecard":
        name, role = str(el.get("name", "")), str(el.get("role", ""))
        w = max(len(name) * 30 + 60, len(role) * 19 + 60)
        return (70, 860, 70 + w, 860 + (126 if role else 82))
    return None


def face_box(el):
    """an actor's head region in screen space (origin at the feet, head centre ~206 px above at scale 1)"""
    s = _scale(el)
    x, y = el.get("x", 960), el.get("y", 900)
    return (x - 80 * s, y - 290 * s, x + 80 * s, y - 150 * s)


def _hit(a, b, pad=6):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])


def _live(el, dur):
    return (el.get("in", 0) or 0, el.get("out", dur) if el.get("out") is not None else dur)


def _overlap_time(a, b):
    return min(a[1], b[1]) - max(a[0], b[0]) > 0.15


TEXT = {"label", "stamp", "headline", "text", "counter", "document", "namecard"}


def overlaps(scene):
    sid = scene["id"]
    dur = scene["end"] - scene["start"]
    out = []
    items = []
    for j, el in enumerate(scene.get("elements", [])):
        if el.get("at") is not None or el.get("screen") is False:
            continue
        if el.get("kind") in TEXT:
            b = box(el)
            if b:
                items.append((j, el, b, _live(el, dur)))
    # badges (always visible for the whole shot)
    zones = []
    if scene.get("letterbox"):
        zones.append(("letterbox bar", (0, 0, 1920, 120)))
        zones.append(("letterbox bar", (0, 960, 1920, 1080)))
    elif scene.get("date"):
        zones.append(("date badge", (20, 30, 40 + max(160, len(scene["date"]) * 25 + 50), 130)))
    if scene.get("place") and not scene.get("letterbox"):
        y0 = 140 if scene.get("date") else 46
        zones.append(("place badge", (20, y0 - 16, 40 + max(160, len(scene["place"]) * 25 + 50), y0 + 84)))
    if scene.get("clock"):
        w = max(160, len(scene["clock"]) * 25 + 50)
        zones.append(("clock badge", (1900 - w - 20, 30, 1900, 130)))
    for i in range(len(items)):
        j, el, b, live = items[i]
        tag = f"{sid}.e{j}({el.get('kind')})"
        for name, z in zones:
            if _hit(b, z):
                out.append(f"{tag}: overlaps the {name} — move it (top-left/top-right corners are reserved)")
        for i2 in range(i + 1, len(items)):
            j2, el2, b2, live2 = items[i2]
            if el.get("kind") == "namecard" and el2.get("kind") == "namecard":
                continue
            if _overlap_time(live, live2) and _hit(b, b2):
                out.append(f"{tag} overlaps {sid}.e{j2}({el2.get('kind')}) — re-layout (text must never sit on text)")
    # text on faces
    for j, el in enumerate(scene.get("elements", [])):
        if el.get("kind") != "actor" or el.get("at") is not None:
            continue
        fb = face_box(el)
        for j2, el2, b2, live2 in items:
            if el2.get("kind") in ("namecard",):
                continue
            if _overlap_time(_live(el, dur), live2) and _hit(fb, b2, pad=-10):
                out.append(f"{sid}.e{j2}({el2.get('kind')}) covers the face of e{j}({el.get('who')}) — move the text")
    return out


# plausible top speeds in the vehicle's own drawing units per second (drawing ≈ 300–600 units long)
VMAX = {
    "tank": 420, "sherman": 420, "panzer4": 400, "tiger": 320, "t34": 450, "panther": 420, "stug": 400,
    "halftrack": 520, "truck": 650, "car": 800, "jeep": 800, "artillery": 300, "horse": 300, "cart": 260,
    "train": 700, "locomotive": 700, "wagon": 700, "traincar": 700,
    "boat": 260, "assaultboat": 220, "cargo": 180, "freighter": 180, "carrier": 160, "battleship": 160,
    "cruiser": 200, "destroyer": 240, "submarine": 180, "uboat": 180,
    "fighter": 2600, "plane": 2200, "divebomber": 2600, "bomber": 1600, "dakota": 1300, "transport": 1300, "glider": 1100,
}


def speeds(scene):
    sid = scene["id"]
    out = []
    for j, el in enumerate(scene.get("elements", [])):
        if el.get("kind") != "vehicle" or not el.get("keys"):
            continue
        vmax = VMAX.get(el.get("type", "tank"), 600)
        s = max(0.05, _scale(el))
        t0, x0 = 0.0, el.get("x")
        if x0 is None:
            continue
        for k in sorted(el["keys"], key=lambda k: k.get("t", 0)):
            if "x" not in k:
                continue
            dt = max(0.01, k["t"] - t0)
            # the default 'drive' profile peaks at 4/3 of the average speed
            v = abs(k["x"] - x0) / dt / s * (4 / 3 if not k.get("ease") or k.get("ease") == "drive" else 1)
            if v > vmax * 1.15:
                need = abs(k["x"] - x0) / s * (4 / 3) / vmax
                out.append(f"{sid}.e{j}(vehicle {el.get('type')}): moves {v:.0f} u/s (max ~{vmax}) — give it ≥ {need:.1f} s or a shorter path")
            t0, x0 = k["t"], k["x"]
    return out


def fix_speeds(plan, margin=0.85):
    """Shorten vehicle paths that exceed their type's top speed (timing is kept; the end point moves closer).
    Returns the number of keys changed."""
    n = 0
    for sc in plan.get("scenes", []):
        for el in sc.get("elements", []):
            if el.get("kind") != "vehicle" or not el.get("keys") or el.get("x") is None:
                continue
            vmax = VMAX.get(el.get("type", "tank"), 600) * margin
            s = max(0.05, _scale(el))
            t0, x0 = 0.0, el["x"]
            first = True
            for k in sorted(el["keys"], key=lambda k: k.get("t", 0)):
                if "x" not in k:
                    continue
                dt = max(0.01, k["t"] - t0)
                peak = 4 / 3 if not k.get("ease") or k.get("ease") == "drive" else 1
                limit = vmax * dt * s / peak
                if abs(k["x"] - x0) > limit:
                    if first:
                        # keep the destination the story needs; start the vehicle closer instead
                        el["x"] = round(k["x"] - (limit if k["x"] > x0 else -limit), 1)
                    else:
                        k["x"] = round(x0 + (limit if k["x"] > x0 else -limit), 1)
                    n += 1
                t0, x0 = k["t"], k["x"]
                first = False
    return n
