"""
GenTech Agent Kit — Algorand x402 Plugin
x402-priced data endpoints on Algorand for the Global x402 Challenge.
Payments route through GoPlausible facilitator for leaderboard tracking.

register_gentech_plugin(mcp) is auto-discovered by the Agent Kit plugin system.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import time
from typing import Any

import httpx

_LOG = logging.getLogger("gentech-kit.plugins.algorand")

# ── Config ──────────────────────────────────────────────────────────────────

ALGORAND_ADDRESS = os.environ.get("ALGORAND_ADDRESS", "LONDMBBAPYRSU6YBIHAK2I7N4OCZUDBFDLBAJ7OFPPQKQVQLJB7JFOTNU4")
ALGORAND_MNEMONIC = os.environ.get("ALGORAND_MNEMONIC", "")
GOPLAUSIBLE_BASE = "https://facilitator.goplausible.xyz"
CMC_API_KEY = os.environ.get("CMC_API_KEY", "")

_SESSION_SECRET = os.environ.get("X402_SESSION_SECRET", "")

# ── GoPlausible Client ──────────────────────────────────────────────────────

_client: httpx.Client | None = None


def _http() -> httpx.Client:
    global _client
    if _client is None:
        _client = httpx.Client(timeout=15.0)
    return _client


def _verify_payment(payment_proof: str) -> dict[str, Any]:
    """Verify an x402 payment through GoPlausible facilitator."""
    resp = _http().post(
        f"{GOPLAUSIBLE_BASE}/verify",
        json={"proof": payment_proof, "network": "algorand:localnet"},
    )
    resp.raise_for_status()
    return resp.json()


def _settle_payment(payment_proof: str) -> dict[str, Any]:
    """Settle a verified payment through GoPlausible."""
    resp = _http().post(
        f"{GOPLAUSIBLE_BASE}/settle",
        json={"proof": payment_proof, "network": "algorand:localnet"},
    )
    resp.raise_for_status()
    return resp.json()


def _session_token(agent_id: str) -> str:
    """Generate an HMAC session token valid for 60 minutes."""
    expiry = int(time.time()) + 3600
    msg = f"{agent_id}:{expiry}"
    secret = _SESSION_SECRET or "gentech-algorand-dev"
    token = hmac.new(secret.encode(), msg.encode(), hashlib.sha256).hexdigest()
    return f"{agent_id}:{expiry}:{token}"


def _verify_session(token: str) -> bool:
    """Verify a session token is valid and not expired."""
    try:
        parts = token.split(":")
        if len(parts) != 3:
            return False
        agent_id, expiry, sig = parts
        if int(time.time()) > int(expiry):
            return False
        expected = _session_token(agent_id)
        return hmac.compare_digest(token, expected)
    except (ValueError, IndexError):
        return False


# ── Session Store ────────────────────────────────────────────────────────────

_sessions: dict[str, float] = {}  # agent_id -> expiry timestamp


def _open_session(payment_proof: str) -> str | None:
    """Verify payment via GoPlausible and open a 60-min session."""
    try:
        result = _verify_payment(payment_proof)
        if result.get("status") != "verified":
            return None
        agent_id = f"agent_{int(time.time())}_{hashlib.md5(payment_proof.encode()).hexdigest()[:8]}"
        token = _session_token(agent_id)
        _sessions[agent_id] = time.time() + 3600
        return token
    except Exception as exc:
        _LOG.error("GoPlausible verification failed: %s", exc)
        return None


def _check_session(session_token: str) -> bool:
    """Check if a session token is valid."""
    if not _verify_session(session_token):
        return False
    agent_id = session_token.split(":")[0]
    expiry = _sessions.get(agent_id, 0)
    return time.time() < expiry


# ── CMC Data Helpers ────────────────────────────────────────────────────────

def _cmc_quote(symbol: str) -> dict[str, Any]:
    if not CMC_API_KEY:
        return {"error": "CMC_API_KEY not configured"}
    resp = _http().get(
        "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest",
        params={"symbol": symbol.upper()},
        headers={"X-CMC_PRO_API_KEY": CMC_API_KEY},
    )
    resp.raise_for_status()
    return resp.json()


# ── Plugin Registration ─────────────────────────────────────────────────────


def register_gentech_plugin(mcp: Any) -> None:
    """Register Algorand x402 tools with the Agent Kit MCP server.
    
    Auto-discovered by the plugin system in plugins.py.
    """
    server = mcp

    @server.tool()
    def algorand_x402_info() -> str:
        """Get Algorand x402 Gateway status — account, GoPlausible connection, and session info."""
        return json.dumps({
            "plugin": "Algorand x402 Gateway",
            "version": "0.1.0",
            "account": ALGORAND_ADDRESS,
            "facilitator": GOPLAUSIBLE_BASE,
            "network": "algorand:localnet",
            "challenge": "Algorand Global x402 Challenge",
            "active_sessions": len(_sessions),
            "status": "live" if _http().get(f"{GOPLAUSIBLE_BASE}/health").status_code == 200 else "degraded",
        }, indent=2)

    @server.tool()
    def algorand_verify_payment(payment_proof: str) -> str:
        """Verify an x402 payment on Algorand through GoPlausible facilitator. Returns session token on success."""
        token = _open_session(payment_proof)
        if token:
            return json.dumps({"status": "verified", "session_token": token, "expires_in": "3600s"})
        return json.dumps({"status": "failed", "error": "Payment verification rejected by GoPlausible"})

    @server.tool()
    def algorand_get_quote(symbol: str, session_token: str) -> str:
        """Get real-time crypto price quote on Algorand x402. Requires valid session from algorand_verify_payment. Cost: 0.001 ALGO/query."""
        if not _check_session(session_token):
            return json.dumps({"error": "Invalid or expired session. Call algorand_verify_payment first."})
        try:
            data = _cmc_quote(symbol)
            result: dict[str, Any] = {"symbol": symbol.upper(), "network": "algorand"}
            for sym, raw in data.get("data", {}).items():
                info = raw[0] if isinstance(raw, list) and raw else raw if isinstance(raw, dict) else {}
                q = info.get("quote", {}).get("USD", {})
                result[sym] = {
                    "price": q.get("price"),
                    "24h_change_pct": q.get("percent_change_24h"),
                    "market_cap": q.get("market_cap"),
                }
            return json.dumps(result, indent=2)
        except Exception as exc:
            return json.dumps({"error": str(exc)})

    _LOG.info("Registered Algorand x402 Gateway plugin: account=%s, facilitator=%s", ALGORAND_ADDRESS, GOPLAUSIBLE_BASE)


__plugin_manifest__ = {
    "name": "Algorand x402 Gateway",
    "version": "0.1.0",
    "description": "x402-priced data endpoints on Algorand via GoPlausible facilitator",
}