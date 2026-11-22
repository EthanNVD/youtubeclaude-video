# 05 — Look at every scene

```
python tools/make.py projects/<slug> review --at all
```

With `--at all` you see the start, the middle and the end of every scene: a scene card changes during the scene (somebody enters, the camera moves in, a thing appears). Without it, `review` renders the middle frame of every scene and makes contact sheets: `review/sheet_01.jpg`, `sheet_02.jpg`, … with 12 scenes per sheet. Each tile shows the scene id (`s014`), its time, and its narration.

To see the start, middle and end of some scenes:
```
python tools/make.py projects/<slug> review --scenes s014,s015 --at all
```

## Open EVERY sheet and answer these questions for every tile

Answer each question with yes or no. Any "no" needs a fix.

**Story**
1. Does the picture show **exactly** what the clause under it says: who, doing what, where? Could a viewer with the sound off guess the clause?
2. Is someone **acting** at the key moment (looking up, slamming, turning, raising binoculars, falling back), not standing still while text explains?
3. Is the side right? Uniforms, flags and map colours.
4. Is this tile different from the one before it (place, composition, people), or a deliberate return to the same place?
5. Does a story place look the same each time it returns, with the same setting and tag, changed only by light or weather?
6. Does the tag show the right place and date? Does each new person get a name card on their first appearance?
7. Is text rare? A `caption` only on the big questions; one `stat` at most every ~2 minutes; no paper or chart standing in for an event.

**People**

8. Are people on the ground? No one floating, no one cut in half unless it is a deliberate close-up.
9. Is no one lying down and walking at the same time?
10. Are faces free of text, bubbles and other people's props? No rifle across a face, no note over a face.

**Battle**

11. Are explosions behind the men who are nearer the camera, never over a near face?
12. Do stretchers read: two bearers, the canvas, a man lying on it?
13. Do muzzle flashes sit at the rifle tips or the gun barrels?

**Text**

14. Is every caption, label and note readable, inside the frame, and clear of faces and badges?
15. Are names and numbers spelled right?

**Maps**

16. Are the named places inside the frame, with the arrows going the right way? Is the map 5 s or less?

**Scene cards** (the problems seen most often; each was found and fixed while testing)

17. Can you see the **focus person** in every frame? Nobody stands in front of them; a crowd between us and a speaker is `"view": "back"` (heads along the bottom edge).
18. Is every **held thing** in the hand and the right size: not over the face, not raised out of the top of a close shot? For a close shot, use `show` (chest height), not `hold_up` (above the head).
19. Is the **writing** readable and the right way round: signs, posters, papers? Is it in the right language for the place?
20. Is every **flag** the right one (`flag:<NATION>`)?
21. Are **children** small (`size` in the cast)? Does everybody who sits have a seat that fits: a chair indoors, a crate outside?
22. Is the same card's picture different from the card before (place, people, act or camera), or a deliberate callback (`revisit`)?
23. Does the gesture happen **on the word**: the head shake on the number, the hand to the mouth on the news?
24. Do the **arms** look natural? Hands in front of the body come straight from the shoulders, with the elbows down. Something is wrong if an elbow sticks out sideways while the forearm folds back into a loop, or if a carried thing sits in front of the face without a reason. If you see either, note the frame in `ROADMAP.md` "Known issues" (an engine fix) and choose another act for now.

## How to fix a "no"

| problem | fix in the card |
|---|---|
| wrong picture for the sentence | answer the five questions again and choose another recipe ([narration-to-picture](narration-to-picture.md)) |
| nobody acts on the key word | set the recipe's `…_on` field to that word, or choose an acted recipe (`interrupt`, `confront`, `contemplate`, `watch_front`, `vista`) |
| a story place looks different on its return | give both cards the same `place_id` (and remove a different `setting`) |
| a note or stat covers a face | move it with `"x"`/`"y"` inside `paper_note`/`stat`, or drop it |
| looks like the scene before | set `"variant": "B"` (or C), or change `setting` or `time` |
| a person or prop overlaps a label | move the label's `on` later, or remove the label |
| the important moment is not visible | move the event later or earlier with its `…_on` words |
| wrong side or uniform | fix `side` / `enemy`, or `era` in `_film.json` |
| map frame wrong | add or remove places in `show`, or change `zoom` (`map_locate`) |
| an engine drawing bug (floating, broken shape) | write it in `ROADMAP.md` "Known issues" and choose another variant for now |
| scene card: someone hidden behind someone | change `at`/`depth`; put a watching crowd `"view": "back"`; move the focus person to `back` and the others to the sides |
| scene card: a held thing covers the face | `show` instead of `hold_up`; `with` a smaller thing; put it `on` a table instead |
| scene card: the wrong act or the act too early/late | change `act` or its `on` words |
| scene card: a thing too big, too small or floating | `scale`; put it `on` a table/counter; for a drawing, fix `size`/`lift` and check it with `preview` |
| scene card: a flag or sign wrong | `flag:<NATION>`; `"text"` on the shop, poster or sign |
| scene card: looks like an earlier card | another place, person, act or camera ([visual-ideas.md](visual-ideas.md)), or `"revisit": true` if it is a deliberate callback |

After the fixes, **touch only the cards that were wrong**:
1. Run `cards` again. The other cards do not change: every card's randomness is tied to its own words.
2. Re-run `review --scenes <the ones you changed> --at all`. The sheets now show only those scenes.
3. Look at those scenes again.
4. If the film was already rendered, `python tools/make.py projects/<slug> patch` re-renders only the changed scenes and splices them in ([06-sound-render.md](06-sound-render.md) §5).

## Done when

Every tile passes. Tick "review" in `STATUS.md` and write the number of fixes you made.

Stills cannot show motion. After the render (step 7), also watch a minute around the busiest battle sequence.
