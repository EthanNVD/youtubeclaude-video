# 07 — YouTube package (titles, thumbnails, description, tags)

The detailed rules are in `.claude/skills/srt-history-video/references/thumbnails.md` and `metadata.md`. This page is the short path through them.

## 1. Three angles
From `understanding.md` §1, write three different curiosities about the same film:
- **myth vs truth** — "Was X REALLY…?";
- **one decision or person** — "Did Germany REALLY lose WW1 in a castle in 1917?";
- **numbers and stakes**.

Each angle gets one title, one thumbnail and one hook line.

## 2. Thumbnail prompts (the main deliverable)
1. Write `projects/<slug>/youtube/thumb_prompts.json`. Use `projects/ww1-turning-point/youtube/thumb_prompts.json` as the model. Each thumbnail needs:
   - layout;
   - characters, with their expression, pose and placement;
   - a background showing one moment;
   - a symbol;
   - a headline of 1–5 words with one accent word;
   - light and palette.
2. Run:
   ```
   python tools/make.py projects/<slug> prompts
   ```
   This writes `out/youtube/thumb_prompts.md`, ready to paste into an image model, and `out/thumbs/ref_characters.png`, to attach to it.

## 3. Engine drafts
1. Write `projects/<slug>/thumbs.json` with the same headlines. Use `projects/ww1-turning-point/thumbs.json` as the model.
2. Run:
   ```
   python tools/make.py projects/<slug> thumbs
   ```
3. Look at `out/thumbs/thumb_1..3.jpg` at small size. Are they readable at 25 %?

If the user later adds AI images as `input/thumb_N.png`, the same command puts the exact headline on them.

## 4. Description, tags, hashtags
1. Write `projects/<slug>/youtube/package.json`. Use `projects/ww1-turning-point/youtube/package.json` as the model. It holds:
   - 3 titles, with one recommended;
   - a description containing `{{CHAPTERS}}`;
   - 20–29 tags, under 500 characters in total;
   - 3–4 hashtags.
2. Run:
   ```
   python tools/make.py projects/<slug> package
   ```
3. Fix what it reports.

Never upload anything. The user publishes the video.
