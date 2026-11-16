# Plan schema (what the engine understands)

Coordinates: stage scenes use a **1920×1080 frame at camera zoom 1**, origin top-left; sets are drawn on a larger
canvas (x −240…2160, y −160…1240) so the camera can move. Default ground line (feet) ≈ **y 900**.
Times inside a scene (`in`, `out`, `keys[].t`, `camera[].t`, `sfx[].t`) are **seconds from the scene start**.
Scene `start`/`end` are absolute seconds on the voice clock.

```jsonc
{
  "meta": { "title": "…", "lang": "en", "fps": 24, "duration": 2133.5, "voice": "input/voice.mp3", "voiceOffset": 0, "grain": 0.5 },
  "cast": { "rochefort": { "nation": "USA", "outfit": "robe", "color": "#8e2c2a", "hair": "baldtop", "age": 0.75 },
            "yama": { "preset": "yamamoto" } },
  "scenes": [ { "id": "s001", "start": 0, "end": 4.2, "type": "stage", "chapter": "Why Midway Was Avoidable", "…": "…" } ]
}
```

## Scene

| field | meaning |
|---|---|
| `id` | unique, e.g. `c03s014` |
| `start`, `end` | absolute seconds; scenes must tile the timeline with no gaps |
| `type` | `stage` (set + elements) · `map` (historical map + elements) · `chapter`/`title` (title card: `title`, `subtitle`) |
| `beat` | the narration this shot shows (review only, keep it) |
| `chapter` | on the first shot of a chapter → YouTube chapter title |
| `set` | `{kind, time?, weather?, …options}` (stage) |
| `map` | `{era, center:[lon,lat], span, colors, labels, labelNames, style, land, ocean, grid}` |
| `shots` | **coverage inside the place** (stage): `[{t, on, size, frameX?, frameY?, push?, panX?, panY?, track?, dx?, dy?, shake?, x?, y?, zoom?}]`, joined by hard cuts at each `t`.<br>• `on`: an element `id` (or index), or a list of them for a group.<br>• `size`: `wide` `full` `medium` `mediumclose` `close` `ecu`.<br>• `frameX`/`frameY`: subject off-centre (fraction of the frame).<br>• `push`: zoom gain over the set-up (default 0.04).<br>• `panX`/`panY`: px of drift.<br>• `track`: follow a walking subject (with a little lag).<br>• Raw `x,y,zoom` for wides and inserts.<br>Takes precedence over `camera`. |
| `camera` | keys `{t, x, y, zoom, rotate, shake, ease}` (stage; x,y = point at screen centre) or `{t, center:[lon,lat], zoom, span}` (map). Shake is smooth noise. Prefer `shots` for stage scenes. |
| `date` | paper badge top-left ("27 MAY 1940"); `clock` badge top-right ("10:22 AM"); `place` second badge |
| `transition` | `cut` (default) · `fade` · `dip` (through black: time/place jump) · `wipe` · `flash` (impact) |
| `world` | **depth model** for stage scenes with people and vehicles: `{horizon?, y?, scale?, vehicles?}` — actors/vehicles/crowds **without** `scale` are sized from their ground y (`scale` = person scale at `y`, default 1.45 at 900; `horizon` defaults per set). Vehicles get the size they should have next to a person at the same depth; far → near draw order is automatic; keying `y` makes things grow toward the camera. `depthScale` on an element nudges one item. |
| `letterbox` | cinema bars for **dramatised** moments only (a handful per film): `true` or the caption for the bottom bar, e.g. `"DRAMATISED — ARNHEM, 19 SEPTEMBER 1944"`; it replaces the date/place badges |
| `tint` | `sepia` (counterfactual / memory / myth) · `grey` (grief) · `cold` · `warm` · `night` · `red` |
| `elements` | list, drawn in order (later = in front) |
| `sfx` | `[{t, id, vol?(dB), dur?}]` explicit cues — see sound.md |
| `ambience` | bed id (`sea`, `wind`, `wind_cold`, `rain`, `room`, `office`, `basement`, `factory`, `battle`, `crowd`, `fire`, `engine`, `jungle`, `city_night`) or `null` for silence; default comes from the set |
| `autoSfx` | `false` to disable automatic SFX for this scene |

