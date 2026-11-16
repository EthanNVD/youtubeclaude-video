import re, sys
src = open(sys.argv[1], encoding="utf-8").read()
out = []
for p in [p.strip() for p in re.split(r"\n\s*\n", src) if p.strip()]:
    m = re.match(r"^([^\W\d][\w .'’-]{0,40}?)(?:\s*\[(QUOTE|REPORTED|DRAMATIZED)\])?\s*:\s*(.*)$", p, re.S)
    assert m and m.group(1) == m.group(1).upper(), p[:60]
    out.append(m.group(3).strip())
open(sys.argv[2], "w", encoding="utf-8", newline="\n").write("\n\n".join(out) + "\n")
