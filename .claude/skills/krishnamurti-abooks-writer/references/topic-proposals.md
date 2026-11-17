# Chế độ `de_xuat`: đề xuất 5 chủ đề

Mỗi chủ đề là **một cuốn sách của Krishnamurti cộng với một nỗi đau người xem Việt Nam**, giống cách các video ABooks nhiều view được dựng. Được chọn sách ABooks hay BBooks đã làm, miễn là lát cắt (chương, buổi nói) và câu hỏi trung tâm khác.

## 1. Thu thập tín hiệu (khoảng 10–15 phút)

1. **Số liệu kênh tham chiếu**: chạy `python -I scripts/yt_research.py channel --filter krishna` (mặc định gồm ABooks và BBooks) để biết video Krishnamurti nào đang được xem, dài bao nhiêu, ra khi nào. So với ảnh chụp trong [sample-analysis.md](sample-analysis.md).
2. **Nhu cầu tìm kiếm**: chạy `python -I scripts/yt_research.py search "krishnamurti <khái niệm>" --n 20` cho 4–6 khái niệm hay nỗi đau ứng viên (sợ hãi, overthinking, cô đơn, cái chết, thiền, tình yêu, giáo dục, AI…). Ghi số video, lượt xem cao nhất, độ mới, và những góc chưa ai làm bằng tiếng Việt.
3. **Nguồn khả dụng**: với mỗi cuốn sách ứng viên, tra nhanh xem có mục lục chính thức và có bài nói gốc toàn văn trên jkrishnamurti.org không ([research-protocol.md](research-protocol.md)). Cuốn nào không dựng được Bản đồ sách thì loại.
4. **Chất liệu kịch tính**: cuốn đó có người đối thoại, cảnh, ngày tháng, câu hỏi gay gắt, khoảnh khắc lịch sử (năm 1929, những ngày cuối năm 1985–1986) không?

## 2. Chấm điểm (0–10 mỗi tiêu chí)

| Tiêu chí | Trọng số | Câu hỏi |
|---|---:|---|
| Nhu cầu | 0,25 | Nỗi đau hay khái niệm có người tìm không; video cùng đề có view không |
| Khoảng trống | 0,15 | Góc này đã có video tiếng Việt tốt chưa; nếu có, góc mình khác ở đâu |
| Chất liệu | 0,25 | Đủ 7–10 chương hay buổi nói để kể 55.000 ký tự không lặp không |
| Kịch tính | 0,20 | Có nghịch lý mở bài mạnh, có nhân vật và cảnh, có bước ngoặt tự nhiên |
| Nguồn | 0,15 | Có văn bản chính thức để kiểm từng ý không |

Loại đề xuất có Nguồn dưới 6 hoặc Chất liệu dưới 6.

## 3. Định dạng trả về trong chat

Trình bày 5 đề xuất, xếp theo điểm, mỗi đề xuất:

```
### [Số]. [Tiêu đề nháp tốt nhất]
- Sách nền: [Tên tiếng Anh] ([năm]) – [loại tài liệu], [bản Việt nếu kiểm được]
- Lát cắt: [những chương hay buổi nói sẽ dùng, ngày và nơi]
- Nỗi đau / ý định tìm kiếm: ...
- Câu hỏi trung tâm: ...
- Câu mồi dự kiến: [nghịch lý, một câu]
- Bước ngoặt và cao trào dự kiến: ...
- Khác gì video đã có: [nếu sách này đã có người làm]
- 3 tiêu đề nháp: ... / ... / ...
- Tín hiệu: [số liệu từ yt_research, ngày chụp]
- Nguồn chính: [1–3 URL]
- Điểm: Nhu cầu x · Khoảng trống x · Chất liệu x · Kịch tính x · Nguồn x → Tổng x,x
```

Kết bằng một câu khuyến nghị nên làm đề xuất nào trước và vì sao. Khi người dùng chọn, chuyển sang chế độ `viet` và dùng phần đề xuất ấy làm hợp đồng chủ đề, không hỏi lại.

Ghi 5 đề xuất vào `D:\youtubeclaude\krishnamurti\_de_xuat\<ngày>.md` để lần sau không đề xuất trùng.
