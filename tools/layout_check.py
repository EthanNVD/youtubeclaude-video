"""Layout + motion checks used by validate_plan.py.

overlaps(scene)  -> list of warnings: on-screen text boxes that collide with each other, with the
                    reserved badge zones (date/place top-left, clock top-right, name card bottom-left)
                    or with an actor's face.
speeds(scene)    -> list of warnings: vehicles moving faster than their type plausibly can.
proportions(scene) -> list of warnings: a vehicle much smaller/larger than the people at the same depth
                    (mirror of src/lib/depth.ts; keep the two tables in sync).

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
    "markiv": 160, "renault": 220, "tank": 420, "sherman": 420, "panzer4": 400, "tiger": 320, "t34": 450, "panther": 420, "stug": 400,
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
        s = max(0.05, effective_scale(scene, el))
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
            s = max(0.05, effective_scale(sc, el))
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


# ------------------------------------------------------------------ depth / proportions (mirror of src/lib/depth.ts)
PERSON_H = 300
VEH = {  # type: (native height, native length, match by, target size in person heights)
    "sherman": (203, 481, "h", 1.15), "tank": (193, 501, "h", 1.12), "tank_flat": (193, 501, "h", 1.12), "tiger": (213, 585, "h", 1.22),
    "markiv": (222, 568, "h", 1.3), "renault": (196, 290, "h", 1.1),
    "panther": (197, 585, "h", 1.18), "panzer4": (187, 525, "h", 1.08), "t34": (185, 511, "h", 1.05), "stug": (156, 485, "h", 0.9),
    "halftrack": (158, 397, "h", 0.98), "truck": (211, 425, "h", 1.32), "jeep": (155, 287, "h", 0.82), "car": (155, 287, "h", 0.85),
    "artillery": (140, 414, "h", 0.78), "gun": (140, 414, "h", 0.78), "train": (209, 395, "h", 1.8), "locomotive": (209, 395, "h", 1.8),
    "wagon": (209, 395, "h", 1.7), "traincar": (209, 395, "h", 1.7), "horse": (217, 275, "h", 1.05), "cart": (217, 462, "h", 1.05),
    "fighter": (120, 320, "L", 3.6), "plane": (120, 320, "L", 3.6), "divebomber": (120, 320, "L", 4.0), "bomber": (175, 509, "L", 7.0),
    "dakota": (199, 656, "L", 7.0), "transport": (199, 656, "L", 7.0), "glider": (135, 576, "L", 7.0), "boat": (171, 259, "L", 2.4),
    "assaultboat": (91, 302, "L", 2.6),
}
SET_HORIZON = {
    "field": 600, "countryside": 600, "steppe": 600, "snow": 600, "desert": 600, "mud": 600, "polder": 620, "heath": 600,
    "airfield": 620, "river": 470, "beach": 520, "sea": 560, "ocean": 560, "harbor": 560, "dock": 560, "railway": 640,
    "station": 640, "trench": 420, "jungle": 500, "city": 760, "street": 760, "ruins": 760, "archbridge": 560, "garden": 600, "hotel": 640,
}


def horizon(scene):
    w, st = scene.get("world") or {}, scene.get("set") or {}
    if w.get("horizon") is not None:
        return w["horizon"]
    if isinstance(st.get("horizon"), (int, float)):
        return st["horizon"]
    if isinstance(st.get("dyke"), (int, float)):
        return st["dyke"]
    return SET_HORIZON.get(st.get("kind", ""), 560)


def person_scale_at(scene, y):
    w = scene.get("world") or {}
    hz = horizon(scene)
    return max(0.03, w.get("scale", 1.45) * (y - hz) / max(1, w.get("y", 900) - hz))


def vehicle_scale_for(vtype, ps, mult=1.0):
    v = VEH.get(vtype)
    if not v:
        return ps * 0.6 * mult
    native = v[0] if v[2] == "h" else v[1]
    return v[3] * PERSON_H * ps / native * mult


def effective_scale(scene, el):
    """the scale the engine will use (explicit, or from the depth model)"""
    if el.get("scale") is not None:
        return float(el["scale"])
    if scene.get("world") and el.get("kind") in ("actor", "vehicle", "crowd") and el.get("at") is None:
        ps = person_scale_at(scene, el.get("y", 900)) * el.get("depthScale", 1)
        if el["kind"] == "vehicle":
            return vehicle_scale_for(el.get("type", "tank"), ps, (scene.get("world") or {}).get("vehicles", 1))
        return ps
    return 1.0


AIR = {"fighter", "plane", "divebomber", "bomber", "dakota", "transport", "glider"}


def proportions(scene, tol=0.42):
    """Vehicles on the ground next to people: compare each vehicle's size with the size it should have for the people
    in the shot, carried to the vehicle's depth by the ground-plane perspective. Flying aircraft are skipped."""
    if scene.get("type") != "stage":
        return []
    els = scene.get("elements", [])
    actors = [e for e in els if e.get("kind") in ("actor", "crowd") and e.get("at") is None and not e.get("seated") and e.get("view") != "back"]
    if not actors:
        return []
    hz = horizon(scene)
    out = []
    for j, v in enumerate(els):
        if v.get("kind") != "vehicle" or v.get("at") is not None or v.get("type") not in VEH:
            continue
        vy = v.get("y", 900)
        if v.get("type") in AIR and vy < hz + 40:
            continue  # in the sky
        if vy <= hz + 10:
            continue
        # people standing near the vehicle's depth say most about its size
        near = sorted(actors, key=lambda a: abs(a.get("y", 900) - vy))[:3]
        exp = []
        for a in near:
            ay = a.get("y", 900)
            if ay <= hz + 10:
                continue
            ps = effective_scale(scene, a) * (vy - hz) / (ay - hz)
            exp.append(vehicle_scale_for(v["type"], ps))
        if not exp:
            continue
        want = sum(exp) / len(exp)
        have = effective_scale(scene, v)
        r = have / max(1e-6, want)
        if r < 1 - tol or r > 1 + tol * 1.6:
            what = "too small" if r < 1 else "too large"
            out.append(f"{scene['id']}.e{j}(vehicle {v['type']}): {what} next to the people at that depth (scale {have:.2f}, ~{want:.2f} expected) — "
                       f"use scene.world + no scale, or scale ≈ {want:.2f}")
    return out
