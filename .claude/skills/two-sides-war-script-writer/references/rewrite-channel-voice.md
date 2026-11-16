# Mode `rewrite_channel_voice` — viết lại kịch bản cũ theo giọng và cách trình bày của kênh

Dùng khi người dùng giao một kịch bản cũ (TXT/SRT/dán vào; tiếng Anh hoặc ngôn ngữ khác) và muốn bản mới **nghe và trình bày như Two Sides of War**. Đây là mặc định khi yêu cầu viết lại nhắc tới giọng/văn phong/cách trình bày của kênh. Nếu người dùng nói "giữ nguyên sườn, chỉ viết lại câu chữ" hoặc "không thêm gì" → dùng chế độ chặt `rewrite_same_structure` ([source-structure-rewrite.md](source-structure-rewrite.md)).

## Hợp đồng

**Giữ (xương sống nội dung):** sự kiện, facts, số, người, trích dẫn có trong bản cũ; luận điểm/câu trả lời và mức chắc chắn; **thứ tự các beat nội dung**; cao trào; ý nghĩa của kết.

**Được thêm (lớp trình bày, đặt ở khớp nối, không đổi thứ tự beat):**
1. Cold open viết lại theo một kiểu trong [channel-formula.md](channel-formula.md) §4 — **dùng sự kiện đã có trong bản cũ** (thường là cao trào hoặc chi tiết nghịch lý), sau đó "rewind" về beat đầu của bản cũ.
2. Câu hỏi tiêu đề nói nguyên văn + đáp án cạnh tranh mà bản cũ đã nêu (hoặc nêu ngầm).
3. Device + tagline + luật chấm, rút từ logic của bản cũ (bản cũ liệt kê quyết định → bảng lối thoát; so sánh trận → cái cân…).
4. Điệp khúc chấm điểm ở cuối mỗi khối nội dung đã có.
5. Câu bắc cầu nhân quả giữa các khối.
6. Cặp host (tùy chọn, mặc định bật) — chỉ hỏi/chốt/luật, không thêm fact.
7. Lớp thoại: biến trích dẫn và lập trường *có sẵn trong bản cũ* thành nhịp thoại theo chính sách §12 channel-formula.
8. CTA giữa bài 33–41% (nếu bản cũ không cấm CTA) và chuỗi kết chuẩn: đọc lại device → verdict của **bản cũ** → "to be fair" (chỉ các quan điểm bản cũ có, hoặc bổ sung khi người dùng cho phép fact-check) → cái giá con người (nếu có số trong bản cũ) → câu hỏi bình luận → bookend về cold open.
9. Callback/setup–payoff bằng đồ vật **đã xuất hiện** trong bản cũ (được báo trước "remember this…" ở lần đầu).

**Không được:** thêm trận/sự kiện/số/nhân vật/trích dẫn mới (trừ khi người dùng yêu cầu fact-check/mở rộng); đổi verdict; đảo thứ tự beat; tiết lộ sớm điều bản cũ để dành, trừ đúng một sự kiện được kéo lên làm cold open (sau đó vẫn kể lại ở vị trí gốc); thay luận điểm bằng blueprint ưa thích.

## Quy trình

1. **Đọc hết bản cũ** (theo §1 source-structure-rewrite: bỏ timecode/nhãn, sửa lỗi ASR có căn cứ, không bỏ ý).
2. **Beat map** như source-structure-rewrite §2, thêm cột: `device state sau beat` và `điệp khúc dự kiến`.
3. **Thiết kế lớp trình bày** trong working file: cold open (beat nguồn nào), câu hỏi, đáp án cạnh tranh, device + tagline + luật, host (nghề, tính cách), danh sách điệp khúc, vị trí CTA giữa bài, đồ vật callback, bookend. Ghi rõ mỗi phần thêm dựa vào beat nào của nguồn.
4. **Độ dài**: không target → bản cũ tiếng Anh: số từ bản cũ +10–15% (lớp trình bày cần chỗ), dải ±5%; bản cũ ngôn ngữ khác: ước lượng theo nội dung từng beat (ghi là ước lượng). Người dùng có target → theo target. Mở rộng bằng làm rõ cơ chế đã có, không thêm fact.
5. **Viết theo cluster** (2–3 beat/cluster), checkpoint như quy trình chung; viết cả hai file (sạch + tagged) song song hoặc tạo tagged trước rồi sinh bản sạch bằng cách bỏ tiền tố.
6. **Audit**: (a) coverage + thứ tự beat như source-structure-rewrite §5; (b) mọi phần thêm truy về beat nguồn; (c) fact/quote không đổi nghĩa; (d) channel-fit rubric ([quality-rubric.md](quality-rubric.md) §Channel fit); (e) hai file khớp chữ.
7. **Export**: `<slug>_script_en.txt`, `<slug>_script_en_tagged.txt`, `<slug>_rewrite_notes.md` (beat map → output, các phần trình bày đã thêm và căn cứ, sửa lỗi nguồn, trạng thái kiểm chứng: *source-faithful*, không phải *independently verified* nếu chưa fact-check).

## Khi bản cũ là kịch bản của kênh khác (kể cả chính Two Sides of War)

- Không viết lại sát câu (paraphrase dòng-theo-dòng) — đó vẫn là bản sao và có rủi ro "reused content"/bản quyền. Phải: câu chữ mới hoàn toàn, **device, tagline, nghề host, câu đùa, cold open và bookend khác** bản gốc; facts phải được kiểm lại từ nguồn độc lập (vì bản gốc không phải authority).
- Nếu người dùng chỉ muốn "làm lại đề tài đó", đề xuất chạy `new_from_title` với cùng câu hỏi và research riêng — thường cho kết quả gốc hơn. Hỏi một lần nếu ý định không rõ; mặc định khi người dùng nói rõ "viết lại kịch bản này" là làm theo mode này với các ràng buộc trên.

## Ví dụ chức năng (tự viết)

Nguồn: kể tuần tự kế hoạch → ba quyết định → trận đánh → tổn thất → nhận xét "lẽ ra tránh được". Bản mới: cold open = phút trận đánh đổ vỡ (beat 4) → đáp án phổ biến "xui xẻo" → câu hỏi tiêu đề → "three decisions, two sides, one ledger" → rewind kế hoạch (beat 1) → mỗi quyết định kết bằng điệp khúc lối thoát → trận đánh kể lại ở vị trí gốc với chi tiết của nguồn → tổn thất → đọc lại sổ → verdict của nguồn → bookend về phút đổ vỡ. Không thêm quyết định thứ tư, không đổi "lẽ ra tránh được" thành "không thể tránh".
