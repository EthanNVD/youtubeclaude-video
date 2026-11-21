# Storytelling like an animated documentary film (measured on the reference channel)

**Source.** Two Ember History films:
- *The Entire History of China in 19 Minutes*;
- *The ENTIRETY of World War II, Explained*.

**Method.**
- 455 shots segmented at 10 fps (dissolves included).
- Camera motion measured on every frame (30 fps) with ECC alignment.
- Words aligned to 0.125–0.25 s frame strips.

The detailed study, with per-shot sheets and the 60-second test, is in `projects/ember-test/ANALYSIS.md`.

This page is the *why*. The *how* for writing cards is in `playbook/narration-to-picture.md`; the engine fields are in `plan-schema.md`.

## 1. Numbers

| | value | what we do |
|---|---|---|
| shot length (median / 10th–90th percentile) | 4.6 s / 2.5–8 s | one card per idea, 3–10 s; montage clauses 2–4 s |
| transitions that are dissolves | ~88 % | every scene comes in with a 0.6 s dissolve (`transition: "fade"`, the default) |
| dissolve length | median 0.6 s (0.4–0.9) | `TD = 0.6` (`transitionDur` to override) |
| hard cuts | ~4 % | `"transition": "cut"` only for a shock |
| reframing inside a place | by dissolve | `shotDissolve: true` (the default for cards) |
| shots with a slow push-in | ~80 %, ~1.5 % per second | `push` 0.03–0.06 on every set-up |
| shots with a slow pan | ~55 %, ~25–30 px/s at 1080p | `panX` 40–80 on wides |
| fully static shots | ~10 % | documents only |
| pixels moving inside the frame (camera removed) | ~2 % | small, meaningful acting, not constant motion |
| text reveal after its word | +0.25 s, fading in over 0.25–0.5 s | `tag_on`, `stat.on`, `paper_note.on` add 0.25 s |
| big-question caption | word by word as spoken, 0.2 s fade, amber accents | `caption` field |

## 2. Grammar

1. **One clause, one concrete picture.** In the opening, every clause gets its own literal vignette about 2.5 s long:
   - "farmed" → farmers on terraces;
   - "written" → a hand writing a character;
   - "ruled" → an emperor enthroned;
   - "conquered by horsemen" → riders;
   - "torn apart by civil wars" → two armies facing each other;
   - "carved up by foreign empires" → foreign names appear on the map;
   - "came back together" → map pieces merge;
   - "rose again" → a skyline lights up.
2. **Enter through a person in a place (anecdote).** Wang Yirong, 1899:
   - courtyard → study → pharmacy with a drawer labelled "DRAGON BONES" → bone insert → magnifier.

   Onoda, 1974:
   - 12 s of a man walking out of the jungle → his rifle side-on ("500 ROUNDS") → his face with a name card.

   A place is built as **outside → inside → person → detail**, with dissolves between.
3. **The same place, changed by time.** Onoda's jungle path goes day → rain → dusk → night, with newspapers on a stump, then a tent, and "29 YEARS". The Zhou palace goes calm → storm → rebels' torches.
4. **Absence and symbols instead of the act.**
   - "He died believing he had failed" → the empty stool under the tree.
   - "Wars grew bloodier" → a broken chariot wheel and spears in the ground.
   - Massacres → an empty ravine in mist, rails to a gate, rows of candles.
5. **Echo and irony.** The 1918 and 1940 railway carriages side by side; Foch's "armistice for 20 years" → a timeline counting "20 YEARS + 65 DAYS".
6. **Text with one identity, used rarely.**
   - The place/time tag (wooden plank, top left) slides in on the date and stays while we stay.
   - Quiet name cards.
   - A few engraved stat cards over mood pictures.
   - Paper notes for quotes ("FIGHT ON. NEVER SURRENDER.").
   - Word-by-word captions **only** for the film's questions.
7. **Maps are short bridges.** Regions fill about 0.25 s after the word. The map dissolves into the scene at that place (Leningrad map → tram street).
8. **Calm battles.** War is wide landscapes with small moving units, aftermath, and the people deciding and enduring. Spectacle is rare; meaning comes first.

## 3. What this means for our films

- The default card set for a story place is:
  - `establish` (outside, tag on the date);
  - `approach` (people on their way, name cards);
  - `interrupt` / `confront` / `decision` / `dialogue` (the room);
  - `contemplate` (alone with it).
- At the front:
  - `watch_front` → `binocular_view` → `vista`;
  - the fighting recipes when the narration describes fighting;
  - `absence` / `aftermath` / `silhouette` for the cost.
- Questions become `caption` on an acted card. Most numbers stay spoken.
- There is no music in our films. The reference uses soft music; we use ambience and sound effects only.

## 4. Engine features behind it

| feature | engine field |
|---|---|
| shot dissolves | `scene.shotDissolve` |
| scene dissolves | `transition: "fade"`, 0.6 s |
| place/time tag | `scene.tag`, `scene.tagIn` (−1 = already there) |
| big-question caption | element `caption` (`words: [{w, t, accent}]`) |
| stat card | element `stat` (`text`, `sub`, `top`) |
| paper note | element `note` (`lines`, `kicker`, `accentLast`) |
| binocular view | element `binoculars` |
| chalk writing | label style `chalk` |
| fonts | `FONT.title` (Cinzel), `FONT.book` (Cormorant Garamond) |
