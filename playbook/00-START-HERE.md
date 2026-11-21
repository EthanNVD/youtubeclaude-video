# 00 — Start here

Read this page completely once per session. It tells you which step you are on and what to do next.

## A. Find out where the project is

1. Read `ROADMAP.md`, sections "Known issues" and the newest milestone. Engine limits are listed there, for example "no biplanes yet".
2. If the user names a project, open `projects/<slug>/STATUS.md`.
   - It lists the steps already done (ticked) and the decisions taken.
   - Continue from the first unticked step.
3. For a new video, create the folder `projects/<slug>/`.
   - Use a short lowercase name with dashes, e.g. `projects/battle-of-midway/`.
   - Copy `templates/STATUS.md` into the folder as `STATUS.md`.
   - Then go to step 1.

## B. The steps

| step | page | finished when |
|---|---|---|
| 1 prepare | [01-setup.md](01-setup.md) | `work/words.json` and `work/reading.md` exist |
| 2 understand | [02-understand.md](02-understand.md) | every section of `understanding.md` is filled in, with one `idea` per clause |
| 2b pre-production | [scene-writing.md §8](scene-writing.md) | `cast`, `sets`, `drawings`, `look` in `cards/_film.json`; `preview` sheets checked |
| 3 cards | [scene-writing.md](scene-writing.md), [03-cards.md](03-cards.md) | one `cards/chNN.json` per chapter, covering the whole narration |
| 4 compile | [04-compile.md](04-compile.md) | `python tools/make.py projects/<slug> cards` prints `"ok": true` with no warnings left that you could fix |
| 5 review | [05-review.md](05-review.md) | every review sheet checked (`--at all`); only the wrong cards fixed, compiled and re-checked |
| 6 sound | [06-sound-render.md](06-sound-render.md) | `out/audio/mix.wav` exists, `sound_warnings` is empty |
| 7 render | [06-sound-render.md](06-sound-render.md) | `out/<slug>.mp4` exists and you checked frames from it; later fixes went through `patch` |
| 8 YouTube | [07-youtube.md](07-youtube.md) | `out/youtube/` written, thumbnail prompts and drafts made |
| 9 hand over | below | the user has the report |

Work through the steps without stopping to ask the user for approval between them. Ask only when:
- the inputs are missing;
- the user wants a preview first;
- a fact is unclear and the narration does not decide it.

## C. How to work so that the result is good

- **One chapter at a time.** For each chapter:
  1. Write the beats for that chapter in `understanding.md` §6.
  2. Write its cards.
  3. Run `check`.
  4. Then move to the next chapter.
- **Write files, not chat.** Everything you decide goes into `understanding.md`, `cards/`, or `STATUS.md`, so the next session can continue from it.
- **When a tool prints an error, do exactly what it says.** If you do not understand an error, look it up in [09-troubleshooting.md](09-troubleshooting.md).
- **Do not invent fields or values.** Use only what `recipes/<recipe>.md` lists. The checker rejects anything else.
- **Check variety yourself.**
  - Before writing a chapter's cards, look at the recipes used in the chapter before.
  - Do not build the same shapes again.

## 9. Hand over

Tell the user, in their language:
1. The MP4 path and its duration.
2. The screen-time mix. It is printed by `cards` and saved in `work/mix.json`.
3. The 3 titles (★ the recommended one) and where the thumbnail prompts and drafts are.
4. Anything you could not verify, or scenes you think are weak.

Then tick the last boxes in `STATUS.md`.
