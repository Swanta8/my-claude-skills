---
name: brand-build-guide
description: Bouw, refactor of review een huisstijl-skill voor een merk (zoals keypro-brand of hooft-petiet-brand). Trigger op "ik wil een brand skill maken voor X", "huisstijl skill", "merk-skill opzetten", "nieuwe brand skill", "blueprint voor een brand skill", "wat moet er in mijn brand skill", "review/fix mijn brand skill". Gebruik ALTIJD wanneer de gebruiker een brand-skill begint of verbetert, ook zonder expliciete term — "ik wil een skill die mijn huisstijl toepast op rapporten en e-mails" valt hieronder. Levert een 12-delige blauwdruk voor SKILL.md, een intake-checklist (design tokens, voice-rules, footer-data, sister-mappings), token-templates (CSS + JSON), een sjabloon-SKILL.md en description-engineering tips zodat de uiteindelijke brand-skill betrouwbaar triggert. Niet gebruiken voor losse documenten of templates zonder skill-context (dan keypro-brand, hooft-petiet-brand of skill-creator).
---

# Brand Skill Build Guide

Eén bron voor het bouwen van een nieuwe brand-skill (huisstijl-skill) volgens hetzelfde patroon als `keypro-brand` en `hooft-petiet-brand`. Werkt voor élk merk dat consistente output nodig heeft over meerdere formaten (rapporten, e-mail, Word, PDF, presentaties).

## Wanneer deze skill gebruiken

Trigger bij élke vraag die neerkomt op "help me een brand-skill bouwen":

- "Ik wil een huisstijl-skill voor [merk]"
- "Maak een brand skill voor [merk X]"
- "Review de structuur van mijn brand skill"
- "Mijn brand skill triggert niet goed — kun je het fixen?"
- "Wat moet er allemaal in een brand skill?"
- "Kun je een blueprint geven voor een merk-skill?"

Ook gebruiken bij refactor van een bestaande brand-skill, of wanneer iemand vraagt om twee brand-skills te vergelijken/harmoniseren.

**Niet gebruiken** voor: één losse template (dan `keypro-brand` of `hooft-petiet-brand`), of voor algemene skill-creatie zonder brand-context (dan `skill-creator`).

## De 12 onderdelen van een brand-skill

Elke goed werkende brand-skill bevat deze 12 onderdelen in deze volgorde. Mist er één, dan triggert de skill slecht of produceert hij onbetrouwbare output.

| # | Onderdeel | Doel |
|---|---|---|
| 1 | **YAML frontmatter** | Triggerwoorden, contexts, wat de skill levert |
| 2 | **Wanneer gebruiken** | Expliciete signaalwoorden + "use even when not explicit" |
| 3 | **Brand identity at a glance** | Persoonlijkheid + voice + visueel ritme in 1 paragraaf |
| 4 | **Design tokens (source of truth)** | Kleuren, typo, spacing, radii, shadows — concreet |
| 5 | **Copy-paste CSS-block** | `:root` met variabelen, direct kopieerbaar |
| 6 | **Anatomy / skeleton** | De vaste opbouw van een deliverable (5–7 elementen) |
| 7 | **Routing tabel** | "Wil je X → lees Y" verwijst naar format-references |
| 8 | **Output contract** | Wat moet er bij elke deliverable: framing + artifact + checklist |
| 9 | **Hard rules** | 8–12 niet-onderhandelbare regels |
| 10 | **Brand compliance checklist** | 5–8 bullets ter controle voor verzending |
| 11 | **Sister-entity mapping** | Hoe omgaan met zustermerken en rebrand-acties |
| 12 | **Bestandsoverzicht** | Wat zit waar (transparantie voor onderhoud) |

Een sjabloon-SKILL.md met alle 12 secties als invul-blokken staat in `assets/skill-md-template.md`.

## Workflow voor het bouwen van een nieuwe brand-skill

