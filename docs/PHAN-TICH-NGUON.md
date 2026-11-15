# Phân tích nguồn: Two Sides of War · repo ethanNVD · repo awesome-opus5-5-videos

Ngày phân tích: 2026-11-15. Tài liệu gốc để thiết kế repo + skill **SRT → video hoạt hình lịch sử + gói YouTube**.

## 0. Phạm vi bằng chứng (đọc trước)

| Nguồn | Đã làm | Giới hạn |
|---|---|---|
| 5 video mẫu | Metadata đầy đủ (tiêu đề, mô tả, tag, chapter, thời lượng, view) + thumbnail | YouTube chặn tải video (403) và phụ đề (429) từ máy này → **tôi chưa tự xem từng frame** |
| Khung hình bên trong video | Dùng nghiên cứu khung-hình có sẵn trong repo ethanNVD (Turning Point: 609 ảnh + 1.824 frame liên tiếp; Midway: 535 ảnh + 1.192 frame; Barbarossa: 268 ảnh + 336 frame) và 2 bảng ảnh tham chiếu 12 khuôn | Nghiên cứu đó **chưa nghe/đo audio** |
| Top 10 video kênh | Metadata + 10 thumbnail (đã xem trực tiếp) | — |
| Repo ethanNVD/animation-production-studio | Clone, đọc README/AGENTS/3 skill/nghiên cứu, **render thử template** | Không khôi phục media trong GitHub Release |
| Repo yihui-dev/awesome-opus5-5-videos | Đọc README + 703 prompt trong `data/videos.json` | Không xem video demo |

---

## 1. Kênh Two Sides of War

- Kênh tiếng Anh, lịch sử quân sự (chủ yếu WW2), **32 video trong ~2 tháng (09–11/2026)** → nhịp ~4 video/tuần, mỗi video 20–48 phút. Nhịp này gần như chắc chắn có pipeline tự động hoá mạnh.
- Slogan: *"every war has two sides" / "history told from both sides"*. Mọi video xét **cả hai phe**.
- 24 fps, bản giải mã 1280×720; ~165 từ/phút (Midway: 5.851 từ / 35,5 phút, 887 cue SRT).

### Top 10 theo lượt xem

| # | Video | Views | Dài | Format/“thiết bị kể chuyện” |
|---|---|---|---|---|
| 1 | What Was The REAL Turning Point of WW2? | 387K | 40:34 | Cái **cân** + người kế toán, đặt từng ứng viên lên cân |
| 2 | Could the Soviets REALLY Have Beaten Hitler Alone? | 267K | 39:16 | Hai **ống/van** (Xô Viết vs Đồng minh) + **WAR METER** |
| 3 | Why Operation Barbarossa Was COMPLETELY Avoidable | 246K | 26:48 | **Con đường** có các lối **EXIT** bị bỏ qua + điểm số 2 phe |
| 4 | Why The Battle of Midway Was COMPLETELY Avoidable | 203K | 35:39 | Một **đường biển** + EXIT + **sổ kế toán** Japan/USA |
| 5 | How Every Country Teaches Hitler | 149K | 20:48 | **Bàn sách giáo khoa** 9 ô, tab XANH (dạy gì)/ĐỎ (bỏ qua) |
| 6 | The ENTIRE Eastern Front Explained \| WW2 1941–1945 (Animated) | 107K | 36:36 | Hai **người lính thường** (Karl/Alexei) đi xuyên cuộc chiến |
| 7 | The Deadliest Battles in Human History | 103K | 26:58 | **3 bảng xếp hạng** khác nhau, mỗi bảng ra #1 khác |
| 8 | What Happened to Hitler's Family After the War? | 91K | 37:50 | **Cây gia phả** trên bảng tối, mỗi chương sáng một nhánh |
| 9 | Why the Fall of France Was COMPLETELY Avoidable | 86K | 39:10 | **Bàn sa bàn** “Bức tường và Khu rừng”, đếm cửa FRANCE/GERMANY/GREY |
| 10 | What REALLY Lost Germany WW2? | 87K | 33:48 | **Bàn thợ** tháo cỗ máy chiến tranh, xếp hạng No.10 → No.1 |

**Kết luận chính:** mỗi video = **một câu hỏi gây tranh cãi** + **một thiết bị trực quan xuyên suốt có tính điểm** + **phán quyết cuối**. Thiết bị là “xương sống” giúp video 40 phút không rời rạc.

---

## 2. Cấu trúc kể chuyện (vĩ mô)

