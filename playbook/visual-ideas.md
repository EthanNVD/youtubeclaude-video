# Visual ideas — a bank of picture devices

When a clause does not give you a picture at once, find its situation below and take a device. Each device:
- is one sentence of what the viewer sees;
- comes with how to stage it with a `scene` card ([scene-writing.md](scene-writing.md)).

They come from the reference films (`.claude/skills/srt-history-video/references/storytelling-film.md`) and from ordinary film grammar.

**Rules for using the bank:**
- Use a device **at most twice per film**, unless it is your film's motif. A motif is one object or place that comes back on purpose (the turnip, the half-read declaration, the hourglass).
- Change at least two of these from the card before: place, people, act, camera.
- The device must show **this** clause, not the topic in general.

---

## 1. The narration gives a number

| device | what we see | stage it |
|---|---|---|
| **Half empty** | a place we saw full is now half empty | same `place_id`, fewer `items`, `revisit: true`, `close_then_wide` |
| **The ledger** | a clerk runs his finger down a ledger and stops, appalled | `read` with `ledger`, `shake_head` on the number |
| **The queue** | the length of a queue is the size of the problem | `crowd: queue`, `camera: pan` |
| **Counting coins** | a hand counts too few coins | `count` with `coins` on a `counter`, `two_shot` |
| **One of many** | one person stands for the thousands | a single figure, `close`, then `wide` with a crowd |
| **Rations on a plate** | the day's food laid out on a table | `things` on a `table`, `detail_then_wide` |
| **The calendar** | time passing in days | `calendar` item, `clock:HH:MM`, the same room at dawn → night |
| **The stat** | one number that must be read | the `stat` field over an acted scene (≤ 1 per ~2 min) |

## 2. The narration names a list

| device | what we see | stage it |
|---|---|---|
| **Things land as they are named** | each item appears on its word | `things` with `appear` on each name; a `pan` or a custom zoom-out |
| **Faces as they are named** | each person steps in or turns on their name | `enter` or `look_up` on each name; `group` camera |
| **Signs as they are named** | each country/town is a sign, a flag, a poster | town items with `text`, or flags on a wall |
| **The montage** | 2–3 short cards, one picture per item (2–3 s each) | three `scene` cards, each a different place |

## 3. Someone decides, orders, is told

| device | what we see | stage it |
|---|---|---|
| **Interrupted at work** | a man writing stops and looks up on the news | `write` then `look_up`, `wide_then_close` (template A) |
| **The hand-over** | a folder, a telegram passes from hand to hand | `give` (`to`, `with`); the giver walks up by himself |
| **The fist on the table** | the decision lands with a slam | `slam` on the word, `medium` |
| **The finger on the map** | a commander taps a place on a wall map or a table | `point` / `point_down`, `admiralty` / `office` room |
| **Alone afterwards** | he walks to the window and turns his back | `walk_to` the window slot, `turn_away`, `push_in` |
| **Command → field** | the next card shows the men carrying it out | the next card: a battle recipe or a street with soldiers |
| **The empty chair** | the decision-maker's chair after he has gone | a `chair`, nobody, `detail_then_wide` |

## 4. Scarcity, hunger, cold

| device | what we see | stage it |
|---|---|---|
| **The bare shelf** | a shop shelf with nothing on it | `shelf:empty`, shop `goods: empty` (the "sold out" card) |
| **The pot** | a mother stirs a thin soup / drops in a turnip | `stir`, `pot` on `stove`, candle light |
| **Children at an empty table** | small faces behind empty plates | children with `size`, seated, `plate`s on a `table` |
| **The queue in snow** | people waiting, shivering, at dawn | `crowd: queue`, mood `cold`, `weather: snow`, `time: dawn` |
| **The cold stove** | a stove without fire, breath in the air | `stove:cold`, `cold: true`, `shiver` |
| **The rotten field** | a farmer kneels by a spoiled crop | `mud` set, `potatoes` dark, `despair` |
| **Shuffling** | thin people walk slowly | `walk: shuffle`, mood `hungry` |

