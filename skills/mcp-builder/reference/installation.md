# Installation Guide

How to install a freshly-built MCP server into Claude Code or Claude Desktop. Run this in Phase 4 after the build verifies clean.

---

## Option A — Claude Code (`claude mcp add`)

The CLI command is the simplest path. From any directory:

```bash
claude mcp add <name> --scope user -- <command> [args...]
```

### Python stdio server example

For a Python server at `~/code/stripe-mcp/server.py`:

```bash
claude mcp add stripe \
  --scope user \
  -e STRIPE_API_KEY="$STRIPE_API_KEY" \
  -- python /Users/you/code/stripe-mcp/server.py
```

Key flags:
- `--scope user` — available in all projects. Use `--scope project` to scope to one repo, or `--scope local` to only the current session.
- `-e KEY=VALUE` — env var, can repeat. Use shell expansion to pull from the parent env.
- `--` separates `claude mcp add` flags from the server command and its own args.

### Node/TypeScript stdio server example

For a TS server built to `~/code/slack-mcp-server/dist/index.js`:

```bash
claude mcp add slack \
  --scope user \
  -e SLACK_BOT_TOKEN="$SLACK_BOT_TOKEN" \
  -- node /Users/you/code/slack-mcp-server/dist/index.js
```

If installed globally via `npm i -g`:
```bash
claude mcp add slack --scope user -e SLACK_BOT_TOKEN=... -- slack-mcp-server
```

### Remote HTTP / SSE server

```bash
claude mcp add my-remote \
  --scope user \
  --transport http \
  --url https://mcp.example.com/v1 \
  --header "Authorization: Bearer $MY_TOKEN"
```

### Verify

```bash
claude mcp list           # shows all installed MCPs
claude mcp get stripe     # detail view + status
```

Restart any running Claude Code session for the new server to be picked up.

### Remove

```bash
claude mcp remove stripe --scope user
```

---

## Option B — Claude Desktop (config file)

Claude Desktop reads from a JSON file. Path:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

Edit the `mcpServers` object. Create the file (and parent dir) if missing.

### Python example

```json
{
  "mcpServers": {
    "stripe": {
      "command": "python",
      "args": ["/Users/you/code/stripe-mcp/server.py"],
      "env": {
        "STRIPE_API_KEY": "sk_test_..."
      }
    }
  }
}
```

### TypeScript example

```json
{
  "mcpServers": {
    "slack": {
      "command": "node",
      "args": ["/Users/you/code/slack-mcp-server/dist/index.js"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-..."
      }
    }
  }
}
```

**Must use absolute paths.** Relative paths will silently fail to start.

**After editing**, fully quit Claude Desktop (Cmd-Q on macOS — closing the window is not enough) and reopen. The new server should appear in the MCP indicator (🔌 icon).

---

## Auto-install flow for the skill

If the user opted in to auto-install during the intake:

1. **Confirm the exact command before running.** Print it and ask "run dit nu? (y/n)".
2. **Don't bake secrets into the command.** Use `$VAR` shell expansion so the secret isn't in shell history in plaintext, or instruct the user to `export VAR=...` first.
3. **Run with `Bash`** if the user confirms.
4. **Verify:** run `claude mcp list` and confirm the new server appears.
5. **Tell the user** to restart any existing Claude Code session to pick it up.

### Example confirmation flow

```
Server bouwde clean. Klaar om te installeren in Claude Code als user-scope MCP:

  claude mcp add stripe --scope user \
    -e STRIPE_API_KEY="$STRIPE_API_KEY" \
    -- python /Users/you/code/stripe-mcp/server.py

Vóór je dit draait: zorg dat `$STRIPE_API_KEY` in je shell-env staat
(check met `echo $STRIPE_API_KEY`).

Akkoord om te installeren?
```

---

## Troubleshooting an install

**`claude mcp list` shows the server but tools don't appear in Claude Code:**
- Restart the Claude Code session (the tool list is fetched on connect).
- Run the server command manually with the right env vars — confirm it doesn't crash on startup.
- Use MCP Inspector (`npx @modelcontextprotocol/inspector <command> [args]`) to see startup errors.

**Claude Desktop doesn't see the new server:**
- Confirm the JSON file is valid (`python -m json.tool < claude_desktop_config.json`).
- Confirm the path in `command`/`args` is absolute.
- Quit Claude Desktop fully (not just close the window) and reopen.
- Check `~/Library/Logs/Claude/mcp*.log` (macOS) for startup errors.

**Server starts but every tool call fails with auth errors:**
- Env vars from your shell don't propagate to subprocesses launched by Claude Desktop. Put them in the `env` object of the JSON config, not just `~/.zshrc`.
- For `claude mcp add`, the `-e KEY=value` flag is the supported way.

**Permission prompts every call:**
- Use `/permissions` in Claude Code to allowlist the specific MCP tools you trust. Don't allowlist destructive tools.
