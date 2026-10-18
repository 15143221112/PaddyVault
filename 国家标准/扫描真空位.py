# -*- coding: utf-8 -*-
import glob, os, re
D = r"D:\zhihong\水稻国家标准\精炼分文件"
files = sorted(glob.glob(os.path.join(D, "*.md")))
total=0
for f in files:
    txt = open(f, encoding="utf-8").read()
    # 真空位：连续2+下划线，后不跟空格+花括号（排除公式下标 _ {x}）
    hits = list(re.finditer(r"_{2,}(?!\s*\{)", txt))
    print(f"=== {os.path.basename(f)}: 真空位x{len(hits)}")
    total+=len(hits)
    for m in hits[:15]:
        ctx = txt[max(0,m.start()-25):m.start()+25].replace("\n"," ")
        print(f"    >> {ctx}")
print(f"\n真空位合计: {total}")
