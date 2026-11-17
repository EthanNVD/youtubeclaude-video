# Style guide — what the reference channel does (frame studies, Nov 2026)

These rules come from studying, frame by frame, five videos of the reference channel: Midway, Turning Point, Barbarossa, *Could the Soviets Have Beaten Hitler Alone?* and *Why German Soldiers Couldn't Use Captured M1 Garands*.

Every plan and every engine change is judged against them.

## 1. Picture
- **Depth.** Three or more layers in every exterior: far (soft, lighter, bluish), mid, near. Backgrounds are **blurred** (depth of field) while the characters stay sharp. Often a blurred foreground element sits at a frame edge: a branch, a snow bank, the edge of a desk.
- **Grade.** Warm, slightly desaturated colours; never candy-bright. Strong vignette and visible film grain. Night is blue-grey, not black.
- **Atmosphere.** Snow falls in small, sparse flakes. Snow sits on helmets and branches. Breath, dust and smoke drift slowly.
- **Lighting.** Window shafts and lamp cones with dust motes. Firelight is orange on faces. Wide snow shots are pale and empty.
- **Negative space.** Wide shots are sparse: a horizon of pines, a road, a few tiny figures, one truck, at most one label. Clutter is the enemy.

## 2. Camera
- **Always slightly alive.** A slow push-in or drift of 3–8 % over the shot. Never a fully static frame.
- **Cut, don't whip.** Wide → close-up on the reaction → detail insert. A push-in to a face takes 2–5 s, not 0.2 s.
- **Two-shots.** Characters are big at the frame edges facing each other, with the background blurred between them.
- **Moving subjects.** On maps the camera follows the ship or column it is talking about.

## 2b. Coverage (several set-ups per place)
- A place is filmed as **wide → medium → close-up on the reaction → insert on the evidence**, joined by hard cuts:
  - 2–4 s per set-up in action;
  - 4–6 s in explanations.
- **Close-ups come before the reaction** and hold it. The subject sits off-centre, clear of the name-card corner.
- **Dialogue** is over the shoulder: the listener big in back view at the frame edge, the speaker in 3/4.
- **Inserts are top-down on a desk**: a print under a magnifier, a red pencil ringing or crossing out, a form being stamped.
- **Arrivals and departures** use depth: walking down a corridor toward the lens, walking away in the rain.

## 3. Characters
- Big round head on a small body; rubber-hose limbs; small hands.
- Hands do things:
  - a rifle is held across the body with **two hands**;
  - papers are read; telegrams are lifted.
- Reactions are slow and readable: one pose change per sentence, an expression that holds for a moment.
- **Motion like an animated film, not a machine**:
  - walks accelerate, keep a steady pace and slow down;
  - feet never slide;
  - pose changes take ½–1 s, with one hand leading and a small settle;
  - nothing pops onto the screen on a cut;
  - vehicles squat when they pull away and dip when they brake.
- In close-ups the face fills 30–50 % of the frame height.

## 4. Vehicles, ships, aircraft
- **Drawn with volume.** The top is lit and the side darker. Tracks have links, a drive sprocket, hubcap road wheels, mud on the lower hull. Markings are small. Crew sometimes sits on the hull.
- **Move at believable speeds.** A tank crosses a wide frame in 8–15 s, a truck in 5–10 s. Motion accelerates and brakes gently; wheels turn with the distance travelled. A close pass fills the frame and leaves motion blur and kicked-up snow or dust.
- **Planes in formation** drift slowly in wide shots. A dive or close pass is fast but short (≤ 1.5 s).

## 4b. Proportion and depth (people with vehicles)
- **Same depth = believable proportion.**
  - A man standing by a tank reaches about the top of the hull; the tank is ~2.5× his height long.
  - A truck is a bit taller than a man; a jeep reaches his chest.
  - A fighter's length is ~3.5 men; a Dakota ~7.
- **Perspective is allowed to break it.** Soldiers walking close to the camera can be as big as a truck in the middle distance, as in the reference "wrong truck" scene. That reads as depth, not as a mistake.
- **Stage shots in depth.** Use three planes:
  - background: a column on the far road, small;
  - middle ground: the action;
  - foreground: a figure close to camera, cut by the frame edge.
- **Close passes.** A heavy vehicle crossing the foreground fills half the frame, with a small camera pan or shake.
- **Engine.** Use `scene.world`: sizes come from the ground y, and draw order runs far → near.

## 4c. Battle action (see `.claude/skills/srt-history-video/references/action.md`)
- **Something moves in every battle frame**: men advancing in staggered depth rows, smoke drifting, guns recoiling, muzzle flashes. Battle chapters are ≥ 55 % action; the whole film ≥ 40 %.
- **Explosions belong to the ground.** A shell bursts *where it lands*: a burst behind a man is behind him and smaller; a burst near the camera covers the men behind it. Earth columns, not cartoon stars; the camera jolts on each one.
- **Hits are a tip-over, never gore.** A man is hit, falls back with a shocked face and lies still. Fallen men never walk or run. Death is shown by stillness, an empty helmet, crosses, silhouettes at dusk, grey tint.
- **Carried means carried.** Two bearers walk; the stretcher is at their hands; the man on it lies still in it, head between them.
- **Weapons fire where they point.** The flash sits at the muzzle (rifle tip, gun barrel), automatic fire flickers, a gun kicks back and smokes. Rifles appear in the hands only when the hands reach them.
- **Stagger and cut.** Starts 0.2–0.3 s apart, falls spread over seconds, wide → group → face → wide every 2.5–5 s.
- **Numbers on the action.** A casualty counter runs over the men it counts; charts only for comparisons.

## 5. Maps
- **Clean old paper.**
  - Tan land with a faint stipple texture, flat slate-blue sea, thin dark borders.
  - Soft fold creases.
  - No graticule, no coastal hatching, no clutter.
- **Colour only the sides that matter.**
  - Clear but printed-looking fills, for example occupied ochre, liberated sage, Germany grey with diagonal hatching, Soviet terracotta, Britain blue.
  - Everything else stays plain tan.
- **Rivers only when the story needs them.**
  - Name them, e.g. Rhine, Waal, Maas.
  - On a city-scale map they are water bands of real width, never hairlines.
- **Labels.**
  - Town names are small spaced capitals next to a small ink dot.
  - The one or two key places sit on a white paper tag.
  - Map titles go on a pinned paper label.
- **Map furniture.** A legend box bottom-left with flags; a date tag top-left.
- **Movers.**
  - Ships, crates, trucks and tank columns are small side-view icons travelling along a dashed route, several in a row.
  - The camera follows them.
- **Motion.**
  - Arrows grow.
  - Fronts slide to their new line.
  - Pockets shrink.
  - The camera pushes in slowly.

## 6. Text and layout
- **Very little text on screen.**
  - One date tag (top-left).
  - One small pinned label per idea: paper tag with a pin dot, condensed capitals, ≤ 6 words.
  - Speech bubbles for quoted words, typed on.
- **Text never overlaps** other text, a face or a key object. Reserve:
  - top-left for date/place;
  - top-right for the clock;
  - bottom-left for the name card.
- Numbers are big only when the number *is* the point; otherwise they live on a tag.

## 7. Devices (the scored metaphor)
- Built as **physical objects in a space**:
  - a glass measuring tube on a wooden wall;
  - a brass gauge with a needle;
  - a chalkboard;
  - a ledger on a desk with a fountain pen;
  - a blueprint.
- Lit like the rest of the scene.
- Introduced once, then revisited with a small, legible change each time.

## 8. Sound (unchanged)
Voice is the clock. Ambience beds under every place. SFX only for visible contacts. No music.
