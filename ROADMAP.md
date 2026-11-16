# ROADMAP — SRT → animated military-history video

How to use this file:
- **Read it at the start of every session**, before touching code or a project.
- Update the status boxes when work lands: `[ ]` todo · `[~]` in progress · `[x]` done.
- Add an entry to `CHANGELOG.md` for every change.
- Problems found while reviewing a video go to **Known issues** here first. Fix them in the engine, never only in one plan.

Related control files:

| file | what it is for |
|---|---|
| `docs/STYLE_GUIDE.md` | the visual rules distilled from the reference channel (what "good" looks like) |
| `docs/QUALITY.md` | definition of done + the review checklist every video must pass |
| `CHANGELOG.md` | what changed, when, why |
| `projects/<slug>/STATUS.md` | per-video progress + decisions + open issues (template: `projects/_template/STATUS.md`) |
| `.claude/skills/srt-history-video/` | the production workflow Claude follows |

---

## Milestones

### M1 — Pipeline works end to end (done 2026-11-15)
- [x] SRT + voice → plan → stills review → audio mix → render → mux
- [x] YouTube package (3 titles, description with chapters, tags, hashtags)
- [x] Thumbnail prompts for image models + engine drafts + headline compositing
- [x] Characters: head attached, rubber-hose limbs, pose blending, walk/run, held props, host + aide
- [x] First full film: Market Garden (34:04)

### M2 — Film-quality look (current)
Goal: a frame from our video can sit next to a frame from the reference channel without looking cheap.

**Look**
- [x] A1 Depth of field: backgrounds soft, actors sharp (`set.dof`)
- [x] A2 Colour grade: warm and slightly desaturated, stronger vignette, film grain (meta.grade)
- [x] A3 Gentle camera drift on every stage shot that has no camera keys
- [ ] A4 Atmospheric perspective inside every set: far layers lighter/bluer, 3+ depth layers
- [ ] A5 Foreground occluders in more sets (branches, snow banks, sandbags, window frames)

**Vehicles & motion**
- [x] B1 Vehicles move with a physical speed profile: accelerate, cruise, brake. Wheels and tracks turn by distance travelled, not by time. Body bob, exhaust and dust.
- [x] B2 Validator flags vehicles that move faster than their type allows
- [x] B3 Redrawn armour with volume: Sherman, Panzer IV, Tiger, Panther, T-34, StuG, half-track. Track links, sprocket, hubcaps, top-light shading, mud. (tanks/StuG done in `src/props/Tanks.tsx`; half-track still flat)
- [x] B4 Redrawn soft-skins (Opel Blitz, GMC, Jeep, horse cart), aircraft and ships with the same finish
- [x] B5 Two-handed rifle hold ("port arms"), aiming, marching with rifle on shoulder

**Devices**
- [x] C1 Road device rebuilt:
  - parallax world (far forest, poplars, verges) that scrolls with the road;
  - exits only above the road, spaced so that they never overlap;
  - real slip roads instead of green blobs;
  - town markers at the verge.
- [x] C2 Devices as physical objects in a room (gauge tube on a wall, scoreboard, ledger on a desk), as the reference channel does

**Maps** (reference: paper map with folds, ink coastlines, named rivers, unit blocks, legend, camera following routes)
- [x] D1 Map finish: paper texture with fold creases, graticule, ripple hatching along coasts, muted palette
- [x] D2 Physical layer: rivers and lakes from Natural Earth (public domain), river names in italic script
- [x] D3 Legend box (flags + names) and date tag as standard map furniture
- [x] D4 Quantity blocks: a grid of small division squares with a "≈160" tag
- [x] D5 Illustrated movers on maps: ship, convoy, tank column and horse carts follow a route, and the camera follows them
- [x] D6 Front lines that move over time (animate between two polylines), pockets that shrink

