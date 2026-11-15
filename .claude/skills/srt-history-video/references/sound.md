# Sound (no music)

**The user only gives the SRT + the narration file.** Every other sound is built by the skill: you never ask the user for music, ambience or effects.

Layers: **voice** (user's file, the clock) · **ambience bed** per place · **SFX** on visible events. Mixed by `tools/mix_audio.py` to −14 LUFS, beds ducked ~5 dB under speech, stems exported for manual fixes.

## Ambience
The bed comes from the set by default:
- `sea`, `deck`, `bridge` → `amb_sea`
- `office` → `amb_office`
- `codebreak`, `bunker`, `radio`, `cell` → `amb_basement` (radio adds static)
- `snow` → `amb_wind_cold`
- `trench` → `amb_battle`
- `factory`, `hangar` → `amb_factory` (hangar adds metal clanks)
- `rally`, `parliament` → `amb_crowd`
- `sky`, `cockpit`, `train_interior` → `amb_engine` (train adds rails)
- `tent`, `airfield`, `garden` → `amb_wind`
- `corridor` → `amb_room`

Maps, devices and studio backdrops are silent by default.
Override with `scene.ambience` (`null` = silence), loudness with `ambienceGain` (dB). Beds follow absolute time, so cutting between shots of the same place does not restart the loop.

## SFX placed automatically (don't duplicate them)
Visuals:
- stamp → `stamp`
- burst / fx explosion → `explosion` (`_big` if size ≥ 0.8); fx splash → `splash`
- document → `typewriter` (telegram/order), `chalk` (blackboard) or `pen` (letter/note), for its typing time
- map arrow → `map_draw`
- headline → `whoosh_soft`
- counter end → `pop`
- transition `flash` → `impact`

Vehicles:
- moving planes → `plane_flyby`
- moving tanks → `tank_engine`; trucks, jeeps, cars → `truck`; trains → `train`

Acting:
- actor moving (`x`/`at` keys, `walk`/`run`) → `footsteps` (`footsteps_snow` in snow) for the whole move
- pose `typing` → `typewriter`
- pose `write` → `pen`
- pose change to `slam` → `thud`
- pose change while holding paper/telegram/folder/book → `paper`

## Add explicit cues (`scene.sfx`) for other contacts
`paper` (sheet picked up/put down), `phone_ring`, `radio_static`, `morse`, `footsteps`/`footsteps_snow`, `gunshot`/`rifle`/`machinegun`/`cannon`/`artillery` (only when muzzles flash on screen), `boom_distant`, `plane_dive`, `plane_engine`, `tank_engine`, `truck`, `train`, `splash`, `ship_horn`, `metal_clank`, `thud`, `bell`/`church_bell`, `cheer`, `heartbeat`, `riser` (build-up before a reveal), `impact`, `whoosh`/`whoosh_fast`, `pop`, `tick`, `clock_tick`, `cash`.
`{t, id, vol (dB, e.g. -6), dur (s, trims/loops sustained sounds)}`.

## Never miss (check after `make.py … audio`)
The audio step prints `sound_warnings`:
- **silent scenes**: no bed and no cue;
- **sets without a default bed**: a newly added set must get an entry in `SET_AMB` in `tools/mix_audio.py`.

Fix every warning, unless the silence is intended (grief/verdict beat: then set `ambience: null`). Then go through the plan once more for visible contacts the automatic rules cannot know about, and add explicit cues for them:
- a door slams;
- a phone rings;
- a gun fires;
- a ship's horn;
- a bell;
- a crowd cheers;
- a heartbeat before a reveal;
- a `riser` before a big reveal.

## Taste
- Sound follows the picture: the hit is on the contact frame, not on the SRT cue start.
- Don't put a whoosh on every cut or gunfire under every war sentence.
- Grief/verdict: drop the bed (`ambience: null`) or keep only wind; no SFX except one bell/candle crackle at most.
- Montage: one short sound per item max; let the voice lead.
- Real recordings beat synthesis: put licensed/CC0 files in `assets/sfx/<id>.wav` (same id) and they replace the generated ones.
