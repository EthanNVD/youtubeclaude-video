# Acting, coverage and motion

Read this before writing any *world* shot. It is what turned the static Market Garden v2 into the approved test (`projects/acting-test/`, `exp/acting-camera`, 2026-11-17).

Before → after, on the same minute of narration (15:29–16:28 of Market Garden):

| | v2 | approved test |
|---|---|---|
| set-ups | 8 (7.4 s each) | 31 (1.9 s each) |
| close-ups | 0 | 8 |
| action told by labels | 4 labels | 1 tag + 2 name cards |

Sources:
- The reference channel, studied frame by frame in the ethanNVD repo.
- The opus-video-skills *painted-animation* guide.

## 1. Reads first, then shots

For every beat, list the **reads**: what a first-time viewer must understand, in order. Example:
1. a message arrives;
2. he reads it;
3. he is worried;
4. he phones for planes.

Rules for reads:
- **One read at a time.** A cause and its reaction come in sequence, never on top of each other.
- **Fast actions, held meanings.** A hand-over can take 0.5 s. The worried face after it needs 1–2 s.
- **The reads set the shot length.** Don't pad a shot whose reads have landed, and don't cut one that hasn't.
- **Lead the eye.** Before an important read, the character looks at it, the camera cuts to it, or it moves first.

## 2. Coverage: several shots inside one place

A place is filmed with `scene.shots`, joined by **hard cuts**. Don't make one static set-up per scene.

| shot | when | engine |
|---|---|---|
| wide / full | establish the place and who is there; consequences | `{t, on:[ids], size:"full"}` or `{t, zoom:1}` |
| medium | business with the hands (reads, phones, writes) | `size:"medium"` |
| close (mediumclose / close / ecu) | the reaction: **cut in before it happens**, hold it | `size:"close"` with `frameX` ±0.12–0.16 |
| insert | the evidence: a photo, a form, a map, a stopwatch | `desk_insert` (top-down wood desk) |
| over the shoulder | dialogue, a commander receiving a report | `ots_dialogue`: listener in back view, big, cut by the frame |
| tracking | someone walking to a place | `track: true` (the camera follows with a little lag) |
| depth walk | arriving or leaving | `walk_to_camera` / `walk_away` (y keys + `world`) |

Rhythm:
- Action and drama: **2–4 s per set-up**. Explanations: 4–6 s.
- The validator warns when a scene with people holds one set-up for more than 6.5 s.

Framing rules:
- **Close-ups**: push the subject off-centre with `frameX` and keep the name card zone (bottom-left) clear of the face.
- **Text**: put labels in shots that are not zoomed. Labels live in world space, so a close-up enlarges them.
- **Depth inside a room**:
  - People stand **behind** a foreground desk (`fg: officedesk`, actor `y` ≈ 990): the desk covers them to the waist.
  - Papers and props lying on the desk need `front: true`.
  - A shoulder in the foreground uses `front: true` + `fixedLayer: true`.
- **Variety**: never use the same recipe for every scene. Each cut must answer a new read.

## 3. Acting

- **Every shot**: an entrance or business, a reaction on the key word, and a pose change every 1.5–3 s.
- **Dialogue**:
  - Turn faces 3/4 toward the partner (`turn` −1…1; negative = looking screen-left).
  - Alternate over-the-shoulder shots: line A from behind B, line B from behind A.
  - Short retorts get a single close-up.
- **Props change hands**: key `holds` (`""` to put a prop down), e.g. reach → `holds: "telegram"` → `hold`.
- **Point at the thing**: use `pointL` when the object is to the actor's left.
- **Expression changes** get an automatic small take (squash → settle). Change expression on the word, not between words.
- **Avoid twinning**: two actors never gesture in sync. Offset their key times by 0.3–0.6 s.

## 4. Motion that reads as animation, not as a machine

The engine does these by default; don't fight them.

**Nothing pops on a cut.**
- Things present when a shot starts are simply there.
- People arriving later fade or walk in.
- Props arriving later are *placed* (short drop, no bounce) or *dropped* (sheet falling on an arc with a sway).
- Labels arriving later get a soft pop.
- Use `enter` only when you want something different.

**People travel with a walking profile.** Keys on `x`/`y` default to `walk`: a short acceleration, a steady pace, a short braking.
- `ease: "out"` → `arrive`: already walking in from outside the frame, slows to a stop.
- `ease: "in"` → `leave`: starts from rest, keeps going out of frame.
- `linear` stays linear.

**Feet don't slide.**
- The stride phase follows the distance actually covered.
- The stride opens and closes with speed, so starting and stopping are smooth.
- Above ~300 px/s at scale 1 the walk becomes a run.

**Give walks time.** About 90–140 px/s at scale 1 is a walk; the validator warns above 420 px/s ("sprint").
- Crossing half a room (~500 px at scale 1.5) takes ~2.5 s.
- An entrance from off-frame takes 1.2–2 s.

**Pose changes take as long as the hands travel** (0.45–0.95 s):
- the leading hand starts first and the other follows ~0.08 s later;
- big moves get a little anticipation;
- arrival overshoots ~4 % and settles.
- `poseDur` overrides the duration.

**Vehicles:**
- Positional keys default to `drive` (accelerate, cruise, brake).
- The body squats as it pulls away and dips its nose when it brakes.
- Aircraft bank along their path and float slightly.
- Keep vehicle speeds believable (the validator fixes them).

**Camera:**
- Hard cuts between set-ups.
- A slow push of 3–7 % inside a set-up.
- Shake is smooth (no per-frame jitter); use it only for a close pass or an impact.

## 5. Check motion, not stills

Stills cannot show jerks. After rendering, look at frame strips of every key motion:
- a walk-in;
- a vehicle arriving and braking;
- a pose change;
- a prop being put down.

```
ffmpeg -ss <t> -t 2.5 -i out/<slug>.mp4 -vf "fps=8,scale=480:-1,tile=5x4" -frames:v 1 strip.jpg
```

Look for:
- a jump of more than ~1/6 of the move between two frames;
- a stop with no slowing;
- feet sliding;
- something appearing at full size from nothing.
