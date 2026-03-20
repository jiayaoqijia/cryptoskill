# x402 for AI Agents

## Agent Workflow

1. **Discover** — Call free discovery API to find endpoints
2. **Evaluate** — Search and check pricing before committing
3. **Pay** — Sign payment and get data in single request-response cycle
4. **Consume** — Parse standard GoldRush JSON responses

## x402 vs API Key for Agents

| Concern | API Key | x402 |
|---------|---------|------|
| Provisioning | Requires signup, key management | Wallet is the credential |
| Budget control | Monthly plan, overage charges | Pay exactly per request |
| Human involvement | Account creation, billing setup | None — fully autonomous |
| Discovery | Read docs or hardcode endpoints | Programmatic endpoint discovery |
| Multi-agent | Share key or provision per agent | Each agent gets its own wallet |

## Rate Limits

100 requests/minute per wallet. Check `X-RateLimit-Remaining` response header.

---

The x402 protocol was designed with machine-to-machine payments in mind. An AI agent with a funded wallet can autonomously access the full GoldRush API - no signup flow, no credentials to rotate, no billing portal, no human in the loop.

## Agent workflow

An AI agent interacting with GoldRush x402 follows four steps:

### 1. Discover

Call the free discovery API to find available endpoints:

```bash
curl https://x402.goldrush.dev/v1/x402/endpoints | jq
```

The response includes endpoint names, descriptions, credit rates, pricing models, and supported chains - everything an agent needs to decide what to call.

### 2. Evaluate

Search for relevant endpoints and check pricing before committing:

```bash
# Find balance-related endpoints
curl https://x402.goldrush.dev/v1/x402/search?q=balance | jq

# Check pricing for a specific endpoint
curl https://x402.goldrush.dev/v1/x402/endpoints/get-token-balances-for-address | jq
```

The agent can compare credit rates against its budget and select the right tier for variable-length responses.

### 3. Pay

Using the x402 client, the agent signs a payment and gets data in a single request-response cycle:

```typescript
import { HTTPClient } from "@x402/core";
import { ExactEvmScheme } from "@x402/evm";

const client = new HTTPClient({
  scheme: new ExactEvmScheme({
    network: "eip155:84532", // Base Sepolia (testnet)
    privateKey: process.env.WALLET_PRIVATE_KEY,
  }),
});

const balances = await client.get(
  "https://x402.goldrush.dev/v1/eth-mainnet/address/0x742d.../balances_v2/"
);
```

No OAuth, no API key provisioning - the agent just needs a funded wallet.

### 4. Consume

Responses use the same JSON format as the standard GoldRush API. Any existing parsing logic works unchanged.

## Why x402 for agents

| Concern | API Key | x402 |
|---------|---------|------|
| Provisioning | Requires signup, key management, rotation | Wallet is the credential |
| Budget control | Monthly plan, overage charges | Pay exactly per request |
| Human involvement | Account creation, billing setup | None - fully autonomous |
| Discovery | Read docs or hardcode endpoints | Programmatic endpoint discovery |
| Multi-agent | Share key or provision per agent | Each agent gets its own wallet |

## Rate limits

Each wallet is rate-limited to **100 requests per minute**. The `X-RateLimit-Remaining` response header shows how many requests remain in the current window.