### Set kinds (`set.kind`)
Detailed acting sets. All of them animate (sea rolls, lamps sway, dust in light, smoke, windsock).
- `garden`: brick house, hedge, bench, path.
- `bridge`: ship's bridge with wheel, telegraph, sea rolling in the windows; `nation`, `convoy`.
- `deck` / `flightdeck`: carrier flight deck with island, parked planes, crew; `nation`, `planes`, `escort`.
- `hangar`: planes, bomb carts, open side to the sea; `nation`.
- `radio`: radio racks with blinking dials, pinned messages; `desk`.
- `tent`: field HQ with lantern, crates, map table; `outside: "snow"`.
- `airfield`: hangars, tower, windsock, runway; `nation`, `planes`.
- `corridor`: receding hallway; `doors: ["ROOM 40","NO ENTRY"]`.
- `parliament`: benches of members.
- `cell`: barred-window light; `bars`.
- `train_interior`: landscape rushing past; `outside`.
- `cockpit`: canopy view with banking horizon; `bank`, `below: "land"`.
- `archbridge`: big steel arch bridge over a river (Arnhem/Nijmegen); `time` (default dusk), `burning`.
- `river`: river bank with far shore; `polder`: flat Dutch fields behind a dyke road (`dyke` y), poplars, windmills; best set for road/convoy shots.
- `workshop` / `board`: warm wooden workroom (plank wall, lamp, shelf, pinned papers, desk edge at `ground`) — the home of the physical devices (glass tubes, corkboard timeline, brass scale). Use it instead of `paper`/`studio` behind devices.
- `cabin`: inside a transport aircraft (paratroopers), `jumplight: red|green`. `heath`: open heath / drop zone. `hotel`: HQ hotel front.

Film look (every set): backgrounds get a depth-of-field blur (`dof`, default 1.6; 0 on paper/studio/void/dark/memorial) and, when the scene has no camera keys, a slow push-in (`drift` = end zoom − 1, default 0.045; `driftX` px; `drift: 0` for devices that must stay still). `meta.grade: "none"` disables the warm film grade.

Lighting runs on every set (corner falloff, window shafts with dust, lamp dust); `light: "none"` disables it.

Foreground (drawn over the actors, slight parallax): `fg`: `plant curtain rail grass sandbags officedesk desk doorframe branches barbed`; `fgSide: left|right|both`. Use `fg: "officedesk"` with `desk: false` to put people *behind* a desk.

Interiors: `office`/`study` (options: `flag`, `portrait`(bool), `portraitFlag`, `map`(label text → wall map), `shelf`, `lamp`, `desk`(bool), `deskW`, `wall`, `clockTime` "10:20"), `cabinet`/`conference` (long table, `cloth`), `warroom`, `bunker` (`map`, `flag`), `codebreak`/`classroom` (blackboard room), `kitchen`/`home`, `factory`, `rally`/`podium` (`flag`), `studio`/`paper`/`void` (`color`) — plain backdrop for devices/inserts, `dark`/`memorial`.
Exteriors: `sea`/`ocean` (`horizon`), `sky`/`air` (`below: "sea"`), `beach` (`cliffs`), `field`/`countryside`/`steppe`, `snow`, `desert`, `mud`, `jungle`, `city`/`street`/`ruins` (`ruined`), `harbor`/`dock`, `trench`, `railway`/`station`.
Common: `time`: `day|dusk|dawn|night`; `weather`: `rain|snow`; `ground` (y of floor/road); field options `road`(bool), `poles`(bool), `houses`(bool), `trees`(`round|pine|bare|palm`), `horizon`.

