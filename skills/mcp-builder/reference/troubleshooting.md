# Troubleshooting & MCP Inspector

The pitfalls that catch out almost every MCP server build, and how to debug them.

---

## MCP Inspector — the one tool you need

`@modelcontextprotocol/inspector` is the official debugger. It launches your server and gives you a web UI to call tools, see schemas, and inspect raw protocol messages.

```bash
# Python stdio server
npx @modelcontextprotocol/inspector python server.py

# Python stdio server with env vars
ENV_VAR=value npx @modelcontextprotocol/inspector python server.py

# TypeScript stdio server (built)
npx @modelcontextprotocol/inspector node dist/index.js

# Remote HTTP server
npx @modelcontextprotocol/inspector --transport http https://mcp.example.com
```

Open the printed URL in your browser. Use it to:
- Verify the tool list loads (catches schema validation errors)
- Call each tool with sample input (catches runtime errors)
- See raw JSON-RPC messages (catches protocol-level bugs)

**Run Inspector before claiming the server works.** A clean `npm run build` only proves the code compiles, not that the server actually responds correctly.

---

## Top 10 pitfalls

### 1. `print()` in a stdio server breaks the protocol

A stdio MCP server reads JSON-RPC from stdin and writes it to stdout. **Any extra bytes on stdout corrupt the stream.**

```python
# WRONG — corrupts protocol
print("Server starting")

# RIGHT — stderr is safe
import sys
print("Server starting", file=sys.stderr)

# Or use logging configured to stderr
import logging
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
```

TypeScript equivalent: `console.error()` is safe, `console.log()` is not.

### 2. Running `python server.py` directly hangs forever

A stdio server waits for input on stdin. Running it without a client just blocks.

**Fix:** test with Inspector or the eval harness. Never directly invoke the server expecting it to "start and stay up" in your terminal.

To check the file at least loads without import errors:
```bash
python -m py_compile server.py
```

### 3. Forgetting to `await` async calls

FastMCP and the TypeScript SDK both require async handlers for any I/O.

```python
# WRONG — returns a coroutine, not a string
@mcp.tool()
async def search(q: str) -> str:
    data = httpx.get(URL)  # blocks the event loop AND returns wrong type
    return data.json()

# RIGHT
@mcp.tool()
async def search(q: str) -> str:
    async with httpx.AsyncClient() as c:
        r = await c.get(URL)
    return r.text
```

### 4. Pydantic v2 deprecation traps

- `max_items` / `min_items` → use `max_length` / `min_length` on `Field`
- `regex=` → use `pattern=`
- `Config` class → use `model_config = ConfigDict(...)`
- `.dict()` → use `.model_dump()`
- `@validator` → use `@field_validator` with `@classmethod`

The Python guide in this skill is correct; double-check older snippets you find online.

### 5. Tools without service prefix collide

If your server has a `search` tool and the user also installs another MCP with a `search` tool, the client has to disambiguate. Always prefix:

```python
@mcp.tool(name="stripe_search_customers")  # not "search_customers"
```

### 6. Returning the full API response wastes context

A `GET /users/{id}` response might be 50 fields. The agent rarely needs all of them.

```python
# WRONG — dumps everything
return json.dumps(await _request("GET", f"/users/{uid}"))

# RIGHT — pick the useful fields
data = await _request("GET", f"/users/{uid}")
return json.dumps({
    "id": data["id"],
    "name": data["name"],
    "email": data["email"],
    "created_at": data["created_at"],
}, indent=2)
```

Especially for list endpoints, the difference between dumping everything and selecting fields can be 10x context savings.

### 7. No CHARACTER_LIMIT truncation on list tools

A `list_messages` tool with no limit can return 100 KB of text and blow the agent's context window. Always:
- Default `limit` to 20
- Cap `limit` at 100 (Pydantic `le=100`)
- Apply `CHARACTER_LIMIT` post-format truncation (see `common_patterns.md`)

### 8. Error messages that don't help the agent

```python
# WRONG — agent has no idea what to do next
return f"Error: {e}"

# RIGHT — actionable
if e.response.status_code == 422:
    return (
        "Error: Invalid input. "
        f"Server said: {e.response.json().get('message')}. "
        "Check the field constraints in the tool description."
    )
```

The agent reads errors as instructions. Tell it what to try.

### 9. Logging secrets

```python
# WRONG
logger.info(f"Request headers: {headers}")  # logs the Bearer token

# RIGHT
safe = {k: v for k, v in headers.items() if k.lower() != "authorization"}
logger.info(f"Request headers: {safe}")
```

Same for query strings — strip `?api_key=...` before logging URLs.

### 10. TypeScript: forgetting `npm run build`

The `dist/` directory must be regenerated after every source edit. The MCP server runs `dist/index.js`, not `src/index.ts`.

Add a `prestart` script so this can't be skipped:
```json
"scripts": {
  "build": "tsc",
  "prestart": "npm run build",
  "start": "node dist/index.js"
}
```

---

## Debugging workflow when a tool fails

1. **Reproduce in Inspector.** Get the exact failing call and input.
2. **Read the raw JSON-RPC response** in Inspector's messages tab. Is the error in the tool result, or in the protocol layer?
3. **Add a temporary `logger.debug(...)` line** in the tool handler (writing to stderr). Re-run Inspector.
4. **If the error is from the upstream API:** check the API's own logs/dashboard. Confirm the auth, params, and rate-limit state.
5. **If the error is in your code:** narrow it down by short-circuiting the handler to return a stub before the failing line.

Never debug by guessing. The protocol is JSON-RPC over stdio — every bug has a precise location.

---

## "It works in Inspector but not in Claude Code"

- **Env vars:** Inspector inherits your shell env. Claude Code's MCP install only sees what you put in `-e` flags (or the `env` block of `claude_desktop_config.json`).
- **Working directory:** the MCP server might rely on relative paths. Use absolute paths in `command` / `args`, and don't `open("./config.json")` — use absolute paths or env-var-driven config.
- **Python interpreter:** if you developed with a venv, the global `python` may lack your deps. Use the venv's absolute path: `/Users/you/code/foo-mcp/.venv/bin/python`.
- **Restart Claude Code** after the install — the tool list is fetched on connect.

---

## Security sanity check before shipping

- [ ] No API keys, tokens, or credentials hard-coded in source
- [ ] All secrets read from `os.environ` / `process.env` and crash early if missing
- [ ] No logging of headers, query strings, or response bodies that might contain secrets
- [ ] `.env` is in `.gitignore`; only `.env.example` is committed
- [ ] Input validation (Pydantic / Zod) on every tool — no `**kwargs` passthrough
- [ ] URLs passed in by the agent are validated (scheme allowlist) before being fetched, if applicable
- [ ] Destructive tools are annotated `destructiveHint: true`
