# Storytelling grammar (from the reference channel)

Source analysis: `docs/PHAN-TICH-NGUON.md` (5 sample videos, top-10 metadata, frame studies). This is the method, not a template to copy — create your own devices, places and compositions for each script.

## Macro structure (25–45 min videos)

```
COLD OPEN  0:00–~1:30   one concrete moment with date/time (in medias res) → the paradox → the question
SETUP      ~1:30        the device + how it scores ("we count every exit, for both sides")
CHAPTERS   8–14 × 1.5–4.5 min   date → place → decision-maker → consequence → device update → bridge line
VERDICT    last 3–5 min  answer the opening question with the device; what historians still debate;
                         a quiet serious hold (graves, candle, empty helmet) before the outro
```
Pace: ~1 beat per 15–20 s, 1–4 shots per beat, average shot 4–8 s. Montage lists can cut every 1–2 s; grief and verdict hold 8–15 s.

## The device (the spine)
One recurring, scored visual that turns the argument into something physical. It returns at the end of every chapter in an updated state and delivers the verdict. Choose by the script's logic:

| script shape | device | engine element |
|---|---|---|
| "Was X avoidable?" — a chain of missed choices | road / sea lane with EXIT signs passed one by one, score for both sides | `road` + `scoreboard` |
| "What was the REAL turning point?" — weighing candidates | balance scale, weights per candidate | `scale` |
| "Could A have done it alone?" — dependency | meter swinging between outcomes, or two supply lines | `meter`, `bars` |
| "What REALLY caused X?" — ranking causes | workbench/list No.10 → No.1 | `ranking` |
| "Deadliest / biggest…" — comparisons | ranking boards per criterion | `ranking`, `bars` |
| "How every country…" — survey | a desk / table with one slot per case, green/red marks | `ledger`, stage props |
| biography / family | timeline or tree on a board | `timeline` |
A presenter character (archivist, accountant…) may own the device; keep them optional and consistent.

## Acting first (the reference channel animates *scenes*, not slides)

Frame studies of the reference videos (Midway, Turning Point) show that most screen time is **people doing things in a real place**:
- Rochefort shuffling through the basement in slippers.
- Two politicians walking down a garden path while arguing.
- An admiral at his desk lifting a telegram.
- A pilot looking down from the cockpit.
- Crews loading bombs in the hangar.

Maps and devices bridge these scenes. Target per chapter: **world/acting ≥ 60 %**, maps 15–25 %, device/charts/documents ≤ 20 %, host 5–10 %.

**Every world shot** = place + action + reaction:
- **Place**: use a detailed set and add life.
  - Sets: `garden`, `bridge`, `deck`, `hangar`, `radio`, `tent`, `corridor`, `parliament`, `cell`, `train_interior`, `cockpit`, `airfield`, plus `office`, `cabinet`, `warroom`, `codebreak`, `trench`, `harbor`, `city`…
  - Foreground `fg` for depth: `plant`, `curtain`, `rail`, `grass`, `sandbags`, `officedesk`, `doorframe`, `branches`, `barbed`.
  - `time`/`weather` for mood.
- **Entrance**: characters walk or run in (keyframe `x`: walking is automatic, with stride, knee bend and arm swing; fast moves become a run). Do not start every shot with people already standing still.
- **Business**: what the hands do on the key words: `hold`/`show` a document (`holds`), `typing`, `write`, `binoculars`, `phone`, `carry` a crate or bomb, `pointUp` at the sky, `pointL`/`point` at a map, `drink`, `smoke`, `salute`.
- **Reaction**: switch `pose` + `expr` on the word that hurts or helps (pose keys blend in 0.4 s with overshoot), e.g. binoculars → hands on head + panic; hold paper → cheer. Use `headMove: nod|shake|tilt` for listening, denial and doubt.
- **Talking**: `talk: true` gives mouth, head nods and beat gestures, so the speaker gestures every few seconds.
- **Cut rhythm**: 2–4 s shots inside action sequences (wide → reaction close-up → detail), 5–8 s for explanations. Push in on the reaction (zoom 1.2–1.4 over 0.2–0.3 s).

