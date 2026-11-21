# `establish` (action)

**Use it when:** The story arrives at a new place or a new day: 'On the 29th of September 1918…', 'In Berlin…', 'That morning at headquarters…'. The FIRST card of every new place. Put the place/time `tag` on it.

**Do NOT use it when:** We are already in this place (go straight to the people: approach / interrupt / decision).

**Camera (what the compiler does, per variant):** A: wide of the place with a slow push; the arrival happens in it; dissolve to a full shot following the arrivals. B: the arrivals walk from the foreground toward the building (depth), wide only.

## Fields

| field | required | value | default | meaning |
|---|---|---|---|---|
| `setting` | no | one of `hotel`, `street`, `city`, `ruins`, `railway`, `station`, `harbor`, `dock`, `countryside`, `field`, `snow`, `desert`, `airfield`, `garden`, `polder`, `heath`, `steppe`, `nomansland`, `jungle` | `"street"` | the outside of the place |
| `arrive` | no | one of `car`, `walk`, `none`, `train`, `ship` | `"car"` | how people arrive (none = life goes on: passers-by) |
| `who` | no | list |  | 0-3 cast ids who arrive (they get out of the car / walk in) |
| `guard` | no | true / false | `true` | a sentry at the door who presents arms when they arrive |
| `side` | no | side name |  | side of the sentry / vehicles / passers-by |

Plus the common fields (`at`, `recipe`, `says`, `variant`, `date`, `place`, `name_card`, `label`, `counter`, `stamp`, `time`, `weather`, `tint`, …) — see [CATALOG.md](CATALOG.md#fields-every-card-can-have).

Variants: A, B (leave `variant` out: the compiler rotates them so the film never repeats a composition).

## Example card

```json
{
 "at": "On the 29th of September",
 "recipe": "establish",
 "says": "Germany's two top generals arrive at headquarters at dawn to see the Kaiser.",
 "setting": "hotel",
 "arrive": "car",
 "who": [
  "hindenburg",
  "ludendorff"
 ],
 "side": "german",
 "time": "dawn",
 "place_id": "spa_hq",
 "tag": "Spa, Belgium · 29 September 1918",
 "tag_on": "1918"
}
```

## Previews (middle frame of the example, each variant)

Variant A: ![](img/establish_A.jpg)
Variant B: ![](img/establish_B.jpg)
