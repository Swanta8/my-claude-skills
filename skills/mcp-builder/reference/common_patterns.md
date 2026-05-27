# Common API Integration Patterns

Recipes for the recurring shapes you'll meet when wrapping an API as an MCP server. Each section has a Python and TypeScript example using the same helpers as the scaffolds in `templates/`.

---

## Authentication

### A. API key in header (most common)

The key is in env, sent as a header on every request. ~80% of REST APIs.

**Python (httpx):**
```python
import os
import httpx

API_KEY = os.environ["SERVICE_API_KEY"]  # crash early if missing
API_BASE_URL = "https://api.service.com/v1"

def _client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=API_BASE_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=30.0,
    )

async def _request(method: str, path: str, **kwargs) -> dict:
    async with _client() as c:
        r = await c.request(method, path, **kwargs)
        r.raise_for_status()
        return r.json()
```

**TypeScript (fetch):**
```typescript
const API_KEY = process.env.SERVICE_API_KEY;
if (!API_KEY) {
  console.error("SERVICE_API_KEY env var is required");
  process.exit(1);
}
const API_BASE_URL = "https://api.service.com/v1";

async function apiRequest<T>(method: string, path: string, init: RequestInit = {}): Promise<T> {
  const r = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    method,
    headers: {
      ...init.headers,
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
  });
  if (!r.ok) throw new ApiError(r.status, await r.text());
  return r.json() as Promise<T>;
}
```

Common header variants — adapt the constant string:
- `Authorization: Bearer <token>` — OAuth-style, also common for PATs (GitHub, Linear)
- `X-API-Key: <key>` — older APIs (Stripe webhooks, some SaaS)
- `Api-Key: <key>` — Notion, some others
- `Authorization: Token <key>` — Django REST Framework convention

### B. Basic auth

```python
import base64
USER = os.environ["SERVICE_USER"]
PASS = os.environ["SERVICE_PASS"]
TOKEN = base64.b64encode(f"{USER}:{PASS}".encode()).decode()
# Header: Authorization: Basic {TOKEN}
```

`httpx` and `axios` both support `auth=(user, pass)` directly — prefer that over hand-encoding.

### C. OAuth 2.0 — refresh token grant

