# Narration → picture: which recipe for which sentence

Use this page for every card:
1. Find the row that matches what the sentence SAYS.
2. Check the row's "then (next card)" column so the following card shows something new.
3. Open `recipes/<recipe>.md` for the recipe's fields.

## 1. Lookup table

### People decide, learn, speak
| the narration says… | recipe | key fields | then (next card) |
|---|---|---|---|
| X decided / ordered / planned / realised / had a problem | `decision` | `who`, `react`, `react_on`, `then` | the consequence in the field (an action recipe) |
| news reached X / X was told / a telegram arrived | `report` | `who`, `react`, `react_on` | what the news was about, or X's decision |
| X told Y / argued / refused / persuaded | `dialogue` | `a`, `b`, `b_on` | the result |
| the generals / cabinet / council met, agreed | `meeting` | `people`, `speaker`, `slam_on` | the plan carried out |
| X said "…" / wrote "…" (a quote) | `quote` | `who`, `text` (≤ 15 words) | back to the action |
| X told the nation / declared / gave a speech | `speech` | `who`, `audience`, `cheer_on` | crowd, enlistment, or the war itself |
| X phoned / radioed | `phone` | `who`, `react` | — |
| they signed a treaty / armistice / surrender | `signing` | `who`, `witnesses` | the war's result (crowd, memorial) |
| X arrived / took command / was dismissed / left | `arrival` | `who`, `direction` | his first decision, or the one who replaces him |

### Soldiers, battles, machines (ACTION — most of a battle chapter)
| the narration says… | recipe | key fields |
|---|---|---|
| they attacked / went over the top / the offensive began (slow, into fire) | `assault` | `side`, `falls`, `hit_on` |
| they stormed / charged / broke through / counter-attacked (fast) | `wave` | `side`, `direction`, `enemy` |
| the battle went on / they held / under bombardment / endurance | `under_fire` | `side`, `setting` |
| the guns opened fire / barrage / bombardment from the gunners' side | `gun_crew` | `side`, `fire_on` |
| machine guns cut them down / the defenders fired | `mg_nest` | `side`, `direction` |
| one man's death stands for many / "X's army bled too" | `hit` | `side`, `hit_on` |
| the wounded / casualties mounted / a number of casualties | `stretcher` (+ `counter`) | `side` |
| the dead / the day after / the worst day | `aftermath` | `side` |
| they surrendered / were captured / the army collapsed | `surrender` | `side`, `captors` |
| they retreated / fled / the front broke | `retreat` | `side`, `direction` |
| tanks attacked / broke through | `tank_attack` | `side`, `enemy` |
| troops marched / reinforcements went to | `march` | `side`, `direction`, `vehicles` |
| tanks / trucks / columns drove | `convoy` | `side`, `vehicle` |
| stalemate / waiting / months in the trenches | `trench_wait` | `side`, `business` |
| sent by train / divisions moved east | `rail` | `side` |
| crossed a river under fire | `river_crossing` | `side` |
| paratroopers / gliders landed | `para_drop` | `side` |
| fleets fought / battleships exchanged fire | `naval_battle` | `side`, `enemy` |
| a ship was sunk | `sinking` | `side`, `ship` |
| U-boats / submarines sank ships | `submarine_attack` | `side`, `target` |
| fighters / dogfight / air battle | `air_battle` | `side`, `enemy` |
| bombers struck a city | `bombing` | `side` |
| pilots scrambled / took off | `airfield` | `side` |

### Home front and mood
| the narration says… | recipe |
|---|---|
| hunger, rationing, a death telegram, queues, letters home | `home_front` (`beat`) |
| factories, production, women working | `factory` |
| crowds celebrated / protested / enlisted / mourned | `crowd` (`mood`) |
| a huge number of dead over a long time; "a whole generation" | `silhouette` |
| remembrance, the human cost, the end | `memorial` |

### Where, what it said, how many (keep SHORT)
| the narration says… | recipe | max length |
|---|---|---|
| where a move went: "toward Paris", "east", "to the coast" | `map_move` | 5 s in battle chapters, 8 s otherwise |
| the front line formed / moved | `map_front` | 8 s |
| long journeys: convoys, shipping troops | `map_route` | 8 s |
| where a place is; who joined which side | `map_locate` | 5 s |
| the words of an order / telegram / memo matter | `document` | 4 s |
| the papers called it… | `newspaper` | 4 s |
| two or more numbers compared | `chart` | 7 s |
| photos / evidence examined | `photo_evidence` | 5 s |
| the narrator asks the viewer / opens / closes / gives a verdict | `host` | 4–10 s |
| the film's scored device is updated | `device` | 5–8 s |

## 2. Sequences that work (copy these patterns)

- **Command → field.** `decision` (2–4 s) → the action it causes. Example: Falkenhayn decides to "let the guns do the killing" → `gun_crew`.
- **Number on the action.**
  - A single number goes on an action card as `counter`:
    - "57,470 casualties" → `stretcher` with a counter;
    - "19,240 killed" → `mg_nest` with a counter.
  - Use `chart` only when numbers are compared.
- **Both sides.** "The Germans bled too" → show German soldiers in the same situation (`hit`, `stretcher`, `under_fire`), not a label.
- **Cause → cost → symbol.** `assault` → `mg_nest` (counter) → `aftermath` (grey) or `silhouette`, with crosses appearing.
- **Map as a bridge only.** `map_move` for at most 5 s, then straight back to people in the place it showed.
- **Arrive → act.** `arrival` (the new commander comes in) → `decision` → the field.

## 3. More action (when the checker says a chapter has too little)

Turn talk, document, chart and map cards into action:

| you wrote | change it to |
|---|---|
| `decision` that is 8 s long | `decision` 3 s + the action it causes, 5 s |
| `chart` with ONE number | the action card the number describes + `counter` |
| `document` read aloud for 8 s | `document` 3 s + what the document caused |
| `map_move` 10 s | `map_move` 4 s + `march` / `convoy` / `wave` in that place |
| `meeting` while the narration describes a battle | the battle |
| `host` in the middle of a battle chapter | remove it; keep the host for chapter edges |

## 4. Variety rules

The checker enforces these:
- Never the same recipe twice in a row.
- No recipe above about 30 % of a chapter's cards.

Also do these yourself:
- Change the place: trench → open field → town → sea → office → map.
- Change the time of day across a chapter: `dawn` attack, `day` battle, `dusk` grief, `night` guns.
- Alternate the sides when the narration allows. The channel shows **both sides**.
- Keep each side's direction consistent. Use `direction`: if side A always moves right, side B moves left.

## 5. If nothing fits

1. Re-read the sentence. Ask: who or what would a camera see if it were there?
2. Choose the closest action recipe and use its fields (side, setting, time) to make it fit.
3. Only if the moment truly cannot be shown with recipes, a strong model may use `raw` (see [08-advanced.md](08-advanced.md)).
4. Never use a label or a chart as a substitute for something that happened.
