<!--
SKILL.md TEMPLATE — Brand Skill
================================

Gebruik dit sjabloon als startpunt voor een nieuwe brand-skill. Vervang elke
[PLACEHOLDER] met merk-specifieke inhoud uit de ingevulde intake-checklist.

Verwijder na invullen:
- Alle HTML-commentaar zoals dit blok
- De korte uitleg-zinnen onder elke sectietitel (cursief)
- Onderdelen die niet van toepassing zijn voor dit merk

Doelgrootte: 200-450 regels. Onder 500 blijven. Bij meer: verplaats naar
references/.
-->

---
name: [brand-slug]-brand
description: [DESCRIPTION — zie sectie "Description engineering" hieronder. Bouw een agressieve, trigger-rijke description die NAAM-varianten, synoniemen, output-formaten en een expliciete "use even when not explicit" instructie bevat. Eindig met wat de skill levert (tokens, templates, checklist).]
---

# [BRAND_NAME] huisstijl

*Eén centrale bron voor design tokens, layoutpatronen en kant-en-klare templates voor alle [BRAND_NAME]-output.*

## Wanneer deze skill gebruiken

*Lijst alle expliciete signalen waarop de skill moet activeren — wees ruim. Brand-skills ondertriggeren standaard.*

Activeer deze skill bij élke deliverable die [BRAND_NAME] vertegenwoordigt:

- [Format 1 — bv. rapporten, dashboards]
- [Format 2 — bv. klantmail, interne updates]
- [Format 3 — bv. Word-documenten, voorstellen]
- [Format 4 — bv. presentaties]
- [Format 5 — bv. handtekening, signature]

Ook gebruiken bij vermelding van [ZUSTERMERK_1] of [ZUSTERMERK_2] — zelfde merkfamilie, zelfde tokens (tenzij gebruiker expliciet een sub-variant noemt).

**When in doubt: apply.** Brand-compliance is goedkoop; brand-drift is duur.

## Brand identity at a glance

*Eén paragraaf die persoonlijkheid, voice en visueel ritme samenvat. Dit is de "smell test" — leest het als [BRAND_NAME]?*

**Persoonlijkheid**: [BV. CALM_PROFESSIONAL_NO_NONSENSE — pas aan]

**Voice**: [BV. Korte zinnen, actief, formeel "u" in klantcontact, "je" intern]

**Visueel ritme**: [BV. Cards op soft-fill achtergrond, [PRIMARY_COLOR_HEX] als accent, één font ([FONT_NAME]) overal, centered logo footer]

## Snelstart: kies de juiste route

*Routing-tabel. Verwijst per format naar één reference-file. Verwijder rijen voor formaten die deze skill niet ondersteunt.*

| Vraag | Lees |
|---|---|
| HTML rapport of PDF maken | `references/report-html.md` + `assets/template-report.html` |
| E-mail opstellen (Outlook-veilig) | `references/email.md` + `assets/template-email.html` |
| Word/.docx document | `references/word-docx.md` |
| Presentatie | `references/powerpoint.md` |
| Data-componenten (tabellen, KPI-cards, chips) | `references/data-components.md` |
| Voice & tone | `references/voice-and-tone.md` |
| Alleen design tokens | `references/design-tokens.md` of laad `assets/tokens.css` |

## Onveranderlijke merkregels

*8–12 niet-onderhandelbare regels. Letterlijk overgenomen uit sectie 11 van de intake-checklist.*

1. **Logo URL**: altijd `https://[LIVE_LOGO_URL]`. Nooit placeholder, nooit verouderde CDN.
2. **Primaire kleur**: `[#PRIMARY]` voor [HEADINGS/LABELS/LINKS].
3. **Accent**: `[#ACCENT]` — alleen voor [CTA/BUTTONS/HIGHLIGHT].
4. **Font**: [PRIMARY_FONT] (web), Arial-eerst (e-mail), [WORD_FALLBACK] (Word).
5. **Container-breedte**: [N]px PDF/HTML rapport, [M]px e-mail.
6. **Datum-format**: "[DATUM_VOORBEELD]" — nooit andere notatie.
7. **Getallen**: decimaal[KOMMA/PUNT], duizendtallen [PUNT/KOMMA], valuta met spatie.
8. **Footer altijd compleet** of regel-voor-regel weggelaten. Nooit blanco rij.
9. **Geen emoji's, geen marketing-superlatieven**.
10. [REGEL_10]
11. [REGEL_11]
12. [REGEL_12]

## Design tokens (single source of truth)

*Concrete waardes. Geen schattingen. Laadt `assets/tokens.css` of inline een `:root` block.*

| Token | Waarde | Gebruik |
|---|---|---|
| Primair | `#PRIMARY` | Titels, labels, links |
| Accent | `#ACCENT` | CTA, highlight |
| Tekst body | `#TEXT_BODY` | Body copy |
| Tekst muted | `#TEXT_MUTED` | Captions, footer |
| Achtergrond page | `#BG_PAGE` | Page background |
| Card | `#FFFFFF` | Card surface |
| Border | `#BORDER` | Borders, dividers |
| Soft-fill | `#SOFT_FILL` | Table header, label-cell |
| Zebra | `#ZEBRA` | Alternating rows |
| Font stack | `'[FONT]', Arial, Helvetica, sans-serif` | Everything |

## CSS variable block (copy-paste)

*Eén `:root` block dat letterlijk in elk HTML-deliverable gekopieerd kan worden.*

