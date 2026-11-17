# `speech` (talk)

**Use it when:** A leader addresses a crowd, parliament or troops: 'he told the nation…', 'he declared war…', 'in a speech…'.

**Do NOT use it when:** A private conversation (dialogue).

**Camera (what the compiler does, per variant):** A: speaker at the podium (low angle medium) → audience wide → speaker close. B: audience first (backs of heads), then the speaker.

## Fields

| field | required | value | default | meaning |
|---|---|---|---|---|
| `who` | **yes** | cast id |  | the speaker |
| `audience` | no | one of `crowd`, `parliament`, `troops`, `radio` | `"crowd"` | who listens |
| `side` | no | side name |  | side of the audience/flag |
| `cheer_on` | no | words copied from this card's narration |  | word(s) where the audience cheers or reacts |
| `mood` | no | one of `worried`, `angry`, `shocked`, `determined`, `sad`, `smug`, `panic`, `happy`, `nervous`, `tired` | `"determined"` | speaker's expression |
| `audience_mood` | no | one of `worried`, `angry`, `shocked`, `determined`, `sad`, `smug`, `panic`, `happy`, `nervous`, `tired`, `cheer` | `"happy"` | audience reaction |

Plus the common fields (`at`, `recipe`, `says`, `variant`, `date`, `place`, `name_card`, `label`, `counter`, `stamp`, `time`, `weather`, `tint`, …) — see [CATALOG.md](CATALOG.md#fields-every-card-can-have).

Variants: A, B (leave `variant` out: the compiler rotates them so the film never repeats a composition).

## Example card

```json
{
 "at": "On the 2nd of April, Wilson",
 "recipe": "speech",
 "says": "President Wilson asked Congress to declare war on Germany.",
 "who": "wilson",
 "audience": "parliament",
 "side": "american",
 "cheer_on": "declare war"
}
```

## Previews (middle frame of the example, each variant)

Variant A: ![](img/speech_A.jpg)
Variant B: ![](img/speech_B.jpg)
