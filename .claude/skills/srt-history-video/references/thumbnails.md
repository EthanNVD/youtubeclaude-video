# Thumbnails — detailed prompts for an image model (default) + engine draft/overlay

The reference channel's thumbnails are **AI-painted** (rich shading, painted maps, fire, smoke) but keep the
channel's character design. Engine drawings cannot reach that level of finish, so the deliverable is:

1. **3 detailed prompts** (one per title angle) → the user generates the images in ChatGPT / Gemini / Ideogram / Midjourney / Flux.
2. **A character reference sheet** (`out/thumbs/ref_characters.png`, rendered from the engine). The user attaches it so the model keeps the cast's look.
3. **Engine drafts** (`thumbs.json` → `out/thumbs/thumb_N.jpg`). They are a layout preview, and a fallback if no image model is used.
4. **Headline compositing**: when the model misspells the words, the user drops the image as `input/thumb_N.png`. `make.py thumbs` then puts a pixel-perfect headline on it.

## What the reference channel does — all 32 thumbnails (Nov 2026)

Layout counts:

| layout | count | examples |
|---|---|---|
| **versus**: two busts at the left/right edges facing each other, the conflict object/map in the middle | 12 | NO, WE WON! (trophy) · DON'T ATTACK? · NOT MIDWAY? · A FEW ROCKS? · BOTH SAID STAY · WHO PLANNED FIRST? (handshake) · THEY SAW IT COMING · EASTERN FRONT |
| **hero**: one huge bust (head 45–55 % of the height) on one side, the story scene behind | 9 | NOT 5 MINUTES (stopwatch + burning carriers) · A DUMB IDEA (map on fire) · DOOMED ANYWAY? · ALONE? · AFTER VICTORY? (document) · WORTHLESS TROPHY · MY NAME IS HITLER. (pointing hands) |
| **split before→after**: same person calm → panicking, with date tags | 7 | 7 DAYS. WAR LOST. (DEC 5 / DEC 11) · 6 WEEKS. FRANCE LOST. · TOO LATE? · BIG PLANS. NO FUEL. (diagonal) · 3 MONTHS → 8 YEARS · 1 VS 3 |
| centre + framing elements | 2 | WHOSE HISTORY? (flags in frames) · WHY SWITCH SIDES? (uniforms on hangers) |
| triptych of numbers | 1 | 70,000 / 1 IN 18 / 2 MILLION |
| objects only | 1 | STILL KING? (tanks, crown) |

**Headline text**
- Length: 1–5 words, median 3. 14/32 end with "?". The text never repeats the title; it gives the twist or the provocation.
  - Title "…Midway Was COMPLETELY Avoidable" ↔ thumbnail "NOT 5 MINUTES".
  - Title "Did Winter REALLY Defeat Hitler?" ↔ thumbnail "IT WASN'T WINTER".
- Position: top in 24/32, bottom in 6 (mostly the split layouts, so the date tags stay on top), centre in 2.
- Colour: white plus one accent. Yellow accent in 21/32, red in 5, icy blue once (WINTER).
  - The accent goes on the twist word: NOT, DUMB, FAKE, KNEW, a number.
- Font:
  - Condensed ultra-bold, like Anton/Impact: about 19/32.
  - Chunky rounded, like Luckiest Guy/Lilita: about 13/32.
- Every headline has a thick black outline (about 1/6 of the letter height) and a drop shadow, spans 80–95 % of the width, and is sometimes tilted about −2°.
- Variants: a red rounded plate behind the text ("MY NAME IS HITLER."), a torn-paper colour band ("DOOMED ANYWAY?", "ALONE?"), two lines in two sizes.

**Characters**
- They are the same chibi design as the videos: big round head sitting directly on the body, simple eyes. About a third of thumbnails use a more painted, semi-real caricature.
- Placement:
  - Busts are cut by the frame edge.
  - Faces turn toward the centre or toward the conflict.
  - A face is never covered by text.
