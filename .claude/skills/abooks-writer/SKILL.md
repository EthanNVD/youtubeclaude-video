---
name: "abooks-writer"
description: "Viết kịch bản tiếng Việt kiểu Abooks (review sách triết học, tâm linh: Krishnamurti, Osho, Phật học), 50.000–60.000 ký tự, mở bài bằng câu cách ngôn và bảy nhịp như video Abooks nhiều view, thân bài khẳng định, giàu hình ảnh và giai thoại đã kiểm, tra cứu không bịa, xuất TXT cho TTS, kèm 3 tiêu đề, mô tả có mốc chương ước tính, hashtag và 10 tag YouTube. Hai cách có kịch bản: viết lại một kịch bản hay phụ đề có sẵn, hoặc tự nghiên cứu rồi viết mới từ một chủ đề, tên sách, khái niệm; ngoài ra đề xuất 5 chủ đề mới. Dùng khi người dùng đưa file phụ đề hay kịch bản để viết lại, xin ý tưởng video, hoặc nêu một cuốn sách, một khái niệm của các tác giả này."
---

# Abooks Writer

Skill này lấy nguyên lõi của skill `abooks-script-rewriter` (giọng, cấu trúc, quy trình, script kiểm tra, gói SEO) và gắn thêm hai chế độ chạy trên cùng lõi ấy: đề xuất chủ đề và viết mới. Mọi chế độ dùng chung mục 3 (giọng), mục 4 (ADN văn phong), mục 7 (luật cứng), mục 8 (thang chất lượng) và mục 12 (gói SEO). Phạm vi: Krishnamurti, Osho, Phật học.

## 0. Chọn chế độ

| Người dùng đưa | Chế độ | Làm theo |
|---|---|---|
| File phụ đề, kịch bản, transcript cần viết lại | **viết lại** | Toàn bộ mục 1–12 dưới đây, đúng như skill gốc |
| "Đề xuất chủ đề", "video tiếp theo nên làm gì" | **đề xuất** | Mục 13 và [topic-proposals.md](references/topic-proposals.md) |
| Một tên sách, một khái niệm, một tiêu đề, hoặc một đề xuất đã chọn | **viết mới** | Mục 14: tra cứu thành một "bản nguồn" rồi chạy mục 2–12 |

Khi không rõ, hỏi đúng một câu. Bản nguồn là kịch bản của kênh khác thì vẫn viết lại hoàn toàn bằng câu chữ mới; không chép câu, tiêu đề hay ví dụ đặc trưng của họ.

**Chuẩn chung cho cả viết lại lẫn viết mới** (người dùng đã duyệt ngày 21/11/2026): mở bài theo công thức bảy nhịp ở mục 4, thân bài theo "Giọng thân bài: khẳng định, không rào đón", kết bài gọi lại câu cách ngôn. Bản mẫu đã duyệt nằm ở [approved-sample.md](references/approved-sample.md): đọc nó trước khi viết câu đầu tiên của bất kỳ kịch bản nào, và đối chiếu giọng mỗi cụm vừa viết với nó. Chạy mục "GIONG ABOOKS" của script (mục 11) sau mỗi cụm.

**Duyệt mở bài trước:** viết xong mở bài (khoảng 3.000–4.500 ký tự đầu, đến hết lời hứa), gửi người dùng xem và chờ một lời "đúng hướng" rồi mới viết tiếp phần còn lại. Áp dụng cho cả hai chế độ.

Biến một kịch bản nguồn thành một kịch bản video YouTube mới, dài, liền mạch, đúng giọng Abooks, đọc được ngay bằng TTS tiếng Việt. Mọi dữ kiện đều phải thật: dữ kiện trong bản nguồn được kiểm chứng, phần bổ sung lấy từ tác phẩm thật của tác giả và có nguồn xác minh.

## 1. Đầu vào và mặc định

Đầu vào: một hay nhiều file kịch bản (thường là `.txt` phụ đề tự động tải từ DownSub, mỗi dòng vài chữ, không chấm câu chuẩn, nhiều lỗi nghe nhầm), hoặc nội dung dán trong chat.

Mặc định, không hỏi lại:

- Độ dài: 50.000–60.000 ký tự, nhắm 55.000. Nếu người dùng nêu một con số, dùng con số đó với dải ±4%.
- Ký tự được đếm gồm cả khoảng trắng và xuống dòng của file cuối, dạng Unicode NFC.
- Giọng: người dẫn review (mục 3).
- Tra cứu: kiểm chứng và bổ sung có nguồn (mục 6).
- Không có câu cố định của kênh, không kêu gọi like, đăng ký hay mua sách.
- Đầu ra: một file TXT liền mạch, chia đoạn bằng một dòng trống, không heading.
- Gói SEO YouTube đi kèm: phân tích tiêu đề và từ khóa của bản nguồn, 3 tiêu đề, mô tả, hashtag, 10 tag (mục 12), lưu thành một file riêng.

Chỉ hỏi khi thiếu nguồn hoặc nguồn không đọc được. Nếu người dùng chỉ đưa tên sách hay chủ đề mà không có kịch bản, nói rõ sẽ dựng từ tra cứu, rồi chạy cùng quy trình với phần tra cứu làm nguồn chính.

## 2. Chuẩn bị nguồn

1. Ghép dòng phụ đề: bỏ `[âm nhạc]`, `>>`, nối các dòng thành văn bản liền. Script kiểm tra ở mục 11 có cờ `--asr` làm việc này khi đếm.
2. Đọc TOÀN BỘ nguồn trước khi viết câu đầu tiên. Không đoán nội dung từ tên file. File dài thì đọc tuần tự đến dòng cuối.
3. Sửa lỗi nghe nhầm khi hiểu nguồn. Phụ đề tự động hay lẫn d/gi/r, ch/tr, s/x, dấu hỏi/ngã, và nghe sai tên riêng. Ví dụ đã gặp: gốc dễ → gốc rễ, chớ trêu → trớ trêu, rằng xé → giằng xé, trai sạn → chai sạn, tiền xử → tiền sử, vô chi → vô tri, ve phái → bè phái, dượt đuổi → rượt đuổi, mổ sẻ → mổ xẻ, chiết gia → triết gia, danh giới → ranh giới, trần trừ → chần chừ, lời chăn trối → lời trăn trối, nhen anh múa vuốt → nhe nanh múa vuốt, trường truyền → trường chuyên, đèn chùa → đền chùa, trễm trệ → chễm chệ, già soát → rà soát, xuyên ngẫm → suy ngẫm, Minh Hoàng nhà Hán → Hán Minh Đế, Maulingaputta → Malunkyaputta. Tên riêng nghe nhầm phải tra cứu để sửa, không đoán.
4. Bỏ hẳn phần quảng cáo kênh của nguồn ("Bạn đang nghe…", "Trước khi vào bản review…", lời mời bình luận). Phần này không tính là nội dung.
5. Lấy tiêu đề gốc của video nguồn theo mục 12.2.

## 3. Giọng kể: người dẫn review

Người dẫn là "tôi" của kênh, nói với "bạn", gần gũi nhưng dứt khoát: người đã đọc kỹ cuốn sách và nói thẳng điều mình thấy, không giảng giải dài dòng, không kể lể. Người dẫn KHÔNG phải tác giả.

