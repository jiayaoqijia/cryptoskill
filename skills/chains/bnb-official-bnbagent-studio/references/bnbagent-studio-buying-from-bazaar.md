---
name: bnbagent-studio-buying-from-bazaar
description: When the user wants their agent to buy a paid x402 capability - market data, inference, any pay-per-call API - from the Binance Bazaar (B402) or any other x402 service. Owns discovery (browse the Bazaar / studio recommendations), trusting a merchant (`bag x402 trust`), wiring the buyer @tools (x402-buyer recipe), verifying with a paid test call, and the mainnet-money caveats.
---

> **Reference file** of the `bnbagent-studio` router skill - installed at `bnbagent-studio/references/` and loaded on demand (not a standalone skill). Route here via the router's decision tree.

# bnbagent-studio-buying-from-bazaar

Procedure to give an agent a **paid capability**: the agent calls an x402-protected API, receives a `402 Payment Required`, selects the explicit network/catalog asset, pays through an allowed wallet route, and gets the data. U is the default only when `--asset` is omitted; Studio never changes token automatically.

**The three roles, kept separate** (do not conflate):

- **Bazaar** (`https://www.binance.com/bapi/ramp/v1/public/ramp/b402/bazaar/…`) - a public, auth-free **catalog** of x402 merchants. It is never in the data path and never in the payment path.
- **The merchant** (e.g. CMC) - the agent talks to it **directly**: request → 402 → signed retry → data.
- **B402 facilitator** (verify/settle, gas fronted) - the **merchant's** payment plumbing. The agent never calls it.

**Recommendation, not admission**: studio ships a reviewed shelf (the CLI's built-in recommended-merchants table - today: CMC's 4 market-data endpoints), but any x402 service can be trusted by URL. Studio recommends; it never gate-keeps the user's own spending choices.

## Step 0 - know what's on offer

Studio-reviewed (the fast path): run `bag x402 trust cmc` and skip to Step 1. CMC's 4 endpoints (all `$0.01/call`, base `https://pro-api.coinmarketcap.com`):

| Endpoint | Path | Good for |
| --- | --- | --- |
| Quotes Latest | `/x402/v3/cryptocurrency/quotes/latest?id=1` | prices, holdings briefs, price alerts |
| Listings Latest | `/x402/v3/cryptocurrency/listings/latest?start=1&limit=10` | top-N market overviews, rotation signals |
| DEX Search | `/x402/v1/dex/search?q=bnb` | new-token discovery, name checks |
| DEX Pairs Quotes | `/x402/v4/dex/pairs/quotes/latest?pair_address=0x…` | pool liquidity/volume, LP monitoring |

Browsing the wider Bazaar (optional): the discovery API is public JSON - `GET …/bazaar/search?query=<keyword>&limit=10`, `…/bazaar/resources`, `…/bazaar/merchant?payTo=0x…`. Each resource carries `accepts[]` (who gets paid, in what asset, on which chain) and 30-day quality signals (`l30DaysTotalCalls`, `l30DaysUniquePayers`). Merchants found there are **unreviewed** - trust them by URL only after checking the payTo out-of-band.

> Doc lag warning: a merchant's human docs may lag its live 402 (CMC's page documents only Base/USDC; the live challenge also accepts BSC $U via EIP-3009). Machine decisions always come from the live `accepts[]` - which is exactly what `bag x402 trust` and `bag x402 quote` read.

## Step 1 - trust the merchant (writes config, never pays)

```bash
bag x402 trust cmc                       # studio-reviewed: pinned payTo byte-compared vs live 402
bag x402 trust https://api.example.com/thing --cap 0.05   # any other x402 service (unreviewed)
```

What it does: probes the live 402 (free), shows **who gets paid and how much per call**, then - after your explicit confirmation - writes:

```toml
[payments.x402.merchants.cmc]
domain = "pro-api.coinmarketcap.com"
pay_to = "0x3C5f3a6cE224BB89D72f5EB4232ecC27F67B3eeA"  # pinned; byte-compared on every payment
per_call_cap_usd = 0.02                                 # clamps every call, LLM cannot widen
verified = true                                         # studio-reviewed shelf
```

Hard-stop cases: a reviewed merchant whose live payTo drifts from the studio pin (address rotation or tampering - upgrade studio or verify out-of-band and pass `--pay-to`), and `--cap` below the live per-call price.

Wallet kinds and rails: `evm-local` and Turnkey use only catalog-verified EIP-3009 U routes; their Permit2 path is deferred. Altana may pay Permit2 Exact only through the SDK's atomic `requestExact` interface, which binds the same challenge's resource, CAIP-2 network, asset, amount, payTo, method, timeout, proxy/name/version and trusted spender before signing. ERC-20 allowance is still checked against canonical Permit2. TWAK does not expose an equivalent verifiable exact-route interface, so Studio fails closed before dispatch. These are code boundaries, not claims that any merchant or live chain flow has passed verification.

## Step 2 - wire the buyer tools into the agent

```bash
bag recipe code x402-buyer        # emits src/x402Buyer.ts (next to src/tools.ts)
```

Then wire the set into the agent's LLM in `src/unifiedMain.ts` (A2A — one entrypoint deployed to both clouds) or `src/mcpMain.ts` (MCP) - the scaffold's `tools:` line carries this exact hint in a comment:

