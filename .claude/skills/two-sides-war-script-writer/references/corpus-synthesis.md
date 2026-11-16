# Tổng hợp toàn bộ sáu kịch bản và chuyển thành skill

## Nền chứng cứ và phạm vi

Bộ nguồn do user cung cấp: sáu SRT auto-generated, được đọc đầy đủ theo cue từ đầu đến cuối bởi ba lượt phân tích song song; không suy nội dung từ title/preview. Tổng **4.677 cue, 30.416 word tokens, 172.979 ký tự lời đã nối**, khoảng **3 giờ 4 phút 48,88 giây** theo mốc cuối từng SRT. Các phép đo không xác minh facts. Manifest gồm paths gốc, SHA-256 và cách đếm ở [corpus-manifest.json](corpus-manifest.json).

Trang kênh chính thức được kiểm kê 15 video, quan sát 15 thumbnail và phần giới thiệu ngày 13/10/2026. Full-script evidence có sáu mẫu; các dạng khác trên kênh chỉ là title/thumbnail evidence. Không nhận đã xem toàn bộ animation/hear soundtrack hoặc biết Analytics. Xem [channel-research.md](channel-research.md).

| Mẫu / báo cáo toàn văn | Cue | SRT duration | Word tokens | Characters joined | WPM |
|---|---:|---|---:|---:|---:|
| [Barbarossa](cases/barbarossa.md) | 705 | 26:41.440 | 4.434 | 25.353 | 166,13 |
| [Midway](cases/midway.md) | 887 | 35:33.414 | 5.833 | 33.318 | 164,05 |
| [Deadliest Battles](cases/deadliest-battles.md) | 706 | 26:59.320 | 4.408 | 25.111 | 163,33 |
| [Pacific Turning Point](cases/pacific-turning-point.md) | 807 | 32:56.867 | 5.266 | 29.936 | 159,83 |
| [Stalingrad](cases/stalingrad.md) | 620 | 26:00.720 | 4.164 | 23.243 | 160,08 |
| [Eastern Front](cases/eastern-front.md) | 952 | 36:37.119 | 6.311 | 36.018 | 172,34 |

Word method: Unicode tokens, giữ apostrophe/hyphen nội từ; không sửa ASR hoặc loại noise trước đếm. Characters là cue text nối bằng một khoảng trắng, không phải byte count của SRT. WPM từ words/mốc cuối; không measured voice speed. Duration toàn video trên thumbnail có thể khác subtitle coverage.

## 1. Đơn vị thật sự của câu chuyện

Các mẫu không chỉ kể “sau đó chuyện gì xảy ra”. Đơn vị thường là **một assumption gặp constraint hoặc evidence**, dẫn tới decision, consequence rồi thay đổi trạng thái. Ở anthology, đơn vị là một mechanism khiến loss lớn theo một criterion. Ở overview, đơn vị là phase đổi balance of capability/initiative.

Nhờ vậy, câu chuyện giữ được question xuyên hàng chục phút. Detail không cần nhiều vì nó nổi tiếng; nó phải giúp hiểu choice, capacity, myth hoặc human cost. Đây là tiêu chuẩn quyết định có nên giữ facts trong draft mới.

## 2. Bốn backbone đã quan sát, không một công thức chung

**Barbarossa:** decision/prewar investigation; paradox trade dependency; warnings hội tụ vào giờ mở. Kết phân biệt Đức chọn xâm lược và Soviet có thể chuẩn bị tốt hơn. Không cover toàn bộ campaign năm 1941 chỉ vì title là Barbarossa.

**Stalingrad:** outcome cold open → oil objective → mission drift → hai decision chains → tactical trap/airlift/hold orders → surrender/cost → limits of avoidability. “Không tại city này/quy mô này” khác “không có chiến tranh”.

**Midway:** outcome clock → long plan/intelligence/repair/scouting chain → battle clock and hard fork → physical climax → intellectual myth audit → counterstrike/bill → conditional verdict. Nó có hai cao trào, không chỉ bombs.

**Pacific:** industrial disparity → competing answers → eight candidates/gauge → state changes → layered verdict. Mỗi candidate phải đóng một causal role khác, không chỉ kể battle nổi tiếng.

**Deadliest:** tease extremes → counting rules → ba hệ đo/xếp hạng → mini narratives → callbacks khi battle quay lại → scale/human cost. Một trận xuất hiện lại không được cộng casualty lần hai vào total.

**Eastern Front:** geography/scale → toàn timeline → strategic/operational/human lens → logistics motif → reversals/adaptation → terminal campaign → promises/cost. Hai người lính và con ngựa là devices của mẫu; SRT không đủ chứng minh họ là hồ sơ thật. Skill mặc định không phát minh counterparts.

## 3. Intro: những nhịp thật sự làm việc

Các intro cho trước kết quả hoặc scale, rồi tạo khoảng trống giải thích. Question thường không là “ai thắng?” mà “vì sao choices lại tạo kết quả này?” hoặc “tiêu chí nào mới xác định turn/deadliest?”.

