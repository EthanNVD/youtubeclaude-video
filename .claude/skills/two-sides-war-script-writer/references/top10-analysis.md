# Phân tích biên tập 10 kịch bản nhiều view nhất — Two Sides of War

Snapshot **15/11/2026**. Nguồn: danh sách video `@TwoSidesOfWar/videos` (32 video công khai lúc đo) lấy bằng `yt-dlp --flat-playlist`, và **phụ đề tiếng Anh tự động của cả 10 video**, đọc toàn văn. View là số công khai tại thời điểm đo, tuổi video khác nhau → không phải bảng xếp hạng hiệu suất thuần. Không có Analytics (CTR, retention, AVD). Transcript gốc chỉ nằm ở scratch, **không** lưu vào skill (bản quyền); file này chỉ ghi cấu trúc, kỹ thuật và ví dụ tự viết.

Làm mới snapshot: `python scripts/channel_snapshot.py --top 10 --out <thư mục scratch>`.

## 1. Bảng tổng

| # | Video | View | Thời lượng | Từ (ASR) | WPM | Dạng | Dụng cụ xuyên bài (device) | Hai nhân vật dẫn |
|---|---|---:|---|---:|---:|---|---|---|
| 1 | What Was The REAL Turning Point of WW2? | 387k | 40:34 | 6.541 | 161 | Cân nhắc ứng viên (10) | Cái cân + con dấu "not yet / close" | Kế toán + con dấu |
| 2 | Could the Soviets REALLY Have Beaten Hitler Alone? | 267k | 39:17 | 6.343 | 161 | Phản thực tế phụ thuộc (5 phép thử) | Bức tường hai đường ống + van | Sếp + thư ký ("clerk") |
| 3 | Why Operation Barbarossa Was COMPLETELY Avoidable | 246k | 26:48 | 4.434 | 165 | Chuỗi lối thoát bị bỏ lỡ | Bộ đếm "missed exits" hai phía | (ít, chưa ổn định) |
| 4 | Why The Battle of Midway Was COMPLETELY Avoidable | 203k | 35:39 | 5.838 | 164 | Chuỗi quyết định + đồng hồ | Sổ log điểm hai phía, mốc 10:22 | Kế toán |
| 5 | What Was The REAL Turning Point of the Pacific War? | 200k | 33:01 | 5.266 | 159 | Cân nhắc ứng viên (8) | Thước đo thủy triều + phao + 2 thẻ | Trưởng cảng + cậu bé |
| 6 | How Every Country Teaches Hitler | 149k | 20:48 | 2.970 | 143 | Khảo sát theo quốc gia (9) | Bàn học, tab xanh / tab đỏ | Thủ thư + "my boy" |
| 7 | The ENTIRE Eastern Front Explained | 106k | 36:36 | 6.300 | 172 | Tổng quan chiến dịch | Hai người lính tổng hợp + con ngựa | Không |
| 8 | The Deadliest Battles in Human History | 103k | 26:58 | 4.408 | 163 | Tuyển tập xếp hạng 3 tiêu chí | Tháp hình người (1 = 10.000) | Kế toán |
| 9 | What Happened to Hitler's Family After the War? | 91k | 37:50 | 5.864 | 155 | Tiểu sử nhóm / gia phả | Cây gia phả tối, thắp từng nhánh, bảng tên | Thủ thư + cậu bé |
| 10 | What REALLY Lost Germany WW2? | 87k | 33:48 | 5.416 | 160 | Xếp hạng nguyên nhân 10→1 | Tháo máy, 10 khay linh kiện, đồng hồ đo | Thợ máy + học việc |

Trung vị ≈ **34 phút, ~5.600 từ, ~161 từ/phút**. Video ngắn nhất (Teaches Hitler, 21 phút) là chủ đề văn hóa–giáo dục rộng, ít chiến trận. Bản đếm ASR gồm cả lời thoại nhân vật.

