"""
GenTech Agent Kit — Robinhood Chain x402 Plugin

x402-priced data endpoints on Robinhood Chain via Naven Network facilitator.
Supports USDG settlement and tokenized stocks (AAPL, NVDA, TSLA, etc.).

register_gentech_plugin(mcp) is auto-discovered by the Agent Kit plugin system.

Features:
- Robinhood Chain network status
- Stock price quotes (tokenized stocks like AAPL, NVDA, TSLA)
- Available stock listings on RH Chain
- Crypto price quotes via CMC (same as main Kit, but USDG-priced)
- x402 payment verification via Naven Network
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

from . import schemas

_LOG = logging.getLogger("gentech-kit.plugins.robinhood")

# ── Robinhood Chain Config ──────────────────────────────────────────────────

ROBINHOOD_CHAIN_ID = 4663
ROBINHOOD_CHAIN_NAME = "Robinhood Chain"
ROBINHOOD_RPC = "https://rpc.mainnet.chain.robinhood.com"
ROBINHOOD_EXPLORER = "https://robinhoodchain.blockscout.com"

# Naven Network facilitator
NAVEN_FACILITATOR = "https://facilitator.naven.network"
NAVEN_API = "https://api.naven.network"

# USDG — Paxos-issued regulated stablecoin on Robinhood Chain
USDG_ADDRESS = "0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168"
USDG_DECIMALS = 6

# Receiver address for x402 payments (GenTech's RH Chain wallet)
# TODO: Replace with GenTech's actual wallet when deployed
RECEIVER_ADDRESS = os.environ.get("RH_CHAIN_RECEIVER", "")

# CMC integration (reuses existing config from server.py)
CMC_API_KEY = os.environ.get("CMC_API_KEY", "")
CMC_BASE = "https://pro-api.coinmarketcap.com"

# Session secret for x402 session tokens
_SESSION_SECRET = os.environ.get("X402_SESSION_SECRET", "gentech-robinhood-dev")

# ── Tokenized Stocks on Robinhood Chain ──────────────────────────────────────
# Source: https://docs.robinhood.com/chain/contracts/

STOCK_TOKENS: dict[str, dict[str, str]] = {
    "AAPL":  {"name": "Apple Inc.",              "contract": "0xaF3D76f1834A1d425780943C99Ea8A608f8a93f9"},
    "AMD":   {"name": "Advanced Micro Devices",  "contract": "0x86923f96303D656E4aa86D9d42D1e57ad2023fdC"},
    "AMZN":  {"name": "Amazon.com Inc.",         "contract": "0x12f190a9F9d7D37a250758b26824B97CE941bF54"},
    "BABA":  {"name": "Alibaba Group",           "contract": "0xad25Ac6C84D497db898fa1E8387bf6Af3532a1c4"},
    "COIN":  {"name": "Coinbase Global Inc.",    "contract": "0x6330D8C3178a418788dF01a47479c0ce7CCF450b"},
    "GOOGL": {"name": "Alphabet Inc.",           "contract": "0x2e0847E8910a9732eB3fb1bb4b70a580ADAD4FE3"},
    "INTC":  {"name": "Intel Corporation",       "contract": "0xc72b96e0E48ecd4DC75E1e45396e26300BC39681"},
    "META":  {"name": "Meta Platforms Inc.",      "contract": "0xc0D6457C16Cc70d6790Dd43521C899C87ce02f35"},
    "MSFT":  {"name": "Microsoft Corporation",   "contract": "0xe93237C50D904957Cf27E7B1133b510C669c2e74"},
    "NVDA":  {"name": "NVIDIA Corporation",      "contract": "0xd0601CE157Db5bdC3162BbaC2a2C8aF5320D9EEC"},
    "ORCL":  {"name": "Oracle Corporation",      "contract": "0xb0992820E760d836549ba69BC7598b4af75dEE03"},
    "PLTR":  {"name": "Palantir Technologies",   "contract": "0x894E1EC2D74FFE5AEF8Dc8A9e84686acCB964F2A"},
    "TSLA":  {"name": "Tesla Inc.",              "contract": "0x322F0929c4625eD5bAd873c95208D54E1c003b2d"},
    # ETFs
    "QQQ":   {"name": "Invesco QQQ Trust",       "contract": "0xD5f3879160bc7c32ebb4dC785F8a4F505888de68"},
    "SPY":   {"name": "SPDR S&P 500 ETF Trust",  "contract": "0x117cc2133c37B721F49dE2A7a74833232B3B4C0C"},
    "SGOV":  {"name": "iShares 0-3 Month Treasury Bond ETF", "contract": "0x92FD66527192E3e61d4DDd13322Aa222DE86F9B5"},
}


# ── HTTP Client ──────────────────────────────────────────────────────────────

_client: httpx.Client | None = None


def _http() -> httpx.Client:
    global _client
    if _client is None:
        _client = httpx.Client(timeout=15.0)
    return _client


# ── Blockchain Helpers ───────────────────────────────────────────────────────


def _get_block_number() -> int | None:
    """Get the latest block number on Robinhood Chain via JSON-RPC."""
    try:
        resp = _http().post(
            ROBINHOOD_RPC,
            json={"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1},
            timeout=10.0,
        )
        resp.raise_for_status()
        data = resp.json()
        if "result" in data:
            return int(data["result"], 16)
    except Exception as exc:
        _LOG.debug("Robinhood RPC block number failed: %s", exc)
    return None


# ── Stock Price via CMC ──────────────────────────────────────────────────────


def _cmc_headers() -> dict[str, str]:
    return {"Accept": "application/json", "X-CMC_PRO_API_KEY": CMC_API_KEY}


def _get_stock_price(symbol: str) -> dict[str, Any]:
    """Get stock price from CMC or external API.
    
    For tokenized stocks, attempts CMC first (they list stock tokens),
    falls back to basic estimate from available data.
    """
    if not CMC_API_KEY:
        return {"error": "CMC_API_KEY not configured"}
    try:
        resp = _http().get(
            f"{CMC_BASE}/v2/cryptocurrency/quotes/latest",
            params={"symbol": symbol},
            headers=_cmc_headers(),
            timeout=10.0,
        )
        resp.raise_for_status()
        data = resp.json()
        result: dict[str, Any] = {}
        for s, raw in data.get("data", {}).items():
            info = raw[0] if isinstance(raw, list) else raw
            q = info.get("quote", {}).get("USD", {})
            result[s] = {
                "price": q.get("price"),
                "percent_change_24h": q.get("percent_change_24h"),
                "market_cap": q.get("market_cap"),
                "volume_24h": q.get("volume_24h"),
            }
        return result
    except Exception as exc:
        _LOG.debug("CMC stock quote failed: %s", exc)
        return {"error": str(exc)}


# ── x402 Session Management ─────────────────────────────────────────────────


def _session_token(agent_id: str) -> str:
    """Generate an HMAC session token valid for 60 minutes."""
    expiry = int(time.time()) + 3600
    msg = f"{agent_id}:{expiry}"
    secret = _SESSION_SECRET or "gentech-robinhood-dev"
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


# Session store (in-memory; verify/settle calls also go through Naven)
_sessions: dict[str, float] = {}


def _open_session(payment_proof: str) -> str | None:
    """Verify payment via Naven Network and open a 60-min session."""
    try:
        # Verify through Naven facilitator
        resp = _http().post(
            f"{NAVEN_FACILITATOR}/verify",
            json={
                "proof": payment_proof,
                "network": f"eip155:{ROBINHOOD_CHAIN_ID}",
                "token": USDG_ADDRESS,
            },
            timeout=15.0,
        )
        result = resp.json()
        if result.get("status") != "verified":
            _LOG.warning("Naven verification failed: %s", result)
            return None
        
        agent_id = f"rh_{int(time.time())}_{hashlib.md5(payment_proof.encode()).hexdigest()[:8]}"
        token = _session_token(agent_id)
        _sessions[agent_id] = time.time() + 3600
        return token
    except Exception as exc:
        _LOG.error("Naven verification error: %s", exc)
        return None


def _check_session(session_token: str) -> bool:
    """Check if a session token is valid."""
    if not _verify_session(session_token):
        return False
    agent_id = session_token.split(":")[0]
    expiry = _sessions.get(agent_id, 0)
    return time.time() < expiry


# ── Plugin Registration ──────────────────────────────────────────────────────


def register_gentech_plugin(mcp: Any) -> None:
    """Register Robinhood Chain x402 tools with the Agent Kit MCP server.
    
    Auto-discovered by the plugin system in plugins.py.
    """

    @mcp.tool()
    def rh_info() -> str:
        """Get Robinhood Chain network status — chain ID, RPC, facilitator, block number, available stocks."""
        block = _get_block_number()
        info = schemas.RobinhoodNetworkInfo(
            plugin="Robinhood Chain x402",
            version="0.1.0",
            chain_id=ROBINHOOD_CHAIN_ID,
            chain_name=ROBINHOOD_CHAIN_NAME,
            native_token="ETH",
            settlement_token="USDG",
            settlement_asset=USDG_ADDRESS,
            facilitator=NAVEN_FACILITATOR,
            status="live" if block else "degraded",
            block_number=block,
        )
        return info.model_dump_json(indent=2)

    @mcp.tool()
    def rh_list_stocks() -> str:
        """List all available tokenized stocks on Robinhood Chain with contracts and categories."""
        stocks = [
            schemas.StockListItem(
                symbol=sym,
                name=info["name"],
                contract=info["contract"],
                category="ETF" if sym in ("QQQ", "SPY", "SGOV") else "stock",
            )
            for sym, info in STOCK_TOKENS.items()
        ]
        resp = schemas.StockListResponse(count=len(stocks), stocks=stocks)
        return resp.model_dump_json(indent=2)

    @mcp.tool()
    def rh_get_stock(symbol: str) -> str:
        """Get price for a tokenized stock on Robinhood Chain. Supports AAPL, NVDA, TSLA, MSFT, META, etc. Cost: $0.005 USDG/query."""
        sym = symbol.strip().upper()
        if sym not in STOCK_TOKENS:
            return json.dumps({"error": f"Unknown stock '{symbol}'. Use rh_list_stocks() to see available symbols."})
        
        token_info = STOCK_TOKENS[sym]
        price_data = _get_stock_price(sym)
        
        result = {
            "symbol": sym,
            "name": token_info["name"],
            "contract": token_info["contract"],
            "network": ROBINHOOD_CHAIN_NAME,
            "explorer": f"{ROBINHOOD_EXPLORER}/address/{token_info['contract']}",
        }
        
        if sym in price_data and isinstance(price_data[sym], dict):
            result["price_usd"] = price_data[sym].get("price")
            result["change_24h_pct"] = price_data[sym].get("percent_change_24h")
            result["source"] = "CoinMarketCap"
        elif "error" in price_data:
            result["price_usd"] = None
            result["source"] = f"error: {price_data['error']}"
        
        return json.dumps(result, indent=2)

    @mcp.tool()
    def rh_crypto_quote(symbol: str, session_token: str = "") -> str:
        """Get crypto price quote settled on Robinhood Chain. Supports BTC, ETH, SOL, etc. Requires valid x402 session (USDG). Cost: $0.001 USDG/query.
        
        For non-x402 mode (free tier), leave session_token empty.
        """
        if session_token and not _check_session(session_token):
            return json.dumps({"error": "Invalid or expired session. Purchase a session via x402 payment first."})
        
        if not CMC_API_KEY:
            return json.dumps({"error": "CMC_API_KEY not configured for price data"})
        
        try:
            resp = _http().get(
                f"{CMC_BASE}/v2/cryptocurrency/quotes/latest",
                params={"symbol": symbol.strip().upper()},
                headers=_cmc_headers(),
                timeout=10.0,
            )
            resp.raise_for_status()
            data = resp.json()
            
            result: dict[str, Any] = {
                "symbol": symbol.strip().upper(),
                "network": f"robinhood_chain",
                "settlement": "USDG",
            }
            for s, raw in data.get("data", {}).items():
                info = raw[0] if isinstance(raw, list) else raw
                q = info.get("quote", {}).get("USD", {})
                result[s] = {
                    "price": q.get("price"),
                    "change_24h_pct": q.get("percent_change_24h"),
                    "market_cap": q.get("market_cap"),
                }
            return json.dumps(result, indent=2)
        except Exception as exc:
            return json.dumps({"error": str(exc)})

    @mcp.tool()
    def rh_verify_payment(payment_proof: str) -> str:
        """Verify an x402 payment on Robinhood Chain through Naven Network facilitator. 
        
        Payment settles in USDG. On success, returns a session token valid for 60 minutes.
        
        Args:
            payment_proof: The x402 payment proof from Naven Network.
        """
        token = _open_session(payment_proof)
        if token:
            payment = schemas.PaymentStatus(
                status="verified",
                session_token=token,
                expires_in="3600s",
                network=f"eip155:{ROBINHOOD_CHAIN_ID}",
            )
            return payment.model_dump_json(indent=2)
        
        error = schemas.PaymentError(
            error="Payment verification rejected by Naven Network facilitator",
            network=f"eip155:{ROBINHOOD_CHAIN_ID}",
        )
        return error.model_dump_json(indent=2)

    _LOG.info(
        "Registered Robinhood Chain x402 plugin v0.1.0: chain_id=%d, facilitator=%s, stocks=%d",
        ROBINHOOD_CHAIN_ID, NAVEN_FACILITATOR, len(STOCK_TOKENS),
    )


__plugin_manifest__ = {
    "name": "Robinhood Chain x402",
    "version": "0.1.0",
    "description": "x402-priced data on Robinhood Chain via Naven Network — tokenized stocks (AAPL, NVDA, TSLA) and USDG settlement",
}