### Map
`era` (basemap year): `bc323 bc200 bc1 100 400 800 1100 1200 1279 1400 1492 1600 1700 1715 1783 1800 1815 1880 1914 1920 1938 1945 1960 1994 2010`.
`colors`: `{ "<polity name in basemap>": "<nation key | css colour>" }`; prefix `~` matches by substring (`"~Japan": "JPN"`). Names in 1938: `Germany`, `USSR`, `United Kingdom`, `France`, `Italy`, `Poland`, `Empire of Japan`, `United States`, `Finland`, `Romania`, `Hungary`, `Czechoslovakia`, `Yugoslavia`, `Chinese warlords`… (check with `python -c "import json;print(sorted({f['properties']['name'] for f in json.load(open('public/maps/world_1938.json'))['features']}))"`).
`center` + `span` (degrees of longitude across the frame: 6 = a city/island, 25 = a country, 60–90 = an ocean/continent). Antimeridian works (Pacific: center 175).
**Vertical extent**: the frame is 16:9 and Mercator stretches latitude, so it shows only `span × 0.5625 × cos(lat)` degrees of latitude (≈ 0.35 × span at 52° N). For a north–south route, choose `span ≥ 2.9 × (latitude extent)` — e.g. Eindhoven→Arnhem (0.55°) needs span ≈ 2.8, the Nijmegen–Arnhem stretch (0.14°) needs ≈ 0.6. Check the review sheet: every named town must be inside the frame.
`labels`: names to write at their centroid (or `true` = all coloured); `labelNames` rename them ("Empire of Japan" → "JAPAN").
`style`: `paper` (default, muted old-paper map), `old` (browner), `war`, `snow` (eastern front winter), `dark`, `sepia`, `poster` (saturated thumbnail look, white borders).
Reference look (default `paper`): tan land with a stippled texture, flat slate-blue sea, thin borders, soft paper folds; **only the sides that matter are coloured** (`colors`), clearly but printed-looking.
- `hatch`: list of country names drawn with diagonal hatching (occupied / enemy), or `true` for every coloured one.
- `rivers`: **opt-in and named** — `["Rhine", "Waal", "Maas"]` draws only those (Natural Earth names), smoothed; on city-scale maps they become water bands of real width. `riverLabels: false` hides their italic names. Never draw all rivers: it clutters the map.
- `texture: false`, `graticule: true`, `ripples: true`, `paper: false` switch the extras.
- `follow`: index of a `route`/`arrow` element — the camera rides along with its tip.
Standard map furniture: a `legend` (who is who) on every map with two or more sides, a date badge on every time jump, and `blocks` when strength matters.
Borders are the basemap's — for exact front lines draw `front`/`region` elements yourself.

## Element (all kinds)

| field | |
|---|---|
| `kind` | see below |
| `x`, `y` | stage px (map scenes: use `at: [lon, lat]` instead) |
| `scale`, `rotate`, `flip`, `opacity` | transform |
| `in`, `out` | appear / disappear time (s from scene start) |
| `enter` | Default: `none` when the element is there at the shot start (`in` ≤ 0.05). Otherwise people/vehicles `fade`, props `place`, everything else a soft `pop`.<br>Other values: `fade` · `place` (set down, no bounce) · `drop` (tossed sheet: arc + sway) · `rise` · `slideL` · `slideR` · `grow` · `stamp` · `draw` (arrows/lines/rings) · `none` |
| `exit` | `fade` (default) · `pop` · `drop` · `rise` · `slideL` · `slideR` · `none` |
| `keys` | `[{t, …any prop…, ease?, dur?}]` — numbers and `[lon,lat]` arrays tween **into** `t` from the previous key (or from the scene start); strings (pose, expr, holds, text) switch at `t`.<br>`ease`: `inOut`/`smooth` (default, smoothstep) · `in` · `out` · `linear` · `back` · `step` · `drive` · `walk` · `arrive` · `leave`.<br>Travel keys (`x`/`y`/`at`) of people default to `walk` (accelerate, steady pace, brake), with `out` → `arrive` and `in` → `leave`. Vehicles default to `drive`. |
| `hud` | `true` = fixed on screen (ignores camera) |
| `dur` | duration of a `draw` reveal (default 1.2–1.4 s) |

### Kinds

