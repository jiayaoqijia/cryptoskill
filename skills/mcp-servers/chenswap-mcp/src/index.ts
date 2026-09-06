/**
 * chenswap-mcp — MCP wrapper for chenswap.chitacloud.dev
 *
 * Tools: get_quote (5-aggregator parallel fan-out + LLM reasoning) and
 * list_supported_chains. Free, no API key, read-only quotes.
 *
 * Author: Alex Chen (autonomous AI agent). License: MIT.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { createHash, randomBytes } from "node:crypto";
import { readFileSync, existsSync, writeFileSync, mkdirSync } from "node:fs";
import { homedir, hostname, platform, release } from "node:os";
import { join } from "node:path";

const VERSION = "0.1.0";
const CHENSWAP_BASE = process.env.CHENSWAP_BASE_URL ?? "https://chenswap.chitacloud.dev";
const TELEMETRY_ENDPOINT =
  process.env.CHENSWAP_MCP_TELEMETRY_URL ?? "https://alexchen.chitacloud.dev/api/telemetry";
const TELEMETRY_ON = (process.env.CHENSWAP_MCP_TELEMETRY ?? "on").toLowerCase() !== "off";

function getInstallId(): string {
  try {
    const cfgDir = join(homedir(), ".config", "chenswap-mcp");
    const cfgFile = join(cfgDir, "install-id");
    if (existsSync(cfgFile)) {
      const v = readFileSync(cfgFile, "utf8").trim();
      if (/^[a-f0-9]{32}$/.test(v)) return v;
    }
    mkdirSync(cfgDir, { recursive: true });
    const id = randomBytes(16).toString("hex");
    writeFileSync(cfgFile, id, { mode: 0o600 });
    return id;
  } catch {
    const h = createHash("sha256");
    h.update(platform() + release() + hostname());
    return h.digest("hex").slice(0, 32);
  }
}

const INSTALL_ID = getInstallId();

async function emitTelemetry(ev: {
  event_type: string;
  tool?: string;
  success: boolean;
  duration_ms?: number;
  error_class?: string;
  mcp_client?: string;
}) {
  if (!TELEMETRY_ON) return;
  try {
    await fetch(TELEMETRY_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        service: "chenswap-mcp",
        version: VERSION,
        install_id: INSTALL_ID,
        timestamp: new Date().toISOString(),
        node_version: process.version,
        platform: `${platform()} ${release()}`,
        ...ev,
      }),
      signal: AbortSignal.timeout(2000),
    });
  } catch {}
}

async function callApi<T = unknown>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(CHENSWAP_BASE + path, {
    method: body === undefined ? "GET" : "POST",
    headers: {
      "User-Agent": `chenswap-mcp/${VERSION}`,
      ...(body === undefined ? {} : { "Content-Type": "application/json" }),
    },
    body: body === undefined ? undefined : JSON.stringify(body),
    signal: AbortSignal.timeout(30000),
  });
  const text = await res.text();
  let parsed: unknown = text;
  try { parsed = JSON.parse(text); } catch {}
  if (!res.ok) {
    const err = new Error(`chenswap API ${path} failed: HTTP ${res.status}`) as Error & { status: number; response: unknown };
    err.status = res.status;
    err.response = parsed;
    throw err;
  }
  return parsed as T;
}

const tools = [
  {
    name: "get_quote",
    description:
      "Get a DEX swap quote from 5 aggregators in parallel (KyberSwap, ParaSwap, Odos, LI.FI, Bebop). Returns all quotes plus best-source, spread percentage, and natural-language reasoning explaining why one route beats the others for the specific pair, chain, and amount. Read-only. No wallet connection. No API key.",
    inputSchema: {
      type: "object",
      required: ["chain_id", "token_in", "token_out", "amount_in_raw", "decimals_in", "decimals_out"],
      properties: {
        chain_id: {
          type: "integer",
          description: "EVM chain ID. Supported: 1 (Ethereum), 8453 (Base), 137 (Polygon), 42161 (Arbitrum), 56 (BNB).",
        },
        token_in: {
          type: "string",
          description: "ERC-20 address of input token (0x-prefixed hex).",
        },
        token_out: {
          type: "string",
          description: "ERC-20 address of output token (0x-prefixed hex).",
        },
        amount_in_raw: {
          type: "string",
          description: "Amount IN as a raw string (not decimal-adjusted). E.g. 1000 USDC with 6 decimals = '1000000000'.",
        },
        decimals_in: { type: "integer", description: "Decimals of token_in." },
        decimals_out: { type: "integer", description: "Decimals of token_out." },
      },
    },
  },
  {
    name: "list_supported_chains",
    description:
      "Return a list of chains supported by ChenSwap with aggregator coverage per chain.",
    inputSchema: { type: "object", properties: {} },
  },
];

const SUPPORTED_CHAINS = [
  { chain_id: 1, name: "Ethereum", aggregators: ["KyberSwap", "ParaSwap", "Odos", "LI.FI", "Bebop"] },
  { chain_id: 8453, name: "Base", aggregators: ["KyberSwap", "ParaSwap", "Odos", "LI.FI", "Bebop"] },
  { chain_id: 137, name: "Polygon", aggregators: ["KyberSwap", "Odos", "LI.FI"] },
  { chain_id: 42161, name: "Arbitrum", aggregators: ["KyberSwap", "ParaSwap", "Odos", "LI.FI"] },
  { chain_id: 56, name: "BNB Chain", aggregators: ["KyberSwap", "Odos", "LI.FI"] },
];

async function dispatchTool(name: string, args: Record<string, unknown>): Promise<string> {
  switch (name) {
    case "get_quote": {
      const r = await callApi("/api/quote", args);
      return JSON.stringify(r, null, 2);
    }
    case "list_supported_chains":
      return JSON.stringify({ chains: SUPPORTED_CHAINS }, null, 2);
    default:
      throw new Error(`unknown tool: ${name}`);
  }
}

async function main() {
  const server = new Server(
    { name: "chenswap-mcp", version: VERSION },
    { capabilities: { tools: {} } }
  );

  let mcpClient = "unknown";

  server.setRequestHandler(ListToolsRequestSchema, async () => {
    void emitTelemetry({ event_type: "list_tools", success: true });
    return { tools };
  });

  server.setRequestHandler(CallToolRequestSchema, async (req) => {
    const toolName = req.params.name;
    const args = (req.params.arguments ?? {}) as Record<string, unknown>;
    const start = Date.now();
    try {
      const clientInfo = (server as unknown as { _clientInfo?: { name?: string; version?: string } })._clientInfo;
      if (clientInfo?.name) mcpClient = `${clientInfo.name}/${clientInfo.version ?? "?"}`;
    } catch {}

    try {
      const text = await dispatchTool(toolName, args);
      void emitTelemetry({
        event_type: "tool_call",
        tool: toolName,
        success: true,
        duration_ms: Date.now() - start,
        mcp_client: mcpClient,
      });
      return { content: [{ type: "text", text }] };
    } catch (err) {
      const e = err as Error & { status?: number };
      void emitTelemetry({
        event_type: "tool_call",
        tool: toolName,
        success: false,
        duration_ms: Date.now() - start,
        error_class: e?.status ? `http_${e.status}` : (e?.name ?? "Error"),
        mcp_client: mcpClient,
      });
      return {
        isError: true,
        content: [{ type: "text", text: `Error calling ${toolName}: ${e?.message ?? String(err)}` }],
      };
    }
  });

  const transport = new StdioServerTransport();
  await server.connect(transport);
  process.stderr.write(
    `chenswap-mcp v${VERSION} ready. Telemetry: ${TELEMETRY_ON ? "on" : "off"}. Install id: ${INSTALL_ID.slice(0, 8)}...\n`
  );
  void emitTelemetry({ event_type: "server_start", success: true });
}

main().catch((err) => {
  process.stderr.write(`[fatal] ${err?.stack ?? err}\n`);
  process.exit(1);
});