- Emotion is the hook:
  - sweat drops: 14/32;
  - panic with hands on the head: 6;
  - pointing: 7;
  - smug with crossed arms: 5;
  - crying: 3;
  - a fake nervous grin: 2.
- In before/after splits the same person goes calm → panic.

**Story symbol**
- About a third of thumbnails show one object that carries the twist, held or placed beside the face: stopwatch, hourglass, fuel gauge on E, trophy, a document with a title (GENERALPLAN OST, HIROSHIMA / SOVIET ENTRY, WAR), plan books, handcuffs on "General Winter".

**Backgrounds**
- Saturated political maps appear in 19/32: red vs blue/yellow, white borders, sometimes painted terrain.
- Other common backgrounds: the event itself (burning ships, city on fire, mushroom cloud), and flags (14/32).
- Map graphics:
  - big curved red arrows with a white edge: 8;
  - red highlight circle: 3;
  - white label boxes with black capitals ("LENINGRAD", "HANKO", name plates "YAMAMOTO / NIMITZ");
  - black date tags with white text: 4.

**Finish**
- Strong saturation and contrast, warm vs cold complementary colours (fire orange against sea blue, red USSR against blue Europe), and a soft vignette.
- A glow or rim light separates the character from the background.

**Never copy**: Their thumbnails show swastikas. We don't (YouTube limited-ads risk; channel rule). Use a plain red armband instead.

## Three angles → three thumbnails (one per title)

| angle | layout | headline idea | picture |
|---|---|---|---|
| myth / turning point | hero or split | the twist in 2–3 words ("THEY KNEW.", "NOT WINTER") | the famous moment + the person who got it wrong, panicking |
| person / secret / decision | versus or hero with object | the secret or the question ("ONE FAKE LINE?", "SHORT OF WATER?") | decider vs decider around the key object or map |
| numbers / stakes / time | split (date tags) or triptych | the number ("6 MINUTES.", "4 VS 3?", "1 IN 18") | before → after, or one number per panel |

The 3 thumbnails must be three different pictures, not 3 variants of one.

## Writing `youtube/thumb_prompts.json`

`python tools/make.py projects/<slug> prompts` builds the final prompts from this file. It adds:
- the fixed STYLE block distilled from the 32 thumbnails;
- character looks taken from the engine presets / plan cast;
- the expression and pose wording;
- the AVOID list (no swastikas, no gore, no extra text, no watermark, correct hands).

It also renders the reference sheet.

```jsonc
{ "thumbs": [
  {
    "angle": "myth vs truth",
    "title": "Why The Battle of Midway Was NOT Bad Luck",         // the title this thumbnail pairs with
    "layout": "hero",            // hero | versus | split | split_diagonal | triptych | center | object
    "heroSide": "right",         // hero only
    "background": "bright Pacific seen from slightly above, three Japanese carriers (red circle on the deck) burning, black smoke, US dive bombers diving out of the clouds",
    "middle": "…",               // versus/center/object: what sits between the characters
    "characters": [
      { "who": "nagumo",                      // cast id or preset → appearance is described automatically
        "name": "Vice-Admiral Chuichi Nagumo", // real name helps the model; the description carries the look
        "look": "…",                           // optional: overrides the automatic description (custom people)
        "position": "right 40%, big bust, head top ~18% from the top, turned toward the ships",
        "expr": "panic",                       // panic cry sad smug angry determined worried shocked grin happy thinking tired
        "pose": "head",                        // head cross point pointUp show hold holdUp chin shrug salute binoculars fist cheer present wipe face stop
        "prop": "a gold stopwatch",            // for show/hold/holdUp
        "target": "the burning ships",         // for point/present
        "extra": "Two big blue sweat drops fly off his head." }
    ],
    "panels": [ { "scene": "…", "tag": "10:20 AM", "characters": [ … ] }, … ],   // split / triptych
    "symbols": ["a thick red curved arrow from the planes to the carriers"],
    "labels": [ { "text": "MIDWAY", "where": "next to the red ring" } ],          // short, few
    "text": { "position": "top-left", "font": "condensed",                        // condensed | rounded
              "lines": [ { "text": "THEY KNEW.", "accent": ["KNEW."], "accentColor": "yellow" } ] },
    "light": "warm firelight on the face from the left, glow behind the head",
    "palette": "ocean blue vs fire orange, one yellow accent",
    "avoid": ["…extra things to avoid…"],
    "fix_tips": ["If the face is small: 'bigger head, closer crop'."]
  }
] }
```

