# Holding-thesis verification — the five checks

Run all five on every holding before allocating more, and re-run when a thesis depends on a dated event.
Numbers below are the 27 Sep 2026 worked example; they will be stale — the **checks** are what to reuse.

## 1. Claim vs mechanism ("backing" usually isn't what the user thinks it is)

User claim: *"ONDO punya backing BlackRock + katalis Q4"*. Verified reality:
- TRUE at product level: OUSG reserves sit in BlackRock's BUIDL fund (Ondo was the largest BUIDL holder,
  ~38%); BlackRock designed three model portfolios (`Ondo Intelligent Portfolios`, 24 Sep 2026) that Ondo
  tokenises. Also a disclosure that BlackRock funds inside pay fees to BlackRock.
- FALSE at token level: BlackRock does not own or guarantee **ONDO**, and ONDO is a **governance token
  with no fee-sharing** — the protocol collected ~$8,1M/quarter and none of it reaches holders.

Ask every time: *what does this token have a claim on?* Fee share, buyback, burn, or nothing. If the
answer is nothing, TVL/revenue growth does **not** mechanically reprice the token, and the only re-rating
path is regulatory/narrative. Say the distinction in exactly those terms — it is the correction the user
values most.

## 2. Catalyst with a date (and its current status)

ONDO's Q4 catalyst was a US market-structure bill (CLARITY Act) that would have enabled revenue sharing
and opened the US investor base. Status check killed it: **cloture failed 15 Sep 2026, 49–50** (needed 60;
four Republicans voted no). Senate headed into recess; reporting (DLA Piper) called it dead for the year,
next window 2027. Remaining live catalysts were company-level only: SEC registration, DTCC/DTC expansion,
TVL milestones, EU approvals.

Rule: a catalyst without a date and a status check is a hope. Search the bill/announcement/deadline by
name, find the latest dated fact, and quote it.

Contrast — a catalyst that **is** dated and verifiable (HYPE, Hyperliquid AQAv2):
- AQAv2 live 26 Aug 2026: ~90% of yield from **$5–5,5B USDC reserves** (3,5–4% yield) → Assistance Fund →
  market-buys HYPE and **burns** it. Governance 69,08%. Coinbase = treasury deployer, Circle = technical
  deployer, each staking 500k HYPE. **First payout 3 Oct 2026**, then every 30–38 days, est. +$135–160M/yr.
- Existing engine: ~99% of trading fees to the same fund; >$1,3B bought by May 2026, ~7% of market cap/yr.
- Corroborating: Binance spot listing 26 Sep 2026; whale bought $45,8M on 25 Sep; ETF inflows.
- Honest risk: buyback is fee-dependent policy, not a contractual dividend; the first payout size was still
  an *estimate* (event risk); ~251M of 1B supply circulating with contributor tokens locked to 2027–2028.

## 3. Supply structure (the check that explains multi-month underperformance)

For ONDO: 49% circulating, inflation +54%/yr, and a **cliff unlock of ~1,94B (~35% of float, ~$900M) on
18 Jan 2027**; token ~25% of ATH. For INJ: 100M total supply fully circulating, no inflation, no cliff —
plus a staking rework that routes network activity into on-chain revenue (value accrual, unlike ONDO).
Same sector, opposite token structure — that comparison carried the recommendation.

Compute: circulating/total, annual inflation, next cliff as % of float and $ value, and put the date in the
monitor as a countdown (see `hermes-cron-automation` → `references/holdings-watchlist-thresholds.md`).

## 4. Upside room — and which kind

% from ATH is only half the read. Classify:
- *Cheap because it fell*: ONDO 25% of ATH, INJ 14,7% (6,8× to ATH), SOL 42%, ETH 54,7%, BTC 67,2%.
- *Price discovery*: HYPE 94,1% of ATH with a **new ATH 4 days earlier** — no overhead supply, different
  trade (momentum) than a beaten-down recovery bet.

## 5. Beta, for sizing

Realized daily vol from the 90d series (PAID ~7,8%/day vs BTC 1,65%/day) is what turns "35% of portfolio"
into a different risk for different assets. Put beta next to the allocation, not in a footnote.

## Scenario model template (label every assumption)

```python
RET = {  # (bull, base, bear) over ~3 months — ASSUMPTIONS, state them as such
 'BTC': (0.55, 0.08, -0.30), 'SOL': (0.95, 0.12, -0.42), 'INJ': (1.60, 0.15, -0.48),
 'ONDO': (1.10, -0.05, -0.52), 'HYPE': (0.85, 0.10, -0.45), 'PAID': (3.50, -0.35, -0.88),
 'LP': (0.40, 0.10, -0.30), 'CASH': (0.0, 0.0, 0.0)}
P = {'bull': 0.30, 'base': 0.45, 'bear': 0.25}   # probabilities, stated explicitly
```

Then: per-portfolio bull/base/bear + EV, and always include the **current** allocation as a row. The
comparison that persuaded: current (BTC 35/ONDO 35/cash 20) → bull +65% / base −4% / bear −37% / EV +8%;
proposed → bull +94% / base +6% / bear −39% / EV +21% ("bear case nearly the same, upside +29 points").

Keep LP EV conservative in the model when the engine's edge is unproven, and say the sleeve is capped until
the signal ledger shows positive expectancy — that is what makes a max-upside portfolio a plan, not a bet.

## Guardrails that the user accepted (reuse the shape)

1. Soft floor for the whole portfolio (here $900, −36%) → de-risk to core and stop LP
2. Cap the risk sleeve until proven (LP ≤$300 until ≥30 signal-ledger episodes)
3. Zero leverage
4. Count the lottery ticket as zero and never add to it
5. Say out loud that max upside only works if they can watch −40% without selling at the bottom
