#!/usr/bin/env python3
"""Kiem tra kich ban Krishnamurti kieu ABooks.

Do dai, nhip cau, loi cam/TTS, dau hieu nhap vai, trich dan, ho an du gat,
lap y, tua chang va moc thoi gian uoc tinh, tu khoa, goi YouTube.

  python -I k_check.py BAN.txt [--min 50000 --max 60000] [--cpm 890]
         [--keywords "krishnamurti,thoi gian tam ly"] [--seo youtube.txt]
         [--source file_doi_chieu.txt] [--asr]
"""
import argparse
import collections
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding="utf-8")

BANNED = [
    # cau co dinh cua kenh va loi keu goi (nguoi dung chot: bo het trong kich ban)
    "bạn đang nghe", "trước khi vào bản review", "trước khi đi vào phần review",
    "hãy mua sách", "mua và đọc", "ủng hộ tác giả", "tìm mua", "để lại bình luận",
    "phần bình luận", "đăng ký kênh", "nhấn like", "bấm like", "nhấn chuông",
    "video tiếp theo", "video tới", "trong video này", "hôm nay chúng ta sẽ",
    # cum noi bo
    "theo nguồn", "trong nguồn", "bản gốc nói", "kịch bản gốc", "fact ledger", "bible",
    # dau van tay cua video mau
    "phẫu thuật tâm lý không gây mê", "khối u đã di căn", "giữ chặt ghế",
    "cuốn sách nguy hiểm nhất thế kỷ", "đánh cắp ngày mai", "cái rìu phá tan",
]
# dau hieu nguoi dan noi nhu Krishnamurti
IMPERSONATION = [
    r"\bngười ta hỏi tôi\b", r"\bmột người hỏi tôi\b", r"\bhọ hỏi tôi\b", r"\bai đó hỏi tôi\b",
    r"\btôi nói với họ\b", r"\btôi trả lời\b", r"\btôi đã gặp (hàng|vô số|rất nhiều)",
    r"\btôi đã đi qua\b", r"\bđừng gọi tôi là thầy\b", r"\btôi không phải là (thầy|đạo sư)",
    r"\bthưa ông\b", r"\btôi không có gì để (dạy|bán)\b", r"\bkhi tôi còn (nhỏ|là cậu bé)",
]
METAPHOR_FAMILIES = {
    "y khoa": ["phẫu thuật", "dao mổ", "khối u", "di căn", "gây mê", "liều thuốc"],
    "đòn đánh": ["nhát dao", "cú tát", "cú đấm", "đòn trí mạng", "gáo nước lạnh"],
    "lửa/phá hủy": ["đốt trụi", "thiêu rụi", "giật sập", "đập tan", "xé toạc"],
    "vực/bóng tối": ["vực thẳm", "tâm bão", "nấm mồ"],
}
HEAVY_ADJ = ["tàn khốc", "trần trụi", "tàn nhẫn", "khủng khiếp"]
TIC_PHRASES = ["hãy tưởng tượng", "hãy hình dung", "điều này không có nghĩa", "nói cách khác",
               "thực chất", "chính là", "bạn có thấy", "thật ra"]
SYMBOLS = re.compile(r"[%&@=<>#*_~^|\\/\[\]{}]|\.{3}|…|!!|\?\?|https?://|\b\d{1,2}/\d{1,2}\b")
QUOTE = re.compile(r"[\"“”]([^\"“”]{3,400})[\"“”]")


def norm(t):
    return unicodedata.normalize("NFC", t)


def join_asr(t):
    t = re.sub(r"\[\d\d:\d\d:\d\d\]|\[âm nhạc\]|&gt;&gt;|>>", "", t, flags=re.I)
    return re.sub(r"\s*\n\s*", " ", t).strip()


def sentences(t):
    flat = re.sub(r"\s+", " ", t)
    return [s.strip() for s in re.split(r"(?<=[.?!])\s+", flat) if s.strip()]


def tokens(t):
    return re.findall(r"\w+", t.lower())


def ngrams(ws, n):
    return [" ".join(ws[i:i + n]) for i in range(len(ws) - n + 1)]