**Hai thế hệ format.** Ba video đầu kênh (Eastern Front, Deadliest, Barbarossa) giọng YouTuber hơn ("like a pizza", "just kidding"), chưa có CTA giữa bài, nhân vật dẫn chưa ổn định, Eastern Front dùng nhân vật tổng hợp. Từ Midway trở đi (và rõ nhất ở các video đăng sau 13/10: Soviets Alone, Teaches Hitler, Family) format **khóa chặt**: device có luật chơi nói rõ, điệp khúc cuối chương, cặp nhân vật dẫn, CTA giữa bài 33–41%, kết bookend, sử học có tên người. Khi viết mới, **lấy thế hệ sau làm chuẩn**.

## 2. Giải phẫu chung (thế hệ sau)

| Pha | Vị trí (40 phút) | Việc phải làm | Ví dụ trong 10 bài (diễn giải) |
|---|---|---|---|
| Cold open | 0:00–0:45 | Một khoảnh khắc cụ thể có ngày/giờ/nơi + nghịch lý | Berlin 11/12/1941 tuyên chiến với Mỹ dù không bị buộc; cùng một ngày: xe tăng Liên Xô ra trận và Roosevelt ký Lend-Lease |
| Tranh luận | 0:45–1:10 | "Mọi người có câu trả lời riêng" → 3–6 đáp án cạnh tranh, kể nhanh dạng câu hỏi | Dunkirk? Phòng nội các? Moscow? 5 phút trên Thái Bình Dương? |
| Câu hỏi = tiêu đề | ~1:00 | Đọc **nguyên văn câu hỏi tiêu đề** | "Could the Soviets really have beaten Hitler alone?" |
| Hợp đồng device | 1:00–1:40 | Tagline bộ ba con số + luật chấm điểm, do nhân vật dẫn nói | "[N] ứng viên, hai phía, một cái cân"; "đóng một van, xem mặt trận" |
| Định nghĩa | 1:20–2:00 | Nói rõ đo cái gì (turning point = lúc một bên không thể thắng nữa; casualties vs killed) | |
| Baseline | 1:30–4:30 | Trạng thái ban đầu của device (cân năm 1939, nước thấp nhất, máy mới xuất xưởng, cây gia phả tối) | Dân số, kinh tế, dầu, thép |
| Chương × 5–10 | 4:30–36:00 | Mỗi chương: neo thời gian/nơi → người quyết định + lập luận hai phía → cơ chế/số liệu → hậu quả → **điệp khúc chấm điểm** → câu bắc cầu | 1,5–4,5 phút/chương |
| CTA giữa bài | 33–41% | 1–2 câu, câu đùa gắn chủ đề, rồi trở lại ngay | "Like giúp kênh — khác kế hoạch của Đức, nó không cần phe kia sụp trước" (diễn giải) |
| Ứng viên ngoài sổ / myth | ~90% | Xử lý trận nổi tiếng nhất mà người xem chờ (D-Day, Bagration) hoặc giai thoại "quá hay để kiểm" | "Họ là lúc trả hóa đơn, không phải lúc bước ngoặt" |
| Tổng kết device | 92–94% | Đọc lại toàn bộ thang điểm từng mục một câu | "Dunkirk, chưa. Năm ngày ở London, gần nhất…" |
| Verdict | 94–97% | Câu trả lời rõ, có ngày/khoảng; số liệu nặng ký; câu đối xứng dễ nhớ | |
| Sử gia bất đồng | 96–98% | "Công bằng mà nói, sử gia không đồng ý…" 2–4 trường phái có tên | |
| Cái giá con người | 97–98% | Tổng tử vong, giọng chậm, không đùa | |
| Kết + CTA | 98–100% | "Đó là câu trả lời của chúng tôi. Còn bạn?" + câu hỏi chọn 1 trong các ứng viên + gợi ý 2 video liên quan + subscribe kèm câu đùa chủ đề + **câu bookend** quay về hình ảnh mở đầu | |

## 3. Từng video — ghi chú biên tập