Volg deze vijf stappen in volgorde. Sla geen stap over — vooral stap 1 niet, want zonder volledige intake bouw je een skill die later moet worden teruggedraaid.

### Stap 1 — Intake

Lees `references/intake-checklist.md` en loop hem hardop door met de gebruiker. Verzamel élk veld voor je begint te schrijven. Onbekende waarden expliciet markeren als `[TE-VERIFIEREN]` — niet gokken. Je hebt minimaal nodig: logo URL, primaire kleur, accentkleur(en), font stack, voice in 1 paragraaf, footer-contactblok.

### Stap 2 — Tokens

Vul `assets/tokens-template.css` en `assets/tokens-template.json` in op basis van de intake. Beide formats horen erbij: CSS voor HTML-output, JSON als machine-leesbare spiegel voor scripts en validatie. Naamprefix per merk (bv. `--kp-`, `--hp-`) om collisions te voorkomen wanneer twee brand-skills in dezelfde sessie actief zijn.

### Stap 3 — Format references

Bepaal welke outputformaten de skill moet ondersteunen. Maak per format één bestand in `references/`. Veelvoorkomende set:

- `references/report-html.md` — HTML-rapport (900px container, shadow, Roboto)
- `references/email.md` — Outlook-veilige e-mail (680px, table-based, inline CSS)
- `references/word-docx.md` — `python-docx` patronen
- `references/powerpoint.md` — `python-pptx` of tokens-based deck
- `references/data-components.md` — tabellen, KPI-cards, status-chips (bij data-output)
- `references/voice-and-tone.md` — schrijfregels, u/je, groeten, verboden frases
- `references/email-signature.md` — handtekening per medewerker

Niet alle formaten zijn altijd nodig. Begin met de twee waar de gebruiker daadwerkelijk output in produceert. Voeg toe wanneer een nieuw format opduikt — beter een kleine, scherpe skill dan een grote met dode references.

Kopieer een werkend HTML/template van een bestaande skill (`keypro-brand/assets/template-*.html` of `hooft-petiet-brand/references/html-reports.md`) als startpunt. Bouw nooit een format-reference from-scratch wanneer er een vergelijkbare bestaat.

### Stap 4 — SKILL.md schrijven

Start vanuit `assets/skill-md-template.md`. Vul de 12 secties in. Houd het onder 500 regels — duik dieper in references als je over die limiet gaat.

Speciale aandacht voor de **frontmatter description**: zie sectie "Description engineering" hieronder.

### Stap 5 — Sanity check

Loop deze vijf vragen langs voordat de skill in gebruik gaat:

1. Triggert de description op realistische zinnen ("maak ons rapport", "in onze huisstijl", impliciete brand-vermeldingen)? Test 3 prompts mentaal.
2. Levert sectie 4 (design tokens) een eenduidige waarde per token — geen "ongeveer dit groen, of misschien dat"?
3. Is het logo een live HTTPS-URL, geen lokale path, geen verouderde CDN?
4. Staat in de compliance-checklist élk onveranderlijk merkkenmerk dat in "Hard rules" wordt genoemd?
5. Lost de skill een echt probleem op? Zo nee: verbeter de tokens of voeg een format toe waar de gebruiker daadwerkelijk in werkt.

## Wat moet de gebruiker aanleveren

Niets bouwen zonder deze input. Volledige checklist in `references/intake-checklist.md`. Korte versie:

- **Identiteit**: merknaam, varianten, parent-/zusterentiteiten
- **Kleuren**: primair, accent, status (positief/negatief/warn), tekst, achtergrond, border, soft-fill, zebra
- **Typografie**: font stack (web), font fallback (Outlook), font fallback (Word/PPT), type-schaal
- **Logo**: live HTTPS-URL + max widths per context + alt text
- **Spacing/radii/shadows**: outer, card, table cell padding; radius card/inner/pill; shadow email/PDF
- **Footer**: contactregels, met regel-voor-regel weglaten-regels
- **Voice**: persoonlijkheid in 1 paragraaf, u/je-conventies, do/don't, groeten/afsluitingen
- **Formaten**: welke outputs moeten ondersteund worden
- **Lokalisatie**: datum-, getal-, valuta-format, taal
- **Hard rules**: 8–12 niet-onderhandelbare regels
- **Sister mapping**: per token, als rebrand-functie nodig is

