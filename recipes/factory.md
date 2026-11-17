# `factory` (action)

**Use it when:** War production: 'factories turned out shells…', 'women took the men's jobs…', 'production doubled'.

**Do NOT use it when:** —

**Camera (what the compiler does, per variant):** A: workers carry and stack shells along the line (wide) → close on a tired worker.

## Fields

| field | required | value | default | meaning |
|---|---|---|---|---|
| `product` | no | one of `shells`, `tanks`, `planes` | `"shells"` | what is made |
| `side` | no | side name |  | whose factory |

Plus the common fields (`at`, `recipe`, `says`, `variant`, `date`, `place`, `name_card`, `label`, `counter`, `stamp`, `time`, `weather`, `tint`, …) — see [CATALOG.md](CATALOG.md#fields-every-card-can-have).

Variants: A (leave `variant` out: the compiler rotates them so the film never repeats a composition).

## Example card

```json
{
 "at": "factories worked day and night",
 "recipe": "factory",
 "says": "Britain's factories produced shells around the clock.",
 "product": "shells",
 "side": "british"
}
```

## Previews (middle frame of the example, each variant)

Variant A: ![](img/factory_A.jpg)
