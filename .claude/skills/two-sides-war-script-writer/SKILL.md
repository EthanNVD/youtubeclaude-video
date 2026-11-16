---
name: two-sides-war-script-writer
description: >-
  Viết kịch bản documentary lịch sử chiến tranh tiếng Anh theo giọng và cách
  trình bày của kênh Two Sides of War (học từ 10 video nhiều view nhất). Ba chế
  độ: (1) nghiên cứu chủ đề mới — tìm, chấm điểm và lập dossier đề tài/tiêu đề;
  (2) viết mới từ tiêu đề — tự research, chọn device, chương, điệp khúc, verdict;
  (3) viết lại kịch bản cũ — giữ facts/thứ tự/kết của bản cũ, khoác lớp trình
  bày của kênh (hoặc chế độ chặt chỉ viết lại câu chữ). Xuất lời đọc TXT + bản có
  nhãn người nói cho bộ dựng chibi. Dùng khi người dùng xin ý tưởng video, đưa một
  title, hoặc đưa script/SRT cũ để viết lại; không dùng để dịch phụ đề giữ
  timecode hay dựng video (việc đó là srt-history-video).
---

# Two Sides War Script Writer

Viết kịch bản lời kể cho video hoạt hình lịch sử quân sự theo **ngữ pháp Two Sides of War**: một câu hỏi có thể kiểm, một device chấm điểm xuyên bài, các chương kết bằng điệp khúc, hai phía có agency, sử gia có tên, verdict cụ thể, kết bookend. Ngữ pháp rút từ phân tích toàn văn 10 video nhiều view nhất ([top10-analysis.md](references/top10-analysis.md)) và 6 SRT gốc của skill Codex ([corpus-synthesis.md](references/corpus-synthesis.md)). Học **cách kể**, không chép câu/câu đùa/device/nhân vật dẫn của video có sẵn.

## Chọn chế độ

| Đầu vào | Chế độ | Đọc |
|---|---|---|
| "Nghiên cứu/gợi ý chủ đề mới", "video tiếp theo nên làm gì", một vùng đề tài rộng chưa có title | **`topic_research`** | [topic-research.md](references/topic-research.md) |
| Một title/câu hỏi lịch sử đủ nhận diện | **`new_from_title`** | quy trình bên dưới |
| Kịch bản cũ (TXT/SRT/dán) + muốn giọng/cách trình bày của kênh | **`rewrite_channel_voice`** (mặc định cho viết lại) | [rewrite-channel-voice.md](references/rewrite-channel-voice.md) |
| Kịch bản cũ + "giữ nguyên sườn, chỉ viết lại câu chữ", "không thêm gì" | **`rewrite_same_structure`** (chặt) | [source-structure-rewrite.md](references/source-structure-rewrite.md) |

- File gửi chỉ để tham khảo văn phong/nghiên cứu không tự thành kịch bản cần viết lại. Có cả title và script để viết lại: script quyết định nội dung, title xác định đề tài.
- `topic_research` xong → người dùng chọn → chạy `new_from_title` với dossier làm research seed, không hỏi lại brief.
- Bản cũ là kịch bản của kênh khác (kể cả Two Sides of War): theo mục "kênh khác" trong rewrite-channel-voice — câu chữ, device, host, đùa, cold open phải mới; facts kiểm lại độc lập.

## Đầu vào và mặc định

- Viết mới chỉ cần **một tiêu đề/câu hỏi**; viết lại chỉ cần **bản cũ đọc được**; nghiên cứu chủ đề không cần gì (hoặc một vùng đề tài). Không đòi outline/target khi đã có mặc định.
- Lời kể **tiếng Anh**; giao tiếp/báo cáo **tiếng Việt**. Người dùng có thể đổi ngôn ngữ, độ dài, CTA, host, thoại.
- Độ dài không target: `new_from_title` = **4.800 từ (~30 phút @160 wpm)**, dải 4.560–5.040; ghi chú: trung vị top 10 là ~34 phút/5.600 từ — nếu đề tài cần 8–10 chương, đề xuất 5.400 trong brief và dùng nếu người dùng không phản đối. `rewrite_channel_voice` = số từ bản cũ +10–15% (bản tiếng Anh); `rewrite_same_structure` = số từ bản cũ ±5%.
- Mặc định format **thế hệ sau của kênh**: host duo BẬT, thoại theo chính sách 4 loại, CTA giữa bài + CTA cuối BẬT, bookend BẬT. Người dùng có thể tắt từng phần ("no host", "no dramatized lines", "no CTA").
- Narrator: giải thích rõ, hình ảnh cụ thể, hài khô ở kiêu ngạo/quan liêu/hậu cần; nghiêm túc tuyệt đối với thương vong, thường dân, tù binh, tội ác.
- Đầu ra chính: `<slug>_script_en.txt` (lời đọc sạch) + `<slug>_script_en_tagged.txt` (nhãn người nói cho bộ dựng) + `<slug>_sources.md` (hoặc `_rewrite_notes.md`). Không mặc định SEO pack/storyboard — phần đó do `srt-history-video` làm sau khi có voice + SRT.
- `evidence-grounded` cho bài mới; `source-faithful` cho viết lại (không nhận đã xác minh độc lập nếu chưa fact-check). Không bịa nhân vật, quyết định, số, trích dẫn hay suy nghĩ để sinh động.
- Title COMPLETELY/REAL/ALONE là **câu hỏi cần kiểm**, không phải đáp án. Kết luận theo bằng chứng; title quá mức thì báo ngắn ngoài narration.
- Chỉ hỏi khi không nhận diện được sự kiện/phạm vi hoặc yêu cầu mâu thuẫn thật.

