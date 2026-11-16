# STATUS — Why Operation Market Garden Was COMPLETELY Avoidable

| | |
|---|---|
| slug | `market-garden` |
| SRT / voice | `input/script.srt` · `input/voice.wav` (34:04.7) |
| language | en |
| started | 2026-11-16 |
| state | re-rendering with the film-quality engine (2026-11-16) |

## Decisions
- Device: the road to Arnhem (road device v2, exits = warnings that were ignored, painted German when lost).
- Host usage: opens, presents the road, chapter turns, verdict.
- Chapters: 12 (plan built from `plan_src/part1-3.py` by `plan_src/build.py`).

## Progress
- [x] analyze + outline
- [x] plan written (254 scenes)
- [x] validate clean (0 errors, 0 overlap/speed/face warnings; 18 long-text/long-shot notes)
- [x] review sheets checked — all 254 scenes re-reviewed after the part-2 upgrade; fixes: map labels (s086, s091, s151), rifle drill (s005, s032), s237 in the workroom, one-hand folders
- [x] audio (−14 LUFS)
- [x] video rendered + muxed (old engine, `out/market-garden.mp4`)
- [~] re-render with the film-quality engine (running; old film kept as `out/market-garden_v1-old-look.mp4`)
- [x] thumbnails: prompts + drafts
- [x] package (titles, description, tags)
- [ ] QUALITY.md checklist on the re-render

## Open issues / to verify
- Letterbox on 7 dramatised scenes (s001, s059, s140, s172, s185, s205, s217).
- Weak but acceptable: s209 (counter on blank paper), s230 (verdict headline on paper).

## Delivered
- MP4: `out/market-garden.mp4` (34:04, old look)
- Package: `out/youtube/`
