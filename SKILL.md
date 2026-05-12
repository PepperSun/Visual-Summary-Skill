---
name: visual-summary
description: create styled HTML visual summaries from long documents, articles, transcripts, notes, pdfs, docx, txt, markdown, images with readable text, or extracted text. use when an agent or model host needs to summarize, visualize, convert, rebuild, or render source content into either a skill-facing landing page or a local app product flow with input, loading, auth setup, and output states. especially useful for argumentative, explanatory, narrative, lyrical, or record-style documents. supports output language selection and visual styles named clear, mature, and vibrant.
---

# Visual Summary

## Goal

Transform source documents into visualized knowledge pages. Rebuild the source structure instead of merely compressing text.

Final outputs from this skill should always be styled HTML pages. Plain text or Markdown may be used during extraction, drafting, or reference lookup, but they are not a final delivery format.

The reader should quickly understand:
1. what the document is doing
2. the core judgment or feeling
3. how the content advances
4. why the argument or explanation works
5. what evidence or scenes support it

## Host portability

Keep the core workflow host-agnostic.

- use the same `SKILL.md`, `references/`, `scripts/`, and `assets/` bundle across Codex, Claude, Gemini, or other model hosts that support installable skills or reusable agent instructions
- adapt invocation syntax locally; do not assume a host-specific command format unless the current host requires one
- prefer direct file upload when the host supports it; otherwise extract Markdown or text first and pass that normalized content to the model
- treat `agents/openai.yaml` as optional OpenAI or Codex UI metadata; hosts that do not use it can ignore it without affecting the core skill

## Default workflow

1. Ingest the user document or pasted text.
2. When a strong local parser is available, extract normalized Markdown or text before prompting. Strip repeated headers, footers, page numbers, hard wraps, and duplicate boilerplate first. Use the same parsing path across host-integrated skill mode and local app mode when consistency matters.
3. Read `.txt`, `.md`, and short pasted text directly, then normalize whitespace and repeated boilerplate instead of routing them through a heavier conversion stack.
4. Extract text and formulas. Parse text-bearing content only by default. Do not infer meaning from diagrams, charts, screenshots, or other image-first content unless the user explicitly asks for image analysis.
5. If the source is a scanned PDF or image-first document and text extraction is weak or empty, switch early to a stable OCR or page-reading path.
6. Keep OCR, chart extraction, picture description, and similar enrichments off by default. Enable them only when the user explicitly asks and the implementation actually supports them.
7. Detect title policy from the source itself. If no document title is visible or extractable, leave the title empty or fall back to the source publication, column, or series name. Never invent a new title.
8. Detect output language: follow the document language unless the user specifies English, Simplified Chinese, or Traditional Chinese.
9. Detect visual style: use Mature by default; use Clear or Vibrant only when requested.
10. Detect source length. For short sources, use exactly 3 major sections. Treat Chinese sources under about 2,000 characters or English sources under about 1,500 words as short sources. For longer sources, keep the summary within 3 to 5 major sections unless the user asks for more detail.
11. Classify the content using `references/summary-framework.md`.
12. Produce the structured summary using the correct output skeleton.
13. Apply language and voice rules from `references/summary-framework.md`: use third-person objective voice, avoid generic AI phrasing, and keep final wording compact.
14. Render the final result as a styled HTML visual page. Use `references/ui-guidelines.md`.
15. Distinguish between two product directions before rendering UI: assistant-integrated skill mode or local app mode.
16. For skill-only landing mode, reuse `assets/ui/product/visual-summary-skill-home.html`.
17. For local app mode, reuse `assets/ui/product/visual-summary-app.html` as the canonical flow example.
18. Use logic chains for causal or inferential structures. Keep tables for parallel structures. Do not convert parallel reasoning into prose.

## Classification sequence

Always classify in this order:

1. form: narrative, argumentation, lyric, or record
2. intent: inform, explain, persuade, resonate, entertain, or preserve
3. structure: chronology, space, logic, taxonomy, comparison, nested, or free
4. type: select the closest subtype under the detected form
5. skeleton: choose the summary skeleton from `references/summary-framework.md`

For persuasive texts, always determine whether it is stance persuasion, rebuttal persuasion, or synthesis persuasion. The output must include the author's preference ranking or core positive claim, not a neutral description. For rebuttal texts, the first section should describe what is being rebutted; if the author restates their own positive claim through the rebuttal, place that reaffirmed claim in the final section.

