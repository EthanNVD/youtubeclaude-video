---
name: srt-history-video
description: Turn an SRT + the user's narration audio into a finished military-history animated explainer (chibi characters acting in detailed places, a recurring host, historical maps, a scored storytelling device, date badges, stamps, action SFX — the "Two Sides of War" grammar) rendered with this repo's Remotion engine, plus the YouTube package (3 titles, 3 detailed thumbnail prompts for image models + drafts, description with chapters, tags, hashtags). Use whenever the user drops an .srt (with or without a voice file) into projects/ or asks to make/re-make/fix a history video, its thumbnails or its metadata.
---

# SRT → military-history animated video

You are the director. The engine draws; you decide what the viewer must *see* for every clause of the narration.
Read the whole pipeline once, then work through it without stopping for approval at each step.
Talk to the user in their language (Vietnamese by default); on-screen text, titles and metadata follow the **SRT language**.

Fixed decisions (do not re-ask): topic = military history · the user supplies the voice file with the SRT ·
**no music** — only ambience + action SFX · visuals drawn in code in the channel style · output 1920×1080 24 fps MP4 ·
**acting first**: most shots are characters *doing things in real places* (decks, bridges, offices, corridors, trenches),
not charts — like an animated film; maps and devices are the minority ([storytelling.md](references/storytelling.md) §Acting first) ·
**the host** (`who: "host"`, the channel's recurring narrator) opens the video, presents the device and closes it ·
**thumbnails = detailed prompts** for an image model + engine drafts ([thumbnails.md](references/thumbnails.md)).

## Before anything
Read `ROADMAP.md` (what the engine can and cannot do yet, known issues) and `docs/STYLE_GUIDE.md` (what a good frame looks like).
Copy `projects/_template/STATUS.md` to `projects/<slug>/STATUS.md` and keep it current (decisions, progress, open issues).
A video is finished only when every box in `docs/QUALITY.md` is ticked.

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
4. **Cast**: every person who appears → preset or custom spec ([cast.md](references/cast.md)). Recurring people keep one look. Always include `"host": {"preset": "host"}`.
5. **Fact flags**: ASR errors in names/numbers/dates (fix them on screen, never in timing), claims shown as "debated".

## 2. Turn narration into shots — [storytelling.md](references/storytelling.md)

Work chapter by chapter. Group cues into **beats** (one idea, usually 8–20 s), then each beat into **shots** (one camera set-up, typically 3–8 s; the plan's `scenes`). For every beat decide, before writing JSON:

- **Which visual language**: *world* (people acting in places — who did what, who suffered: the default, ≥ 60 % of screen time), *map* (where, how far, encirclement, routes), *device/chart/document* (comparison, verdict, numbers, evidence), *host* (the narrator in his study / at the device for hooks, transitions, verdicts).
- **The acting beat**: for every *world* shot write the physical action in one line — entrance (walk/run in), business (reads, types, looks through binoculars, carries, points at the map), reaction (pose + expression change on the key word), exit. Characters change pose every 1.5–3 s (pose keys blend smoothly); nobody stands frozen.
- **Before → action → after → reaction**: the visible change that proves the sentence. A label is not an action.
- **What is revealed when**: an element appears on the word that names it (use cue times from `work/cues.json`).
- **Text on screen**: date badge on place/time jumps, name card on first appearance of a person, 1–5-word labels/stamps. Never subtitles.

Coverage is mandatory: scenes are contiguous from 0 to the end of the voice (validator enforces it).

## 3. Write the plan — [plan-schema.md](references/plan-schema.md)

- Short videos: `projects/<slug>/plan.json`.
- Long videos (> 5 min): `plan/_meta.json` (`meta`, `cast`) + `plan/ch01.json`, `plan/ch02.json`… each `{ "scenes": [...] }`. Write one chapter, validate, continue.
- Put `"chapter": "Title"` on the first scene of each chapter (drives YouTube chapters).
- Start from the shot templates in `tools/shotlib.py` ([shots.md](references/shots.md)) and the `Plan` helper (tiles the timeline, fixes vehicle speeds); then tune every timing to the cue words.
- Letterbox (`letterbox`) only the dramatised acting moments — about one per chapter, never on maps or devices.
- Devices are physical objects: put bars/timeline/scale scenes in the `workshop` set, not on blank paper.
- Maps: colour only the sides that matter, name only the rivers the story needs, key places as `tag` cities, a legend on every multi-side map, and movers (`route` + `icon` + `trail`, `map.follow`) whenever something travels.
- Use only vocabulary the engine has (sets, props, vehicles, fx, poses, presets — listed in plan-schema.md; the validator reads them from `src/`). If something is truly missing, add it to the engine (see §8) rather than faking it with a label.

`python tools/make.py projects/<slug> validate` → fix every error; read every warning.
**Zero tolerance** for layout/motion warnings: text overlapping text, a badge zone (date/place top-left, clock top-right, name card bottom-left) or a face, and vehicles faster than their type (`moves … u/s`).
If you generate the plan from Python, call `tools/layout_check.fix_speeds(plan)` before writing it (keeps each vehicle's destination, starts it closer).

## 4. Look at it — `python tools/make.py projects/<slug> review`

Open every `review/sheet_*.jpg` and judge as a viewer: does each frame show what the narration says at that moment? Check overlaps, text cut off, characters floating, empty frames, vehicles barely in frame, scenery that should scroll but stands still, repeated compositions, wrong flags/colours/dates. Count the shots: if world/acting shots are under ~60 %, replace charts/inserts with scenes of people doing the thing. Use `--scenes s012,s013 --at all` to inspect start/middle/end of a shot. Fix and re-review the changed scenes. Do this for the whole film, not a sample.

## 5. Sound — [sound.md](references/sound.md)

The user supplies only the SRT and the narration — **all ambience and SFX are generated by the skill** (never ask for them). `python tools/make.py projects/<slug> audio` builds `out/audio/mix.wav` (voice + ambience beds + SFX, −14 LUFS) and stems, and prints `sound_warnings` (silent scenes, sets without a bed): fix them all.
Ambience defaults from the set; SFX are placed automatically for stamps, explosions, documents, map arrows, flashes — add explicit `sfx` cues for every other on-screen contact (paper, phone, footsteps, guns that actually fire). Silence/low bed for grief beats.

## 6. Render — `python tools/make.py projects/<slug> video` then `mux`

Never run two render commands at the same time (stills, thumbs, prompts' reference sheet and video each start a headless Chrome; in parallel they time out). Full render ≈ 1–2× real time on this PC (check the first progress lines; partial: `--from 120 --to 180`). Result: `out/<slug>.mp4`. Spot-check the encoded file (a few frames + listen to a minute around a busy sequence) before calling it done.

## 7. YouTube package — [thumbnails.md](references/thumbnails.md) + [metadata.md](references/metadata.md)

1. Three **angles** from the same script (each a different curiosity: myth vs truth, decision/person, numbers/stakes…). Each angle = 1 title + 1 thumbnail + 1 hook line.
2. **Thumbnail prompts (main deliverable)**: write `youtube/thumb_prompts.json` (layout, characters with expression/pose/placement, the one-moment background, symbol, labels, exact headline 1–5 words with accent, light, palette) → `python tools/make.py projects/<slug> prompts` → `out/youtube/thumb_prompts.md` (Full prompt · Clean plate · Midjourney for each thumbnail) + `out/thumbs/ref_characters.png` (to attach to the image model). Read the generated prompts once as the image model would.
3. **Engine drafts**: `thumbs.json` with the same headlines → `python tools/make.py projects/<slug> thumbs` → layout preview, check at 25 % size. When the user brings AI images back as `input/thumb_N.png`, the same command composites the exact headline on them.
4. `youtube/package.json` (titles, description with `{{CHAPTERS}}`, 20–29 tags, 3–4 hashtags) → `python tools/make.py projects/<slug> package` → `out/youtube/`.

## 8. Extending the engine

Missing set/prop/vehicle/pose/preset? Add it in `src/` (follow the neighbours' style: flat fill, `INK` 4 px outline, one shade), `npx tsc --noEmit`, render a still, then use it. Reusable cast goes in `src/char/presets.ts`. Keep additions generic so the next video benefits.

## Deliver

Report to the user: the MP4 path, duration, the 3 titles (★ recommended) with their thumbnail prompts (`out/youtube/thumb_prompts.md` — which variant for which model, the reference sheet to attach) and drafts, paths to description/tags/hashtags, and anything you could not verify (facts flagged, scenes you consider weak). Never upload or publish.
