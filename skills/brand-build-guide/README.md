# brand-build-guide

> Een **meta-skill** voor [Claude Code](https://docs.claude.com/en/docs/claude-code) die van aangeleverde huisstijl-materialen automatisch een complete, upload-klare **merk-skill** bouwt.

<p align="center">
  <a href="https://github.com/Swanta8/my-claude-skills/releases/latest/download/brand-build-guide.zip">
    <img src="https://img.shields.io/badge/⬇%20Download-brand--build--guide.zip-2ea44f?style=for-the-badge&logo=github&logoColor=white" alt="Download brand-build-guide.zip">
  </a>
  &nbsp;
  <a href="https://github.com/Swanta8/my-claude-skills/releases/latest">
    <img src="https://img.shields.io/github/v/release/Swanta8/my-claude-skills?style=for-the-badge&label=versie&color=blue" alt="Laatste versie">
  </a>
</p>

---

## Wat doet het?

Je geeft de skill je huisstijl-bronnen — brand books / huisstijlboeken (PDF), logo's, kleur- en font-specificaties, tone-of-voice documenten, voorbeeldteksten, voorbeeld-templates, of gewoon een website. De skill:

1. **Leest** die bronnen uit.
2. **Extraheert** design tokens (kleuren met rollen, typografie, logo, spacing, footer) én de tone of voice.
3. **Genereert** een nette, herbruikbare merk-skill (`SKILL.md` + references + `design-tokens.json` + HTML-rapport- en e-mail-scaffolds) die je direct als `.zip` / `.skill` kunt uploaden naar organizational skills.

Zo blijft je merk-output consistent over rapporten, e-mails en documenten.

## Wat zit erin?

```
brand-build-guide/
├── SKILL.md                              # de instructies + YAML-header
├── references/
│   ├── intake-and-extraction.md          # hoe bronnen inlezen & tokens extraheren
│   ├── output-blueprint.md               # de 12-delige blauwdruk van de output
│   ├── scaffolds.md                       # HTML-rapport- en e-mail-sjablonen
│   ├── packaging-and-upload.md           # inpakken als .zip/.skill + uploaden
│   └── quality-checklist.md              # eindcontrole vóór oplevering
├── scripts/
│   ├── extract_brand_assets.py           # haalt kleuren/fonts/logo uit bronnen
│   ├── validate_brand_skill.py           # valideert de gegenereerde skill
│   └── package_skill.py                  # pakt de skill netjes in
└── assets/
    ├── design-tokens.schema.json         # JSON-schema voor de tokens
    └── example-design-tokens.json        # voorbeeld design-tokens
```

## Installeren

**Optie A — via de installer (aanbevolen):**

```bash
git clone https://github.com/Swanta8/my-claude-skills.git
cd my-claude-skills
./install.sh brand-build-guide
```

Dit kopieert de skill naar `~/.claude/skills/brand-build-guide/`. Claude Code pikt hem automatisch op zodra je een nieuwe sessie start.

**Optie B — losse download:**

Klik op de **Download**-knop hierboven, pak `brand-build-guide.zip` uit, en plaats de map `brand-build-guide/` in `~/.claude/skills/`.

## Hoe gebruik je het?

Vraag Claude gewoon iets wat bij de skill past — hij start dan vanzelf:

- *"Maak een brand skill van dit huisstijlboek."*
- *"Bouw een huisstijl-skill uit deze documenten."*
- *"Turn our brand book into a skill."*

Of activeer hem expliciet: *"gebruik de brand-build-guide skill"*.

## Bijwerken

```bash
cd my-claude-skills
git pull
./install.sh brand-build-guide   # opnieuw uitvoeren zet de laatste versie erop
```
