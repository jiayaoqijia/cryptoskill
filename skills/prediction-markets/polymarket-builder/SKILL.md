---
name: polymarket-builder
description: "Polymarket Builder Program integration — register as a builder to earn weekly USDC fee rebates on routed volume, use py-builder-signing-sdk with Gnosis Safe wallets, discover 5-minute epoch-based Up/Down crypto markets via slug pattern {coin}-updown-5m-{epoch}, fix the CTF conditional token 400 balance/allowance error with polling (update_balance_allowance is a GET not a tx), and implement production-grade scalper bots on Polygon."
license: Apache-2.0
metadata:
  author: error403agent
  version: "1.0"
  chain: polygon
  category: Trading
tags:
  - polymarket
  - prediction-markets
  - builder-program
  - clob
  - conditional-tokens
  - 5-minute-markets
  - scalper
  - polygon
  - gnosis-safe
---

# Polymarket Builder Program

Polymarket operates a **Builder Program** that pays weekly USDC rewards to developers who route trading volume through their registered builder credentials. If you're building bots, dashboards, or any integration that places orders on Polymarket, you should register as a builder — you earn fee rebates on every order your users place.

This skill covers the builder-specific integration patterns that are **not** documented in the standard `polymarket` skill: builder registration, `py-builder-signing-sdk` usage, Gnosis Safe wallet setup, 5-minute epoch market discovery, and the CTF conditional token balance polling fix that eliminates the `400 not enough balance/allowance` error in production scalper bots.

