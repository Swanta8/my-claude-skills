# Quality Checklist — final QA for the generated brand skill

Run this before delivering. Report each item as ✅ / ⚠️ and fix ⚠️ before zipping. `scripts/validate_brand_skill.py` automates the structural items; the brand-judgment items are on you.

## Structure & upload-readiness (mostly automated)

- [ ] Exactly one `SKILL.md`, at the folder root
- [ ] Frontmatter has valid `name` and `description`
- [ ] `name` = `{{brand_slug}}-brand` and matches the folder name
- [ ] `description` ≤ 1024 characters
- [ ] No leftover `{{PLACEHOLDER}}` anywhere (intentional `<vul ... in>` data placeholders are allowed and should be listed for the user)
- [ ] `assets/design-tokens.json` is valid JSON and validates against the schema
- [ ] All four reference files present (`design-tokens.md`, `voice-and-tone.md`, `html-reports.md`, `email.md`)
- [ ] `report-scaffold.html` and `email-scaffold.html` present and contain no `{{...}}`

## Brand correctness (human judgment)

- [ ] Every color came from the source material (none invented); roles assigned correctly (primary = titles/links, accent = highlight)
- [ ] Accent color is NOT used as body text; titles use the primary
- [ ] Font stack starts with the brand font, with sensible fallbacks; email ordering is Outlook-safe if the brand font is a web font
- [ ] Logo URL is public and correct; render sizes set; footer block complete with no empty rows
- [ ] Status tints are on-brand (not Bootstrap red/green) unless the brand specifies
- [ ] Number/date/currency format matches the brand's locale
- [ ] Voice section reflects the real source copy (formality, do/don't, greetings) — not generic filler

## Coverage & scope

- [ ] Generated coverage matches what was agreed (default: tokens, voice, HTML report, email)
- [ ] Any requested add-ons (Word, PowerPoint, signature) included via the same pattern
- [ ] No platform document templates (Current RMS / MoreApp) bundled into the brand skill — only referenced as a separate concern if relevant

## Deliverable

- [ ] Zip built with the folder at the top level, excludes `.DS_Store`/junk, passes `unzip -t`
- [ ] User told the upload steps and any `<vul ... in>` placeholders they still need to complete

## Output a short report

End by printing, for the user:
1. The brand name, color roles (hex + role), and font chosen.
2. Coverage included.
3. Any unfilled data placeholders they must complete.
4. The path to the zip and how to upload it.
