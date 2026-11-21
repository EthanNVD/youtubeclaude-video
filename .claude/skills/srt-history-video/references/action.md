# Action: screen-time mix, battle recipes, depth rules

Read this before planning any chapter. In a battle chapter, read it before writing each scene.
Proven on `projects/ww1-action-test/` (WW1 599–723 s: Verdun → the first tanks):
- **Action went from 43 % to 74 %** of the same narration.
- `plan_src/build.py` there is the worked example.

## 1. The mix (what the screen shows, per chapter)

> **Superseded targets (2026-11-21).** The film is now told like an animated documentary ([storytelling-film.md](storytelling-film.md)).
> The rule is no longer "action ≥ 55 %". It is:
>
> - every clause gets one concrete picture of what it says;
> - acted cards (action + talk) ≥ 75 % of every chapter;
> - maps ≤ 10 %;
> - documents/charts ≤ 10 %.
>
> Battle chapters still use the recipes below when the narration describes fighting.
> The classes and the per-chapter report described here still apply.

`validate` measures it.
- It prints `mix` for the film.
- It writes `work/mix.json` per chapter.
- It warns when a chapter is off target.

Classes (`tools/validate_plan.py: classify`):

| class | what counts |
|---|---|
| **action** | People or vehicles DOING something. They move (x/y keys), fire (`fireAt`/`fire`), fall (`fallAt`), lie (`lying`), run, or are under fire (bursts, muzzle, tracer on screen). |
| **talk** | People in place, gesturing, reacting. Generals at desks, quotes, dialogue. |
| **map** | Map scenes. |
| **device** | Documents, charts, counters, memorial cards with nobody acting. |
| **host** | The narrator (and aide). |

Targets:

| class | whole film | battle chapter (≥ 25 % of its time has combat on screen) |
|---|---|---|
| action | **40–45 %** (warn < 35 %) | **55–60 %+** (warn < 50 %) |
| talk | ≤ 15 % (every talk shot has business, see §4) | ≤ 10 % |
| map | 12–15 % (≤ 12 s per map, always moving) | ~10 % |
| device / docs / charts | 12–15 % | ≤ 10 % |
| host | 5–7 % | 0–5 % |

Reference points:
- The reference channel runs about 20–25 % action overall and ~50 % in battle chapters.
- The WW1 film shipped at 22 %, with talk 25 % and maps 18 %.
- We aim higher than the reference because static talk is what makes our films feel slow.

How to raise action without new narration:
1. **Every number lands on a scene, not a chart.**
   - Run a `counter` (HUD) over men advancing ("57,470 CASUALTIES" over the first wave of the Somme).
   - Or over stretcher bearers ("≈ 337,000 GERMAN").
   - Keep a chart only when two or more values must be compared, and keep it ≤ 7 s.
2. **Command → field.** A general decides (2–4 s, close), then cut to the men doing it.
   - Falkenhayn: "let the guns do the killing" → the GUN_CREW shot.
3. **"Who or what is doing something in this frame?"** If the answer is nobody, replace the shot.
4. **A document gets ≤ 4 s.** Read one line, then cut to what the line causes.
5. **Maps ≤ 5 s inside battle chapters.** Arrows draw while the voice names the place, then back to people.
6. **Symbolic consequence objects** instead of numbers on cards:
   - crosses appearing one by one;
   - an empty helmet;
   - life rings on the water for a sunk ship;
   - a stretcher.

## 2. Action recipes (`tools/shotlib.py`, section ACTION RECIPES)

All of them are element builders. Put them in a stage scene with `world=WORLD`, or with your own world for another horizon.
Combine several in one scene. Put the burst times in `impacts` so the camera jolts.

