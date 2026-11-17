# `phone` (talk)

**Use it when:** An urgent call or radio message: 'he phoned…', 'the order came by radio…', 'the line went dead…'.

**Do NOT use it when:** A written message (report).

**Camera (what the compiler does, per variant):** A: medium → close on the reaction. B: cross-cut caller / receiver (needs other).

## Fields

| field | required | value | default | meaning |
|---|---|---|---|---|
| `who` | **yes** | cast id |  | who is on the phone |
| `other` | no | cast id |  | optional person on the other end (cut between both) |
| `react` | no | one of `worried`, `angry`, `shocked`, `determined`, `sad`, `smug`, `panic`, `happy`, `nervous`, `tired` | `"worried"` | reaction |
| `react_on` | no | words copied from this card's narration |  | word(s) where he reacts |
| `setting` | no | one of `office`, `warroom`, `tent`, `bunker`, `cabinet`, `study`, `conference`, `radio`, `codebreak`, `hotel`, `train_interior`, `bridge` | `"office"` | where |

Plus the common fields (`at`, `recipe`, `says`, `variant`, `date`, `place`, `name_card`, `label`, `counter`, `stamp`, `time`, `weather`, `tint`, …) — see [CATALOG.md](CATALOG.md#fields-every-card-can-have).

Variants: A, B (leave `variant` out: the compiler rotates them so the film never repeats a composition).

## Example card

```json
{
 "at": "He called Paris",
 "recipe": "phone",
 "says": "The general phoned Paris to ask for every reserve.",
 "who": "joffre",
 "react": "determined"
}
```

## Previews (middle frame of the example, each variant)

Variant A: ![](img/phone_A.jpg)
Variant B: ![](img/phone_B.jpg)
