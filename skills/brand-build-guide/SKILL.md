---
name: brand-build-guide
description: Bouw automatisch een complete, upload-klare organizational brand skill uit aangeleverde huisstijl-materialen — huisstijlboeken/brand books (PDF), logo's, kleur- en font-specificaties, tone-of-voice documenten, voorbeeldteksten en voorbeeld-templates, of een website. De skill leest die bronnen, extraheert design tokens (kleuren met rollen, typografie, logo, spacing, footer) en tone of voice, en genereert een nette merk-skill (SKILL.md + references + design-tokens.json + HTML-rapport- en e-mail-scaffolds) die direct als .zip/.skill te uploaden is naar organizational skills. Gebruik bij vragen als "maak een brand skill", "bouw een huisstijl-skill", "turn our brand book into a skill", "genereer een merk-skill uit deze documenten", "brand-build-guide", of wanneer iemand huisstijlboeken/voorbeeldtemplates uploadt om er een herbruikbare merk-skill van te maken.
---

# Brand Build Guide — generate a perfect organizational brand skill

**EN:** This is a meta-skill. It turns uploaded brand materials (brand books, logos, color/font specs, tone-of-voice docs, example texts and templates, or a website) into a complete, upload-ready **organizational brand skill** — a folder with a `SKILL.md`, reference files, a `design-tokens.json`, and ready-to-use HTML-report and email scaffolds. The output mirrors a proven structure (colors, typography, tone of voice, HTML reports, email).

**NL:** Dit is een meta-skill. Hij maakt van aangeleverde huisstijl-materialen automatisch een volledige, upload-klare **merk-skill**. Output-dekking: design tokens (kleuren, fonts, spacing), tone of voice, HTML-rapport en e-mail. (Word, PowerPoint en e-mailhandtekening zijn optionele uitbreidingen — zie §6.)

## 0. What this skill produces / Wat dit oplevert

A generated brand skill named like `acme-brand/` with this exact layout:

```
<brand>-brand/
├── SKILL.md                      # tokens table + CSS-var block + hard rules + checklist (bilingual)
├── references/
│   ├── design-tokens.md          # the full token reference (colors, fonts, spacing, logo, footer)
│   ├── voice-and-tone.md         # voice, formality, do/don't, phrasings, examples
│   ├── html-reports.md           # report/dashboard scaffold + chart palette
│   └── email.md                  # branded email/newsletter scaffold (inline CSS, Outlook-safe)
└── assets/
    ├── design-tokens.json        # machine-readable single source of truth
    ├── report-scaffold.html      # working HTML report, CSS variables filled
    └── email-scaffold.html       # working email, inline values filled
```

Deliver it as a `.zip` (or `.skill`) with the brand folder at the top level, ready to upload under organizational skills.

## 1. Workflow — always follow these five steps

1. **Intake** — gather and confirm the brand materials and basics.
2. **Extraction** — read the materials and pull out tokens + voice.
3. **Generation** — build the brand skill folder from the blueprint.
4. **Packaging** — validate and zip into an upload-ready file.
5. **Delivery** — present the zip + upload steps + the QA report.

Do not skip the intake or the validation. A wrong color or an over-long description means the skill is either off-brand or rejected on upload.

## 2. Step 1 — Intake

First, check what the user already gave you (uploaded files in the conversation, a website URL, pasted text). Then use **`AskUserQuestion`** to fill the gaps. Ask only what you cannot already infer.

Collect:
- **Brand name** and any parent/sister entities (for the skill name, e.g. `acme-brand`, and the footer).
- **Materials available** (multi-select): brand book / style guide (PDF), logo files or URL, color list, font names, tone-of-voice document, example texts, example templates (email/report/Word), website URL.
- **Coverage** — default: design tokens, tone of voice, HTML report, email. Confirm or extend.
- **Language** of the generated skill — default bilingual (English core + brand-language triggers/examples).
- **Logo hosting** — a public URL is strongly preferred (email/PDF need an external `src`). If only a file is provided, note it must be hosted and use a `{{LOGO_URL}}` placeholder.