## Output rules

Use the source content as the basis. Avoid adding external facts unless the user requests research.

### Section compression

Apply this to every structured summary:

1. **Section 1** — may use 2 or 3 short sentences or lines when the source needs a whole-content judgment.
2. **Sections 2+** — every bullet, row, evidence point, rebuttal, residual judgment, and table cell must stay to one simple sentence.
3. **If a point needs more than one sentence** — split it into separate rows or drop the lower-priority detail instead of stacking clauses into prose.

### Content priority hierarchy

Apply this hierarchy to every document type, not just argumentation:

1. **Core claim** — the judgment or position the author returns to repeatedly. Always preserve in full.
2. **Logic chain** — the reasoning structure that leads to the core claim. Always preserve the chain as a whole; this is as important as the claim itself.
3. **Supporting evidence** — cases, data, anecdotes, and examples used to back individual steps in the logic chain. These are low priority. Omit most of them. For each step in the logic chain, keep at most 1 of the most forceful pieces of evidence by default. Use 2 only when each piece does different work. The rest should be dropped entirely.

The summary should feel complete at the claim and logic level, and alive at the evidence level — not exhaustive at any level.

Use 3 to 5 major blocks for non-narrative content according to the source. For short sources, use exactly 3 major blocks. Control item count. Auxiliary structures normally should contain no more than 6 rows or bullets unless the source requires more.

For lyric, memoir, diary-like, or strongly first-person essays, keep the source stance, movement, and perceptual emphasis, but write the summary in compact third-person objective voice. Do not let first-person scenes override trunk-based classification.

When the source contains a parallel structure, use a table. Use logic chains for causality or inference. When points, categories, cases, or dimensions unfold in parallel rather than through causality, inference, or time, prefer a table. Required cases include:
- opponent claim versus author rebuttal
- option A versus option B
- old method versus new method
- multiple categories in parallel
- multiple cases compared

When the source rejects or limits an interpretation, create a separate section for rebuttal, boundary condition, or residual judgment only if that point is not already handled in the main structure. Do not repeat the same boundary or rebuttal in multiple sections.

Evidence should support the relevant section where the claim is made. Do not create a standalone evidence section unless the source itself is organized as an evidence catalogue or the user explicitly asks for one.

Section titles must be content-specific and follow the source's main movement. Avoid generic skeleton labels such as Core mechanism, Key clarification, or Supplement in the rendered page unless they are also meaningful titles for this specific document. When in doubt, calibrate section titles against `references/cases-summary-reference.md`, but do not copy them mechanically.

For rebuttal texts that also reaffirm the author's own thesis:
- section 1 should state the dispute or critique being answered, not jump straight to the author's final doctrine
- the rebuttal table should carry the concrete opponent claims and replies
- the mechanism section should explain how the rebuttal works
- the final section should synthesize the author's reaffirmed core claim, such as how secondary factors are subordinated to the main mechanism

For argumentation with a clear top-level judgment and direct, oral, or commentary-like delivery:
- make section 1 the whole-content block when the source has a clear top-level judgment
- write that block in 2 or 3 short sentences or lines; avoid long, nested, clause-heavy sentences
- keep the header metadata-only when section 1 is carrying the whole-content summary; do not place the main summary directly under the title
- move history or chronology later when it functions as support rather than as the trunk of the piece
- decide whether a comparison is the trunk or only support; if it is only support, state the author's final judgment first and place the comparison after it
- place speech-at-a-glance, big-numeral, or dashboard-style overview panels after the main conclusion blocks unless the source itself is primarily quantitative

When a table has more than 3 rows, highlight at least one load-bearing phrase in each row or major cell cluster. Do not let only one row carry the visual emphasis.

When the user gives explicit formatting or PRD-like corrections during iteration, treat those corrections as higher priority than the default skeleton for that output.


## Compression and voice rules

Use the source's language unless the user requests a different output language.

For short sources, keep the summary compact:
- Chinese sources under about 2,000 characters: use exactly 3 major sections.
- English sources under about 1,500 words: use exactly 3 major sections.
- Omit optional supplement sections when they would only restate the core claim.

Avoid generic AI summary phrasing. Prefer plain, direct wording with short sentences. In Chinese, avoid formulaic constructions such as “不是……而是……”, “如果说……则是……”, stacked negative openings, stiff analyst language, overextended metaphor chains, and prose-level colons or em dashes. In English, prefer simple syntax and restrained wording.