- Gọi tác giả ở ngôi thứ ba: "Krishnamurti", "ông", "Osho", "Đức Phật", "Ngài". Không gắn tên tác giả vào mọi câu; một khối ý chỉ cần nêu một hai lần cho rõ quan điểm của ai.
- Các bản nguồn thường nhập vai tác giả. Khi viết lại, chuyển hết sang lời dẫn:
  - "Tôi không phải là thầy của các bạn" → "Krishnamurti luôn từ chối vai trò người thầy. Ông muốn người nghe ngồi ngang hàng với mình…"
  - Chuyện đời tác giả kể ở ngôi thứ nhất → "Osho kể lại một đêm tháng ba năm 1953…" (sau khi đã kiểm chứng ngày và chi tiết).
  - "Vài ngày trước tôi trò chuyện với các chuyên gia máy tính" → "Những năm cuối đời, Krishnamurti nhiều lần bàn về máy tính và trí tuệ nhân tạo…" (chỉ khi tra cứu xác nhận).
- Không bao giờ để người dẫn nhận trải nghiệm của tác giả, hay để tác giả bình luận về Việt Nam ("Ở mảnh đất này, tôi thấy…"). Người dẫn có thể tự nói về đời sống Việt Nam bằng giọng của mình.
- Lời trực tiếp của tác giả chỉ dùng khi đã tìm thấy câu đó ở nguồn đáng tin, giữ ngắn (một câu, dưới mười lăm chữ) và tối đa một lần cho mỗi nguồn. Còn lại thuật ý: "ông nói đại ý rằng…", "theo cách nhìn của ông…". Không đặt lời diễn giải trong ngoặc kép như thể là trích dẫn.
- Người dẫn dùng các động tác thân mật một cách tiết kiệm: "Hãy cùng tôi nhìn kỹ…", "Bạn có thấy không?", "Thưa bạn…", "Tôi muốn mời bạn làm một thí nghiệm nhỏ…". Tổng cộng tối đa 3–4 lần cả bài; còn lại để câu khẳng định và câu hỏi tu từ làm việc. Đó là lời mời quan sát, không phải giảng đạo.
- Rào đón kiểu "Krishnamurti cho rằng…", "theo cách nhìn của ông…", "ông nói đại ý rằng…": mỗi khối ý một lần là đủ để rõ ý của ai. Mở nhiều đoạn liên tiếp bằng tên tác giả là dấu hiệu bài đang thành bài giảng (script đếm ở mục "GIONG ABOOKS").

## 4. ADN văn phong Abooks (rút từ các kịch bản mẫu)

### Không khí

Một cuộc cùng nhau điều tra, có sức đẩy: không ai đứng trên ai, không trao công thức, nhưng câu chữ dứt khoát và giàu hình ảnh. Hình ảnh khung (tách trà, băng ghế, chuyến tàu, sân ga) là tùy chọn; thứ bắt buộc gọi lại ở kết bài là **câu cách ngôn mở đầu**, với nghĩa mới.

### Mở bài (khoảng 6–9% độ dài, 3.000–4.500 ký tự): công thức mặc định

Người dùng đã duyệt công thức này sau khi chê một bản mở bằng cảnh "kéo ghế, tách trà" là chậm và chán (ngày 21/11/2026). Đây là cách các video Abooks và BBooks nhiều view thật sự mở bài. Không chào kênh, không "Hôm nay chúng ta sẽ", không "Trong video này". Đi đúng bảy nhịp:

1. **Câu cách ngôn đứng riêng một đoạn**: 1–2 câu ngắn, nghịch lý, đọc lên muốn nhớ, chưa nhắc sách. Ví dụ đã duyệt: "Nhà tù chắc chắn nhất không được xây bằng gạch đá. Nó được xây bằng những gì ta tin rằng mình đã biết." (mẫu BBooks: "Tự do không ở cuối con đường mà hiện hữu trong từng bước đi.")
2. **Cuốn sách như một vật thể**: "Có những cuốn sách…" hay "Nằm trong tay tôi…", nêu tên gốc, tên Việt, rồi tả bằng chuỗi phủ định ba nhịp ngắn ("Nó không trao thêm kiến thức. Nó lấy bớt đi. Nó không vẽ đường. Nó xóa bản đồ.") và một so sánh (tấm gương không khung, không chỗ trốn).
3. **Những gì tấm gương ấy cho thấy**: 2–3 câu "Thấy nỗi sợ nằm ngay trong lòng tình yêu…".
4. **Chân dung tác giả bằng một nghịch lý có thật** (đã kiểm), kèm năm, người biên tập, bối cảnh của sách.
5. **Chuỗi đối lập về cách ta đang sống**, cùng một khuôn câu: "Ta đi tìm… nhưng lại… Ta đi tìm… nhưng lại…", rồi dồn vào một câu hỏi lớn đứng riêng ("Vì sao biết nhiều đến thế, mà lòng vẫn không yên?").
6. **Cái giá phải trả**: "Điều đáng sợ nhất không phải là… Điều đáng sợ nhất là…", rồi 2–3 câu hỏi treo.
7. **Lời hứa bằng hình ảnh**: không hệ thống, không nghi lễ, chỉ một lời mời; liệt kê ngắn chặng đường sắp đi; câu chốt ngắn ("Không có gì để tin. Chỉ có điều để thấy."). Rồi vào thẳng khối đầu.

Mở bằng cảnh "kéo ghế ngồi xuống, tách trà" chỉ dùng khi người dùng yêu cầu; nếu có hình ảnh khung thì đặt nó sau câu cách ngôn, không thay câu cách ngôn.

### Giọng thân bài: khẳng định, không rào đón

Cũng từ lần góp ý ấy: bản bị chê vì câu nào cũng bắt đầu bằng "Krishnamurti cho rằng…", "theo cách nhìn của ông…", nghe như bài giảng. Cách sửa đã duyệt:

- Mỗi khối ý nêu quan điểm là của ai **một lần** ở đầu khối, sau đó người dẫn nói thẳng ý ấy như một sự thật đang cùng người nghe nhìn thấy: "Hiểu biết là quá khứ." chứ không phải "Krishnamurti cho rằng hiểu biết là quá khứ."
- Nhịp nhanh: nhiều câu khẳng định ngắn, chuỗi ba nhịp, đối lập song song, câu một hai chữ đóng ý. Xen câu dài để thở, nhưng không để quá hai câu dài liền nhau.
- Giai thoại kể gọn như một cảnh phim, thoại ngắn, rồi rút ý bằng 2–4 câu, không giảng lại câu chuyện.
- Hạn chế các động tác trò chuyện kéo dài ("Tôi muốn mời bạn làm một thí nghiệm nhỏ…", "Thưa bạn…"): tối đa 3–4 lần cả bài.
- Câu trung bình 13–17 từ là đạt với giọng này (thấp hơn mức 15–20 ở mục Nhịp bên dưới cũng được).

### Thân bài: chuỗi khối ý

Mỗi khối ý có một chức năng mới và thường đi theo nhịp:

