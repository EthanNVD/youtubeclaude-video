---
name: krishnamurti-abooks-writer
description: >-
  Viết kịch bản video sách nói tiếng Việt về Jiddu Krishnamurti theo cấu trúc và
  giọng gắt, ngược dòng của các video nhiều view trên kênh ABooks/BBooks (học từ 7
  video mẫu), dài 50.000–60.000 ký tự (~56–67 phút đọc), người dẫn ngôi thứ ba suốt
  bài, mọi dữ kiện tra cứu có nguồn. Hai chế độ: (1) đề xuất 5 chủ đề mới (mỗi
  chủ đề = một cuốn sách của Krishnamurti + một nỗi đau người xem), (2) nghiên cứu
  và viết kịch bản từ chủ đề, tên sách hoặc khái niệm đã chọn. Luôn kèm gói YouTube:
  3 tiêu đề, mô tả theo mẫu ABooks có mốc chương, 15–20 tag, hashtag và file nguồn.
  Dùng khi người dùng xin ý tưởng hoặc kịch bản Krishnamurti, nêu một cuốn sách
  hay khái niệm của ông. Không dùng để viết lại một kịch bản có sẵn (việc đó là
  abooks-script-rewriter) hay cho tác giả khác.
---

# Krishnamurti ABooks Writer

Viết mới, từ nghiên cứu, một kịch bản sách nói dài về Jiddu Krishnamurti mà nghe như video ABooks nhiều view: câu mồi nghịch lý, giới thiệu một cuốn sách thật trong bối cảnh thật, thân bài đi theo các chương hay các buổi nói chuyện của cuốn đó, bước ngoặt, cao trào lặng, rồi "gấp lại trang cuối" với câu hỏi treo. Khác mẫu ở ba điểm do người dùng chốt: người dẫn kể ở ngôi thứ ba suốt bài (không nhập vai Krishnamurti), không có câu cố định của kênh hay lời kêu gọi trong kịch bản, và mọi dữ kiện có nguồn.

Giao tiếp với người dùng bằng tiếng Việt. Kịch bản và gói YouTube bằng tiếng Việt.

## Chọn chế độ

| Người dùng nói | Chế độ |
|---|---|
| "đề xuất chủ đề", "video tiếp theo làm gì", "gợi ý 5 chủ đề Krishnamurti" | **`de_xuat`**, xem [topic-proposals.md](references/topic-proposals.md) |
| Chọn một trong các đề xuất ("làm chủ đề 3") | **`viet`**, dùng dossier của đề xuất đó làm hạt giống, không hỏi lại |
| Đưa tên sách ("The Ending of Time"), một khái niệm ("sợ hãi"), hoặc một tiêu đề | **`viet`** |
| Đưa một kịch bản hay phụ đề có sẵn để viết lại | Không phải skill này; dùng `abooks-script-rewriter` |

Nếu người dùng chỉ đưa khái niệm mà không đưa sách, chọn cuốn sách hợp nhất trong [book-catalog.md](references/book-catalog.md), nói ngắn lý do trong chat rồi viết. Chỉ hỏi khi yêu cầu mâu thuẫn thật hoặc không nhận ra cuốn sách.

## Mặc định (không hỏi lại)

