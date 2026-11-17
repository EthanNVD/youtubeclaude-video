# `dialogue` (talk)

**Use it when:** Two people argue, persuade or exchange views: 'X told Y…', 'Y refused…', 'they disagreed…'.

**Do NOT use it when:** One person alone decides (decision); a crowd listens (speech).

**Camera (what the compiler does, per variant):** A: over-the-shoulder on A, then on B when B answers, then a two-shot. B: two-shot walking side by side (garden/corridor) then close-ups. C: A close, B close, two-shot (fast back-and-forth).

## Fields

| field | required | value | default | meaning |
|---|---|---|---|---|
| `a` | **yes** | cast id |  | first speaker (cast id) |
| `b` | **yes** | cast id |  | second speaker (cast id) |
| `b_on` | no | words copied from this card's narration |  | word(s) where B answers (cut to B) |
| `a_mood` | no | one of `worried`, `angry`, `shocked`, `determined`, `sad`, `smug`, `panic`, `happy`, `nervous`, `tired` | `"determined"` | A's expression |
| `b_mood` | no | one of `worried`, `angry`, `shocked`, `determined`, `sad`, `smug`, `panic`, `happy`, `nervous`, `tired` | `"worried"` | B's expression |
| `setting` | no | one of `office`, `warroom`, `tent`, `bunker`, `cabinet`, `study`, `conference`, `radio`, `codebreak`, `hotel`, `train_interior`, `bridge`, `garden`, `corridor`, `railway`, `street`, `deck` | `"office"` | where |

Plus the common fields (`at`, `recipe`, `says`, `variant`, `date`, `place`, `name_card`, `label`, `counter`, `stamp`, `time`, `weather`, `tint`, …) — see [CATALOG.md](CATALOG.md#fields-every-card-can-have).

Variants: A, B, C (leave `variant` out: the compiler rotates them so the film never repeats a composition).

## Example card

```json
{
 "at": "Ludendorff told the Kaiser",
 "recipe": "dialogue",
 "says": "Ludendorff admitted to the Kaiser that the army could not hold.",
 "a": "ludendorff",
 "b": "kaiser_wilhelm",
 "b_on": "The Kaiser",
 "a_mood": "worried",
 "b_mood": "shocked"
}
```

## Previews (middle frame of the example, each variant)

Variant A: ![](img/dialogue_A.jpg)
Variant B: ![](img/dialogue_B.jpg)
Variant C: ![](img/dialogue_C.jpg)