1. Câu nối nhận sợi ý từ khối trước, có khi tóm một câu: "Chúng ta vừa thấy… Nhưng…".
2. Đặt vấn đề bằng câu hỏi hoặc mệnh đề gây chú ý.
3. Cảnh đời thường Việt Nam, giàu chi tiết giác quan: chuông báo thức và cảm giác bồn chồn, xe tạt đầu, kẹt xe ngã tư, ánh mắt của sếp, tiền nhà tháng tới, người bạn cũ vừa mua nhà, mâm cao cỗ đầy ngày rằm, vàng mã, xin xăm, cúng sao giải hạn, xem ngày xuất hành, trường chuyên lớp chọn, biên chế, ma chay hiếu hỉ, bỏ phố về rừng, khóa thiền mười ngày nộp điện thoại, lướt điện thoại lúc vừa mở mắt, đài tụng kinh mở suốt ngày. Đây là cảnh giả định, mở bằng "Hãy thử nhìn…", "Giả sử…", "Có thể bạn từng…", không gán tên người, ngày, địa điểm cụ thể như sự kiện thật.
4. Bóc tách cơ chế từng bước, chậm: "Hãy nhìn thật kỹ…", bước một, bước hai, bước ba; có khi gói thành một công thức nói được, ví dụ cảm giác cộng với tư duy thành ham muốn.
5. Một ẩn dụ hay so sánh đắt: con rắn độc dưới chân, tấm gương phủ bụi, mặt hồ in trăng, cái gai trong bàn chân, chiếc ba lô nặng như chì, căn gác xép chưa dọn, đứa trẻ nín khóc vì món đồ chơi, ngọn đèn rọi vào góc tối. Ưu tiên ẩn dụ chính tác giả từng dùng (đã kiểm chứng); ẩn dụ mới phải phục vụ đúng luận điểm.
6. Phản biện thay người nghe: "Bạn sẽ nói với tôi rằng…", "Nhưng làm thế nào?", rồi lật lại phản biện đó.
7. Câu ngắn đóng ý: "Không.", "Hoàn toàn không.", "Đó là một ảo tưởng.", "Cái thấy và cái hành động là một."
8. Câu móc sang khối sau, thường là câu hỏi treo: "…Vậy tại sao sự phân chia lại là gốc rễ của bạo lực?", "Thứ đó chính là ham muốn. Nó vận hành thế nào?"

Giai thoại và ngụ ngôn: khoảng một câu chuyện cho mỗi 5.000–8.000 ký tự (kho chuyện đã kiểm xuất xứ: [anecdotes.md](references/anecdotes.md)), kể như một cảnh nhỏ có thoại ngắn, rồi rút ý. Chuyện phải thật trong kho chuyện của tác giả hay truyền thống (đã kiểm chứng xuất xứ), hoặc nói rõ là giả định.

**Thứ tự ưu tiên nguồn giai thoại** (người dùng chốt 21/11/2026, theo các video mẫu):
1. Thế giới của chính tác giả: người hỏi và câu trả lời trong các buổi nói chuyện, hỏi đáp có ghi chép (với Krishnamurti: các bản ghi "public questions", "public discussion" trên kfoundation.org; các cuộc gặp trong Commentaries on Living; đối thoại với Bohm, Pupul Jayakar, học sinh), những khoảnh khắc trong đời tác giả (đã kiểm). Với Osho: những chuyện chính Osho hay kể trong bài giảng (ghi rõ "Osho kể…"). Với Phật học: chuyện trong chính bộ kinh đang bàn.
2. Truyền thống gần gũi (truyện Thiền, kinh Phật khác): xen tối đa 1–2 lần mỗi bài, đặt ở chỗ cần một cú lật.
3. Cảnh đời thường Việt Nam giả định: dùng tự do, luôn rõ là giả định.

### Động cơ triển khai học từ video mẫu (dùng trong giọng người dẫn)

Phân tích 7 video ở [sample-analysis.md](references/sample-analysis.md), mục 0. Các video nhiều view nhất giữ người nghe suốt một tiếng nhờ những động cơ sau; skill dùng chúng trong giọng người dẫn ngôi thứ ba (không nhập vai):

- **Dựng cảnh trước, giảng ý sau.** Mở một chặng bằng một cảnh có thật: năm, nơi, khung cảnh, ai đang hỏi ai ("Mùa đông năm 1985, ở Rishi Valley…", "Một buổi sáng ở Saanen, một người đàn ông đứng lên hỏi…"). Chỉ dùng chi tiết có trong Fact Ledger.
- **Người hỏi và câu trả lời**, khoảng mỗi 6.000–9.000 ký tự một lần: kể câu hỏi bằng giọng người hỏi (ngắn, đời thường), câu trả lời của tác giả thuật ý ở ngôi thứ ba, gọn và giàu hình ảnh, rồi người dẫn rút ý trong 2–3 câu.
- **Chuyển chặng nối xích**: chặng sau mọc ra từ câu hỏi treo của chặng trước ("Nhưng nếu ký ức đứng chắn ở cửa, thì cái gì đang canh cửa?"), không chuyển bằng "tiếp theo, chúng ta sẽ bàn về…".
- **Leo thang**: mỗi chặng đánh vào một ảo tưởng sâu hơn chặng trước; báo trước bằng một câu ("Điều khó nghe nhất vẫn còn ở phía trước").
- **Móc thời sự và đời thường Việt Nam**: mạng xã hội, khóa học chữa lành, AI, khóa thiền nộp điện thoại, áp lực trường chuyên, nhóm chat chung cư. Mỗi chặng ít nhất một cảnh như vậy.
- **Người dẫn lùi ra ở kết** ("Gấp lại những trang cuối…"), tổng kết bằng nghịch lý, câu hỏi treo, "Đừng vội trả lời".

Có thể dùng tối đa sáu "câu đề mục nói thành lời": một câu ngắn giàu hình ảnh đứng riêng một đoạn để mở một chặng lớn (kiểu "Kẻ đã tự chặt đầu mình từ trước."). Không đánh số, không dấu hai chấm, phải đọc lên tự nhiên.

### Kết bài (khoảng 8–10% độ dài)

1. Tổng duyệt hành trình trong một đoạn có hình ảnh, không liệt kê khô.
2. Câu hỏi cuối cùng được nâng lên: vì sao không thể đợi đến ngày mai.
3. Một câu chuyện vui hay ngụ ngôn có cú lật (ba đạo sĩ ngồi thiền ba mươi năm, người vừa lên thiên đàng vẫn thấy khổ…), rồi giải nghĩa ngắn.
4. Lời chia tay: chuyến tàu dừng ở sân ga này; đừng biến những lời này thành niềm tin mới; bạn là người thầy, là cuốn sách của chính mình.
5. Câu cuối mời tĩnh lặng hoặc quan sát, gọi lại câu cách ngôn mở đầu (và hình ảnh khung nếu có). Thêm "Đừng vội trả lời…" trước câu cuối khi hợp. Không kêu gọi thương mại.

### Từ vựng và xưng hô

- Xưng "tôi" (người dẫn), gọi "bạn", "các bạn", thỉnh thoảng "thưa bạn", "này bạn", "bạn của tôi". Dùng "chúng ta" khi cùng quan sát.
- Từ khóa theo tác giả, chỉ dùng khi đúng với tác giả đó. Krishnamurti: cái đang là, người quan sát chính là cái bị quan sát, thời gian tâm lý, tư duy là thời gian, sự chú tâm trọn vẹn, nhìn mà không chọn lựa, đột biến trong tế bào não, tuệ giác, chân lý là vùng đất không lối mòn. Osho: thiền là quan sát, nhân chứng, vô ngã, sự hiện diện, hiện tại, buông. Phật học: vô ngã, khổ, tham sân si, chánh niệm, bát chánh đạo, dùng đúng thuật ngữ Hán Việt thông dụng.

### Nhịp (đo trên các mẫu)

- Câu trung bình 13–17 từ (bản đã duyệt: 13,6; các video Abooks gắt: 15–16). Câu trên 30 từ không quá 10%. Không câu nào trên 45 từ.
- Có nhịp ngắn: câu từ 5 từ trở xuống chiếm khoảng 8–15% số câu (bản đã duyệt: 12,7%), dùng để đóng ý, không dùng thành chuỗi dài.
- Câu hỏi chiếm khoảng 8–14% số câu, không quá ba câu hỏi liên tiếp, trừ chuỗi câu hỏi có chủ đích ở mở bài và kết bài.
- Đoạn 2–6 câu, độ dài thay đổi. Đôi khi một câu ngắn đứng riêng thành đoạn để nghỉ, nhưng không chuỗi dài đoạn một câu.
- Không mở nhiều đoạn liền nhau bằng cùng một cụm ("Hãy…", "Bạn có…", "Và…").

