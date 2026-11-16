# CHANGELOG

Newest first. One entry per change that matters to the look, the pipeline or the docs.

## 2026-11-17 — WW1 Turning Point film + voice-only input
Why: the user supplied only a narration WAV for "What Was The REAL Turning Point of WW1".
- `tools/transcribe.py`: voice → SRT with faster-whisper (CPU, int8, word timestamps). With `--script`, the recognised words are aligned to the written script, so names and numbers are spelled as written (95.5 % matched on this film).
- WW1 vocabulary:
  - `pickelhaube` hat;
  - presets for the Kaiser, Hindenburg, Ludendorff, Moltke, Schlieffen, Kluck, Falkenhayn, Scheer, Holtzendorff, Zimmermann, Bauer, Joffre, Lanrezac, Gallieni, Foch, Jellicoe, Brusilov, Wilson, Lenin, Monash, Currie, plus 1914/1918 soldiers of each army and sailors;
  - `markiv` and `renault` tanks;
  - `turnip` prop;
  - a brass-framed hourglass with a falling sand stream.
- The validator accepts every machine vehicle type.
- `projects/ww1-turning-point/plan_src/timing.py` resolves scene starts from phrases of the aligned words; `lib.py` adds a cut to any people-shot held longer than 6 s (skipping people who have walked out of frame). This is a candidate for shotlib.
- Film: 259 scenes, 487 set-ups (avg 4.0 s), 12 chapters.

## 2026-11-17 — Acting, coverage and natural motion
Why: the user found Market Garden v2 static and its motion jerky.
- Static: one frozen set-up per 8 s scene, no close-ups, actions told by labels.
- Jerky: things popping in on every cut, moves that lunge then stop dead, sliding feet.

Approved on a 1-minute test (`projects/acting-test`).

Changes:
- **Coverage** (`scene.shots` in `src/scene/SceneView.tsx`):
  - set-ups framed by subject id and size (`wide … ecu`), `frameX`, push/pan;
  - `track` with a lagging camera;
  - hard cuts inside a place.
- **Acting:**
  - `turn` (3/4 face);
  - expression take;
  - `front` layer for desk props and over-the-shoulder actors;
  - keyed `holds`;
  - walking toward/away from the camera;
  - props `photo`, `magnifier`, `suitcase`; element `viewfinder`.
- **Motion** (`src/lib/anim.ts`, `Elements.tsx`, `Character.tsx`):
  - default ease is smoothstep (the old cubic peaked at 3× speed);
  - people travel with `walk`/`arrive`/`leave` profiles and vehicles with `drive`;
  - the gait is driven by the distance covered and its amplitude follows speed;
  - pose blends take 0.45–0.95 s with overlapping hands, anticipation and a 4 % settle;
  - no pop on cuts (`place`/`drop` enters for props, soft pop for text);
  - vehicles pitch with acceleration and aircraft bank;
  - camera shake is smooth noise.
- **Validator:**
  - errors for unknown shot ids/sizes;
  - warnings for single set-ups over 6.5 s and for sprinting actors;
  - a `coverage` summary (set-ups, average length, close-ups, acting share).
- **shotlib:** `SHOT`, `AID`, coverage templates `desk_read`, `ots_dialogue`, `desk_insert`, `walk_to_camera`, `walk_away`, `vehicle_arrives`.
- **Skill:** new `references/acting-camera.md` (reads, coverage, acting, motion, strip checks); SKILL, plan-schema, shots, storytelling, STYLE_GUIDE, QUALITY and ROADMAP updated.
- **Learned from** the ethanNVD frame studies (cut grammar, phases of an action) and opus-video-skills *painted-animation* (reads, timing, animation principles).

## 2026-11-17 — Script-writer skill and first drafts
Why: the user wanted the Codex `two-sides-war-script-writer` skill ported to Claude, upgraded from an editor's study of the channel's top 10 videos, able to research new topics and rewrite old scripts in the channel's voice.
- `.claude/skills/two-sides-war-script-writer/`: modes `topic_research` / `new_from_title` / `rewrite_channel_voice` / `rewrite_same_structure`; new references (top-10 analysis, channel formula, topic research, channel-voice rewrite); dialogue policy (QUOTE / REPORTED / DRAMATIZED / HOST, ≤15 %); clean + speaker-tagged outputs.
- Scripts: `channel_snapshot.py` (yt-dlp channel list + subtitles), `script_metrics.py --tagged` (tagged file matches clean text, dialogue share).
- `scripts_out/`: topic shortlist (18 scored candidates) and four research-limited drafts — Market Garden, WW1 turning point, Singapore, Battle of the Bulge — each with clean text, tagged text and sources.

