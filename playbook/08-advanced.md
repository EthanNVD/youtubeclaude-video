# 08 — Advanced (strong models and engine work only)

Recipes cover almost every sentence of a military-history narration. This page is for the rare cases they do not cover.

## A. The `raw` recipe: one hand-built scene

```json
{"at": "Pigeons carried the last message", "recipe": "raw", "class": "action",
 "says": "The trapped battalion's last carrier pigeon flew out with a plea for help.",
 "scene": {"type": "stage", "set": {"kind": "ruins", "time": "dusk"},
           "elements": [ … engine elements … ], "shots": [ … ], "world": {"scale": 1.0, "y": 900}}}
```

- The scene uses the engine schema in `.claude/skills/srt-history-video/references/plan-schema.md`.
- `class` sets how the scene counts in the mix.
- `start`, `end` and `id` are filled in by the compiler.
- Common fields (`date`, `label`, `counter`, …) still work.
- Before writing raw scenes, read `references/action.md` and `references/acting-camera.md`.
- A raw scene is not tested. Review it with `--at all`.

## B. Add or improve a recipe (preferred over raw)

When a kind of sentence keeps coming back, for example "the convoy was attacked by aircraft", make it a recipe:

1. Add a function to the right `tools/cardlib/recipes_*.py` with `@recipe(...)`. Give it:
   - `when` and `not_when`;
   - the fields, as `Param` with type, default and allowed values;
   - 2–3 composition variants;
   - an example card;
   - `shots`, which describes the camera of each variant.
2. Build the scene from tested builders: `shotlib` (`assault`, `stretcher_team`, `man_path`, `shells`, …) and the existing recipes.
3. Run `python tools/catalog.py --previews`. It renders a preview of every variant and regenerates `recipes/`.
4. Open `projects/_recipes/review/sheet_*.jpg` and check your recipe's tiles.
5. Add a row to `playbook/narration-to-picture.md`.
6. Log the change in `CHANGELOG.md`.

## C. Change the engine (new set, prop, vehicle, pose, effect)

- Read the engine notes in `.claude/skills/srt-history-video/SKILL.md` §8 and `references/plan-schema.md`.
- Follow the neighbouring code's style: flat fill, 4 px ink outline, one shade.
- Run `npx tsc --noEmit`. Then render a still, and run `python tools/catalog.py --previews` if recipes use the change.
- Never fake a missing visual with a label. Add it to the engine, or note it in `ROADMAP.md`.
