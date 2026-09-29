"""pnllabs_mcp.py — MCP server for the PnL Labs trust & risk API.

Exposes four tools that call the hosted PnL Labs API (https://api.pnllabs.com):
  check_wallet_trust     — proof of real realized PnL for a Solana wallet
  check_wallet_forensics — funding origin & cluster links
  check_token_safety     — structural token risk
  check_trade_cost       — real expected slippage for your size

No dependencies (Python standard library only). No RPC keys, no local setup —
it just calls the hosted API. Paid calls use x402 (USDC on Solana); when payment
is required the tool returns the HTTP 402 payment requirements so an x402-capable
client can pay and retry.

Add to an MCP client:
  { "mcpServers": { "pnllabs": { "command": "python3",
      "args": ["/path/to/pnllabs_mcp.py"] } } }
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request

API_BASE = os.environ.get("PNLLABS_API_BASE", "https://api.pnllabs.com")
PROTOCOL_FALLBACK = "2025-06-18"
_ADDR_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")

TOOLS = [
    {
        "name": "check_wallet_trust",
        "description": (
            "Proof of real PnL for a Solana wallet: recomputes REALIZED SOL "
            "profit/loss on-chain (not peak scores, which are routinely wrong — "
            "~50% of tracked 'smart money' is genuinely losing). Returns verdict "
            "TRUSTED/NEUTRAL/UNTRUSTED/INSUFFICIENT/UNVERIFIABLE with confidence, "
            "reason codes and flags (e.g. known_sniper_bot). Conservative: says "
            "UNVERIFIABLE instead of guessing. Use before copy-trading a wallet."),
        "inputSchema": {"type": "object", "properties": {"address": {
            "type": "string", "description": "Solana wallet address (base58)"}},
            "required": ["address"]},
    },
    {
        "name": "check_wallet_forensics",
        "description": (
            "Trace a Solana wallet's funding ORIGIN and freshness. Returns "
            "CEX_FUNDED (real end-user), WALLET_FUNDED (possible cluster/Sybil "
            "link), UNKNOWN_ORIGIN, UNVERIFIABLE_ORIGIN, plus a fresh_wallet flag "
            "(elevated insider/bundle risk). Complements check_wallet_trust."),
        "inputSchema": {"type": "object", "properties": {"address": {
            "type": "string", "description": "Solana wallet address (base58)"}},
            "required": ["address"]},
    },
    {
        "name": "check_token_safety",
        "description": (
            "Structural risk check for a Solana token: real-holder concentration "
            "(bonding-curve/LP excluded), known sniper bots among early buyers, "
            "honeypot. Returns LOW_RISK/ELEVATED/HIGH_RISK/CRITICAL/UNKNOWN. "
            "Behavioral rugs are invisible to structural checks — for those, check "
            "the wallets involved."),
        "inputSchema": {"type": "object", "properties": {"mint": {
            "type": "string", "description": "Solana token mint address (base58)"}},
            "required": ["mint"]},
    },
    {
        "name": "check_trade_cost",
        "description": (
            "Execution cost oracle: expected slippage for YOUR size in the token's "
            "main pool, round-trip cost calibrated with measured real-world "
            "execution overhead, and a recommended max size. Verdicts "
            "ACCEPTABLE_COST/ELEVATED_COST/HIGH_COST/UNTRADEABLE/NO_POOL/UNKNOWN."),
        "inputSchema": {"type": "object", "properties": {
            "mint": {"type": "string", "description": "Solana token mint (base58)"},
            "size_sol": {"type": "number", "description": "trade size in SOL (default 0.5)"}},
            "required": ["mint"]},
    },
]

_ROUTE = {
    "check_wallet_trust": ("address", lambda a: f"/check/wallet/{a['address']}"),
    "check_wallet_forensics": ("address", lambda a: f"/check/funder/{a['address']}"),
    "check_token_safety": ("mint", lambda a: f"/check/token/{a['mint']}"),
    "check_trade_cost": ("mint", lambda a: f"/check/trade/{a['mint']}"
                         f"?size_sol={a.get('size_sol', 0.5)}"),
}


def _log(m: str) -> None:
    print(f"[pnllabs-mcp] {m}", file=sys.stderr, flush=True)


def _reply(msg_id, result=None, error=None) -> None:
    out = {"jsonrpc": "2.0", "id": msg_id}
    out["error" if error is not None else "result"] = error if error is not None else result
    sys.stdout.write(json.dumps(out) + "\n")
    sys.stdout.flush()


def _call_api(path: str) -> dict:
    req = urllib.request.Request(API_BASE + path,
                                 headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 402:                       # x402: payment required
            try:
                body = json.load(e)
            except Exception:
                body = {}
            return {"payment_required": True, "x402": body,
                    "note": "This call is paid via x402 (USDC on Solana). Pay the "
                            "requirements with an x402-capable client and retry."}
        return {"error": f"HTTP {e.code}", "detail": e.read().decode()[:300]}


def _tool_call(name: str, args: dict) -> dict:
    spec = _ROUTE.get(name)
    if not spec:
        raise ValueError(f"unknown tool: {name}")
    key, route = spec
    val = str(args.get(key, "")).strip()
    if not _ADDR_RE.match(val):
        raise ValueError(f"INVALID_ADDRESS: '{key}' must be a base58 Solana address")
    data = _call_api(route(args))
    return {"content": [{"type": "text", "text": json.dumps(data)}], "isError": False}


def main() -> None:
    _log(f"ready · api={API_BASE}")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except Exception:
            continue
        method, msg_id = msg.get("method"), msg.get("id")
        if method == "initialize":
            proto = (msg.get("params") or {}).get("protocolVersion") or PROTOCOL_FALLBACK
            _reply(msg_id, {"protocolVersion": proto, "capabilities": {"tools": {}},
                            "serverInfo": {"name": "pnllabs", "version": "1.0.0"}})
        elif method == "ping":
            _reply(msg_id, {})
        elif method == "tools/list":
            _reply(msg_id, {"tools": TOOLS})
        elif method == "tools/call":
            p = msg.get("params") or {}
            try:
                _reply(msg_id, _tool_call(p.get("name", ""), p.get("arguments") or {}))
            except Exception as e:
                _reply(msg_id, {"content": [{"type": "text",
                                "text": f"{type(e).__name__}: {e}"}], "isError": True})
        elif msg_id is None:
            continue
        else:
            _reply(msg_id, error={"code": -32601, "message": f"method not found: {method}"})


if __name__ == "__main__":
    main()
