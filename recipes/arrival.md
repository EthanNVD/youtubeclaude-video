# `arrival` (action)

**Use it when:** Someone arrives or leaves: 'he arrived at…', 'he took command…', 'he was dismissed and left…', 'he went home'.

**Do NOT use it when:** A crowd or an army moves (march / convoy).

**Camera (what the compiler does, per variant):** A: one depth shot, he grows toward the lens (or shrinks away). B: wide of the place then a close tracking shot of his face.

## Fields

| field | required | value | default | meaning |
|---|---|---|---|---|
| `who` | **yes** | cast id |  | who walks |
| `direction` | no | one of `toward`, `away` | `"toward"` | toward the camera (arrives) or away (leaves) |
| `setting` | no | one of `corridor`, `railway`, `station`, `street`, `hotel`, `garden`, `airfield`, `dock`, `snow`, `field` | `"corridor"` | where |
| `holds` | no | one of `folder`, `suitcase`, `none`, `telegram` | `"folder"` | what he carries |
| `mood` | no | one of `worried`, `angry`, `shocked`, `determined`, `sad`, `smug`, `panic`, `happy`, `nervous`, `tired` | `"determined"` | expression |

Plus the common fields (`at`, `recipe`, `says`, `variant`, `date`, `place`, `name_card`, `label`, `counter`, `stamp`, `time`, `weather`, `tint`, …) — see [CATALOG.md](CATALOG.md#fields-every-card-can-have).

Variants: A, B (leave `variant` out: the compiler rotates them so the film never repeats a composition).

## Example card

```json
{
 "at": "By the end of August, Falkenhayn was gone",
 "recipe": "arrival",
 "says": "Falkenhayn was dismissed and left headquarters.",
 "who": "falkenhayn",
 "direction": "away",
 "setting": "corridor",
 "holds": "suitcase",
 "mood": "sad"
}
```

## Previews (middle frame of the example, each variant)

Variant A: ![](img/arrival_A.jpg)
Variant B: ![](img/arrival_B.jpg)