```
[0:00–~1:30] COLD OPEN    Một khoảnh khắc cụ thể có ngày/giờ (10:22 a.m., 4/6/1942…)
                          → nghịch lý → câu hỏi của video. Bắt đầu bằng hành động, không bằng title.
[~1:30]      SETUP        Giới thiệu thiết bị (cân/đường EXIT/van/bàn thợ) + người dẫn (Accountant/Archivist)
                          + luật chấm điểm. "We'll count every exit, for both sides."
[11–14 chương, mỗi chương 1:30–4:30]
             Mỗi chương:  date badge → master xác lập nơi chốn → người quyết định → hậu quả
                          → cập nhật thiết bị (điểm +1, đi qua EXIT, cân nghiêng) → câu nối sang chương sau
[~3–4 phút cuối] THE BILL / THE VERDICT
                          Tổng kết bằng chính thiết bị, trả lời đúng câu hỏi mở đầu, phần "historians still debate"
                          → hold nghiêm trang (nến, mũ sắt, cánh đồng) → câu hỏi cho comment
```

**Vi mô (mỗi nhịp 10–25 giây):** *trước → hành động → kết quả → phản ứng*. Một cue SRT ≠ một cảnh; gom cue theo mệnh đề. Midway: 887 cue → ~85 nhịp; Turning Point: 973 cue → 120 nhịp. Trung bình **1 nhịp / 15–20 giây**, mỗi nhịp có 1–4 shot.

**Kỹ thuật kể đáng học:**
1. **Myth-busting**: nêu huyền thoại phổ biến (“5 phút may rủi ở Midway”) → đóng dấu MYTH → sửa bằng chứng cứ. Có lần tự sửa lỗi của video cũ của kênh → tăng uy tín.
2. **Phản thực tế (counterfactual)** tách bằng màu sepia/khung khác để không lẫn với sự kiện thật.
3. **Callback**: đạo cụ quay lại (thẻ MUNICH, tờ giấy, Göring hứa hẹn ở Dunkirk ↔ Stalingrad).
4. **Số liệu gắn vào vật** (thanh NEEDED 300 tấn → GOT 6…48 trong khi cảnh sân bay tuyết cho thấy hàng tới thế nào).
5. **Độ bất định hiển thị**: “debated”, khoảng 5–7 tàu thay vì 8, ghi “estimates”.
6. **Nhịp nghiêm**: Holocaust/thảm hoạ → hold 10–12 giây một cây nến, giảm chuyển động và âm.

---

## 3. Chuyển lời → hình (ngữ pháp hình ảnh)

Video luân phiên **3 ngôn ngữ hình**, chọn theo loại ý:

| Loại ý trong lời kể | Ngôn ngữ hình | Ví dụ thật |
|---|---|---|
| Ai làm gì, ai chịu hậu quả, vật liệu, che khuất | **Không gian cụ thể** có nhân vật | Phòng nội các 5 người có biển tên; vườn đi dạo; hầm Paulus; bếp gia đình nghe tin |
| Nguồn–đích, cự ly, bao vây, mở rộng lãnh thổ | **Bản đồ** | Mũi tên đỏ cong mọc dần, hai đầu gặp nhau → loé sáng → viền túi vây xuất hiện |
| So sánh, phán xét, điểm số | **Thiết bị/biểu đồ** | Cân nghiêng khi thêm nhà máy/dầu; thanh BUILT > SUNK; stamp WEIGHED |
| Chi tiết làm bằng chứng | **Insert cận đạo cụ** | Đôi dép của Rochefort; bảng AF = ? → MIDWAY; vệt sóng của tàu Arashi; đồng hồ bấm giờ |

**Chữ trên hình (có thứ bậc, không phụ đề):**
- **Date badge** góc trên trái: thẻ giấy trắng viền xám, chữ tay in hoa nghiêng (“27 MAY 1940”, “4 JUNE 1942”, “SPRING 1943”).
- **Clock badge** góc trên phải khi nén thời gian (10:20 AM → 10:25).
- **Name card**: “CMDR. JOSEPH ROCHEFORT / chief of Station Hypo” (đỏ đậm + dòng nhỏ viết tay).
- **Label gắn vật** (STOP, REVENGE, BAIT, FAKE NEWS, SLIPPERS), **speech bubble** tên người, **stamp** kết luận (MYTH, WEIGHED, BUILT>SUNK).
- Không đặt phụ đề nguyên câu lên hình.

**POV & reveal:** góc sau lưng phi công nhìn xuống tàu sân bay; lính ở bãi biển “không thấy RAF” → cắt rộng mới lộ máy bay trên tầng mây. Góc nhìn = điều nhân vật biết.

