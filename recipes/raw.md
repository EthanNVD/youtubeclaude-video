# `raw` (action)

**Use it when:** ONLY when no recipe can show the moment and you know the engine schema (playbook/08-advanced.md). Strong models only.

**Do NOT use it when:** Any recipe fits — recipes are tested; raw scenes are not.

**Camera (what the compiler does, per variant):** Whatever the scene says.

## Fields

| field | required | value | default | meaning |
|---|---|---|---|---|
| `scene` | **yes** | object |  | an engine scene without start/end/id: {"type": "stage", "set": {...}, "elements": [...], "shots": [...], "world": {...}} (references/plan-schema.md) |
| `class` | no | one of `action`, `talk`, `map`, `device`, `host` | `"action"` | what it counts as in the screen-time mix |

Plus the common fields (`at`, `recipe`, `says`, `variant`, `date`, `place`, `name_card`, `label`, `counter`, `stamp`, `time`, `weather`, `tint`, …) — see [CATALOG.md](CATALOG.md#fields-every-card-can-have).

Variants: A (leave `variant` out: the compiler rotates them so the film never repeats a composition).

## Example card

```json
{
 "at": "and so the story",
 "recipe": "raw",
 "says": "A custom scene built by hand for a moment no recipe covers.",
 "scene": {
  "type": "stage",
  "set": {
   "kind": "harbor",
   "time": "dusk"
  },
  "elements": [
   {
    "kind": "vehicle",
    "type": "cargo",
    "nation": "UK",
    "x": 900,
    "y": 640,
    "scale": 0.5
   }
  ],
  "shots": [
   {
    "t": 0,
    "zoom": 1.0,
    "push": 0.04
   }
  ]
 }
}
```

## Previews (middle frame of the example, each variant)

Variant A: ![](img/raw_A.jpg)
