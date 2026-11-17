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
{"at": "Attacks on the Western Front", "recipe": "assault",
 "says": "Frontal attacks won almost no ground and killed huge numbers of men.",
 "side": "british", "falls": 3, "hit_on": "cost enormous", "shells": 4}
```

| field | required | how to fill it |
|---|---|---|
| `at` | yes | The first 3–6 words of the narration where this scene starts, **copied exactly** from `work/reading.md`. Spelling must match. Punctuation and capital letters do not matter. |
| `recipe` | yes | The kind of scene. Choose it with [narration-to-picture.md](narration-to-picture.md), then open `recipes/<recipe>.md` to see its fields. |
| `says` | yes | One sentence, in your own words, saying what this part of the narration MEANS: who does what, and why it matters. Do not copy the narration. This proves you understood it. It never appears on screen. |
| recipe fields | depends | Only the fields listed in `recipes/<recipe>.md`. Fields marked **yes** in its "required" column must be there. |
| `variant` | no | Leave it out. The compiler rotates compositions (A, B, C) so scenes never look the same. Set it only to fix a scene that looked wrong in review. |
| common fields | no | `date`, `place`, `name_card`, `label`, `counter`, `stamp`, `time`, `weather`, `tint` (see below). |

### Fields that take narration words (`…_on`, `on`)
- Fields like `react_on`, `hit_on`, `fire_on`, and `"on"` inside `label` or `counter` take **words from this card's narration**.
- The event happens when those words are spoken: the man falls on "cost", the counter starts on "fifty-seven".
- Copy 1–4 words exactly. Leave the field out to let the recipe choose a good moment.

### Common fields (any card)

| field | example | use it |
|---|---|---|
| `date` | `"21 FEBRUARY 1916"` | on every jump in time (badge, top left) |
| `place` | `"VERDUN"` | the place badge under the date |
| `name_card` | `"falkenhayn"` | the first time a named person appears (cast id) |
| `label` | `{"text": "≈ 300 DAYS", "on": "three hundred days"}` | a 1–5 word tag at the top, on the words |
| `counter` | `{"to": 57470, "suffix": " CASUALTIES", "on": "fifty-seven thousand"}` | a number counting up **over the action** |
| `stamp` | `{"text": "FAILED", "on": "failed"}` | a stamp slammed on screen (verdicts, myths) |
| `time` | `"dusk"` | `day dusk dawn night`: mood and silhouettes |
| `weather` | `"snow"` | `rain snow` |
| `tint` | `"grey"` | grief (`grey`), memory or myth (`sepia`), `cold`, `warm` |
| `letterbox` | `"DRAMATISED"` | cinema bars, about once per chapter, for a dramatised moment |

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

`projects/example-ww1-verdun/cards/ch01.json` covers 2 minutes of narration in 28 cards: 70 % action, 8 % talk, 10 % maps, 12 % documents and charts. Read it before writing your first chapter.

## 7. After each chapter

Run the quick check:
```
python tools/make.py projects/<slug> check
```
Fix what it says, then write the next chapter. When all chapters are written, go to [04-compile.md](04-compile.md).