### Điều cần tránh

- Lặp "Hãy tưởng tượng" ở các đoạn gần nhau. Lặp "Điều này không có nghĩa là". Lạm dụng "chính là", "thực chất".
- Câu triết lý rỗng không gắn với luận điểm nào.
- Liệt kê mẹo, gạch đầu dòng, giọng sách tự lực.
- Phần giữa chỉ giảng giải đều đều, thiếu cảnh, tương phản hay bước ngoặt.
- Mở bài chậm: cảnh mời ngồi, tả không gian, kể lể vì sao chọn cuốn sách trước khi có câu móc. Ba câu đầu phải khiến người nghe muốn nghe câu thứ tư.
- Đoạn nào cũng bắt đầu bằng tên tác giả hoặc "ông cho rằng". Kể giai thoại rồi giảng lại nó dài hơn chính câu chuyện.
- Lời khẳng định y khoa, thần kinh học, "chữa lành" chắc chắn.

## 5. Tác vụ và tệp làm việc

Tạo task list cho các chặng: Chuẩn bị nguồn, Source Bible, Phân tích SEO bản nguồn, Tra cứu, Dàn ý và ngân sách, Viết theo cụm, Kiểm định, Chỉnh độ dài, TTS, Gói SEO, Xuất file.

Thư mục làm việc `D:\youtubeclaude\abooks\<ten-ngan-khong-dau>\work\` (kịch bản Krishnamurti cũ nằm ở `D:\youtubeclaude\krishnamurti\`):

- `source_joined.txt`: nguồn đã ghép dòng và sửa lỗi nghe nhầm.
- `bible.md`: Source Bible, Fact Ledger, Narrative Bible, ngân sách, sổ chống lặp.
- `part01.txt`, `part02.txt`…: từng cụm đã viết.
- Script kiểm tra dùng trực tiếp từ `scripts/abooks_check.py` của skill (mục 11).
- `seo.txt`: gói SEO theo định dạng mục 12.7.

Bài dài phải ghi ra file từng cụm. Nếu phiên bị ngắt, đọc lại `bible.md` và cụm cuối rồi viết tiếp, không viết lại từ đầu.

## 6. Quy trình

### Bước 1: Source Bible

Ghi vào `bible.md`:

- Tác giả, tác phẩm, bài nói (ngày, nơi chốn nếu nguồn nêu), thể loại nguồn.
- Luận đề trung tâm trong một câu.
- Tiến trình lập luận đầy đủ theo thứ tự.
- Luận điểm chính (mỗi cái có mã C1, C2…) và luận điểm phụ.
- Ví dụ, giai thoại, ẩn dụ của nguồn.
- Ranh giới và sắc thái phải giữ (điều gì là "có thể", điều gì tác giả tránh khẳng định).
- Danh sách mọi câu có dáng dữ kiện: tên người, năm, số liệu, giai thoại lịch sử, trích dẫn, tên sách, khẳng định khoa học.

### Bước 1b: Phân tích tiêu đề và từ khóa bản nguồn

Làm theo mục 12.2 và ghi kết quả vào `bible.md`. Bộ từ khóa chốt ở bước này dẫn đường cho cả kịch bản lẫn gói SEO.

### Bước 2: Tra cứu và Fact Ledger

Dùng WebSearch (chế độ standard trước, extended khi cần chi tiết hiếm) và WebFetch để đọc trang gốc. Truy vấn bằng cả tiếng Anh và tiếng Việt; tên tác phẩm tiếng Anh thường cho kết quả tốt hơn. Gửi các truy vấn độc lập trong cùng một lượt. Thường cần 15–30 lượt tra cứu.

Thứ bậc nguồn:

1. Nguồn chính thức và văn bản gốc: jkrishnamurti.org và kfoundation.org (Krishnamurti), osho.com (Osho), suttacentral.net và accesstoinsight.org (kinh Pali), thuvienhoasen.org và budsas.org (bản dịch Phật học tiếng Việt), trang nhà xuất bản, sách điện tử chính thức.
2. Học thuật và bách khoa: Britannica, Stanford Encyclopedia of Philosophy, bài báo học thuật, báo chí uy tín.
3. Wikipedia: dùng để định hướng, phải đối chiếu với bậc 1 hoặc 2 cho dữ kiện quan trọng.
4. Trang trích dẫn, blog, video khác: không đủ để xác nhận. Rất nhiều câu "trích dẫn" gán cho Krishnamurti, Osho, Đức Phật trên mạng là giả.

Mỗi dữ kiện trong nguồn nhận một trạng thái trong Fact Ledger, kèm URL:

- ĐÚNG: giữ.
- SỬA: nguồn sai (tên, năm, con số, người trong chuyện). Viết theo dữ kiện đúng. Ví dụ loại lỗi hay gặp: phóng đại thời gian ("hai nghìn năm chưa ai bác bỏ" cho một bài luận thế kỷ hai mươi), nhầm nhân vật trong giai thoại, sai niên hiệu.
- THEO LỜI KỂ: giai thoại, truyền thuyết hay chuyện chỉ có trong lời giảng của tác giả, không phải sử liệu. Giữ, nhưng đóng khung: "Osho kể rằng…", "tương truyền…", "trong một bài giảng, Osho thuật lại…".
- KHÔNG XÁC MINH ĐƯỢC: bỏ, hoặc làm mềm thành câu hỏi hay tình huống giả định. Không dùng kiến thức sẵn có để "hợp thức hóa".

Khẳng định khoa học (tiến hóa, não bộ, dopamine…) giữ ở mức thận trọng và đúng: "hơn hai triệu năm" thay vì một con số chính xác giả, "có thể", "nhiều nhà nghiên cứu cho rằng" khi đúng là vậy. Không đưa lời hứa y khoa.

Chất liệu bổ sung: để đạt 50.000–60.000 ký tự mà không lặp, tìm 8–15 chất liệu thật nằm đúng trục luận đề, ghi vào ledger với URL và đánh dấu BỔ SUNG:

- Bối cảnh thật của tác phẩm hay bài nói (thời gian, nơi chốn, người đối thoại).
- Ý liên quan từ các bài nói hay sách khác của chính tác giả, càng gần chủ đề càng tốt.
- Ẩn dụ, ví dụ, giai thoại mà chính tác giả hay truyền thống ấy dùng.
- Khái niệm nền mà người nghe cần để hiểu (giải nghĩa ngắn, chính xác).

Không thêm chất liệu làm lệch hay đảo luận đề. Thuật ý bằng lời của mình, không chép đoạn văn. Ghi rõ nguồn của từng chất liệu trong ledger để báo cáo cuối.

### Bước 3: Narrative Bible và ngân sách

Ghi vào `bible.md`:

- Câu hỏi trung tâm xuyên suốt bài; mỗi khối làm nó sâu thêm, rẽ hướng hoặc tiến gần lời đáp.
- Kiểu mở bài, hình ảnh khung, ẩn dụ trung tâm nếu có.
- Vị trí từ khóa: tên tác giả và từ khóa chính xuất hiện tự nhiên trong khoảng 1.000 ký tự đầu; mở bài cho người nghe thấy ngay vì sao chủ đề trong tiêu đề đáng nghe; mỗi từ khóa phụ được giao cho khối ý bàn về nó. Không nhồi từ khóa, không câu gượng.
- Mạch cảm xúc: nhận diện → căng thẳng, đào sâu → bước ngoặt nhận thức → tích hợp vào đời sống → hội tụ → dư âm.
- Mạch mặc định, co giãn theo nguồn, không đảo tiến trình lập luận nếu làm đổi nghĩa: nghịch lý → biểu hiện đời sống → cơ chế → hiểu lầm phổ biến → hệ quả → bước ngoặt → sống với điều đó → hội tụ → gọi lại mở bài.
- Danh sách 8–12 khối ý. Mỗi khối: mục đích, mã luận điểm nguồn, mã chất liệu bổ sung, động tác nhận thức mới, cảnh đời thường dự kiến, giai thoại dự kiến, câu nối vào, câu móc ra, ngân sách ký tự min/target/max.
- Ngân sách (mẫu cho 55.000): mở 4.500–5.500; mỗi khối thân 3.500–6.500 theo trọng lượng luận điểm, không chia đều máy móc; kết 4.500–5.500. Tổng target của các khối bằng target toàn bài.
- Mỗi luận điểm chính phải có ít nhất một khối. Mỗi motif khi quay lại phải đổi vai trò: lần đầu nhận diện, lần giữa giải thích cơ chế hoặc bước ngoặt, lần cuối hội tụ.

### Bước 4: Viết theo cụm

- Cụm đầu tiên là mở bài (theo bảy nhịp ở mục 4) cộng khối ý đầu. Gửi riêng phần mở bài cho người dùng duyệt trước khi viết các cụm sau (xem mục 0).
- Mỗi lượt viết 2–3 khối liền nhau (khoảng 8.000–15.000 ký tự), ghi bằng Write vào `partNN.txt`. Nội dung do chính mình viết; không dùng script hay API để sinh văn bản.
- Trước mỗi cụm, đọc lại một đoạn thân bài trong [approved-sample.md](references/approved-sample.md) để giữ đúng nhịp; sau mỗi cụm chạy script với `--min 1` để xem mục "GIONG ABOOKS" của riêng cụm ấy.
- Viết lại hoàn toàn bằng câu chữ mới. Giữ ý, giữ ẩn dụ và giai thoại đã kiểm chứng của tác giả, nhưng không bám câu chữ của bản nguồn. Đổi thứ tự cảnh minh họa, đổi chi tiết đời thường, phát triển sâu hơn.
- Sau mỗi cụm, cập nhật sổ trong `bible.md`: luận điểm và chất liệu đã dùng, cảnh và ví dụ đã dùng, giai thoại đã dùng, motif, câu hỏi treo, các cụm từ đã dùng nhiều, số ký tự hiện tại (đếm bằng `wc -m` hoặc script).
- Trước cụm tiếp theo, đọc lại đoạn cuối cụm trước và sổ chống lặp.

### Bước 5: Kiểm định

Ghép các phần bằng thao tác cơ học (`cat part*.txt`, mỗi phần cách nhau một dòng trống) thành bản nháp, rồi chạy script mục 11 với `--source source_joined.txt`.

Kiểm theo thứ tự, sửa đúng vùng lỗi bằng Edit, không viết lại cả bài:

1. Dữ kiện: mọi câu có dáng dữ kiện truy được về Fact Ledger (ĐÚNG, SỬA, THEO LỜI KỂ hoặc BỔ SUNG). Không còn mục KHÔNG XÁC MINH nào lọt vào.
2. Giọng: không còn câu nào để người dẫn nói như tác giả, không trích dẫn chưa kiểm chứng, không lời diễn giải đặt trong ngoặc kép.
3. Lặp theo nghĩa: hai đoạn chữ khác nhau nhưng nói cùng một ý cũng là lặp. Chỉ giữ khi lần sau có chức năng mới. Script báo cụm tám chữ lặp lại và các cụm quen tay.
4. Trùng với bản nguồn: tỉ lệ cụm tám chữ trùng dưới 5%. Cao hơn thì viết lại những đoạn bám sát.
5. Văn phong Abooks: mỗi khối có cảnh, cơ chế, phản biện hoặc bước ngoặt; phần giữa không giảng giải đều đều; mở bài nối đúng luận đề; kết bài gọi lại hình ảnh khung với nghĩa mới.

### Bước 6: Chỉnh độ dài

- Dưới mức tối thiểu: tính số ký tự thiếu, tìm luận điểm và chất liệu bổ sung chưa khai thác hết, chia phần thiếu cho nhiều khối, mở rộng có mục tiêu bằng: giải nghĩa sâu hơn, phân biệt hai khái niệm, nguyên nhân và hệ quả, cảnh đời thường giả định mới, phản biện của người nghe, giai thoại đã kiểm chứng, cầu nối. Nếu hết chất liệu, quay lại Bước 2 tra thêm. Sau đó chạy lại kiểm định và đếm lại.
- Trên mức tối đa: cắt lặp ý, giải thích vòng vo, ví dụ thứ hai cho cùng ý, câu chuyển thừa. Giữ câu mang luận điểm, bước ngoặt, motif có chức năng, mở bài và kết bài.
- Nếu không thể đạt độ dài mà không lặp hay bịa, dừng và báo con số tối đa an toàn cùng lý do. Không gọi là hoàn thành.

### Bước 7: Chuẩn TTS

- Chỉ nội dung để đọc thành tiếng: không Markdown, heading, gạch đầu dòng, bảng, emoji, URL, ghi chú biên tập, nhãn kỹ thuật.
- Không ký hiệu `% & @ = < > / # *`, không `...` hay `…`, không `!!` `??`, không ngoặc đơn dài, không gạch chéo kiểu "và/hoặc".
- Số đếm nhỏ viết bằng chữ ("ba câu hỏi", "hai triệu năm", "một phần mười giây"). Năm bốn chữ số có thể giữ chữ số ("năm 1953"). Ngày tháng viết "ngày hai mươi mốt tháng ba năm 1953", không viết "21/3".
- Tên riêng viết một cách thống nhất toàn bài. Tên Việt hóa thông dụng giữ dạng Việt (Đức Phật, Tất Đạt Đa, Lão Tử, Trang Tử, Xá Lợi Phất khi phù hợp); tên phương Tây giữ nguyên chữ (Krishnamurti, Osho, Bertrand Russell). Không tự thêm phiên âm.
- Tách câu trên 30 từ khi nhịp khó lấy hơi hay mất chủ ngữ. Không câu trên 45 từ.
- Không còn cụm nội bộ: "nguồn nói", "theo nguồn", "trong nguồn", "bản gốc", "kịch bản gốc", hay câu cố định của kênh.
- Đọc mô phỏng mở bài, một đoạn giữa, mọi tên riêng và kết bài. Lưu UTF-8, NFC.

