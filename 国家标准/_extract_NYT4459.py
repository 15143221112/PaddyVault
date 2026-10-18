# -*- coding: utf-8 -*-
"""NYT4459-2025 水稻品种MNP标记鉴定.pdf —— 提取表格+图片并验证保存正确性"""
import csv, sys
from pathlib import Path
import fitz
from PIL import Image

PDF = Path(r"D:\zhihong\水稻国家标准\NYT4459-2025-水稻品种MNP标记鉴定.pdf")
OUT = Path(r"D:\zhihong\水稻国家标准\NYT4459_提取")
TABLES = OUT / "tables"
IMAGES = OUT / "images"
TABLES.mkdir(parents=True, exist_ok=True)
IMAGES.mkdir(parents=True, exist_ok=True)

def main():
    doc = fitz.open(str(PDF))
    print(f"总页数: {doc.page_count}")
    table_count = 0
    image_count = 0
    seen_xref = set()

    for pno in range(doc.page_count):
        page = doc[pno]
        # ---- 表格：PyMuPDF find_tables ----
        finder = page.find_tables()
        for ti, tab in enumerate(finder.tables):
            data = tab.extract()
            if not data:
                continue
            table_count += 1
            csv_path = TABLES / f"p{pno+1:03d}_t{ti+1:02d}.csv"
            with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
                csv.writer(f).writerows(data)
        # ---- 图片：get_images + extract_image，按 xref 去重 ----
        for img in page.get_images(full=True):
            xref = img[0]
            if xref in seen_xref:
                continue
            seen_xref.add(xref)
            info = doc.extract_image(xref)
            ext = info["ext"]  # png / jpeg ...
            img_path = IMAGES / f"p{pno+1:03d}_xref{xref}.{ext}"
            img_path.write_bytes(info["image"])
            image_count += 1

    doc.close()
    print(f"提取结果 → 表格 {table_count} 个 / 图片 {image_count} 张")

    # ---- 验证 ----
    # 1) 图片能否被正确解码
    img_files = list(IMAGES.iterdir())
    ok = 0; bad = []
    for im in img_files:
        try:
            Image.open(im).verify()
            ok += 1
        except Exception as e:
            bad.append((im.name, str(e)))
    print(f"[验证-图片] 文件 {len(img_files)} 个，可正常打开 {ok} 个，损坏 {len(bad)} 个")
    for name, err in bad:
        print(f"   损坏: {name} -> {err}")

    # 2) 表格 CSV 是否非空、列数是否一致
    tab_files = list(TABLES.glob("*.csv"))
    empty = []; ragged = []
    for t in tab_files:
        with open(t, encoding="utf-8-sig") as f:
            rows = [r for r in csv.reader(f)]
        if len(rows) < 2:
            empty.append(t.name); continue
        widths = {len(r) for r in rows}
        if len(widths) > 1:
            ragged.append((t.name, sorted(widths)))
    print(f"[验证-表格] 文件 {len(tab_files)} 个，空表 {len(empty)} 个，列宽不齐 {len(ragged)} 个")
    for e in empty:
        print(f"   空表: {e}")
    for name, w in ragged:
        print(f"   列宽不一: {name} 列宽={w}")

    # 3) 图片的原始像素尺寸抽查
    sizes = {}
    for im in img_files[:200]:
        with Image.open(im) as p:
            sizes[im.name] = p.size
    print("[抽查-前若干图片尺寸]", list(sizes.items())[:5])

    print(f"\n输出目录: {OUT}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("脚本出错:", e, file=sys.stderr)
        raise
