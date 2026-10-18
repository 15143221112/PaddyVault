# -*- coding: utf-8 -*-
import glob, os, re, shutil, sys

D = r"D:\zhihong\水稻国家标准\国家标准"
BACKUP = r"D:\zhihong\水稻国家标准\国家标准_原始备份"

def eq_clean(s):
    """把 <eq> 内的 MinerU LaTeX 转成可读 Unicode 文本"""
    s = s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    s = s.replace("\\leqslant", "≤").replace("\\geqslant", "≥")
    s = s.replace("\\Delta", "Δ").replace("\\sum", "Σ").replace("\\circ", "°")
    s = s.replace("\\overline{", "")   # 去上划线，保留内容
    s = s.replace("\\mathrm", "")
    s = s.replace("\\,", "").replace("\\ ", "").replace("\\~", "").replace("\\ ", "")
    s = re.sub(r"_\{(.+?)\}", r"\1", s)   # 下标 {x}
    s = re.sub(r"_(\w)", r"\1", s)        # 下标 x
    s = re.sub(r"\^\{?([^\\{}]*)\}?", r"\1", s)  # 上标
    s = re.sub(r"[\\{}]", "", s)          # 残留 LaTeX 花括号/反斜杠
    s = re.sub(r"\s+", " ", s).strip()
    return s

def clean(txt):
    # 1) 错字
    txt = txt.replace("垨白", "垩白")
    # 2) 失效 CDN 外链图片整行删除
    txt = re.sub(r"!\[image\]\(https?://[^)\s]*\)[ \t]*\n?", "", txt)
    # 3) 编号乱码 � 修复（数字�数字 -> 数字.数字）
    txt = re.sub(r"(\d)\ufffd(\d)", r"\1.\2", txt)
    # 4) 公式编号标签乱码：……(A.1} / \tag{……(A.1}
    txt = re.sub(r"…+\(([A-Za-z]?\.?\d+)\}?\)?", r"(\1)", txt)
    txt = txt.replace("……", "")
    txt = re.sub(r"\\tag\{", "(", txt)
    txt = re.sub(r"\\tag", "", txt)
    # 5) <eq> LaTeX 转 Unicode
    txt = re.sub(r"<eq>(.*?)</eq>", lambda m: eq_clean(m.group(1)), txt, flags=re.S)
    return txt

def main():
    files = sorted(glob.glob(os.path.join(D, "*.md")))
    if not files:
        print("无 md 文件"); return
    # 备份
    os.makedirs(BACKUP, exist_ok=True)
    for f in files:
        dst = os.path.join(BACKUP, os.path.basename(f))
        if not os.path.exists(dst):
            shutil.copy2(f, dst)
    print(f"已备份 {len(files)} 个原文件到 {BACKUP}")
    # 清洗
    report = []
    for f in files:
        orig = open(f, encoding="utf-8").read()
        new = clean(orig)
        n_eq = orig.count("<eq>")
        n_ui = orig.count("\ufffd")
        with open(f, "w", encoding="utf-8", newline="") as fh:
            fh.write(new)
        report.append((os.path.basename(f), n_eq, n_ui, orig != new))
    print("\n清洗结果（eq标记数, �数, 是否有改动）:")
    for name, eq, ui, chg in report:
        print(f"  {name}: eq={eq} �={ui} 改动={'是' if chg else '否'}")

if __name__ == "__main__":
    main()
