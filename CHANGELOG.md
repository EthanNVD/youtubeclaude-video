# CHANGELOG

Newest first. One entry per change that matters to the look, the pipeline or the docs.

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
