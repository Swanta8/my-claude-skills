# Brand Skill Intake Checklist

Volledige lijst van wat verzameld moet worden voordat je een brand-skill gaat bouwen. Loop deze hardop door met de gebruiker. Onbekende waarden expliciet markeren als `[TE-VERIFIEREN]` en pas invullen wanneer geverifieerd — gok niet.

Werkmethode: kopieer deze hele checklist naar een nieuwe markdown-file in je werk-directory, vul per regel in, en gebruik dat ingevulde bestand als input voor stap 2 (tokens) en stap 4 (SKILL.md schrijven).

---

## 1. Identiteit

| Veld | Waarde |
|---|---|
| Merknaam (volledig) | |
| Merknaam (afkorting) | |
| Variant in URL/domein | |
| Parent-/holding-entiteit | |
| Zustermerken | |
| Tagline (indien aanwezig) | |
| Persoonlijkheid in 1 zin | |

Zustermerken zijn belangrijk: wanneer de gebruiker iets in het ene merk vraagt maar het uiteindelijk in een ander zustermerk moet, moet de skill weten welke andere skill aan te roepen of welke mapping toe te passen.

## 2. Kleuren

| Token | Hex | Toelichting |
|---|---|---|
| Primaire merkkleur | | Waar gebruikt: headings, accents, links? |
| Accent-/secundaire kleur | | Beperkingen: alleen CTA? Alleen header? |
| Tekst — body | | |
| Tekst — heading (donker) | | |
| Tekst — secondary/muted | | |
| Achtergrond — page | | |
| Achtergrond — card | | |
| Soft-fill (table headers, label-cells) | | |
| Zebra-fill (alternating rows) | | |
| Border / table divider | | |
| Link-kleur | | Vaak gelijk aan primair |
| Link-kleur (a11y-veilig) | | Donkere variant bij contrast <4.5:1 |
| Status positief — vol | | |
| Status positief — soft | | |
| Status negatief — vol | | |
| Status negatief — soft | | |
| Status warn — vol | | |
| Status warn — soft | | |

Status-tints zijn optioneel maar aanbevolen voor data-output (KPI-deltas, chips). Als het merk geen status-kleuren heeft: kies tinten die harmoniëren met de primaire kleur in plaats van Bootstrap-rood/groen.

## 3. Typografie

| Veld | Waarde |
|---|---|
| Primaire font (web) | bv. `Roboto, Arial, Helvetica, sans-serif` |
| Email font stack (Outlook eerst) | bv. `Arial, Roboto, Helvetica, sans-serif` |
| Word fallback (system-safe) | bv. `Calibri` |
| PowerPoint fallback | bv. `Arial` |
| Font-CDN URL (optioneel) | bv. Google Fonts URL |

**Type-schaal:**

| Element | Web/PDF | Email | PPT |
|---|---|---|---|
| H1 / titel | | | |
| Block-titel | | | |
| Body | | | |
| Caption / klein | | | |
| Footer | | | |

**Weights:**

| Gebruik | Weight |
|---|---|
| Titel | bv. 800 |
| Label/heading | bv. 700 |
| Body | bv. 400 |

## 4. Logo

| Veld | Waarde |
|---|---|
| Logo URL (live HTTPS) | |
| Max width — email footer | bv. 160px |
| Max width — PDF footer | bv. 120px |
| Max width — email signature | bv. 80px |
| Alt text | |
| Donkere variant URL (optioneel) | |

**Belangrijk:** logo móet via een stabiele HTTPS-URL beschikbaar zijn. Lokale paths werken niet in e-mail, en CDN-URL's die per release veranderen breken de skill stilletjes. Controleer dat de URL minstens 6 maanden onveranderd is gebleven.

## 5. Spacing, radii, shadows

| Token | Waarde |
|---|---|
| Outer page padding | bv. `24px 12px` |
| Card padding (PDF) | bv. `22px` |
| Card padding (email) | bv. `18px 22px` |
| Table cell padding | bv. `10px 12px` |
| Block-gap | bv. `8px` |
| PDF page margin | bv. `14mm 12mm 16mm 12mm` |
| Radius — card | bv. `12px` |
| Radius — inner element | bv. `10px` |
| Radius — pill button | bv. `999px` |
| Radius — photo | bv. `12px` |
| Shadow — email card | bv. `0 4px 12px rgba(0,0,0,.08)` |
| Shadow — PDF container | bv. `0 6px 18px rgba(0,0,0,.08)` |

## 6. Container-breedtes

| Format | Max-width |
|---|---|
| Email | bv. 680px |
| HTML-rapport | bv. 900px |
| PDF | bv. 900px |
| Dashboard | bv. 1200px (vol-breedte) |

## 7. Footer-contactblok

Per regel, in renderingsvolgorde. Geef ook aan welke regels overslaan-bij-leeg moeten zijn versus altijd verplicht.