Maintained by **DeepBlue** ([deepbluebase.xyz](https://deepbluebase.xyz)) — an autonomous trading agent team running live on Polymarket.

---

## What You Probably Got Wrong

> These are production bugs discovered running live scalper bots. Every item below cost real USDC to learn.

- **"`update_balance_allowance` submits an on-chain transaction"** — It does NOT. `update_balance_allowance` is a `GET /balance-allowance/update` request that tells Polymarket's CLOB server to re-read your on-chain token balance into its cache. Calling it does not grant any approval. If you call it and immediately place a sell order, you will get `400 not enough balance/allowance` because the buy fill may not have settled on-chain yet. The fix: call `update_balance_allowance` then `get_balance_allowance` in a loop until `balance >= expected_shares`.

- **"I need to approve CTF tokens before every sell"** — The CTF Exchange allowance is set once and persists. What actually expires or lags is Polymarket's **server-side cache** of your on-chain balance. The correct fix is cache-busting via polling, not re-approving.

- **"Builder rewards require smart contract integration"** — Builder rewards work entirely through HTTP headers. Pass `builder_config` when initializing `ClobClient` and Polymarket automatically attributes your volume. No contract interaction needed.

- **"The builder SDK only works with EOA wallets"** — `py-builder-signing-sdk` supports Gnosis Safe wallets (`signature_type=2`). The Safe's EOA controller signs the builder auth headers; the Safe address is the funder. This unlocks gasless order signing for your bot.

- **"5-minute markets have unpredictable slugs"** — They follow a deterministic pattern: `{coin}-updown-5m-{epoch}` where `epoch = (unix_timestamp // 300) * 300`. You can pre-compute the slug for any 5-minute window without querying the API.

- **"The Gamma API works with default headers"** — The Gamma API (`gamma-api.polymarket.com`) returns `403 Forbidden` without a browser User-Agent header. Always set `User-Agent: Mozilla/5.0 (X11; Linux x86_64)` or equivalent.

- **"I can place BUY and SELL for the same market simultaneously"** — The CLOB rejects this. Cancel your opposite-side open order before placing a sell. Use `cancel_order(order_id)` then wait one tick before placing.

- **"Builder credentials use the same format as trader credentials"** — Builder API key, secret, and passphrase come from `py-builder-signing-sdk`, not from the standard `create_or_derive_api_creds()` flow. They are separate credential sets.

---

## Builder Program Overview

The Polymarket Builder Program pays weekly USDC rewards based on trading volume routed through your builder credentials. Revenue comes from a share of protocol fees — makers pay 0%, takers pay a fee that scales with price (highest near $0.50, lower near extremes).

**How to register:**
1. Go to [polymarket.com/builders](https://polymarket.com/builders)
2. Connect your wallet and submit your project details
3. You receive a Builder API Key, Secret, and Passphrase
4. Install `py-builder-signing-sdk` and pass `BuilderConfig` to `ClobClient`

**What you earn:**
- Weekly USDC distributions based on attributed taker volume
- Volume is attributed when orders are placed with your builder headers
- Rewards are paid to your registered wallet address on Polygon

---

## Installation

```bash
pip install py-clob-client py-builder-signing-sdk web3
```

Required versions (tested in production, March 2026):
```
py-clob-client>=0.18.0
py-builder-signing-sdk>=0.1.0
web3>=6.0.0
```

---

## Quick Start

### 1. Initialize with Builder Credentials

```python
import asyncio
import os
from py_clob_client.client import ClobClient
from py_builder_signing_sdk.config import BuilderConfig
from py_builder_signing_sdk.sdk_types import BuilderApiKeyCreds

CLOB_HOST = "https://clob.polymarket.com"
CHAIN_ID = 137  # Polygon

async def init_builder_client() -> ClobClient:
    # Builder config — earns weekly USDC rewards on routed volume
    builder_config = BuilderConfig(
        local_builder_creds=BuilderApiKeyCreds(
            key=os.environ["POLY_BUILDER_API_KEY"],
            secret=os.environ["POLY_BUILDER_SECRET"],
            passphrase=os.environ["POLY_BUILDER_PASSPHRASE"],
        )
    )

    # Use signature_type=2 for Gnosis Safe, 0 for plain EOA
    client = ClobClient(
        CLOB_HOST,
        key=os.environ["POLY_PRIVATE_KEY"],
        chain_id=CHAIN_ID,
        signature_type=2,                         # POLY_GNOSIS_SAFE
        funder=os.environ["POLY_SAFE_ADDRESS"],   # Safe address (not EOA)
        builder_config=builder_config,
    )

    # Derive trading credentials (L1 → L2)
    client.set_api_creds(client.create_or_derive_api_creds())
    return client
```

### 2. Discover a 5-Minute Market

```python
import time
import aiohttp

GAMMA_API = "https://gamma-api.polymarket.com"
GAMMA_HEADERS = {
    # Required — Gamma returns 403 without a browser User-Agent
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Accept": "application/json",
}

def get_current_epoch() -> int:
    """5-minute window start, aligned to 300-second boundaries."""
    return (int(time.time()) // 300) * 300

async def discover_5min_market(coin: str) -> dict | None:
    """
    Discover a 5-minute Up/Down market by epoch slug.

    Slug pattern: {coin}-updown-5m-{epoch}
    Example: btc-updown-5m-1774086300

    Returns token IDs, prices, and market metadata, or None if not yet listed.
    """
    epoch = get_current_epoch()
    slug = f"{coin}-updown-5m-{epoch}"

    async with aiohttp.ClientSession(headers=GAMMA_HEADERS) as session:
        async with session.get(
            f"{GAMMA_API}/events",
            params={"slug": slug},
            timeout=aiohttp.ClientTimeout(total=8),
        ) as resp:
            if resp.status != 200:
                return None
            events = await resp.json()

    if not events:
        return None

    event = events[0]
    mkt = (event.get("markets") or [{}])[0]

    outcomes = mkt.get("outcomes", "[]")
    tokens   = mkt.get("clobTokenIds", "[]")
    prices   = mkt.get("outcomePrices", "[]")

    # Fields may be JSON strings or already parsed lists
    if isinstance(outcomes, str): outcomes = json.loads(outcomes)
    if isinstance(tokens,   str): tokens   = json.loads(tokens)
    if isinstance(prices,   str): prices   = json.loads(prices)

    up_idx   = next((i for i, o in enumerate(outcomes) if o.lower() == "up"),   None)
    down_idx = next((i for i, o in enumerate(outcomes) if o.lower() == "down"), None)

    if up_idx is None or down_idx is None:
        return None

    return {
        "slug":            slug,
        "epoch":           epoch,
        "coin":            coin,
        "up_token_id":     tokens[up_idx],
        "down_token_id":   tokens[down_idx],
        "up_price":        float(prices[up_idx]),
        "down_price":      float(prices[down_idx]),
        "accepting_orders": mkt.get("acceptingOrders", False),
        "question":        mkt.get("question", ""),
    }
```

---

## Core Concepts

### Epoch Windows

Polymarket's 5-minute crypto markets resolve at the boundary of each 300-second window. The window start timestamp is embedded in the slug.

```
Window:   1774086000  →  1774086300  (5 minutes)
Slug:     btc-updown-5m-1774086300  ← uses the NEXT window's start as the epoch
                                       i.e., the window that closes at this timestamp
```

```python
def get_current_window() -> int:
    return (int(time.time()) // 300) * 300

def seconds_remaining_in_window() -> int:
    now = int(time.time())
    return ((now // 300) + 1) * 300 - now

def get_next_window() -> int:
    return ((int(time.time()) // 300) + 1) * 300
```

**Supported coins (as of March 2026):** BTC, ETH, SOL, XRP

### Conditional Token Balance — The 400 Error

When your BUY order fills, Polymarket mints conditional tokens (ERC-1155) to your wallet on Polygon. These tokens are what you SELL for the TP. The CLOB validates your token balance server-side before accepting a SELL order.

**The problem:** There is a propagation delay between your on-chain buy fill confirming and Polymarket's CLOB cache reflecting your new balance. During this window — typically 2–10 seconds — SELL orders fail with `400 not enough balance/allowance`.

**The wrong fix (seen in many bots):**
```python
# ❌ This does NOT submit an on-chain approval transaction
await client.update_balance_allowance(params)
await asyncio.sleep(2)  # Hoping the cache refreshes — unreliable
```

**The correct fix:** Poll `update_balance_allowance` + `get_balance_allowance` until the CLOB confirms your balance:

```python
import asyncio
from py_clob_client.clob_types import BalanceAllowanceParams, AssetType

async def wait_for_token_balance(
    client,
    token_id: str,
    expected_shares: float,
    sig_type: int = 0,      # 0=EOA, 2=Safe
    timeout: float = 30.0,
) -> bool:
    """
    Poll until Polymarket's CLOB confirms we hold `expected_shares` of token_id.

    update_balance_allowance is a GET that tells the CLOB to re-read our on-chain
    balance. get_balance_allowance reads back the cached value. We loop until the
    cache reflects what we expect, then place the sell.

    Returns True when balance confirmed, False on timeout.
    """
    loop = asyncio.get_event_loop()
    params = BalanceAllowanceParams(
        asset_type=AssetType.CONDITIONAL,
        token_id=token_id,
        signature_type=sig_type,
    )

    deadline = loop.time() + timeout
    attempt = 0
    while True:
        attempt += 1
        try:
            # Trigger server-side cache refresh
            await loop.run_in_executor(
                None, lambda: client.update_balance_allowance(params)
            )
            # Read the refreshed cache
            result = await loop.run_in_executor(
                None, lambda: client.get_balance_allowance(params)
            )
            balance  = float((result or {}).get("balance",  0))
            allowance = float((result or {}).get("allowance", 0))

            if balance >= expected_shares and allowance >= expected_shares:
                print(f"Balance confirmed after {attempt} polls: {balance:.2f} shares")
                return True

            print(f"Poll {attempt}: balance={balance:.2f} allowance={allowance:.2f} need={expected_shares:.2f}")
        except Exception as e:
            print(f"Poll {attempt} error: {e}")

        if loop.time() >= deadline:
            print(f"Balance not confirmed after {timeout}s — placing sell anyway")
            return False

        await asyncio.sleep(2)
```

**Usage in a fill handler:**
```python
async def on_buy_filled(client, token_id: str, shares: float):
    # Wait for CLOB to see our tokens before placing TP sell
    confirmed = await wait_for_token_balance(client, token_id, shares, timeout=25)
    if not confirmed:
        print("Warning: placing sell without balance confirmation")

    sell_order = await place_limit_sell(client, token_id, price=0.40, size=shares)
```

### Builder Attribution

Builder headers are attached to every order automatically when you pass `builder_config` to `ClobClient`. You do not need to set headers manually. Volume is attributed by order, not by session — each order placement independently earns builder rewards.

```python
# ✅ Builder rewards attributed automatically — no extra steps
result = client.post_order(order, post_only=False)
```

### Gnosis Safe Signing (signature_type=2)

Using a Safe wallet with Polymarket provides gasless order signing. The EOA key controls the Safe; the Safe address is the `funder` (holds USDC and conditional tokens).

```python
# EOA = your signing key
# Safe = the address that holds funds and receives tokens
client = ClobClient(
    host,
    key=EOA_PRIVATE_KEY,         # Signs orders
    chain_id=137,
    signature_type=2,            # POLY_GNOSIS_SAFE
    funder=SAFE_ADDRESS,         # Holds USDC.e and CTF tokens
    builder_config=builder_config,
)
```

**Important:** When checking token balances via `get_balance_allowance`, use `signature_type=2` to check the Safe's balance, not the EOA's.

---

## Common Patterns

### Full 5-Minute Scalper (Buy Low, Sell High)

```python
import asyncio
import time
import json
import aiohttp
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, BalanceAllowanceParams, AssetType
from py_clob_client.order_builder.constants import BUY, SELL
from py_builder_signing_sdk.config import BuilderConfig
from py_builder_signing_sdk.sdk_types import BuilderApiKeyCreds

CLOB_HOST = "https://clob.polymarket.com"
GAMMA_API  = "https://gamma-api.polymarket.com"
CHAIN_ID   = 137

GAMMA_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Accept": "application/json",
}

BUY_PRICE  = 0.30   # Only enter when market is pricing 30% probability
SELL_PRICE = 0.40   # Exit at 40% — pure spread capture, no directional bet
BET_USDC   = 5.00

def get_epoch() -> int:
    return (int(time.time()) // 300) * 300

def seconds_left() -> int:
    now = int(time.time())
    return ((now // 300) + 1) * 300 - now

async def discover_market(coin: str) -> dict | None:
    slug = f"{coin}-updown-5m-{get_epoch()}"
    async with aiohttp.ClientSession(headers=GAMMA_HEADERS) as s:
        async with s.get(f"{GAMMA_API}/events", params={"slug": slug}) as r:
            events = await r.json() if r.status == 200 else []
    if not events:
        return None
    mkt = events[0].get("markets", [{}])[0]
    outcomes = json.loads(mkt["outcomes"]) if isinstance(mkt.get("outcomes"), str) else mkt.get("outcomes", [])
    tokens   = json.loads(mkt["clobTokenIds"]) if isinstance(mkt.get("clobTokenIds"), str) else mkt.get("clobTokenIds", [])
    prices   = json.loads(mkt["outcomePrices"]) if isinstance(mkt.get("outcomePrices"), str) else mkt.get("outcomePrices", [])
    up_i   = next((i for i,o in enumerate(outcomes) if o.lower()=="up"),   None)
    down_i = next((i for i,o in enumerate(outcomes) if o.lower()=="down"), None)
    if up_i is None or down_i is None:
        return None
    return {
        "up_token":   tokens[up_i],
        "down_token": tokens[down_i],
        "up_price":   float(prices[up_i]),
        "down_price": float(prices[down_i]),
        "accepting":  mkt.get("acceptingOrders", False),
    }

async def wait_balance(client, token_id: str, need: float, sig_type: int) -> bool:
    loop = asyncio.get_event_loop()
    params = BalanceAllowanceParams(AssetType.CONDITIONAL, token_id, sig_type)
    deadline = loop.time() + 25
    while loop.time() < deadline:
        try:
            await loop.run_in_executor(None, lambda: client.update_balance_allowance(params))
            r = await loop.run_in_executor(None, lambda: client.get_balance_allowance(params))
            bal = float((r or {}).get("balance", 0))
            if bal >= need:
                return True
        except Exception:
            pass
        await asyncio.sleep(2)
    return False

async def place_order(client, token_id: str, side: str, price: float, size: float) -> str | None:
    loop = asyncio.get_event_loop()
    order = await loop.run_in_executor(None, lambda: client.create_order(
        OrderArgs(token_id=token_id, price=price, size=size,
                  side=BUY if side == "BUY" else SELL)
    ))
    result = await loop.run_in_executor(None, lambda: client.post_order(order, post_only=False))
    return (result or {}).get("orderID")

async def scalper_window(client, coin: str = "btc"):
    """Trade one 5-minute window: buy the dip at $0.30, sell at $0.40."""
    market = await discover_market(coin)
    if not market or not market["accepting"]:
        print(f"No market for {coin} window {get_epoch()}")
        return

    shares = int(BET_USDC / BUY_PRICE)

    # Pre-warm the balance cache for both tokens before buying
    # (avoids cold-start delay when sell order comes in)
    sig = 2  # Change to 0 for EOA
    loop = asyncio.get_event_loop()
    for token in [market["up_token"], market["down_token"]]:
        params = BalanceAllowanceParams(AssetType.CONDITIONAL, token, sig)
        await loop.run_in_executor(None, lambda: client.update_balance_allowance(params))

    # Place both sides at our entry price
    up_oid   = await place_order(client, market["up_token"],   "BUY", BUY_PRICE, shares)
    down_oid = await place_order(client, market["down_token"], "BUY", BUY_PRICE, shares)
    print(f"Buys placed: UP={up_oid[:12] if up_oid else 'FAIL'} DN={down_oid[:12] if down_oid else 'FAIL'}")

    # Poll for fill — one side fills, cancel the other
    filled_side = None
    filled_oid  = None
    while seconds_left() > 100:
        open_orders = {o["id"] for o in await loop.run_in_executor(None, client.get_orders)}
        if up_oid and up_oid not in open_orders:
            filled_side, filled_oid = "up", up_oid
            if down_oid:
                await loop.run_in_executor(None, lambda: client.cancel_order(down_oid))
            break
        if down_oid and down_oid not in open_orders:
            filled_side, filled_oid = "dn", down_oid
            if up_oid:
                await loop.run_in_executor(None, lambda: client.cancel_order(up_oid))
            break
        await asyncio.sleep(1)

    if not filled_side:
        # Cancel both — window closing
        for oid in [up_oid, down_oid]:
            if oid:
                await loop.run_in_executor(None, lambda: client.cancel_order(oid))
        print("No fill — both buys cancelled")
        return

    token = market["up_token"] if filled_side == "up" else market["down_token"]

    # CRITICAL: Wait for balance confirmation before placing sell
    confirmed = await wait_balance(client, token, shares, sig)
    if not confirmed:
        print("WARNING: sell placed without balance confirmation — may 400")

    sell_oid = await place_order(client, token, "SELL", SELL_PRICE, shares)
    print(f"TP sell placed: {sell_oid[:12] if sell_oid else 'FAILED'}")
    print(f"Expected profit: ${shares * (SELL_PRICE - BUY_PRICE):.2f}")
```

### Check Builder Rewards Earned

```python
import requests

# Polymarket Data API — no auth needed
DATA_API = "https://data-api.polymarket.com"

def get_builder_earnings(builder_address: str) -> dict:
    """
    Check total builder rewards earned (paid to your registered wallet).
    """
    resp = requests.get(
        f"{DATA_API}/earnings/builders",
        params={"builder": builder_address},
        timeout=10,
    )
    return resp.json() if resp.status_code == 200 else {}
```

---

## Contract Addresses (Polygon, Last verified March 2026)

| Contract | Address |
|----------|---------|
| USDC.e (collateral) | `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174` |
| CTF (ERC-1155 conditional tokens) | `0x4D97DCd97eC945f40cF65F87097ACe5EA0476045` |
| CTF Exchange (standard markets) | `0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E` |
| Neg Risk CTF Exchange | `0xC5d563A36AE78145C45a50134d48A1215220f80a` |
| Neg Risk Adapter | `0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296` |

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `400 not enough balance/allowance` | CLOB cache hasn't seen your buy fill yet | Use `wait_for_token_balance()` — poll until balance confirmed |
| `403` from Gamma API | Missing User-Agent header | Add `User-Agent: Mozilla/5.0 ...` to all Gamma requests |
| `401 Unauthorized` | L2 HMAC signature mismatch or expired | Re-derive credentials with `create_or_derive_api_creds()` |
| `INVALID_ORDER_MIN_TICK_SIZE` | Price doesn't match market tick size | Query tick size from market data; round to nearest tick |
| `Order already exists` | Duplicate order placement | Check open orders before placing; use idempotency key |
| `ethers v6` import error | SDK requires ethers v5 | `pip install "ethers==5.*"` — v6 is incompatible |
| `Session key agent mismatch` | Wrong `sessionKeyStrategy` in Paperclip | Use `"run"` not `"issue"` for multi-agent setups |

---

## Security Considerations

- **Never embed private keys in code.** Use `os.environ` or a secrets manager. The CLOB client only needs the key at init time.
- **Separate EOA and Safe keys.** Your EOA signs orders; your Safe holds funds. If the EOA key leaks, an attacker can place bad orders but cannot drain funds directly.
- **Builder credentials are separate from trading credentials.** Store `POLY_BUILDER_API_KEY`, `POLY_BUILDER_SECRET`, `POLY_BUILDER_PASSPHRASE` separately from `POLY_API_KEY`, `POLY_API_SECRET`, `POLY_API_PASSPHRASE`.
- **Rate limit your polling.** The `wait_for_token_balance` pattern polls every 2s. Don't poll faster — the CLOB rate-limits aggressively.
- **Validate `acceptingOrders` before buying.** Markets are created a few seconds before their window opens. If `acceptingOrders=false`, orders will be rejected.
- **Cancel before window close.** Unfilled orders at window resolution create positions that resolve at extreme prices. Cancel anything unfilled with >90s remaining.

---

## Related Skills

- `polymarket` — Core CLOB integration, authentication, standard order types
- `gnosis-safe` — Safe wallet architecture, signing flows
- `polygon` — MATIC/gas management, RPC configuration

---

## References

- [Polymarket CLOB API Docs](https://docs.polymarket.com)
- [Polymarket Builder Program](https://polymarket.com/builders)
- [py-clob-client GitHub](https://github.com/Polymarket/py-clob-client)
- [py-builder-signing-sdk](https://github.com/Polymarket/py-builder-signing-sdk)
- [CTF Conditional Token Framework](https://docs.gnosis.io/conditionaltokens/)
- [DeepBlue — Live implementation](https://deepbluebase.xyz)
