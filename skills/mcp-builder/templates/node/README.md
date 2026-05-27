# {service}-mcp-server

MCP server for the {Service} API. Built with the [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk).

## Tools

| Name | Purpose |
|------|---------|
| `{service}_search_things` | Search {Service} for matching things |
| _(add the rest here)_ | |

## Setup

```bash
npm install
cp .env.example .env
# edit .env and set {SERVICE}_API_KEY
npm run build
```

## Test with MCP Inspector

```bash
npm run inspect
```

Open the printed URL, confirm the tool list loads, and call each tool with a realistic input.

## Install in Claude Code

```bash
claude mcp add {service} \
  --scope user \
  -e {SERVICE}_API_KEY="$( grep '^{SERVICE}_API_KEY' .env | cut -d= -f2- )" \
  -- node "$(pwd)/dist/index.js"
```

Verify:
```bash
claude mcp list
claude mcp get {service}
```

Restart any running Claude Code session for the new tools to appear.

## Install in Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "{service}": {
      "command": "node",
      "args": ["/absolute/path/to/dist/index.js"],
      "env": {
        "{SERVICE}_API_KEY": "your_key_here"
      }
    }
  }
}
```

Fully quit Claude Desktop (Cmd-Q) and reopen.

## Development

- `npm run dev` — watch mode with tsx
- `npm run build` — compile to `dist/`
- `npm run inspect` — build + open MCP Inspector
- Stdout is reserved for MCP protocol — use `console.error()`, not `console.log()`
- Don't run `node dist/index.js` directly (it hangs waiting on stdin) — use Inspector
