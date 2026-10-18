# -*- coding: utf-8 -*-
"""验证 md 蒸馏产物的表格完整性"""
import re
from pathlib import Path

def re_full_sep(r):
    """判断是否为分隔行（---）"""
    body = r.strip().strip("|")
    if not body:
        return False
    return all(not x.strip() or set(x.strip()) <= set("-: ") for x in body.split("|"))

def cells(line):
    body = line.strip().strip("|")
    return len(body.split("|")) if body else 0

md = Path(r"D:\zhihong\水稻国家标准\NYT4459_提取\dist_v2\NYT4459-2025-MNP标记鉴定_蒸馏.md")
lines = md.read_text(encoding="utf-8").splitlines()

tables = []
cur = None
for ln in lines:
    s = ln.strip()
    if s.startswith("**表 ") or s.startswith("### 表格 "):
        if cur is not None:
            tables.append(cur)
        cur = {"title": s, "rows": []}
    elif cur is not None and s.startswith("|"):
        cur["rows"].append(s)
if cur is not None:
    tables.append(cur)

print(f"检测到 Markdown 表格块: {len(tables)} 个")

bad = []
for t in tables:
    ncol = None
    for i, r in enumerate(t["rows"]):
        if i == 1 and re_full_sep(r):
            continue
        c = cells(r)
        if ncol is None:
            ncol = c
        elif c != ncol:
            bad.append((t["title"], i, ncol, c))
            break
print(f"列结构不一致的表格: {len(bad)} 个")
for b in bad[:10]:
    print("   ", b)

print("\n=== 抽查前3个表格（行数 x 列数）===")
for t in tables[:3]:
    nrow = len(t["rows"]) - 1
    ncol = cells(t["rows"][0])
    print(f"{t['title']}: {nrow} 数据行 x {ncol} 列")
    print(f"   表头: {t['rows'][0]}")
    print(f"   首数据行: {t['rows'][2] if len(t['rows'])>2 else ''}")

imgs = [l for l in lines if l.strip().startswith("![")]
print(f"\n图片引用: {len(imgs)} 个")