### Bước 8: Gói SEO YouTube

Sau khi kịch bản đã qua Bước 7, làm theo mục 12.3 đến 12.7: ba tiêu đề, mô tả, hashtag, mười tag, ghi vào `work/seo.txt`. Mọi dữ kiện trong tiêu đề và mô tả phải có trong Fact Ledger; mọi lời hứa trong tiêu đề phải được kịch bản trả lời. Chạy script trên bản kịch bản cuối với `--seo work/seo.txt --keywords "<từ khóa chính>,<từ khóa phụ>"` để kiểm độ dài và vị trí từ khóa.

### Bước 9: Xuất và báo cáo

- Tên file: `[ten-ngan-khong-dau]_abooks_[so-ky-tu].txt` trong `D:\youtubeclaude\abooks\<ten-ngan-khong-dau>\` (không commit, trừ khi người dùng bảo). Đã có thì thêm `_2`, `_3`.
- Chạy script lần cuối trên đúng file xuất; mọi cổng ở mục 8 phải đạt.
- Chép `work/seo.txt` thành `[ten-ngan-khong-dau]_abooks_seo.txt` trong cùng thư mục xuất.
- Gửi cả hai file bằng SendUserFile. Không dán toàn bộ kịch bản vào chat. Gói SEO ngắn nên dán luôn vào chat để người dùng chép ngay.
- Báo cáo ngắn trong chat:
  - Số ký tự (có khoảng trắng), số từ, ước lượng thời lượng đọc.
  - Tỉ lệ trùng với bản nguồn.
  - Những dữ kiện đã SỬA so với bản nguồn, mỗi mục một dòng.
  - Những chất liệu BỔ SUNG chính.
  - Gói SEO: phân tích ngắn tiêu đề và từ khóa của bản nguồn, 3 tiêu đề kèm số ký tự và điểm, mô tả, hashtag, 10 tag.
  - Mục "Nguồn:" liệt kê các trang đã dùng dạng [Tiêu đề](URL).

## 7. Luật cứng

1. Không viết trước khi đọc hết nguồn.
2. Không có dữ kiện nào không truy được về Fact Ledger. Không bịa tên, năm, số liệu, nghiên cứu, sách, giai thoại, trích dẫn.
3. Người dẫn không nhập vai tác giả.
4. Ví dụ mới phải rõ là giả định.
5. Không kéo dài bằng cách diễn đạt lại cùng ý.
6. Không chép đoạn văn từ bản nguồn hay từ trang tra cứu; trích dẫn trực tiếp chỉ một câu ngắn đã kiểm chứng.
7. Không gọi hoàn thành khi ngoài dải độ dài.
8. Không hy sinh độ chính xác để đạt độ dài.
9. Không dán kịch bản dài vào chat; đầu ra là một file TXT.
10. Không làm lệch, phóng đại hay đổi sắc thái luận đề: "có thể" không thành "chắc chắn", "gợi ý" không thành "chứng minh".
11. Tiêu đề, mô tả, hashtag và tag không hứa điều kịch bản không trả lời, không chứa dữ kiện ngoài Fact Ledger, không dùng tên kênh khác, không chép nguyên tiêu đề của video khác. Tên kênh của người dùng chỉ đưa vào khi người dùng đã cho biết.

## 8. Thang chất lượng

Cổng bắt buộc: đã đọc hết nguồn; luận điểm chính phủ 100%; dữ kiện không xác minh 0; nhập vai tác giả 0; giả định không đánh dấu 0; cụm nội bộ và câu cố định 0; lặp ý nghiêm trọng 0; trùng bản nguồn dưới 5%; độ dài trong dải; mở bài nối luận đề; kết bài gọi lại mở bài.

Điểm tối thiểu: chính xác dữ kiện 9/10, giữ nghĩa 9/10, giọng Abooks 8/10, mạch lạc 8/10, không lặp 8/10, dễ đọc thành tiếng 8/10. Chính xác và giữ nghĩa là cổng phủ quyết; điểm văn phong cao không bù được lỗi dữ kiện.

Câu hỏi cuối trước khi xuất:

1. Nếu không thấy chỗ ngắt chặng, người nghe có vẫn theo được mạch không?
2. Mỗi khối có thêm một chuyển động mới không?
3. Có chỗ nào người dẫn vô tình nói như tác giả không?
4. Có câu nào nghe như dữ kiện mà không có trong ledger không?
5. Có ví dụ giả định nào dễ bị hiểu là chuyện có thật không?
6. Phần giữa có đều đều và giảng quá lâu không?
7. Kết có quay lại mở bài với nghĩa mới không?

## 9. Bài học đã rút

- Đọc hết nguồn rồi mới viết giữ luận đề tốt hơn vừa đọc vừa viết.
- Viết liên tục trong một mạch tạo chuyển tiếp tự nhiên hơn các đoạn rời.
- Đủ số ký tự không có nghĩa là đạt; phải kiểm lặp theo nghĩa.
- Mở rộng an toàn nhất: giải nghĩa, phân biệt, hệ quả, cảnh giả định, chất liệu thật đã tra cứu.
- Câu hỏi trung tâm phải sống suốt bài, không chỉ ở mở và kết.
- Khi sửa cuối, vá đúng vùng lỗi; viết lại cả bài dễ phá độ chính xác và độ dài.
- Bản nguồn thường đã nhập vai tác giả và có dữ kiện sai hoặc phóng đại; kiểm chứng trước khi viết sẽ đỡ phải sửa ngược.
- Ở các video mẫu, từ khóa của tiêu đề thường xuất hiện muộn trong kịch bản (có bài ở 58%, có bài ở 91% độ dài) và tên tác giả gần như không được nhắc vì người kể nhập vai. Bản viết lại nêu tên tác giả và từ khóa chính ngay ở mở bài để tiêu đề và nội dung khớp nhau.

- (21/11/2026) Mở bằng cảnh mời ngồi xuống, tách trà, rồi giảng giải với "Krishnamurti cho rằng…" ở mọi đoạn bị người dùng chê là chán ngay từ đầu. Mở bằng câu cách ngôn và bảy nhịp ở mục 4, thân bài khẳng định thẳng, được duyệt. Khi người dùng đã chê một bản, bản mới phải viết lại từ nguồn, không bê nguyên ví dụ và câu chữ của bản bị chê; kiểm bằng `--source <bản bị chê>`.
- Trước khi viết hết 50.000 ký tự, gửi người dùng duyệt phần mở bài (khoảng 3.000–4.000 ký tự đầu). Sửa hướng ở đây rẻ hơn nhiều so với viết lại cả bài.

## 10. Mẫu Fact Ledger

```
| Mã | Câu trong nguồn / chất liệu | Trạng thái | Viết lại thành | URL |
|----|------------------------------|------------|----------------|-----|
| F1 | ... | ĐÚNG / SỬA / THEO LỜI KỂ / KHÔNG XÁC MINH / BỔ SUNG | ... | ... |
```

## 11. Script kiểm tra

Script nằm ở `scripts/abooks_check.py` trong thư mục skill (nguyên bản của skill gốc, thêm hai mục: dấu hiệu nhập vai tác giả và mốc chương ước tính). Chạy:

```
python -I D:/youtubeclaude/.claude/skills/abooks-writer/scripts/abooks_check.py BAN_NHAP.txt --source work/source_joined.txt --min 50000 --max 60000
```

- `--asr`: đếm một file phụ đề chưa ghép dòng.
- `--keywords "a,b,c"`: số lần và vị trí đầu tiên của từng từ khóa.
- `--seo work/seo.txt`: kiểm gói SEO.
- `--cpm 890`: in mốc thời gian ước tính của các câu đề mục (đoạn một câu ngắn), dùng cho mục 12.4. 890 ký tự mỗi phút là tốc độ đo trên các video Abooks mẫu.
- Mục "NHAP VAI" phải bằng 0 (luật cứng 3).
- Mục "GIONG ABOOKS" (thêm `--author "Osho"` hay tên khác khi không phải Krishnamurti) phải đạt hết: đoạn đầu là 1–2 câu cách ngôn, không dấu hiệu mở chậm trong 1.500 ký tự đầu, tên tác giả trong 1.200 ký tự đầu, cụm rào đón không quá 4 trên 10.000 ký tự, động tác trò chuyện không quá 6 cả bài, đoạn mở bằng tên tác giả không quá 15%, câu ngắn 8–15%, kết gọi lại câu mở. Ngưỡng đã thử trên ba bản: bản v3 được duyệt đạt hết; bản v2 bị chê trượt 5 mục; bản v1 trượt mục rào đón.
- Khi viết lại một bản mà chính mình đã viết trước đó và người dùng muốn bản mới hoàn toàn, chạy thêm `--source <bản cũ>` và giữ tỉ lệ trùng dưới 5%.

## 12. Gói SEO YouTube

### 12.1 Tiêu đề mẫu đã phân tích

Năm video tham chiếu (tiêu đề khôi phục từ tên file phụ đề, dấu câu có thể hơi khác bản thật):

| Tiêu đề | Ký tự | Công thức | Từ khóa chính | Từ khóa phụ | Móc |
|---|---:|---|---|---|---|
| Bẫy TÂM LÝ mang tên THỜI GIAN \| Jiddu Krishnamurti | 50 | Ẩn dụ + KHÁI NIỆM IN HOA \| Tác giả | Krishnamurti, thời gian tâm lý | tâm lý | chữ "Bẫy" |
| Krishnamurti BẪY TÂM LINH \| Sức Mạnh Của Sự Tĩnh Lặng | 53 | Tác giả + ẨN DỤ IN HOA \| Lợi ích | Krishnamurti, tâm linh | tĩnh lặng | "BẪY", "Sức Mạnh" |
| Sự Thật Về Thiền Định & Trí Tuệ Nhân Tạo - Jiddu Krishnamurti | 61 | Sự Thật Về X & Y - Tác giả | thiền định | trí tuệ nhân tạo | ghép chủ đề kinh điển với chủ đề thời sự |
| Thiền Định Đích Thực: Cái Tôi Là Gì? \| Jiddu Krishnamurti | 57 | X Đích Thực: Câu hỏi định nghĩa? \| Tác giả | thiền định | cái tôi | câu hỏi "Là Gì?" đúng ý định tìm kiếm |
| Osho - Mắc Kẹt Trong Đau Khổ và Hoài Nghi: Thức Tỉnh Tâm Trí Bằng Nhát Búa Triết Học của Đức Phật | 97 | Tác giả - Nỗi đau: Lời giải + thực thể uy tín thứ hai | Osho, Đức Phật | đau khổ, hoài nghi, thức tỉnh, triết học | nỗi đau người xem, hình ảnh "nhát búa" |

Quy luật rút ra:

- Tên tác giả luôn có mặt, vì đó là thực thể người xem gõ tìm nhiều nhất. Đặt ở đầu, hoặc ở cuối sau " | " hay " - ".
- Một khái niệm lõi làm từ khóa chính; nhấn một đến ba chữ bằng IN HOA (TÂM LÝ, THỜI GIAN, BẪY TÂM LINH), không in hoa cả câu.
- Một từ móc cảm xúc hoặc tò mò: Bẫy, Sự Thật Về, Đích Thực, Sức Mạnh, Mắc Kẹt, Thức Tỉnh, Là Gì?
- Viết hoa chữ cái đầu mỗi từ; không emoji; không hashtag trong tiêu đề.
- Vùng độ dài chung 50–61 ký tự. Tiêu đề 97 ký tự sẽ bị cắt trên điện thoại và trang tìm kiếm.
- Điểm yếu cần sửa khi viết lại: từ khóa của tiêu đề thường xuất hiện muộn trong kịch bản, tên tác giả gần như không được nhắc.

### 12.2 Phân tích bản nguồn (Bước 1b)

1. Lấy tiêu đề gốc. File DownSub có dạng `[Vietnamese] (auto-generated) <tiêu đề> [DownSub.com].txt`, chữ có dấu và ký tự đặc biệt bị thay bằng `_`. Khôi phục bằng cách đối chiếu với nội dung kịch bản. Nếu vẫn không chắc, tìm bằng WebSearch (tên tác giả + cụm khôi phục được + youtube). Vẫn không ra thì hỏi người dùng đúng một câu.
2. Ghi vào `bible.md`: tiêu đề gốc, số ký tự, công thức (theo bảng 12.1), từ khóa chính, từ khóa phụ, từ móc, vị trí tên tác giả, chữ in hoa.
3. Chạy script với `--asr --keywords "<tác giả>,<từ khóa chính>,<từ khóa phụ>"` trên file nguồn để biết mỗi từ khóa xuất hiện bao nhiêu lần và lần đầu ở đâu. Ghi nhận xét: giữ gì, sửa gì.
4. Nghiên cứu từ khóa với 2–4 lượt WebSearch, ví dụ `<tác giả> <khái niệm> youtube`, `<tác giả> <khái niệm>` bằng tiếng Việt, và tên khái niệm hay tác phẩm bằng tiếng Anh. Mục đích: xem các video cùng chủ đề được đặt tên thế nào, cụm từ nào người xem hay dùng, tên tác phẩm hay bài nói nào gắn với chủ đề. Không chép nguyên tiêu đề của kênh khác.
5. Chốt bộ từ khóa:
   - Một từ khóa chính: tác giả + khái niệm lõi (ví dụ "Krishnamurti thời gian tâm lý").
   - Ba đến sáu từ khóa phụ: khái niệm phụ, tên tác phẩm hay bài nói, cụm người xem hay gõ (thiền định, cái tôi, buông bỏ, sống trong hiện tại…).
   - Tối đa hai từ khóa xu hướng, chỉ khi kịch bản thật sự bàn tới (ví dụ trí tuệ nhân tạo).

### 12.3 Ba tiêu đề

Viết nội bộ khoảng 9 phương án, mỗi họ công thức 3 phương án, chấm điểm, rồi chọn ba tiêu đề thuộc ba họ khác nhau:

- Họ A, ẩn dụ trước, tác giả sau: `[Ẩn dụ + KHÁI NIỆM IN HOA] | [Tác giả]`.
- Họ B, tác giả trước: `[Tác giả] [CỤM LÕI IN HOA] | [Lợi ích hoặc kết quả]`.
- Họ C, đúng ý định tìm kiếm: `Sự Thật Về X…`, `X Đích Thực: Y Là Gì?`, `[Nỗi đau]? [Lời giải] - [Tác giả]`.

Luật:

- 45–70 ký tự; tối đa 100. Từ khóa chính nằm trong khoảng 40 ký tự đầu khi được.
- Luôn có tên tác giả. Một đến ba chữ IN HOA. Viết hoa đầu mỗi từ như mẫu.
- Không emoji, không hashtag, không "gây sốc", "100%", "bí mật không ai nói".
- Chỉ hứa điều kịch bản trả lời. Chỉ nêu tên tác phẩm nếu kịch bản dựa trên tác phẩm đó và đã kiểm chứng.
- Khác rõ tiêu đề bản nguồn: không trùng cụm bốn chữ liên tiếp, trừ tên riêng và tên khái niệm.

Chấm điểm, mỗi tiêu chí 0–10:

- SEO = trung bình của: từ khóa rõ, đúng ý định tìm kiếm, tác giả nổi bật.
- CTR = trung bình của: tò mò, cụ thể, sức căng cảm xúc.
- Tin cậy = trung bình của: đúng sự thật, khớp nội dung, tự nhiên khi đọc.
- Độ dài = 10 nếu 45–70 ký tự, 7 nếu 71–85, 4 nếu 86–100.
- Tổng = SEO × 0,30 + CTR × 0,25 + Tin cậy × 0,35 + Độ dài × 0,10.

Loại mọi phương án có Tin cậy dưới 8. Khi hai phương án ngang điểm, chọn cái dễ hiểu hơn.

### 12.4 Mô tả

- Dài khoảng 700–1.800 ký tự (tính cả mốc thời gian). Giới hạn của YouTube là 5.000 byte; chữ Việt có dấu tốn nhiều byte hơn, script báo cả hai số.
- Một hai câu đầu, khoảng 150 ký tự, là phần hiện trước nút "Xem thêm": phải có từ khóa chính, tên tác giả và lời hứa của video.
- Đoạn tiếp theo, ba đến năm câu, tóm hành trình nội dung và rải tự nhiên ba bốn từ khóa phụ. Giọng người dẫn, gọi tác giả ở ngôi thứ ba.
- Một dòng bắt đầu bằng "Tư liệu:": tác phẩm gốc (tên gốc, năm, người biên tập nếu có), các kinh hay truyện đã dùng làm giai thoại, và câu "Nội dung được tổng hợp và diễn giải; hãy tìm đọc bản gốc để cảm nhận trọn vẹn." Chỉ nêu những gì có trong Fact Ledger.
- Có mục "Mốc thời gian" ước tính: dòng đầu 00:00, thêm 8–12 mốc lấy từ câu đề mục và những câu chuyển chặng lớn, tính bằng `--cpm 890`. Ghi chú cho người dùng (ngoài mô tả) rằng mốc là ước tính, chỉnh theo voice thật. Không link. Một câu mời đăng ký nhẹ nhàng là đủ; tên kênh chỉ khi người dùng đã cho biết.
- Dòng cuối là các hashtag.
- Mọi dữ kiện trong mô tả phải có trong Fact Ledger.

### 12.5 Hashtag

- Ba đến năm hashtag ở dòng cuối mô tả. YouTube có thể hiện ba hashtag đầu phía trên tiêu đề, nên xếp theo thứ tự: tác giả, khái niệm lõi, chủ đề rộng.
- YouTube bỏ qua toàn bộ hashtag của video có quá 60 hashtag; một số hướng dẫn nêu ngưỡng 15. Giữ ở mức năm trở xuống là an toàn.
- Viết liền, không khoảng trắng. Tên riêng viết hoa đầu (#Krishnamurti, #Osho). Chủ đề viết không dấu, chữ thường, viết liền (#thiendinh, #triethoc), trừ khi người dùng muốn giữ dấu.
- Không hashtag gây hiểu lầm hoặc không liên quan.

### 12.6 Mười tag

- Đúng mười tag. Tổng tối đa 500 ký tự tính cả dấu phẩy; tag có khoảng trắng được YouTube tính thêm hai ký tự ngoặc kép. Thường chỉ 150–300 ký tự.
- Mỗi tag một đến năm từ, không lặp hệt nhau.
- Cơ cấu gợi ý:
  - 1 tag đúng nguyên từ khóa chính.
  - 2 tag biến thể tên tác giả (Jiddu Krishnamurti, triết lý Krishnamurti…).
  - 3–4 tag khái niệm có dấu.
  - 1–2 tag không dấu của từ khóa chính.
  - 1 tag ngách rộng (sách nói triết học, review sách tâm linh…).
  - 1 tag tên tác phẩm hay bài nói, nếu có.
- Không tên kênh khác, không tag không liên quan.

### 12.7 Định dạng file SEO

Script đọc file này theo đúng các nhãn đầu dòng:

```
PHÂN TÍCH BẢN NGUỒN
Tiêu đề gốc: ...
Công thức: ...
Từ khóa chính: ...
Từ khóa phụ: ...
Vị trí từ khóa trong bản nguồn: ...
Nhận xét: ...