---

## 4. Mỹ thuật

- **Nhân vật** kiểu chibi phẳng: đầu to (~42–45% chiều cao), mắt chấm/khép, lông mày + nếp nhăn tiết chế, má hồng; nhận diện bằng **tóc/hói thái dương, ria, mũ, quân phục, kính**. Tay là đường cong đen có khối, bàn tay sáng; chân mảnh, giày đặc; bóng dưới chân. Không có model 3D: đi bộ = mặt vẫn chính diện + chân luân phiên + nhún đầu.
- **Biểu cảm**: giọt mồ hôi, tay đưa lên cằm, khóc, mặt đỏ giận. Rất ít khẩu hình.
- **Bối cảnh**: phẳng có gradient nhẹ, chi tiết theo chức năng (đồng hồ = thời gian, biển tên = vị trí, radio, ống nước, đinh tán). Nhiều lớp: tiền cảnh che, mây nhiều cỡ, biển xa. Ánh sáng có nguồn (đèn Leigh, đèn pha, hàn).
- **Bản đồ**: màu phẳng, đỏ = Liên Xô/Nhật tuỳ ngữ cảnh, xám/xanh; ký hiệu đơn vị kiểu NATO; nhãn địa danh chữ tay; mũi tên đỏ cong có viền sáng.
- **Bảng màu**: trầm, ấm, hơi giấy cũ; đỏ là màu nhấn chính.
- **Font**: chữ tay in hoa hẹp (họ marker/hand-lettered condensed).

## 5. Camera & nhịp

- **Phần lớn camera đứng yên** (đo đạc: nền không dịch < 0,03 px trong 2 giây) — chuyển động đến từ nhân vật/mũi tên/cân/ánh sáng.
- Đổi cỡ cảnh bằng **cut** (wide → close vào vật/phản ứng), không zoom liên tục. Ngoại lệ: **push-in chậm trên bản đồ** (~17%/giây ở Dunkirk).
- Có master → close → master; giữ trục và hướng di chuyển.
- Montage nhanh khi liệt kê; hold dài khi nghiêm trang.

## 6. Âm thanh (suy luận — chưa đo được)

- Giọng kể tiếng Anh, nam, trầm, đều kiểu documentary (rất có thể TTS chất lượng cao, chưa xác minh).
- SRT tự động có nhãn `[music]` → **có nhạc nền** (orchestral/ambient nhẹ, dưới giọng).
- SFX gắn hành động: giấy, bước chân, điện thoại, động cơ máy bay, sóng, pháo khi thật sự bắn, stamp “thịch”.
- Đề xuất mix cho repo mới: giọng −14 LUFS tích hợp, nhạc nền thấp hơn giọng ~18–24 dB và tự duck khi có lời, ambience thưa, SFX theo frame tiếp xúc.

---

## 7. Gói metadata YouTube (từ top 10)

### 7.1 Tiêu đề — 5 khuôn lặp lại

| Khuôn | Ví dụ |
|---|---|
| `Why [Sự kiện] Was COMPLETELY Avoidable` (series, 7+ video) | Why Operation Barbarossa Was COMPLETELY Avoidable |
| `What Was The REAL [X]?` / `What REALLY [Y]?` | What Was The REAL Turning Point of WW2? |
| `Could [A] REALLY Have [B]?` | Could the Soviets REALLY Have Beaten Hitler Alone? |
| `Did [A] REALLY [B]?` | Did Winter REALLY Defeat Hitler at Moscow? |
| `How Every Country [X]` / `The ENTIRE [X] Explained \| … (Animated)` / `The Deadliest …` | How Every Country Teaches Hitler |

Quy luật: **một từ IN HOA nhấn mạnh** (REALLY/COMPLETELY/REAL/ENTIRE), dạng câu hỏi hoặc phủ định huyền thoại, 35–60 ký tự, tên riêng nổi tiếng (Hitler, Stalin, Midway, WW2) ở đầu/giữa.

### 7.2 Mô tả — template cố định

```
[Tiêu đề lặp lại]

[Hook 2–4 câu: ngày cụ thể + chi tiết sống động + nghịch lý]
So — [câu hỏi của video]?

In this animated documentary we [mô tả thiết bị kể chuyện + luật chấm].

[Đoạn dài liệt kê mọi nội dung: tên người, chiến dịch, địa danh, con số — giàu keyword]

[1 câu thesis]

⏱ Chapters
0:00 …   (11–14 mốc, tiêu đề chương ngắn, gợi hình: "The Bill", "Seventy-Two Hours")

[Câu hỏi cho comment, gắn đúng tranh luận của video] Tell us in the comments.
Subscribe for more history told from both sides. Also on this channel: "…" and "…".

In memory of …   (tưởng niệm nạn nhân 2 phía)

Sources include [sách + tác giả + năm]. [Các điểm tranh cãi được nêu là debated.]
All scenes are animated illustrations, not archival footage.

#history #ww2 #[chủ đề]     (3–4 hashtag)
```

