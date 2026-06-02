# Output Blueprint — the generated brand skill

This is the exact structure and content to generate. Fill every `{{PLACEHOLDER}}` from `design-tokens.json`. Placeholders use `{{...}}`; intentional unknown *data* (like IBAN) uses `<vul ... in>` and may remain.

## Folder layout to create

```
{{brand_slug}}-brand/
├── SKILL.md
├── references/
│   ├── design-tokens.md
│   ├── voice-and-tone.md
│   ├── html-reports.md
│   └── email.md
└── assets/
    ├── design-tokens.json        # the filled tokens (single source of truth)
    ├── report-scaffold.html      # from references/scaffolds.md, tokens filled
    └── email-scaffold.html       # from references/scaffolds.md, tokens filled
```

`{{brand_slug}}` = lowercase, hyphenated brand name (e.g. "Acme Living" → `acme-living`). Skill `name` = `{{brand_slug}}-brand`.

## SKILL.md template (fill all placeholders)

> Keep the `description` **under 1024 characters** (hard upload limit). Include both what it does and brand-specific trigger phrases in the brand's language AND English. Be a little "pushy" on triggering.

````markdown
---
name: {{brand_slug}}-brand
description: Apply the {{brand_name}} house style and brand voice to any deliverable — colors, typography/fonts, tone of voice, and visual output such as HTML reports, dashboards, and branded emails/newsletters. Triggers on "{{brand_name}}", {{brand_aliases_quoted}}, "onze huisstijl", "ons rapport", "onze e-mail", "huisstijl", "merkkleuren", "brand colors", "tone of voice", "company template", and on any request to make a deliverable look or sound like {{brand_name}} — even without the word "huisstijl". Use whenever output will represent the {{brand_name}} brand. {{optional_sister_line}}
---

# {{brand_name}} — Brand & House Style

**EN:** Single source of truth for the {{brand_name}} visual identity and brand voice: colors, typography, tone of voice, and on-brand visual deliverables (HTML reports, dashboards, branded email/newsletter).

**NL:** De centrale bron voor de {{brand_name}} huisstijl en merkstem: kleuren, typografie, tone of voice en visuele output (HTML-rapporten, dashboards, branded e-mail).

## 1. When to use / Wanneer gebruiken

Trigger eagerly. If a deliverable might be seen by a customer or colleague on behalf of {{brand_name}}, apply this skill. Signals: mentions of {{brand_name}}/{{brand_aliases_plain}}, "onze huisstijl", "ons rapport", "onze mail", "maak hier een grafiek van", "tone of voice". When in doubt: apply.

## 2. Brand identity at a glance

**Personality / Persoonlijkheid:** {{personality}}

**Voice:** {{voice_oneliner}} Full guide in `references/voice-and-tone.md`.

**Visual rhythm:** Cards on {{bg}} background, {{radius_card}} corners, a {{accent}} accent, {{primary}} for titles/labels/links, {{font_short}} throughout, centered logo footer.

## 3. Design tokens (source of truth)

Machine-readable in `assets/design-tokens.json`. Never improvise colors or fonts.

| Token | Value | Use |
|---|---|---|
| Primary | `{{primary}}` | Titles, labels, links, buttons |
| Accent | `{{accent}}` | Accent bar, highlights — never as text |
| Primary text | `{{text_primary}}` | Body copy |
| Secondary text | `{{text_secondary}}` | Captions, footer |
| Background | `{{bg}}` | Page background, zebra |
| Card | `{{card}}` | Surfaces |
| Border | `{{border}}` | Borders, dividers |
| Soft fill | `{{soft}}` | Table headers, label cells |
| Zebra | `{{zebra}}` | Alternating rows |
| Link | `{{link}}` | Hyperlinks |
| Font stack | `{{font_stack}}` | Everything |

Status tints: positive `{{status_positive_text}}` on `{{status_positive_bg}}`; warning `{{status_warning_text}}` on `{{status_warning_bg}}`; critical `{{status_critical_text}}` on `{{status_critical_bg}}`.

