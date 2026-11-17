# `sinking` (action)

**Use it when:** A ship is sunk: 'the Lusitania went down…', 'three battlecruisers blew up…', 'the ship sank in minutes'.

**Do NOT use it when:** —

**Camera (what the compiler does, per variant):** A: the ship is hit (flash, fire), lists and slides under, smoke; splashes of men in the water; slow push. Symbolic: debris stays.

## Fields

| field | required | value | default | meaning |
|---|---|---|---|---|
| `side` | no | side name |  | whose ship sinks |
| `ship` | no | one of `battleship`, `cruiser`, `destroyer`, `cargo`, `freighter`, `carrier` |  | ship type (default: the side's capital ship) |
| `hit_on` | no | words copied from this card's narration |  | word(s) where it is hit |
| `time` | no | one of `day`, `dusk`, `night` | `"day"` | time |

Plus the common fields (`at`, `recipe`, `says`, `variant`, `date`, `place`, `name_card`, `label`, `counter`, `stamp`, `time`, `weather`, `tint`, …) — see [CATALOG.md](CATALOG.md#fields-every-card-can-have).

Variants: A (leave `variant` out: the compiler rotates them so the film never repeats a composition).

## Example card

```json
{
 "at": "The Lusitania sank in eighteen minutes",
 "recipe": "sinking",
 "says": "A German submarine sank a liner full of civilians.",
 "side": "british",
 "ship": "cargo"
}
```

## Previews (middle frame of the example, each variant)

Variant A: ![](img/sinking_A.jpg)
