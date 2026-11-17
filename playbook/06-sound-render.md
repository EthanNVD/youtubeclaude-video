# 06 — Sound, render, final file

**Only one render at a time.** `review`, `video`, `thumbs` and `prompts` each start a browser. Two at once time out. Wait for one to finish before starting another.

## 1. Sound
```
python tools/make.py projects/<slug> audio
```
- This builds `out/audio/mix.wav`: the voice plus ambience beds plus sound effects, at −14 LUFS. There is **never music**.
- Sound effects are added automatically from the cards: explosions, guns that fire, tanks, trains, typewriters, crowds.
- The report ends with `sound_warnings`. Fix every one:
  - `silent scene` → add `"ambience": "battle"` (or `room`, `wind`, `sea`, …) to that card.
  - `no default ambience` → the same fix.
- With no voice (SRT only), the mix has ambience and sound effects only. That is expected.

## 2. Picture
```
python tools/make.py projects/<slug> video
```
- This renders `out/picture.mp4`. It takes about 1–2× the film's length; a 30-minute film takes 30–60 minutes.
- Run it in the background if your tools allow, and wait for it to finish. Do not start another render.
- To render only a part: `--from 120 --to 180` (seconds).

## 3. Put picture and sound together
```
python tools/make.py projects/<slug> mux
```
The result is `out/<slug>.mp4`.

## 4. Check the final file

Take frames from the encoded MP4, around 6 moments spread over the film:
```
ffmpeg -ss 120 -i projects/<slug>/out/<slug>.mp4 -frames:v 1 -vf scale=640:-1 projects/<slug>/review/final_120.jpg
```
- Look at the frames: picture and timing should be right.
- If you can play audio, listen to a minute around a busy battle.

## Done when

`out/<slug>.mp4` exists, the frames look right, and `STATUS.md` is ticked.
