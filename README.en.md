# 🌾 PaddyVault

> Cold-region rice farming knowledge vault — national standards + decision cards + distilled book lists + 1000+ Q&A, all in one searchable repository.
> Built for Northeast China cold-region rice cultivation, covering the full chain: variety selection → planting → pest control → harvest → storage.

[中文](README.md) · [Changelog](CHANGELOG.md)

---

## ✨ Highlights

- **National standards collection**: curated current national / industry / local standards (PDF) for rice — cold damage grades, quality grading, seed quarantine, production technical regulations.
- **Ready-to-use decision cards**: variety × temperature-belt × saline-alkali × official-recommended selection logic distilled into executable rules — input your accumulated temperature, get matched varieties.
- **Distilled book lists**: Top-10 classic rice books distilled + where to obtain them.
- **1000+ practical Q&A**: 1300+ cold-region rice Q&As (jsonl) covering seedling raising, fertilizing, pest control, water-saving irrigation — directly consumable by a RAG knowledge base.
- **Retrieval-friendly**: Q&A and decision cards carry structured tags / trigger words / data sources for precise RAG recall.

---

## 📦 Content

| Directory | Content |
|---|---|
| **国家标准/** | National / industry / local standards PDF + KB config |
| **问答库/** | 1300+ cold-region rice Q&A (jsonl) |
| **书籍蒸馏书单/** | Distilled Top-10 book list + sources |
| **决策卡格式模板.md** | Decision card writing template |
| **品种-积温带选型决策卡.md** | Core variety selection decision card |

---

## 🚀 Quick Start

```bash
git clone https://github.com/15143221112/PaddyVault.git
cd PaddyVault
# Browse 国家标准/ for standards, read 问答库/qa_1_1300.jsonl for Q&A corpus
```

**RAG ingestion**: `qa_1_1300.jsonl` and decision cards are structured — import directly as knowledge base corpus.

---

## 📄 License

[MIT](LICENSE) © 2026 PaddyVault contributors. Standards PDFs belong to their original publishers; Q&A and decision cards are original compilations.
