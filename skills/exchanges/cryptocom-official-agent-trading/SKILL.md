---
name: cryptocom-official-agent-trading
description: "Agent skills for trading cryptocurrency via the Crypto.com APIs. Works with any SKILL.md-compatible agent platform (OpenClaw, Cursor, Claude Code, and others)."
---

# cryptocom-official-agent-trading

_Source: [github.com/crypto-com/crypto-agent-trading](https://github.com/crypto-com/crypto-agent-trading). The body below is the upstream README.md captured at the time of registration._

---

# crypto-agent-trading

Agent skills for trading cryptocurrency via the Crypto.com APIs. Works with any SKILL.md-compatible agent platform (OpenClaw, Cursor, Claude Code, and others).

This repository contains two independent skills:

| Skill | Directory | Description |
|-------|-----------|-------------|
| **Main App** | `crypto-com-app/` | Execute trading, check balances, token prices via Crypto.com App |
| **Exchange** | `crypto-com-exchange/` | Execute trading, check balances, token prices via Crypto.com Exchange |

Each skill has its own `SKILL.md` and references. Install one or both depending on your use case.

---

## Main App Skill

### Features

- **Trade**: Market buy, sell, swap, and exchange across 200+ tokens (BTC, ETH, CRO, and more)
- **Balances**: Query fiat and crypto portfolio holdings
- **Prices**: Discover coins and check market prices
- **History**: View recent transaction history
- **Trading Limits**: Check weekly trading budget usage
- **Kill Switch**: Emergency API key revocation
- **Cash Management**: Deposit and withdraw fiat currencies, view bank accounts, check payment networks, and email deposit instructions

### Quickstart

#### 1. Set environment variables

First, generate an API key following the [API Key Management](https://help.crypto.com/en/articles/13843786-api-key-management) guide. Then export the key and secret in your terminal:

```bash
export CDC_API_KEY="your-api-key"
export CDC_API_SECRET="your-api-secret"
```

#### 2. Install the skill

```bash
npx skills add crypto-com/crypto-agent-trading/crypto-com-app -g -y
```

Or manually copy the skill folder to your agent platform's skill directory:

| Platform | Install location | Activation |
|----------|-----------------|------------|
| **OpenClaw** | `~/.openclaw/skills/crypto-com-app/` | Say "Initialize the crypto-com-app skill" |
| **Cursor** | `~/.cursor/skills/crypto-com-app/` | Add as an agent skill in settings |
| **Claude Code** | `~/.claude/skills/crypto-com-app/` | Point Claude at the `SKILL.md` path |
| **Other agents** | Any local directory | Point your agent at `SKILL.md` |

The skill uses **relative script paths** (`./scripts/...` from the skill root), so it works from any install location without path modifications.

### Example Conversation

```
User: "Buy CRO with 100 USD"
Agent: (runs quote) "Confirm: buy 1,250 CRO for 100 USD? This quote expires in 15 seconds."
User: "Yes"
Agent: (runs confirm) "Done! Purchased 1,250 CRO for 100 USD."
```

```
User: "What's my balance?"
Agent: (runs balance check) "You hold 1,250 CRO ($105.00) and 400.00 USD."
```

```
User: "Swap 500 CRO to BTC"
Agent: (runs quote) "Confirm: swap 500 CRO for 0.00045 BTC? Expires in 15 seconds."
User: "No, make it 200 CRO instead"
Agent: (runs new quote) "Confirm: swap 200 CRO for 0.00018 BTC? Expires in 15 seconds."
User: "Confirm"
Agent: (runs confirm) "Done! Swapped 200 CRO for 0.00018 BTC."
```

### Skill Workflows

The skills work together in typical trading flows:

**Basic Trading**: Check balance (crypto-com-app) → Get quote (crypto-com-app) → Confirm trade (crypto-com-app)

**Portfolio Review**: View balances (crypto-com-app) → Check history (crypto-com-app) → Analyze limits (crypto-com-app)

### Main App File Structure

```
crypto-com-app/
├── _meta.json          # OpenClaw package metadata
├── SKILL.md            # Core skill: configs, commands, business logic
├── CHANGELOG.md        # Version history
├── references/
│   └── errors.md       # Detailed error scenarios + recovery
└── scripts/
    ├── lib/
    │   ├── api.ts      # HTTP client, HMAC signing
    │   └── output.ts   # Structured output + error codes
    ├── account.ts      # Balances, trading limit, kill switch
    ├── coins.ts        # Coin discovery
    ├── fiat.ts         # Cash deposits, withdrawals, bank accounts
    └── trade.ts        # Quotations, orders, history
```

### Prerequisites

- Node.js 18+ (for `npx tsx` and built-in `fetch`)
- A Crypto.com App account with API key and secret

### Main App Security

- **No withdrawal permissions** -- the API key can only trade; it cannot withdraw funds from your account
- **Weekly trading limit** -- a configurable cap on total trading volume acts as a financial guardrail against runaway spending
- **HMAC-SHA256 signing** -- all requests are signed to prevent tampering and replay attacks
- **Environment-only credentials** -- API keys are read from environment variables only and never stored in files
- **Kill switch** -- instantly revoke API access in emergencies to stop all further trading

---

## Exchange Spot Skill

### Features

- **Spot Orders**: Place, amend, and cancel LIMIT and MARKET orders
- **Advanced Orders**: STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT
- **Order Groups**: Manage OCO, OTO, and OTOCO order groups
- **Balances & Positions**: Query balances, positions, order history, and trade history
- **Withdrawals**: Withdraw funds and check deposit/withdrawal status
- **Market Data**: Tickers, order book, candlesticks, and trades

### Setup

1. Copy the `crypto-com-exchange/` skill folder into your agent platform's skill directory
2. Provide your Crypto.com Exchange API key and secret
3. The agent reads the `SKILL.md` and handles authentication, signing, and request formatting directly — no scripts or runtime dependencies required

#### Getting API Keys

1. Log in to [Crypto.com Exchange](https://crypto.com/exchange)
2. Go to **Settings → API Keys**
3. Create a new key with desired permissions (Spot Trading, Withdrawal, etc.)
4. Set IP whitelist for production use
5. Store the API key and secret securely

### Example Conversation

```
User: "Place a limit buy for 0.1 BTC at $93,000"
Agent: "Confirm: LIMIT BUY 0.1 BTC_USD @ $93,000?"
User: "CONFIRM"
Agent: "Done! Order placed — order ID 6530219599901000701."
```

```
User: "Set up an OCO on BTC — sell limit at $108,000, stop-loss at $80,000, 0.1 BTC each"
Agent: "Confirm: OCO on BTC_USD — SELL LIMIT @ $108,000 + SELL STOP_LOSS trigger @ $80,000, 0.1 BTC per leg?"
User: "CONFIRM"
Agent: "Done! OCO created — list ID 6498090546073120100."
```

```
User: "What are my balances?"
Agent: "You hold 1.25 BTC, 5,000 USDT, and 10,000 CRO on your Exchange account."
```

### Environments

| Environment | Base URL |
|-------------|----------|
| Production | `https://api.crypto.com/exchange/v1/` |
| UAT Sandbox | `https://uat-api.3ona.co/exchange/v1/` |

UAT Sandbox requires separate credentials (institutional access only).

### Coverage

- **52 endpoints** — public market data, private trading, advanced orders, wallet, account management
- **Production-tested** — every endpoint verified against live API with real orders
- **66 edge cases documented** — param types, pagination quirks, error codes, validation rules

### Rate Limits

| Endpoint | Limit |
|----------|-------|
| `create-order`, `cancel-order`, `cancel-all-orders` | 15 req / 100ms each |
| `get-order-detail` | 30 req / 100ms |
| `get-trades`, `get-order-history` | 1 req / second |
| Other private endpoints | 3 req / 100ms each |
| Public market data | 100 req / second (per IP) |

Max open orders: 200 per trading pair, 1,000 across all pairs (per account/subaccount).

### Key Things Your Agent Should Know

- Order params (`price`, `quantity`, `notional`, `ref_price`, `amount`) must be **strings**
- `limit` must be a **number** (not string)
- Instrument names are case-sensitive: `BTC_USD` not `btc_usd`
- Public endpoints = GET only, Private endpoints = POST only
- All private requests use JSON body with HMAC-SHA256 signature

See the Exchange `SKILL.md` for the full reference.

### Exchange File Structure

```
crypto-com-exchange/
├── SKILL.md                      # Full skill definition — 52 endpoints, parameters, edge cases, agent behavior
├── references/
│   └── authentication.md         # HMAC-SHA256 signing implementation (Python, JavaScript, Bash), error codes
└── LICENSE.md                    # MIT License
```

### Exchange Security

- **HMAC-SHA256 signing** -- all private requests are signed to prevent tampering and replay attacks
- **Production confirmation** -- the agent requires explicit user confirmation (typing "CONFIRM") before executing any production trade
- **Credential masking** -- API keys and secrets are never displayed in full; only partial characters are shown
- **IP whitelisting** -- API keys can be restricted to specific IP addresses for production use
- **Withdrawal whitelisting** -- withdrawal destination addresses must be pre-approved in your Exchange account settings

---

## FAQ & Resources

- [OpenClaw Integration with Agent Key](https://help.crypto.com/en/collections/18662855-openclaw-integration-with-agent-key)
- [OpenClaw Trading Overview](https://help.crypto.com/en/articles/13843765-openclaw-trading-overview)
- [Getting Started](https://help.crypto.com/en/articles/13843782-getting-started)
- [API Key Management](https://help.crypto.com/en/articles/13843786-api-key-management)
- [Trading with OpenClaw](https://help.crypto.com/en/articles/13843788-trading-with-openclaw)
- [Weekly Trading Limit](https://help.crypto.com/en/articles/13843797-weekly-trading-limit)
- [Safety and Security](https://help.crypto.com/en/articles/13843804-safety-and-security)
- [Notifications](https://help.crypto.com/en/articles/13843811-notifications)

## License

- **Main App Skill**: Apache License 2.0
- **Exchange Spot Skill**: MIT License
