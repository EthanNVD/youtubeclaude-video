# Quy trình tra cứu

Mục tiêu: kịch bản kể đúng nội dung tác phẩm đã chọn, đúng bối cảnh, đúng tư tưởng. Dùng cho Bước 2 (Tra cứu và Fact Ledger) ở mục 6 và cho chế độ viết mới ở mục 14 của SKILL.md. Không dựa vào trí nhớ, không dựa vào video khác.

## 1. Thứ bậc nguồn

1. **Văn bản gốc chính thức**: với Osho là osho.com; với kinh Pali là suttacentral.net, accesstoinsight.org; bản dịch Việt Phật học ở thuvienhoasen.org, budsas.org. Với Krishnamurti: jkrishnamurti.org (thư viện bài nói, đối thoại, nhật ký và trích sách của Krishnamurti Foundation Trust và Krishnamurti Foundation of America, có ngày và nơi chốn), kfoundation.org (Ấn Độ), kfa.org, trang của nhà xuất bản (Krishnamurti Publications, HarperCollins, Gollancz…), các trang mẫu sách chính thức.
2. **Tiểu sử và học thuật**: Mary Lutyens, Pupul Jayakar; Britannica; bài báo học thuật; báo chí uy tín (ví dụ cáo phó năm 1986); trang về David Bohm của các tổ chức khoa học.
3. **Wikipedia và mục lục sách**: dùng để định hướng (thư mục sách, năm xuất bản), phải đối chiếu với bậc 1–2 khi đưa vào kịch bản.
4. **Không đủ để xác nhận**: trang tổng hợp "câu nói hay", Pinterest, ảnh trích dẫn, blog, video YouTube (kể cả ABooks, BBooks), bản dịch không rõ người dịch. Rất nhiều "câu nói của Krishnamurti" lan truyền trên mạng là giả hoặc bị cắt ghép.

## 2. Cách tra

- Dùng WebSearch ở chế độ standard trước, extended khi cần chi tiết hiếm (ngày của một buổi đối thoại, người hỏi). Truy vấn bằng tiếng Anh cho văn bản gốc, tiếng Việt cho tên bản dịch và cách người xem gọi khái niệm.
- Mẫu truy vấn: `"<tên sách>" Krishnamurti contents`, `site:jkrishnamurti.org <khái niệm> <năm>`, `Krishnamurti Bohm 1980 Ojai dialogue <chủ đề>`, `"<câu trích tiếng Anh>" Krishnamurti`, `Krishnamurti <tên sách> bản dịch tiếng Việt`.
- Đọc trang gốc bằng WebFetch. Nếu bị chặn hay trang dựng bằng JavaScript, mở bằng trình duyệt trong app (`get_page_text`).
- Đã gặp ngày 17/11/2026: jkrishnamurti.org và kfa.org trả về trang xác minh chống bot cho cả WebFetch và trình duyệt trong app. Không tìm cách vượt qua; nhờ người dùng tự mở trang trong khung trình duyệt để qua bước xác minh, rồi đọc tiếp bằng `get_page_text`. kfoundation.org và kinfonet.org vẫn đọc được.
- Nếu WebSearch hoặc WebFetch lỗi, đọc Wikipedia bằng `curl -s "https://en.wikipedia.org/w/index.php?title=<Trang>&action=raw"` (để định hướng và lấy năm, biên tập, URL nguồn), và dùng `yt_research.py` cho tín hiệu YouTube.
- Gửi các truy vấn độc lập trong cùng một lượt. Thường cần 15–30 lượt cho một kịch bản.
- Nếu toàn văn cuốn sách không có ở nguồn chính thức: dựng Bản đồ sách từ mục lục chính thức, rồi lấy nội dung từ **các bài nói gốc** mà cuốn sách tuyển lại (jkrishnamurti.org thường có cùng bài nói theo ngày và nơi). Ghi rõ trong bible là đang dùng bài nói gốc.
- Không tải hay dùng file sách lậu.

## 3. Bản đồ sách (ghi vào `work/bible.md`)

```
| Mã | Chương / buổi nói | Ngày, nơi | Người đối thoại / người hỏi | Ý chính (thuật ý, 1–3 câu) | Ẩn dụ, ví dụ, câu hỏi đáng dùng | URL |
|----|-------------------|-----------|-----------------------------|----------------------------|---------------------------------|-----|
| B1 | ...               | ...       | ...                         | ...                        | ...                             | ... |
```

Chọn lát cắt: 7–10 mục làm xương cho các chặng thân bài, theo đúng thứ tự trong sách trừ khi đổi thứ tự không làm sai nghĩa. Ghi mục nào làm bước ngoặt, mục nào làm cao trào.

## 4. Fact Ledger

```
| Mã | Câu có dáng dữ kiện | Trạng thái | Viết trong kịch bản thành | URL |
|----|---------------------|------------|---------------------------|-----|
| F1 | ... | ĐÚNG / THEO LỜI KỂ / KHÔNG XÁC MINH | ... | ... |
```

- **ĐÚNG**: có ở nguồn bậc 1–2.
- **THEO LỜI KỂ**: chuyện chỉ có trong lời kể của Krishnamurti, người viết tiểu sử, hay truyền thuyết (ví dụ chuyện Nachiketa trong Katha Upanishad). Giữ nhưng đóng khung: "Krishnamurti kể…", "tương truyền…".
- **KHÔNG XÁC MINH**: bỏ, hoặc nói ở mức chung không có chi tiết cụ thể.

Những thứ bắt buộc phải có dòng trong Ledger: năm, tuổi, ngày, nơi; tên người đối thoại và vai trò của họ; số liệu (số trang, số năm "hai triệu năm", số người nghe); câu trích; chi tiết tiểu sử; tên bản dịch tiếng Việt; khẳng định khoa học (tiến hóa, não bộ). Khẳng định khoa học giữ ở mức thận trọng và gắn với người nói: "Krishnamurti và Bohm bàn đến khả năng…", không biến thành "khoa học đã chứng minh".

## 5. Trích dẫn

- Chỉ trích câu đã thấy nguyên văn tiếng Anh ở nguồn bậc 1 (hoặc bản dịch Việt đã xuất bản có người dịch rõ ràng). Ghi URL.
- Dịch sang tiếng Việt bằng lời mình, ngắn, dưới 15 chữ. Tối đa 4 câu trích trong cả bài, mỗi nguồn một câu. Còn lại thuật ý.
- Văn bản của Krishnamurti còn bản quyền (các Quỹ Krishnamurti giữ). Không chép đoạn dài, không dịch nguyên đoạn.
- Câu mở mô tả YouTube nếu là lời Krishnamurti phải theo cùng luật này. Nếu không có câu đủ ngắn thì dùng một câu của chính kịch bản (lời người dẫn), không gán cho ông.

## 6. Ghi nguồn cho người dùng

`<slug>_nguon.md` gồm: cuốn sách chính (tên tiếng Anh, năm, nhà xuất bản nếu biết, tên bản Việt nếu kiểm được); bảng Bản đồ sách rút gọn (mã, chương hay buổi nói, ngày, nơi, URL); các câu trích đã dùng kèm URL; các dữ kiện tiểu sử đã dùng kèm URL; ghi chú những điểm đã cố ý bỏ vì không kiểm được.