Rules:
- `text.lines` is 1–2 lines and at most 4–5 words in total, written in the SRT language. Vietnamese works best with ChatGPT or Ideogram; with other models use the clean plate + compositing.
- Describe the background as **one concrete moment** (who/what/where/when), not a list of keywords.
- Put the most important element in the biggest shape. The emotion must be readable at 25 % size.
- Use real historical names; the generated look comes from the preset description, which keeps the caricature consistent with the video.
- Keep labels to at most 3, each 1–2 words. Date tags are for splits only.

## Output — `out/youtube/thumb_prompts.md`

Each thumbnail gets three prompt variants:
- **Full prompt**, with the headline rendered by the model: ChatGPT (gpt-image), Gemini / Imagen, Ideogram, Flux. Ask for 16:9 (1536×864 / 1792×1024) and attach `ref_characters.png`.
- **Clean plate**, with no text: keeps the headline area simple so you can add the headline later.
- **Midjourney v7**: compact, with `--ar 16:9 --v 7 --style raw --s 150 --no …`. Midjourney draws text poorly, so prefer its clean plate.

The same prompts are also in `out/youtube/prompts/thumb_N_<variant>.txt`.

## Compositing the headline on the user's image — `thumbs.json`

1. Put the image in `projects/<slug>/input/thumb_N.png` (or .jpg / .webp).
2. Run `python tools/make.py projects/<slug> thumbs`. The image becomes the background, and `texts` from `thumbs.json` thumbnail N are drawn on top (the draft overlay is skipped).

Text options:
- `size` 150–300; `x`, `y`;
- `accent` words, `accentColor`;
- `font`: `heavy` (Anton) · `round` (Baloo 2, Vietnamese OK) · `comic`;
- `maxWidth` (squeezes to fit), `rotate`, `plate` (rounded colour box), `box`, `outline`, `shadow`.

## Engine drafts (layout preview / fallback) — `thumbs.json`

```jsonc
{ "thumbs": [ {
  "panels": [ <scene>, … ],            // 1 = hero/versus, 2 = split, 3 = triptych; normal scenes frozen at `at`
  "split": "diagonal",                 // 2 panels only (default vertical)
  "overlay": [ <elements in full-frame px> ],   // busts that cross the split, arrows, rings, labels, `drop`, `hand`, `torn`, `glow`
  "texts": [ {"text": "THEY KNEW.", "accent": "KNEW.", "x": 620, "y": 250, "size": 250, "rotate": -2} ],
  "grade": "punch"                     // punch (default) | soft | none
} ] }
```

Placement and element notes:
- Busts: actor `scale` 3.2–3.8. Put `y` (the feet) at about 1330 so the head centre lands near y 560 and the hips fall under the frame.
- Use `map.style: "poster"` for the saturated map look.
- Split date tags come from the panels' `date` and are drawn as black boxes.
- Element `drop`: a big sweat or tear drop (`size`, `falling`).
- Element `hand`: a giant pointing hand with a sleeve (points to +x; use `rotate`/`flip`, `sleeve`, `skin`).
- Element `torn`: a torn-paper band (`w`, `h`, `color`).
- Element `glow`: a radial light (`r`, `color`, `strength`).

## Check before delivering

1. Open the drafts and the reference sheet. Read `thumb_prompts.md` once as the image model would: does every prompt say who, where, what emotion, what symbol, which exact words, and where the text goes?
2. Tell the user which variant to use for which model. Say that `make.py thumbs` can fix the text on their images.
3. After the user brings images back, look at them at 25 % size:
   - emotion, headline and symbol readable in one second;
   - headline spelled exactly;
   - no hate symbols;
   - faces not covered.
