# my-claude-skills

A collection of [Claude Code](https://docs.claude.com/en/docs/claude-code) skills you can install with one command.

## Available skills

| Skill | Purpose |
|-------|---------|
| [`mcp-builder`](./skills/mcp-builder) | Build production-quality MCP servers from API docs through a guided interview → research → implement → install workflow |

## Install

```bash
git clone https://github.com/Swanta8/my-claude-skills.git
cd my-claude-skills
./install.sh mcp-builder
```

This copies the skill to `~/.claude/skills/<name>/` where Claude Code picks it up automatically.

### Install all skills at once

```bash
./install.sh --all
```

### Uninstall

```bash
./install.sh --uninstall mcp-builder
```

### Update

```bash
git pull
./install.sh mcp-builder    # re-running copies the latest version
```

## Using a skill

Once installed, Claude Code auto-discovers it on the next session. To trigger it:

- **Implicit**: ask Claude something that matches the skill's `description` field — Claude invokes it automatically
- **Explicit**: tell Claude "use the mcp-builder skill" or invoke the `Skill` tool by name

The `mcp-builder` skill activates when you ask Claude to build an MCP server (e.g. *"build me a Stripe MCP server"*). It then runs a short intake interview before touching code.

## Contributing a skill

PRs welcome. A skill is a folder containing at minimum:

```
skills/<name>/
├── SKILL.md          # YAML frontmatter + instructions
└── (optional) reference/, scripts/, templates/
```

The `SKILL.md` frontmatter must include `name` and `description`:

```markdown
---
name: my-skill
description: One sentence describing when Claude should use this skill.
---

# My Skill

...instructions for Claude...
```

See [`skills/mcp-builder/SKILL.md`](./skills/mcp-builder/SKILL.md) as a reference example.

## License

Each skill ships with its own license file in its folder. The `mcp-builder` skill is Apache 2.0 (originally from Anthropic, modified). The repository scaffolding (this README, `install.sh`) is MIT — see [`LICENSE`](./LICENSE).
