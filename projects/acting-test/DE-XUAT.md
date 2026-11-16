# Đề xuất: diễn hoạt + camera (bản thử 1 phút, nhánh `exp/acting-camera`)

## Vì sao bản Market Garden v2 "chán" (đo trên plan)
- 254 cảnh / 34 phút, **mỗi cảnh = 1 góc máy đứng yên ~8 s** (chỉ 21/254 cảnh có camera chủ động; còn lại là drift 4%).
- 84 cảnh không có người, 95 cảnh chỉ 1 người; cả phim chỉ 15 lần nhân vật đi lại.
- Mọi khung là **toàn thân, chính diện, cùng tầm mắt**; không có cận mặt, không qua vai, không insert tay/đồ vật.
- Hành động được **viết bằng nhãn chữ** ("REQUEST: RECONNAISSANCE FLIGHTS") thay vì cho nhân vật làm.
- Nhân vật đứng xếp hàng nhìn camera, không tương tác với nhau, đổi biểu cảm "bụp" không có phản ứng.

## Mẫu làm khác thế nào (repo ethanNVD — nghiên cứu khung hình; video mẫu)
- Một nơi chốn được quay bằng **nhiều shot nối bằng hard cut**: rộng → cận phản ứng → insert vật → rộng. Cận mặt *trước* sự kiện, giữ phản ứng đủ đọc.
- Camera phần lớn đứng yên nhưng **đổi cỡ cảnh liên tục**; có pan theo vật chuyển động, người đi trong hành lang (nền trôi), lật panel để chuyển cảnh.
- Đạo cụ là bằng chứng: tay cầm bút gạch chữ, kính lúp trên ảnh, đồng hồ chạy, mẫu giấy được đóng dấu.
- Repo mẫu tự ghi: "thêm keyframe camera **không** tự là thêm diễn xuất" — phải có pha *chuẩn bị → hành động → kết quả → phản ứng*.

## Học từ repo opus-video-skills (painted-animation)
- **"Reads"**: mỗi shot liệt kê điều người xem phải hiểu theo thứ tự; *mỗi lúc một điều*; hành động nhanh, ý nghĩa thì giữ lâu; độ dài shot do reads quyết định.
- **Nhân vật to**: trung cảnh / cận cảnh là mặc định; người nhỏ giữa khung rộng chỉ để mở cảnh.
- **Đổi biểu cảm có "take"** (nheo/nén → bật → lắng), không đổi mặt tức thì.
- **View 3/4** cho hội thoại; tránh "twinning" (hai tay/đám đông cử động giống hệt).
- Vòng soát: xem **strip từng frame** ở động tác/chuyển cảnh, **crop** mặt/tay — không chỉ ảnh giữa cảnh.
- Không áp dụng: cấm chữ (thể loại mình cần date badge/nhãn), màu nước, cắt theo nhạc.

## Đã thêm vào engine (chỉ trên nhánh thử)
| tính năng | dùng trong plan |
|---|---|
| `scene.shots` — nhiều shot trong một cảnh, khung theo nhân vật (`wide/full/medium/mediumclose/close/ecu`), `frameX`, `push`, `pan`, `track` (camera bám người), nhóm 2 người | coverage: rộng → trung → cận bằng hard cut |
| `turn` −1..1 — mặt quay 3/4 | hội thoại, qua vai |
| take khi đổi `expr` | phản ứng có lực |
| đi về phía/xa camera (key `y`) | hành lang, rời đi trong mưa |
| `front: true` — đồ vật nằm trên bàn tiền cảnh, người qua vai | bàn làm việc, OTS |
| props `photo` (ảnh trinh sát), `magnifier`, `suitcase`; element `viewfinder` (khung máy ảnh F24 + chớp) | insert bằng chứng |

## Đoạn thử: 15:29–16:28, 22 shot, trung bình 2,7 s/shot (bản cũ: 8 shot, 7,4 s/shot)
Sau khi bạn duyệt: cập nhật SKILL (bước "reads" + coverage bắt buộc cho cảnh diễn), shotlib (template coverage), validator (cảnh > 6 s không có shot/cut, tỉ lệ cận cảnh), STYLE_GUIDE, QUALITY, ROADMAP, CHANGELOG; rồi merge vào `main`.
