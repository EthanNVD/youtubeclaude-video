# Chương mẫu "nhiều hành động" — WW1, đoạn 599,4–722,7 s (Verdun → xe tăng đầu tiên)

Video: `out/ww1-action-test.mp4` (2:04). Kịch bản cảnh: `plan_src/build.py`.

## Tỉ lệ thời lượng (đo trên plan, cùng đoạn lời thoại)

| loại | bản WW1 đã xuất (đoạn này) | chương mẫu | mục tiêu chương chiến trận |
|---|---|---|---|
| cảnh có lính/xe (bản cũ: nhiều cảnh trong đó là đứng yên, co rúm) | 43% | **74%** (đều có chuyển động: đi, chạy, bắn, ngã, khiêng) | 55–60%+ |
| tướng đứng nói/phản ứng | 18% | 9% (Falkenhayn, Brusilov) | ≤ 10% |
| bản đồ | 15% | 10% (3 bản đồ ≤ 4,6 s) | ~10% |
| tài liệu/biểu đồ/bia tưởng niệm | 24% | 8% | ≤ 10% |

## Thêm vào engine (dùng chung cho mọi phim)
- `fallAt` / `fallDir` (người): trúng đạn → ngã nghiêng quanh bàn chân, nảy nhẹ, nằm lại (không máu).
- `silhouette: true` (mọi phần tử): bóng đen ngược sáng cho cảnh hoàng hôn/bình minh.
- Xe/pháo `fireAt: [t…]`: chớp lửa đầu nòng, khói nở, giật lùi; tự gắn tiếng pháo.
- Người cầm súng `fireAt: [t…]` (bắn từng phát) hoặc `fire: [từ, đến, chu kỳ]` (súng máy liên thanh): chớp lửa đúng đầu nòng súng trường.
- Cảnh `impacts: [t…]`: camera giật theo từng tiếng nổ.
- Bối cảnh `nomansland` (vùng đất không người WW1: hố bom đọng nước, gốc cây gãy, cọc dây thép gai, cột khói chân trời; `time`, `weather: snow`, `horizon` để làm cảnh bóng đen trên đỉnh dốc).
- Hiệu ứng `shellburst` (cột đất bốc lên rồi rơi xuống), đạo cụ `stretcher` (cáng).

## Công thức hành động đã dùng
OVER_TOP (trèo khỏi chiến hào, tiến vào chiều sâu theo hàng so le, vài người ngã) · GUN_CREW (lính nạp đạn ôm đạn pháo tới, pháo bắn, cả tổ bịt tai) ·
WAVE (đợt xung phong ngang chiến trường, theo máy người dẫn đầu) · UNDER_FIRE (kẹt trong hố, đạn nổ dần lại gần, liên lạc viên chạy qua) ·
HIT (trúng đạn, đồng đội chạy tới) · SILHOUETTE (khiêng cáng trên đỉnh dốc lúc hoàng hôn, thập tự hiện dần) · RAIL (lên tàu, tàu chạy) ·
MG_NEST (tổ súng máy sau bao cát) · AFTERMATH (cánh đồng sau trận, người sống sót đi về) · TANK (xe tăng bò tới, lính bỏ chạy).
Con số đặt LÊN cảnh hành động (bộ đếm thương vong chạy trên đầu đợt tấn công) thay vì cắt sang biểu đồ.

## Nếu duyệt → cập nhật repo/skill
1. `tools/shotlib.py`: thêm các hàm công thức trên (assault, gun_crew, mg_nest, stretcher_team, silhouette_ridge, aftermath, tank_breakthrough).
2. Validator: cảnh báo theo chương khi hành động < 35% (chương chiến trận < 55%), cảnh nói > 5 s không có "việc tay", bản đồ > 12 s.
3. Skill/docs: bảng tỉ lệ, quy tắc "ai/cái gì đang làm gì trong khung hình này?", lệnh → hậu quả ngoài chiến trường, con số đặt trên cảnh hành động.
4. ROADMAP, CHANGELOG.
