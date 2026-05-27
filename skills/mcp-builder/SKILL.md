---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers from an API and a short user interview. Walks through intake → research → plan → implement → verify → install. Default language is Python (FastMCP); TypeScript is fully supported. Use whenever the user wants to wrap an API or service as an MCP server.
license: Complete terms in LICENSE.txt
---

# MCP Server Builder

Build a production-quality MCP server from (a) API documentation and (b) a short interview with the user. The interview is non-optional — it prevents shipping a server that wraps the wrong endpoints, uses the wrong auth, or includes destructive tools the user did not want.

## Operating principles

1. **Ask first, build second.** Phase 0 is an interview using `AskUserQuestion`. Skipping it is the #1 reason MCP servers turn out wrong.
2. **Workflows, not endpoints.** Wrapping every endpoint produces a sprawling, low-signal server. Pick 5–15 tools that match what the user actually wants to do.
3. **Verification gates.** At three points (after intake, after plan, after build) stop and confirm with the user before continuing.
4. **Templates over freehand.** Start from the scaffolds in `templates/` and adapt. Don't reinvent the file structure each time.
5. **Default language is Python (FastMCP).** Switch to TypeScript only if the user asks, or if remote/HTTP deployment is a hard requirement.

---

## Phase 0 — Intake (REQUIRED)

Before reading any API docs or writing any code, run the intake interview.

**Load the script:** [📝 Intake questions](./reference/intake_questions.md)

The intake covers, at minimum:

1. **Service & docs** — which API; URL to docs
2. **Authentication** — API key / Bearer / OAuth 2.0 / Basic / session; where credentials live
3. **Scope** — which workflows matter (not "wrap everything")
4. **Read vs write** — include destructive operations? (default: read-only first)
5. **Language** — Python (default) or TypeScript
6. **Transport** — stdio (local, default) or HTTP/SSE (remote/multi-client)
7. **Project location & name** — where to write the server
8. **Evaluations** — generate a 10-question eval suite? (default: yes)
9. **Auto-install** — install in Claude Code / Claude Desktop after build?

→ **Gate 1:** Summarize the intake answers back to the user in 5–8 lines. Ask "akkoord?" before continuing.

---

## Phase 1 — Research

Once the intake is approved:

### 1.1 Study the MCP protocol (one-time per session)

Use `WebFetch` on `https://modelcontextprotocol.io/llms-full.txt` if anything about MCP itself is unclear. Skip if already familiar.

### 1.2 Study the SDK (one-time per language)

- **Python:** `WebFetch` `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- **TypeScript:** `WebFetch` `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`

### 1.3 Study the target API exhaustively

From the docs URL the user provided, gather:
- All endpoints relevant to the chosen workflows
- Authentication flow (load: [🔐 Common patterns](./reference/common_patterns.md) for the auth pattern that matches)
- Pagination scheme (offset/limit, cursor, Link-header)
- Rate limits and how they're signaled (429, headers)
- Error response shape and status codes
- Data models for the resources the user cares about

**Use sub-agents for breadth** when docs are large. Spawn `Explore` or `general-purpose` subagents to read sections in parallel and report back concise summaries. Keep the main context lean.

### 1.4 Design the tool list

Apply the principles from [📋 MCP best practices](./reference/mcp_best_practices.md):

- 5–15 tools is a healthy range. More than 20 is a smell.
- Each tool should map to a *task the user described*, not an endpoint name.
- Consolidate: a `schedule_event` that checks availability + creates beats `check_availability` + `create_event` as two separate tools when they're always used together.
- Name with service prefix: `slack_send_message`, not `send_message`.
- For each tool, draft (a) name, (b) one-sentence purpose, (c) inputs, (d) what it returns.

→ **Gate 2:** Present the tool list to the user in a compact table. Ask for additions, removals, renames, or destructive-tool confirmations. Wait for approval.

---

## Phase 2 — Implementation

### 2.1 Scaffold from template

- **Python:** copy `templates/python/` into the project directory the user chose. Rename `{service}` placeholders.
- **TypeScript:** copy `templates/node/` and run `npm install`.

The template gives you: server entry point, shared API helper, error handler, response-format enum, pagination helper, `CHARACTER_LIMIT` constant, `.env.example`, `README.md`, `requirements.txt` / `package.json`.

Load the language-specific guide for the API surface details:
- [🐍 Python implementation guide](./reference/python_mcp_server.md)
- [⚡ TypeScript implementation guide](./reference/node_mcp_server.md)

### 2.2 Build shared infrastructure first

Before any tool:
- API client (auth wiring, base URL, timeouts) — the template has the skeleton
- `handle_api_error()` — translate HTTP errors into actionable LLM-facing messages
- `format_response()` — JSON vs Markdown switch
- `paginate()` helper if the API uses cursors

### 2.3 Implement tools one at a time

For each tool from the approved list:
1. Define the Pydantic model (Python) or Zod schema (TypeScript) with constraints + descriptions + examples per field
2. Write the docstring/description — see [🐍 Python guide § Tool Docstrings](./reference/python_mcp_server.md) for the required structure
3. Implement the handler — use the shared helpers, do not inline auth or error handling
4. Add tool annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`)
5. Apply `CHARACTER_LIMIT` truncation if the response can be large

