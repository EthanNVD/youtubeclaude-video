# Project: SRT → military-history animated video + YouTube package

- When the user gives an SRT (+ voice) or asks for a video/thumbnails/metadata, follow `.claude/skills/srt-history-video/SKILL.md`.
- Talk to the user in Vietnamese; on-screen text and YouTube metadata follow the SRT language.
- Fixed choices: military history; user supplies the voice; NO music (ambience + SFX only); visuals drawn by the engine in `src/`; 1920×1080 24 fps.
- Pipeline entry point: `python tools/make.py projects/<slug> <step>`. Always `validate` and look at `review/sheet_*.jpg` before a full render.
- Extend the engine (`src/`) instead of faking missing visuals; run `npx tsc --noEmit` after changes.
- Never upload/publish to YouTube. Don't commit media (`projects/*/out|review|work`, voice files, `assets/sfx/*.wav`).
