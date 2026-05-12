# UI Guidelines

Use these guidelines when generating a visual output page or product prototype. The bundled design system is in `assets/ui/`. The source design rules are also summarized in `references/design-system.md` and `references/ui-authoring-rules.md`.

Final outputs from this skill should always be styled HTML pages. Plain Markdown summaries may be used only as internal reference material, case references, or drafting intermediates.

## Product flow

Support two different delivery modes. Pick one deliberately instead of blending them.

### 1. Skill-only landing mode

Use this when the user wants a homepage, landing page, or explanation page for the skill itself and not a standalone local app.

In this mode:
- do not present a working upload control
- do not imply that the page itself can parse files
- do not show fake loading or fake summary transitions
- explain that the skill is meant to be invoked inside a host assistant or model workspace
- show example prompts or integration guidance instead

The canonical example is:
- `assets/ui/product/visual-summary-skill-home.html`

### 2. Local app mode

Use this when the user wants a local HTML app, browser app shell, or upload-to-summary experience backed by a local server.

The input page should show three areas:
1. upload entry: PDF, image, TXT, DOCX, and similar text-bearing files; recommend files under 50 MB
2. output language: follow source language by default, or choose English, Simplified Chinese, Traditional Chinese; it is fine to note that more languages will be supported later
3. output style: Clear, Mature, Vibrant; default to Mature

For local app mode, also include an API access area:
- let the user enter a model-provider API key in the frontend
- send it to the local backend for storage
- do not persist the API key in browser storage by default
- show backend/auth status clearly
- if model calls fail because of auth or backend state, reopen the API-entry path so the user can correct it

Make it clear on the input page that the current parser extracts text and formulas only. Do not imply that charts, diagrams, photos, or other image-first content are being semantically parsed unless the user explicitly asked for image analysis and the implementation actually supports it.

After upload, transition directly into loading unless the user explicitly asked for a multi-step wizard. The loading state should show progress items such as:
- uploading file and options
- extracting text and formulas
- calling the model
- rendering visual summary

Use either a separate input page, route, or state for the upload screen. Do not collapse the upload controls into the summary page by default.

The output page should include a "new summary" action at the top right. Opening it should lead to a clean input page without destroying the current output page. In a single-file prototype, prefer a clean input state reset rather than silently reusing stale summary data.
When the summary page belongs to the Visual Summary product itself, also include a visible top-right entry that opens the landing page in a new page so users can quickly review the tool's basic capabilities. For bundled local assets, prefer the sibling path `./visual-summary-skill-home.html`.

## Page structure

Every output page should include:
- title
- author, if available
- writing date, if available
- generated tags for domain and subdomain only; do not display internal classification values such as form, intent, structure, subtype, or output style as content tags
- summary sections selected from the framework

After section 1, prefer compact lists, tables, and chains over prose blocks. Keep each later bullet, cell, node, or callout to one direct sentence.

## Design system source

Use `assets/ui/colors_and_type.css` as the canonical token source. It defines three styles under `[data-style="clear"]`, `[data-style="mature"]`, and `[data-style="vibrant"]`. `:root` defaults to Clear.

Use one style only per page. Set the style on the page root, for example:

```html
<body data-style="clear">
```

Do not mix Clear, Mature, and Vibrant in one output unless the user explicitly asks for a style comparison.

## Style modes

### Clear

Use Clear when explicitly requested. It feels light, soft, and breathable.

Key traits:
- near-white background and white surfaces
- pastel families: blue, teal, lavender, mint, peach
- Inter typography
- pill geometry and soft shadows
- thin borders and generous spacing
- safest choice for general readers and non-experts

Use Clear for most articles, explainers, reports, and neutral summaries.

### Mature

Use Mature as the default. It is suited for refined editorial output, long-form essays, literary/philosophical works, or dense analytical writing.

Key traits:
- ivory paper background
- locked palette: ivory, lilac, chestnut, ink only
- Source Serif display with Inter body
- square geometry, no rounded card softness
- no decorative extra colors
- hierarchy through type, spacing, and restrained accenting

Mature has a locked highlight rule: `<b>...</b>` renders as bold serif on lilac. Use it only for load-bearing phrases.

### Vibrant

Use Vibrant for manifesto-style, polemical, business-book, or decisive argumentative content.

Key traits:
- saturated primaries: blue, yellow, red, green, purple, ink
- bold sans typography
- strong outlines and visible accents
- pill geometry with decisive blocks
- no tints or shades unless already defined by the token file

Preserve readability. Vibrant should be more assertive, not crowded.

## Highlight grammar

Highlight only load-bearing phrases of 1 to 6 words. A phrase is load-bearing when removing it would collapse the sentence's meaning. In comparison or rebuttal tables with more than three rows, highlight load-bearing phrases inside cells so the table does not become visually flat.

Do not highlight whole sentences.

Markup by style:
- Clear: `<span class="hl hl-blue">...</span>`, also teal/lav/mint/peach when useful
- Mature: `<b>...</b>`
- Vibrant: `<span class="h hl-yellow">...</span>` or another defined vibrant highlight class

## Pattern menu

Choose the primitive based on the summary structure:
- Timeline: events on a time axis, dates, ages, eras, historical evolution
- Comparison: N objects across M dimensions, especially A vs B or old vs new
- Logic chain: A causes B causes C; mechanism, inference, process
- Big numerals: scale, quantity, ratio, magnitude, threshold, rank

For parallel reasoning, prioritize comparison tables over prose. For causal or inferential reasoning, use a logic chain. For time evolution, use a timeline. For scale, use a big numeral block with context. When points, categories, cases, or dimensions unfold in parallel rather than through causality, inference, or time, prefer a table. Avoid rendering optional sections that duplicate claims, boundaries, or residual judgments already covered in a table.

## Component guidance

Use cards for summary blocks, tables for parallel structures, timelines for chronology, and compact callouts for boundary conditions or residual judgments.

Icons may be used to help orientation, but the text structure is primary. Prefer small utility icons in upload cards, loading steps, metadata lines, API status cards, and section headers. Avoid decorative complexity that makes the summary harder to scan. Rendered section headings should be specific to the document, not generic skeleton names. Do not render section 2 and later as long prose paragraphs.

For rebuttal pages where the author reaffirms a positive thesis through the rebuttal, render that reaffirmed claim as the final summary block. Do not display it as a metadata tag, a standalone evidence section, or a repeated boundary-condition table.

## Implementation guidance

When generating an exportable or shareable prototype, prefer a self-contained HTML file or a single React component. Reuse the CSS token names from `assets/ui/colors_and_type.css`.

When writing React, include the CSS tokens directly in the component or as a companion CSS block when the user requests a single-file implementation. Do not reference local paths from the user's computer. If assets are needed, use only bundled assets under `assets/ui/` or assets uploaded in the current conversation.

Canonical examples are available in:
- `assets/ui/elements/clear.html`
- `assets/ui/elements/mature.html`
- `assets/ui/elements/vibrant.html`
- `assets/ui/comparison/*.html`
- `assets/ui/product/visual-summary-app.html`
- `assets/ui/product/visual-summary-skill-home.html`
- `assets/ui/design-canvas.jsx`