- Độ dài **50.000–60.000 ký tự, nhắm 55.000** (tính cả khoảng trắng, xuống dòng, NFC). Tốc độ đọc đo trên mẫu là khoảng **890 ký tự mỗi phút**, nên 55.000 ký tự ≈ 62 phút. Trong 10 video Krishnamurti của ABooks, các video trên 55 phút đứng đầu về lượt xem.
- **Mỗi video bám một cuốn sách chính** (có thể thêm 1–2 bài nói khác cùng chủ đề làm chất liệu phụ). Được làm lại sách ABooks đã khai thác nếu chọn lát cắt hay góc khác.
- **Người dẫn "tôi" suốt bài**, gọi Krishnamurti ở ngôi thứ ba. Giọng **gắt, ngược dòng**, xen những đoạn lặng ở cao trào và kết ([style-dna.md](references/style-dna.md)).
- **Không có câu cố định của kênh** trong kịch bản: không "Bạn đang nghe…", không mời mua sách, không mời bình luận hay đăng ký, không "video tiếp theo". Các lời mời này chỉ nằm trong mô tả.
- Nguồn: tự tra cứu, ưu tiên toàn văn chính thức trên jkrishnamurti.org ([research-protocol.md](references/research-protocol.md)). Không bịa trích dẫn, ngày tháng, người đối thoại hay giai thoại.
- Đầu ra trong `D:\youtubeclaude\krishnamurti\<slug>\` (thư mục riêng, tách hẳn khỏi phần video lịch sử; không commit trừ khi người dùng bảo):
  - `<slug>_kichban_<sokytu>.txt`: lời đọc sạch cho TTS.
  - `<slug>_youtube.txt`: 3 tiêu đề, mô tả, hashtag, tag ([seo-package.md](references/seo-package.md)).
  - `<slug>_nguon.md`: danh sách nguồn và Fact Ledger rút gọn.
  - `work/`: bible, các phần nháp, ghi chép tra cứu.

## Tài liệu đọc đúng lúc

1. Luôn đọc trước khi lập dàn ý: [style-dna.md](references/style-dna.md), gồm cấu trúc, ngân sách, giọng và các động tác kể.
2. Khi cần ví dụ cụ thể từ mẫu: [sample-analysis.md](references/sample-analysis.md).
3. Khi chọn sách hoặc đề xuất chủ đề: [book-catalog.md](references/book-catalog.md) và [topic-proposals.md](references/topic-proposals.md).
4. Khi tra cứu: [research-protocol.md](references/research-protocol.md).
5. Khi làm gói YouTube: [seo-package.md](references/seo-package.md).
6. Kiểm tra: `scripts/k_check.py`. Số liệu kênh: `scripts/yt_research.py` (ảnh chụp ngày 17/11/2026 nằm trong sample-analysis; muốn số hiện tại thì chạy lại).

## Quy trình `viet`

Tạo task list theo các bước sau. Bài dài phải ghi ra file từng phần. Nếu phiên bị ngắt, đọc lại `work/bible.md` và phần cuối cùng rồi viết tiếp, không viết lại từ đầu.

### 1. Hợp đồng chủ đề
Ghi vào `work/bible.md`: cuốn sách chính (tên tiếng Anh, tên tiếng Việt nếu có bản dịch, năm, loại: đối thoại, bài nói, nhật ký, thư, tuyển tập), lát cắt sẽ khai thác (những chương hay buổi nói nào), nỗi đau người xem, **câu hỏi trung tâm** (một câu, sống suốt bài), nghịch lý mở bài, từ khóa chính và phụ dự kiến. Ghi giả định để người dùng sửa sau; không dừng lại xin duyệt dàn ý.

### 2. Tra cứu, Bản đồ sách và Fact Ledger
Theo [research-protocol.md](references/research-protocol.md):
- **Bản đồ sách**: mục lục hay danh sách buổi nói của cuốn sách, mỗi mục có ngày, nơi chốn, người đối thoại và ý chính (thuật ý bằng lời mình), kèm URL toàn văn nếu có.
- **Bối cảnh thật**: tiểu sử liên quan (đã kiểm chứng), hoàn cảnh ra đời của sách, người đối thoại là ai.
- **Kho chất liệu**: 10–15 ẩn dụ, ví dụ, câu hỏi của người nghe, cảnh thiên nhiên mà chính Krishnamurti dùng trong các văn bản đó; 2–4 câu trích ngắn (dưới 15 chữ) đã tìm thấy nguyên văn ở nguồn chính thức.
- **Fact Ledger**: mọi câu có dáng dữ kiện (năm, tuổi, nơi, tên người, số trang, câu trích) đều có trạng thái ĐÚNG, THEO LỜI KỂ, hoặc KHÔNG XÁC MINH (thì bỏ), kèm URL.
Thường cần 15–30 lượt tra cứu; gửi các truy vấn độc lập trong cùng một lượt.

### 3. Narrative Bible và ngân sách
Thiết kế theo khung 6 phần trong [style-dna.md](references/style-dna.md): câu mồi, giới thiệu sách và lời cảnh báo, thân bài 7–10 chặng (mỗi chặng ứng với một chương hay buổi nói trong Bản đồ sách và mở bằng một **tựa chặng đọc thành lời**), bước ngoặt, cao trào, rồi "gấp lại trang cuối". Mỗi chặng ghi: mục đích, mã mục trong Bản đồ sách, mã dữ kiện, cảnh mở, cơ chế bóc tách, ẩn dụ của Krishnamurti, cảnh đời thường Việt Nam (giả định), phản biện thay người nghe, câu đóng ý, câu móc sang chặng sau, và ngân sách ký tự (min/target/max). Cài 2–3 **vòng lặp mở** ở mở bài và đánh dấu chỗ sẽ trả. Ghi vị trí các **móc giữ chân** (cứ khoảng 8.000–10.000 ký tự một móc).

### 4. Viết theo cụm
- Mỗi lượt viết 2–3 chặng liền nhau (8.000–15.000 ký tự), ghi bằng Write vào `work/part01.txt`, `part02.txt`… Chính assistant viết; không dùng script hay API ngoài để sinh văn bản.
- Thuật ý bằng câu chữ mới. Không chép đoạn văn của Krishnamurti, của bản dịch hay của video mẫu. Học cách kể của mẫu, không chép câu của mẫu ([sample-analysis.md](references/sample-analysis.md) liệt kê những câu đặc trưng không được dùng lại).
- Sau mỗi cụm, cập nhật sổ trong bible: mục sách đã dùng, dữ kiện đã dùng, ẩn dụ và cảnh đã dùng, họ ẩn dụ gắt đã dùng bao nhiêu lần, vòng lặp đã mở và đã trả, số ký tự hiện tại. Trước cụm sau, đọc lại đoạn cuối cụm trước và sổ chống lặp.

### 5. Kiểm định và chỉnh
Ghép các phần thành bản nháp bằng thao tác cơ học (`cat`, mỗi phần cách nhau một dòng trống), rồi chạy:

```
python -I D:/youtubeclaude/.claude/skills/krishnamurti-abooks-writer/scripts/k_check.py <ban_nhap.txt> --min 50000 --max 60000 --keywords "krishnamurti,<từ khóa chính>,<phụ>"
```

Sửa đúng vùng lỗi bằng Edit theo thứ tự: dữ kiện (truy được về Ledger), ngôi kể (không nhập vai), trích dẫn (ngắn, có nguồn), lặp ý theo nghĩa, độ gắt (không lạm một họ ẩn dụ), cấu trúc (đủ 6 phần, móc giữ chân, bước ngoặt, vòng lặp đã trả), độ dài. Thiếu chữ thì mở rộng bằng chất liệu thật chưa dùng trong Bản đồ sách; nếu hết thì tra thêm. Thừa thì cắt ví dụ thứ hai cho cùng một ý và các câu chuyển thừa. Không đạt độ dài mà không bịa hay lặp thì dừng, báo con số tối đa an toàn, không gọi là xong.

### 6. Chuẩn TTS
Chỉ nội dung để đọc: không Markdown, heading, gạch đầu dòng, emoji, URL, ghi chú. Không dùng `% & @ = < > / # *`, `...`, `…`, `!!`, `??`. Số đếm nhỏ viết bằng chữ; năm có thể giữ chữ số ("năm 1980"); ngày viết "ngày mười lăm tháng tư năm 1980". Tên riêng viết thống nhất: Krishnamurti (lần đầu "Jiddu Krishnamurti"), David Bohm, Ojai, Brockwood Park, Rajghat, Madanapalle… Câu trên 45 từ phải tách.

