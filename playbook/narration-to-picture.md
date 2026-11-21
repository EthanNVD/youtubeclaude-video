# Narration → picture: tell the story like an animated film

This is the most important page of the playbook. Read it fully before writing the first card of a film, and look things up in it for every card.

The reference channel (Ember History; measurements in `.claude/skills/srt-history-video/references/storytelling-film.md`) does not illustrate a narration with charts and labels. It **films a story**:
- every clause of the narration gets **one concrete picture of exactly what the clause says**;
- that picture is almost always **people doing something in a real place**;
- the camera drifts slowly and pictures **dissolve** into each other.

Text appears rarely, as a small tag, a big question, or one number.

You write cards; the compiler handles the camera, dissolves and timing. Your job is to choose, for every clause, **what the camera would see if it had been there**.

**Two ways to write a card:**
- **The `scene` card** composes the picture from the clause: an idea, a place, people acting on the words, things, a camera. It is not limited to a fixed composition. Use it for most of the story ([scene-writing.md](scene-writing.md)).
- **A recipe** is a tested composition. It is the fast way when one shows the clause exactly: battles, maps, charts, documents, and the story recipes below.

When in doubt, write the scene card.

---

## 1. The picture-writing method (do this for every clause)

Take one clause of the narration (one idea, usually 3–8 seconds) and answer five questions in `understanding.md` §6.

1. **WHO** is in it? A named person, a group (soldiers, workers, a crowd, a fleet), or "nobody". If the clause is abstract ("the war was lost"), find the people it happens to: the men who retreat, the general who realises, the family who waits.
2. **DOES WHAT?** Turn the verb into a **visible action**:

   | the clause says | the camera sees |
   |---|---|
   | told / informed | X speaks; the listener stops what he was doing |
   | decided | he stands up / slams the desk / points at the map |
   | could hardly believe it | he walks to the window and turns his back |
   | was 56 km from Paris | men on a ridge look at a city on the horizon |
   | the war was lost | exhausted men walking back through the rain |
   | was dismissed | he walks out of the building carrying a suitcase |
   | grew stronger | factories, men drilling, columns marching |
   | starved | a mother puts a turnip on an empty plate |
   | died | an empty chair, a helmet on a rifle (`absence`) |

3. **WHERE?** A real place (an office, a corridor, a hotel front, a trench, a ridge, a classroom, a deck), not a blank background. If we were already there, **stay** (same `place_id`).
4. **WHEN?** The time of day and weather that carry the mood: dawn for beginnings, dusk for endings and losses, night for fear, rain for defeat. Use the same place at a new time to show **time passing**.
5. **WHICH RECIPE?** Look the action up in §2. Pick the recipe that shows the action; never pick by keyword alone.

### Rules for the picture
- **Literal and concrete.** "The fighting spread across Europe, Asia and Africa" is shown as a map that fills in as each continent is named. "They were conquered by horsemen" is horsemen riding. A label saying "CONQUEST" is never the picture.
- **One clause, one picture.** A long sentence with three ideas becomes three cards, each one a different picture of 2–4 s (a montage). A sentence that stays with one idea stays in one place for 6–10 s; the camera reframes inside it.
- **Acted, not shown.** Somebody must DO something on the key word: look up, slam, turn, raise binoculars, fall back, write. Their pose or expression changes exactly on that word (`react_on`, `hit_on`, `look_up_on`…).
- **People in places.** Find the anecdote: the one person in the one room on the one day (the Kaiser at Spa, Onoda in the jungle, Wang Yirong in his study). Big history is told through that person; come back to them.
- **Text is rare.**
  - **Allowed:**
    - the place/time `tag` on every new place;
    - name cards on first appearance;
    - the film's 2–4 **big questions** as a `caption` over an acted scene;
    - one `stat` every ~2 minutes when a number must be read;
    - one `paper_note` for an exact quote or order.
  - **Not allowed:** paper, cards or charts standing in for something that happened.

---

## 2. Lookup table: what the narration says → recipe

