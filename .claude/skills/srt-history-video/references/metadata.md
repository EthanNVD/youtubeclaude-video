# Titles, description, tags, hashtags (language = SRT language)

## Titles — exactly 3, one per angle (each paired with a thumbnail)
Patterns that carry the reference channel (top 10 = 86K–387K views):
- `Why [Event] Was COMPLETELY Avoidable`  (a series — 7+ videos)
- `What Was The REAL [Turning Point / Cause] of [War]?` · `What REALLY [Lost/Won] [X]?`
- `Could [A] REALLY Have [B]?` · `Did [A] REALLY [B]?`
- `How Every Country [Teaches/Remembers] [X]` · `The ENTIRE [Front/War] Explained | [years] (Animated)` · `The Deadliest [X] in History`
Rules: one ALL-CAPS emphasis word (REALLY / COMPLETELY / REAL / ENTIRE — Vietnamese: THẬT SỰ / HOÀN TOÀN / CHÍNH…); a famous entity early; a question or a myth-flip; 40–65 characters; promise only what the video answers.
Vietnamese equivalents: "Vì Sao Trận Midway HOÀN TOÀN Có Thể Tránh Được?", "Liên Xô Có THẬT SỰ Thắng Hitler Một Mình?".

Score each title/thumbnail pair (editorial guess, not a prediction): curiosity 35 · thumbnail carries the same question 20 · title–thumb synergy 15 · search clarity 15 · truthfulness gate (fails = 0) · fit with channel series 15. Recommend one.

## Description template (fill from the script only)
```
<Title>

<Hook 2–4 sentences: exact date/time + vivid concrete fact + the paradox.>
So — <the question>?

In this animated documentary we <device: what we put on the table/road/scale and how we score it>.

<One long paragraph naming everything covered: people, operations, places, numbers — rich in search terms, in narrative order.>

<One-line thesis.>

⏱ Chapters
{{CHAPTERS}}

<Engagement question tied to the video's real debate.> Tell us in the comments.
Subscribe for more history told from both sides.

In memory of <the victims on all sides>.

Sources include <books/authors/years actually used by the script, if the user gave them; otherwise omit>. <Disputed points> are presented as debated.
All scenes are animated illustrations, not archival footage.
```
`{{CHAPTERS}}` is filled from `scene.chapter` timestamps (first must be 0:00, ≥3 chapters, each ≥10 s). Never invent sources; if the script names none, write a neutral line or skip it.
No `<` or `>` characters anywhere (YouTube rejects them). ≤ 5000 characters.

## Tags (20–29, ≤ 500 characters)
1. Title phrase in lowercase + query variants (`battle of midway`, `midway explained`, `battle of midway documentary`, `why midway was avoidable`).
2. Broad: `ww2`, `world war 2`, `ww2 documentary`, `history documentary`, `military history`, `animated history`.
3. Entities really in the video: people, operations, ships, places, books.
4. One or two memorable phrases from the script ("af is short of water") and the channel name.

## Hashtags
3–4 at the end of the description: `#history #ww2 #<topic>` (first three show above the title). Vietnamese: `#lichsu #thechienthu2 #<chude>`.

## package.json
```jsonc
{
  "language": "en",
  "titles": [
    { "angle": "myth vs truth", "title": "Why The Battle of Midway Was NOT Bad Luck", "thumb": 1, "hook": "At 10:22 …", "why": "…" },
    { "angle": "codebreaker", "title": "…", "thumb": 2, "hook": "…", "why": "…" },
    { "angle": "numbers", "title": "…", "thumb": 3, "hook": "…", "why": "…" }
  ],
  "recommended": 1,
  "description": "…{{CHAPTERS}}…",
  "chapters": "auto",
  "hashtags": ["#history", "#ww2", "#midway"],
  "tags": ["…"]
}
```
`python tools/make.py projects/<slug> package` checks lengths, chapters, tags budget and writes `out/youtube/`.