BỘ TỪ KHÓA CHO BẢN VIẾT LẠI
Chính: ...
Phụ: ...

TIÊU ĐỀ 1: ...
Ghi chú: họ A, [số] ký tự, điểm [x], dùng khi ...
TIÊU ĐỀ 2: ...
Ghi chú: ...
TIÊU ĐỀ 3: ...
Ghi chú: ...

MÔ TẢ:
[đoạn mô tả]
#A #B #C

HASHTAG: #A #B #C

TAG: tag 1, tag 2, tag 3, tag 4, tag 5, tag 6, tag 7, tag 8, tag 9, tag 10
```

## 13. Chế độ đề xuất chủ đề

Làm theo [topic-proposals.md](references/topic-proposals.md). Mỗi đề xuất là một tác phẩm thật của tác giả (Krishnamurti, Osho, hay một bộ kinh, một tác phẩm Phật học) cộng với một nỗi đau người xem Việt Nam. Tiêu đề nháp theo họ A/B/C của mục 12.3. Số liệu YouTube lấy bằng `scripts/yt_research.py`. Danh mục sách và nguồn: [book-catalog.md](references/book-catalog.md), [research-protocol.md](references/research-protocol.md).

## 14. Chế độ viết mới

Không có bản nguồn, nên tra cứu đóng vai bản nguồn:

1. Chốt chủ đề: tác phẩm chính, lát cắt (chương, bài nói, bài kinh), nỗi đau người xem, câu hỏi trung tâm. Ghi vào `work/bible.md`.
2. Tra cứu theo [research-protocol.md](references/research-protocol.md), dựng "Bản đồ tác phẩm": mỗi chương hay bài nói một dòng, ý chính thuật lại bằng lời mình, ngày, nơi, người đối thoại, URL. Bản đồ này thay cho mục 2 (Chuẩn bị nguồn) và là đầu vào của Source Bible ở Bước 1.
3. Từ đó chạy đúng Bước 1–9 của mục 6. Phân tích tiêu đề bản nguồn (Bước 1b) thay bằng phân tích tiêu đề 3–5 video cùng chủ đề tìm được bằng `yt_research.py search`.
4. Mọi dữ kiện lấy từ tra cứu phải có trạng thái trong Fact Ledger như dữ kiện của bản nguồn.
5. Giọng, mở bài, kết bài giống hệt chế độ viết lại: công thức bảy nhịp, giọng thân bài khẳng định, kết gọi lại câu cách ngôn, duyệt mở bài trước khi viết tiếp. Không vì không có bản nguồn mà viết thành bài giảng hay bài tổng hợp: chất liệu tra cứu được kể bằng cảnh, giai thoại (kho [anecdotes.md](references/anecdotes.md)), câu hỏi treo, như một video Abooks.
6. Kiểm định bằng script như Bước 5, chỉ bỏ cờ `--source` (không có bản nguồn); nếu chủ đề đã có video của kênh khác mà mình đã đọc transcript, dùng transcript đó làm `--source` để chắc không bám câu chữ của họ.

## 15. Tài liệu kèm theo

- [approved-sample.md](references/approved-sample.md): đoạn mẫu đã được người dùng duyệt (mở bài, một khối thân bài, kết bài), là chuẩn giọng cho mọi chế độ.
- [anecdotes.md](references/anecdotes.md): kho giai thoại, ngụ ngôn đã kiểm xuất xứ, kèm cách kể và chỗ hợp dùng.
- [book-catalog.md](references/book-catalog.md): danh mục tác phẩm Krishnamurti, Osho, Phật học để định hướng.
- [research-protocol.md](references/research-protocol.md): thứ bậc nguồn, cách tra khi trang bị chặn, Fact Ledger.
- [topic-proposals.md](references/topic-proposals.md): quy trình đề xuất 5 chủ đề.
- [sample-analysis.md](references/sample-analysis.md): phân tích 7 video Krishnamurti của ABooks và BBooks: mục 0 là cách mở bài và ba mô hình triển khai thân bài (đọc trước khi lập dàn ý); các mục sau là số liệu, tiêu đề, mô tả, tag. Giọng của skill theo mục 3–4 (người dẫn ngôi thứ ba, mượn động cơ của mô hình lời thầy và phim tài liệu).
- `scripts/abooks_check.py`, `scripts/yt_research.py`.