**actor** fields:
- `who`: cast id or preset (`host` = the narrator).
- `pose`, `expr`.
- `talk`: mouth + head nods + beat gestures.
- `look`: −1…1 pupils. `headMove`: `nod shake tilt`.
- `view: "back"` (over-the-shoulder), `seated`, `kneel`.
- `turn`: −1…1 — 3/4 view of the face (features shifted toward the heading, far eye foreshortened); negative = looking screen-left. Use it for dialogue.
- `id`: needed when a `shot` frames the actor.
- `front: true`: drawn after the set foreground (a shoulder over a desk; also props lying on a foreground desk). `fixedLayer: true` keeps the slot in the depth sort.
- `holds`: prop item, placed in the hand(s) automatically; `holdsScale`, `holdsRotate`, `holdsText`. Key it to change props (`"holds": ""` puts it down).
- `tag`: nameplate under the feet.

Motion:
- Keyframing `x`/`y`/`at` makes the actor **walk**: direction comes from the movement, with stride, knee bend, counter-swinging arms and lean. Keying `y` walks toward/away from the camera.
- The stride phase follows the distance covered, so feet don't slide. The stride opens and closes with speed.
- About 90–140 px/s at scale 1 is a walk; above ~300 px/s becomes a **run**. The validator warns above 420 px/s.
- `walk: true` / `run: true` + `dir` walks on the spot.
- **Pose keys blend** over 0.45–0.95 s (by hand travel): the leading hand first, the other 0.08 s later, a little anticipation on big moves, a 4 % settle. `poseDur` overrides the duration. Example: `"keys":[{"t":1.1,"pose":"head","expr":"panic"}]`.
- An expression change gets a small take (`take: 0` disables it).
- Height ≈ 280 px × scale: 1.3–1.7 for medium shots, 3.2–3.8 for thumbnail busts.

Rifle drill (with `holds: "rifle"`): `port` (across the chest, two hands), `aim`, `shoulder` (marching, rifle on the shoulder), `charge` (bayonet forward), `ease` (butt on the ground). Flat props held with `hold`/`carry` (`paper telegram folder book crate`) are gripped by their side edges.
Poses: `idle hips point pointL pointUp pointDown pointSelf raise cheer chin think head face facepalm cross hold holdUp carry show talk talk2 explain shrug present offer salute phone binoculars wave write typing fist slam cower wipe drink smoke behind pockets reach stop beg rub scratch count`.
Expressions: `neutral happy smile laugh angry rage determined smug worried sad cry panic nervous sweat shocked shout tired grin`.

**crowd** — `who` (id or list), `count`, `spacing`, `pose`, `expr`, `walk`.

**prop** — `item`: `paper telegram folder book photo magnifier suitcase phone radio stopwatch clock candle helmet crate barrel bomb shell binoculars globe hourglass medal cigar typewriter microphone sign exit flag ledger coins oil factory chair table pen skull cross grave rifle`. `photo` is an aerial reconnaissance print (`text` = caption, `value` = number of tanks); `text` (telegram/folder/book/crate/barrel/sign), `value` (stopwatch seconds, clock hour, hourglass 0–1, coins count), `nation`, `on` (phone ringing / radio playing), `color`.

**vehicle** — `type`: `tank sherman panzer4 tiger t34 panther stug halftrack truck car jeep artillery gun train locomotive wagon traincar horse cart fighter plane bomber divebomber dakota transport glider carrier battleship cruiser destroyer cargo freighter submarine uboat boat assaultboat` (all drawn with volume; nation sets the look: e.g. `fighter` UK = Spitfire camouflage, GER = grey with yellow nose, USA = bare metal; `car` GER = Kübelwagen; `bomber` UK = Lancaster black belly; old flat drawings stay as `<type>_flat`); `nation`, `color`, `moving`, `damaged`, `burning`, `crew` (tank commander in the hatch). Side view facing right (`flip` for left). Ships: scale 0.3–0.6. `tank` picks the nation's usual tank.
`parked: true` draws landing gear and puts an aircraft's wheels on its `y` (for planes on the ground).
Size next to people (in person heights, by height for ground vehicles, by length for aircraft): Sherman 1.15 tall, Tiger 1.22, truck 1.32, jeep 0.82, half-track 0.98, gun 0.78; fighter 3.6 long, Dakota/bomber/glider 7. With `world` this is automatic; with explicit scales the validator flags a vehicle that is >40 % off for the people at its depth.
Motion: key `x` (or `at`); the default `drive` profile accelerates and brakes, wheels/tracks turn with the distance, exhaust/dust while moving. **Speed limits** (drawing units/s at scale 1, peak): tanks 320–450, half-track 520, truck 650, jeep 800, boats 120–260, ships 160–240, Dakota 1300, fighters 2600. On screen that is roughly: a tank at scale 0.4 crosses ≤ 170 px/s — give a 1000 px drive ≥ 6 s, or start it closer. The validator flags anything faster.

