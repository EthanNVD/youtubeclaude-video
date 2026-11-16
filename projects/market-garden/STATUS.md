# STATUS — Why Operation Market Garden Was COMPLETELY Avoidable

| | |
|---|---|
| slug | `market-garden` |
| SRT / voice | `input/script.srt` · `input/voice.wav` (34:04.7) |
| language | en |
| started | 2026-11-16 |
| state | delivered (old engine) · plan upgraded, **re-render pending** |

## Decisions
- Device: the road to Arnhem (road device v2, exits = warnings that were ignored, painted German when lost).
- Host usage: opens, presents the road, chapter turns, verdict.
- Chapters: 12 (plan built from `plan_src/part1-3.py` by `plan_src/build.py`).

## Progress
- [x] analyze + outline
- [x] plan written (254 scenes)
- [x] validate clean (0 errors, 0 overlap/speed/face warnings; 18 long-text/long-shot notes)
- [~] review sheets checked — after the 2026-11-16 upgrade only s002, s007, s074, s077 re-checked
- [x] audio (−14 LUFS)
- [x] video rendered + muxed (old engine, `out/market-garden.mp4`)
- [ ] re-render with the film-quality engine (~40 min, one render at a time)
- [x] thumbnails: prompts + drafts
- [x] package (titles, description, tags)
- [ ] QUALITY.md checklist on the re-render

## Open issues / to verify
- Full review of all 254 scenes with the new look before re-render.
- Half-tracks and Dakotas are still the flat drawings (ROADMAP B4).

## Delivered
- MP4: `out/market-garden.mp4` (34:04, old look)
- Package: `out/youtube/`
