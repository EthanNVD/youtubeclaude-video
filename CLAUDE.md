# Project: narration → military-history animated video + YouTube package (studio edition)

- **Read `AGENTS.md` first, every session.** It is the whole workflow in one page; `playbook/` has every step in detail.
- Videos are planned as **scene cards** (`projects/<slug>/cards/*.json`) compiled by `python tools/make.py projects/<slug> cards`.
  Most cards are `scene` cards (`playbook/scene-writing.md`, vocabulary `recipes/STAGECRAFT.md`): an `idea` per clause, then place, people acting on the words, things, camera. Recipes (`recipes/CATALOG.md`) for battles, maps, charts. Do not hand-write engine JSON unless a scene card truly cannot show the moment (`playbook/08-advanced.md`).
- Pre-production before cards: `cast`, `sets`, `drawings`, `look` in `cards/_film.json`, checked with `python tools/make.py projects/<slug> preview`. After review, fix only the wrong cards; after a render, `patch` re-renders only the changed scenes.
- Talk to the user in Vietnamese; on-screen text and YouTube metadata follow the narration's language.
- Fixed choices: military history; the user supplies the narration (SRT and/or voice); NO music (ambience + SFX only); visuals drawn by the engine in `src/`; 1920×1080 24 fps.
- Start every session with `ROADMAP.md` (known issues) and, for a video, its `projects/<slug>/STATUS.md`. Done = `docs/QUALITY.md` ticked. Log changes in `CHANGELOG.md`.
- After changing a recipe: `python tools/catalog.py --previews`. After changing the engine: `npx tsc --noEmit`.
- Never run two renders (review/video/thumbs/prompts) at the same time. Never upload/publish to YouTube. Don't commit media (`projects/*/out|review|work`, voice files, `assets/sfx/*.wav`).
