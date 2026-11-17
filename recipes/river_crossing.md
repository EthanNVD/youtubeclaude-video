# `river_crossing` (action)

**Use it when:** An assault across water: 'they crossed the river under fire…', 'boats paddled across…'.

**Do NOT use it when:** —

**Camera (what the compiler does, per variant):** A: wide of the boats crossing with splashes and tracer from the far bank → closer on the lead boat.

## Fields

| field | required | value | default | meaning |
|---|---|---|---|---|
| `side` | no | side name |  | who crosses |
| `boats` | no | whole number | `3` | 2-4 boats |

Plus the common fields (`at`, `recipe`, `says`, `variant`, `date`, `place`, `name_card`, `label`, `counter`, `stamp`, `time`, `weather`, `tint`, …) — see [CATALOG.md](CATALOG.md#fields-every-card-can-have).

Variants: A (leave `variant` out: the compiler rotates them so the film never repeats a composition).

## Example card

```json
{
 "at": "the paratroopers crossed the Waal",
 "recipe": "river_crossing",
 "says": "American paratroopers rowed across the river under heavy fire.",
 "side": "american"
}
```

## Previews (middle frame of the example, each variant)

Variant A: ![](img/river_crossing_A.jpg)
