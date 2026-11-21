# 03 — Write the scene cards

A **card** is one scene: one place and one idea, usually 3–10 seconds of narration. You write cards as JSON. The compiler does all the drawing work:
- positions, sizes and depth;
- camera cuts;
- walking and timing;
- sound.

## 1. Film settings: `cards/_film.json`

`prepare` already copied a template. Fill it in from `understanding.md`:

```json
{
 "title": "What Was The REAL Turning Point of WW1?",
 "lang": "en",
 "era": "ww1",
 "sides": ["german", "french"],
 "host_set": "station",
 "cast": {
  "falkenhayn": {"preset": "falkenhayn", "name": "General Erich von Falkenhayn", "role": "Chief of the German General Staff, 1914-16"},
  "brusilov":   {"preset": "brusilov",   "name": "General Aleksei Brusilov",     "role": "Russian South-Western Front"}
 },
 "places": {"Pless": [18.95, 49.98]}
}
```

| field | what it means |
|---|---|
| `era` | Decides uniforms, tanks, planes and the map year. One of `ww1 ww2 napoleonic ancient vietnam modern`. |
| `sides` | The two main sides. The first one is used when a card has no `side`; the second when it has no `enemy`. |
| `host_set` | Where the narrator stands: a set name, e.g. `study`, `station`, `workshop`. |
| `cast` | Every named person: `preset` (from `recipes/PEOPLE.md`), plus the `name` and `role` that appear on their name card. |
| `places` | Only places missing from `data/places.json`, as `[longitude, latitude]`. |

## 2. Chapter files: `cards/ch01.json`, `cards/ch02.json`, …

Write one file per chapter, in narration order:

```json
{
 "chapter": "Bleeding",
 "cards": [
  { … card 1 … },
  { … card 2 … }
 ]
}
```

- `chapter` is the chapter title. It becomes a YouTube chapter.
- The cards must follow the narration in order, and together they must cover all of it.
- The first card of `ch01.json` starts the film.
- A card lasts until the next card starts.

## 3. One card, field by field

```json
{"at": "told Kaiser Wilhelm", "recipe": "interrupt",
 "says": "They tell the Kaiser, who is busy writing, that the front can no longer be held.",
 "who": "kaiser_wilhelm", "speakers": ["ludendorff", "hindenburg"], "business": "write",
 "look_up_on": "Kaiser Wilhelm", "react_on": "could no longer", "react": "shocked",
 "setting": "office", "flag": "german", "name_card": "kaiser_wilhelm",
 "place_id": "kaiser_study", "tag": "Spa, Belgium · 29 September 1918"}
```

| field | required | how to fill it |
|---|---|---|
| `at` | yes | The first 3–6 words of the narration where this scene starts, **copied exactly** from `work/reading.md`. Spelling must match. Punctuation and capital letters do not matter. |
| `recipe` | yes | The kind of scene. Choose it with [narration-to-picture.md](narration-to-picture.md) (the five questions, then the lookup table), then open `recipes/<recipe>.md` to see its fields. |
| `says` | yes | One sentence, in your own words, saying what this part of the narration MEANS: who does what, and why it matters. Do not copy the narration. This proves you understood it. It never appears on screen. |
| recipe fields | depends | Only the fields listed in `recipes/<recipe>.md`. Fields marked **yes** in its "required" column must be there. |
| `variant` | no | Leave it out. The compiler rotates compositions (A, B, C) so scenes never look the same. Set it only to fix a scene that looked wrong in review. |
| common fields | no | See the two tables below. |

### Fields that take narration words (`…_on`, `on`)
- Fields like `react_on`, `hit_on`, `look_up_on`, `goal_on`, `tag_on`, and `"on"` inside `stat` or `paper_note` take **words from this card's narration**.
- The event happens when those words are spoken: the Kaiser looks up on his name; the fist lands on "immediately".
- Copy 1–4 words exactly. Leave the field out to let the recipe choose a good moment.

### Story fields (use them on every film)