## Tài liệu đúng thời điểm

1. **Luôn**, trước khi lập cấu trúc: [channel-formula.md](references/channel-formula.md) (ngữ pháp kênh, device, host, điệp khúc, thoại, CTA, ngân sách). Khi cần ví dụ cụ thể theo dạng: phần tương ứng của [top10-analysis.md](references/top10-analysis.md).
2. Viết mới: [narrative-blueprints.md](references/narrative-blueprints.md) để chọn backbone; case chi tiết trong `references/cases/` khi cần.
3. Research (bài mới, dossier đề tài, hoặc fact-check được giao): [research-protocol.md](references/research-protocol.md).
4. Trước viết: [style-guide.md](references/style-guide.md) + [workbook.md](references/workbook.md).
5. Budget/checkpoint: [length-and-delivery.md](references/length-and-delivery.md).
6. Export: [quality-rubric.md](references/quality-rubric.md) (gồm Channel fit).
7. [channel-research.md](references/channel-research.md) (snapshot 13/10) và top10-analysis (snapshot 15/11) là ảnh chụp; làm mới bằng `scripts/channel_snapshot.py` khi cần số hiện tại, không gọi số cũ là hiện tại.

## Quy trình `new_from_title`

### 1. Hợp đồng title
Working file ghi: sự kiện, thời kỳ/địa bàn, central question (nguyên văn tiếng Anh sẽ đọc trong bài), nghĩa từ khóa, backbone, device dự kiến, ngôn ngữ, target, giới hạn, mode. Ghi giả định để người dùng sửa; không dừng xin duyệt outline khi brief đủ.

Định nghĩa trước: avoidable tránh **chiến tranh, chiến dịch, thế trận hay quy mô thiệt hại**? Turning point đổi **thế chủ động, khả năng phục hồi hay kết quả dài hạn**? Alone/without nghĩa là **tắt yếu tố nào, từ năm nào**? Deadliest đo deaths, casualties hay tỷ lệ? Không giải câu hỏi khác chỉ vì dễ viết.

### 2. Research có thể truy vết
Tìm web, mở và đọc nguồn thật. Research bible: timeline; mục tiêu/thông tin từng phía; nhân lực/vật lực/hậu cần/địa lý; quyết định; cơ chế; tranh cãi **có tên sử gia**; nguồn cho mọi số/trích; **ít nhất một giai thoại phổ biến để myth-audit**; **một vật thể có thật làm setup–payoff**; hình ảnh cold open có nguồn. Ưu tiên lưu trữ, lịch sử chính thức, bảo tàng chuyên môn, sử gia đáng tin. Transcript video mẫu là chứng cứ về *cách viết*, không là authority lịch sử. Không có web/nguồn chưa đủ → giao dossier giới hạn, không bịa để ra bài hoàn chỉnh.

### 3. Research Bible → Narrative Bible
Chốt thesis sau research. Thiết kế theo channel-formula: cold open (kiểu + sự kiện), đáp án cạnh tranh, câu hỏi nguyên văn, device + tagline + luật + định nghĩa, baseline, 6–10 chương (mỗi chương: neo, hai phía, cơ chế, thoại, hậu quả, **điệp khúc**, cầu), vị trí CTA giữa bài (33–41%), myth audit, loop ledger, verdict + câu đối xứng, "to be fair", cái giá con người, CTA cuối, bookend. Mỗi block có claim IDs và budget từ. Device giữ trạng thái nhất quán (điểm số không tự đổi).

