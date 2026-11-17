# Understanding — fill this in BEFORE writing any card

Read `work/reading.md` from the first line to the last line before you write anything here. Do not skim, and do not stop after the first part.
Write in English, in your own words. Short answers are fine. Do not leave any section empty.

## 1. The film in three lines
- **Question**: what question does the video answer? (one sentence)
- **Answer / verdict**: what does it conclude? (one sentence)
- **Era and sides**: e.g. WW1; Germany vs France and Britain.

## 2. People (everyone named in the narration)
For each person, give the cast id you will use, their preset (`recipes/PEOPLE.md`), and what they DO in the story.

| cast id | preset | name on the name card | role on the name card | what they do in the story |
|---|---|---|---|---|
| falkenhayn | falkenhayn | General Erich von Falkenhayn | Chief of the German General Staff | plans Verdun to bleed France |

## 3. Places and dates
Every place and date the narration names, in order. Check each place exists in `data/places.json`. If it doesn't, write its coordinates here and add it to `cards/_film.json` "places".

| time in reading.md | place | date |
|---|---|---|
| 0:00 | Verdun | February 1916 |

## 4. Numbers
Every number in the narration (casualties, distances, durations). Note which numbers are compared with another number (→ `chart`) and which stand alone (→ a `counter` on an action card).

## 5. Chapters
Split the film into 8–14 chapters of 1.5–4.5 minutes each. Start each chapter at a sentence boundary.

| # | starts at (time + first words) | title (1–4 words) | what happens in it | battle chapter? (yes/no) |
|---|---|---|---|---|

## 6. Beats, chapter by chapter
Fill this in one chapter at a time, just before you write that chapter's cards.

For every sentence or clause, write one line:

`time | first words | WHO does WHAT (or what is SHOWN) | recipe you will use`

Rules:
- Pick the recipe by looking it up in `playbook/narration-to-picture.md`.
- Never write the same recipe on two lines in a row.
- In a battle chapter, at least 6 of every 10 lines are action recipes.

Example:
```
9:59 | By the end of 1915 | Falkenhayn faces a stalemate | decision (worried, warroom)
10:08 | Attacks on the Western Front | men attack and fall for nothing | assault (british, 3 falls)
10:14 | So he went looking | Falkenhayn writes his plan | decision variant C → write
```

## 7. Fact flags
List anything that is uncertain or debated, and any name that may be misspelled. Fix the spelling on screen; never change the timing.
