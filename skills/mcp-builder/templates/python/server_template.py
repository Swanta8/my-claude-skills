#!/usr/bin/env python3
"""MCP Server for {SERVICE}.

Replace {SERVICE} placeholders with the real service name and fill in
the API base URL, env var name, and tools below.

This template includes:
- shared API client with auth + timeout
- consistent error handler
- pagination helper
- CHARACTER_LIMIT truncation
- one example tool to copy from
"""

from __future__ import annotations

import json
import os
import sys
from enum import Enum
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field, field_validator

# ============================================================
# Configuration
# ============================================================

SERVICE_NAME = "{service}"  # e.g. "stripe"
API_BASE_URL = "https://api.{service}.com/v1"
ENV_VAR_NAME = "{SERVICE}_API_KEY"  # e.g. "STRIPE_API_KEY"
CHARACTER_LIMIT = 25_000

API_KEY = os.environ.get(ENV_VAR_NAME)
if not API_KEY:
    print(f"ERROR: {ENV_VAR_NAME} environment variable is required.", file=sys.stderr)
    sys.exit(1)

mcp = FastMCP(f"{SERVICE_NAME}_mcp")


# ============================================================
# Shared utilities
# ============================================================


class ResponseFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"


def _client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=API_BASE_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=30.0,
    )


async def _request(method: str, path: str, **kwargs: Any) -> dict[str, Any]:
    """Make an authenticated request to the API. Raises on non-2xx."""
    async with _client() as c:
        r = await c.request(method, path, **kwargs)
        r.raise_for_status()
        return r.json() if r.content else {}


def _handle_api_error(e: Exception) -> str:
    """Translate exceptions into actionable LLM-facing messages."""
    if isinstance(e, httpx.HTTPStatusError):
        status = e.response.status_code
        if status == 401:
            return (
                f"Error: Authentication failed. Verify {ENV_VAR_NAME} is set "
                "to a valid credential."
            )
        if status == 403:
            return "Error: Permission denied. Your credential lacks scope for this operation."
        if status == 404:
            return "Error: Resource not found. Verify the ID is correct and exists."
        if status == 422:
            try:
                detail = e.response.json()
            except Exception:
                detail = e.response.text
            return f"Error: Invalid input — {detail}"
        if status == 429:
            retry_after = e.response.headers.get("retry-after", "unknown")
            return (
                f"Error: Rate limit exceeded. Retry after {retry_after} seconds. "
                "Reduce concurrency or narrow your query."
            )
        return f"Error: API request failed with status {status}: {e.response.text[:200]}"
    if isinstance(e, httpx.TimeoutException):
        return "Error: Request timed out after 30s. The API may be slow — try again, or narrow the query."
    if isinstance(e, httpx.RequestError):
        return f"Error: Network error: {type(e).__name__}: {e}"
    return f"Error: Unexpected error ({type(e).__name__}): {e}"


def _truncate(payload: dict[str, Any], items_key: str) -> dict[str, Any]:
    """If the serialized payload exceeds CHARACTER_LIMIT, halve the items and annotate."""
    rendered = json.dumps(payload, indent=2)
    if len(rendered) <= CHARACTER_LIMIT:
        return payload
    items = payload.get(items_key, [])
    if not items:
        return payload
    keep = max(1, len(items) // 2)
    payload[items_key] = items[:keep]
    payload["truncated"] = True
    payload["truncation_message"] = (
        f"Response truncated from {len(items)} to {keep} items "
        f"to stay under {CHARACTER_LIMIT} characters. "
        "Use the `offset`/`cursor` parameter or add filters to retrieve more."
    )
    return payload


# ============================================================
# Tool: example_search_things
# Copy this block for each new tool. Delete this comment when done.
# ============================================================


class SearchThingsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    query: str = Field(
        ...,
        description="Search string (e.g. 'invoice', 'customer@example.com', 'project:alpha')",
        min_length=1,
        max_length=200,
    )
    limit: int = Field(
        default=20,
        description="Maximum results to return",
        ge=1,
        le=100,
    )
    offset: int = Field(
        default=0,
        description="Number of results to skip for pagination",
        ge=0,
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="'markdown' for human-readable, 'json' for machine-readable",
    )

    @field_validator("query")
    @classmethod
    def _strip_query(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("query cannot be empty or whitespace")
        return v


@mcp.tool(
    name=f"{SERVICE_NAME}_search_things",
    annotations={
        "title": f"Search {SERVICE_NAME} things",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def search_things(params: SearchThingsInput) -> str:
    """Search {SERVICE} for matching things.

    Use this when the user asks to find, look up, or list things in {SERVICE}.
    Returns a paginated list — use `offset` to fetch subsequent pages.

    Args:
        params: validated input, see SearchThingsInput.

    Returns:
        JSON string (or markdown if response_format='markdown') with:
        - items: list of matching things, each with {id, name, ...}
        - total: total matches found
        - count: items in this response
        - offset: current offset
        - has_more: bool
        - next_offset: int | None

    Error handling:
        - 401: Returns "Authentication failed" — fix {ENV_VAR_NAME}
        - 404: No things found is NOT a 404 — returns empty list instead
        - 429: Rate limited — message includes Retry-After hint
    """
    try:
        data = await _request(
            "GET",
            "/things",
            params={"q": params.query, "limit": params.limit, "offset": params.offset},
        )
        items = data.get("items", [])
        total = data.get("total", len(items))

        if params.response_format == ResponseFormat.MARKDOWN:
            if not items:
                return f"No things found matching '{params.query}'."
            lines = [f"# Search results for '{params.query}'", f"Found {total} (showing {len(items)})", ""]
            for it in items:
                lines.append(f"## {it.get('name', 'Untitled')} ({it.get('id', '?')})")
                if it.get("description"):
                    lines.append(it["description"])
                lines.append("")
            return "\n".join(lines)

        payload = {
            "total": total,
            "count": len(items),
            "offset": params.offset,
            "items": items,
            "has_more": params.offset + len(items) < total,
            "next_offset": params.offset + len(items) if params.offset + len(items) < total else None,
        }
        payload = _truncate(payload, "items")
        return json.dumps(payload, indent=2)

    except Exception as e:
        return _handle_api_error(e)


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    mcp.run()
