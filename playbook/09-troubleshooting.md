# 09 — Troubleshooting

| symptom | cause | fix |
|---|---|---|
| `python: can't open file` | You are not in the repo root. | Run commands from the repo folder (the one containing `AGENTS.md`). |
| `node: command not found` / render fails at once | The engine is not installed. | Run `npm ci` (see [01-setup](01-setup.md)). |
| `TimeoutError` / `Target closed` while rendering | Two renders are running. | Stop one; run them one at a time. |
| Review sheet shows the same picture for several tiles | Cards repeat a recipe, or there are several cards inside one long sentence. | Follow the variety rules ([narration-to-picture §4](narration-to-picture.md#4-variety-rules)). |
| A scene shows the wrong army | `side` is missing, so the film's first side was used. | Add `"side"` to the card. |
| Officers look like privates | You used the side's soldier for a named person. | Add the person to `cast` with a preset. |
| Map shows the wrong year's borders | `era` in `_film.json` is wrong, or the map era does not fit. | Fix `era`, or set `"map_era": "1920"` in `_film.json`. |
| Counter / label appears too early | Its `on` is missing. | Add `"on": "words"` from the card's narration. |
| Everything is correct but the film feels slow | Talk, maps and charts are too long, or cards are 8–12 s each. | Raise action toward 60 %; cut long cards in two (one idea each). |
| `sound_warnings`: silent scene | The set has no ambience. | Add `"ambience": "room"` (or `battle`, `wind`, `sea`, …) to the card. |
| `video` takes very long | Normal: about 1–2× the film's length. | Use `--from/--to` for tests; render the whole film once. |
| Voice and picture out of sync | The SRT is shifted relative to the voice. | Re-run `prepare --align` to time the words on the voice. |
