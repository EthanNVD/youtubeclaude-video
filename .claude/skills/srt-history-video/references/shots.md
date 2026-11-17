# Shot templates (`tools/shotlib.py`)

Proven compositions that already follow `docs/STYLE_GUIDE.md`:
- depth;
- slow camera;
- believable vehicle speeds;
- one text block per zone;
- badge corners kept free.

Use them as the first draft of a shot, then tune the timings to the cue words. Each template returns one scene dict. Its `at=`/key times are seconds from the scene start; the scene end is filled in by `Plan.finish()`.

```python
import sys; sys.path.insert(0, "tools")
from shotlib import *            # element builders + templates + Plan

P = Plan(end=VOICE_SECONDS)
P.add(host_talk(0.0, "WHY IT FAILED", aide=True, chapter="The Question"))
P.add(office_decision(12.4, "montgomery", reads="telegram", title="FROM SHAEF", react="angry", stamp="REFUSED", date="10 SEPTEMBER 1944"))
P.add(convoy(30.2, "sherman", "UK", n=3, set_="polder"))
P.add(map_convoy(41.0, [-40, 45], 80, ATLANTIC_ROUTE, icon="freighter", colors={"United States": "USA", "United Kingdom": "UK"}))
P.finish(META, CAST, "projects/<slug>/plan.json", letterbox={"s001": "DRAMATISED — ARNHEM, 17 SEPTEMBER 1944"})
```
`Plan.finish` sorts the scenes, tiles the timeline, numbers the ids, runs `layout_check.fix_speeds` and writes the JSON. Any extra keyword is copied onto the scene, such as `date`, `place`, `chapter`, `beat`, `camera`, `transition` or `tint`. Use `extra=[...]` to add elements.

| template | what the viewer sees | use for |
|---|---|---|
| `host_talk(start, label, set_, aide)` | narrator in his study talking to camera, aide reacting | hook, chapter turn, verdict |
| `office_decision(start, who, reads, title, react, stamp)` | leader behind a desk reads a telegram/folder, reacts on the key word, slams/points; optional stamp | orders, refusals, bad news |
| `two_shot(start, a, b, set_, speaker)` | over-the-shoulder conversation: A big in back view, B facing camera | arguments, meetings |
| `march(start, who, n, set_)` | a section marching with rifles shouldered | movement of infantry, arrivals |
| `convoy(start, vtype, nation, n, set_)` | a column already in frame drives on with drive easing | advances on a road, supply |
| `river_crossing(start, nation, boats)` | assault boats paddled across under fire, splashes, tracer | crossings |
| `air_drop(start, nation, planes)` | Dakotas cross the sky, paratroopers drift down | airborne landings |
| `map_advance(start, center, span, path, nation, towns, legend)` | arrow grows along the axis, towns appear before it arrives | where/how far |
| `map_convoy(start, center, span, path, icon, trail)` | ships/crates/trucks/tanks moving along a dashed route; camera follows | supply lines, convoys, movements |
| `front_shift(start, center, span, line_from, line_to, nation, pocket)` | front slides to a new line; a pocket shrinks | retreats, advances, encirclement |
| `tubes(start, title, items)` | glass tubes on a wooden plaque in the workroom | comparisons (strength, losses) |
| `corkboard(start, items, title)` | pinned cards on red yarn on a corkboard | dates, sequences, "a week before" |
| `document_insert(start, style, title, lines, stamp)` | a typed telegram/order/newspaper, stamped | evidence, quotes |
| `crew_with_vehicle(start, vtype, nation, who)` | vehicle parked mid-frame, commander in the hatch, crew talking by the front plate (people ≈ ⅓ of its length) | crews, briefings by a vehicle |
| `column_depth(start, vtype, nation)` | 3 depth planes: column on the far road, infantry marching mid-ground, one soldier close to camera watching | advances, scale of an army |
| `vehicle_pass(start, vtype, nation)` | a heavy vehicle crosses the foreground filling half the frame, camera pans/shakes, infantry tiny behind | menace, arrival of armour |
| `foreground_walk(start, who, vtype)` | soldiers walk past close to camera (waist-up), a truck drives in the middle distance | marches, retreats, "dramatised" moments |
| `airfield_line(start, nation, pilot)` | pilots walk past a parked fighter; a Dakota further back | airborne / air force chapters |

The depth templates (`crew_with_vehicle` … `airfield_line`) use `world` (depth model): no scales are written; sizes come from the ground y.

### Coverage templates (several set-ups inside one place — `scene.shots`)
Use these for every acting beat; see [acting-camera.md](acting-camera.md).

| template | set-ups | use for |
|---|---|---|
| `desk_read(start, who, item, name, role)` | wide: a messenger walks in and hands it over → medium: he reads → close: the reaction | reports, warnings, bad news arriving |
| `ots_dialogue(start, speaker, listener, side, holds)` | over the listener's shoulder onto the speaker in 3/4; flip `side` for the reverse line | dialogue, a commander receiving a report |
| `desk_insert(start, items, magnifier, rings, crosses)` | top-down wood desk: prints/forms, a magnifier pass, red-pencil rings and crosses on the words | evidence: photos, forms, maps, counts |
| `walk_to_camera(start, who, set_, holds)` | someone walks down a corridor toward the lens and grows | "he took them to his commander" |
| `walk_away(start, who, set_, holds)` | back view, walking away and getting smaller | leaving, dismissal, defeat |
| `vehicle_arrives(start, vtype, nation, who, parked)` | wide: a vehicle drives in and brakes, a soldier strolls over → full shot of the group | armour arriving, units in position |

Helpers:
- `SHOT(t, on, size, **kw)`: one set-up.
- `AID(id, who, x, y, s, …)`: an actor with an id; `s=None` = depth-sized.
- `WOOD_DESK`: insert background.
- `OFFICE`: an office with a foreground desk.

Worked example of a full minute: `projects/acting-test/build.py`.

Rules when adapting a template:
- Two to four set-ups per acting scene, cut on the reads. Never the same recipe for every scene.
- Keep vehicles inside the frame for most of the shot.
- Cap text at about 2 labels at a time, never in the badge corners.
- Have every actor change pose or expression every 1.5–3 s.

## Action recipes (battle scenes)
See [action.md](action.md) §2: `assault`, `shells`, `gun_crew`, `mg_nest`, `hit_and_help`, `stretcher_team`, `fallen`, `man_path` (all in `tools/shotlib.py`, for scenes with `world=WORLD`). Worked example: `projects/ww1-action-test/plan_src/build.py`.