**fx** — `type`: `smoke fire explosion impact muzzle flash tracer searchlight rain snow sparks dust splash wake fireworks speedlines question exclaim`; `dir` (deg), `count`, `color`. Explosions play once from `in`.
**burst** — explosion at `x,y` / `at` (`size` 0.4–1).

**label** — `text` (use `\n` for 2 lines), `style`: `tag` (paper) · `red` · `dark` · `green` · `yellow` · `plain` (hand-written, no box) · `map` (spaced caps); `size`, `tx`,`ty` (leader line to a point, same coordinates), `tilt`.
**stamp** — `text` (MYTH, VERDICT, FAKE, CANCELLED, 1–2 words), `color`, `size`, `tilt`; use `enter: "stamp"`.
**bubble** — speech `text` at the speaker's mouth (`x`,`y` = tail tip), `thought`, `side` (1 right / −1 left). Only for short quoted words.
**headline** / **text** — big outlined words (`size`, `color`, `accent` word in yellow, `font: "hand"`).
**counter** — `from`, `to`, `dur`, `prefix`, `suffix`, `decimals`, `size`, `color`.
**document** — `style`: `telegram letter order newspaper book blackboard note`; `title`, `lines[]` (typed progressively at `speed` chars/s), `w`, `h`, `size`, `stamp` (applied after the text finishes).

**viewfinder** (`hud: true`) — reconnaissance-camera view over an aerial `photo` (scaled up to fill the frame): corner brackets, crosshair and an `F24 <label> 042` counter; `shots: [t…]` fire the shutter (short flash, counter +1), `start` = first frame number.
**namecard** — `name`, `role` (first appearance of a person; bottom-left). **date** — extra badge (`text`, `right`).
**panel** — coloured rectangle (`w`,`h`,`color`|`nation`) for split screens; **shape** — `shape: circle|rect|ring|cross|check`.
**flag** — `nation`, `w`, `h`, `still`.
Thumbnail/emphasis helpers:
- **drop**: big sweat/tear drop (`size`, `falling`).
- **hand**: giant pointing hand with a sleeve, points +x (`sleeve`, `skin`).
- **torn**: torn-paper colour band (`w`, `h`, `color`).
- **glow**: radial light (`r`, `color`, `strength`).

Map-oriented (work on stage too with `screen: true` + px coordinates):
**arrow** — `path` (≥2 points), `color` (nation key or css), `width` (24), `dashed` (plans/intentions), `head`, `label`, `dur`, `progress` (0–1 keyable; otherwise it draws itself from `in`).
**front** / **line** / **route** — polyline `path`; `route` is dashed and carries movers: `icon` = side-view `freighter warship crate truck column tank train` (upright, facing the travel direction) or top-down `ship carrier plane sub`; `trail` = how many more icons follow behind, `gap` px apart; `iconSize`. A front can move: `path2` (the later line) + keyable `morph` 0→1.
**region** / **pocket** — `polygon` filled area (`color`, `fillOpacity`, `dashed`); `pocket` pulses (encirclement); keyable `shrink` 0→1 closes it toward its centre.
**city** — `name`, `capital`, `side` (`right left top bottom`), `size` (26), `tag: true` = the key place on a white paper tag (one or two per map); `font: "hand"` for the old handwritten style.
**unit** — NATO counter: `type` (`inf armor art cav hq`), `nation`, `label`. Move it with keys on `at`.
**ship** / **icon** — top-down `type` (`ship carrier plane sub`), `nation`, `label`, `burning`.
**ring** — `at`, `km` (radius) or `r` px; `color`, `dashed`.

