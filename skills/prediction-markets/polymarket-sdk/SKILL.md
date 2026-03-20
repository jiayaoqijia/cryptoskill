---
name: polymarket
description: "Interact with Polymarket US prediction markets. Use when the user wants to: browse/search prediction markets, check market prices and odds, view portfolio positions and balances, place or cancel trades, check order status, look up events or sports markets, or get market settlement info. Requires the polymarket-us Python package and optionally API keys for trading."
---

# Polymarket US

Trade and browse prediction markets via the Polymarket US API using the Python SDK.

## Setup

Ensure the SDK is installed:
```bash
pip install polymarket-us
```

API keys are needed only for trading/portfolio endpoints. Generate at https://polymarket.us/developer

Store credentials as environment variables:
- `POLYMARKET_KEY_ID` — API key UUID
- `POLYMARKET_SECRET_KEY` — Ed25519 private key (base64)

## Usage

Write and execute Python scripts using the `polymarket_us` SDK. For full API details, read [references/api_reference.md](references/api_reference.md).

### Public Data (no auth)

```python
from polymarket_us import PolymarketUS
client = PolymarketUS()

# Search markets
results = client.search.query({"query": "bitcoin", "limit": 5})

# Browse trending markets
markets = client.markets.list({"limit": 10, "orderBy": ["volumeNum"], "orderDirection": "desc"})

# Check price
bbo = client.markets.bbo("market-slug")

client.close()
```

### Trading (auth required)

```python
import os
from polymarket_us import PolymarketUS

client = PolymarketUS(
    key_id=os.environ["POLYMARKET_KEY_ID"],
    secret_key=os.environ["POLYMARKET_SECRET_KEY"],
)

# Check balance
balances = client.account.balances()

# View positions
positions = client.portfolio.positions()

# Preview then place order
preview = client.orders.preview({"request": {
    "marketSlug": "some-market",
    "intent": "ORDER_INTENT_BUY_LONG",
    "type": "ORDER_TYPE_LIMIT",
    "price": {"value": "0.55", "currency": "USD"},
    "quantity": 100,
}})

# Place order (ALWAYS confirm with user before executing)
order = client.orders.create({
    "marketSlug": "some-market",
    "intent": "ORDER_INTENT_BUY_LONG",
    "type": "ORDER_TYPE_LIMIT",
    "price": {"value": "0.55", "currency": "USD"},
    "quantity": 100,
    "tif": "TIME_IN_FORCE_GOOD_TILL_CANCEL",
})

client.close()
```

## Key Rules

1. **Always preview orders before placing** — show the user what they're about to trade
2. **Always confirm with the user before placing any order** — never auto-trade
3. **Price is always the YES side** — to buy NO at $0.40, set price to $0.60 (1.00 - 0.40)
4. **In market slugs**: first team = YES, second team = NO
5. **Valid price range**: 0.001 to 0.999
6. **Handle errors gracefully** — catch `AuthenticationError`, `BadRequestError`, `RateLimitError`, etc.

## Formatting Results

When presenting market data to the user:
- Show market title/question clearly
- Display YES/NO prices as percentages (e.g., 55¢ = 55% implied probability)
- For positions, show P&L and current value
- Keep it conversational — this is prediction markets, make it fun