**Logo:** `{{logo_url}}` — centered, {{logo_email_size}} in email footer, {{logo_report_size}} in report footer.

**Footer block (omit empty lines):**
```
{{footer_company}}
{{footer_address}}
{{footer_phone}}
{{footer_website_display}}
```

## 4. CSS variable block (copy-paste)

```css
:root {
  --brand: {{primary}};
  --accent: {{accent}};
  --bg: {{bg}};
  --card: {{card}};
  --soft: {{soft}};
  --border: {{border}};
  --text: {{text_primary}};
  --muted: {{text_secondary}};
  --zebra: {{zebra}};
  --link: {{link}};
  --radius-card: {{radius_card}};
  --font: {{font_stack}};
}
```

## 5. Anatomy of a branded deliverable

1. Top accent — a {{accent_bar_height}} {{accent}} bar on the main card.
2. Title block — {{primary}} title.
3. Meta/summary — bordered table, {{primary}} labels on {{soft}}.
4. Content cards — {{soft}} header band, {{primary}} title, white body.
5. Footer — centered logo + contact lines. Always.

## 6. Routing

| Want | Read |
|---|---|
| HTML report / dashboard / web | `references/html-reports.md` |
| Branded email / newsletter | `references/email.md` |
| Tokens (colors/fonts/spacing) | `references/design-tokens.md` |
| Voice & tone, copy examples | `references/voice-and-tone.md` |

## 7. Hard rules

- Only the tokens above. For signals use the status tints — never Bootstrap red/green.
- {{font_short}} first, fallbacks only as listed.
- Accent is for the bar/highlights, never body text. Titles use {{primary}}, not the accent.
- No CTA unless asked. No empty footer rows. No emoji unless requested.
- Logo URL is always `{{logo_url}}`.
- {{locale_number_date_rule}}

## 8. Compliance checklist

- [ ] Colors match tokens exactly
- [ ] {{font_short}} applied throughout
- [ ] Accent used as bar/highlight, primary for titles/links
- [ ] Logo URL correct, footer complete with no empty rows
- [ ] {{locale_short}} number/date format where relevant
- [ ] Voice on-brand, no marketing fluff

For platform document templates (if the org uses them) keep those in a separate templates skill; only reference the split here.
````

## Reference files to generate

Generate these four from `references/scaffolds.md` (which holds the brand-neutral templates with the same `{{...}}` tokens):

1. **`references/design-tokens.md`** — a readable table of every token + the `:root` block + the status tints + logo/footer. Essentially section 3–4 expanded, with a short "how to use in HTML/email" note.
2. **`references/voice-and-tone.md`** — from the extracted voice: personality paragraph, formality table by context, sentence do/don't, greetings/sign-offs, vocabulary swaps, number/date format, and 2–3 before/after examples.
3. **`references/html-reports.md`** — the full report scaffold from `scaffolds.md` (container → top accent → header → meta → blocks → footer), the dashboard grid + KPI tile, the chart palette (`primary`, `accent`, `text_secondary`, then reduced opacity), and a "common mistakes" list.
4. **`references/email.md`** — the email scaffold from `scaffolds.md`: inline CSS, `<table>` layout, `Margin` capital-M on body, max-width ~680px, preheader, top accent, centered logo footer, optional meta table + CTA (CTA in `primary`, only on request).

## Color → role mapping (apply when filling)

- `primary` = the color used for titles/links in the source.
- `accent` = the sparing highlight color; if the source has none, set `accent` = `primary` and skip the bar, or derive a tint.
- `soft` = a light tint of `primary`/`accent` used for table headers; if absent, lighten `primary` to ~10–15% opacity equivalent.
- `link` defaults to `primary`.
- Keep `card` = `#ffffff` and neutrals as-is unless the brand specifies otherwise.

## Optional add-ons (only if coverage requested)

Same pattern, one reference file each, all driven by the same tokens:
- `references/word-docs.md` — A4 setup, heading/table colors, python-docx color constants.
- `references/powerpoint.md` — 16:9, master colors, slide layouts, chart palette.
- `references/email-signature.md` — table-based signature with the accent divider.