### Storytelling devices (one element each)
**scale** — brass balance; the newest weight's label hangs as one paper tag per pan (no overlapping text): `left`, `right`, `leftNation`, `rightNation`, `title`, `items: [{side:"L"|"R", label, value, in, color}]` (tilts with a spring as weights drop in).
**meter** — `value` −1…1 (keyable), `left`, `right`, `title`, `leftColor`, `rightColor`.
**bars** — glass tubes with liquid on a wooden plaque: `items: [{label, value, nation|color, in}]`, `max`, `unit`, `title`, `width` (label plates sit left of the tubes: leave ~350 px).
**scoreboard** — `sides: [{nation, label, score}]`, `scores` (keyable array), `title`.
**road** — a journey as a road through a scrolling landscape: `progress` 0…1 (keyable), `length` (px of road; 24000 for a 30-min film, keep exits ≥ 900 px apart), `exits: [{at, label, painted: "allied"|"german"|"blank", paintIn, num, in}]` (slip road + gantry sign above the road; the sign is repainted at `paintIn` s, `num` shows in a badge), `towns: [{at, label}]` (boards at the verge), `vehicle`, `nation`, `vehicles` (convoy size), `time`. The convoy stays at the left third; the world (forests, poplars, posts, signs) scrolls past with parallax.
**ranking** — `items: [{label, sub, in}]` (listed top = No.N … bottom = No.1), `highlight` index, `title`.
**timeline** — a corkboard with red yarn and pinned cards: `items: [{label, sub(date), at 0…1, in, color}]`, `cursor` 0…1, `start`, `end`, `width`.
**legend** — map key box: `items: [{nation, label, color?}]`, `x`, `y` (bottom-right by default).
**blocks** — strength as a grid of small division squares: `count`, `cols`, `nation`|`color`, `size`, `label`, `dur` (squares pop in over `dur`), shows a "≈N" tag.
**ledger** — `columns: [{title, nation, entries: [{label, value, in, taken:false → struck}]}]` (running totals).

## Nation keys
`GER GERI USSR RUS USA UK JPN FRA ITA POL CHN FIN ROM HUN NED BEL AUS OTT VN SPQR CARTH NEUTRAL` — used for map fills, uniforms, flags, markings, bar colours.

## Cast spec (custom people)
`{nation, outfit, color, pants, skin, hair, hairColor, facial, hat, hatColor, badge, glasses, extra[], eyes, build, age}`
- outfit `tunic suit navy navywhite coat sailor civil dress party armor robe pilot`
- hair `side back bald baldtop short part curly bun long messy none`; facial `toothbrush walrus pencil handlebar beard goatee stubble`
- hat `peaked garrison helmet_de helmet_us helmet_uk helmet_su helmet_jp navy navy_white beret kepi bicorne ushanka fedora tophat pith sailor pilot roman crown conical pith_vn`
- glasses `round pince sun`; extra `cigar pipe cigarette medals armband epaulettes tie redtie bowtie monocle wrinkles jowls blush thickbrows star ironcross`
- eyes `dot lid big`; build 0.85–1.35; age 0–1 (≥0.55 wrinkles, ≥0.7 grey hair)
Presets (src/char/presets.ts): hitler, hitler_uniform, goering, himmler, rommel, guderian, manstein, paulus, halder, goebbels, german_officer/soldier/tanker/pilot, uboat_captain, stalin, zhukov, molotov, beria, khrushchev, soviet_officer/soldier/winter, churchill, chamberlain, halifax, montgomery, british_soldier, raf_pilot, roosevelt, truman, eisenhower, macarthur, patton, nimitz, american_soldier/sailor/pilot, us_navy_officer, hirohito, tojo, yamamoto, nagumo, japanese_officer/soldier/pilot/sailor, de_gaulle, petain, gamelin, french_soldier, mussolini, italian_soldier, mannerheim, finnish_soldier, chiang, polish_soldier, kaiser, ww1_german/british/french, napoleon, wellington, kutuzov, hannibal, roman_legionary, caesar, vn_soldier, vn_peasant, civilian_man/woman, worker, diplomat, reporter, narrator_archivist, narrator_accountant.