```ts
import { X402_BUYER_TOOLS } from "./x402Buyer.js";
// ...
tools: { ...LLM_READ_TOOLS, ...X402_BUYER_TOOLS },
```

This is the whole point of the feature: the DEPLOYED agent buys the data itself at work time (e.g. inside `notify_funded` while producing a deliverable) - the CLI commands below are only the operator's test rig. The LLM gets two tools:

- `buy_with_x402(url, max_usd, method="GET")` - pay + fetch. The LLM chooses **which** allowed URL to call and with what query params; it can NEVER choose who gets paid (pinned `pay_to`) or widen the caps (per-call cap, `[budget].max_per_day_usd`, `[payments.x402].max_per_request_usd`).
- `quote_x402(url, method="GET")` - free 402 inspection.

This is commitment #3 intact: signing stays fixed handler code; the merchant table is user-confirmed config, not an LLM-writable surface.

> **For the agent's LLM - the one invariant it keeps getting wrong:** x402 merchants need **NO API key**. CMC's x402 endpoints (and every Bazaar merchant) authenticate the caller by the on-chain EIP-3009 payment the agent's wallet signs - there is no `Authorization` / `X-API-KEY` header anywhere. So when a funded task asks for CMC/paid data and `buy_with_x402` is in the toolset, the LLM MUST call it - it must never fall back to "I need an API key / I can't do this without a key." Payment is already fenced by `per_call_cap_usd` + `[budget].max_per_day_usd`, so the call is always safe to make. The recipe bakes this into the tool description and the scaffold's `system` prompt; keep it there if you edit them.

## Step 3 - verify end to end

```bash
bag x402 quote "https://pro-api.coinmarketcap.com/x402/v3/cryptocurrency/quotes/latest?id=1" --asset U  # free
bag x402 buy   "https://pro-api.coinmarketcap.com/x402/v3/cryptocurrency/quotes/latest?id=1" --asset U --max-usd 0.02
bag dev        # then ask the agent something that needs the paid data
```

`buy` needs the wallet backend ready and the selected token funded. An unavailable or underfunded selection prints only verified alternatives with exact `--asset SYMBOL` hints; it never switches asset or retries. Treat a success message as evidence for that invocation only, not as general live compatibility.

## The money - read before funding

- **Mainnet, real $U.** CMC (and current Bazaar merchants) settle **only** on BSC mainnet (`eip155:56`); there is no testnet channel. This is independent of your project's `[network].default` - a testnet seller can still buy mainnet data.
- **Exposure is fenced** three ways: per-call `per_call_cap_usd`, per-request `max_per_request_usd`, and the daily `[budget].max_per_day_usd` (shared ledger at `.studio/spend-ledger.json`).
- **Platform trials:** `bag deploy` warns (never blocks) when `[deploy].destination = "platform"` meets a merchants table - the trial ships the wallet key to the operator's Secrets Manager under testnet-scoped consent. For paid-capability agents prefer self-deploy, or keep a throwaway wallet holding only pocket money.
- **Funding**: buy $U on PancakeSwap (`?outputCurrency=0xcE24439F2D9C6a2289F741120FE202248B666666`) to the agent wallet address (`bag wallet status`). A few dollars covers hundreds of CMC calls; x402 payments themselves are gasless for the buyer (the facilitator fronts gas).

## Troubleshooting

| Symptom | Meaning / fix |
| --- | --- |
| `X402HostNotAllowedError` | Merchant not trusted yet → `bag x402 trust <merchant\|url>` |
| `X402RecipientRequiredError` | No pinned recipient for that host → same fix |
| `X402RecipientMismatchError` | Live payTo drifted from the pin - do NOT override casually; re-verify the merchant |
| `X402BudgetExhaustedError` | Per-call cap or daily budget hit - raise `per_call_cap_usd` / `[budget].max_per_day_usd` deliberately |
| `x402 402 has no EIP-3009-payable option` | The selected asset has no catalog-verified EIP-3009 route for a local/Turnkey buyer. Do not enable raw Permit2 signing. Altana requires a matching `requestExact` Permit2 route; TWAK paid x402 remains pre-dispatch unsupported. |
| `…→Permit2 allowance … cannot cover max_usd` | Altana only: the bounded Permit2 allowance for that asset is spent/too small - re-run `bag wallet session x402-setup --allowance <amount>` (admin key) |
| `wallet/payment method unsupported for USDC/USDT` | The asset settles b402 through `permit2-exact` only, and `evm-local`/`turnkey` sign EIP-3009 only (`twak` is fail-closed for paid x402). The route is fine - the wallet cannot sign it. Pay it from an `altana` session wallet armed with `bag wallet session x402-setup --allowance <amount> --asset USDC`, or retry the offered EIP-3009 alternative. |
| `X402PolicyError` / `PolicyViolation` | Signing allowlist - see `bnbagent-studio-extending-signing.md` |

**Different from**:

- `bnbagent-studio-buying-via-8183.md` (same directory) - buying from an **ERC-8183 seller agent** (jobs, disputes, settle windows). This file is about flat pay-per-call x402 APIs; no job lifecycle.
- `bnbagent-studio-extending-signing.md` - the signing-policy allowlist mechanics that back all of this.