### #1 Real Turning Point of WW2 (387k) — chuẩn mực của kênh
- **Hook**: mở bằng một câu thoại kịch tính của lãnh đạo, rồi ngày–nơi, rồi nghịch lý "không ai bắt ông ấy làm". Trong 45 giây đã có: sự kiện, nghịch lý, câu hỏi phân biệt *kết thúc* và *thua*.
- **Luật chơi**: 10 ứng viên đi theo thời gian từ 1939; định nghĩa bước ngoặt = khi một bên không thể thắng dù làm gì. Baseline là cái cân 1939 (dân số, dầu, đế quốc, hai người khổng lồ đứng ngoài). Kết baseline bằng câu hỏi xuyên bài: tốc độ vs trọng lượng — "khi nào tốc độ không còn đủ?".
- **Chương**: Dunkirk → nội các 5 ngày → Battle of Britain → Barbarossa → Moscow + Pearl Harbor + tuyên chiến → Midway → El Alamein → Stalingrad → Đại Tây Dương → Kursk → (D-Day/Bagration ngoài sổ). Mỗi chương kết bằng "Cân có nghiêng ở đây không?" + con dấu **not yet / close**. Chương được nối bằng **liên kết nhân quả** ("Anh không chịu đàm phán, nên Hitler có một vấn đề chưa từng lên kế hoạch").
- **Kỹ thuật đáng học**: callback xuyên chương (lời hứa của Göring ở Dunkirk → lời hứa tiếp tế ở Stalingrad; "nhớ các tàu sân bay vắng mặt"); nhân vật kế toán **trì hoãn con dấu** ở tuần tháng 12/1941 ("giữ ý đó lại") để giữ mạch tới cuối; câu chốt chương dạng đối xứng ("El Alamein là nơi Anh bắt đầu thắng; Stalingrad là nơi Đức bắt đầu thua").
- **Verdict**: một tuần cụ thể (5–11/12/1941) với ba sự kiện trong 7 ngày; số máy bay/dầu; Nhật tách riêng; sau đó mới nêu sử gia khác ý; tổng tử vong; CTA với câu đùa "lời tuyên bố duy nhất không ai hối hận".
- **Rủi ro cần tránh khi học**: nhiều câu thoại tái dựng của Hitler/Göring/Zhukov — chỉ học dạng *chức năng*, không bịa lời; xem mục 5.

### #2 Could the Soviets Have Beaten Hitler Alone? (267k, tăng nhanh nhất)
- **Hook "hai bức tranh"**: cùng một ngày, hai hình ảnh đối nghịch (xe tăng nội địa ra trận / chữ ký viện trợ). Mỗi phe tranh luận giữ một bức và bỏ bức kia → câu hỏi. Đây là mô hình hook mạnh cho đề tài *tranh cãi sử học*.
- **Sử học là nhân vật**: mở bằng con số 4% chính thức của Liên Xô và con số 7–10% phương Tây, rồi hỏi "4% của cái gì?" — biến tranh luận thành bí ẩn cần giải.
- **Phép thử có luật**: mỗi chương "đóng một van, xem mặt trận": giữ được → xa xỉ; trượt → là cả cuộc chiến; chậm lại → "đếm tháng, vì tháng là mạng người". Năm phép thử: Moscow 1941, Stalingrad, đường vận chuyển (chương *cơ chế*, không phải trận), Bagration (tốc độ), oanh tạc + mặt trận phía tây (đòn bẩy vô hình), cộng mặt trận Mãn Châu không mở.
- **Chương "cái hộp"**: liệt kê hàng viện trợ theo kiểu mở thùng — trước hết nói *không* phải xe tăng (1/10), rồi xe tải, đầu máy, radio, nhôm, xăng máy bay, thực phẩm. Tuyệt vời cho việc biến thống kê thành phát hiện.
- **Bằng chứng nhiều tầng**: tuyên bố công khai vs lời riêng (hồi ký, ghi âm KGB) được gắn nhãn rõ "không phải tài liệu thời chiến". Kết luận dạng *khoảng*: "gần như chắc không thua; thắng tới Berlin thì chậm 12–18 tháng, có thể hơn".
- **Bookend**: Torgau — một xe Jeep phía Mỹ, một T-34 và một xe tải Detroit phía Liên Xô; kết lại bằng hai bức tranh ở đầu bài.

