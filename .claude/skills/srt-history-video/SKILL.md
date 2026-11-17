---
name: srt-history-video
description: Turn a narration (an .srt, a voice recording, or both) into a finished military-history animated explainer — chibi characters acting in detailed places, battles with real action, maps, a recurring host, date badges, SFX, "Two Sides of War" style — rendered with this repo's engine, plus the YouTube package (3 titles, thumbnail prompts + drafts, description with chapters, tags, hashtags). Planned as scene cards compiled by tools/make.py. Use whenever the user drops an .srt and/or a voice file into projects/ or asks to make, re-make or fix a history video, its thumbnails or its metadata.
---

# Narration → military-history animated video (studio edition)

You are the director. The engine draws. You decide what the viewer sees for every sentence, by writing **scene cards**.

**Follow `AGENTS.md`, then `playbook/00-START-HERE.md`, step by step.** This skill file only adds what a Claude session needs on top of them.

## The path (details in playbook/)
1. `python tools/make.py projects/<slug> prepare`. It accepts an SRT only, a voice only, or both.
2. Read **all** of `work/reading.md`. Then fill `understanding.md`: question and answer, people → presets, places, numbers (compare or alone), chapters, and the beats of each chapter with the recipe for each sentence.
3. Write the cards:
   - `cards/_film.json`: era, sides, cast with name and role, extra places.
   - `cards/chNN.json`: one card per idea, 3–10 s. Each card has:
     - `at`: the first words, copied exactly;
     - `recipe`;
     - `says`: the meaning in your own words;
     - the recipe's fields.

   Choose recipes with `playbook/narration-to-picture.md`; the fields are in `recipes/<id>.md`.
4. `python tools/make.py projects/<slug> cards`. Fix every error, which says what to change. Fix the warnings too:
   - the same recipe twice in a row;
   - chapter mix;
   - card length;
   - `says` copied from the narration.

   Targets: action ≥ 40 % for the film, ≥ 55 % in battle chapters; talk, maps and devices ≤ 15 % each.
5. `review`. Open every `review/sheet_*.jpg` and answer the yes/no checklist in `playbook/05-review.md`.
6. `audio` → `video` → `mux`. Run one render at a time. Then check frames of the final MP4.
7. The YouTube package (`playbook/07-youtube.md`).

## Fixed choices (never ask)
- Military history.
- The narration comes from the user.
- **No music**: ambience and SFX only.
- All visuals are drawn by the engine.
- 1920×1080, 24 fps.

Talk to the user in their language (Vietnamese by default). On-screen text and metadata follow the narration's language. Never upload or publish anything.

## When recipes are not enough (strong models)
- **A recurring kind of sentence**: add a recipe in `tools/cardlib/recipes_*.py`. Then run `python tools/catalog.py --previews`, check its preview tiles, and add a row to `narration-to-picture.md` (`playbook/08-advanced.md` §B).
- **A one-off moment**: use the `raw` recipe, which takes an engine scene. Schema: [references/plan-schema.md](references/plan-schema.md).
- **A missing visual** (set, prop, vehicle, pose, fx): extend the engine in `src/`, then run `npx tsc --noEmit` and render a still. Follow the neighbouring code's style. Never fake a missing visual with a label.

## Reference material (for recipe and engine work)
- [references/action.md](references/action.md): screen-time mix, battle depth rules, how to animate action.
- [references/acting-camera.md](references/acting-camera.md): reads, coverage, acting and motion rules behind the recipes' camera work.
- [references/plan-schema.md](references/plan-schema.md): the engine's scene and element schema (`raw` scenes, engine work).
- [references/storytelling.md](references/storytelling.md): macro structure, the scored device, the host.
- [references/sound.md](references/sound.md), [references/thumbnails.md](references/thumbnails.md), [references/metadata.md](references/metadata.md), [references/cast.md](references/cast.md).
- `docs/STYLE_GUIDE.md` (what a good frame looks like) and `docs/QUALITY.md` (definition of done).
