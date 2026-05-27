# Phase 0 — Intake Script

Run this interview before doing any research or writing any code. Each block below is a complete `AskUserQuestion` call you can copy-paste and adapt. **Do not batch all questions into one call** — split by topic so the user sees one focused screen at a time, and you can branch based on earlier answers.

The user gave you their initial request (e.g. "build me a Stripe MCP") — your job here is to fill the gaps that the request did not specify.

---

## Order of operations

1. **Service & docs** — confirm what you're integrating
2. **Authentication** — how the server will authenticate
3. **Scope** — which workflows / endpoint groups to include
4. **Read vs write** — destructive operations confirmation
5. **Language** — Python (default) or TypeScript
6. **Transport** — stdio (default) or HTTP/SSE
7. **Project location** — where to write files
8. **Evaluations & install** — opt-in steps

After all questions: summarize the answers in 5–8 lines and ask "akkoord?" before proceeding to Phase 1.

**Skip questions you already know the answer to.** If the user wrote "build me a TypeScript Slack MCP at ~/code/slack-mcp", you already have service, language, location — only ask about the missing items.

---

## Block 1 — Service & docs

If the user named the service but not the docs URL, ask for it.

```
AskUserQuestion({
  questions: [{
    question: "Which API docs should I use as the authoritative reference?",
    header: "Docs URL",
    multiSelect: false,
    options: [
      { label: "Official docs (paste URL)", description: "You'll provide a URL to the official API reference. I will WebFetch it as my primary source." },
      { label: "OpenAPI / Swagger spec", description: "You have a machine-readable OpenAPI 3.x spec — preferred when available, easier to enumerate endpoints accurately." },
      { label: "Let me search for it", description: "I'll search the web for the official docs and confirm the URL with you before proceeding." }
    ]
  }]
})
```

---

## Block 2 — Authentication

This is the question most likely to cause rework if skipped. Ask it explicitly.

```
AskUserQuestion({
  questions: [{
    question: "How does this API authenticate?",
    header: "Auth method",
    multiSelect: false,
    options: [
      { label: "API key in header", description: "Static key sent as a header like `Authorization: Bearer ...` or `X-API-Key: ...`. Simplest case. Key lives in env var." },
      { label: "OAuth 2.0", description: "Three-legged flow (client_id, client_secret, redirect, refresh token). Significantly more code; only choose if user-scoped access is required." },
      { label: "Basic auth", description: "Username + password (base64-encoded). Common for older APIs. Both go in env vars." },
      { label: "Personal access token", description: "Long-lived user token (GitHub-style PAT). Treated like an API key in practice — header-based." }
    ]
  }]
})
```

**Follow-up if API key or token:**
```
AskUserQuestion({
  questions: [{
    question: "What environment variable name should hold the credential?",
    header: "Env var",
    multiSelect: false,
    options: [
      { label: "{SERVICE}_API_KEY", description: "Default naming. E.g. STRIPE_API_KEY, GITHUB_TOKEN. Recommended unless the service has a strong convention." },
      { label: "Use service-specific name", description: "If the official SDK uses a specific name (e.g. OPENAI_API_KEY, SLACK_BOT_TOKEN), match it." },
      { label: "I'll specify a custom name", description: "Pick your own. I'll use it consistently across code, .env.example, and the README." }
    ]
  }]
})
```

**Follow-up if OAuth 2.0:**
```
AskUserQuestion({
  questions: [{
    question: "OAuth is complex. How do you want to handle the token lifecycle?",
    header: "OAuth scope",
    multiSelect: false,
    options: [
      { label: "I already have a long-lived refresh token", description: "I'll write the server to read CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN from env and refresh access tokens on demand. No login flow needed at runtime." },
      { label: "Build the full OAuth flow", description: "Server includes a one-time `authenticate` CLI flow that opens a browser, captures the callback, and stores tokens. More work but enables fresh users." },
      { label: "Bring-your-own access token", description: "Simplest: assume the user pastes a valid access token into env. No refresh logic. Fine for short-lived testing." }
    ]
  }]
})
```

---

## Block 3 — Scope

Wrapping every endpoint is the most common failure mode. Force the user to pick workflows.

```
AskUserQuestion({
  questions: [{
    question: "What should this MCP server actually let an agent do? Pick the workflows that matter — I'll design 5–15 tools around these, not every endpoint.",
    header: "Workflows",
    multiSelect: true,
    options: [
      { label: "Read / search resources", description: "List, search, get-by-id. Read-only inspection of data in the service." },
      { label: "Create new resources", description: "Tools that POST — e.g. create issue, send message, schedule event." },
      { label: "Update existing resources", description: "PATCH/PUT — edit, rename, change status, add labels." },
      { label: "Delete / archive", description: "Destructive ops. I'll mark these with destructiveHint=true and double-check with you in Phase 1." }
    ]
  }]
})
```

Then a free-form follow-up:
```
AskUserQuestion({
  questions: [{
    question: "Any specific tasks you want this MCP to handle well? (Examples: 'find all bugs assigned to me from last sprint', 'post a summary to a Slack channel'.)",
    header: "Use cases",
    multiSelect: false,
    options: [
      { label: "Generic — I'll trust your judgment", description: "Use the workflow categories I picked above. Design the tool list and run it past me in Gate 2." },
      { label: "I'll describe specific tasks", description: "Tell me 2–4 concrete tasks so I can design tools that handle them end-to-end." }
    ]
  }]
})
```