Negative Chinese patterns to avoid:
- “身份设定不是在告诉模型‘怎么写’，而是在告诉它‘你是谁’。”
- “这不是简单的‘编’，而是一种更高级、更具欺骗性的幻觉。”
- “不是因为它‘知道更多’，而是因为它会在回答前先‘想一想’。”
- “如果说案例 1 验证了……案例 2 要验证的则是另一个更微妙的变量。”
- “它做的事情更像是一个遥控器……那是天线的事，不是遥控器能管的。”

When using a metaphor, keep it brief and stop once the comparison has clarified the point. Do not extend one metaphor into a multi-link analogy chain. In body prose, prefer periods or commas over colons and em dashes unless a label, table, or literal source formatting requires them.

Write the final summary in compact third-person objective voice, including for first-person sources. If the source is lyric, memoir, diary-like, or strongly personal, keep its feeling, image, and stance, but do not imitate its first-person speaking position in the final summary.

### Token discipline

Reduce prompt size before the model sees the source:

- prefer locally normalized Markdown or text over raw document binaries
- strip repeated page headers, footers, page numbers, blank-line runs, parser noise, and duplicate boilerplate
- merge hard-wrapped body lines when they do not change structure
- send lightweight metadata separately from the main extracted text when possible

## Visual page requirements

Generate a single self-contained styled HTML page unless the user asks for a multi-file project. The page should include:

- document header: title, author if available, date if available, generated tags
- summary blocks based on classification
- visual hierarchy through cards, grids, tables, timelines, and concise icons
- a visible affordance for creating a new summary if the page represents a product UI
- clear loading or progress states if creating an app flow

Do not overdecorate. The visual layer should clarify structure, not compete with the content.

If the source title is missing, keep the header restrained and explicit about the fallback choice. Use the publication or column name if needed, but do not fabricate a document title for visual neatness alone.

If the source contains decorative cover art, inserted images, or screenshots and the user did not ask for image analysis, omit them from the rendered summary page by default.

For argumentative and speech-based pages, let the first substantive summary block start the content. Do not let hero copy, intro prose, timeline panels, or glance cards displace section 1.

For product-style outputs:
- separate skill-only landing mode from local app mode
- for skill-only landing mode, do not show a working upload button or any false implication that the page can parse files directly
- for local app mode, parse files in the backend rather than the browser
- for local app mode, when a parser backend exists, send extracted Markdown or text to the model instead of raw document binaries
- for local app mode, keep the parser profile consistent with the skill path when consistency matters
- for local app mode, make the input page show upload, output language, output style, and API-access controls
- for local app mode, treat the API key as backend-managed state; the frontend collects it but should not be the long-term storage layer
- for local app mode, auto-enter loading after upload rather than waiting on a second submit step unless the user asks for a slower wizard-like flow
- keep loading visible with explicit progress items
- add a top-right new-summary action on the summary page that opens a clean input page without destroying the current output
- add a top-right landing-page entry on the summary page that opens a new page when the summary belongs to the Visual Summary product flow
- if auth or model calls fail in local app mode, reopen the API-entry path so the user can correct the stored key
- use small icons in upload cards, progress items, API status cards, and section headers only when they help orientation

## Resource usage

Read `references/summary-framework.md` before summarizing documents, including classification, output skeleton, compression, evidence placement, and language/person rules.
Read `references/ui-guidelines.md` before generating the final HTML output, React implementation, or product UI.
Read `references/ui-authoring-rules.md` when translating structure into highlights, callouts, tables, chains, timelines, numerals, or taxonomy blocks.
Read `references/design-system.md` when selecting a style or browsing the bundled component and pattern library.
Read `references/cases-summary-reference.md` when the user asks for bundled examples, case studies, sample outputs, in-skill reference passages, or section-title calibration.
Open `assets/ui/index.html` when you need a quick visual index of the bundled kits and comparison patterns.
Use `scripts/extract_text.py` when a local file needs basic zero-dependency extraction and normalization, and no stronger built-in document tool is available.
Reuse `assets/ui/product/visual-summary-skill-home.html` when the user asks for a skill landing page.
Reuse `assets/ui/product/visual-summary-app.html` when the user asks for a local upload-to-summary app shell or a default local product flow.
Reuse `assets/ui/design-canvas.jsx` when the user wants a canvas-like design surface or iterative layout playground instead of a static page.
