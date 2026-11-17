# `newspaper` (device)

**Use it when:** Public reaction / news: 'the papers called it…', 'the headlines…', 'the public learned…'. ≤ 4 s.

**Do NOT use it when:** —

**Camera (what the compiler does, per variant):** A: the front page spins in and lands on the desk, push.

## Fields

| field | required | value | default | meaning |
|---|---|---|---|---|
| `headline` | **yes** | text |  | the headline (2-6 words) |
| `accent` | no | text |  | one word of the headline shown in yellow |
| `paper` | no | text | `"THE DAILY"` | newspaper name |

Plus the common fields (`at`, `recipe`, `says`, `variant`, `date`, `place`, `name_card`, `label`, `counter`, `stamp`, `time`, `weather`, `tint`, …) — see [CATALOG.md](CATALOG.md#fields-every-card-can-have).

Variants: A (leave `variant` out: the compiler rotates them so the film never repeats a composition).

## Example card

```json
{
 "at": "The newspapers called it",
 "recipe": "newspaper",
 "says": "British papers celebrated the tank as a war-winner.",
 "headline": "TANKS SMASH THROUGH",
 "accent": "TANKS"
}
```

## Previews (middle frame of the example, each variant)

Variant A: ![](img/newspaper_A.jpg)