---

## Block 4 — Destructive operations gate

Only ask if the user picked Create / Update / Delete in Block 3.

```
AskUserQuestion({
  questions: [{
    question: "Destructive tools (delete, archive, irreversible updates) are risky when an agent uses them. How do you want to handle them?",
    header: "Destructive ops",
    multiSelect: false,
    options: [
      { label: "Include them, mark destructiveHint=true", description: "Tools are available but annotated so the client UI can prompt for approval per call." },
      { label: "Skip destructive tools entirely (Recommended)", description: "Build read + create + non-destructive update only. You can add destructive ones later if needed." },
      { label: "Include with a dry-run flag", description: "Each destructive tool gets a `dry_run: bool = True` default. The agent has to explicitly opt out to mutate." }
    ]
  }]
})
```

---

## Block 5 — Language

Skip if the user already specified.

```
AskUserQuestion({
  questions: [{
    question: "Which language for the MCP server?",
    header: "Language",
    multiSelect: false,
    options: [
      { label: "Python (FastMCP) — Recommended", description: "Less boilerplate, fastest path from API docs to working server. Great for stdio (local) deployments." },
      { label: "TypeScript (MCP SDK)", description: "Better when the team is JS-native or the server will be deployed as a remote HTTP/SSE service." }
    ]
  }]
})
```

---

## Block 6 — Transport

```
AskUserQuestion({
  questions: [{
    question: "How will the MCP server be deployed?",
    header: "Transport",
    multiSelect: false,
    options: [
      { label: "Local — stdio (Recommended)", description: "Runs as a subprocess of Claude Code / Claude Desktop. Simplest, no network config. Default for personal use." },
      { label: "Remote — HTTP / Streamable HTTP", description: "Hosted somewhere, multiple clients can connect. Requires auth, hosting, CORS — more work." },
      { label: "Remote — SSE (Server-Sent Events)", description: "Like HTTP but with server-push streams. Pick only if you need real-time updates from server to client." }
    ]
  }]
})
```

---

## Block 7 — Project location & name

```
AskUserQuestion({
  questions: [{
    question: "Where should I create the server, and what should it be named?",
    header: "Project",
    multiSelect: false,
    options: [
      { label: "~/code/{service}-mcp (default)", description: "Standard location. Python name will be `{service}_mcp`, TypeScript name `{service}-mcp-server` per MCP naming conventions." },
      { label: "Current working directory", description: "Create the server in a subfolder of $PWD. Useful if you're inside a monorepo." },
      { label: "Custom path", description: "I'll ask for the exact absolute path." }
    ]
  }]
})
```

---

## Block 8 — Evaluations & install

Combine these into one question if you've gotten this far.

```
AskUserQuestion({
  questions: [
    {
      question: "Should I generate a 10-question evaluation suite after building?",
      header: "Evals",
      multiSelect: false,
      options: [
        { label: "Yes (Recommended)", description: "10 read-only questions + run the eval harness against the new server. Gives you a quality baseline and surfaces tool-description issues." },
        { label: "Skip evals", description: "Just build the server. Faster but no objective quality check." }
      ]
    },
    {
      question: "Should I install the server in Claude Code / Claude Desktop after it builds successfully?",
      header: "Install",
      multiSelect: false,
      options: [
        { label: "Yes — Claude Code (`claude mcp add`)", description: "I'll run the install command and show you the resulting config. You can use the new server immediately." },
        { label: "Yes — Claude Desktop config", description: "I'll edit claude_desktop_config.json. You'll need to restart Claude Desktop after." },
        { label: "No — just give me the command", description: "I'll print the exact install command in the final summary. You run it when ready." }
      ]
    }
  ]
})
```

---

## After the interview — Gate 1

Summarize back to the user. Example template:

```
Hier is mijn samenvatting van de intake:

- Service: Stripe (https://docs.stripe.com/api)
- Auth: API key in `STRIPE_API_KEY`
- Scope: read + create (no destructive)
- Workflows: payment lookup, customer search, refund creation
- Language: Python (FastMCP)
- Transport: stdio
- Project: ~/code/stripe-mcp
- Evals: ja, 10 vragen
- Install: ja, in Claude Code via `claude mcp add`

Akkoord? Dan ga ik de docs lezen en kom ik terug met een tool-lijst.
```

Wait for explicit confirmation before continuing to Phase 1.

---

## Notes on follow-up branching

- If user picks **OAuth full flow** in Block 2 follow-up → budget ~2x time; flag this in Gate 1
- If user picks **HTTP/SSE transport** in Block 6 → also ask about deployment target (Cloudflare Workers, Vercel, self-hosted) before scaffolding
- If user says **"current directory"** in Block 7 → run `pwd` to confirm and include the absolute path in the Gate 1 summary
- If the user resists picking workflows in Block 3 ("just wrap everything") → push back once: "Wrapping all N endpoints will produce a low-quality server. Can you name the top 3 tasks?" If they still insist, proceed but cap at 15 tools.