### 7.3 Tags (20–29 tag)
1. Cụm tiêu đề viết thường (`why midway was avoidable`) + biến thể truy vấn (`midway explained`, `battle of midway documentary`).
2. Chủ đề rộng: `ww2`, `world war 2`, `ww2 documentary`, `history documentary`, `military history`, `animated history`.
3. Thực thể cụ thể trong nội dung: người, chiến dịch, tàu, sách (`nagumo`, `shattered sword`, `station hypo rochefort`).
4. Câu “catchphrase” của video (`af is short of water`) và tên kênh.

### 7.4 Thumbnail (đã xem cả 10)

| Video | Chữ | Hình |
|---|---|---|
| Turning Point | **7 DAYS. WAR LOST.** | Chia đôi DEC 5 / DEC 11 1941, Hitler tự tin → Hitler ôm đầu |
| Soviets Alone | **ALONE?** 1941–1945 | Stalin cau mày + đoàn xe Lend-Lease trên tuyết |
| Barbarossa | **A DUMB IDEA** | Bản đồ Liên Xô cháy, Hitler cười gượng đổ mồ hôi |
| Midway | **NOT 5 MINUTES** | Tàu sân bay cháy nhìn từ trên + đô đốc Nhật khóc cầm đồng hồ bấm giờ |
| Every Country | **WHOSE HISTORY?** | Hitler ở bàn với cuốn sách, 6 lá cờ |
| Eastern Front | EASTERN FRONT 1941–1945 | Hitler vs Stalin đối mặt, bản đồ chia xanh/đỏ |
| Deadliest | 70,000 / 1 IN 18 / 2 MILLION | 3 ô dọc, mỗi ô một nhân vật + một con số |
| Hitler's Family | **MY NAME IS HITLER.** | Thuỷ thủ trẻ buồn, nhiều ngón tay chỉ vào |
| Fall of France | **6 WEEKS. FRANCE LOST.** | Chia đôi MAY 10 / JUNE 22 1940, tướng Pháp tự tin → hoảng |
| What Lost Germany | **1 VS 3** | Hitler hoảng tiền cảnh, Roosevelt/Stalin/Churchill + nhà máy |

Quy luật thumbnail:
- **Ảnh AI** (phong cách cartoon viền đậm, cel-shading — chi tiết hơn style trong video).
- **2–4 từ**, trắng + 1 màu nhấn (vàng hoặc đỏ), viền đen dày; **không lặp tiêu đề** mà bổ sung “cú twist” (title Midway “Avoidable” ↔ thumb “NOT 5 MINUTES”).
- **Cảm xúc mạnh** (5/10 có giọt mồ hôi/hoảng), nhân vật lãnh đạo nhận ra ngay.
- **Bản đồ làm nền** 7/10; **chia đôi trước/sau có date badge** 3/10; **con số** 4/10.

---

## 8. Repo ethanNVD/animation-production-studio

**Là gì:** hệ thống (private, ~6.500 file) do một người xây để tái tạo đúng phong cách kênh này từ SRT: skill `srt-cinematic-animation` (đạo diễn + rig + âm cảnh + QA), `youtube-seo-packager`, `thumb-mo-ta-history`, MCP server, Studio desktop, kho nghiên cứu ~830 file.

**Cách dựng:** model **viết code vẽ từng cảnh** bằng `@napi-rs/canvas` theo thời gian tuyệt đối `drawFrame(t)` → pipe RGBA vào ffmpeg → MP4. Không dùng ảnh AI cho nhân vật. Âm thanh: chỉ ambience/foley/SFX, **không giọng, không nhạc**.

**Điểm mạnh nên kế thừa:**
- Nghiên cứu khung-hình 3 video mẫu rất kỹ (bảng lời → hình 120 nhịp).
- Quy trình “phiếu lời–hình”: mệnh đề → trước/hành động/sau → camera → bằng chứng.
- Quy tắc âm: SFX bám frame tiếp xúc, ambience giữ pha qua cut.
- Rubric SEO “curiosity-v2” (tò mò tiêu đề 35/100, thumb 20/100, phối hợp 15/100), cổng độ thật trước điểm.