```css
:root {
  --[prefix]-primary: #PRIMARY;
  --[prefix]-accent: #ACCENT;
  --[prefix]-bg: #BG_PAGE;
  --[prefix]-card: #FFFFFF;
  --[prefix]-soft: #SOFT_FILL;
  --[prefix]-border: #BORDER;
  --[prefix]-text: #TEXT_BODY;
  --[prefix]-muted: #TEXT_MUTED;
  --[prefix]-zebra: #ZEBRA;
  --[prefix]-link: #LINK;
  --[prefix]-radius-card: 12px;
  --[prefix]-radius-inner: 10px;
  --[prefix]-shadow-card: 0 4px 12px rgba(0,0,0,.08);
  --[prefix]-font: '[FONT]', Arial, Helvetica, sans-serif;
}
```

## Anatomy van een deliverable

*De vaste opbouw. Wat zit waar, in welke volgorde, en welke elementen mogen NIET ontbreken.*

Elke gebrande output volgt deze skelet:

1. **[ELEMENT_1]** — bv. top accent bar (6px, primary color)
2. **[ELEMENT_2]** — bv. titel block, centered
3. **[ELEMENT_3]** — bv. meta-table (label/value)
4. **[ELEMENT_4]** — bv. content cards
5. **[ELEMENT_5]** — bv. centered logo footer

Sla je [ELEMENT_X] of [ELEMENT_Y] over, dan is de output niet langer [BRAND_NAME].

## Workflow voor elke output

1. **Identificeer het format** — kies de juiste reference (routing tabel hierboven).
2. **Laad de tokens** — neem `assets/tokens.css` over of inline de `:root` block.
3. **Gebruik de template als basis** — start vanuit `assets/template-*.html`. Begin niet from-scratch.
4. **Pas de merkregels toe** — loop alle 8–12 langs.
5. **Bij data-output**: lees ook `references/data-components.md`.

## Output contract

*Wat moet de skill altijd produceren bij élke deliverable.*

1. **Korte framing** (1–3 zinnen) — type artifact + aannames over scope/content.
2. **Complete artifact** — nooit een snippet. Voor HTML: volledig document met `<!DOCTYPE html>`.
3. **Brand compliance checklist** — 5–8 bullets ter controle.

## Brand compliance checklist

*Loop bij élke output deze bullets langs voor verzending.*

- [ ] Kleuren matchen de design tokens exact (geen off-brand kleuren)
- [ ] [FONT] toegepast als font-stack overal
- [ ] [KENMERK_X — bv. groen top-accent aanwezig] op container
- [ ] Primaire kleur voor titels/labels, niet voor body
- [ ] Logo URL = `https://[LIVE_LOGO_URL]`
- [ ] Footer compleet en zonder lege rijen
- [ ] Voice klopt — formeel/informeel passend bij context, geen marketing-superlatieven
- [ ] [Voor data-output] cijfers rechts uitgelijnd met `tabular-nums`

## Veelvoorkomende valkuilen

*Bekende issues die telkens terugkomen — adresseren voor verzending.*

- **Outlook breekt op flexbox/grid** — e-mail altijd `<table role="presentation">` + MSO conditional comments.
- **Google Fonts laden niet in e-mail** — Arial-eerst in e-mail font-stack. PDF/HTML mag wel met [FONT] beginnen.
- **WCAG-contrast**: `#[PRIMARY]` op wit is [X]:1. Voor lange link-runs in body: gebruik `#[LINK_SAFE]`.
- **Bedragen rechts uitlijnen** met `font-variant-numeric: tabular-nums`.
- **Logo nooit lokaal opslaan** — altijd live linken voor consistente updates.

## Sister-entiteiten en rebrand

*Hoe gaat de skill om met zustermerken? Verwijst naar andere skills of biedt mapping voor rebrand.*

[BRAND_NAME] is onderdeel van [PARENT_GROUP]. Zustermerken zijn [ZUSTER_1] en [ZUSTER_2].

- Voor [ZUSTER_1]-output: gebruik [zuster-1-brand] skill (apart merk, andere kleuren/logo).
- Voor rebrand vanuit [ANDER_MERK] naar [BRAND_NAME]: pas de mapping toe uit `assets/tokens.css` sectie sister-rebrand. Vervang [ANDER_PRIMARY] → `#PRIMARY`, [ANDER_ACCENT] → `#ACCENT`, [ANDER_LOGO_URL] → `https://[LIVE_LOGO_URL]`.

## Bestandsoverzicht

```
[brand-slug]-brand/
├── SKILL.md                          # Dit bestand
├── references/
│   ├── design-tokens.md              # Tokens uitgebreid (optioneel naast tokens.css)
│   ├── report-html.md                # HTML/PDF rapport patronen
│   ├── email.md                      # Outlook-veilige e-mail patronen
│   ├── word-docx.md                  # Word styling met python-docx
│   ├── powerpoint.md                 # PPT styling met python-pptx
│   ├── data-components.md            # Tabellen, chips, KPI-cards
│   └── voice-and-tone.md             # Schrijfregels, u/je, groeten
├── assets/
│   ├── tokens.css                    # CSS-variabelen, single source of truth
│   ├── tokens.json                   # Machine-leesbare spiegel
│   ├── template-report.html          # Werkend HTML/PDF template
│   └── template-email.html           # Werkend Outlook-compatible template
└── scripts/
    └── [brand_prefix]_docx.py        # Python helper voor python-docx (optioneel)
```
