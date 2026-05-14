# Visualized Knowledge — Authoring Skill

Use this when producing a visualized book/essay summary in any of the three styles.

## 1. Pick a style. One only.

- `data-style="clear"` — default, light pastels, pill geometry
- `data-style="mature"` — ivory paper, lilac highlight, square geometry
- `data-style="vibrant"` — saturated primaries, ink outlines, bold sans

Set on `<body>` (or page root). Never mix.

## 2. Honor the palette

| Style | Operating colors |
|---|---|
| Clear | 5 pastel families (blue · teal · lavender · mint · peach) + neutrals |
| Mature | 4 colors locked: ivory · lilac · chestnut · ink. **No others.** |
| Vibrant | Blue · yellow · red · green · purple + ink. No tints, no shades. |

## 3. The highlight is the workhorse

Highlight only **load-bearing phrases** — 1–6 words that, if removed, would collapse the sentence's meaning.

| Style | Markup | Look |
|---|---|---|
| Clear | `<span class="hl hl-blue">…</span>` (or teal/lav/mint/peach) | Pastel pill behind the words |
| Mature | `<b>…</b>` | Bold serif on solid lilac, 1.06× size |
| Vibrant | `<span class="h hl-yellow">…</span>` | Solid yellow/red pill, bold sans |

Never highlight whole sentences.

## 4. Pattern menu

Pick the right primitive for the structure. Use visual structure to clarify reasoning, not to decorate it.

- **Timeline** — when events sit on an axis (dates, ages, eras)
- **Comparison** — when N objects vary across M dimensions
- **Logic chain** — when A causes B causes C
- **Big numerals** — when scale itself is the point
- **Exhibition listing** — when 3 to 8 items need parallel display across 3 to 6 compact columns
- **Taxonomy tree** — when categories have parent-child relations

Each pattern has a per-style realization. See `comparison/pattern-*.html`.

After the first section, every cell, line, or node should stay to one direct sentence.



## 5. Pattern constraints from summary rules

Use these constraints unless the user gives a more specific design direction.

### Timeline

Use for chronology, evolution, eras, ages, or dated stages. Prefer about 5 time knots. Each knot should carry 2 to 4 compact perspectives when useful. Each perspective should stay to one sentence and usually be 10 to 20 words. If the source uses intensity, certainty, priority, or risk, a 5-star or 5-step rating can be used.

### Comparison

Use for 2 to 3 objects compared across 5 to 10 dimensions. Each cell should stay to one sentence and usually be 10 to 20 words. When comparing operating models, methods, or systems, cover execution, cost, organization, and decision-making when relevant.

### Logic chain

Use for mechanism, inference, process, or causality. Keep the chain to 4 to 8 stages. Each stage can carry 2 to 4 compact perspectives. Keep each stage line to one sentence. If the chain grows beyond 8 stages, compress adjacent steps or switch to a short explanatory paragraph. If the items are parallel points, categories, cases, or dimensions with no causal, inferential, or temporal order, switch to a table or exhibition listing.

### Exhibition listing

Use for category displays, case collections, or compact knowledge cards. Prefer 3 to 6 columns and 3 to 8 rows or cards. Keep each cell to one sentence and short enough to scan, usually 10 to 20 words.

### Dense tables

For tables with more than 3 rows, highlight at least one load-bearing phrase in each row or major cell cluster. Do not let only the first row or one column carry all emphasis.

## 6. Case reference behavior

Use `references/cases-summary-reference.md` as examples of summary structure and compression, not as templates to copy mechanically. Match the current source first. Use cases to resolve ambiguity about rebuttal structure, narrative layers, argumentation with direct or commentary-like delivery, or chain evidence. When in doubt, calibrate section titles against `references/cases-summary-reference.md`, but do not copy them mechanically.

## 7. References

- `elements/{clear,mature,vibrant}.html` — full kit per style
- `comparison/*.html` — one element across all three styles
- `colors_and_type.css` — all tokens
