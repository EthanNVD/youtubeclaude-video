# Research từ một title

Protocol này dành cho `new_from_title`, hoặc phần fact-check/research user yêu cầu thêm trong bản viết lại. `rewrite_same_structure` mặc định truy claims về các đoạn của bản cũ, không tự dựng thesis mới/nghiên cứu mở rộng; nguồn mới nếu cần chỉ làm rõ/sửa điểm liên quan và không thay sườn. Tách báo cáo source fidelity khỏi independent historical verification theo [source-structure-rewrite.md](source-structure-rewrite.md).

## Câu hỏi nghiên cứu

Tách title thành entity, thời kỳ/địa bàn, question và điều cần chứng minh. Tìm bốn lớp: chuyện xảy ra thế nào; actor có mục tiêu/thông tin gì; mechanism nào tạo kết quả; phản biện mạnh nhất và giới hạn. Không chỉ tìm headline đồng ý title.

| Nhánh tìm kiếm thích ứng | Query idea | Kết quả cần có |
|---|---|---|
| Timeline | `[operation] official history chronology` | Mốc, kế hoạch và thay đổi |
| Actor A/B | `[actor] diary directive [date]` | Ý định/thông tin đương thời |
| Hậu cần | `[operation] fuel rail shipping supply report` | Capacity và bottleneck |
| Fork | `[decision] alternatives contemporary orders` | Phương án có thật trước kết quả |
| Phản biện | `[claim] historiography evidence debate` | Lập luận đối lập mạnh nhất |
| Số | `[battle] killed wounded captured methodology` | Definition/range/scope |
| Quote | Quote fragment + author + diary/trial/date | Truy nguyên và attribution |

Cho WWII, điểm bắt đầu có thể là U.S. Army Center of Military History, Naval History and Heritage Command, U.S. National Archives, UK National Archives, Imperial War Museums, Bundesarchiv và ấn bản lưu trữ có provenance từ các bên. Đây là gợi ý loại nguồn, không giả rằng một trang cụ thể đã được đọc; kiểm URL hiện tại bằng công cụ web.

## Đọc và độ độc lập

Mở/đọc tài liệu, không dùng snippet làm nguồn cuối. Documentary dài thường cần nhiều nguồn độc lập; 6–12 tài liệu tốt có thể là điểm bắt đầu, không là quota đạt chuẩn. Một official overview dựng spine; luận đề/forks/tranh cãi cần evidence riêng. Ghi phần/pages thực sự đọc, không nhận đã đọc hết sách dài.

Primary records cho biết ai viết/báo cáo gì, không tự chứng minh họ đúng/trung thực. Memoir hậu chiến có hindsight/self-justification; báo cáo bên thắng có mục đích và cách đếm; bảo tàng tổng quan có thể lược tranh luận. Wikipedia/video khác/snippets phục vụ discovery rồi truy tài liệu nền. SRT mẫu có lỗi ASR, không là authority cho facts mới.

Ghi nguồn phụ thuộc nguồn nào. Hai site chép cùng sách, nhiều bản dịch cùng directive hay nhiều bài dẫn một memoir là một gốc chứng cứ. Critical claim nên được kiểm chéo độc lập nếu khả dụng; chỉ có một witness thì ghi giới hạn, không tạo nguồn thứ hai.

Hai nguồn có uy tín vẫn có thể mâu thuẫn: institutional overview có thể viết “intelligence failed to detect tanks”, trong khi lịch sử chính thức chi tiết ghi những cảnh báo đã tới headquarters. Ghi discrepancy, truy phạm vi/chứng cứ cụ thể, rồi sửa wording phù hợp; không đếm cả hai thành consensus và không mặc định nguồn official nào cũng luôn đúng. Đây là bài học quan sát từ pilot Market Garden, không quyết định sẵn kết luận cho đề tài khác.

## Ledger

Source: `Sxx | URL/path | title | author/institution | document/publication date | access date | type | pages/sections read | relevance | limits/dependency`.

Claim: `Cxx | proposition | date/place/actor | class | sources + exact locator | certainty | competing interpretation/estimate | wording allowed | blocks using it`.

- `FACT`: sự kiện/số/statement có chứng cứ, đúng scope/range/attribution.
- `INTERPRETATION`: causal/strategic reading từ facts; không tự coi unanimous.
- `COUNTERFACTUAL`: alternative và hậu quả có điều kiện, không là lịch sử đã xảy ra.
- `NARRATIVE DEVICE`: metaphor/công cụ narrator không tạo fact mới.
- `UNRESOLVED`: chưa đủ evidence; không đưa như fact vào narration.

