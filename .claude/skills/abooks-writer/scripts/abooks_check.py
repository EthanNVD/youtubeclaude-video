#!/usr/bin/env python3
"""Kiem tra kich ban Abooks (nguyen ban skill abooks-script-rewriter, them muc nhap vai va moc chuong)."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import re, argparse, unicodedata, collections

BANNED = [
    "nguồn nói", "theo nguồn", "trong nguồn", "mạch nguồn", "chất liệu nguồn",
    "văn bản nguồn", "lời kết nguồn", "kịch bản gốc", "bản gốc",
    "bạn đang nghe abooks", "trước khi vào bản review", "hãy mua sách ủng hộ",
    "khuyến khích khán thính giả", "bấm like", "đăng ký kênh", "nhấn chuông",
    "trong video này", "hôm nay chúng ta sẽ", "ở phần tiếp theo",
]

IMPERSONATION = [
    r"\bngười ta hỏi tôi\b", r"\bmột người hỏi tôi\b", r"\bhọ hỏi tôi\b", r"\btôi nói với họ\b",
    r"\btôi đã gặp (hàng|vô số|rất nhiều)", r"\bđừng gọi tôi là thầy\b", r"\bthưa ông\b",
    r"\btôi không có gì để (dạy|bán)\b", r"\bkhi tôi còn (nhỏ|là cậu bé)",
]

SYMBOLS = re.compile(r"[%&@=<>#*_~^|\\/\[\]{}]|\.{3}|…|!!|\?\?|https?://|\b\d{1,2}/\d{1,2}\b")
DIGIT = re.compile(r"\d+")


def norm(t):
    return unicodedata.normalize("NFC", t)


def join_asr(t):
    t = re.sub(r"\[âm nhạc\]|\[Âm nhạc\]|>>", "", t)
    return re.sub(r"\s*\n\s*", " ", t).strip()


def sentences(t):
    flat = re.sub(r"\s+", " ", t)
    return [s.strip() for s in re.split(r"(?<=[.?!])\s+", flat) if s.strip()]


def ngrams(words, n):
    return [" ".join(words[i:i + n]) for i in range(len(words) - n + 1)]


def tokens(t):
    return re.findall(r"\w+", t.lower())


def check_seo(path):
    t = norm(open(path, encoding="utf-8").read())
    print("\n=== GOI SEO ===")
    titles = [x.strip() for x in re.findall(r"^TIÊU ĐỀ \d+:\s*(.+)$", t, re.M)]
    for x in titles:
        n = len(x)
        flag = "DAT" if 45 <= n <= 70 else ("CHAP NHAN" if n <= 100 else "QUA 100")
        print(f"  [{n} ky tu, {flag}] {x}")
    if len(titles) != 3:
        print("  CAN DUNG 3 TIEU DE, dang co", len(titles))
    m = re.search(r"^MÔ TẢ:\s*\n(.*?)(?=^HASHTAG:|^TAG:|\Z)", t, re.M | re.S)
    if m:
        d = m.group(1).strip()
        b = len(d.encode("utf-8"))
        flag = "VUOT GIOI HAN 5000 BYTE" if b > 5000 else ("DAI HON MUC GON 1500" if len(d) > 1500 else "DAT")
        print(f"  Mo ta: {len(d)} ky tu, {b} byte -> {flag}")
        print(f"  ~150 ky tu dau (hien truoc 'Xem them'): {d[:150]}")
        tags_in_desc = re.findall(r"#\w+", d)
        print(f"  Hashtag trong mo ta: {tags_in_desc}")
    else:
        print("  KHONG THAY MO TA")
    h = re.search(r"^HASHTAG:\s*(.+)$", t, re.M)
    if h:
        hs = re.findall(r"#\w+", h.group(1))
        print(f"  HASHTAG: {len(hs)} -> {'DAT' if 3 <= len(hs) <= 5 else 'NEN 3-5'}")
    g = re.search(r"^TAG:\s*(.+)$", t, re.M)
    if g:
        tags = [x.strip() for x in g.group(1).split(",") if x.strip()]
        total = len(",".join(tags)) + 2 * sum(1 for x in tags if " " in x)
        print(f"  TAG: {len(tags)} tag, ~{total} ky tu tinh theo YouTube -> {'DAT' if len(tags) == 10 and total <= 500 else 'CAN 10 TAG, <=500 KY TU'}")
        low_tags = [x.lower() for x in tags]
        dup = sorted({x for x in low_tags if low_tags.count(x) > 1})
        if dup:
            print("  Tag trung:", dup)


HEDGES = ["cho rằng", "theo cách nhìn của ông", "theo cách nhìn của bà", "ông nói đại ý", "theo ông,", "ông nói rằng", "ông chỉ ra rằng"]
CHATTY = ["tôi muốn mời bạn", "thưa bạn", "hãy cùng tôi", "bạn của tôi", "bạn thân mến"]
SLOW_OPEN = ["kéo ghế", "ngồi xuống đây", "ấm trà", "tách trà", "hôm nay chúng ta", "xin chào"]
STOP = set("của và là có không những một các được cho với trong này đó thì mà như ta bạn tôi khi đã sẽ đang rằng nó người".split())


def voice_check(text, low, paras, sents, wl, chars, author):
    """Giong Abooks da duyet 21/11/2026: mo bai bang cau cach ngon, than bai khang dinh, ket goi lai cau mo."""
    print("\n=== GIONG ABOOKS (chuan da duyet) ===")
    if not paras:
        return
    first = paras[0].strip()
    fs = sentences(first)
    fw = len(first.split())
    ok1 = len(fs) <= 2 and fw <= 35
    print(f"Doan mo dau: {len(fs)} cau, {fw} tu -> {'DAT (cau cach ngon dung rieng)' if ok1 else 'XEM LAI: doan dau phai la 1-2 cau ngan, nghich ly, dung rieng'}")
    head = low[:1500]
    slow = [w for w in SLOW_OPEN if w in head]
    print(f"Dau hieu mo cham trong 1.500 ky tu dau: {slow if slow else 'khong'}")
    if author:
        i = low.find(author.lower())
        print(f"Ten tac gia '{author}' lan dau o ky tu {i:,} -> {'DAT' if 0 <= i <= 1200 else 'XEM LAI (nen trong 1.200 ky tu dau)'}")
    per10k = 10000 / max(1, chars)
    hed = sum(low.count(h) for h in HEDGES)
    print(f"Cum rao don ('cho rang', 'theo cach nhin cua ong'...): {hed} (~{hed * per10k:.1f}/10.000 ky tu; muc tieu <= 4)")
    chat = {c: low.count(c) for c in CHATTY if low.count(c)}
    tot = sum(chat.values())
    print(f"Dong tac tro chuyen: {tot} {chat if chat else ''} (muc tieu <= 6 ca bai)")
    if author:
        starts = [p.strip().lower().startswith((author.lower(), "ông ", "bà ")) for p in paras]
        run = best = 0
        for s in starts:
            run = run + 1 if s else 0
            best = max(best, run)
        print(f"Doan mo bang ten tac gia/'ong': {sum(starts)} ({sum(starts) / len(paras) * 100:.0f}% so doan), chuoi lien tiep dai nhat {best} (muc tieu <= 15%, chuoi <= 2)")
    short = sum(1 for w in wl if w <= 5)
    print(f"Cau <= 5 tu: {short / max(1, len(sents)) * 100:.1f}% (muc tieu 8-15%) | cau TB {sum(wl) / max(1, len(wl)):.1f} tu (muc tieu 13-17)")
    tok = lambda s: {w for w in re.findall(r"\w+", s.lower()) if len(w) > 2 and w not in STOP}
    echo = tok(first) & tok(" ".join(paras[-2:]))
    print(f"Ket goi lai cau mo: tu chung {sorted(echo)[:8]} -> {'DAT' if len(echo) >= 3 else 'XEM LAI (cau cuoi nen goi lai cau cach ngon mo dau)'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--source")
    ap.add_argument("--min", type=int, default=50000)
    ap.add_argument("--max", type=int, default=60000)
    ap.add_argument("--asr", action="store_true")
    ap.add_argument("--keywords", help="tu khoa, phan cach bang dau phay")
    ap.add_argument("--seo", help="file goi SEO can kiem tra")
    ap.add_argument("--cpm", type=float, default=0, help="ky tu moi phut; in moc chuong uoc tinh")
    ap.add_argument("--author", default="Krishnamurti", help="ten tac gia de kiem vi tri ten va doan mo bang ten")
    a = ap.parse_args()

    raw = norm(open(a.draft, encoding="utf-8").read())
    text = join_asr(raw) if a.asr else raw
    chars = len(text)
    words = len(text.split())
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    sents = sentences(text)
    wl = [len(s.split()) for s in sents]
    longs = [(n, s) for n, s in zip(wl, sents) if n > 30]
    q = sum(1 for s in sents if s.endswith("?"))
    low = text.lower()

    print("=== DO DAI ===")
    status = "DAT" if a.min <= chars <= a.max else ("THIEU %d" % (a.min - chars) if chars < a.min else "THUA %d" % (chars - a.max))
    print(f"Ky tu (gom khoang trang, xuong dong): {chars:,} | dai {a.min:,}-{a.max:,} -> {status}")
    print(f"So tu: {words:,} | doan: {len(paras)} | cau: {len(sents)} | uoc luong doc ~{words/155:.0f} phut")

    print("\n=== NHIP CAU ===")
    if sents:
        print(f"TB {sum(wl)/len(wl):.1f} tu/cau | >30 tu: {len(longs)} ({len(longs)/len(sents)*100:.1f}%) | <=5 tu: {sum(1 for w in wl if w<=5)} | cau hoi: {q} ({q/len(sents)*100:.1f}%)")
    if paras:
        pl = [len(p) for p in paras]
        print(f"Doan: TB {sum(pl)/len(pl):.0f} ky tu, dai nhat {max(pl)}, ngan nhat {min(pl)}")
    for n, s in sorted(longs, reverse=True)[:15]:
        print(f"  [{n} tu] {s[:160]}")
    over45 = [s for n, s in longs if n > 45]
    if over45:
        print(f"CAU >45 TU PHAI TACH: {len(over45)}")

    print("\n=== LOI CAM / TTS ===")
    hits = [(b, low.count(b)) for b in BANNED if b in low]
    print("Cum cam:", hits if hits else "khong")
    sym = collections.Counter(m.group(0) for m in SYMBOLS.finditer(text))
    print("Ky hieu kho doc:", dict(sym) if sym else "khong")
    dg = collections.Counter(m.group(0) for m in DIGIT.finditer(text))
    print("Chu so (kiem tra cach doc):", dict(dg.most_common(20)) if dg else "khong")
    print("Markdown/heading:", "CO" if re.search(r"^\s*(#|-|\*|\d+\.)\s", text, re.M) else "khong")
    names = collections.Counter()
    for s in sents:
        ws = re.findall(r"\w+", s)
        i = 1
        while i < len(ws):
            if ws[i][0].isupper():
                j = i
                while j + 1 < len(ws) and ws[j + 1][0].isupper():
                    j += 1
                names[" ".join(ws[i:j + 1])] += 1
                i = j + 1
            else:
                i += 1
    print("Ten rieng giua cau (kiem tra viet thong nhat):", dict(names.most_common(40)) if names else "khong")

    print("\n=== LAP Y TRONG BAI ===")
    tk = tokens(text)
    c8 = collections.Counter(ngrams(tk, 8))
    rep = [(g, n) for g, n in c8.items() if n > 1]
    print(f"Cum 8 tu lap lai: {len(rep)}")
    for g, n in sorted(rep, key=lambda x: -x[1])[:15]:
        print(f"  x{n}: {g}")
    openers = collections.Counter(" ".join(p.split()[:2]).lower() for p in paras)
    print("Mo doan hay dung:", [(k, v) for k, v in openers.most_common(8) if v > 2])
    for phrase in ["hãy tưởng tượng", "điều này không có nghĩa", "bạn có thấy", "nói cách khác", "thực chất", "chính là"]:
        n = low.count(phrase)
        if n:
            print(f"  '{phrase}': {n}")

    print("\n=== NHAP VAI TAC GIA (phai = 0) ===")
    imp = []
    for pat in IMPERSONATION:
        for mm in re.finditer(pat, low):
            imp.append(text[max(0, mm.start() - 50): mm.end() + 50].replace("\n", " "))
    print(f"So dau hieu: {len(imp)}")
    for x in imp[:10]:
        print(f"  ...{x}...")

    if not a.asr:  # phu de ghep dong khong co doan, muc giong chi dung cho ban nhap
        voice_check(text, low, paras, sents, wl, chars, a.author)

    if a.cpm:
        print(f"\n=== MOC CHUONG UOC TINH (@{a.cpm:.0f} ky tu/phut) ===")
        pos = 0
        print("  00:00 - [mo bai]")
        for part in re.split(r"(\n\s*\n)", text):
            ps = part.strip()
            if ps and "\n" not in ps and len(sentences(ps)) == 1 and 2 <= len(ps.split()) <= 14 and not ps.endswith("?"):
                sec = int(round(pos / a.cpm * 60))
                print(f"  {sec // 60:02d}:{sec % 60:02d} - {ps.rstrip('.')}")
            pos += len(part)

    if a.source:
        src = join_asr(norm(open(a.source, encoding="utf-8").read()))
        s8 = set(ngrams(tokens(src), 8))
        d8 = ngrams(tk, 8)
        shared = sum(1 for g in d8 if g in s8)
        ratio = shared / max(1, len(d8)) * 100
        print("\n=== TRUNG LAP VOI BAN NGUON ===")
        print(f"Ty le cum 8 tu trung: {ratio:.1f}% (muc tieu < 5%) -> {'DAT' if ratio < 5 else 'VIET LAI CHO TRUNG'}")

    if a.keywords:
        print("\n=== TU KHOA ===")
        for kw in [k.strip().lower() for k in a.keywords.split(",") if k.strip()]:
            n = low.count(kw)
            i = low.find(kw)
            pos = f"lan dau o ky tu {i:,} ({i / max(1, chars) * 100:.0f}% bai)" if i >= 0 else "KHONG CO"
            print(f"  {kw}: {n} lan, {pos}")

    if a.seo:
        check_seo(a.seo)


if __name__ == "__main__":
    main()