### A. A story place and its people (the backbone of every chapter)
| the narration says… | recipe | key fields | usually followed by |
|---|---|---|---|
| a date / a new day / we arrive somewhere ("On 29 September 1918…", "In Berlin…") | `establish` | `setting`, `arrive`, `who`, `tag`, `tag_on`, `place_id` | `approach` or `interrupt` |
| people go to something important ("went to see the emperor", "were summoned") | `approach` | `who`, `setting`, `carry`, `name_card` | `interrupt` / `meeting` / `dialogue` |
| X is told something while busy ("they told the Kaiser that…") | `interrupt` | `who`, `speakers`, `business`, `look_up_on`, `react_on` | the consequence, or `contemplate` |
| a demand, a refusal, a blow-up ("needed an armistice, immediately") | `confront` | `a`, `b`, `hit_on`, `gesture` | `contemplate` / the field |
| X alone with it ("could hardly believe it", "knew it was over") | `contemplate` | `who`, `action` (window/sit/stare/walk_away) | a map or the past (flashback) |
| X decides / realises (no visitors) | `decision` | `who`, `react`, `react_on`, `then` | the order carried out in the field |
| news arrives on paper ("a telegram reached…") | `report` | `who`, `react_on` | what the news was about |
| two people argue / persuade | `dialogue` | `a`, `b`, `b_on` | the result |
| a council / cabinet / staff meeting | `meeting` | `people`, `speaker`, `slam_on` | the plan carried out |
| X arrives to take over / is dismissed and leaves | `arrival` | `who`, `direction` | his first decision |
| someone's exact words matter ("he said…") | `quote` (bubble) or any acted card + `paper_note` | `text` / `lines` | back to the story |
| a speech to the nation / parliament / troops | `speech` | `who`, `audience`, `cheer_on` | crowds / enlistment |
| the debate among historians ("some say…, others…", "you'll get a list") | `lecture` | `items` | each candidate shown as its own scene |

### B. Soldiers and the front
| the narration says… | recipe | key fields |
|---|---|---|
| the front is about to break / the enemy is coming / "could not hold for two hours" | `watch_front` | `threat`, `business` (watch/binoculars/aim), `react_on` |
| what someone sees far away (after binoculars) | `binocular_view` | `setting`, `movers` |
| men within sight of a goal / looking back at a lost one / marching past at dusk | `vista` | `action` (look/binoculars/turn_back/march_past), `goal` |
| an attack on foot into fire | `assault` | `falls`, `hit_on`, `climb` |
| a charge / breakthrough / counter-attack | `wave` | `direction`, `enemy` |
| holding on under shelling | `under_fire` | `setting` |
| guns firing / a barrage | `gun_crew` | `fire_on` |
| machine guns mowing down an attack | `mg_nest` | `direction` |
| one man's death stands for many | `hit` | `hit_on` |
| the wounded carried back | `stretcher` | — |
| the field after the battle | `aftermath` | — |
| surrender / prisoners | `surrender` | `captors` |
| retreat / collapse / fleeing | `retreat` | `direction` |
| tanks breaking in | `tank_attack` | `enemy` |
| marching, reinforcements | `march` | `direction`, `vehicles` |
| columns of vehicles | `convoy` | `vehicle` |
| waiting, stalemate, trench routine | `trench_wait` | `business` |
| troops by train | `rail` | — |
| a river crossed under fire | `river_crossing` | — |
| paratroops | `para_drop` | — |

### C. Sea, air, home front
| the narration says… | recipe |
|---|---|
| fleets fight | `naval_battle` |
| a ship is sunk | `sinking` |
| submarines | `submarine_attack` |
| dogfights | `air_battle` |
| bombing a city | `bombing` |
| pilots scrambling | `airfield` |
| hunger, a death telegram, queues, letters | `home_front` (`beat`) |
| war production | `factory` |
| crowds celebrate, protest, enlist, mourn | `crowd` (`mood`) |
| loss, the dead, "a generation" | `absence` (`object`) or `silhouette` |
| remembrance at the end | `memorial` |