Use when the user already obtained a refresh token (e.g. via the service's developer console) and you just need to mint access tokens at runtime.

**Python:**
```python
import time
import httpx

CLIENT_ID = os.environ["SERVICE_CLIENT_ID"]
CLIENT_SECRET = os.environ["SERVICE_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["SERVICE_REFRESH_TOKEN"]
TOKEN_URL = "https://api.service.com/oauth/token"

_access_token: str | None = None
_expires_at: float = 0

async def _get_access_token() -> str:
    global _access_token, _expires_at
    if _access_token and time.time() < _expires_at - 30:
        return _access_token
    async with httpx.AsyncClient() as c:
        r = await c.post(TOKEN_URL, data={
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        })
        r.raise_for_status()
        body = r.json()
    _access_token = body["access_token"]
    _expires_at = time.time() + body.get("expires_in", 3600)
    return _access_token

async def _request(method: str, path: str, **kwargs) -> dict:
    token = await _get_access_token()
    kwargs.setdefault("headers", {})["Authorization"] = f"Bearer {token}"
    async with httpx.AsyncClient(base_url=API_BASE_URL) as c:
        r = await c.request(method, path, **kwargs)
        r.raise_for_status()
        return r.json()
```

### D. Full OAuth flow (interactive)

Only build this if the user explicitly asked. Pattern: a separate `authenticate` CLI subcommand that opens a browser, runs a tiny local HTTP server on `localhost:8765` to catch the redirect, exchanges the code for tokens, writes them to a config file or keychain. Out of scope for the MCP server itself — it just reads the resulting refresh token from env.

---

## Pagination

### A. Offset / limit

```python
class ListInput(BaseModel):
    limit: int = Field(default=20, ge=1, le=100, description="Max results per page")
    offset: int = Field(default=0, ge=0, description="Skip this many results")

async def list_things(p: ListInput) -> str:
    data = await _request("GET", "/things", params={"limit": p.limit, "offset": p.offset})
    total = data.get("total", 0)
    items = data["items"]
    return json.dumps({
        "total": total,
        "count": len(items),
        "offset": p.offset,
        "items": items,
        "has_more": p.offset + len(items) < total,
        "next_offset": p.offset + len(items) if p.offset + len(items) < total else None,
    }, indent=2)
```

### B. Cursor-based

Many modern APIs (Stripe, Linear, Notion) return a `next_cursor` you pass back.

```python
class ListInput(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)
    cursor: str | None = Field(default=None, description="Opaque cursor from a previous response's next_cursor")

async def list_things(p: ListInput) -> str:
    params = {"limit": p.limit}
    if p.cursor:
        params["cursor"] = p.cursor
    data = await _request("GET", "/things", params=params)
    return json.dumps({
        "items": data["items"],
        "has_more": data.get("has_more", False),
        "next_cursor": data.get("next_cursor"),
    }, indent=2)
```

### C. Link-header (GitHub style)

```python
import re

def _parse_link_header(header: str) -> dict[str, str]:
    """Parse RFC 5988 Link header into {rel: url}."""
    links = {}
    for part in header.split(","):
        m = re.match(r'\s*<([^>]+)>;\s*rel="([^"]+)"', part)
        if m:
            links[m.group(2)] = m.group(1)
    return links

async def list_things(p: ListInput) -> str:
    async with _client() as c:
        r = await c.get("/things", params={"per_page": p.limit, "page": p.page})
        r.raise_for_status()
        items = r.json()
        links = _parse_link_header(r.headers.get("link", ""))
    return json.dumps({
        "items": items,
        "next_page_url": links.get("next"),
        "last_page_url": links.get("last"),
    }, indent=2)
```

---

## Rate-limit handling

Don't silently retry forever. Translate to an actionable error message.

```python
import httpx

async def _request_with_retry(method: str, path: str, max_retries: int = 1, **kwargs):
    """One automatic retry on 429 if the API tells us when to retry."""
    async with _client() as c:
        for attempt in range(max_retries + 1):
            r = await c.request(method, path, **kwargs)
            if r.status_code == 429 and attempt < max_retries:
                retry_after = float(r.headers.get("retry-after", "1"))
                if retry_after <= 5:  # only auto-retry short waits
                    await asyncio.sleep(retry_after)
                    continue
                # otherwise fall through and let _handle_api_error format the message
            r.raise_for_status()
            return r.json()
```

In the error handler:
```python
def _handle_api_error(e: Exception) -> str:
    if isinstance(e, httpx.HTTPStatusError):
        if e.response.status_code == 429:
            retry_after = e.response.headers.get("retry-after", "unknown")
            return (
                f"Error: Rate limit exceeded. Retry after {retry_after} seconds. "
                f"Consider reducing concurrent requests or adding filters to retrieve fewer results per call."
            )
        # ... other status codes
```

---

## Response formatting (JSON vs Markdown)

Templates already include a `ResponseFormat` enum. Apply consistently:

```python
class ResponseFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"

def _format_user(user: dict, fmt: ResponseFormat) -> str:
    if fmt == ResponseFormat.MARKDOWN:
        return (
            f"## {user['name']} ({user['id']})\n"
            f"- Email: {user['email']}\n"
            f"- Joined: {format_ts(user['created_at'])}\n"
        )
    return json.dumps(user, indent=2)
```

**Markdown rules:**
- Convert ISO/epoch timestamps to "2024-01-15 10:30 UTC"
- `Name (ID)` not just `ID`
- One image URL, not all sizes
- Skip null/empty fields

**JSON rules:**
- Include all fields
- Stable key order
- Keep IDs even if names are shown

---

## CHARACTER_LIMIT truncation

```python
CHARACTER_LIMIT = 25_000

def _truncate_if_large(payload: dict, items_key: str) -> dict:
    rendered = json.dumps(payload, indent=2)
    if len(rendered) <= CHARACTER_LIMIT:
        return payload
    items = payload[items_key]
    payload[items_key] = items[: max(1, len(items) // 2)]
    payload["truncated"] = True
    payload["truncation_message"] = (
        f"Response truncated from {len(items)} to {len(payload[items_key])} items "
        f"to stay under {CHARACTER_LIMIT} characters. "
        f"Use the `offset` or `cursor` parameter, or add filters, to see more."
    )
    return payload
```

Apply on the list/search tools — these are where over-large responses come from.

---

## Idempotency keys (for create operations)

If the API supports them (Stripe, some others), accept an optional `idempotency_key` param so retries don't double-create.

```python
class CreatePaymentInput(BaseModel):
    amount: int
    currency: str
    idempotency_key: str | None = Field(
        default=None,
        description="Optional idempotency key. Pass the same value on retries to ensure the operation runs at most once.",
    )

async def create_payment(p: CreatePaymentInput) -> str:
    headers = {}
    if p.idempotency_key:
        headers["Idempotency-Key"] = p.idempotency_key
    data = await _request("POST", "/payments", json=p.model_dump(exclude={"idempotency_key"}), headers=headers)
    return json.dumps(data, indent=2)
```

---

## Webhooks / async operations

MCP tools are synchronous from the agent's point of view. If the API uses async jobs (long-running exports, batch operations):

1. The tool kicks off the job and returns the `job_id` immediately
2. A separate `get_job_status` tool polls
3. Document the pattern clearly so the agent knows to poll

Don't block in-tool for more than ~30s — the client may time out.

---

## When the API doesn't have docs

Last resort: read the OpenAPI/Swagger JSON if exposed (often at `/openapi.json` or `/swagger.json`), or use the service's official SDK as a reference (read its source on GitHub). Confirm with the user before guessing endpoints.
