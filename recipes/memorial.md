# `memorial` (device)

**Use it when:** A quiet, serious hold: the dead remembered, the verdict's human cost, the end of a war. 6-12 s, no hurry.

**Do NOT use it when:** —

**Camera (what the compiler does, per variant):** A: grey/dark, slow push on the image.

## Fields

| field | required | value | default | meaning |
|---|---|---|---|---|
| `what` | no | one of `crosses`, `candle`, `helmet` | `"crosses"` | the image |

Plus the common fields (`at`, `recipe`, `says`, `variant`, `date`, `place`, `name_card`, `label`, `counter`, `stamp`, `time`, `weather`, `tint`, …) — see [CATALOG.md](CATALOG.md#fields-every-card-can-have).

Variants: A (leave `variant` out: the compiler rotates them so the film never repeats a composition).

## Example card

```json
{
 "at": "In memory of",
 "recipe": "memorial",
 "says": "The film pauses for the millions who died.",
 "what": "candle"
}
```

## Previews (middle frame of the example, each variant)

Variant A: ![](img/memorial_A.jpg)
