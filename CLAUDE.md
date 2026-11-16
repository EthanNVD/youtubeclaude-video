# Project: SRT → military-history animated video + YouTube package

- When the user gives an SRT (+ voice) or asks for a video/thumbnails/metadata, follow `.claude/skills/srt-history-video/SKILL.md`.
- Talk to the user in Vietnamese; on-screen text and YouTube metadata follow the SRT language.
- Fixed choices: military history; user supplies the voice; NO music (ambience + SFX only); visuals drawn by the engine in `src/`; 1920×1080 24 fps.
- Pipeline entry point: `python tools/make.py projects/<slug> <step>`. Always `validate` and look at `review/sheet_*.jpg` before a full render.
- Extend the engine (`src/`) instead of faking missing visuals; run `npx tsc --noEmit` after changes.
- Start every session by reading `ROADMAP.md` (milestones, known issues) and, for a video, its `projects/<slug>/STATUS.md`.
  The look rules are in `docs/STYLE_GUIDE.md`; a video is done only when `docs/QUALITY.md` is fully ticked. Log changes in `CHANGELOG.md`.
- Never run two renders (video/stills/thumbs/prompts) at the same time — each starts a headless Chrome and they time out.
- Never upload/publish to YouTube. Don't commit media (`projects/*/out|review|work`, voice files, `assets/sfx/*.wav`).