| field | example | what it does |
|---|---|---|
| `place_id` | `"kaiser_study"` | Names a story place. Every card with the same `place_id` keeps the same setting and tag. To show time passing in the same place, change only `time`, `weather` or `tint`. A new room or a new outside is a new `place_id`. |
| `tag` | `"Spa, Belgium · 29 September 1918"` | The place/time tag (small wooden plank, top left). Put it on the first card of every place, or every time jump. Cards with the same `place_id` inherit it. A tag that stays the same from one card to the next does not re-animate. |
| `tag_on` | `"1918"` | The word where the tag slides in (the date or the place name). The default is the start of the scene. |
| `name_card` | `"kaiser_wilhelm"` | The first time a named person appears (cast id); the name and role come from `cards/_film.json`. |
| `time`, `weather`, `tint` | `"dusk"`, `"rain"`, `"cold"` | Light and mood: dawn for beginnings, dusk for endings, night for fear, rain for defeat, grey for grief. |

### Text fields (rare; most of the film has no text at all)

| field | example | use it only for |
|---|---|---|
| `caption` | `{"from": "So how does", "to": "summer?", "accent": ["Paris", "collapse"]}` | The film's 2–4 **big questions**. The words appear as they are spoken; accent words are amber. Put it on an **acted** card, not on a map or document. |
| `stat` | `{"text": "About 56 km from Paris", "sub": "the closest since 1914", "top": "June 1918", "on": "fifty-six"}` | One number that must be read, at most one every ~2 minutes. Usually the voice says the number and the picture shows the thing. |
| `paper_note` | `{"lines": ["Fight on.", "Never surrender."], "kicker": "Orders, 1944", "on": "Fight", "accent_last": true}` | The exact words of an order or quote, typed on a small paper note over an acted scene. |
| `date`, `place` | `"21 FEBRUARY 1916"`, `"VERDUN"` | The older paper badges. Prefer `tag`. |
| `label`, `counter`, `stamp` | | Short tags, a running number, a verdict stamp. Use them sparingly (battle chapters, verdicts). |
| `letterbox` | `"DRAMATISED"` | Cinema bars for a dramatised moment, about once per chapter. |

### What the compiler adds for you (do not write these)
- **Transitions**: every scene comes in with a 0.6 s dissolve, and every change of camera set-up inside a place dissolves too. The first scene of the film starts on a cut. Use `"transition": "cut"` only for a deliberate shock.
- **Camera**: a slow push-in on almost every set-up, close-ups timed on the `…_on` words, and an extra reframing in any set-up longer than 6 s.
- **Sound**: ambience from the place, and sound effects from what happens (footsteps, guns, a fist on a desk). There is **never music**.

## 4. How long is a card?

- A card should cover **one idea**: usually one sentence, 3–10 seconds.
- Long sentences with two ideas get two cards. Start the second at its clause, e.g. `"at": "inflicting losses"`.
- Very short sentences, under 2 seconds, join the card before or after.
- The compiler warns about cards under 1.8 seconds or over 12 seconds.

## 5. JSON rules (the checker is strict)

- Use double quotes `"` only. Never use single quotes.
- No comma after the last item in a list or object.
- Numbers have no quotes: `"falls": 3`. True and false are `true` and `false`, with no quotes.
- Lists look like `["Verdun", "Metz"]`.
- Nothing after the closing `}` of the file.

## 6. Worked example

Read both examples before writing your first chapter:
- `projects/example-ww1-cold-open/cards/ch01.json`: 60 s, 14 cards, told as a film. It has story places, an arrival, an interruption, a confrontation, the front, a ridge looking at Paris, the big questions and a historian at a blackboard. About 95 % of it is acted.
- `projects/example-ww1-verdun/cards/ch01.json`: 2 minutes of battle narration, 28 cards.

## 7. After each chapter

Run the quick check:
```
python tools/make.py projects/<slug> check
```
Fix what it says, then write the next chapter. When all chapters are written, go to [04-compile.md](04-compile.md).
