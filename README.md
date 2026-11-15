# SRT → Video lịch sử quân sự hoạt hình

Từ **file SRT + file giọng đọc** → video hoạt hình giải thích lịch sử quân sự theo ngữ pháp của kênh *Two Sides of War*
(nhân vật chibi, bản đồ lịch sử, "thiết bị kể chuyện" có tính điểm, date badge, stamp, SFX theo hành động — **không nhạc nền**),
kèm **gói YouTube**: 3 tiêu đề, **3 prompt thumbnail chi tiết** để mang sang ChatGPT / Gemini / Midjourney / Ideogram (kèm ảnh tham chiếu nhân vật + bản phác bố cục), mô tả có chapters, tags, hashtags.

Video ưu tiên **diễn cảnh thực** như phim hoạt hình: nhân vật đi lại, cầm nắm, phản ứng trong bối cảnh chi tiết (boong tàu, buồng lái, phòng vô tuyến, hành lang, khu vườn…). Có **người dẫn chuyện cố định** (`host`) xuất hiện ở mở đầu, chuyển chương và kết luận.

Hình vẽ hoàn toàn bằng code (React/SVG + [Remotion](https://www.remotion.dev)), âm thanh tổng hợp bằng code — không cần API trả phí, không dùng tài sản có bản quyền.
Phân tích nguồn (kênh mẫu, 2 repo tham khảo, top 10 video): [docs/PHAN-TICH-NGUON.md](docs/PHAN-TICH-NGUON.md).

## Cách dùng (với Claude Code)

1. Tạo thư mục dự án và bỏ file vào:
   ```
   projects/<ten-video>/input/<ten>.srt
   projects/<ten-video>/input/voice.mp3        (hoặc .wav/.m4a — giọng đọc khớp SRT)
   ```
2. Mở Claude Code trong thư mục repo và nói: **"Dựng video từ projects/<ten-video>"**.
   Claude dùng skill [`srt-history-video`](.claude/skills/srt-history-video/SKILL.md): đọc toàn bộ SRT → dàn ý + thiết bị kể chuyện → kế hoạch cảnh
   → tự soi ảnh từng cảnh và sửa → trộn âm → render → 3 thumbnail + gói YouTube.
3. Kết quả trong `projects/<ten-video>/out/`:
   - `<ten-video>.mp4` — video 1920×1080, 24 fps, âm −14 LUFS
   - `audio/stems/` — voice / ambience / sfx tách riêng
   - `youtube/thumb_prompts.md` — **3 prompt thumbnail** (bản đầy đủ cho ChatGPT/Gemini/Ideogram, bản "không chữ", bản Midjourney)
   - `thumbs/ref_characters.png` — ảnh tham chiếu nhân vật, đính kèm khi tạo ảnh để giữ đúng tạo hình
   - `thumbs/thumb_1..3.jpg` — bản phác bố cục (vẽ bằng engine)
   - `youtube/` — `titles.txt` (★ đề xuất), `description.txt`, `tags.txt`, `hashtags.txt`, `chapters.txt`, `report.md`
4. Tạo ảnh thumbnail bằng model bạn chọn. Nếu model viết sai chữ, lưu ảnh vào `projects/<ten-video>/input/thumb_1.png` (…2, 3) rồi chạy
   `python tools/make.py projects/<ten-video> thumbs` → tiêu đề chữ chuẩn được ghép lên ảnh của bạn.

Ngôn ngữ chữ trên hình và metadata theo ngôn ngữ của SRT (Anh, Việt… — font hỗ trợ tiếng Việt).

## Lệnh thủ công

```bash
python tools/make.py projects/<slug> analyze    # đọc SRT + giọng -> work/reading.md, stats.json
python tools/make.py projects/<slug> validate   # kiểm tra kế hoạch cảnh
python tools/make.py projects/<slug> review     # ảnh từng cảnh -> review/sheet_*.jpg
python tools/make.py projects/<slug> audio      # trộn giọng + ambience + SFX
python tools/make.py projects/<slug> video      # render hình (≈ 1× thời lượng thực trên máy 12 luồng)
python tools/make.py projects/<slug> mux        # ghép hình + tiếng
python tools/make.py projects/<slug> prompts    # 3 prompt thumbnail + ảnh tham chiếu nhân vật
python tools/make.py projects/<slug> thumbs     # bản phác thumbnail, hoặc ghép chữ lên input/thumb_N.png
python tools/make.py projects/<slug> package    # kiểm tra + xuất gói YouTube
python tools/make.py projects/<slug> all        # audio → video → mux → prompts → thumbs → package
npm run studio                                  # Remotion Studio để xem/chỉnh trực tiếp
```
Ví dụ đầy đủ: `projects/_test` (60 giây về Midway; giọng máy Windows chỉ để thử timing). `projects/_showcase`: 12 bối cảnh diễn mẫu (`node tools/render.mjs stills projects/_showcase/plan.json <thư-mục>`).

## Cài trên máy mới

Yêu cầu: Node ≥ 20, Python ≥ 3.11 (`numpy scipy pillow shapely`), FFmpeg/FFprobe trong PATH.
```bash
npm ci
pip install numpy scipy pillow shapely
python tools/sfx_synth.py        # tạo thư viện SFX/ambience (assets/sfx, ~40 MB, không commit)
```
Lần render đầu Remotion tự tải Chrome headless. Font tải từ Google Fonts khi render (cần mạng).

## Cấu trúc

| Đường dẫn | Nội dung |
|---|---|
| `.claude/skills/srt-history-video/` | Skill đạo diễn: quy trình, ngữ pháp kể chuyện, DSL kế hoạch cảnh, âm thanh, thumbnail, metadata |
| `src/` | Engine Remotion: `char/` nhân vật + 76 preset, `sets/` 38 bối cảnh, `props/` đạo cụ & phương tiện, `fx/`, `map/` bản đồ lịch sử, `devices/` cân/đồng hồ/biểu đồ/đường EXIT/xếp hạng/timeline/sổ, `overlays/` chữ trên hình, `Thumbnail.tsx` |
| `tools/` | `make.py` (điều phối), `srt_tool.py`, `validate_plan.py`, `render.mjs`, `contact_sheet.py`, `mix_audio.py`, `sfx_synth.py`, `seo_check.py`, `fetch_maps.py`, `guide_voice.py` |
| `public/maps/` | Bản đồ biên giới lịch sử 25 thời kỳ (323 TCN → 2010) |
| `assets/sfx/` | SFX/ambience (sinh bằng `sfx_synth.py`; file thật cùng tên sẽ thay thế) |
| `projects/` | Mỗi video một thư mục (`input/`, `plan.json` hoặc `plan/ch*.json`, `thumbs.json`, `youtube/package.json`) |

## Giới hạn hiện tại

- Nhân vật là con rối 2D nhìn chính diện: đầu gắn liền thân, tay chân "ống cao su" cong mềm, bàn tay đổi dáng theo tư thế, chuyển tư thế mượt, đi/chạy có gập gối, cầm đạo cụ đúng tay. Chưa có góc nghiêng 3/4 thật như kênh mẫu.
- SFX tổng hợp nghe "sạch" hơn thu âm thật; bỏ file CC0/có bản quyền vào `assets/sfx/<id>.wav` để nâng chất lượng.
- Thumbnail cuối cùng do bạn tạo bằng model ảnh từ prompt; bản engine chỉ là phác bố cục / phương án dự phòng.

## Giấy phép dữ liệu

`public/maps/*` chuyển từ [aourednik/historical-basemaps](https://github.com/aourednik/historical-basemaps) (GPL-3.0). Remotion: miễn phí cho cá nhân/công ty ≤ 3 người.