## 5. Loss, death, absence

| device | what we see | stage it |
|---|---|---|
| **What is left** | a helmet on an empty chair, a coat on a hook | template G; `hooks`, `helmet` on `chair` |
| **The telegram** | a mother opens a letter and her hand goes to her mouth | `read` with `telegram`, then `gasp` |
| **Prayer** | someone kneels in a church by candlelight | `church` room, `kneel`, `pray`, light `candle` |
| **The long table** | one place laid, nobody there | `table` with one `plate`, `detail_then_wide` |
| **Silence and grey** | the same place, grey tint, no movement | `tint: grey`, `life: false`, `push_in` |

## 6. Two sides, contrast, irony

| device | what we see | stage it |
|---|---|---|
| **Mirror cut** | the same act in each capital, mirrored | two cards: same act, mirrored `at`/`face`, different place |
| **Waiting for nothing** | men wait for an enemy who never comes | binoculars, then `scratch_head` (the Wilhelmshaven card) |
| **Comfort and want** | a full table here, an empty one there | two rooms, same camera, `revisit` on the second |
| **The smile at the wrong time** | an official smiles at a document we know is a lie | `show` + mood `smug`, `medium` |
| **The poster vs the street** | a bright poster above a grim queue | town `poster` with `text` + `crowd: queue` |

## 7. News, rumour, public reaction

| device | what we see | stage it |
|---|---|---|
| **The newsboy** | a boy holds up a paper and shouts | `hold_up` a newspaper drawing, `shout` |
| **Reading aloud in a pub** | one man reads, the others listen and react | `tavern`, `read` + `say`, listeners `shake_head` |
| **Flashbulbs** | a man faces cameras and denies everything | press room, `listeners` with `view: back`, `flash` effects, `palms` |
| **The notice board** | people crowd round a posted order | the `notice_board` drawing, `crowd: watchers`, `react_on` |
| **The whisper** | two people lean together and look around | `look_around`, `two_shot` |

## 8. Movement, journeys, logistics

| device | what we see | stage it |
|---|---|---|
| **The quay** | goods carried ashore past a foreman | `harbor`, people `walk_to` with `holds: sack`, `vehicles` |
| **The patrol line** | grey ships one behind the other | `sea`, three `cruiser`s moving, `dusk`, `rain` |
| **The cart through town** | a loaded cart crosses a street | a `cart` thing (`n: 1`) with `to`, or a moving drawing |
| **The departure** | someone walks out of the frame and does not come back | `exit` |
| **The arrival** | someone enters and the room turns to him | `enter`, the others `look_at` him |
| **The map bridge** | where it all is, 3–5 s | a `map_*` recipe between two scenes |

## 9. Memory, history, the present looking back

| device | what we see | stage it |
|---|---|---|
| **The document as motif** | the same paper returns changed (half read → read) | your own drawings (`declaration_half` → `declaration_full`) |
| **The classroom** | a teacher at a blackboard frames the question | `classroom`, `blackboard` with `text`, pupils at `school_desk`s |
| **The researcher** | someone in an archive finds (or does not find) the evidence | `office` with `drawers`, `read` a `book`, `shake_head` |
| **Then and now** | the same place in two eras | two `sets` with the same layout, different `light`/`grade`/props |
| **The speech that changes it** | a leader at a lectern, the hall silent | template E, `paper_note` with the exact words |

## 10. The film's big question

- Put the big question as a `caption` over an acted scene: people turning back, a family at a table, a teacher at a board. Never over an empty card.
- Come back to the opening place at the end (`revisit: true`), changed. The answer is in the change.

---

**When nothing fits:** describe the picture you want in one sentence, then build it from parts:
- a place (§3 of scene-writing);
- people with acts;
- things.

If a piece does not exist:
- **draw it** (scene-writing §5.2);
- or put it in `wish` and use the closest thing.

The `work/missing_assets.json` log of every film becomes the next engine upgrade.