If a brand book PDF is uploaded, you can extract its text with `scripts/extract_brand_assets.py` (optional helper) or read it directly. Then read `references/intake-and-extraction.md` for exactly what to pull out and how.

## 3. Step 2 — Extraction

Read **`references/intake-and-extraction.md`**. Extract and write down, before generating:

- **Colors with roles** — not just hex values, but what each is *for*: primary/brand, accent, body text, secondary text, background, card, border, soft fill, zebra, link, plus status tints (positive/warning/critical). Mapping color → role is the most important and most error-prone step.
- **Typography** — primary font stack + fallbacks, weights, size scale.
- **Logo** — public URL, render sizes, alt text.
- **Spacing & shape** — padding rhythm, border radius, shadows.
- **Footer / contact block** — company, address, phone, website, and (for invoices) IBAN/VAT/CoC as placeholders if unknown.
- **Voice & tone** — formality, sentence style, do/don't list, greetings/sign-offs, number/date format.

Fill `assets/design-tokens.json` against `assets/design-tokens.schema.json`. This JSON is the single source of truth the generated skill is built from.

When a value is genuinely unknown, use a clearly marked placeholder (e.g. `<vul IBAN in>` / `{{LOGO_URL}}`) — never invent brand values.

## 4. Step 3 — Generation

Read **`references/output-blueprint.md`** (the full bilingual `SKILL.md` template and the reference set to generate) and **`references/scaffolds.md`** (the brand-neutral HTML report + email + voice templates with `{{TOKEN}}` placeholders). Then:

1. Create the `<brand>-brand/` folder.
2. Write `SKILL.md` from the blueprint, filling every `{{PLACEHOLDER}}` from the tokens.
3. Write the four reference files (`design-tokens.md`, `voice-and-tone.md`, `html-reports.md`, `email.md`).
4. Write the three assets (`design-tokens.json`, `report-scaffold.html`, `email-scaffold.html`).
5. Leave **no** unfilled `{{PLACEHOLDER}}` except intentional `<vul ... in>` data placeholders.

Match colors to roles deliberately (see the blueprint's mapping rules). A brand's "primary" is whatever it uses for titles/links; its "accent" is the highlight color used sparingly — never swap these.

## 5. Step 4 & 5 — Packaging, validation, delivery

Read **`references/packaging-and-upload.md`**. Then:

1. Run `scripts/validate_brand_skill.py <brand>-brand/` — checks single `SKILL.md`, valid frontmatter, **description ≤ 1024 characters** (hard upload limit), token completeness, and no leftover `{{PLACEHOLDER}}`.
2. Fix anything it flags. The description limit is a real upload-blocker — keep it under 1024.
3. Run `scripts/package_skill.py <brand>-brand/ <output-dir>` to produce `<brand>-brand.zip` with the folder at the top level.
4. Present the zip and the upload steps (organizational skills → Upload skill → drag the zip).
5. Print the QA report from `references/quality-checklist.md`.

## 6. Notes & deliberate scope

- **Default coverage**: tokens, voice, HTML report, email. To add **Word**, **PowerPoint**, or an **email signature** reference, follow the same pattern (one reference file + the brand tokens) — see the blueprint's "optional add-ons".
- **Brand vs. document-templates**: this skill builds the *brand/house-style* skill. Platform document templates (e.g. Current RMS / MoreApp) are a separate skill — keep them out of the brand skill, and only mention the split in the generated skill's routing.
- **Never invent brand values.** Missing color/font/logo → ask, or use a marked placeholder.
- **One SKILL.md per skill.** Supporting docs go in `references/` as non-`SKILL.md` files (the upload API rejects multiple `SKILL.md`).

## 7. Reference map

| Read when | File |
|---|---|
| Gathering materials + extracting tokens/voice | `references/intake-and-extraction.md` |
| Building the generated skill (full SKILL.md template + reference set) | `references/output-blueprint.md` |
| Filling the HTML report / email / voice templates | `references/scaffolds.md` |
| Zipping, the 1024-char limit, upload steps | `references/packaging-and-upload.md` |
| Final QA before delivery | `references/quality-checklist.md` |
| Token shape / a worked example | `assets/design-tokens.schema.json`, `assets/example-design-tokens.json` |
