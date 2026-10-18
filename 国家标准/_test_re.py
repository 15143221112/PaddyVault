# -*- coding: utf-8 -*-
import re

s = 'NY/T４４５９—２０２５前　　言'
print("s len:", len(s))
print("s[0:5] codes:", [hex(ord(c)) for c in s[:5]])

for label, pat in [
    ("^NY", r"^NY"),
    ("^NY/T", r"^NY/T"),
    ("[NY]", r"[NY]"),
    ("^[NYＮＹ]", r"^[NYＮＹ]"),
    ("full literal", r"^[NYＮＹ][/／][TＴ]\s*４?４５９\s*[—\-–]\s*２０２５\s*"),
]:
    print(f"{label}: pat=repr({pat!r}) ->", "MATCH" if re.match(pat, s) else "NO MATCH")

# 检查脚本源文件编码
with open(r"D:\zhihong\水稻国家标准\_test_re.py", "rb") as f:
    head = f.read(4)
    print("file BOM:", head.hex())
