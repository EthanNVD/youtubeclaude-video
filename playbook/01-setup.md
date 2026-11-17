# 01 — Set up the project and prepare the inputs

## First time on a machine (once)
```
npm ci
pip install numpy pillow
python tools/sfx_synth.py
```
- `npm ci` installs the engine.
- `pip install numpy pillow` installs what the audio and contact sheets need.
- `python tools/sfx_synth.py` generates the sound effects into `assets/sfx/`.

Only if the user gives a voice without subtitles:
```
pip install faster-whisper
```

## 1. Put the inputs in `projects/<slug>/input/`

Any of these works:

| the user gave | put in `input/` | what happens |
|---|---|---|
| an `.srt` and a voice file | both | The SRT gives the words; the voice is the soundtrack. Best case. |
| only a voice file (`.wav`, `.mp3`, `.m4a`…) | the audio file. Add `script.txt` (the text that was read) if the user has it. | The voice is transcribed to `input/script.srt`. With `script.txt`, names and numbers are spelled as written. |
| only an `.srt` | the `.srt` | The video is timed to the subtitles. It has no narration, only ambience and sound effects. Tell the user they can drop the voice in later and re-run `audio` and `mux`. |

The file names do not matter. Use the user's files as they are; `prepare` finds them.

## 2. Run prepare
```
python tools/make.py projects/<slug> prepare
```
Add `--align` when the user gave an SRT and a voice and you want cuts timed exactly on the spoken words. It is slower, about 1 minute per 5 minutes of voice.

It prints a short JSON report. Check these three things:
- `"words"` is a big number (about 150 per minute of narration).
- `"voice"` names the voice file, or is `null` if there is no voice.
- `"next"` tells you what to do next.

It created:
- `work/reading.md` — the whole narration in blocks with timestamps. **You will read all of it in step 2.**
- `work/words.json` — every word with its time. The compiler uses it to place your cards.
- `understanding.md` — the form you fill in at step 2.
- `cards/_film.json` — the film settings you fill in at step 3.

## 3. Update STATUS.md
Tick "prepare". Write which inputs you used: SRT, voice, or both.

## If something goes wrong

| message | what to do |
|---|---|
| `Nothing in .../input` | The inputs are missing. Ask the user for the `.srt` and/or the voice file. |
| `transcription failed` | Run `pip install faster-whisper`. If it still fails, ask the user for an `.srt`. |
| `"words": 0` or very small | The `.srt` is empty or broken. Open it and check it has `-->` time lines and text. |
