# STATUS — WW1 sample action chapter (test)

| | |
|---|---|
| slug | `ww1-action-test` |
| source | `projects/ww1-turning-point`, voice 599.4–722.7 s (Falkenhayn → Verdun → Brusilov → the Somme → the first tanks); words shifted into `work/transcript.words.json` |
| purpose | prove the action mix and the battle recipes before changing the skill (approved 2026-11-17) |
| state | approved; engine fixes from the review are in; video not re-rendered (user: not needed) |

## Result
- Mix (validate): action 74 % · talk 9 % · map 10 % · device 8 % (the same narration in the WW1 film: action 43 %, talk 18 %, map 15 %, device 24 %).
- `plan_src/build.py` is the worked example for `references/action.md`: it uses `shotlib` action recipes (`assault`, `shells`, `stretcher_team`, `hit_and_help`, `mg_nest`, `fallen`, `man_path`).
- Rendered once (`out/ww1-action-test.mp4`, 2:04) before the review fixes.

## Review findings (fixed in the engine, see CHANGELOG 2026-11-17 "Action")
- Shell smoke drawn over a sentry in front of it → ground fx now depth-sorted (and depth-sized in world scenes).
- Fallen men and the man on the stretcher kept walking/running → no gait when down (`fallAt`, `lying`); `run: true` only while moving.
- Stretcher unreadable (patient covered it) → `shotlib.stretcher_team` geometry.
- Rifle floated across a face when going from hands-on-head to aim → rifle appears at 80 % of the pose blend.

## Known weaknesses
- The heavy guns are drawn bigger than the depth model expects (`depthScale`/vehicles 1.9): the validator warning is intended.
- Bearers and runners are front-facing chibis walking sideways (ROADMAP known issue).
