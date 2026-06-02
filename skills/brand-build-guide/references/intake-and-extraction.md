# Intake & Extraction

How to gather brand materials and pull out everything the generated brand skill needs. Goal of this step: a fully filled `design-tokens.json` plus a clear voice-and-tone summary, with nothing invented.

## 1. Materials checklist

Ask for / look for these. More is better, but you can build a solid skill from just a brand book or even a single well-branded example template.

| Material | What you get from it |
|---|---|
| Brand book / style guide (PDF) | Colors (hex/CMYK/RGB), typography, logo rules, spacing, do/don't, voice |
| Logo files or a public logo URL | The `logo.url` (must be web-hosted for email/PDF) and alt text |
| Color list / swatches | Exact hex values and their names/roles |
| Font specification | Primary font, weights, fallbacks |
| Tone-of-voice document | Formality, sentence style, vocabulary, greetings/sign-offs |
| Example texts (emails, web copy) | Real voice in practice — extract patterns, not just rules |
| Example templates (email/report/Word) | Layout rhythm, header/footer, table styling, component patterns |
| Website URL | Live colors/fonts/voice when no brand book exists (fetch and inspect) |

If little is provided, start from the strongest single source and mark the rest as `ask` or placeholder. Do not guess brand values.

## 2. Reading the sources

- **PDF brand book**: read it directly, or run `scripts/extract_brand_assets.py <file.pdf>` to dump text and any hex codes it finds. Look for pages titled "Kleur/Color", "Typografie/Typography", "Logo", "Tone of voice".
- **Images (logo, swatches)**: you can view them. Read hex values printed next to swatches; do not eyedrop-guess a hex from a JPEG unless no numeric value exists, and then mark it as approximate.
- **Website**: fetch the page; inspect CSS for `color`, `background`, `font-family`, and the logo `src`. The most-used non-neutral color is usually the brand/primary; the most-used heading color too.
- **Example templates**: the footer block, header bar, and table header colors are gold — they encode the house style precisely.

## 3. Colors — extract by ROLE, not just value

This is the most important and most error-prone step. A list of hexes is useless without roles. For every color, decide what it is *for*:

| Role | Definition | Typical use |
|---|---|---|
| `primary` / brand | The main brand color | Titles, labels, links, primary buttons |
| `accent` | A second brand color used sparingly | Top accent bar, highlights — often NOT used as text |
| `text_primary` | Body text color | Paragraph copy |
| `text_secondary` | Muted text | Captions, footer, metadata |
| `heading` | Optional darker heading | Headings if different from primary |
| `bg` | Page background | Behind cards |
| `card` | Surface | Card/container background (often `#ffffff`) |
| `border` | Dividers | Table/borders |
| `soft` | Soft fill | Table headers, label cells, highlight boxes |
| `zebra` | Alternating rows | Striped tables |
| `link` | Hyperlinks | Usually equals `primary` |
| status `positive` / `warning` / `critical` | Signal tints (text + soft bg) | Chips, deltas |

**Mapping rules:**
- The color a brand puts on **titles/links** is the `primary`. The bright color it uses as a thin bar or highlight (and rarely as text) is the `accent`. Never swap these.
- If the brand has only one strong color, use it as `primary` and derive `soft` as a very light tint of it for table headers.
- Status tints should be earth-toned and on-brand, not Bootstrap red/green, unless the brand book says otherwise.
- Keep neutrals (`#000`, `#fff`) as-is.

Record every color in `design-tokens.json` under `colors`, keyed by role.

## 4. Typography

- `primary_font_stack`: the brand font first, then safe fallbacks, e.g. `"Brandont", Arial, Helvetica, sans-serif`.
- Note an email-safe ordering if the brand font is a web font (put a system font first for Outlook).
- `weights`: title (700–900), label (700), body (400).
- `sizes`: a small scale (title, block title, body, caption, footer).

If the brand uses a paid/web font that won't load in email/PDF, record the fallback and note it.

## 5. Logo, spacing, footer

- **Logo**: `url` (public), render sizes (email footer, report footer), `alt`. If only a file exists, set `url` to `{{LOGO_URL}}` and tell the user it must be hosted.
- **Spacing/shape**: outer padding, card padding, table cell padding, border-radius, shadows. Defaults are fine if the brand book is silent — record them so output is consistent.
- **Footer/contact block**: company name, address, phone, website (display + href), email. For invoice-capable brands also IBAN/VAT/CoC — use `<vul ... in>` placeholders if unknown.

## 6. Voice & tone

From the tone doc and example texts, capture:
- **Formality** per context (customer vs internal) and the form of address (e.g. NL "u" vs "je").
- **Sentence style**: length, active/passive, jargon level.
- **Do / Don't** list (e.g. no exclamation marks, no marketing superlatives).
- **Greetings & sign-offs**, formal and informal.
- **Number/date/currency format** for the brand's locale.
- 2–3 **before/after** rewrite examples if the source gives enough material.

## 7. Output of this step

A filled `assets/design-tokens.json` (validate against `assets/design-tokens.schema.json`) and a short voice summary. Only then move to generation (`references/output-blueprint.md`).
