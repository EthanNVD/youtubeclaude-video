# AGENTS.md — how to make a video in this repo (read this first, every session)

This repo turns a narration (an `.srt` subtitle file and/or a voice recording) into an animated military-history video, in
the "Two Sides of War" style, plus its YouTube package. You are the **director**:
- you decide what the viewer sees for every sentence;
- the code draws it.

**You do not write animation code or coordinates.**
- You write **scene cards**: small JSON objects that pick a *recipe* (a tested kind of scene) and fill in its fields.
- A compiler turns the cards into the film.

## The 9 steps (do them in order; each has its own page in `playbook/`)

| # | step | you run / write | page |
|---|---|---|---|
| 0 | Start the session | read this file, `ROADMAP.md`, the project's `STATUS.md` | [00-START-HERE](playbook/00-START-HERE.md) |
| 1 | Prepare the inputs | `python tools/make.py projects/<slug> prepare` | [01-setup](playbook/01-setup.md) |
| 2 | Understand the script | read **all** of `work/reading.md`, fill in `understanding.md` | [02-understand](playbook/02-understand.md) |
| 3 | Write the cards | `cards/_film.json` + `cards/ch01.json`, `ch02.json`, … | [03-cards](playbook/03-cards.md) + [narration-to-picture](playbook/narration-to-picture.md) + [recipes/CATALOG](recipes/CATALOG.md) |
| 4 | Compile and fix | `python tools/make.py projects/<slug> cards` (repeat until `"ok": true`) | [04-compile](playbook/04-compile.md) |
| 5 | Look at it | `python tools/make.py projects/<slug> review`, open every `review/sheet_*.jpg` | [05-review](playbook/05-review.md) |
| 6 | Sound | `python tools/make.py projects/<slug> audio` | [06-sound-render](playbook/06-sound-render.md) |
| 7 | Render | `python tools/make.py projects/<slug> video`, then `mux` | [06-sound-render](playbook/06-sound-render.md) |
| 8 | YouTube package | titles, thumbnail prompts, description, tags | [07-youtube](playbook/07-youtube.md) |
| 9 | Hand over | report to the user, update `STATUS.md` | [00-START-HERE](playbook/00-START-HERE.md#9-hand-over) |

## Rules that are never broken

1. **Understand before you build.**
   - Read the whole of `work/reading.md`, not just the first part.
   - Fill in `understanding.md` before writing any card.
   - Every card has a `says` field: what the narration MEANS, in your own words.
2. **One card = one scene = one idea**, usually 3–10 seconds.
   - The card starts where that idea starts in the narration (`at` = the first words, copied exactly).
3. **Tell it like an animated film: one clause, one concrete picture.**
   - For every clause answer WHO, DOES WHAT (a visible action), WHERE, WHEN, then pick the recipe (`playbook/narration-to-picture.md` §1–2).
   - The picture shows exactly what the clause says, acted by people in a real place. Never pick by keyword or habit.
4. **People in places, not text.**
   - At least 75 % of every chapter is acted (people doing the thing); maps ≤ 10 % (≤ 5 s each); documents/charts ≤ 10 %.
   - Follow the anecdotes: the same people in the same places (`place_id`), revisited as time passes.
   - Text is rare: a place/time `tag`, name cards, the 2–4 big questions as `caption`, one `stat` per ~2 minutes at most.
5. **Never the same recipe twice in a row** (unless it is the same place revisited).
   - After a decision, show its consequence.
   - After an attack, show the other side or the cost.
6. **Fix every error the tools print.**
   - Every message says exactly what to change.
   - Do not move to the next step while `"ok"` is `false`.
7. **Look at the pictures.** Open every review sheet and answer the checklist in `playbook/05-review.md`.
8. **Never run two renders at the same time.** Renders are `review`, `video`, `thumbs` and `prompts`; each one starts a browser, and two at once time out.
9. **Never upload or publish anything to YouTube.**
   - Do not commit media: `projects/*/out|review|work`, voice files, `assets/sfx/*.wav`.
10. **Language.**
    - Talk to the user in their language (Vietnamese by default).
    - Text on screen and YouTube metadata follow the narration's language.

## Fixed choices (do not ask the user about these)
- Military history.
- The user supplies the narration (`.srt`, voice, or both).
- **No music**: ambience and sound effects only.
- 1920×1080, 24 fps.
- Every picture is drawn by the engine in `src/`.

## Where things are

| path | what |
|---|---|
| `playbook/` | step-by-step instructions (start at `00-START-HERE.md`) |
| `recipes/CATALOG.md` | every recipe: when to use it, its fields, preview images |
| `recipes/PEOPLE.md` | sides, uniforms, character presets |
| `data/places.json` | map places by name |
| `templates/` | `understanding.md`, `cards/_film.json`, `STATUS.md` |
| `projects/example-ww1-verdun/` | a complete worked example (understanding + cards → 70 % action) |
| `tools/cardlib/` | the compiler and the recipes (Python). Change recipes here, then `python tools/catalog.py --previews` |
| `src/` | the drawing engine (Remotion/React/SVG). Engine work: `.claude/skills/srt-history-video/references/` + `npx tsc --noEmit` |
| `docs/STYLE_GUIDE.md`, `docs/QUALITY.md` | what a good frame looks like; the definition of done |