**Điểm yếu (lý do không nên dựng tiếp trên nó):**
- Rất nặng quy trình/gate; README tự ghi “không bảo đảm mỹ thuật”, bài thử mới chỉ 1 phút.
- Mỗi video phải **viết tay code riêng cho từng cảnh** → 30–40 phút là khối lượng khổng lồ.
- Render thử template: bối cảnh vector khá ổn, **nhân vật cứng, đơn giản hơn mẫu nhiều**.
- Không có giọng/nhạc → khác đầu ra bạn cần.

## 9. Repo yihui-dev/awesome-opus5-5-videos

703 prompt video tạo bằng Opus 5.5 viết code (Canvas 267, SVG 183, Three.js 131, shader 92, GSAP 86). Kỹ thuật rút ra:
1. **Hàm thuần `draw(t)` / `seek(t)`**: mỗi frame chỉ phụ thuộc thời gian → render offline từng frame (headless Chrome/Playwright hoặc canvas) → ffmpeg. Không timer, không state.
2. **Style bible + component kit trước**, rồi mới dựng từng cảnh → mọi cảnh “cùng một show”.
3. **Contact sheet mỗi beat → model tự soi ảnh → sửa → render đầy đủ** (vòng tự phê bình bằng thị giác).
4. **Một ý hình mạnh mỗi cảnh**; spring thay vì linear; chuyển động trên beat.
5. Prompt podcast: tìm 35–50 thời điểm trong transcript để chèn animation, đồng bộ beat với lời, **không bịa số/trích dẫn**.
6. Âm thanh tổng hợp từ chính trạng thái hình (SFX theo sự kiện).

---

## 10. Đề xuất kiến trúc repo + skill SRT → video

**Cách tiếp cận khuyến nghị: Hybrid** — ảnh AI cho nhân vật/bối cảnh (nhất quán bằng style bible) + **code** cho mọi thứ chuyển động: camera, bản đồ, mũi tên, thiết bị tính điểm, nhãn, date badge, stamp, biểu đồ, puppet cắt lớp (nháy mắt, đổi pose tay, nhún đầu, trượt/đi). Lý do: bản đồ/biểu đồ/thiết bị — chiếm phần lớn thời lượng — code làm gần ngang mẫu; còn cảnh nhân vật thì code thuần (như ethanNVD) tốn công mà vẫn cứng.

```
SRT (+ giọng) ─► 1. Phân tích: gộp cue → câu, sửa lỗi ASR, thực thể, chương (11–14), nhịp (~1/15–20 s)
               ─► 2. Chọn thiết bị kể chuyện + người dẫn + format tiêu đề
               ─► 3. scene-plan.json: mỗi nhịp → loại cảnh, set, nhân vật, hành động trước/sau,
                     đạo cụ, nhãn, date badge, camera, SFX cue, mốc thời gian từ SRT
               ─► 4. Tài sản: thư viện nhân vật (tái dùng giữa các video), bối cảnh, bản đồ GeoJSON theo thời kỳ
               ─► 5. Render (Remotion/Canvas) → contact sheet → Claude soi & sửa → render full
               ─► 6. Âm: giọng + nhạc nền (duck) + ambience + SFX → chuẩn −14 LUFS
               ─► 7. Gói YouTube: 3 tiêu đề, 3 thumbnail, mô tả, chapters, tags, hashtags
```

**Thư viện loại cảnh (component):** MapScene (lãnh thổ, mũi tên mọc, bao vây, tuyến đường), WorldScene (bối cảnh + puppet), DeviceScene (cân, đường EXIT, van/ống, sổ kế toán, bàn thợ, bảng xếp hạng, meter), StatScene (thanh so sánh gắn vật), DocumentScene (telegram, lệnh, sách, bảng đen), InsertScene (cận đạo cụ), TitleCard/Chapter, HoldScene (nến, nghiêm trang), Counterfactual (sepia).

**Giới hạn thật:** tự động hoá hoàn toàn đến mức diễn xuất nhân vật ngang Two Sides of War (bước chân bám đất, tay cầm giấy có tiếp xúc) là khó; mục tiêu thực tế là bản đồ/thiết bị/insert ngang mẫu, cảnh nhân vật ở mức puppet tốt. Nên tạo **bản sắc riêng** (thiết bị, người dẫn, bảng màu) thay vì sao chép nguyên nhân vật/thiết bị của kênh — vừa tránh trùng lặp, vừa an toàn với chính sách nội dung tái sử dụng của YouTube.
