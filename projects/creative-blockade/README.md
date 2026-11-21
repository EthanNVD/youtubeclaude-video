# Example: the blockade and the Turnip Winter (scene cards)

A 94-second excerpt of the WW1 film, told with **`scene` cards only** (plus two short maps): 20 cards, 13 story places, 22 people.
Read `cards/_film.json` (pre-production: cast, story places, look) and `cards/ch01.json` (every card starts with its `idea`).

What it shows (playbook/scene-writing.md, playbook/visual-ideas.md):
- **things land as they are named**: cotton, wool, hides, copper, oil, rubber, saltpetre pop onto the Hamburg quay on their words;
- **the same place, time passing**: the Hamburg warehouse full in 1913, half empty in 1915 (`"revisit": true`);
- **the admiralty**: an over-the-shoulder decision, then the same room at dusk with the plan handed over (`give`);
- **irony**: German officers watching an empty sea; the patrol line at dusk; sailors playing cards at Scapa Flow;
- **public reaction**: a Shetland pub reading the notice aloud (a `paper_note` with the exact words);
- **scarcity**: Kirkwall customs seizing crates; a Rotterdam merchant by day and by night; a rotten potato field; a Berlin kitchen by candlelight;
- **detail → reveal**: the turnip on the plate, then the family.

Rebuild:
- The voice is not in the repo. Without it, the film is timed to `input/script.srt`.
- To use the voice, put the WW1 voice from 447.0 s to 540.2 s in `input/voice.wav`.

```
python tools/make.py projects/creative-blockade prepare
python tools/make.py projects/creative-blockade preview
python tools/make.py projects/creative-blockade cards
python tools/make.py projects/creative-blockade review --at all
python tools/make.py projects/creative-blockade audio
python tools/make.py projects/creative-blockade video
python tools/make.py projects/creative-blockade mux
```