## Description engineering (cruciaal voor triggering)

Brand-skills ondertriggeren standaard, omdat gebruikers zelden expliciet "huisstijl" zeggen. Volg deze vier principes voor de frontmatter description:

1. **Noem alle synoniemen**: "huisstijl", "ons rapport", "onze mail", "merkkleuren", "brand colors", "company template", "in onze branding", plus alle merknaam-varianten (volledig, afkorting, domein).
2. **Noem alle outputformaten** waar de skill voor werkt — rapporten, e-mails, dashboards, MoreApp PDF, Word, etc.
3. **Voeg een expliciete trigger-instructie toe** zoals: "Use whenever output will represent the [merk] brand — even if the user does not say 'huisstijl'."
4. **Eindig met wat de skill concreet levert** — tokens, templates, checklist — zodat het model snapt wat de uitkomst is.

Voorbeeld-zin uit `hooft-petiet-brand`: *"Use whenever output will represent the Hooft & Petiet brand — even if the user does not say 'huisstijl' — including reports, customer emails, memos, dashboards, MoreApp PDF/email HTML, and any 'make this look like our brand' request."*

## Universele hard rules (voor élke brand-skill)

Deze regels horen in iedere brand-skill thuis, ongeacht het merk:

1. **Logo is een live HTTPS-URL**, nooit een lokale path, nooit een placeholder.
2. **Eén bron van waarheid voor tokens** — CSS-variabelen in `:root` met JSON-spiegel. Improviseer nooit hex-codes elders in de skill.
3. **Container-breedtes vaststellen per format** (typisch 900px PDF/HTML, 680px e-mail).
4. **Font stack expliciet per context**: web (Roboto eerst), email (Arial eerst voor Outlook), Word/PPT (system-safe fallback).
5. **Datum/getal-format vastleggen** op één plek — voor NL: decimaalkomma, datum lang "maandag 11 mei 2026".
6. **Footer is altijd compleet of regel-voor-regel weggelaten** — nooit een lege rij renderen.
7. **Voice is bindend**: geen emoji's, geen marketing-superlatieven, geen uitroeptekens (tenzij quote).
8. **WCAG-contrast adresseren** wanneer de primaire kleur op wit onder 4.5:1 zit — geef een donkere link-variant.
9. **Geen flexbox/grid in e-mail**: Outlook breekt. Tabel-based layout, inline CSS, MSO conditional comments voor knoppen.
10. **Sister-entities expliciet maken**: weet welk merk overneemt, hoe gerebrand wordt, en wanneer naar een andere skill verwezen wordt.

## Bestandsoverzicht

```
brand-build-guide/
├── SKILL.md                          # Dit bestand
├── references/
│   └── intake-checklist.md           # Welke info verzamelen voor je begint
└── assets/
    ├── skill-md-template.md          # Lege SKILL.md met de 12 secties
    ├── tokens-template.css           # Lege CSS-variabelen
    └── tokens-template.json          # Lege JSON design-tokens-spiegel
```

## Referentie-skills (good examples)

Twee bestaande, werkende brand-skills die als good-example dienen:

- `keypro-brand/` — compact, references-heavy, includes Python helper script
- `hooft-petiet-brand/` — uitgebreid in SKILL.md, MoreApp-coverage, JSON tokens

Kopieer geen tekst letterlijk over — die zijn merk-specifiek — maar gebruik ze als structurele referentie en als bron van werkende HTML/CSS-patronen.
