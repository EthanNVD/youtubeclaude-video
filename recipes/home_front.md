# `home_front` (action)

**Use it when:** Civilians at home: hunger, rationing, waiting for news, a death telegram: 'the Turnip Winter…', 'families went hungry…', 'the telegram every mother feared'.

**Do NOT use it when:** —

**Camera (what the compiler does, per variant):** hunger: a mother puts a turnip on the plate, the child's face falls. telegram: a woman opens the door to a messenger, reads, covers her face. queue: a line of women in the street waiting for bread. letter: a soldier's family reads a letter by candlelight.

## Fields

| field | required | value | default | meaning |
|---|---|---|---|---|
| `beat` | no | one of `hunger`, `telegram`, `queue`, `letter` | `"hunger"` | which home-front moment |
| `side` | no | side name |  | whose home (flag/uniform in the photo) |

Plus the common fields (`at`, `recipe`, `says`, `variant`, `date`, `place`, `name_card`, `label`, `counter`, `stamp`, `time`, `weather`, `tint`, …) — see [CATALOG.md](CATALOG.md#fields-every-card-can-have).

Variants: A, B (leave `variant` out: the compiler rotates them so the film never repeats a composition).

## Example card

```json
{
 "at": "That winter, Germans ate turnips",
 "recipe": "home_front",
 "says": "The blockade left German families with almost nothing but turnips.",
 "beat": "hunger",
 "side": "german"
}
```

## Previews (middle frame of the example, each variant)

Variant A: ![](img/home_front_A.jpg)
Variant B: ![](img/home_front_B.jpg)
