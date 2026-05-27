# {service}_mcp

MCP server for the {Service} API. Built with [FastMCP](https://github.com/modelcontextprotocol/python-sdk).

## Tools

| Name | Purpose |
|------|---------|
| `{service}_search_things` | Search {Service} for matching things |
| _(add the rest here)_ | |

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and set {SERVICE}_API_KEY
```

## Test with MCP Inspector

```bash
npx @modelcontextprotocol/inspector python server.py
```

Open the printed URL, confirm the tool list loads, and call each tool with a realistic input.

## Install in Claude Code

```bash
claude mcp add {service} \
  --scope user \
  -e {SERVICE}_API_KEY="$( grep '^{SERVICE}_API_KEY' .env | cut -d= -f2- )" \
  -- python "$(pwd)/server.py"
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
      "command": "python",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "{SERVICE}_API_KEY": "your_key_here"
      }
    }
  }
}
```

Fully quit Claude Desktop (Cmd-Q) and reopen.

## Development

- All tools are async — never use blocking HTTP clients
- Stdout is reserved for MCP protocol — log to stderr only
- Run `python -m py_compile server.py` to syntax-check
- Use MCP Inspector for runtime checks; never run `python server.py` directly (it hangs waiting for stdin)