## 2026-11-16 — Proportion and depth
Why: the user saw people as big as (or bigger than) the tank they stand next to.
Reference study:
- people next to vehicles are small (a man by a plane is fuselage-plus-gear high);
- people close to the camera can outsize a truck behind them.
Changes:
- `src/lib/depth.ts` + `scene.world`: ground-plane perspective; vehicles sized relative to people at the same depth (measured drawing sizes); far→near draw order; keyed `y` grows toward the camera.
- `layout_check.proportions` in validate: flags vehicles >40 % off.
- `parked: true`: landing gear for aircraft on the ground.
- Five depth-staged shot templates.
- Test clip: `projects/_test/out/depth-test.mp4` (32 s, silent).

## 2026-11-16 — Film-quality look, part 2
Why: the user found the maps cluttered and unlike the reference, spotted an extra blob on hands, and asked for roadmap items a–e in order, a stronger grade and occasional letterbox.
- Maps: clean coloured paper look (stipple, slate sea, thin borders), opt-in named rivers drawn as smooth water bands, `hatch`, small-caps town labels with `tag` for key places.
- Hands: thumb behind the palm (no ball on top), clean open hand; flat props gripped by their edges.
- Grade: stronger warm grade + vignette; `letterbox` scenes with a "DRAMATISED — …" caption.
- (a) Machines.tsx: trucks, jeep/Kübelwagen, half-tracks, field gun, fighters per nation, Stuka, heavy bombers, Dakota, Horsa, warships, Liberty ship, U-boat, boat — all with volume.
- (b) Rifle drill poses: port, aim, shoulder, charge, ease (rifle placed between the hands).
- (c) Physical devices in the new `workshop` set: glass tubes (bars), corkboard + yarn (timeline), brass scale with hanging tags.
- (d) Map movers (side-view icons with trails), `map.follow` camera, morphing fronts, shrinking pockets.
- (e) `tools/shotlib.py`: 13 shot templates + `Plan` assembler; documented in references/shots.md.

## 2026-11-16 — Film-quality look, part 1
Why: the user found the look crude (road scene: trees not scrolling, overlapping exits, vehicles zooming then stopping, sparse maps, text on text).
Studied two reference videos frame by frame → rules in `docs/STYLE_GUIDE.md`.
- Look: depth-of-field blur on backgrounds (`set.dof`), warm desaturated film grade + stronger vignette (`meta.grade`), slow camera drift on every shot without camera keys (`set.drift`).
- Vehicles: `drive` easing (accelerate–cruise–brake) is the default on vehicle `x`/`at` keys; wheels/tracks turn by distance travelled; new volume tanks `sherman panzer4 tiger t34 panther stug` (`src/props/Tanks.tsx`, `crew` = commander in the hatch).
- Road device v2: parallax world (forests, poplars, fence posts) scrolling with the road, exits only above the road with gantry signs, culled when far, town boards, `time`, `vehicles` (convoy).
- Maps: Natural Earth rivers + lakes (`public/maps/physical.json`, `tools/fetch_physical.py`), italic river names, inked coasts, ripple hatching, graticule, paper folds; `legend` and `blocks` elements.
- Validator: `tools/layout_check.py` — text/text, text/badge, text/face overlaps; vehicle speed limits; `fix_speeds()` for plan builders.
- Control docs: `ROADMAP.md`, `docs/STYLE_GUIDE.md`, `docs/QUALITY.md`, `projects/_template/STATUS.md`.
- Market Garden plan: 0 overlap/speed warnings. Needs a re-render to get the new look.

## 2026-11-16 — Market Garden delivered
- Full film (254 scenes, 34:04), package, thumbnail prompts. Rally banners now carry national flags. Mixer processes long voices in 30 s chunks.

## 2026-11-15 — Pipeline v1
- SRT + voice → plan → review → audio → render → mux → YouTube package. Characters with attached heads, hose limbs, pose blending, host + aide.