| recipe | builder | what you see | notes |
|---|---|---|---|
| OVER_TOP | `assault(prefix, who, rows, falls, view="back", climb=True)` + set `fg: "sandbags"` | The near row rises from behind the parapet. Staggered rows walk away into the smoke; some men fall at staggered times. | Rows are `(y0, y1, [x…], t0, t1)`, near row first. Never put several men on one horizontal line. Use 3 rows: near y 1100→850, mid 900→740, far 760→660. |
| WAVE | `assault(..., view=None, run=True)` with rows that move in x, or `man_path` per man | A charge across the frame in depth, shells ahead, one falls. | Then a `full` shot with `track=True` on the leader (not `medium`: too many big faces). |
| shells | `els, impacts = shells([(t, x, y)], size=2.0)` | Columns of earth (`shellburst`) where they land. | Depth-sorted and depth-sized. `size` 2 ≈ 2.5 men tall at that depth; 3 for heavy shells. |
| GUN_CREW | `gun_crew(prefix, who, gun_x, gun_y, fire=[t…], nation, heavy=1.9)` | The loader carries a shell in and loads it. The gun fires (recoil, flash, smoke, boom); the layer covers his ears each time. | Cut: wide → `mediumclose` on the layer for one shot → wide again. Fire a second gun in depth on other beats. |
| MG_NEST | `mg_nest(prefix, who, xs, y=1170, scale=1.9, fire=(t0, t1))` + set `fg: "sandbags"` | Men aiming over sandbags, automatic muzzle flashes at the rifle tips, a spotter with binoculars. | Add sfx `machinegun` with `dur`. Feet low (y ≈ 1150–1200) so the bags hide the legs. |
| HIT | `hit_and_help(prefix, who, x0, x1, y, hit_t, dur)` | A man advancing is hit and tips over backwards; a comrade runs in, kneels by his head and cries. | Cut to `close` on `prefix+"k"` after he kneels. No gore, ever. |
| STRETCHER | `stretcher_team(prefix, who, x0, x1, y, t1, scale=None\|s, silhouette=False)` | Two bearers walk with a stretcher; the man on it lies still. | Geometry is computed: hand height, stretcher drawn over his lower half, head between the bearers. Do not hand-place stretcher parts. |
| SILHOUETTE | any builder + `silhouette=True`, set `{"kind": "nomansland", "time": "dusk", "horizon": 880, "wire": false}` | Black cut-outs on a ridge against the sunset: bearers, a column, crosses appearing one by one (`in` staggered, `enter: "place"`). | For grief and "for most of a year" beats. Explicit scales, no world. |
| AFTERMATH | `fallen(prefix, who, [(x, y)…])` + a survivor walking back (`man_path`, `expr: "cry"`) | Men lying where they fell, helmets beside them, `tint: "grey"`. | Hold 3–4 s, then a medium on the survivor. |
| TANK | `{"kind": "vehicle", "type": "markiv", "keys": …, "fireAt": [t]}` + defenders running (`run: True`) + one aiming then cowering | The tank crawls in from frame left and fires; the defenders flee. | Wide ≥ 3 s so the tank reads, then a `mediumclose` on the shocked defender. |
| RAIL / COLUMN | locomotive + traincars with the same keys, `smoke` fx keyed with the engine; men walking toward it (`man_path`, `pose: "shoulder"`) | Troops go east, reinforcements stream to the front. | Train at y ≈ 740 (far), men near. |

Engine fields behind the recipes (see plan-schema.md):
- Actor `fallAt` / `fallDir` / `lying`.
- Rifle `fireAt` / `fire`.
- Vehicle `fireAt` / `muzzle`.
- `silhouette`.
- Scene `impacts`.
- `depthY`.
- Set `nomansland`.
- Fx `shellburst`.
- Prop `stretcher`.

## 3. Depth rules (why things looked wrong, and what the engine now does)

- **Draw order is by feet y.** In a `world` scene, people, vehicles, props and *ground* effects are drawn far → near by their current ground y.
  - Ground effects: `shellburst explosion impact dust smoke fire splash`.
  - A shell bursting behind a man is drawn behind him.
  - Without a world, battle scenes (any ground effect present) still sort people, vehicles and bursts by y.
  - Give every burst the y **where it lands**, not where its cloud should be.
- **Ground effects shrink with distance** in a world scene: native size at the world's reference y (900), smaller further back. `size` multiplies that.
  - `depth: false` on an fx opts out (e.g. a burst meant to fill the frame).
- **Riders sort with their carrier.** `depthY` overrides the sort depth (the stretcher patient sorts with the bearers). `stretcher_team` sets it.
- **Men who are down never walk.**
  - After `fallAt`, or with `lying: true`, the gait is off even if x/y are still keyed (carried, dragged).
  - `run: true` only gives a running gait **while the path moves**; with no x/y keys it still means "run in place".
- **Rifles appear when the hands arrive.** When a pose with a rifle follows a pose without one (hands on head → aim), the rifle appears only when the hands are 80 % of the way there.
- Use scene `world` for every outdoor action scene. The validator warns when bursts sit next to unscaled people without one.

## 4. Animating action (the rules that make it read)

- **Something moves in every frame of a battle shot**: men advancing, smoke drifting, a gun recoiling, flashes. A battle shot with nobody moving is a mistake.
- **Stagger everything.**
  - Start times 0.2–0.3 s apart per man.
  - Falls spread over 1–4 s, never two in the same second.
  - Shots from two guns out of phase.
- **Cause → effect on the word.** The burst lands on the noun ("guns"), the counter starts on the number, the fall on "cost".
- **Cut every 2.5–5 s in battle**: wide (establish the line) → full/medium on a group (who falls) → close on one face (cost) → wide.
- **Camera jolts** (`impacts`) on every burst within ~800 px of the camera's subject. Add a small `shake` (2–4) on MG shots.
- **No gore.**
  - Hits are a tip-over with a shocked face.
  - Death is shown by lying still, an empty helmet, a cross, silhouettes, grey tint.
- **Both sides.** When the narration says "the Germans bled as well", show German men in the same situation (stretcher, cowering under the barrage), not a label.
- **Business for talk shots.** A general never just talks:
  - he reads a report, writes, slams the table, points at a map, puts on his cap, walks to the window;
  - he changes pose every 1.5–3 s;
  - the validator warns for people standing > 6 s with no pose change.

## 5. Checklist for a battle chapter

- [ ] `work/mix.json`: action ≥ 55 %, talk ≤ 10 %, maps ~10 %, devices ≤ 10 %.
- [ ] Every number is on a scene (counter over action) unless it is a comparison.
- [ ] Every outdoor action scene has `world`, bursts at their landing y, `impacts` on the scene.
- [ ] Look at `--at all` stills.
  - Bursts behind near men.
  - No one lying and walking.
  - Stretchers read.
  - No rifle across a face.
  - Muzzle flashes at the rifle tips.
- [ ] One symbolic consequence object per battle (crosses, helmet, stretcher, life rings).
