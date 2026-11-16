# STATUS — What Was The REAL Turning Point of WW1?

| | |
|---|---|
| slug | `ww1-turning-point` |
| SRT / voice | `input/script.srt` (made from the voice: `tools/transcribe.py`, faster-whisper small + aligned to `scripts_out/ww1-turning-point/…_script_en.txt`, 95.5 % of words matched) · `input/voice.wav` (32:22) |
| language | en |
| started | 2026-11-17 |
| state | delivered (v1) |

## Decisions
- Device: a brass hourglass on the station-master's desk ("every German plan had a deadline"); stamps NOT YET / TURNED / TURNED BACK / PLESS on the log.
- Host usage: the script's HOST_A (station master) = channel host `host` on a station platform with a pocket watch; HOST_B ("Porter") = `aide`.
- Chapters: 12 — Two Hours · The Hourglass · Forty Days to Paris · The Crack in the Glass · Bleeding · Who Held the Door · Six Months to London · The Glass Turns · The Last Window · The Black Day · The Last Myth · The Verdict.
- First film built with the coverage grammar (scene.shots) and natural motion; `plan_src/lib.py` auto-adds a cut to any people-shot held > 6 s.
- New engine pieces for WW1: `pickelhaube` hat, WW1 presets (Kaiser, Hindenburg, Ludendorff, Moltke, Joffre, Foch, …), `markiv` and `renault` tanks, `turnip` prop, better hourglass.

## Progress
- [x] analyze + outline (script structure in `scripts_out/ww1-turning-point/work/`)
- [x] plan written (`plan_src/part1-4.py`, 259 scenes, 488 set-ups, avg 3.98 s, 154 close-ups)
- [x] validate clean (0 errors)
- [x] review sheets checked (all scenes); ~30 fixes applied, the user then asked to export
- [x] audio (−14.1 LUFS)
- [x] video rendered + muxed: `out/ww1-turning-point.mp4` (32:23, 1920×1080, 917 MB)
- [x] spot-check frames of the encoded file
- [x] thumbnails: `out/youtube/thumb_prompts.md` + `out/thumbs/ref_characters.png` + drafts `out/thumbs/thumb_1-3.jpg`
- [x] package: `out/youtube/` (3 titles, description with 12 chapters, 21 tags / 411 chars, 4 hashtags)

## Open issues / to verify
- Research-limited script (Wikipedia + BYU archive); figures are presented as estimates where the script says so.
- Moltke's 1914 line is shown as REPORTED · UNPROVEN, as in the script.

## Known weaknesses (not fixed before export)
- Some montage shots are short and wide (ships at a distance); ship drawings are WW2-era silhouettes.
- No motion strips were reviewed for this film (only stills + an encoded spot-check).
- The verdict corkboard is busy (7 cards).
