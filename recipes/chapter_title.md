# `chapter_title` (device)

**Use it when:** A chapter opens with its title card (only if the film uses title cards; usually the date badge on the first scene is enough).

**Do NOT use it when:** —

**Camera (what the compiler does, per variant):** A: title card.

## Fields

| field | required | value | default | meaning |
|---|---|---|---|---|
| `title` | **yes** | text |  | chapter title |
| `subtitle` | no | text | `""` | date or place |

Plus the common fields (`at`, `recipe`, `says`, `variant`, `date`, `place`, `name_card`, `label`, `counter`, `stamp`, `time`, `weather`, `tint`, …) — see [CATALOG.md](CATALOG.md#fields-every-card-can-have).

Variants: A (leave `variant` out: the compiler rotates them so the film never repeats a composition).

## Example card

```json
{
 "at": "Chapter three",
 "recipe": "chapter_title",
 "says": "A new chapter about Verdun begins here.",
 "title": "BLEEDING",
 "subtitle": "1916"
}
```

## Previews (middle frame of the example, each variant)

Variant A: ![](img/chapter_title_A.jpg)