### 2.4 Common pitfalls to actively avoid

See [🩹 Troubleshooting](./reference/troubleshooting.md). The big ones:
- Never `print()` to stdout in a stdio server — it corrupts the protocol. Use `stderr` or a logger.
- Don't `python server.py` directly to test — it hangs forever waiting for stdin. Use MCP Inspector or the eval harness.
- Pydantic v2: `max_length` for lists, not `max_items` (deprecated).
- Don't log secrets. Don't embed API keys in code. Always `os.environ`.

### 2.5 Verify the build

- **Python:** `python -m py_compile server.py` (or `ruff check` if available)
- **TypeScript:** `npm run build` — must complete cleanly, must emit `dist/index.js`
- **Both:** start MCP Inspector and call each tool once with realistic input:
  ```bash
  npx @modelcontextprotocol/inspector <command> <args>
  ```
- Confirm: tools list correctly, each tool returns sensible output, error paths return helpful messages.

→ **Gate 3:** Tell the user the server builds and tools work in Inspector. Ask whether to proceed to evaluations and/or installation.

---

## Phase 3 — Evaluations (optional but recommended)

Load: [✅ Evaluation guide](./reference/evaluation.md).

Create 10 questions that are independent, read-only, stable, complex enough to require multiple tool calls, and verifiable by string comparison. Save as XML. Then run:

```bash
pip install -r scripts/requirements.txt
export ANTHROPIC_API_KEY=...
python scripts/evaluation.py -t stdio -c python -a server.py -o report.md evaluation.xml
```

Use the report's per-task feedback section to iterate on tool descriptions and response formats.

---

## Phase 4 — Install

Load: [🔌 Installation guide](./reference/installation.md).

If the user approved auto-install in intake:
- **Claude Code:** `claude mcp add <name> -- <command> [args]` with `-e KEY=value` for env vars
- **Claude Desktop:** edit `~/Library/Application Support/Claude/claude_desktop_config.json`

Always confirm the exact command before running it. Show the user the resulting config block so they can verify.

---

## File map

```
SKILL.md                                    ← you are here
reference/
  intake_questions.md                       ← Phase 0 script
  mcp_best_practices.md                     ← Phase 1.4 design principles
  python_mcp_server.md                      ← Phase 2 Python details
  node_mcp_server.md                        ← Phase 2 TypeScript details
  common_patterns.md                        ← auth, pagination, rate-limit recipes
  troubleshooting.md                        ← Phase 2.4 pitfalls + MCP Inspector
  installation.md                           ← Phase 4 install in Claude Code/Desktop
  evaluation.md                             ← Phase 3 eval creation guide
templates/
  python/                                   ← copy for Python scaffolds
    server_template.py
    requirements.txt
    .env.example
    README.md
  node/                                     ← copy for TypeScript scaffolds
    package.json
    tsconfig.json
    src/index.ts
    .env.example
    README.md
scripts/
  evaluation.py                             ← eval harness (Phase 3)
  connections.py                            ← stdio/sse/http MCP clients
  example_evaluation.xml                    ← sample eval file
  requirements.txt
```

## Quick reference

| Phase | Action | Gate? |
|-------|--------|-------|
| 0 | Intake interview with `AskUserQuestion` | ✓ summarize + confirm |
| 1 | Read docs, design tool list | ✓ approve tool list |
| 2 | Scaffold, build, test in Inspector | ✓ confirm before eval/install |
| 3 | Generate 10-question evals (optional) | — |
| 4 | Install in Claude Code/Desktop | confirm command first |
