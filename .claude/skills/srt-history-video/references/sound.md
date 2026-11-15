# Sound (no music)

Layers: **voice** (user's file, the clock) · **ambience bed** per place · **SFX** on visible events. Mixed by `tools/mix_audio.py` to −14 LUFS, beds ducked ~5 dB under speech, stems exported for manual fixes.

## Ambience
Default from the set (`sea`→`amb_sea`, `office`→`amb_office`, `codebreak/bunker`→`amb_basement`, `snow`→`amb_wind_cold`, `trench`→`amb_battle`, `factory`, `rally`→`amb_crowd`, `sky`→`amb_engine`…). Maps, devices, studio backdrops: silent by default.
Override with `scene.ambience` (`null` = silence), loudness with `ambienceGain` (dB). Beds follow absolute time, so cutting between shots of the same place does not restart the loop.

## SFX placed automatically (don't duplicate them)
stamp → `stamp` · burst / fx explosion → `explosion`(`_big` if size ≥ 0.8) · document → `typewriter` (telegram/order), `chalk` (blackboard), `pen` (letter/note) for its typing time · map arrow → `map_draw` · headline → `whoosh_soft` · counter end → `pop` · moving planes → `plane_flyby` · transition `flash` → `impact`.

## Add explicit cues (`scene.sfx`) for other contacts
`paper` (sheet picked up/put down), `phone_ring`, `radio_static`, `morse`, `footsteps`/`footsteps_snow`, `gunshot`/`rifle`/`machinegun`/`cannon`/`artillery` (only when muzzles flash on screen), `boom_distant`, `plane_dive`, `plane_engine`, `tank_engine`, `truck`, `train`, `splash`, `ship_horn`, `metal_clank`, `thud`, `bell`/`church_bell`, `cheer`, `heartbeat`, `riser` (build-up before a reveal), `impact`, `whoosh`/`whoosh_fast`, `pop`, `tick`, `clock_tick`, `cash`.
`{t, id, vol (dB, e.g. -6), dur (s, trims/loops sustained sounds)}`.

## Taste
- Sound follows the picture: the hit is on the contact frame, not on the SRT cue start.
- Don't put a whoosh on every cut or gunfire under every war sentence.
- Grief/verdict: drop the bed (`ambience: null`) or keep only wind; no SFX except one bell/candle crackle at most.
- Montage: one short sound per item max; let the voice lead.
- Real recordings beat synthesis: put licensed/CC0 files in `assets/sfx/<id>.wav` (same id) and they replace the generated ones.