**Proportion & depth**
- [x] G1 Depth model (`scene.world`): actors/vehicles sized from ground y, vehicle sizes relative to people, far→near draw order (2026-11-16)
- [x] G2 Validator: vehicle out of proportion with the people at its depth
- [x] G3 Depth-staged shot templates (crew_with_vehicle, column_depth, vehicle_pass, foreground_walk, airfield_line); parked aircraft with landing gear
- [ ] G4 Back-port `world` to older plans (Market Garden has 41 out-of-proportion vehicles; only if it is re-rendered)
- [ ] G5 Vehicles seen at 3/4 or head-on (driving toward the camera); today all vehicles are side views

**Layout**
- [x] E1 Validator: overlap check for text and HUD (labels, stamps, headlines, counters, badges, name cards, documents). Zero overlaps required.
- [x] E2 Safe zones: date badge top-left, clock top-right, name card bottom-left; labels are kept out of them
- [ ] E3 Engine-side auto-nudge for labels that still collide at render time

**Acting, coverage & motion** (approved test `projects/acting-test`, 2026-11-17)
- [x] H1 Coverage inside a scene (`scene.shots`): framing by subject and size, push/pan, tracking with lag, hard cuts
- [x] H2 Acting tools: 3/4 face `turn`, expression take, `front` layer (desk props, shoulders), props change hands (`holds` keys), photo/magnifier/suitcase props, viewfinder
- [x] H3 Natural motion:
  - walking/arrive/leave speed profiles, distance-driven gait that opens and closes, pose blends 0.45–0.95 s with overlap and anticipation;
  - no pop on cuts, place/drop enters;
  - vehicle pitch on accelerating and braking, aircraft banking;
  - smooth shake.
- [x] H4 Validator: shot references, single set-ups > 6.5 s, people sprinting, `coverage` summary; coverage templates in shotlib
- [ ] H5 Side (profile) view for walking across the frame; true hand-over of a prop between two actors (grip → release)
- [ ] H6 Periodic `hall`/street sets that scroll for long tracking shots
- [ ] H7 Back-port coverage to Market Garden (validate reports 254 set-ups at 8 s, 0 close-ups) — only if it is re-rendered

### M3 — Faster, safer production
- [x] F1 Scene library: reusable shot templates (office decision, map advance, convoy, river crossing, cockpit…) so a 30-min plan is assembled from proven pieces
- [ ] F2 Partial re-render: re-render only changed scenes and splice them into the film
- [ ] F3 Automatic "review pack": start/mid/end frames for every scene plus overlap report in one HTML page

---

## Known issues (fix in the engine, then tick)
- [x] Hands: thumb drawn as a separate ball on top of the hand, hook on the open hand; flat props held with both hands in the middle (fixed 2026-11-16)
- [ ] Horse and cart still flat
- [ ] `field` set telegraph poles read as grave crosses at small size
- [ ] Polder set: drainage ditches read as a blue grid
- [x] Road device: trees stayed still while the road scrolled, exits overlapped each other and the town boards, slip roads looked like green worms (Market Garden s022–s252)
- [x] Vehicles: fast move then hard stop (fixed: 'drive' easing by default + VMAX check + `fix_speeds` that keeps the destination and starts the vehicle closer)
- [x] Map scenes too sparse / then too busy (fixed 2026-11-16: clean coloured paper maps, named rivers only, movers): rivers, river names, paper finish, legend and unit blocks added; still missing illustrated movers (D5) and moving fronts (D6)
- [x] Ships, tanks and planes flat next to the reference (2026-11-16: Machines.tsx): tanks redrawn with volume (B3); soft-skins, aircraft and ships still to do (B4)
- [x] Rally/podium banners looked like Nazi banners (fixed 2026-11-16: national flags)
- [x] Mixer ran out of memory on 34-min voice (fixed 2026-11-16: chunked)
- [ ] `sky` set with `below: land` leaves a black band at the bottom (use `polder`/`field` until fixed)
