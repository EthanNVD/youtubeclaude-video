# 05 — Look at every scene

```
python tools/make.py projects/<slug> review
```

This renders the middle frame of every scene and makes contact sheets: `review/sheet_01.jpg`, `sheet_02.jpg`, … with 12 scenes per sheet. Each tile shows the scene id (`s014`), its time, and its narration.

To see the start, middle and end of some scenes:
```
python tools/make.py projects/<slug> review --scenes s014,s015 --at all
```

## Open EVERY sheet and answer these questions for every tile

Answer each question with yes or no. Any "no" needs a fix.

**Story**
1. Does the picture show what the narration under it says, including who, doing what, and where?
2. Is the side right? Uniforms, flags and map colours.
3. Is this tile different from the one before it? Different place, composition, or people.

**People**

4. Are people on the ground? No one floating, no one cut in half unless it is a deliberate close-up.
5. Is no one lying down and walking at the same time?
6. Are faces free of text, bubbles and other people's props? No rifle across a face.

**Battle**

7. Are explosions behind the men who are nearer the camera, never over a near face?
8. Do stretchers read: two bearers, the canvas, a man lying on it?
9. Do muzzle flashes sit at the rifle tips or the gun barrels?

**Text**

10. Is every label readable, inside the frame, and not overlapping another label or the date or name badges?
11. Are names and numbers spelled right?

**Maps**

12. Are the named places inside the frame, with the arrows going the right way?

## How to fix a "no"

| problem | fix in the card |
|---|---|
| wrong picture for the sentence | choose another recipe ([narration-to-picture](narration-to-picture.md)) |
| looks like the scene before | set `"variant": "B"` (or C), or change `setting` or `time` |
| a person or prop overlaps a label | move the label's `on` later, or remove the label |
| the important moment is not visible | move the event later or earlier with its `…_on` words |
| wrong side or uniform | fix `side` / `enemy`, or `era` in `_film.json` |
| map frame wrong | add or remove places in `show`, or change `zoom` (`map_locate`) |
| an engine drawing bug (floating, broken shape) | write it in `ROADMAP.md` "Known issues" and choose another variant for now |

After the fixes:
1. Run `cards` again.
2. Re-run `review --scenes <the ones you changed> --at all`.
3. Look at those scenes again.

## Done when

Every tile passes. Tick "review" in `STATUS.md` and write the number of fixes you made.

Stills cannot show motion. After the render (step 7), also watch a minute around the busiest battle sequence.
