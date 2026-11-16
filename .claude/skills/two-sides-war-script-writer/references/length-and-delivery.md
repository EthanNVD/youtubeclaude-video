# Length, checkpoints và bàn giao

## Hợp đồng đếm

Default 4.800 English words, hard range 95–105% (4.560–5.040), preferred 98–102% (4.704–4.896). Nếu user cho words, dùng words; nếu characters, dùng characters gồm spaces/newlines Unicode code points sau khi chuẩn newline; nếu minutes, thiết kế words bằng reading rate đã nêu. User explicit hard exact/range thay defaults. Không gọi một count thiếu 30% là hoàn thành.

Default 4.800 chỉ áp dụng `new_from_title`. Với `rewrite_same_structure`, không target thì nguồn tiếng Anh lấy số từ lời kể gốc làm target, giữ mức chi tiết và tỷ trọng beats; nguồn khác ngôn ngữ giữ coverage/phân bổ và ước lượng budget output, không ép count hai ngôn ngữ bằng nhau. Xem [source-structure-rewrite.md](source-structure-rewrite.md). User đổi length không tự cho phép đổi sườn.

Duration là estimate, không đo audio. Default 160 words/minute; sáu ASR samples khoảng 160–172 theo token method trong manifest. TTS giọng/pauses có thể khác. Với user yêu cầu duration nghiêm ngặt, cần đo giọng đọc/track thực và sửa; narration TXT một mình không chứng minh audio duration.

Character target không chuyển qua word ratio cứng. Budget mỗi block đúng đơn vị user. Script report gồm raw/logical character counts và method; đừng so Windows byte count với Unicode char count. Không đưa heading/source notes vào count lời kể.

## Budget

Mỗi block min/target/max và reason. Khởi đầu theo blueprint, điều chỉnh theo complexity. Example design 4.800: hook+promise 190, contextual contract 480, core reasoning 3.120, climax/verdict 800, closure/CTA 210 = 4.800. Đây là template phân bổ, không measured ratio bắt buộc.

Với pilot ngắn user yêu cầu, gom macro stages thành vài chức năng và giảm số forks/candidates thay vì rút đều mọi phần thành một câu. Giữ central question, ít nhất một alternative có chứng cứ và cost, opposing response/mechanism, rồi qualified verdict. Pilot ngắn chỉ kiểm override và pipeline ở phạm vi đó; không chứng minh coherence của bài 30 phút hoặc resume sau một lần ngắt thật.

## Viết và lưu

Với >=20.000 characters hoặc nhiều clusters, tạo scratch ngay trước draft; viết bằng assistant và file-edit tools. Sau mỗi cluster đếm và cập nhật ledger. Bị ngắt thì resume, không rewrite toàn bài. Cơ học ghép/sao chép được; không external AI API/model hoặc hardcoded generator.

Thiếu target: tìm unanswered mechanism/fork/counterargument/context thực sự cần, research bổ sung nếu cần, phân bổ deficit. Không paraphrase cùng ý để padding. Thừa: cắt lặp, detail không đổi question, quotes dài, intro promise trùng; giữ evidence-bearing sentences và bridges. Mỗi patch factual/oral review rồi đếm lại. Nếu evidence không đủ cho length, giao limitation đúng và phạm vi khả thi, không bịa.

Các cách bổ sung research/candidate/fork ở trên dành cho bài mới. Nhánh viết lại chỉ mở rộng làm rõ ý đã có trong beat tương ứng; rút câu/lặp diễn đạt mà không bỏ khâu diễn biến hoặc di chuyển reveal. Target không khả thi trong giới hạn này thì báo đúng xung đột, không phá sườn để đạt count.

## File output

- `<slug>_script_en.txt`: UTF-8, words to speak only, đoạn văn liền mạch; mỗi câu thoại là một đoạn riêng không nhãn; chỉ đổi suffix nếu user đổi language.
- `<slug>_script_en_tagged.txt`: cùng nội dung, mỗi đoạn có tiền tố `NARRATOR:` / `HOST_A:` / `HOST_B:` / `<NAME> [QUOTE|REPORTED|DRAMATIZED]:` (channel-formula §12); kiểm khớp bằng `script_metrics.py --tagged`.
- `<slug>_sources.md`: bibliography, key claims/locators, disputes, scope và editorial caveats có tác động thực tế.
- Working/scratch giữ riêng để resume. User yêu cầu một file thì chỉ giao TXT, sources internal.
- Slug tương đối ngắn, filesystem-safe, không ghi đè; trùng thì `_2`, `_3`.
- Final chat ngắn: structure, words/characters, estimated duration/rate, status và links. Không dán full long script.

## Công cụ đếm

`python scripts/script_metrics.py <absolute-script-path> --target-words 4800 --rate 160 --json <report-path>`

Hoặc `--target-characters 30000`; không dùng cả hai target nếu brief chỉ có một. `--tolerance 0.05` mặc định; exact có thể 0. Script check mechanical residue, sentence length, duplicate paragraph, metrics; warnings cần người viết đọc sửa. Nó không chứng minh source fidelity/TTS quality/history.
