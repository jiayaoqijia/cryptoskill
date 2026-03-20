---
name: openclaw-x402-skill
description: "Discover, browse, filter, and pay for x402-compatible API endpoints and MCP tools from the x402 Bazaar — the autonomous discovery layer for agentic payments. Browse all available services, filter by price or type, inspect payment requirements, and call any discovered endpoint using USDC micropayments on Base with no API keys or account setup. Use when the agent needs to find a payable API service, check what x402 services exist for a given task (web scraping, AI inference, weather data, market data), pay for a single API call via x402, or list services under a given price threshold. Requires EVM_PRIVATE_KEY in .env (Base wallet with USDC) for paid calls. Discovery browsing requires no keys at all."
metadata:
  openclaw:
    emoji: "🛒"
    requires:
      bins: ["python3"]
      env:
        - EVM_PRIVATE_KEY
    install:
      - id: pip
        kind: shell
        command: "pip install -r ~/clawd/skills/openclaw-x402-skill/requirements.txt"
        label: "Install Python dependencies"
---

# x402 Bazaar Skill

The x402 Bazaar is the discovery layer for the x402 ecosystem — a
machine-readable catalog helping AI agents find and integrate with x402-compatible
API endpoints and MCP tools. Query, find, pay, and use with no pre-baked
integrations.

Two modes:
- **Browse only** — no wallet needed, zero cost, discover all available services
- **Browse + Pay** — requires Base wallet with USDC to call discovered endpoints

---

## Prerequisites

### Browse only (no keys needed)
```bash
python3 agent.py "list services"
python3 agent.py "find weather APIs"
```

### To call paid endpoints
1. Get a Base wallet private key (MetaMask → export, or Coinbase Wallet)
2. Fund with USDC on Base — get from coinbase.com or bridge.base.org
3. Add to `.env`:
```
EVM_PRIVATE_KEY="0xYourPrivateKeyHere"
MAX_SPEND_PER_CALL=0.10
```

### Install dependencies (run once)
```bash
pip install -r ~/clawd/skills/x402-bazaar/requirements.txt
```

---

## When to Activate This Skill

Activate when user says any of:

**Discovery**
- "What x402 services are available?"
- "Find me an API for [task] on x402"
- "Browse the x402 Bazaar"
- "What services cost less than $0.01?"
- "Find a weather API I can pay per call"
- "What MCP tools are on x402?"
- "Show me x402 services under [price]"
- "Search x402 for [keyword]"

**Paying for services**
- "Call this x402 endpoint: [url]"
- "Pay for and call [service name]"
- "Use x402 to get [data] — find and pay the cheapest service"
- "Make a paid x402 request to [url]"

Do NOT activate for:
- Checking agent's own wallet balance → use /agent-wallet skill
- Listing on the Bazaar as a seller → manual setup, see seller section below
- Alpaca or stock trading → use /alpaca-trading skill

---

## Exact Commands

### List all available services
```bash
cd ~/clawd/skills/x402-bazaar && python3 agent.py "list services"
```

### Search by keyword
```bash
python3 agent.py "find weather"
python3 agent.py "search for AI inference"
python3 agent.py "find web scraping services"
```

### Filter by max price
```bash
python3 agent.py "services under 0.01"
python3 agent.py "services under 0.001 USDC"
```

### Filter by type
```bash
python3 agent.py "list http services"
python3 agent.py "list mcp tools"
```

### Inspect a specific service
```bash
python3 agent.py "inspect https://api.example.com/x402/weather"
```

### Call a discovered service (requires EVM_PRIVATE_KEY + USDC)
```bash
python3 agent.py "call https://api.example.com/x402/weather?location=NYC"
python3 agent.py "pay and call https://api.example.com/x402/sentiment"
```

### Full autonomous flow: find + pay + use
```bash
python3 agent.py "find the cheapest weather API and get weather for London"
python3 agent.py "find a web scraping API and scrape https://example.com"
```

---

## How x402 Payment Works