Barbarossa 00:00–00:46 đi từ giờ/ngày → quân vượt biên → scale → không tất yếu → tàu ngũ cốc nghịch lý. Lời hứa/rewind và đoạn đùa tên chiến dịch kéo tới khoảng 01:11. Stalingrad mở promotion trong basement, giải ý nghĩa, surrender, rồi thu hẹp nghĩa avoidable trước rewind vào oil. Midway mở 10:22 và carriers cháy, thách explanation luck/five minutes, tease planning/intelligence/failures cả hai phía rồi gài clock payoff.

Pacific 00:00–01:02 đi từ carrier-production contrast → câu hỏi khi nào Nhật mất → các đáp án cạnh tranh → gauge/eight candidates. Rules còn được triển khai rõ sau context; không đo intro chỉ bằng câu “this is…”. Deadliest intro và counting contract đến khoảng 01:30 đặt casualties/killed, ranges và ba rankings. Eastern 00:00.080–01:21.040 dùng geography → loss scale → khoảng trống hiểu biết phương Tây → scope/human lenses/motifs → promise.

Điều chuyển vào skill: anchor/stakes/contradiction/question/promise/method. **Không** giữ mọi intro đúng 60 giây hoặc mở bằng cùng một câu. Cold-open ngắn khác narrative contract hoàn chỉnh. Những chi tiết giác quan/hội thoại không xác minh trong sample không là permission bịa ở bài mới.

## 4. Context có chức năng và điểm dừng

Context giải objectives/constraints để judgment có nghĩa. Barbarossa trade trước ideology/decision; Stalingrad oil trước city; Midway carrier problem trước battle; Pacific baseline resource war trước candidates; Deadliest measurement trước numbers; Eastern pact/initial expectations trước invasion.

Sau context, listener phải biết kế hoạch cần điều gì đúng và yếu tố nào nằm ngoài kiểm soát. Nếu thêm quá khứ không đổi question, cắt. Mốc lùi bắt đầu tùy topic, không mặc định kể từ đầu thế kỷ.

## 5. Hai phía: bất cân xứng thông tin và agency

Hai phía không chia đôi word count. Đổi perspective tại lúc phía kia cho thấy implication của choice vừa kể. Midway đưa Hypo sau khi người nghe hiểu Nhật dựa vào surprise; repair readiness tạo dramatic irony khi Tokyo vẫn tin một carrier vắng. Barbarossa cho biết cả cảnh báo phía Soviet lẫn phản đối phía Đức, nhưng final responsibility không đối xứng.

Skill cần hai cards: knowledge believed then và opposing action actually occurring. Không bên thắng hoàn hảo, không bên thua toàn incompetent. Enemy agency, systems và chance có thể khiến mistake mang hậu quả ngược kỳ vọng. Narrator có hindsight; actor không tự có.

## 6. Material objects là bộ nhớ của bài

Tàu ngũ cốc/Lützow, fuel, carrier-deck cycles, gauge, casualty tower và horse logistics làm facts trừu tượng nhìn được. Object được giới thiệu, giải mechanism, trở lại ở payoff. Không phải tất cả đều cần mascot/visual gag.

Skill chọn object thuộc topic mới và có source. Audio-only listener vẫn hiểu: verbal state updates thay “look at this”. Không lấy Carl/Alexi/Greta, accountant hoặc cùng joke của sample làm assets chung cho bài mới.

## 7. Loop và reveal

Có ba loop: **information** (vật/chi tiết sẽ trở lại), **causal** (tại sao choice dẫn đến outcome), **evaluation** (candidate/fork được phán thế nào). Loops có ledger riêng; trả nợ đúng block, không rải curiosity gaps không closure.

Midway gài war-game/codes/clock trong opening, payoff ở các đoạn khác nhau; một fork Nagumo được trình bày có arguments rồi dùng cho CTA. Barbarossa “remember the ship/city/name” trở thành callbacks có meaning. Eastern promises về logistics/photo/date cần được trả ở timeline thích hợp. Skill không cố ý giữ answer chính đến cuối nếu đã đủ rõ; suspense nằm ở reasoning.

## 8. Nhịp macro và micro

Macro: setup chậm hơn để hiểu system; chronology sát hơn khi clock/tactical interaction là mechanism; pause ở contested verdict/human cost; ending hội tụ. Micro: concrete scene/detail → fact/constraint → short analytical hinge → next question. Câu ngắn đóng ý sau câu vừa/dài tạo biến thiên.

Mẫu có thoại/cartoon pauses nhưng SRT không đủ xác định hiệu quả dựng/sound. Skill chuyển những functions thành prose/oral clarity; không tự gán hiệu ứng âm thanh. WPM metadata khoảng 160–172 là mô tả sample, không command user phải đọc nhanh.

## 9. Số liệu tạo logic, không chỉ shock

Trade share giải dependency; repair days vs deadline giải improvisation; search coverage/deck cycles giải operational choices; production giải capacity; casualty windows giải ranking. Số được đặt trong context rồi giải implication.