| Regel | Inhoud | Altijd of overslaan-bij-leeg |
|---|---|---|
| Bedrijfsnaam | | altijd |
| Adres | | |
| Telefoon | | |
| Website | | |
| KVK / BTW | | overslaan |
| Slogan (optioneel) | | |

Belangrijk: nooit een blanco regel renderen. Beter een rij weglaten dan een lege rij tonen.

## 8. Voice & tone

| Veld | Antwoord |
|---|---|
| Persoonlijkheid (1 paragraaf) | |
| Customer email — u of je | |
| Customer PDF — u of je | |
| Interne mail — u of je | |
| Documentatie — u of je | |
| Marketing/web copy — u of je | |
| Gemiddelde zinslengte (woorden) | bv. 12–18 |
| Actief of passief | |
| Emoji's toegestaan | |
| Uitroeptekens toegestaan | |

**Verboden woorden of frases** (bv. "uniek", "ongeëvenaard", "het beste van het beste"):

- 
- 
- 

**Standaard groeten (formeel):**

- 
- 

**Standaard groeten (informeel):**

- 
- 

**Standaard afsluitingen:**

- 
- 

## 9. Outputformaten

Welke formaten moet de skill ondersteunen? Vink aan wat van toepassing is.

- [ ] HTML-rapport (PDF-print via browser of headless Chromium)
- [ ] E-mail (klant, intern, transactioneel)
- [ ] E-mail signature
- [ ] Word document (`.docx` via `python-docx`)
- [ ] PowerPoint (`.pptx` via `python-pptx`)
- [ ] Excel (`.xlsx` met branded headers)
- [ ] Dashboard / web-UI
- [ ] MoreApp PDF (Advanced Mode) — als van toepassing
- [ ] MoreApp email body — als van toepassing
- [ ] Anders: ___

Per aangevinkt format komt later één file in `references/`. Begin niet met meer formaten dan de gebruiker daadwerkelijk produceert.

## 10. Lokalisatie

| Veld | Waarde |
|---|---|
| Hoofdtaal | bv. Nederlands |
| Datumformaat (lang) | bv. `maandag 11 mei 2026` |
| Datumformaat (kort) | bv. `11 mei 2026` |
| Getalformat — duizendtallen | bv. `1.230` |
| Getalformat — decimaal | bv. `2,8%` |
| Valuta — symbool en positie | bv. `€ 1.230,45` (spatie tussen symbool en bedrag) |
| Tweede taal (optioneel) | |

## 11. Hard rules

8–12 niet-onderhandelbare regels die in élke output gerespecteerd moeten worden. Voorbeelden:

1. Logo altijd via [URL], nooit anders.
2. Primair gebruikt voor [headings/links/accent].
3. Accent uitsluitend voor [CTA-buttons in e-mail].
4. Container-breedte [N]px PDF, [M]px e-mail.
5. NL-datum/getalformat overal.
6. Footer altijd compleet, anders rij weglaten.
7. Geen emoji's.
8. Roboto-stack web, Arial-stack e-mail.
9. ...
10. ...

Schrijf deze regels merk-specifiek; ze worden letterlijk in sectie "Hard rules" van de SKILL.md opgenomen.

## 12. Sister-entity mapping

Heeft het merk zustermerken of een rebrand-functie nodig? Vul de mapping in.

| Bron-token (ander merk) | Doel-token (dit merk) |
|---|---|
| KeyPro green `#34AA9E` | bv. `#CBD300` |
| KeyPro purple `#BF80FF` | bv. `#1E2883` |
| KeyPro logo URL | bv. H&P logo URL |
| KeyPro dark text `#111111` | bv. `#3C3436` |

Wanneer rebrand niet van toepassing is, laat deze sectie leeg en noteer dat in de SKILL.md sectie 11.

## 13. Triggerwoorden voor description

Verzamel élke variant waarop de skill moet activeren. Hoe meer signalen, hoe beter de triggering.

- Merknaam (volledig): 
- Merknaam (afkorting): 
- Domein: 
- Vestigingsnaam/adres: 
- Synoniemen ("ons rapport", "onze mail", "huisstijl", "in onze branding"): 
- Zustermerken die kunnen leiden tot rebrand: 
- Format-specifieke triggers (bv. "MoreApp template", "klantmail", "offerte"): 

## 14. Test-prompts voor sanity check

Schrijf 3 realistische zinnen waarop de skill moet activeren. Gebruik deze in stap 5 (sanity check) en optioneel in een eval-set:

1. 
2. 
3. 

---

## Klaar?

Als alle bovenstaande velden zijn ingevuld (of als `[TE-VERIFIEREN]` gemarkeerd) is de intake compleet. Ga door naar stap 2 (tokens-template invullen) en stap 4 (SKILL.md schrijven).

Bewaar dit ingevulde bestand in de werkdirectory naast de skill — het is je single source of truth en bewijslast voor latere refactors.
