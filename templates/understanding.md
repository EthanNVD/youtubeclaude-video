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
| kaiser_wilhelm | kaiser_wilhelm | Kaiser Wilhelm II | German Emperor | is told on 29 Sept 1918 that the war is lost |

## 3. Story arcs (anecdotes) — the people the film follows
A documentary told like a film follows a few people in a few places. List each anecdote the narration tells, with the person and the place we will keep coming back to.

| arc | person(s) | main place(s) (place_id) | where it starts and where it returns |
|---|---|---|---|
| the Spa meeting | Hindenburg, Ludendorff, Kaiser | spa_hq, spa_corridor, kaiser_study | cold open; returns at the verdict |

## 4. Story places (place_id)
Every place that appears more than once, with its setting, its tag text, and how it changes over time.

| place_id | setting | tag text | appears at (times) | changes (time / weather / what is there) |
|---|---|---|---|---|
| marne_ridge | nomansland (vista) | The Marne · June 1918 | 0:34, 0:39 | dusk: they look at Paris → dusk: they turn back |

Check each map place in `data/places.json` (search the file for the name). If it is missing, write its coordinates here and add them to `cards/_film.json` "places".

## 5. Symbols and big questions
- **Symbols**: objects or images that stand for an idea and can come back. Examples: an empty helmet for the dead; the clock for "two hours"; the ridge facing Paris for the high-water mark.
- **Big questions**: the 2–4 questions the film asks out loud, usually in the opening and the verdict. Copy their exact first and last words; they become `caption`s.

## 6. Numbers
List every number in the narration (casualties, distances, durations) and decide how each one is shown:
- **spoken only**: the scene shows the thing, and the voice says the number. This is the default.
- **stat**: the one number per ~2 minutes that must be read on screen.
- **chart**: two or more numbers that are compared.

## 7. Chapters
Split the film into 8–14 chapters of 1.5–4.5 minutes each. Start each chapter at a sentence boundary.

| # | starts at (time + first words) | title (1–4 words) | what happens in it | arcs / places used |
|---|---|---|---|---|

## 8. Beats, chapter by chapter
Fill this in one chapter at a time, just before you write that chapter's cards.

For every clause, answer the five questions of `playbook/narration-to-picture.md` §1 in one line:

`time | first words | WHO | DOES WHAT (visible action) | WHERE (place_id) | WHEN (time/weather) | recipe`

Rules:
- Every line names a visible action. "is shown", "map of", or "text saying" are not actions.
- Never write the same recipe on two lines in a row, unless it is the same place revisited.
- At least 3 lines in 4 are acted recipes (sections A, B and C of the lookup table).
- Maps are at most 5 s each; numbers are spoken, not written, unless the line says "stat".

Example:
```
0:00 | On the 29th of September | Hindenburg, Ludendorff | arrive by car at dawn, sentry salutes | spa_hq | dawn | establish (tag on "1918")
0:07 | Field Marshal Paul       | the two generals      | stride down the corridor            | spa_corridor | day | approach (name cards)
0:11 | told Kaiser Wilhelm      | Kaiser + generals     | Kaiser stops writing, looks up, stunned on "could no longer" | kaiser_study | day | interrupt
0:16 | Not for weeks.           | officer at the front  | checks his watch, tanks roll out of the mist, panics on "two hours" | front | dawn | watch_front
0:20 | Germany needed an armistice | Ludendorff → Kaiser | fist on the desk on "immediately"  | kaiser_study | day | confront
0:23 | The Kaiser could hardly  | Kaiser                | walks to the window, back to us     | kaiser_study | dusk | contemplate
```

## 9. Fact flags
List anything that is uncertain or debated, and any name that may be misspelled. Fix the spelling on screen; never change the timing.
