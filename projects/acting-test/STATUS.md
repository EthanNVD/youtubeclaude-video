# STATUS — acting-test (1-minute coverage + motion test)

- Source: Market Garden narration 15:29–16:28 ("the photographs"), voice cut from the Market Garden wav (not committed).
- Purpose: prove the coverage grammar (several set-ups per place) and natural motion before changing the repo. **Approved by the user 2026-11-17.**
- Build: `python projects/acting-test/build.py && python tools/make.py projects/acting-test validate` → `audio` → `video` → `mux`.
- Result: `out/acting-test.mp4` (59.4 s).
  - 22 scenes, 31 set-ups (≈1.9 s each), 8 close-ups.
  - Validate: 0 errors, 1 warning (a deliberate 0.9 s close-up).
- Proposal and findings: `DE-XUAT.md`.
- Known limits:
  - the Spitfire is the generic fighter drawing;
  - no profile view for walks across the frame;
  - prop hand-over is a cut on action, not a real grip/release.