### 4. Logic theo dạng
- **Avoidable:** ai quyết, biết gì lúc đó, phương án có thật, cái giá, vì sao bỏ; bảng điểm là heuristic, không đo trách nhiệm đạo đức bằng phép cộng; kết tách "bị bắt chưa chuẩn bị" với "chọn gây chiến".
- **Turning point:** cùng định nghĩa/phép thử cho mọi ứng viên; tách nền tảng, chặn đà, đổi chủ động, bền vững, chứng minh cuối; xử lý ứng viên nổi tiếng nhất mà khán giả chờ.
- **Counterfactual test (Could X alone…):** tắt từng yếu tố theo năm/giai đoạn, kết quả ba mức (giữ/trượt/chậm); phân biệt "không thua" với "thắng tới cùng"; verdict dạng khoảng.
- **Ranked teardown:** mỗi mục đối chiếu lời biện hộ hậu chiến với số liệu; nói rõ thứ tự là quan điểm; top 3 có phản biện; mục số 1 có thể là cơ chế tổng hợp.
- **Survey / group biography:** mỗi trường hợp một nhãn ngắn + một điệp khúc; tôn trọng người còn sống; nạn nhân không bị phán xét.
- **Comparative / overview / inquiry:** như narrative-blueprints (đơn vị đếm, wayfinding, phiên bản mạnh nhất của claim).

### 5. Viết bằng model trong phiên
Chính assistant viết/biên tập. Không gọi AI endpoint ngoài, không đọc key, không nhờ tool dự án sáng tác. Subagent cùng phiên chỉ research/phản biện khi người dùng cho phép; một narrator thống nhất bản cuối. Viết 2–3 block/cluster bằng file-edit tools, viết **bản tagged trước** (NARRATOR/HOST_A/HOST_B/NHÂN VẬT [QUOTE|REPORTED|DRAMATIZED]), bản sạch sinh ra bằng cách bỏ tiền tố. Sau mỗi cluster cập nhật ledger: claim, timeline, loops, trạng thái device, điệp khúc đã dùng, tên, budget, lặp ý.

### 6. Biên tập toàn bài
Fact/quote/counterfactual audit trước style. Sau đó: câu hỏi đọc nguyên văn trước 1:15 (≈200 từ); device + luật trước 2:00 (≈320 từ); mọi chương có điệp khúc cùng khung; cầu nối nhân quả; CTA giữa bài đúng vị trí và gắn chủ đề; mọi loop được trả; myth audit có kết luận và mức chắc chắn; thoại ≤ ~15% số từ, không thoại DRAMATIZED cho nạn nhân/tội ác, mọi QUOTE truy được; verdict cụ thể + "to be fair"; bookend quay về cold open. Oral pass tiếng Anh: biến thiên câu, chủ thể rõ, thuật ngữ giải nghĩa lần đầu, ngày kiểu "the 22nd of June, 1941", số làm tròn có chủ ý.

### 7. Đếm, sửa, export
`python scripts/script_metrics.py <file> --target-words N --json <report>` trên bản **đã ghi** (bản sạch). Thiếu: bổ sung cơ chế/phản biện/chi tiết có nguồn; thừa: cắt lặp, chi tiết không phục vụ câu hỏi. Kiểm hai file khớp chữ. Export khi gates đạt; báo ngắn bằng tiếng Việt: dạng, device, số chương, số từ, thời lượng ước tính, link. Không dán toàn bài vào chat. Không ghi đè file cũ nếu không được yêu cầu.

## Checkpoint
Từ ~20.000 ký tự hoặc nhiều cluster: tạo `scratch/<slug>_working.md` và draft trước khi viết; lưu trạng thái/count sau mỗi cluster. Bị ngắt: đọc checkpoint/tail rồi viết tiếp, không viết lại từ đầu; không gọi hoàn thành khi còn placeholder hoặc claim trọng yếu chưa giải.

Trong repo này, đặt output tại `projects/<slug>/script/` khi người dùng đã có/định tạo project video; nếu không, tại thư mục người dùng chỉ định hoặc `scripts_out/<slug>/`. Không commit transcript tham khảo.

## Bất biến
- Không dựng facts/quotes/nhân vật/quyết định để đạt độ dài hoặc giống mẫu. Thoại DRAMATIZED chỉ diễn đạt lập trường đã có hồ sơ và được ghi căn cứ.
- Không nâng ước tính/tranh cãi thành chắc chắn; không cho nhân vật biết tương lai.
- Hiểu hai phía không buộc kết luận đối xứng về trách nhiệm, độ tin cậy hay đạo đức.
- Không đùa về nạn nhân; không vẽ/miêu tả biểu tượng Quốc xã như trang trí.
- Không chép câu, câu đùa, tagline, device, nhân vật dẫn của video có sẵn; không lưu transcript của kênh khác vào skill.
- Không giả research, coverage, count hay kiểm chứng. Không tự đăng video hay nhắn người khác.

## Cách gọi
`/two-sides-war-script-writer Nghiên cứu 5 chủ đề mới cho kênh, ưu tiên Mặt trận Thái Bình Dương.`

`/two-sides-war-script-writer Could Britain REALLY Have Survived Without America?`

`/two-sides-war-script-writer Viết lại kịch bản trong projects/kursk/input/old.srt theo giọng kênh, khoảng 5.000 từ.`

`/two-sides-war-script-writer Viết lại file đính kèm, giữ nguyên sườn, chỉ viết lại câu chữ, không CTA.`
