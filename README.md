# my-claude-skills

Een verzameling **skills** voor [Claude Code](https://docs.claude.com/en/docs/claude-code) die je met één commando installeert.

## Wat is een skill?

Een skill is een setje instructies dat Claude leert hoe hij een specifieke taak moet aanpakken. Je installeert hem één keer, en daarna herkent Claude automatisch wanneer hij hem moet gebruiken. Zie het als een soort "extra superkracht" die je aan Claude toevoegt.

## Welke skills zitten erin?

| Skill | Wat doet het? |
|-------|---------------|
| [`mcp-builder`](./skills/mcp-builder) | Helpt je een MCP-server te bouwen vanuit API-documentatie. Claude stelt eerst een paar vragen, doet onderzoek, schrijft de code, en installeert het voor je. |

> **Wat is een MCP-server?** Een MCP-server is een brug tussen Claude en een andere dienst (zoals Stripe, GitHub, of een eigen API). Daarmee kan Claude bijvoorbeeld direct betalingen ophalen of issues aanmaken.

## Installeren

```bash
git clone https://github.com/Swanta8/my-claude-skills.git
cd my-claude-skills
./install.sh mcp-builder
```

Dit kopieert de skill naar `~/.claude/skills/<naam>/`. Claude Code pikt hem daarna automatisch op zodra je een nieuwe sessie start.

### Alles in één keer installeren

```bash
./install.sh --all
```

### Verwijderen

```bash
./install.sh --uninstall mcp-builder
```

### Bijwerken naar de nieuwste versie

```bash
git pull
./install.sh mcp-builder    # opnieuw uitvoeren zet de laatste versie erop
```

## Hoe gebruik je een skill?

Zodra een skill geïnstalleerd is, kun je hem op twee manieren activeren:

1. **Vanzelf** — vraag Claude iets wat bij de skill past, en hij gebruikt hem automatisch.
   *Voorbeeld:* "Bouw een MCP-server voor Stripe" → de `mcp-builder` skill start vanzelf.

2. **Expliciet** — zeg gewoon: "gebruik de mcp-builder skill".

Bij `mcp-builder` begint Claude eerst met een paar korte vragen voordat hij code gaat schrijven. Zo weet je zeker dat het resultaat klopt met wat jij wilt.

## Zelf een skill toevoegen

Pull requests zijn welkom! Een skill is gewoon een mapje met minimaal dit erin:

```
skills/<naam>/
├── SKILL.md          # instructies + YAML-header
└── (optioneel) reference/, scripts/, templates/
```

In de YAML-header bovenaan `SKILL.md` moeten in elk geval `name` en `description` staan:

```markdown
---
name: mijn-skill
description: Eén zin die beschrijft wanneer Claude deze skill moet gebruiken.
---

# Mijn Skill

...instructies voor Claude...
```

Kijk naar [`skills/mcp-builder/SKILL.md`](./skills/mcp-builder/SKILL.md) voor een goed voorbeeld.

## Licentie

Elke skill heeft zijn eigen licentiebestand in zijn eigen mapje. De `mcp-builder` skill valt onder Apache 2.0 (origineel van Anthropic, aangepast). De rest van de repo (deze README, `install.sh`) is MIT — zie [`LICENSE`](./LICENSE).