Những lỗi/rủi ro của sample cần tránh: killed/casualties chưa hoàn toàn cùng basis trong Deadliest; denominators và windows khác; repeated battle có risk overlap; totals của scoreboard không đọc rõ mọi ticks; aircraft/carrier/aircrew thay thế không cùng loại; witness number có thể sai nhưng vẫn evidence perception. Một source quote sai phải được giải là belief, không recite thành fact.

## 10. Research và certainty

Mẫu có những markers như reported, estimates, disputed accounts và historians differ. Điểm mạnh là có lúc sửa myth, tách documentary records khỏi memoir và cho disputed fork fair hearing. Điểm yếu là ASR/name corruption và dialog không phân biệt quote/reconstruction rõ.

Skill mới tạo separate claim/quote/counterfactual registers, không lấy script video làm authority. Narrator có thể nêu debate bằng natural attribution; source ledger ngoài narration. “Reportedly” chỉ dùng khi có source cho report. Không gọi mọi tài liệu là unanimous hoặc authentic nếu chưa đọc provenance.

## 11. Cao trào không đồng nhất với battlefield destruction

Barbarossa là warnings/commitments hội tụ vào invasion clock. Stalingrad là những cửa escape đóng lại và thảm họa cuối. Midway physical climax rồi intellectual debunk; cả hai payoff setup. Pacific là comparison đủ để xác định nghĩa “turn”; Deadliest là scale/criterion reversal; Eastern là terminal campaign đã được chuẩn bị bằng system imbalance.

Skill đặt trước climax state change nào cần chứng minh. Không tăng drama bằng adjective mà bỏ evidence. Giữ aftermath nếu nó sửa hiểu lầm về thắng/loss hoặc cho thấy capacity nào mất không thay được.

## 12. Ending: trả question, trả motif, giữ limits

Avoidable verdict không cộng số ticks thành causal/moral score. Barbarossa khoảng 24:03–24:23 explicitly tách Soviet failure to prepare khỏi German choice to invade; Stalingrad khoảng 24:54–25:49 giới hạn scope của “avoidable”. Midway gần 33:54–35:00 cân systems/individual/chance rồi trả clock opening. Pacific kết cần giữ một initiative criterion; xem case để thấy wording drift đáng sửa. Anthology/overview ending đưa scale trở lại human meaning và closes promises.

CTA là optional, ngắn, có thể hỏi một fork/candidate đã supported. Không cho question comment thay answer chính; không hứa upload kế tiếp chưa giao. Moral/human-cost tone xuất phát evidence/scope, không thêm sermon generic.

## 13. Những gì học từ triển khai Abooks

Đã đọc SKILL.md và toàn bộ bảy references của `abooks-script-rewriter`: style, source safety, narrative, length, rubric, TTS, lessons. Giữ phần hữu ích: đọc đầy đủ nguồn cốt lõi trước thesis; Source/Research Bible rồi Narrative Bible; thought blocks; min/target/max budgets; cluster writing cùng narrator; ledger/checkpoint; source audit; semantic repetition; length controller; oral pass; TXT; counts file thực; không outsource qua external AI API.

Những phần đổi có lý do:

- Abooks **rewrite Vietnamese từ nguồn user**, nên cấm facts mới và web; skill này **new researched English từ title**, nên cần tìm nguồn mới có evidence ledger. Không áp source-only prohibition sai nhiệm vụ.
- Abooks yêu cầu nguồn + target; skill mới chỉ title, default length hợp lý và optional overrides, không thêm vòng intake phiền.
- Abooks explanatory self-reflection arc không phù hợp mọi war genre; skill mới có bốn demonstrated blueprints và inquiry extensions có nhãn.
- Budget intro/ending Abooks 8–12% không bê máy móc; documentary hook/promise gọn, core mechanism nặng, verdict tùy format.
- TTS English dùng English names/dates/abbreviations và sentence rhythm; không bê mọi quy tắc đọc số tiếng Việt.
- Nhiều perspectives và counterfactual cần anti-hindsight, scope, attribution và false-equivalence checks.

## 14. Những điều không lấy từ mẫu

Không copy distinctive prose/catchphrases; không làm mọi video có accountant; không bịa historical dialogue/human biographies; không luôn có eight candidates/three rankings/two soldiers; không phải every choice a mistake; không lấy absolutes marketing làm fact; không đếm ticks như trách nhiệm; không giả channel Analytics hoặc documentary style đã chứng minh retention.

## 15. Dùng synthesis thế nào

Khi viết: đọc phần backbone + style/research + case liên quan khi cần finer examples. Khi nghiên cứu sâu phong cách: mở sáu cases, mỗi file có intro nhịp nhỏ, full timeline cue/timestamps, rhetorical devices, loops/callbacks, climax/ending và caveats. Khi kiểm skill: thử title mới đúng một genre, xem nó chọn structure, tự tìm evidence và giữ final TXT sạch, không chỉ pass YAML.