### #3 Barbarossa Avoidable (246k) — thế hệ đầu, chủ đề cực lớn
- Hook giờ/ngày/quy mô → "không phải vì…, không phải vì…, không phải vì…" → nghịch lý chuyến tàu ngũ cốc. Một câu đùa tua ngược tới năm 1190 rồi "đùa thôi" + fun fact tên chiến dịch.
- Vật thể ghi nhớ: thành phố Brest ("nhớ thành phố này"), tàu tuần dương Lützow bán dở ("nhớ con tàu này, nó sẽ quay lại") → payoff: con tàu bắn vào quân Đức ở Leningrad. Đây là **mẫu setup–payoff bằng đồ vật** tốt nhất.
- Kết phân biệt rõ hai loại lỗi: Moscow lỡ lối thoát *chuẩn bị*, Berlin lỡ lối thoát *chọn chiến tranh*; bác bỏ thuyết "đánh phủ đầu". Không CTA giữa bài.

### #4 Midway Avoidable (203k)
- Cold open đồng hồ 10:22 + "năm phút may rủi — phút thì có thật, may rủi phức tạp hơn" → tease 4 lỗi phía Nhật, 2 lỗi phía Mỹ → bảng điểm 0–0, "quay lại lúc 10:22".
- Đi chậm qua kế hoạch, tình báo, sửa tàu, trinh sát; nhịp **sát đồng hồ** khi tới trận. Có **myth audit** sau cao trào (chiếc thủy phi cơ trễ thực ra *giúp* Nhật; phi công giỏi không chết hết). Verdict cân hai trường phái (hệ thống vs cá nhân/may rủi) có tên sử gia; điểm 11–4; để lại một "phao không chấm" cho khán giả bình luận — CTA dùng đúng một ngã rẽ còn tranh cãi.

### #5 Real Turning Point of the Pacific (200k)
- Hook bằng tương phản sản xuất (15 tàu sân bay vs 0 trong một năm) → "hỏi 10 sử gia, nghe nhiều đáp án" → tagline device.
- Luật: 8 phao buộc theo mực nước ngày đó, **hai thẻ** cho mỗi ứng viên (Tokyo tin gì / Washington biết gì), con dấu yes/no/not yet. Phao đầu tiên là *một đạo luật trước chiến tranh* — ứng viên bất ngờ mở màn tạo tò mò.
- Verdict hai tầng (nước ngừng dâng ở Midway; nước rút ở Guadalcanal) + phản biện "nổi tiếng không phải là cuối cùng" + câu hỏi phản thực tế "nếu Nhật thắng Midway" trả lời bằng sản xuất. Bookend ẩn dụ "mặt trăng kéo thủy triều làm bằng thép Mỹ".

### #6 How Every Country Teaches Hitler (149k, 21 phút)
- Hook montage 4 sự kiện lạ ở 4 nước (bắt buộc thăm trại, bị kết án vì repost, cho phép Mein Kampf trong lớp, cửa hàng tên Hitler) → "cùng một người, cùng một cuộc chiến" → câu hỏi.
- Lời hứa vòng lặp mạnh nhất kênh: nghiên cứu UNESCO tìm ra **một câu gần như mọi sách đều có — sẽ cho xem ở cuối**. Payoff ở 19:20 thành luận điểm chính.
- Mỗi nước một nhãn hai chữ (quê hương thủ phạm, nạn nhân đầu tiên, đất giữa hai kẻ xâm lược…) và điệp khúc "Đặt gì lên bàn? Tab xanh: điều họ nói. Tab đỏ: điều họ bỏ qua." Mỗi nước có số liệu khảo sát + một chi tiết gây tranh cãi. Kết: tab đỏ của mọi nước đều là trang "phe mình đã đồng ý/thỏa hiệp/ngoảnh mặt".
- Bài học: đề tài *văn hóa–ký ức* (không cần trận đánh) vẫn đạt view cao khi có câu hỏi phổ quát và cấu trúc khảo sát rõ.

