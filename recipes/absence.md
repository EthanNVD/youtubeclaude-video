# `absence` (action)

**Use it when:** Loss, death, the end of someone — shown by what is left behind: 'he died believing he had failed', 'none of them came back', 'a whole generation was gone'. An empty place, one object, quiet light.

**Do NOT use it when:** The narration describes the fighting (show the fighting) or mourning crowds (crowd mood=mourn).

**Camera (what the compiler does, per variant):** A: wide of the empty place, slow push toward the object. B: start close on the object, pull back by dissolve to the empty place.

## Fields

| field | required | value | default | meaning |
|---|---|---|---|---|
| `setting` | no | one of `nomansland`, `office`, `study`, `home`, `kitchen`, `garden`, `trench`, `street`, `ruins`, `field` | `"nomansland"` | the empty place |
| `object` | no | one of `helmet_rifle`, `empty_chair`, `candle`, `cross`, `letter`, `boots` | `"helmet_rifle"` | what is left |

Plus the common fields (`at`, `recipe`, `says`, `variant`, `date`, `place`, `name_card`, `label`, `counter`, `stamp`, `time`, `weather`, `tint`, …) — see [CATALOG.md](CATALOG.md#fields-every-card-can-have).

Variants: A, B (leave `variant` out: the compiler rotates them so the film never repeats a composition).

## Example card

```json
{
 "at": "none of them came back",
 "recipe": "absence",
 "says": "The men who left never returned.",
 "setting": "home",
 "object": "empty_chair",
 "time": "dusk",
 "tint": "grey"
}
```

## Previews (middle frame of the example, each variant)

Variant A: ![](img/absence_A.jpg)
Variant B: ![](img/absence_B.jpg)
