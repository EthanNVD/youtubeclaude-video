# 04 — Compile the cards and fix them

```
python tools/make.py projects/<slug> cards
```

This does three things:
1. Checks every card.
2. Builds `plan.json`.
3. Runs the engine validator.

It prints one JSON report:

```json
{
 "ok": true,
 "errors": [],
 "warnings": [ "…" ],
 "scenes": 28, "duration": 125.08,
 "mix": {"action": 0.74, "talk": 0.09, "map": 0.1, "device": 0.08},
 "engine_errors": [], "engine_warnings": [ "…" ],
 "coverage": {"setups": 52, "avg_setup_s": 2.41, "close_shots": 17},
 "next": "…"
}
```

## The loop

1. Run the command.
2. If `"ok": false`:
   - Read the first error.
   - It names the file and the card (`ch03.json card #7`) and says exactly what to change.
   - Change it, then go back to 1.
   - Fix errors from the top; one fix often removes several errors.
3. When `"ok": true`, read every warning and fix the ones you can. Most have a direct fix:

| warning starts with… | fix |
|---|---|
| `same recipe '…' as the card before` | Change one of the two cards to the next thing that happens: the consequence, the other side, or a close detail. |
| `chapter '…': only 60 % of the time shows people acting` | Replace map, document and chart cards with the scene the clause describes. Ask the five questions in [narration-to-picture.md §1](narration-to-picture.md#1-the-picture-writing-method-do-this-for-every-clause). |
| `map is …`, `device is …`, `host is …` | Shorten those cards (start the next card earlier), or replace them with acted cards. |
| `a 9.0 s map` | Keep maps ≤ 5 s: move the next card's `at` earlier, to where the narration returns to people. |
| `a caption on a map card` | Move the `caption` to an acted card (big questions run over people, not over maps). |
| `N stat cards` | Keep one `stat` per ~2 minutes; let the voice carry the other numbers. |
| `place_id "…" was "office" … here it is "corridor"` | A `place_id` is one setting. Give the new room its own `place_id`, and repeat the `tag` text if it is the same building. |
| `recipe '…' is used N times` | Swap some of them for other recipes that fit the same sentences. |
| `only 1.2 s long` | Merge it with the card before (delete it) or after (move `at`). |
| `13.5 s long` | Split it at a sentence start into 2–3 cards. |
| `"says" copies the narration` | Rewrite `says` in your own words: who does what, and why it matters. |
| `"at" matched approximately` | Copy the words exactly from `work/reading.md`. |
| `No input/voice.*` | Fine if the user gave only an SRT. Mention it in the hand-over. |
| engine: `crosses …px … sprint` | That recipe needs more time: make the card longer, or choose a calmer variant. |
| engine: `too large next to the people` | Ignore it only for `gun_crew` (heavy guns are drawn big on purpose). |

4. The `mix` line must meet the targets:
   - action + talk (acted recipes) ≥ 0.75 in every chapter;
   - map ≤ 0.10;
   - device (documents, charts, devices) ≤ 0.10;
   - host ≤ 0.08.
5. When the report is clean, go to [05-review.md](05-review.md).

## Errors you may see

| error | meaning | fix |
|---|---|---|
| `"at" … was not found in the narration after the previous card` | The words are wrong or out of order. | Copy them from the narration text shown in the error. |
| `unknown recipe "attack"` | The recipe name is wrong. | Use one of the suggested names; all names are in `recipes/CATALOG.md`. |
| `unknown field "where"` | The field does not exist for this recipe. | Use the allowed fields listed in the error. |
| `"react" = "scared" is not allowed` | The value is not on the list. | Pick one of the listed values. |
| `the phrase "…" is not in this card's narration` | An `…_on` field uses words from another card. | Copy words from this card's own narration, shown in the error. |
| `place "Pless" is not in data/places.json` | A map place is missing. | Add it to `cards/_film.json` `"places"`. |
| `is neither in cards/_film.json "cast" nor a preset` | A person is missing. | Add them to the cast with a preset. |
| `is not valid JSON` | Broken JSON. | Fix the comma or quote at the line given ([03-cards §5](03-cards.md#5-json-rules-the-checker-is-strict)). |
