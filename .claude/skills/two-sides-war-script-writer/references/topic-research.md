# Mode `topic_research` — nghiên cứu chủ đề mới

Dùng khi người dùng muốn **tìm/chọn đề tài** ("nghiên cứu chủ đề mới", "gợi ý video tiếp theo", "đề tài nào nên làm"), hoặc đưa một vùng chủ đề rộng ("chiến tranh Triều Tiên", "hải chiến WW1") mà chưa có title. Đầu ra là một **topic dossier** để người dùng chọn; sau khi chọn, chạy `new_from_title` với title đó (không cần hỏi lại brief).

## 1. Đọc trạng thái kênh

1. Snapshot kênh tham chiếu: `python scripts/channel_snapshot.py --out <scratch>/tsow` (không cần transcript) → danh sách video, view, ngày, thời lượng. Nếu không chạy được, dùng bảng trong [top10-analysis.md](top10-analysis.md) và ghi rõ ngày snapshot.
2. Nếu người dùng có kênh riêng/danh sách video đã làm (`projects/*/`), đọc để tránh trùng.
3. Ghi "đã có trên kênh tham chiếu" để không đề xuất bản sao. Đề tài trùng chủ đề vẫn được nếu **câu hỏi khác** (ví dụ kênh có "Midway avoidable" → ta có thể làm "Could Japan have won at Midway?" chỉ khi device và luận điểm khác thật).

## 2. Sinh ứng viên

Tạo 12–20 ứng viên từ ba nguồn:
- **Lỗ hổng cùng công thức**: áp các mẫu tiêu đề ([channel-formula.md](channel-formula.md) §1) vào sự kiện lớn chưa làm (Kursk, Normandy, Market Garden, Gallipoli, Somme, Dien Bien Phu, Inchon, Bulge, Singapore, Leyte, Operation Torch, Berlin 1945…).
- **Tranh cãi sử học thật**: tìm web các cuộc tranh luận ("historiography debate", "myth", "revisionist") — câu hỏi có ≥2 đáp án được sử gia có tên bảo vệ.
- **Tò mò phổ quát ngoài chiến trường**: ký ức, giáo dục, gia đình, hậu chiến, vũ khí đời thường, hậu cần, những người "ở sai bên" (dạng Teaches Hitler / Family đạt view cao dù ít trận).
Mỗi ứng viên viết ở dạng title tiếng Anh theo công thức + một câu tiếng Việt nói câu hỏi thật.

## 3. Chấm điểm (0–3 mỗi tiêu chí)

| Tiêu chí | 3 điểm khi |
|---|---|
| Độ nhận diện | tên sự kiện/người ai cũng biết (WW2, Hitler, Stalingrad, D-Day) |
| Câu hỏi có tranh cãi thật | ≥2 trường phái có tên, có bằng chứng hai phía |
| Hai phía | cả hai bên có quyết định/thông tin/agency để kể |
| Device rõ | nghĩ ra ngay một vật thể chấm điểm có trạng thái đổi theo chương |
| Đủ chương | 6–10 chương độc lập có cơ chế khác nhau |
| Nguồn truy được | có lịch sử chính thức/sách sử gia/lưu trữ online để kiểm số và trích |
| Khác kênh tham chiếu | không trùng câu hỏi; góc mới |
| Hình ảnh dựng được | bản đồ, người, đồ vật — engine `src/` vẽ được hoặc mở rộng hợp lý |
| An toàn nội dung | không cần tái dựng tàn bạo, không xúc phạm nạn nhân, không cổ vũ |

Tổng /27. Loại ứng viên <15 hoặc có tiêu chí "Nguồn" = 0. Không chấm "khả năng viral" như sự thật; ghi suy luận thành giả thuyết.

## 4. Kiểm sơ bộ 3–5 ứng viên tốt nhất

Với mỗi ứng viên: mở 3–5 nguồn thật (không chỉ snippet), ghi:
- Câu hỏi chính xác + định nghĩa từ khóa (REAL/ALONE/AVOIDABLE nghĩa là gì trong tập này).
- Đáp án cạnh tranh + tên người bảo vệ.
- Backbone + device + tagline đề xuất (tự viết).
- 6–10 chương dự kiến (một dòng/chương: ngày, nơi, cơ chế, điệp khúc trả lời gì).
- Cold open đề xuất (kiểu nào trong §4 channel-formula, sự kiện có nguồn).
- Một myth audit có thể làm; một vật thể setup–payoff.
- Verdict *dự kiến* + mức chắc chắn (có thể đổi sau research đầy đủ).
- Nguồn chính (URL thật đã mở) + rủi ro (số tranh cãi, nguồn một phía, thiếu tài liệu).

**Khi WebSearch/WebFetch lỗi:** tải text bài Wikipedia bằng API (`curl -s -A "research-script/1.0" "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&format=json&redirects=1&titles=<Title>"`), lưu vào scratch, grep các con số, tên sử gia và công trình được dẫn. Gắn nhãn đó là **nguồn khám phá**, và liệt kê các công trình gốc *cần đọc* khi viết. Không gọi đó là kiểm chứng.

## 5. Đầu ra

`scratch/topics_<yyyymmdd>.md` (hoặc thư mục người dùng chỉ định):
1. Bảng xếp hạng tất cả ứng viên với điểm.
2. Dossier chi tiết 3–5 ứng viên đầu.
3. Đề xuất một lựa chọn kèm lý do một câu.
4. Ba biến thể title cho lựa chọn đó (một chữ in hoa mỗi title).

Báo cáo chat ngắn bằng tiếng Việt: top 3 + đề xuất + link file. Người dùng chọn → chạy `new_from_title` ngay với dossier làm research seed (vẫn phải research đầy đủ theo [research-protocol.md](research-protocol.md)). Không tự viết kịch bản dài trước khi người dùng chọn, trừ khi họ bảo "chọn giúp và viết luôn".
