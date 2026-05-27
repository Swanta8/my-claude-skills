#!/usr/bin/env node
/**
 * MCP Server for {Service}.
 *
 * Replace {SERVICE} / {service} placeholders and fill in tools below.
 *
 * Includes:
 *  - shared API client with auth + timeout
 *  - consistent error handler
 *  - CHARACTER_LIMIT truncation
 *  - one example tool to copy from
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// ============================================================
// Configuration
// ============================================================

const SERVICE_NAME = "{service}"; // e.g. "stripe"
const API_BASE_URL = "https://api.{service}.com/v1";
const ENV_VAR_NAME = "{SERVICE}_API_KEY"; // e.g. "STRIPE_API_KEY"
const CHARACTER_LIMIT = 25_000;

const API_KEY = process.env[ENV_VAR_NAME];
if (!API_KEY) {
  console.error(`ERROR: ${ENV_VAR_NAME} environment variable is required.`);
  process.exit(1);
}

// ============================================================
// Shared utilities
// ============================================================

enum ResponseFormat {
  MARKDOWN = "markdown",
  JSON = "json",
}

class ApiError extends Error {
  constructor(public status: number, public body: string) {
    super(`API error ${status}: ${body}`);
  }
}

async function apiRequest<T>(
  method: string,
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const url = `${API_BASE_URL}${path}`;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 30_000);
  try {
    const r = await fetch(url, {
      ...init,
      method,
      signal: controller.signal,
      headers: {
        ...(init.headers ?? {}),
        Authorization: `Bearer ${API_KEY}`,
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });
    if (!r.ok) {
      throw new ApiError(r.status, await r.text());
    }
    return (await r.json()) as T;
  } finally {
    clearTimeout(timer);
  }
}

function handleApiError(e: unknown): string {
  if (e instanceof ApiError) {
    if (e.status === 401)
      return `Error: Authentication failed. Verify ${ENV_VAR_NAME} is a valid credential.`;
    if (e.status === 403)
      return "Error: Permission denied. Your credential lacks scope for this operation.";
    if (e.status === 404)
      return "Error: Resource not found. Verify the ID is correct.";
    if (e.status === 422) return `Error: Invalid input — ${e.body.slice(0, 300)}`;
    if (e.status === 429)
      return "Error: Rate limit exceeded. Reduce concurrency or narrow your query.";
    return `Error: API returned ${e.status}: ${e.body.slice(0, 200)}`;
  }
  if (e instanceof Error && e.name === "AbortError")
    return "Error: Request timed out after 30s. The API may be slow.";
  if (e instanceof Error) return `Error: ${e.name}: ${e.message}`;
  return `Error: ${String(e)}`;
}

function truncate<T>(payload: Record<string, unknown>, itemsKey: string): Record<string, unknown> {
  const rendered = JSON.stringify(payload, null, 2);
  if (rendered.length <= CHARACTER_LIMIT) return payload;
  const items = payload[itemsKey] as T[] | undefined;
  if (!items || items.length === 0) return payload;
  const keep = Math.max(1, Math.floor(items.length / 2));
  payload[itemsKey] = items.slice(0, keep);
  payload.truncated = true;
  payload.truncation_message =
    `Response truncated from ${items.length} to ${keep} items ` +
    `to stay under ${CHARACTER_LIMIT} characters. ` +
    "Use the `offset`/`cursor` parameter or add filters to retrieve more.";
  return payload;
}

// ============================================================
// Server
// ============================================================

const server = new McpServer({
  name: `${SERVICE_NAME}-mcp-server`,
  version: "0.1.0",
});

// ============================================================
// Tool: example_search_things
// Copy this block for each new tool. Delete this comment when done.
// ============================================================

const SearchThingsInputSchema = z
  .object({
    query: z
      .string()
      .min(1, "query cannot be empty")
      .max(200)
      .describe("Search string (e.g. 'invoice', 'customer@example.com')"),
    limit: z
      .number()
      .int()
      .min(1)
      .max(100)
      .default(20)
      .describe("Maximum results to return"),
    offset: z
      .number()
      .int()
      .min(0)
      .default(0)
      .describe("Number of results to skip for pagination"),
    response_format: z
      .nativeEnum(ResponseFormat)
      .default(ResponseFormat.MARKDOWN)
      .describe("'markdown' for human-readable, 'json' for machine-readable"),
  })
  .strict();

type SearchThingsInput = z.infer<typeof SearchThingsInputSchema>;

server.registerTool(
  `${SERVICE_NAME}_search_things`,
  {
    title: `Search ${SERVICE_NAME} things`,
    description: `Search ${SERVICE_NAME} for matching things.

Use this when the user asks to find, look up, or list things in ${SERVICE_NAME}.
Returns a paginated list — use \`offset\` to fetch subsequent pages.

Args:
  - query (string, 1-200 chars): Search string
  - limit (number, 1-100, default 20): Max results
  - offset (number, default 0): Skip this many results
  - response_format ('markdown' | 'json', default 'markdown')

Returns (JSON format):
  {
    "total": number,
    "count": number,
    "offset": number,
    "items": [{ "id": string, "name": string, ... }],
    "has_more": boolean,
    "next_offset": number | null
  }

Errors:
  - 401: returns "Authentication failed" — fix ${ENV_VAR_NAME}
  - 429: rate-limited — message includes guidance
  - Empty results return an empty list, not an error`,
    inputSchema: SearchThingsInputSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true,
    },
  },
  async (params: SearchThingsInput) => {
    try {
      const data = await apiRequest<{ items: Array<Record<string, unknown>>; total?: number }>(
        "GET",
        `/things?q=${encodeURIComponent(params.query)}&limit=${params.limit}&offset=${params.offset}`,
      );
      const items = data.items ?? [];
      const total = data.total ?? items.length;

      if (params.response_format === ResponseFormat.MARKDOWN) {
        if (items.length === 0) {
          return { content: [{ type: "text", text: `No things found matching '${params.query}'.` }] };
        }
        const lines = [`# Search results for '${params.query}'`, `Found ${total} (showing ${items.length})`, ""];
        for (const it of items) {
          lines.push(`## ${it.name ?? "Untitled"} (${it.id ?? "?"})`);
          if (it.description) lines.push(String(it.description));
          lines.push("");
        }
        return { content: [{ type: "text", text: lines.join("\n") }] };
      }

      const payload: Record<string, unknown> = {
        total,
        count: items.length,
        offset: params.offset,
        items,
        has_more: params.offset + items.length < total,
        next_offset: params.offset + items.length < total ? params.offset + items.length : null,
      };
      return { content: [{ type: "text", text: JSON.stringify(truncate(payload, "items"), null, 2) }] };
    } catch (e) {
      return { content: [{ type: "text", text: handleApiError(e) }] };
    }
  },
);

// ============================================================
// Entry point
// ============================================================

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error(`${SERVICE_NAME}-mcp-server running via stdio`);
}

main().catch((e) => {
  console.error("Server error:", e);
  process.exit(1);
});
