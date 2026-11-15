---
name: srt-history-video
description: Turn an SRT + the user's narration audio into a finished military-history animated explainer (chibi characters, historical maps, a scored storytelling device, date badges, stamps, action SFX — the "Two Sides of War" grammar) rendered with this repo's Remotion engine, plus the YouTube package (3 titles, 3 thumbnails, description with chapters, tags, hashtags). Use whenever the user drops an .srt (with or without a voice file) into projects/ or asks to make/re-make/fix a history video, its thumbnails or its metadata.
---

# SRT → military-history animated video

You are the director. The engine draws; you decide what the viewer must *see* for every clause of the narration.
Read the whole pipeline once, then work through it without stopping for approval at each step.
Talk to the user in their language (Vietnamese by default); on-screen text, titles and metadata follow the **SRT language**.

Fixed decisions (do not re-ask): topic = military history · the user supplies the voice file with the SRT ·
**no music** — only ambience + action SFX · visuals drawn in code in the channel style · output 1920×1080 24 fps MP4.

## 0. Set up the project

```
projects/<slug>/input/<name>.srt     # required
projects/<slug>/input/voice.(mp3|wav|m4a)   # the user's narration — the master clock
```
If the voice is missing, ask for it; only for a timing preview may you run `python tools/guide_voice.py projects/<slug>` (robotic dev voice, never deliver it).
First run on a machine: `npm ci` and `python tools/sfx_synth.py` (see README).

## 1. Understand the whole script — `python tools/make.py projects/<slug> analyze`

Read **all** of `work/reading.md` (in chunks if long). Never plan from the first minutes or from keywords. Then write `work/outline.md`:

1. **The question** the video answers and its **verdict** (one line each).
2. **The device** — one recurring, scored visual that carries the argument for the whole video
   (see [storytelling.md](references/storytelling.md) §Device). Pick it from the script's logic, not from habit.
3. **Chapters** (normally 8–14, each 1.5–4.5 min): start time (a sentence boundary), short evocative title, what changes in the device at its end.
4. **Cast**: every person who appears → preset or custom spec ([cast.md](references/cast.md)). Recurring people keep one look.
5. **Fact flags**: ASR errors in names/numbers/dates (fix them on screen, never in timing), claims shown as "debated".

## 2. Turn narration into shots — [storytelling.md](references/storytelling.md)

Work chapter by chapter. Group cues into **beats** (one idea, usually 8–20 s), then each beat into **shots** (one camera set-up, typically 3–8 s; the plan's `scenes`). For every beat decide, before writing JSON:

- **Which visual language**: *world* (people, places, objects — who did what, who suffered), *map* (where, how far, encirclement, routes), *device/chart/document* (comparison, verdict, numbers, evidence).
- **Before → action → after → reaction**: the visible change that proves the sentence. A label is not an action.
- **What is revealed when**: an element appears on the word that names it (use cue times from `work/cues.json`).
- **Text on screen**: date badge on place/time jumps, name card on first appearance of a person, 1–5-word labels/stamps. Never subtitles.

Coverage is mandatory: scenes are contiguous from 0 to the end of the voice (validator enforces it).

## 3. Write the plan — [plan-schema.md](references/plan-schema.md)

- Short videos: `projects/<slug>/plan.json`.
- Long videos (> 5 min): `plan/_meta.json` (`meta`, `cast`) + `plan/ch01.json`, `plan/ch02.json`… each `{ "scenes": [...] }`. Write one chapter, validate, continue.
- Put `"chapter": "Title"` on the first scene of each chapter (drives YouTube chapters).
- Use only vocabulary the engine has (sets, props, vehicles, fx, poses, presets — listed in plan-schema.md; the validator reads them from `src/`). If something is truly missing, add it to the engine (see §8) rather than faking it with a label.

`python tools/make.py projects/<slug> validate` → fix every error; read every warning.

## 4. Look at it — `python tools/make.py projects/<slug> review`

Open every `review/sheet_*.jpg` and judge as a viewer: does each frame show what the narration says at that moment? Check overlaps, text cut off, characters floating, empty frames, repeated compositions, wrong flags/colours/dates. Use `--scenes s012,s013 --at all` to inspect start/middle/end of a shot. Fix and re-review the changed scenes. Do this for the whole film, not a sample.

## 5. Sound — [sound.md](references/sound.md)

`python tools/make.py projects/<slug> audio` builds `out/audio/mix.wav` (voice + ambience beds + SFX, −14 LUFS) and stems.
Ambience defaults from the set; SFX are placed automatically for stamps, explosions, documents, map arrows, flashes — add explicit `sfx` cues for every other on-screen contact (paper, phone, footsteps, guns that actually fire). Silence/low bed for grief beats.

## 6. Render — `python tools/make.py projects/<slug> video` then `mux`

Full render ≈ 1–2× real time on this PC (check the first progress lines; partial: `--from 120 --to 180`). Result: `out/<slug>.mp4`. Spot-check the encoded file (a few frames + listen to a minute around a busy sequence) before calling it done.

## 7. YouTube package — [thumbnails.md](references/thumbnails.md) + [metadata.md](references/metadata.md)

1. Three **angles** from the same script (each a different curiosity: myth vs truth, decision/person, numbers/stakes…). Each angle = 1 title + 1 thumbnail + 1 hook line.
2. `thumbs.json` (3 thumbnails, engine-drawn) → `python tools/make.py projects/<slug> thumbs` → look at `out/thumbs/*.jpg` at 25 % size: readable? one idea? emotion visible?
3. `youtube/package.json` (titles, description with `{{CHAPTERS}}`, 20–29 tags, 3–4 hashtags) → `python tools/make.py projects/<slug> package` → `out/youtube/`.

## 8. Extending the engine

Missing set/prop/vehicle/pose/preset? Add it in `src/` (follow the neighbours' style: flat fill, `INK` 4 px outline, one shade), `npx tsc --noEmit`, render a still, then use it. Reusable cast goes in `src/char/presets.ts`. Keep additions generic so the next video benefits.

## Deliver

Report to the user: the MP4 path, duration, the 3 titles (★ recommended) with their thumbnails, paths to description/tags/hashtags, and anything you could not verify (facts flagged, scenes you consider weak). Never upload or publish.
