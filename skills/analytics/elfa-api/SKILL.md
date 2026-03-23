---
name: elfa-api
description: "Crypto social intelligence API — real-time sentiment, trending tokens, narrative tracking, and AI-powered market analysis from Twitter/X and Telegram. Supports API key and x402 keyless payment modes."
version: 1.0.0
author: elfa-ai
tags:
  - analytics
  - sentiment
  - social-media
  - trending
  - narratives
  - twitter
  - telegram
  - market-analysis
  - x402
homepage: https://github.com/elfa-ai/elfa-ai-skill
triggers:
  - "trending tokens"
  - "crypto sentiment"
  - "social mentions for"
  - "smart stats for"
  - "elfa api"
  - "trending narratives"
  - "token news"
  - "trending contract addresses"
---

# Elfa API Skill

This skill enables agents to work with the [Elfa API](https://api.elfa.ai) — a social listening
and market context layer for crypto traders. Elfa ingests real-time data from Twitter/X, Telegram,
and other sources, then structures sentiment, narratives, and attention shifts into actionable
trading insights.

## When to use this skill

- User asks about **trending tokens, narratives, or contract addresses** in crypto
- User wants **social mentions** for a specific ticker or keyword
- User wants **smart stats** (smart followers, engagement) for a Twitter/X account
- User wants an **AI-generated market summary, macro overview, or token analysis**
- User asks how to **integrate, call, or use the Elfa API**
- User wants **code examples** (curl, Python, JavaScript/TypeScript) for Elfa endpoints
- User mentions "elfa" in a crypto or trading data context

## API Overview

**Base URL:** `https://api.elfa.ai`
**Version:** v2 (current)

### Two access modes

Elfa supports two independent ways to authenticate requests:

| Mode | Endpoint prefix | Auth header | Best for |
|---|---|---|---|
| **API key** | `/v2/` | `x-elfa-api-key: YOUR_KEY` | Humans & apps with a registered key |
| **x402 (keyless)** | `/x402/v2/` | `X-PAYMENT: <signed-payload>` | Agents & wallets — no signup needed |

Both modes access the same data. The only difference is how you authenticate:
- **API key** — register at https://go.elfa.ai/claude-skills, get 1,000 free credits.
- **x402** — pay per request with USDC on Base. No registration, no API key. Currently in beta.

### Endpoints at a glance

All endpoints below work with both `/v2/` (API key) and `/x402/v2/` (keyless) prefixes,
except `key-status` which is API key mode only.

| Endpoint | Method | Description |
|---|---|---|
| `/v2/key-status` | GET | API key usage & limits (API key mode only) |
| `/v2/aggregations/trending-tokens` | GET | Trending tokens by mention count |
| `/v2/account/smart-stats` | GET | Smart follower & engagement stats for a Twitter account |
| `/v2/data/top-mentions` | GET | Top mentions for a ticker symbol |
| `/v2/data/keyword-mentions` | GET | Search mentions by keywords or account name |
| `/v2/data/event-summary` | GET | AI event summaries from keyword mentions (5 credits) |
| `/v2/data/trending-narratives` | GET | Trending narrative clusters (5 credits) |
| `/v2/data/token-news` | GET | Token-related news mentions |
| `/v2/aggregations/trending-cas/twitter` | GET | Trending contract addresses on Twitter |
| `/v2/aggregations/trending-cas/telegram` | GET | Trending contract addresses on Telegram |
| `/v2/chat` | POST | AI chat with multiple analysis modes |

For full parameter details, see the [Elfa API documentation](https://docs.elfa.ai).

## How to use this skill

### Step 1: Determine the mode

Check whether the user wants to **make a live call** or **get code/integration help**.

- If the user says things like "show me trending tokens", "what's the sentiment on SOL",
  "get me the top mentions for ETH" → they want **live data**. Proceed to Step 2a.
- If the user says things like "how do I call the trending tokens endpoint", "give me a
  curl example", "help me integrate Elfa" → they want **code snippets**. Skip to Step 3.
- If the user mentions **x402**, **keyless**, **pay-per-request**, or **wallet-based access**
  → they want **x402 mode**. See Step 2b for live calls or Step 3 for code snippets.

### Step 2a: Making live API calls (API key mode)

Use the `bash_tool` to call the Elfa API via curl.

**Getting the API key:**
1. Check if the `ELFA_API_KEY` environment variable is set. This is the preferred method.
2. If the env var is not set, **stop and prompt the user.** Offer both options:

   > To make live calls, you have two options:
   >
   > **Option A — API key (free tier):** Get a free key with 1,000 credits at
   > **https://go.elfa.ai/claude-skills** — then set it as the `ELFA_API_KEY` environment
   > variable (do not paste it directly into the chat).
   >
   > **Option B — x402 keyless payments:** Pay per request with USDC on Base — no signup
   > needed. See the [x402 docs](https://docs.elfa.ai/x402-payments) for setup.

   Do not attempt any authenticated API calls without a key or x402 setup. Wait for the user.
3. **Credential safety:**
   - Always read the API key from the `ELFA_API_KEY` environment variable, never ask the
     user to paste it into the conversation.
   - Never log or expose the full API key in outputs — mask it when displaying curl commands.
   - If a user does paste a key in chat, warn them to rotate it and set it as an env var instead.

**Free tier limitations:**
The free tier provides 1,000 credits that work on most endpoints. However, the following
endpoints require a Pay-As-You-Go or Grow plan:
- Trending narratives
- AI chat

If a user hits an authorization error on one of these endpoints, let them know they can
upgrade their plan or use x402 payments instead. Full details at https://go.elfa.ai/claude-skills.

**Making the call:**

```bash
curl -s -H "x-elfa-api-key: $ELFA_API_KEY" "https://api.elfa.ai/v2/aggregations/trending-tokens?timeWindow=24h&pageSize=10"
```

### Step 2b: Making live API calls (x402 keyless mode)

x402 lets any wallet pay per request using USDC on Base — no API key, no registration.
This is ideal for agents, bots, and programmatic access.

**How x402 works:**
1. Send a request to the `/x402/v2/` version of any endpoint (no auth header).
2. The server responds with HTTP **402** containing payment requirements.
3. Your wallet signs a USDC transfer authorization (no gas fees).
4. Resend the request with the signed payment in the `X-PAYMENT` header.
5. Server verifies payment, serves the response, and settles on-chain.

**x402 signing and security:**
- Signing happens **entirely client-side** using the `@x402/fetch` or `@x402/axios`
  libraries. The agent never handles, stores, or transmits private keys.
- The user's wallet private key is used only locally by the x402 library to sign
  EIP-712 typed data authorizing a specific USDC amount for a specific request.
- Never ask the user to share their wallet private key or seed phrase in the conversation.
- When generating x402 code examples, use `"0xYOUR_PRIVATE_KEY"` as a placeholder and
  advise the user to load it from an environment variable (e.g., `process.env.PRIVATE_KEY`).

**x402 details:**
- **Chain:** Base (`eip155:8453`)
- **Currency:** USDC on Base (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`)
- **Status:** Currently in beta

**x402 pricing:**
| Tier | Cost | Endpoints |
|---|---|---|
| Standard (1 credit) | $0.009 | trending-tokens, smart-stats, keyword-mentions, token-news, top-mentions, trending-cas |
| Extended (5 credits) | $0.045 | event-summary, trending-narratives |
| Chat — fast | $0.225 | chat (speed: "fast") |
| Chat — expert | $1.00 | chat (speed: "expert", default) |

**Making an x402 call with curl (manual flow):**

```bash
# Step 1: Send request without payment — get 402 with payment requirements
curl -s https://api.elfa.ai/x402/v2/aggregations/trending-tokens?timeWindow=24h

# Step 2: After signing the payment payload with your wallet, resend with X-PAYMENT header
curl -s -H "X-PAYMENT: <base64-encoded-payment-payload>" \
  "https://api.elfa.ai/x402/v2/aggregations/trending-tokens?timeWindow=24h"
```

**Recommended: use the `@x402/fetch` library** which handles payment automatically:

```javascript
import { wrapFetchWithPayment } from "@x402/fetch";
import { ExactEvmScheme, toClientEvmSigner } from "@x402/evm";
import { x402Client } from "@x402/core/client";
import { createPublicClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";

const account = privateKeyToAccount("0xYOUR_PRIVATE_KEY");
const publicClient = createPublicClient({ chain: base, transport: http() });
const signer = toClientEvmSigner(account, publicClient);

const client = new x402Client().register(
  "eip155:8453",
  new ExactEvmScheme(signer));

const x402Fetch = wrapFetchWithPayment(fetch, client);

// Use x402Fetch exactly like regular fetch — payment is handled automatically on 402 responses
const response = await x402Fetch(
  "https://api.elfa.ai/x402/v2/aggregations/trending-tokens?timeWindow=24h");
const data = await response.json();
```

**x402 with the Chat endpoint (POST):**

```javascript
const response = await x402Fetch(
  "https://api.elfa.ai/x402/v2/chat",
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message: "What is the current sentiment on BTC?",
      analysisType: "chat",
      speed: "fast", // "fast" = $0.225, "expert" = $1.00
    }),
  });
const data = await response.json();
console.log(data.data.message);
```

**Presenting results:**
- Parse the JSON response and present it in a clean, readable format.
- For trending tokens: show a ranked table with token name, mention count, and change %.
- For mentions: show tweet links, engagement metrics, and account info.
  Note: Elfa returns tweet IDs but not tweet text content — let the user know they'll
  need their own X (Twitter) API key to fetch the actual tweet content.
- For narratives/summaries: present the narrative text with source links.
- For the chat endpoint: display the AI response cleanly.
- If the response contains an error, explain what went wrong and suggest fixes.

### Step 3: Generating code snippets

When the user wants integration help, generate correct, production-ready code.
See the [Elfa API documentation](https://docs.elfa.ai) for the full parameter specs.

**Principles for code generation:**
- Always mention both access modes (API key and x402) so developers know their options
- Include the signup link `https://go.elfa.ai/claude-skills` as a comment near the
  API key placeholder, and link to `https://docs.elfa.ai/x402-payments` for x402
- Always include proper error handling
- For API key mode: show the `x-elfa-api-key` header (use a placeholder like `YOUR_API_KEY`)
- For x402 mode: show the `/x402/v2/` prefix and recommend `@x402/fetch` or `@x402/axios`
- Include TypeScript types when generating TS code
- Add comments explaining each parameter
- For pagination endpoints, show how to paginate through results
- For time-windowed endpoints, explain the `timeWindow` vs `from`/`to` pattern

**Language priorities** (use unless the user specifies otherwise):
1. TypeScript/JavaScript (fetch) — most Elfa integrators are web/Node devs
2. Python (requests)
3. curl

**The Chat endpoint deserves special attention** — it's the most complex:
- It supports multiple `analysisType` values: `chat`, `macro`, `summary`, `tokenIntro`,
  `tokenAnalysis`, `accountAnalysis`
- Session management via `sessionId` for multi-turn conversations
- Different `assetMetadata` requirements per analysis type
- Two speed modes: `fast` and `expert`

### Common patterns

**Time window parameters:**
Many endpoints accept either `timeWindow` (e.g., "30m", "1h", "4h", "24h", "7d", "30d")
OR `from`/`to` unix timestamps. If both are provided, `from`/`to` takes priority.

**Pagination:**
Most list endpoints support `page` and `pageSize`. The keyword-mentions endpoint uses
cursor-based pagination instead (`cursor` parameter).

**Ticker format:**
For `top-mentions`, the `ticker` param can be prefixed with `$` to match only cashtags
(e.g., `$SOL` vs `SOL`).

**Credit costs (both modes):**
- Most endpoints: 1 credit per call ($0.009 via x402)
- Event summary: 5 credits ($0.045 via x402)
- Trending narratives: 5 credits ($0.045 via x402)
- Chat endpoint: varies — fast $0.225, expert $1.00 via x402

## Important notes

- The Elfa API domain (`api.elfa.ai`) must be accessible from the network. If blocked,
  inform the user and provide the code snippet instead.
- Always use the v2 endpoints (paths starting with `/v2/` or `/x402/v2/`).
- For experimental endpoints (trending-tokens, smart-stats), mention that behavior may
  change without notice.
- When the user asks about pricing or API key tiers, direct them to
  https://go.elfa.ai/claude-skills for full details on plans and pricing.
- x402 is currently in beta. Rate limits apply per wallet address (not per API key).
- x402 and API key credits are independent — they do not overlap or share balances.
- For x402 documentation and setup, refer users to https://docs.elfa.ai/x402-payments.