Một câu có thể có nhiều claims. Một citation chung cho đoạn không bảo đảm từng số/quote. IDs nằm ở working file/outline, không trong TXT đọc.

## Thông tin tại thời điểm quyết định

Mỗi phía: objectives, constraints, resources, enemy perception, available intelligence, information actually received, competing reports, chain of command, institutional pressure, feasible choices. Tách **có cảnh báo** với **tới đúng người, đúng lúc, đủ tin cậy**.

Actor chưa biết tương lai thì không viết “he knew the war was lost” thiếu chứng cứ. Narrator có thể giải thích implications của số rồi lý do actor chọn khác. Giữ agency đối phương: hậu quả không chỉ do bên thua mắc lỗi; còn deception, adaptation và hành động bên thắng.

## Counterfactual

Fork table: `date | decision-maker | known facts then | actual choice | alternative | contemporary advocate/evidence | cost/constraint | immediate effect | uncertainty later`.

Tách ba tầng: không khởi sự chiến tranh/chiến dịch; tránh thế trận/timing cụ thể; giảm tổn thất dù chiến tranh tiếp tục. Ưu tiên alternative có advocate đương thời/hồ sơ khả thi. “Nghe hợp lý” theo hindsight chỉ là hypothesis cần nhãn rõ. Với rút quân/breakout: kiểm fuel, mobility, enemy reaction, orders và window; một mũi tên trên map không là lối thoát chắc chắn. Không tạo phần trăm thắng giả; dùng conditional wording.

Sổ điểm là device nhớ các quyết định, không phép tính trách nhiệm. Không xếp một bên chủ động xâm lược và bên bị tấn công ngang nhau chỉ vì cả hai có forks. Hành vi/tội ác đã xác nhận cần attribution rõ, không bị cân bằng giả bằng giọng trung lập.

## Số và so sánh

Phân biệt **killed, deaths, casualties, losses** theo định nghĩa nguồn; casualties có thể gồm wounded/missing/captured. Deaths sau captivity có thể ngoài battle window. Strength: initial/peak/cumulative/available? Carriers: fleet/light/escort, launched/commissioned/operational? Không so categories khác nhau chỉ vì cùng chữ.

Mỗi số có unit, window, geographic scope, side, military/civilian, denominator, range/rounding và overlap. Số cổ đại thiếu hồ sơ thường có exaggeration; không lấy upper bound gây shock. Ranking có số không comparable: sửa tiêu chí hoặc trình bày incompatibility. Battle/campaign/siege không tráo; không cộng trùng các trận đã tái xuất.

## Quote và dialogue

Quote cần nguyên văn, người nói/viết, ngày, tài liệu, locator và translation status. Hồi ký nhớ sau nhiều năm khác transcript đương thời. Không truy được quote thì bỏ ngoặc kép; chỉ paraphrase nếu evidence về ý đủ. “Reportedly” không cứu quote không có nguồn.

Thoại theo [channel-formula.md](channel-formula.md) §12. QUOTE cần đủ locator như trên. REPORTED cần nguồn ghi nhận lời đó (hồi ký, nhật ký, phỏng vấn) và narrator nói nguồn ngay sau. DRAMATIZED (mặc định bật vì đây là ngữ pháp kênh; tắt khi người dùng yêu cầu) chỉ được diễn đạt **lập trường/quyết định đã có hồ sơ**, ≤2 câu, ghi căn cứ vào quote register với nhãn `DRAMATIZED — based on Sxx`; không dùng để tạo sự kiện, con số, cảm xúc riêng, và không dùng cho nạn nhân/tội ác. Không đặt ngoặc kép cho DRAMATIZED trong bản sạch. Mặc định không bịa composite hoặc chi tiết camera/giác quan; composite chỉ khi người dùng đồng ý và được khai báo trong lời kể.

## Research readiness và sources sidecar

Đủ viết khi timeline phủ title; thesis chịu phản biện chính; key facts có locators; các phía có context; numbers/quotes được resolve hoặc hạ certainty; unresolved peripheral details đã cắt. Không phải biết mọi sự kiện chiến tranh. Thiếu evidence thay thesis thì tiếp tục đúng nhánh; nguồn không truy cập thì ghi limitation/đổi thesis hoặc giao dossier giới hạn.

Sources sidecar gồm bibliography links thật, annotations, key claims/locators, disputes và editorial choices. Attributions xuất hiện trong narration khi giúp hiểu bằng chứng; URLs/claim IDs/notes nằm ngoài voice. Access date khác event/publication date. Không giả nguồn đọc hoặc metadata.
