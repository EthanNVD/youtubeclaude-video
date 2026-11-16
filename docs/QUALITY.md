# Quality — definition of done and review checklist

A video is **done** only when every box below is ticked. Copy this list into `projects/<slug>/STATUS.md` and tick it there.

## A. Before rendering (plan + stills)
- [ ] `validate`: 0 errors. Every warning was read; overlap and speed warnings are fixed, not ignored.
- [ ] `review` sheets inspected for **every** scene (not a sample) at start/mid/end where motion matters:
  - [ ] nothing overlaps: text on text, text on faces, signs on signs, badges on labels;
  - [ ] nothing floats: characters stand on the ground, seated people have a seat, vehicles touch the ground or water;
  - [ ] nothing is half off-frame unless it is meant to be (busts at the edges are fine; a cut-off label is not);
  - [ ] every named place on a map is inside the frame and labelled;
  - [ ] backgrounds and foregrounds scroll consistently (no static trees beside a moving road);
  - [ ] vehicles move at believable speeds and ease in and out;
  - [ ] a shot is never fully static: there is camera drift or an actor gesture;
  - [ ] ≥ 60 % acting shots, ≤ 20 % charts and documents, maps 15–25 %;
  - [ ] validate `coverage`: average set-up ≤ 4 s, close-ups in every chapter, no `one set-up for …` or `crosses … px` (sprint) warnings;
  - [ ] every acting scene has a reaction close-up or an over-the-shoulder shot; evidence is shown as an insert, not a label;
  - [ ] each idea on screen appears on the word that names it.
- [ ] No hate symbols: armbands plain, no swastika banners; rally/podium banners show national flags.
- [ ] Fact flags from the outline are fixed on screen (spelling of names and places; numbers as narrated).

## B. Sound
- [ ] `audio` reports `sound_warnings: []`.
- [ ] Integrated loudness −14 LUFS ±0.5; true peak ≤ −1 dBTP.
- [ ] Listen to one busy minute and one quiet minute: SFX land on the contact frame; ambience ducks under the voice.

## C. Render
- [ ] Only one render process at a time.
- [ ] The final MP4 lasts as long as the voice (±0.5 s): 1920×1080, H.264 + AAC.
- [ ] Spot-check 12 frames spread over the film plus motion strips (8 fps) of:
  - a walk-in;
  - a vehicle arriving and braking;
  - a pose change;
  - a prop put down;
  - a map move.
  Check for no jumps, no stops without slowing, no sliding feet, nothing popping in from nothing.

## D. Package
- [ ] 3 titles on three different angles; recommended one marked; 40–65 characters.
- [ ] Description: chapters valid (start 0:00, ≥ 10 s each), no `<` or `>`, sources only if real.
- [ ] Tags ≤ 500 characters; 3–4 hashtags.
- [ ] Thumbnail prompts: 3 layouts; exact headline of ≤ 5 words; reference sheet attached; drafts checked at 25 % size.

## E. Hand-off
- [ ] `projects/<slug>/STATUS.md` updated: what was delivered, known weaknesses, what to verify.
- [ ] Engine problems found during this video logged in `ROADMAP.md` → Known issues.
- [ ] Repo committed and pushed. No media committed.
