# Example: classroom two, Austria (a different kind of script)

A 65-second excerpt of "How countries teach Hitler": no battles, only classrooms, ministries, a press conference and a parliament. 13 `scene` cards.
It was written to prove that a new script with different content gets its own places, people and objects.

Pre-production (`cards/_film.json`):
- **cast**: the teacher and the caretaker, officials of 1945, a researcher, a 1960s teacher and three pupils (`size` 0.7), a newsboy, Waldheim, Vranitzky, deputies, a reporter;
- **story places**: a classroom today and in the 1960s, a Vienna ministry (`flag:AUS`), an archive, a Vienna street in 1986 with WALDHEIM posters, a press room, the parliament;
- **drawings** (things the engine did not have): a broom, a school desk, a lectern, the 1943 declaration with paragraph two faded (`declaration_half`) and read at last (`declaration_full`), a 1986 newspaper.

What it shows:
- **a document as a motif**: the half-read declaration in 1945, then shown whole at the end (`"revisit": true`);
- **a dialogue that carries the argument**: the caretaker's joke, over the shoulder;
- **flashbulbs**: reporters seen from behind (`"view": "back"`) never hide the speaker;
- **the speech**: Vranitzky rises, walks to the lectern, reads; the exact words in a `paper_note`; the deputies' reaction.

Rebuild: as in `projects/creative-blockade/README.md`. Without the voice, the film is timed to `input/script.srt`.