### #7 ENTIRE Eastern Front (106k) — thế hệ đầu
- Hook địa lý (3.000 km ≈ New York–Denver) → khoảng trống hiểu biết của khán giả phương Tây → hứa ba điều bí ẩn cụ thể (con ngựa, bức ảnh bị sửa, ngày chiến thắng lệch một ngày).
- Dùng hai người lính hư cấu (Karl/Alexei) + con ngựa làm sợi chỉ; kết theo số phận họ. **Không** chép thiết bị này mặc định — phải khai báo là composite (xem style-guide).
- Không CTA giữa bài, kết hỏi khán giả muốn nghe chuyện của ai.

### #8 Deadliest Battles (103k) — thế hệ đầu
- Tease 4 cực trị trước khi xếp hạng; luật đếm (casualties vs killed, khoảng ước tính) ngay phút 0:49; ba bảng xếp hạng (một ngày, quân đội biến mất, lớn nhất); tháp hình người là device.
- Kết "ba bảng, ba quán quân" → tháp gần như toàn thế kỷ 20, chủ yếu Mặt trận phía Đông → dẫn sang video Eastern Front → câu hỏi khép "bạn đếm thế nào?".

### #9 What Happened to Hitler's Family (91k)
- Hook trớ trêu con người: cháu ruột tên Hitler nhập ngũ Hải quân Mỹ, em cùng cha khác mẹ chết trong tù Liên Xô, cháu khác ở trại Stalingrad → "Có thoát được một cái tên không?" (tiêu đề được *chuyển* thành câu hỏi đạo đức).
- Mỗi chương một nhánh cây gia phả được "thắp sáng", điệp khúc "Cái tên đã khiến họ trả giá gì?". Một chi tiết treo từ chương 1 ("cái ô trống trong sổ rửa tội — sẽ quay lại") được trả ở chương 7.
- **Kiểm chứng thành giải trí**: hồi ký Liverpool bị đối chiếu hồ sơ cảnh sát; giai thoại "tôi tên Hess" bị gắn nhãn *quá hay để không kiểm*; Purple Heart "có thể, chưa chứng minh"; tôn trọng người còn sống (bảng tên để trống). Đây là bản sắc "chúng tôi kiểm giấy tờ" của kênh.
- Nạn nhân trong gia đình (bị giết trong chương trình T4) được tách giọng: "cô ấy nhận một bông hoa, không nhận phán quyết".

### #10 What REALLY Lost Germany (87k)
- Hook nghịch lý số liệu (năm 1944 Đức làm nhiều máy bay nhất — vô ích) → mọi người sống sót đều có lời giải thích đổ cho người khác → tháo máy 10 bộ phận.
- **Hai luật**: mỗi bộ phận nghe lời tướng Đức nói sau chiến tranh rồi đối chiếu con số; thứ tự top 3 là quan điểm, sử gia còn tranh cãi. Đếm ngược 10→1 kiểu "đồng minh yếu → bùn → mật mã → Hitler → ý thức hệ → Lend-Lease → dầu → không chiến–hải chiến → Hồng quân → tổng hóa đơn".
- Mạch phụ xuyên bài: **huyền thoại "chỉ do Hitler" của các tướng** bị tháo dần (nhật ký Halder đối chiếu hồi ký) → trở thành luận điểm kết. Số 1 không phải một bộ phận mà là *phép cộng* — kết bằng câu đảo nghĩa ("thứ duy nhất cỗ máy không bao giờ thiếu là kẻ thù" — diễn giải).

## 4. Những gì đứng sau view (suy luận có giới hạn)

