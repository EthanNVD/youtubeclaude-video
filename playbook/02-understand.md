# 02 — Understand the script (before ANY card)

Films go wrong when scenes are chosen from keywords: every "attack" becomes the same picture, and the film loops. You avoid that by understanding the story first.

## 1. Read the whole narration

Open `work/reading.md` and read it from the first line to the last line. If it is long, read it in parts of about 300 lines, and keep going until the end. Do not start writing cards after reading only the beginning.

While reading, keep a scratch list of:
- **people** (every name);
- **places** (every town, river, country);
- **dates**;
- **numbers** (casualties, distances, durations);
- **turns** in the story ("but", "then", "by the end of…").

## 2. Fill in `understanding.md`

The file is already in your project; it was copied by `prepare`. Fill in every section. Here is how to do each one.

**§1 The film in three lines.** The question the video asks, its answer, the era and the sides.
- These decide `era` and `sides` in `cards/_film.json`.
- Era is one of `ww1 ww2 napoleonic ancient vietnam modern`.
- Sides come from `recipes/PEOPLE.md`.

**§2 People.**
- Give every named person a short cast id, e.g. `falkenhayn`.
- Pick a `preset` from `recipes/PEOPLE.md`. If the exact person is missing, use the closest preset, e.g. `german_officer`, and note it.
- The name and role written here go on the name card when they first appear.

**§3 Places and dates.**
- Check each place in `data/places.json` (search the file for the name).
- If it is missing, find its longitude and latitude once, write them here, and add them to `cards/_film.json` under `"places"`.

**§4 Numbers.** Mark each number:
- **compare** — the narration puts two or more numbers side by side. This becomes a `chart` card.
- **alone** — a single number. This becomes a `counter` field on an action card, running over the men it counts.

**§5 Chapters.** Split the film into 8–14 chapters of 1.5–4.5 minutes each, starting at sentence boundaries. Mark a chapter **battle: yes** when most of it is about fighting.

**§6 Beats.** Do this one chapter at a time, just before writing that chapter's cards.
- Write one line per sentence or clause, in the form `time | first words | WHO does WHAT | recipe`.
- Choose each recipe from [narration-to-picture.md](narration-to-picture.md).
- Then check the lines against three rules:
  - No recipe appears on two lines in a row.
  - In a battle chapter, at least 6 lines in 10 are action recipes. Any other chapter needs at least 4 in 10.
  - Each number marked "alone" is on an action line as a counter.

**§7 Fact flags.**
- List names the subtitles may have misspelled, and claims the narration itself calls uncertain.
- On screen, spell names correctly.

## 3. Example

See `projects/example-ww1-verdun/understanding.md` for a filled-in example covering two minutes of WW1 narration.

## Done when

Every section has content, and §6 is filled in for the chapter you are about to build. Tick "understand" in `STATUS.md`.
