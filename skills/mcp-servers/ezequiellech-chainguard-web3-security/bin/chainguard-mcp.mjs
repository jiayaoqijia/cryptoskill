#!/usr/bin/env node
import readline from "node:readline";

const MCP_URL = process.env.CHAINGUARD_MCP_URL || "https://chainguard-studio-production.up.railway.app/mcp";
const API_KEY = process.env.CHAINGUARD_API_KEY || "";
const args = process.argv.slice(2);

if (args.includes("--version") || args.includes("-v")) {
  console.log("1.5.0");
  process.exit(0);
}
if (args.includes("--help") || args.includes("-h")) {
  console.log("ChainGuard MCP v1.5.0 — Zero-install stdio MCP bridge (npx -y github:EzequielLech/chainguard-mcp)");
  console.log("Set CHAINGUARD_API_KEY=cg_live_... for unlimited calls, or use 5 free calls/hr automatically.");
  process.exit(0);
}

const rl = readline.createInterface({ input: process.stdin, terminal: false });
rl.on("line", async (line) => {
  const raw = line.trim();
  if (!raw) return;
  let msg;
  try {
    msg = JSON.parse(raw);
  } catch {
    process.stdout.write(JSON.stringify({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "Parse error" } }) + "\n");
    return;
  }
  if (msg.id === undefined || msg.id === null) return;
  const headers = { "Content-Type": "application/json", "Accept": "application/json" };
  if (API_KEY) headers["X-API-Key"] = API_KEY;
  try {
    const res = await fetch(MCP_URL, { method: "POST", headers, body: JSON.stringify(msg) });
    const data = await res.json();
    process.stdout.write(JSON.stringify(data) + "\n");
  } catch (err) {
    process.stdout.write(JSON.stringify({ jsonrpc: "2.0", id: msg.id, error: { code: -32603, message: String(err.message || err) } }) + "\n");
  }
});