1. Agent discovers a service from the Bazaar catalog
2. Calls the endpoint — gets HTTP 402 Payment Required response
3. Reads payment requirements from the 402 response headers
4. Pays via facilitator using USDC on Base
5. Retries the exact same request with payment proof header
6. Service verifies proof and returns paid result

No accounts, no subscriptions, no API keys — just USDC per request.

---

## MCP Integration

This skill can be integrated with **Model Context Protocol (MCP)** servers to enable
Claude Desktop and other MCP clients to autonomously pay for and use x402 APIs.

**See the full MCP integration guide:** [x402-MCP.md](x402-MCP.md)

Key capabilities:
- Expose x402 services as MCP tools in Claude Desktop
- Automatic payment handling when Claude calls an API
- Support for both EVM (Base) and Solana networks
- No manual payment steps — fully autonomous

Example: Claude can discover weather APIs via this skill, then call them via MCP
with automatic USDC micropayments on Base.

---

## Facilitators Queried

| Facilitator | Discovery URL | Notes |
|---|---|---|
| Coinbase CDP | `api.cdp.coinbase.com/platform/v2/x402/discovery/resources` | Largest catalog, default |
| PayAI | `facilitator.payai.network/discovery/resources` | Alternative catalog |

Both are queried and merged when you run "list services".

---

## Output Format

**Service list:**
```
🛒 x402 Bazaar — 42 services found

 1. 🌐 Weather API
    URL:      https://api.weather-x402.com/current
    Type:     http GET
    Price:    $0.001 USDC
    Network:  Base (eip155:8453)
    Updated:  2h ago

 2. 🤖 Llama 3.3 70B Inference
    URL:      https://api.x402network.com/llm/llama
    Type:     http POST
    Price:    $0.005 USDC
    Network:  Base (eip155:8453)
    Updated:  4h ago
```

**Paid call result:**
```
💸 x402 Payment Executed
   Endpoint:  https://api.weather-x402.com/current
   Paid:      $0.001 USDC
   Network:   Base (eip155:8453)
   TxHash:    0xabc123...
   Status:    200 OK

📦 Response:
   {"temperature": 72, "conditions": "sunny", "humidity": 45}
```

---

## Spending Limits

Default max spend per call is $0.10 USDC. Set in `.env`:
```
MAX_SPEND_PER_CALL=0.10
```

The skill refuses any call where maxAmountRequired exceeds this limit
and asks the user to confirm before proceeding.

---

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| `EVM_PRIVATE_KEY not set` | Missing .env key | Add key to .env (only needed for paid calls) |
| `Insufficient USDC balance` | Wallet underfunded | Bridge USDC to Base at bridge.base.org |
| `Spend limit exceeded` | Service costs more than MAX_SPEND_PER_CALL | Raise limit in .env or confirm manually |
| `402 verification failed` | Facilitator rejected payment | Retry or switch facilitator |
| `No services found` | Empty Bazaar result | Broaden search or try again later |
| `Network mismatch` | Service on unsupported chain | Filter by network eip155:8453 |

---

## Supported Networks (v1.0)

- Base mainnet: eip155:8453 (real USDC)
- Base Sepolia: eip155:84532 (test USDC — use for testing)

Solana support planned for v1.1.

---

## Listing Your Own API (Sellers)

To list your x402 API on the Bazaar (v2 spec-compliant):

1. Add `bazaarResourceServerExtension` to your x402 resource server
2. Use `declareDiscoveryExtension()` in your route configuration
3. Set `maxAmountRequired` in your accepts[] entries (replaces v1 `amount` field)
4. Listing is free — services set their own per-call price

The v2 discovery API returns:
```json
{
  "x402Version": 2,
  "items": [...],
  "pagination": {...}
}
```

**Note:** This skill handles both v1 (flat list) and v2 (wrapped response) for resilience.

**MCP tool uniqueness:** For MCP servers, uniqueness is determined by `(resource_url, tool_name)`,
not just the URL, since one MCP server can host multiple tools.

Full seller guide: [docs.cdp.coinbase.com/x402/bazaar](https://docs.cdp.coinbase.com/x402/bazaar)
