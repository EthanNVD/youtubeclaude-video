# Thumbnails (3 per video, engine-drawn)

## What the reference channel's top 10 do
| title | thumbnail text | picture |
|---|---|---|
| What Was The REAL Turning Point of WW2? | 7 DAYS. WAR LOST. | split: DEC 5 / DEC 11 1941 badges, leader confident → leader panicking, arrows |
| Could the Soviets REALLY Have Beaten Hitler Alone? | ALONE? 1941–1945 | angry leader + Lend-Lease trucks, map behind |
| Why Operation Barbarossa Was COMPLETELY Avoidable | A DUMB IDEA | burning map, leader sweating with a fake grin |
| Why The Battle of Midway Was COMPLETELY Avoidable | NOT 5 MINUTES | burning carriers from above, admiral crying with a stopwatch |
| How Every Country Teaches Hitler | WHOSE HISTORY? | figure at a desk with a book, 6 flags |
| The ENTIRE Eastern Front Explained | EASTERN FRONT 1941–1945 | two leaders face to face, map split red/blue |
| The Deadliest Battles in Human History | 70,000 / 1 IN 18 / 2 MILLION | triptych, one number per panel |
| What Happened to Hitler's Family After the War? | MY NAME IS HITLER. | sad young sailor, fingers pointing at him |
| Why the Fall of France Was COMPLETELY Avoidable | 6 WEEKS. FRANCE LOST. | split MAY 10 / JUNE 22 1940, general calm → panicking |
| What REALLY Lost Germany WW2? | 1 VS 3 | panicking leader vs three leaders + factories |

**Formula**: one strong emotion on a recognisable face (sweat drops in 5/10) · a map or the place behind (7/10) · 2–4 words, white + one accent colour (yellow or red), heavy black outline · the text **adds the twist the title doesn't say** (title "Avoidable" ↔ thumb "NOT 5 MINUTES") · split before/after with date badges (3/10) · numbers (4/10).

## Three angles → three thumbnails
1. **Transformation / myth** — split screen, two date badges, same person calm → panic; text = the twist ("NOT BAD LUCK.", "6 WEEKS. LOST.").
2. **Person / secret** — one character big (scale 2.3–2.8, head in the upper half), the key prop or document, 2–3-word text ("ONE FAKE MESSAGE").
3. **Numbers / stakes** — versus or triptych with flags, a big "4 VS 3" / "1 IN 18" and a short question.

## Writing `thumbs.json`
```jsonc
{ "thumbs": [ { "panels": [ <scene>, <scene> ], "texts": [ {"text": "NOT BAD LUCK.", "accent": "NOT", "x": 960, "y": 330, "size": 210} ] }, … ] }
```
- A panel is a normal scene (`type` stage/map, `set`/`map`, `elements`, `date`, optional `at` = time to freeze, default 2.5 s; use `in` ≤ 0 for elements you want fully visible).
- With 2 panels each shows only the centre half of its own 1920-wide scene (**x 480–1440**); 3 panels → x 640–1280. Date badges are moved to each panel's corner automatically.
- Text: `size` 150–300, `y` 250–350 (top) or 950–1030 (bottom), `accent` words (yellow by default, `accentColor: "red"`), `color`, `box` (colour bar behind), `font: "comic"` for a punchier variant, `anchor`.
- Characters for thumbnails: scale 2.0–2.6 with `y` 1200–1300 (bust shot), strong `expr` (`panic`, `smug`, `cry`, `angry`, `shocked`) and readable pose (`head`, `cross`, `point`).
- Never put the title text on the thumbnail; never more than 4 words; keep faces clear of text.

## Check
Render (`make.py … thumbs`), open the three JPGs and also look at them at ~25 % size: the emotion, the number/twist and the setting must read in one second. Re-render after fixes.
