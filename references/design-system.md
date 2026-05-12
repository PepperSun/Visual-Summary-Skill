# Visualized Knowledge — Design System

A design system for turning a book or essay into a structured, **visualized summary**: chapters become chains, claims become highlighted phrases, perspectives become side-by-side blocks, scale becomes big numerals. The system should make the document structure easier to see rather than add decoration around a generic summary. After the first section, compress content into one-sentence cells, chains, or cards instead of long prose.

## The three styles

| Style | Voice | Use when |
|---|---|---|
| **Clear** | Light, soft, breathable |  Most non-experts feel safe here, normal. |
| **Mature** | Refined editorial | The default. Long-form essays, literary or philosophical works. |
| **Vibrant** | Loud, primary, decisive | Manifesto-style, polemic, business-book energy. |

There is **no Atlas / Fieldnote / Meridian** — those earlier directions were retired. Every component, pattern, and token is defined for these three styles only.

## How it's organized

| Path | What's there |
|---|---|
| `colors_and_type.css` | Tokens for all three styles, scoped under `[data-style="<name>"]`. `:root` defaults to Mature. |
| `elements/{clear,mature,vibrant}.html` | The **canonical** kit per style — palette, type, tags, buttons, inputs, highlight rule, four chart-pattern primitives. |
| `comparison/*.html` | One element per file, rendered side-by-side in all three styles. Use these to compare or pick. |
| `SKILL.md` | Authoring rules: highlight grammar, palette discipline, pattern menu. |

## Where to start

Open `index.html` — the system index links every kit and comparison.

## Foundations (× 3 styles each)

- **Palette** — `comparison/palette.html`
- **Typography** — `comparison/type.html`
- **Special type** — `comparison/special-type.html` · CJK · numerals · quotes · micro labels · formulas
- **Highlight rule** — `comparison/highlight.html`
- **Callouts & specials** — `comparison/callout.html` · note · warning · key · definition · footnote
- **Icons** — `comparison/icons.html`

## Components (× 3 styles each)

- **Buttons** — `comparison/buttons.html`
- **Inputs** — `comparison/inputs.html`
- **Cards** — `comparison/cards.html`

## Patterns — the structural primitives (× 3 styles each)

- **Timeline** — `comparison/pattern-timeline.html`
- **Logic chain** — `comparison/pattern-logic.html`
- **Chain (4 stages)** — `comparison/chain.html`
- **Comparison · 3-col** — `comparison/pattern-comparison.html`
- **Contrast block · A vs B** — `comparison/contrast.html`
- **Dense table · 6 × 7** — `comparison/table-dense.html` · row + column grouping per style
- **Tree / taxonomy** — `comparison/tree.html`
- **Exhibition listing / compact grids** — use cards, dense tables, or taxonomy patterns depending on the source
- **Big numerals** — `comparison/pattern-numerals.html`

## Activating a style

```html
<body data-style="clear">    <!-- or "mature" / "vibrant" -->
  <p>What changed is the <b>story we live inside</b>.</p>
</body>
```

In Mature, `<b>` automatically renders as the bold-serif lilac highlight (the locked rule). In Clear and Vibrant, use the per-style highlight markup shown in `elements/`.

## Caveats

- All faces are loaded from Google Fonts. No self-hosted webfont licensing yet.
- Logos and marks were removed in the cleanup pass — if a brand-mark direction is needed, ask and I'll do one specifically for the chosen style.
