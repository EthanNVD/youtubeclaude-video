# `report` (talk)

**Use it when:** News reaches someone: 'a telegram arrived', 'he was told…', 'word reached Berlin…', 'the report said…'.

**Do NOT use it when:** Nobody receives anything (use decision); the content of the paper matters more than the reaction (use document, ≤ 4 s).

**Camera (what the compiler does, per variant):** A: messenger walks in from the left, hands it over (full shot) → medium on the reader → close before the reaction. B: the reader at his desk in close-up first; the messenger's hand enters; cut wide to both; close on the reaction.

## Fields

| field | required | value | default | meaning |
|---|---|---|---|---|
| `who` | **yes** | cast id |  | cast id of the person who receives the news |
| `messenger` | no | cast id |  | who brings it (default: an officer of the receiver's side) |
| `side` | no | side name |  | side of the messenger if not given |
| `item` | no | one of `telegram`, `paper`, `folder`, `photo` | `"telegram"` | what is handed over |
| `react` | no | one of `worried`, `angry`, `shocked`, `determined`, `sad`, `smug`, `panic`, `happy`, `nervous`, `tired` | `"shocked"` | reaction when he reads it |
| `react_on` | no | words copied from this card's narration |  | word(s) where he reacts |
| `setting` | no | one of `office`, `warroom`, `tent`, `bunker`, `cabinet`, `study`, `conference`, `radio`, `codebreak`, `hotel`, `train_interior`, `bridge` | `"office"` | where |

Plus the common fields (`at`, `recipe`, `says`, `variant`, `date`, `place`, `name_card`, `label`, `counter`, `stamp`, `time`, `weather`, `tint`, …) — see [CATALOG.md](CATALOG.md#fields-every-card-can-have).

Variants: A, B (leave `variant` out: the compiler rotates them so the film never repeats a composition).

## Example card

```json
{
 "at": "Word reached Berlin",
 "recipe": "report",
 "says": "The bad news from the front reached the Kaiser.",
 "who": "kaiser_wilhelm",
 "react": "shocked",
 "react_on": "lost"
}
```

## Previews (middle frame of the example, each variant)

Variant A: ![](img/report_A.jpg)
Variant B: ![](img/report_B.jpg)
