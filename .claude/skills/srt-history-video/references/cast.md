# Cast

- **The host** (`host`, `host_field`, `host_winter`) is the channel's narrator. Drawn in the style of the reference channel's narrator (pale face with cool grey shading on the lower half, heavy-lidded sardonic eyes with small pupils, thick brows) but a different, younger man: about 30, clean-shaven with freckles, dark-brown hair under an olive eight-panel newsboy cap, camel belted trench coat over a white shirt and navy tie, a pencil tucked behind the right ear; carries a reporter's notebook. Variants: `host_field` (trench + Brodie helmet), `host_winter` (greatcoat + ushanka + navy scarf). Usage: add `"host": {"preset": "host"}` to every plan; restyle him only in `src/char/presets.ts` (every future video follows).
- Body: big round head sitting directly on a small body (the chin overlaps the collar), rubber-hose arms and legs, mitten hands shaped per pose (open, fist, point, grip). Origin = feet, height ≈ 280 px × scale.
- Face options for any cast member: `eyes: "heavy"` (narrator-style heavy-lidded eyes), `shadeFace: true` (pale face, cool lower shading), `skin`, extras `freckles`, `pencil`, `thickbrows`; outfit `trench` (+ `tie`), hat `newsboy`.
- Every recurring person gets one entry in `plan.cast` and keeps it for the whole film (same hat, colours, glasses).
- Prefer a preset; override fields to fit the period (e.g. `{"preset": "stalin", "color": "#9a9670"}` for a white tunic).
- Identity = silhouette: hair/hat shape, moustache, glasses, build, uniform colour. Faces stay simple (dot eyes).
- Leaders: use the presets (caricature, respectful, no hate symbols). Ordinary soldiers/civilians: generic presets, vary `hair`, `facial`, `build`, `age`.
- Uniform colours follow nation keys automatically; check the period (WW1 vs WW2 helmets, 1812 coats).
- New recurring figure for future videos → add to `src/char/presets.ts` (lowercase id, short comment).
- Name card on first appearance: `{ "kind": "namecard", "name": "Adm. Isoroku Yamamoto", "role": "Combined Fleet", "in": 0.6 }` (language of the SRT).
- Check the gallery when designing: `npx remotion still src/index.ts Gallery out.png --props='{"names":["stalin","zhukov"],"poses":["talk"],"exprs":["angry"]}'`.
