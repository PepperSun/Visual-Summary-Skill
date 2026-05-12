# Visual Summary

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Styles](https://img.shields.io/badge/Styles-3-blueviolet)](#styles)
[![Languages](https://img.shields.io/badge/Languages-EN%20%7C%20ZH--Hans%20%7C%20ZH--Hant-orange)](#language-detection)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-green)](https://code.claude.com)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-standard-lightgrey)](https://agentskills.io)

**A dissection, not a summary — the first section is always the TL;DR, and the rest rebuilds the full argument so you can internalize the essay rather than just extract its conclusion.**

Visual Summary is an agent skill for Claude, Cursor, Codex, Gemini CLI, and other model hosts that dissects long documents (essays, reports, speeches, papers) into a **styled, visual HTML page** — not plain text or markdown. Argument structure, logic chains, comparison tables, and key data are rendered as designed components you can read at a glance. Each output opens with the core judgment, then traces the logic chain, evidence, and limits — everything a close reader would need to hold the argument in their head.

---

## Output Gallery

Three real outputs, all three styles, two languages.

| Case | Style | Language | Source type |
|------|-------|----------|-------------|
| [Great Myths of the Great Depression](https://peppersun.github.io/Visual-Summary-Skill/examples/great-depression-trial.html) | **Clear** | English | Policy essay |
| [Response to Jeffrey Sachs](https://peppersun.github.io/Visual-Summary-Skill/examples/response-to-jeffrey-sachs-visual-summary.html) | **Mature** | English | Academic rebuttal |
| [官方的人口预估可能偏乐观 · 荣鼎](https://peppersun.github.io/Visual-Summary-Skill/examples/荣鼎人口分析.html) | **Vibrant** | 简体中文 | Macroeconomic report |

> Live previews hosted via GitHub Pages. Clone the repo to open locally — no server needed.

---

## Why use this

- **Dissection, not extraction.** The output preserves the full argument — logic chain, supporting evidence, boundary conditions, and residual judgments — so you can internalize the essay, not just cite its conclusion.
- **Section 1 is always the TL;DR.** The core judgment comes first, in 2–3 sentences. Everything after supports, qualifies, or challenges it.
- **Strict one-sentence discipline.** Every bullet, table cell, and chain node after section 1 stays to one sentence. The output is scannable, not encyclopedic.
- **Three editorial styles.** Mature for long-form essays and analysis, Clear for reports and explainers, Vibrant for speeches and decisive arguments.
- **Bilingual by default.** Follows the document language automatically; English, Simplified Chinese, and Traditional Chinese are all supported.
- **Single-file output.** Each result is a fully self-contained HTML page with embedded CSS — no external dependencies, shareable immediately.

---

## Install

**Claude Code**
```bash
/skill install PepperSun/visual-summary
```

**Cursor**

Add the skill to your Cursor rules directory, or install via the Cursor plugin marketplace by pointing it to `PepperSun/visual-summary`. Cursor will pick up `SKILL.md` automatically.

**OpenAI Codex**

The `agents/openai.yaml` file is included for Codex compatibility. Clone the repo and register the skill folder in your Codex agent configuration.

```bash
git clone https://github.com/PepperSun/Visual-Summary-Skill
```

**Gemini CLI**
```bash
git clone https://github.com/PepperSun/Visual-Summary-Skill
# Point your Gemini CLI skill path to the cloned folder
```

**Any Agent Skills-compatible host**

Download [`visual-summary.skill`](visual-summary.skill) and load it through your host's skill or plugin manager — the `.skill` format follows the [Agent Skills open standard](https://agentskills.io) supported by Claude, Cursor, Codex, Gemini CLI, Windsurf, and others.

**From source (all platforms)**
```bash
git clone https://github.com/PepperSun/Visual-Summary-Skill
```
Then point your agent host at the cloned folder. The entry point is `SKILL.md`.

---

## Quick start

Once installed, just describe your document and the skill triggers automatically:

```
Summarize this PDF into a visual page.
```
```
Turn this essay into a visual summary in Vibrant style.
```
```
把这篇报告做成可视化摘要，用简体中文输出。
```
```
Summarize this speech. Use the Mature style.
```

The skill handles classification, compression, and HTML rendering without additional instructions.

---

## How it works

```
Document in  →  Extract text  →  Classify  →  Structure  →  Render HTML
```

1. **Ingest** — reads PDF, DOCX, TXT, MD, or pasted text
2. **Normalize** — strips headers, footers, page numbers, hard-wrap noise
3. **Classify** — detects form, intent, and structure (see framework below)
4. **Summarize** — applies strict compression: core claim → logic chain → 1 evidence point per step
5. **Render** — outputs a single self-contained HTML page in the detected or requested style

### Classification framework

| Axis | Options |
|------|---------|
| Form | Narrative · Argumentation · Lyric · Record |
| Intent | Inform · Explain · Persuade · Resonate · Entertain · Preserve |
| Structure | Chronology · Logic · Taxonomy · Comparison · Nested · Free |
| Persuasion subtype | Stance · Rebuttal · Synthesis |

The classification determines which visual skeleton is used: logic chains for causal arguments, comparison tables for parallel structures, timelines for chronology, big-numeral panels for quantitative pieces.

---

## Styles

### Mature *(default)*
Ivory paper background, Source Serif display type, lilac highlights. Suited for long-form essays, analytical reports, and philosophical writing.

### Clear
Near-white background, pastel accent families, pill geometry, Inter type. Best for reports, explainers, and neutral summaries.

### Vibrant
White background, saturated primaries (blue / yellow / red), 2px ink outlines, bold pill geometry, Inter Black. Best for speeches, manifestos, and decisive arguments.

Request a style explicitly:
```
Summarize this report. Use the Clear style.
```
Or let the skill choose — it defaults to Mature.

---

## Language detection

The skill follows the document language by default. To override:
```
Summarize in English.
用简体中文输出。
用繁體中文輸出。
```

---

## Supported input formats

| Format | Notes |
|--------|-------|
| PDF | Text-bearing PDFs; scanned/image PDFs use OCR fallback |
| DOCX | Full text extraction |
| TXT / MD | Read directly |
| Pasted text | No upload needed |

Image-first content (charts, diagrams, photos) is excluded from extraction by default unless you explicitly request image analysis.

---

## Compression rules

The skill applies these rules to every output:

- **Section 1** — 2–3 short sentences for the whole-content judgment
- **Sections 2+** — every bullet, table cell, chain node, and callout is **one sentence**
- **Evidence** — at most 1 strongest example per logic chain step; the rest are dropped
- **Section count** — 3 sections for short sources; 3–5 for longer ones

---

## Repo structure

```
visual-summary/
├── SKILL.md                        # Skill instructions and workflow
├── visual-summary.skill            # Packaged skill file (one-click install)
├── references/
│   ├── summary-framework.md        # Classification and output skeletons
│   ├── ui-guidelines.md            # Visual rendering rules
│   ├── ui-authoring-rules.md       # Component and pattern usage
│   ├── design-system.md            # Token and color system
│   └── cases-summary-reference.md  # Calibration examples
├── assets/
│   └── ui/                         # Design system: CSS tokens, component kits
├── scripts/
│   └── extract_text.py             # Zero-dependency text extraction
├── agents/
│   └── openai.yaml                 # Codex / OpenAI agent metadata
└── examples/                       # Rendered HTML output gallery
```

---

## Compatibility

Works across any host that supports the [Agent Skills open standard](https://agentskills.io):

- Claude Code
- Claude.ai (paid plans)
- Claude API
- OpenAI Codex
- Gemini CLI
- Cursor
- Windsurf

---

## License

Apache 2.0 — free to use, modify, and redistribute. See [LICENSE](LICENSE).