### 7. Gói YouTube
Theo [seo-package.md](references/seo-package.md): 3 tiêu đề thuộc 3 họ khác nhau, mô tả theo khung mẫu ABooks kèm mốc chương ước tính (script in sẵn mốc từ các tựa chặng), dòng tư liệu, 15–20 tag sạch, 5–7 hashtag. Kiểm bằng `--seo <file>`.

### 8. Xuất và báo cáo
Chạy script lần cuối trên đúng file xuất. Gửi ba file bằng SendUserFile; không dán kịch bản vào chat. Dán gói YouTube vào chat để người dùng chép. Báo cáo ngắn: số ký tự, số từ, thời lượng ước tính; cuốn sách và lát cắt đã dùng; dữ kiện chính đã kiểm chứng; câu trích nguyên văn đã dùng kèm nguồn; những điểm của mẫu đã cố ý không theo (nếu có); danh sách nguồn dạng [Tiêu đề](URL).

## Luật cứng

1. Người dẫn không bao giờ nói như Krishnamurti ("Một người hỏi tôi…", "Tôi đã gặp hàng ngàn người…"). Lời ông chỉ xuất hiện dạng thuật ý ("ông trả lời đại ý rằng…") hoặc trích ngắn đã kiểm chứng.
2. Không câu trích nào chưa tìm thấy nguyên văn ở nguồn bậc 1–2. Mạng có rất nhiều "câu nói của Krishnamurti" giả. Không đặt lời diễn giải trong ngoặc kép.
3. Không dữ kiện nào nằm ngoài Fact Ledger: ngày, tuổi, nơi, người đối thoại, số năm, tên sách, chi tiết đời ông.
4. Cảnh đời thường Việt Nam phải là giả định ("Thử nhìn…", "Có thể bạn từng…"), không gán tên người hay sự kiện thật.
5. Độ gắt phục vụ luận điểm, không phải để giật gân: không khẳng định y khoa, không hứa chữa lành, không công kích tôn giáo, thầy hay nhóm người cụ thể.
6. Không câu cố định của kênh và không lời kêu gọi trong kịch bản.
7. Không chép câu đặc trưng của video mẫu, không chép tiêu đề của kênh khác.
8. Không gọi là hoàn thành khi ngoài dải độ dài hoặc còn lỗi ở các cổng trong [style-dna.md](references/style-dna.md).