1. **Câu hỏi lớn về kết cục WW2** (ai/điều gì quyết định, có tránh được không) với tên quen thuộc (WW2, Barbarossa, Midway, Stalingrad, Hitler) chiếm 7/10. Đề tài nhỏ/kỹ thuật đăng tháng 11 (M1 Garand, Ý sụp đổ, Nhật thua ở Trung Quốc) hiện thấp — nhưng tuổi quá ngắn, chưa kết luận.
2. **Từ khóa nghi vấn viết hoa** REAL/REALLY/COMPLETELY xuất hiện ở 6/10, nhưng ba video không có (Teaches Hitler, Family, Deadliest) vẫn trên 90k nhờ **tò mò phổ quát** (giáo dục, gia đình, "đẫm máu nhất"). Lời hứa nội dung quan trọng hơn chữ in hoa.
3. **Đề tài "tranh cãi giữa hai trường phái"** (Liên Xô tự thắng?) tăng nhanh nhất — người xem mang sẵn quan điểm, kịch bản cho họ một khung để kiểm tra; CTA "bạn đứng phe nào khi bắt đầu xem?" khai thác đúng điều đó.
4. Dài 33–40 phút không cản view; video 21 phút cũng đạt cao. Độ dài nên theo số chương cần thiết, không độn.
Đây là quan sát một thời điểm trên một kênh mới, không phải quan hệ nhân quả đã chứng minh.

## 5. Lời thoại nhân vật — kênh dùng thế nào, skill được làm gì

Mỗi video thế hệ sau có **45–120 lần đổi giọng** (đánh dấu `>>` trong phụ đề). Bốn loại:
1. **Trích dẫn thật** (diễn văn Churchill, nhật ký Halder, thư William Patrick gửi Roosevelt, lời khai Paula) — giữ nguyên văn, thường kèm nguồn trong lời kể.
2. **Lời được ghi nhận gián tiếp, nén lại** ("theo hồi ký của X, Y đã nói…") — kênh thường nói rõ nguồn ngay sau câu thoại ("Đó là cách Guderian kể lại", "Simonov ghi lại Zhukov nói riêng…").
3. **Tái dựng kịch tính** của nhân vật lịch sử thể hiện lập trường đã có hồ sơ (Göring hứa tiếp tế bằng không quân, sĩ quan báo "tuyến bị cắt") — kênh dùng nhiều nhất, đôi khi không gắn nhãn.
4. **Cặp nhân vật dẫn hư cấu** (sếp/thư ký, thủ thư/cậu bé, trưởng cảng/cậu bé, thợ máy/học việc, kế toán): hỏi câu ngây thơ thay khán giả, nói luật chơi, chốt điểm chương bằng một câu, tạo nhịp nghỉ hài nhẹ.

Skill **cho phép** loại 1, 2, 4 và loại 3 có điều kiện (xem `channel-formula.md` §Thoại). Không bao giờ bịa quyết định, số liệu, sự kiện hay suy nghĩ riêng qua thoại; không thoại hài cho nạn nhân.

## 6. Bài học chuyển thành luật cho skill

1. Câu hỏi tiêu đề được nói nguyên văn trước phút 1:15; device và luật chơi trước phút 2.
2. Mỗi chương kết bằng **điệp khúc chấm điểm cùng một cú pháp** (đổi nội dung, giữ khung) — đây là khung retention chính.
3. Chuỗi chương nối bằng nhân quả, không bằng "meanwhile".
4. Ít nhất 2 vòng setup–payoff bằng *đồ vật/chi tiết cụ thể* và 1 lời hứa công khai "sẽ cho xem ở cuối".
5. Ít nhất 1 myth audit với nhãn kiểm chứng vui ("quá hay để không kiểm", "có thể, chưa chứng minh").
6. Sử học có tên người: 3–6 sử gia/công trình được nêu khi có tranh luận; trước verdict luôn có "công bằng mà nói…".
7. Verdict là câu trả lời cụ thể (một tuần, một trận, một khoảng thời gian), kèm một câu đối xứng dễ nhớ.
8. CTA giữa bài một lần ở 33–41%, câu đùa gắn chủ đề; CTA cuối = câu hỏi chọn phe + 1–2 video liên quan + subscribe đùa + câu bookend.
9. Hài khô ở sự kiêu ngạo, quan liêu, hậu cần; im lặng nghiêm túc khi nói tới thường dân, tù binh, diệt chủng.
10. Viết tách hai lớp: lời kể (narrator) và lớp thoại (nhân vật) — để bộ dựng chibi có người nói.