### D. Bridges (short, rare)
| the narration says… | recipe | limit |
|---|---|---|
| where a move went | `map_move` | ≤ 5 s, then back to the people in that place |
| the front line formed / moved | `map_front` | ≤ 5 s |
| a long journey | `map_route` | ≤ 6 s |
| where a place is / who joined | `map_locate` | ≤ 4 s |
| the exact words of an order / treaty clause | `document` | ≤ 4 s (prefer an acted card + `paper_note`) |
| numbers COMPARED (two sides' losses) | `chart` | ≤ 6 s; a single number goes on an acted scene as `stat` or is just spoken |
| the narrator addresses the viewer | `host` | chapter edges only |

---

## 3. Patterns that make it a film (copy them)

1. **Arrive → approach → interrupt → react → alone.** A crisis meeting in five cards:
   - `establish` (the building at dawn, the car arrives, tag slides in on the date);
   - `approach` (the corridor, name cards);
   - `interrupt` (the man at his desk stops writing when they speak);
   - `confront` (the demand lands with a fist);
   - `contemplate` (he walks to the window).

   Examples: `projects/example-ww1-cold-open/cards/ch01.json` cards 1–6.
2. **Command → field.** A decision (≤ 4 s) is followed by the men who carry it out.
3. **The threat, felt.** Do not say "the front collapsed" with an arrow. Show `watch_front`: an officer checks his watch while tanks roll out of the mist, and his face breaks on the key words.
4. **Look → see.** `vista` (action binoculars) → `binocular_view` of what he sees.
5. **Same place, time passing.** Re-use a `place_id` with a new `time`/`weather`. Example: the ridge at dusk (look at Paris) → the same ridge, the men turn back (`turn_back`) → the same men retreating in the rain.
6. **The question over the story.** The film's opening question runs as a `caption` over an acted scene (the men turning back), never over a blank card.
7. **The debate as a scene.** "Ask around and you'll get a list" → `lecture`: a historian chalks the years on a board. Then each candidate is its own story place.
8. **Loss by absence.** After the fighting, show what is left: `absence` (helmet on a rifle at dusk, an empty chair), `silhouette`, `aftermath`. No gore.
9. **Both sides.** The channel's promise is "two sides". When the narration allows, cut from one side's room to the other's (Berlin → London), or show the same moment from the other side of the wire.
10. **Map as a bridge.** At most 5 s; it dissolves into the people in that place.

---

## 4. Screen-time targets (checked by the compiler)

| class | target | what counts |
|---|---|---|
| **acted** (action + talk recipes) | **≥ 75 %** of every chapter | people doing what the clause says, in a place |
| maps | ≤ 10 % (each ≤ 5 s) | `map_*` |
| documents / charts / devices | ≤ 10 % | `document`, `chart`, `newspaper`, `device`, `photo_evidence`… |
| host | ≤ 8 %, at chapter edges | `host` |
| stat cards | ≤ 1 every ~2 min | `stat` field |

There is **no background music**, ever: ambience and sound effects only (added automatically from the cards).

---

## 5. Variety (also checked)

- Never the same recipe twice in a row, unless it is a deliberate revisit of the same place (`place_id`, e.g. `vista` look → `vista` turn_back).
- Vary the shot sizes across a sequence: wide (establish) → full (approach) → medium/close (interrupt, confront).
- Vary the light across a chapter: dawn, day, dusk, night, rain.
- Introduce each important person **once** with a name card, then let us recognise them. Keep their look (cast) the same all film.

---

## 6. If nothing fits

1. Re-read the clause and answer the five questions again: who, does what, where, when.
2. Choose the closest acted recipe, then adapt it with its fields: `setting`, `side`, `time`, `weather`, `business`, `action`.
3. Write a `scene` card ([scene-writing.md](scene-writing.md)). It stages any place, people, acts, things and camera; [visual-ideas.md](visual-ideas.md) has a device for most situations.
4. If a thing, a piece of equipment or a vehicle does not exist, draw it in `cards/_film.json` `"drawings"` (scene-writing §5.2), or name it in the card's `wish` and use the closest thing.
5. Only if even that cannot show it may a strong model use `raw` ([08-advanced.md](08-advanced.md)), or add a recipe (§B there).
6. **Never** replace an event with a label, a stat or a chart.
