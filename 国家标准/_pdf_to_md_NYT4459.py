# -*- coding: utf-8 -*-
"""NYT4459-2025 → 干净 Markdown 蒸馏 v2：去页眉页脚/目录点线/合并段落/识别章节标题，表格完整保留"""
import re, sys
from pathlib import Path
import fitz

PDF = Path(r"D:\zhihong\水稻国家标准\NYT4459-2025-水稻品种MNP标记鉴定.pdf")
OUT = Path(r"D:\zhihong\水稻国家标准\NYT4459_提取\dist_v2")
IMGS = OUT / "images"
OUT.mkdir(parents=True, exist_ok=True)
IMGS.mkdir(exist_ok=True)

HEADER_RE = re.compile(r"^[NYＮＹ][/／][TＴ]")          # 页眉：NY/T...
_HEADER_STRS = ("NY/T４４５９—２０２５", "ＮＹ／Ｔ４４５９—２０２５", "NY/T 4459—2025")
def strip_header(t):
    t2 = t.lstrip()
    for h in _HEADER_STRS:
        if t2.startswith(h):
            return t2[len(h):].strip()
    return t
DOTS = "􀆺·.∙◦"
def is_dotline(t):
    """目录/页码引导点线行"""
    if not t or len(t) < 3:
        return False
    n = sum(1 for c in t if c in DOTS)
    return n >= max(2, len(t) * 0.4)

def is_pageno(t):
    """纯页码/罗马数字"""
    t = t.strip()
    if not t:
        return False
    return bool(re.fullmatch(r"[\d\s]+|[ⅠⅡⅢⅣⅤⅥ]+|I{1,4}|[a-zA-Z]?", t))

def is_heading(t):
    """章节/条款标题（数字开头 或 附录）"""
    t = t.strip()
    if re.match(r"^[０-９0-9]{1,2}\s*\S", t) or re.match(r"^附录[AB]", t):
        return True
    return False

def cell_to_md(c):
    if c is None:
        return ""
    c = str(c).replace("|", "\\|")
    c = re.sub(r"\s*\n\s*", "<br>", c)
    return c.strip()

def table_to_md(data):
    if not data:
        return ""
    rows = [[cell_to_md(c) for c in r] for r in data]
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    lines = ["| " + " | ".join(rows[0]) + " |"]
    lines.append("| " + " | ".join(["---"] * ncol) + " |")
    for r in rows[1:]:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)

def in_rect(rect, bbox):
    x0, y0, x1, y1 = rect
    bx0, by0, bx1, by1 = bbox
    return not (x1 < bx0 or x0 > bx1 or y1 < by0 or y0 > by1)

def main():
    doc = fitz.open(str(PDF))
    md = ["# NY/T 4459—2025 水稻品种及其实质性派生品种鉴定 MNP标记法", ""]
    md.append("> PDF 蒸馏 Markdown（表格原样保留，正文已去页眉页脚/目录噪音，章节标题结构化）\n")

    table_cnt = 0
    seen_xref = set()

    for pno in range(doc.page_count):
        page = doc[pno]
        H = page.rect.height
        tables = page.find_tables()
        tab_bboxes = [t.bbox for t in tables.tables]

        md.append(f"\n## 第 {pno+1} 页\n")

        # --- 正文文本块：过滤噪音 + 段落化 ---
        blocks = page.get_text("blocks", sort=True)
        paras = []
        for blk in blocks:
            x0, y0, x1, y1, text, bno, btype = blk
            if btype != 0:
                continue
            if any(in_rect((x0, y0, x1, y1), b) for b in tab_bboxes):
                continue
            t = text.strip().replace("\n", " ").strip()
            if not t:
                continue
            # 剥离行首页眉（NY/T 4459—2025）
            t = strip_header(t)
            if not t:
                continue
            # 页眉/页脚/页码/点线过滤
            if HEADER_RE.match(t) and len(t) < 30:
                continue
            if y1 > H - 45 and is_pageno(t):
                continue
            if is_pageno(t) and len(t) <= 3:
                continue
            if is_dotline(t):
                continue
            # 封面/目录的孤立单字（如“Ⅰ”“发布”“实施”）——保留长度≥2且有意义的
            if len(t) <= 1:
                continue
            paras.append(t)

        # 合并成段落：同一自然段（相邻、且前段非标题）拼成一段，标题独立
        cleaned = []
        i = 0
        while i < len(paras):
            t = paras[i]
            if is_heading(t):
                cleaned.append(("H", t))
            else:
                # 向后吸收紧邻的短句（属于同一段落）
                buf = t
                j = i + 1
                while j < len(paras) and not is_heading(paras[j]) and len(buf) + len(paras[j]) < 120 and len(paras[j]) < 40:
                    buf = buf + paras[j]
                    j += 1
                cleaned.append(("P", buf))
                i = j - 1
            i += 1

        for kind, t in cleaned:
            if kind == "H":
                md.append(f"### {t}")
            else:
                md.append(t)
            md.append("")

        # --- 表格 ---
        for tab in tables.tables:
            data = tab.extract()
            if not data:
                continue
            table_cnt += 1
            md.append(f"**表 {table_cnt}（第 {pno+1} 页）**\n")
            md.append(table_to_md(data))
            md.append("")

        # --- 图片 ---
        for img in page.get_images(full=True):
            xref = img[0]
            if xref in seen_xref:
                continue
            seen_xref.add(xref)
            info = doc.extract_image(xref)
            fn = IMGS / f"p{pno+1:03d}_xref{xref}.{info['ext']}"
            fn.write_bytes(info["image"])
            md.append(f"![图-第{pno+1}页](images/{fn.name})\n")

    doc.close()
    out_md = OUT / "NYT4459-2025-MNP标记鉴定_蒸馏.md"
    out_md.write_text("\n".join(md), encoding="utf-8")
    print(f"完成：表格 {table_cnt} 个 → {out_md}  ({round(out_md.stat().st_size/1024,1)} KB)")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("脚本出错:", e, file=sys.stderr)
        raise