### The host (recurring narrator — `who: "host"`)
A young field historian: tousled brown hair with a cowlick, round glasses, tweed jacket, mustard vest, red scarf. Variants: `host_field` (coat), `host_winter` (ushanka). He is the same in every video.

Use him for:
- the cold-open *myth* line: `study` set, holding the symbol prop, `headMove: shake` → `stop`;
- presenting the device (`present`, `explain`, `point` at the scale or bars);
- chapter transitions (walking along a `corridor`, sitting in a `train_interior`);
- the verdict and the outro question.

Keep him out of the historical scenes themselves.

## Clause → picture (choose the visual language)

| the narration says… | show… |
|---|---|
| who decided / argued / reacted | **world**: the person in a functional room (desk, map on wall, phone, clock), with a prop that embodies the argument (abacus for "his maths", a MUNICH card for appeasement) |
| where, how far, who moves where, encirclement | **map**: same map stays while layers appear in narrative order; arrows draw tip-first; pincers advance → meet → glow → pocket appears |
| numbers, comparisons | **bars / counter** placed in the world that produces them when possible (shipyard + BUILT > SUNK) |
| a claim is false / a myth | the claim as a quote/prop → **stamp MYTH** (red) → the evidence |
| an order, telegram, letter, code | **document** typed on screen, then a stamp or a person's reaction |
| time pressure | **clock badge** advancing (10:20 → 10:25), stopwatch prop |
| counterfactual "what if" | same set/map with `tint: "sepia"` and a dashed arrow |
| tragedy, death toll | slow, sparse: candle, graves, empty chair, grey tint; few elements, no jokes, low/no SFX |
| two sides | split screen with `panel`s, or the two nations on opposite sides of a map/scale, same staging for both |

## Rules that make it read like the channel
1. **Action before explanation** — the opener is an event, not a title.
2. **Before → action → after → reaction**: the hand reaches, touches, lifts; the arrow travels then the pocket closes; the officer reads the telegram, then sweats. Do not cut away before the result is visible.
3. **Camera mostly still**; motion comes from actors, arrows, gauges, light. Change framing with **cuts** (wide master → close on the evidence/reaction → back). Slow push-in on maps is fine. One camera idea per shot.
4. **Reveal what a character could not see**: limited view first (soldier on a beach), then the wider shot that shows what he missed.
5. **Text hierarchy**: date badge (place/time jump), name card (first appearance), labels glued to objects, stamps for verdicts. 1–5 words. Never subtitles.
6. **Callbacks**: reuse props/sets/compositions when the story returns to them; keep state (a sunk ship stays sunk, the score keeps its number).
7. **Both sides**: whenever one side gets a scene of its decision, the other side's decision gets the same treatment.
8. **Accuracy**: dates, flags, uniforms, borders (pick the right `era`), numbers exactly as narrated; show uncertainty ("~", "est.", "debated").
9. **Variety**: no more than ~3 consecutive shots of the same visual language; alternate wide/close; don't reuse the same composition for different ideas.
10. **Respect**: victims are never a punchline; Nazi symbols are not drawn (the armband is a plain red band).

## Shot recipes (copy the idea, not the numbers)
- **Decision in an office**: `office` + actor `chin`/`worried` → cut-in (`zoom` 1.4 in 0.2 s) on the telegram prop → reaction `sweat`.
- **Phone call between capitals**: two scenes back-to-back, each actor `pose: phone`, same framing mirrored (`flip`).
- **Advance**: map, `arrow` drawing over 1.5–2.5 s, `unit` counters moving with `keys` on `at`, city captured → `city` + small `stamp`.
- **Encirclement**: two arrows from both sides (`dur` 2), at their meeting time a `burst` small + `pocket` polygon `enter: fade`.
- **Battle at sea**: `sea` set, ships at different scales for depth, `burst` on the hull + `fire` + `smoke` stay afterwards.
- **Air raid on a city**: `city` `time: night`, `searchlight` fx ×3, `burst` among buildings, `smoke`.
- **Production race**: `factory` set with sparks, then `bars` on `paper`.
- **Myth**: `studio` dark + prop + `label style plain` with the quote → `stamp MYTH`.
- **Verdict**: device full-screen, final weight/needle/score, `stamp VERDICT`, then a quiet `memorial` hold.
