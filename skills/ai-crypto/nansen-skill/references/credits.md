# Nansen Credits — Budget Rules & Traps

## Plans

| Plan | Price | Starter credits | Notes |
|------|-------|-----------------|-------|
| **Pro** | $49/mo annual or $69/mo monthly | 1000 (one-time grant) | Top-up any amount. Credits expire 1 year from purchase. |
| **Free** | $0 | 1000 (one-time trial) | **Consumes 10× faster.** 1 Pro credit = 10 Free credits. |
| x402 pay-per-call | per request | N/A | USDC on Base or Solana, no subscription, 5/60 rps/rpm per wallet. |

Enterprise plans only for bulk purchases > $10,000.

## Budget thresholds (applied per operation)

| Estimated credits | Action |
|-------------------|--------|
| **< 50** | Proceed silently |
| **50–200** | Tell user estimate + reason before executing |
| **> 200** | STOP. Propose cheaper alternative (narrower filter, different endpoint, fewer pages). Execute only with explicit approval. |

Same independent-threshold principle as Dune. For batches, multiply per-call cost by expected number of calls.

## Credit cost multiplier traps

### 1. `premium_labels: true` — silent 30× cost
TGM endpoints with premium labels cost **150 credits** instead of 5.
- `tgm/holders`
- `tgm/pnl-leaderboard`
- `tgm/perp-positions`
- `tgm/perp-pnl-leaderboard`
- `tgm/perp-trades`

**Rule:** never set `premium_labels: true` unless user explicitly asked for premium-label data. Default (omit or `null`) returns labels according to plan tier.

### 2. Free-tier 10× multiplier
If on Free plan, a 5-credit Smart Money call = 50 Free credits. 1000 starter credits = only **~20 Smart Money calls**. Check tier before recommending workflow.

### 3. Labels endpoints
- `profiler/address/labels`: **100 credits** per address
- `profiler/address/premium-labels`: **500 credits** per address

For a batch of 10 wallets just to get names: 1000 / 5000 credits. Prefer `labels` in response of other endpoints — many endpoints include label info for free.

### 4. Agent endpoints
- `agent/fast`: 200 credits
- `agent/expert`: 750 credits

At 1000 Pro starter credits, `agent/expert` is ~75% of your trial budget. **Always confirm with user** before calling agent endpoints.

### 5. Pagination stacking
Each page is a separate call = separate credit charge. Paginating 10 pages of Smart Money endpoint = 50 credits, not 5.

**Mitigation:** always set `pagination.per_page: 1000` (maximum) to fit full result in single call when possible.

## Live credit monitoring — response headers

Every response includes:
```
X-Nansen-Credits-Used: 5           — this call
X-Nansen-Credits-Remaining: 983    — account balance after this call
```

**In scripts:**
- Log remaining after each call
- Check against safety threshold (e.g. stop if remaining < 200)
- If user has multiple keys (multi-key mode), rotate when remaining is low

## Multi-key rotation policy

Same as Dune / Solscan (see memory `feedback_dune_credits.md`):

- **Single key** → use it, thresholds apply
- **Multiple `NANSEN_API_KEY_*`** → rotate on 403 "insufficient credits" or 429
- **x402 (pay-per-call)** — use as last resort, ask user first (each call costs real USDC)

## x402 pay-per-call fallback

When all API keys are out of credits and user agreed:
1. Send request WITHOUT `apiKey` header
2. Server returns 402 with `Payment-Required` header containing payment details
3. Use x402 client library (e.g. `x402.client.x402_client`) to auto-pay in USDC on Base/Solana
4. Retry with payment receipt

Rate limits for x402 are separate: **5 req/sec, 60 req/min per wallet.**

Log each x402 payment to user so they can audit spend. See `examples/x402_payment.py` for reference (not written yet — TODO).

## Tracking usage manually

Nansen dashboard: https://app.nansen.ai/api?tab=usage-analytics

From API — no explicit `/usage` endpoint (unlike Solscan `/monitor/usage`). Use response headers for real-time tracking.

## Source

- https://docs.nansen.ai/about/credits-and-pricing-guide
- https://docs.nansen.ai/getting-started/rate-limits
- https://docs.nansen.ai/getting-started/error-handling
- OpenAPI schema in llms-full.txt