def mmss(chars, cpm):
    sec = int(round(chars / cpm * 60))
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def check_seo(path):
    t = norm(open(path, encoding="utf-8").read())
    print("\n=== GOI YOUTUBE ===")
    titles = [x.strip() for x in re.findall(r"^TIÊU ĐỀ \d+:\s*(.+)$", t, re.M)]
    for x in titles:
        n = len(x)
        flag = "DAT" if 50 <= n <= 85 else ("CHAP NHAN" if 45 <= n <= 100 else "NGOAI DAI")
        k40 = "krishnamurti" in x[:40].lower()
        print(f"  [{n} ky tu, {flag}, ten trong 40 ky tu dau: {'co' if k40 else 'KHONG'}] {x}")
    if len(titles) != 3:
        print("  CAN DUNG 3 TIEU DE, dang co", len(titles))
    m = re.search(r"^MÔ TẢ:\s*\n(.*?)(?=^HASHTAG:|^TAG:|^GHI CHÚ|\Z)", t, re.M | re.S)
    if m:
        d = m.group(1).strip()
        b = len(d.encode("utf-8"))
        flag = "VUOT 5000 BYTE" if b > 5000 else ("DAT" if 900 <= len(d) <= 2400 else "XEM LAI DO DAI")
        print(f"  Mo ta: {len(d)} ky tu, {b} byte -> {flag}")
        print(f"  ~150 ky tu dau: {d[:150]}")
        print(f"  Co ten Krishnamurti trong 300 ky tu dau: {'co' if 'krishnamurti' in d[:300].lower() else 'KHONG'}")
        stamps = re.findall(r"^\s*(\d{1,2}:\d{2}(?::\d{2})?)\s*[–-]", d, re.M)
        print(f"  Moc thoi gian: {len(stamps)} {'(dong dau 00:00)' if stamps and stamps[0] in ('00:00', '0:00') else '(THIEU 00:00 hoac khong co)'}")
        print(f"  Dong 'Tu lieu': {'co' if re.search(r'^Tư liệu:', d, re.M) else 'KHONG'}")
        for bad in ["like, subscribe", "subcribe", "osho", "eckhart", "luật hấp dẫn", "tần số rung động"]:
            if bad in d.lower():
                print(f"  CANH BAO trong mo ta: '{bad}'")
    else:
        print("  KHONG THAY 'MÔ TẢ:'")
    h = re.search(r"^HASHTAG:\s*(.+)$", t, re.M)
    if h:
        hs = re.findall(r"#\w+", h.group(1))
        print(f"  HASHTAG: {len(hs)} -> {'DAT' if 5 <= len(hs) <= 7 else 'NEN 5-7'} {hs[:3]} (3 cai dau hien tren tieu de)")
    g = re.search(r"^TAG:\s*(.+)$", t, re.M)
    if g:
        tags = [x.strip() for x in g.group(1).split(",") if x.strip()]
        total = len(",".join(tags)) + 2 * sum(1 for x in tags if " " in x)
        ok = 15 <= len(tags) <= 20 and total <= 500
        print(f"  TAG: {len(tags)} tag, ~{total} ky tu theo cach YouTube tinh -> {'DAT' if ok else 'CAN 15-20 TAG, <=500 KY TU'}")
        low = [x.lower() for x in tags]
        dup = sorted({x for x in low if low.count(x) > 1})
        if dup:
            print("  Tag trung:", dup)
        for bad in ["osho", "eckhart", "luật hấp dẫn", "tần số", "minh niệm"]:
            if any(bad in x for x in low):
                print(f"  CANH BAO tag an theo: '{bad}'")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--min", type=int, default=50000)
    ap.add_argument("--max", type=int, default=60000)
    ap.add_argument("--cpm", type=float, default=890.0, help="ky tu moi phut doc (mau ABooks ~890)")
    ap.add_argument("--asr", action="store_true", help="file phu de/transcript chua ghep dong")
    ap.add_argument("--keywords")
    ap.add_argument("--seo")
    ap.add_argument("--source", help="van ban doi chieu de do ty le trung cum 8 tu")
    a = ap.parse_args()

    raw = norm(open(a.draft, encoding="utf-8").read())
    text = join_asr(raw) if a.asr else raw
    chars = len(text)
    low = text.lower()
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    sents = sentences(text)
    wl = [len(s.split()) for s in sents]
    words = len(text.split())

    print("=== DO DAI ===")
    st = "DAT" if a.min <= chars <= a.max else (f"THIEU {a.min - chars:,}" if chars < a.min else f"THUA {chars - a.max:,}")
    print(f"Ky tu: {chars:,} | dai {a.min:,}-{a.max:,} -> {st}")
    print(f"Tu: {words:,} | doan: {len(paras)} | cau: {len(sents)} | uoc luong doc ~{chars / a.cpm:.0f} phut @ {a.cpm:.0f} ky tu/phut")

    print("\n=== NHIP CAU === (muc tieu: TB 14-18 tu, hoi 7-12%, <=4 tu 4-8%, >30 tu <=10%, >45 tu = 0)")
    if sents:
        q = sum(1 for s in sents if s.endswith("?"))
        longs = [(n, s) for n, s in zip(wl, sents) if n > 30]
        print(f"TB {sum(wl) / len(wl):.1f} tu/cau | hoi {q / len(sents) * 100:.1f}% | <=4 tu {sum(1 for w in wl if w <= 4) / len(sents) * 100:.1f}% | >30 tu {len(longs) / len(sents) * 100:.1f}%")
        run, worst = 0, 0
        for s in sents:
            run = run + 1 if s.endswith("?") else 0
            worst = max(worst, run)
        print(f"Chuoi cau hoi lien tiep dai nhat: {worst} {'(QUA 4)' if worst > 4 else ''}")
        over45 = [s for n, s in longs if n > 45]
        for s in over45[:10]:
            print(f"  CAU >45 TU PHAI TACH: {s[:160]}")
        one_word = sum(1 for s in sents if len(s.split()) <= 2)
        print(f"Cau 1-2 chu ('Khong.', 'Sai.'): {one_word} (~{chars / max(1, one_word):,.0f} ky tu moi cau; nen >= 3.000)")

    print("\n=== LOI CAM / TTS ===")
    hits = [(b, low.count(b)) for b in BANNED if b in low]
    print("Cum cam:", hits if hits else "khong")
    sym = collections.Counter(m.group(0) for m in SYMBOLS.finditer(text))
    print("Ky hieu kho doc:", dict(sym) if sym else "khong")
    dg = collections.Counter(re.findall(r"\d+", text))
    print("Chu so (kiem tra cach doc):", dict(dg.most_common(20)) if dg else "khong")
    print("Markdown/heading:", "CO" if re.search(r"^\s*(#|-|\*|•|►|\d+\.)\s", text, re.M) else "khong")

    print("\n=== NGOI KE (phai = 0) ===")
    imp = []
    for pat in IMPERSONATION:
        for m in re.finditer(pat, low):
            imp.append(text[max(0, m.start() - 60): m.end() + 60].replace("\n", " "))
    print(f"Dau hieu nhap vai Krishnamurti: {len(imp)}")
    for x in imp[:12]:
        print(f"  ...{x}...")
    k_first = low.find("krishnamurti")
    print(f"Ten 'Krishnamurti': {low.count('krishnamurti')} lan, lan dau o {k_first / max(1, chars) * 100:.1f}% bai" if k_first >= 0 else "KHONG NHAC TEN KRISHNAMURTI")

    print("\n=== TRICH DAN (moi cau trich phai co trong Ledger, < 15 chu, toi da 4) ===")
    quotes = [q.strip() for q in QUOTE.findall(text)]
    print(f"So doan trong ngoac kep: {len(quotes)}")
    for qt in quotes[:20]:
        n = len(qt.split())
        print(f"  [{n} chu{' - QUA DAI' if n >= 15 else ''}] {qt[:140]}")

    print("\n=== DO GAT: HO AN DU (tran 3/ho) VA TINH TU NANG (tran 4/tu) ===")
    for fam, ws in METAPHOR_FAMILIES.items():
        c = {w: low.count(w) for w in ws if low.count(w)}
        tot = sum(c.values())
        print(f"  {fam}: {tot} {'QUA TRAN' if tot > 3 else ''} {c if c else ''}")
    for w in HEAVY_ADJ:
        n = low.count(w)
        if n:
            print(f"  '{w}': {n} {'QUA TRAN' if n > 4 else ''}")

    print("\n=== TUA CHANG (doan 1 cau, 3-14 tu, khong hoi) VA MOC THOI GIAN UOC TINH ===")
    pos = 0
    heads = []
    for p in re.split(r"(\n\s*\n)", text):
        if p.strip() and "\n" not in p.strip():
            ps = sentences(p)
            if len(ps) == 1 and 3 <= len(p.split()) <= 14 and not p.strip().endswith("?"):
                heads.append((pos, p.strip()))
        pos += len(p)
    print(f"So tua chang: {len(heads)} (muc tieu 7-10)")
    print(f"  00:00 - [cau moi / mo bai]")
    for ps, h in heads:
        print(f"  {mmss(ps, a.cpm)} - {h.rstrip('.')}   ({ps / max(1, chars) * 100:.0f}%)")

    print("\n=== LAP ===")
    tk = tokens(text)
    c8 = collections.Counter(ngrams(tk, 8))
    rep = sorted([(g, n) for g, n in c8.items() if n > 1], key=lambda x: -x[1])
    print(f"Cum 8 tu lap lai: {len(rep)}")
    for g, n in rep[:12]:
        print(f"  x{n}: {g}")
    openers = collections.Counter(" ".join(p.split()[:2]).lower() for p in paras)
    print("Mo doan hay dung (>2):", [(k, v) for k, v in openers.most_common(10) if v > 2])
    for ph in TIC_PHRASES:
        n = low.count(ph)
        if n:
            print(f"  '{ph}': {n}")

    if a.source:
        src = join_asr(norm(open(a.source, encoding="utf-8").read()))
        s8 = set(ngrams(tokens(src), 8))
        d8 = ngrams(tk, 8)
        r = sum(1 for g in d8 if g in s8) / max(1, len(d8)) * 100
        print(f"\n=== TRUNG VOI VAN BAN DOI CHIEU === {r:.1f}% cum 8 tu (muc tieu < 3%) -> {'DAT' if r < 3 else 'VIET LAI DOAN BAM SAT'}")

    if a.keywords:
        print("\n=== TU KHOA === (tu khoa chinh nen xuat hien trong ~3.000 ky tu dau)")
        for kw in [k.strip().lower() for k in a.keywords.split(",") if k.strip()]:
            i = low.find(kw)
            where = f"lan dau o ky tu {i:,} ({i / max(1, chars) * 100:.0f}%)" if i >= 0 else "KHONG CO"
            print(f"  {kw}: {low.count(kw)} lan, {where}")

    if a.seo:
        check_seo(a.seo)


if __name__ == "__main__":
    main()
