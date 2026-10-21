---
name: crypto-chart-analysis
description: >-
  Analyze cryptocurrency charts (spot/perp) in Cursor Cloud Agents: fetch live
  OHLCV/OI/funding via this skill's script, then apply practitioner hierarchy
  (structure → risk → volume/positioning → indicators as timing only). Use when
  the user asks to read a crypto chart, review a setup, map levels, assess
  trend vs range, interpret funding/OI/liquidations, or critique a trading idea
  — especially in cloud/background agent sessions. Do NOT use for unrelated
  coding or as a guarantee of returns.
---

# Crypto Chart Analysis (Cloud Agent)

Educational market-structure framework for reading crypto charts **from a Cursor Cloud Agent VM**. Not investment advice. Never promise profits, “sure” entries, or guaranteed targets.

## When to use

- User shares a ticker, chart screenshot, timeframe, or setup (long/short)
- Asks for structure, levels, bias, invalidation, R-multiple
- Asks about OI, funding, liquidations, breakouts, or alt vs BTC context
- Cloud session: “разбери BTC”, “что по ETH”, “оценка сетапа”

## When not to use

- Non-market coding or infra work
- Guaranteed signals / “what to buy now” as personalized advice
- Pure news/tokenomics without a chart ask

## Priority weights (keep this order)

| Weight | Layer | Job |
|--------|--------|-----|
| ~70% | Structure + risk | Regime, levels, MTF, invalidation, size logic |
| ~20% | Volume / flow / positioning | Confirm or challenge the structure story |
| ~10% | Oscillators / named patterns | Timing only, never the thesis |

**Hard rule:** structure → risk/invalidation → volume/flow/OI-funding → indicators. Reverse order is a failure mode.

---

## Cloud Agent runtime (mandatory here)

This skill is meant to run **in the current Cloud Agent environment**, not on the user’s phone or local TradingView.

### Skill location

Resolve the skill directory in this order (first hit wins):

1. `$CRYPTO_CHART_SKILL_DIR` if set
2. `/cursor/stores/self/skills/crypto-chart-analysis`
3. `/agent/skills/crypto-chart-analysis`
4. `.cursor/skills/crypto-chart-analysis` under the workspace (if a repo is mounted)

Fetcher script: `<skill_dir>/fetch_market_context.py`

### Before analysis — pull live data

Unless the user only wants theory, **always fetch** before concluding:

```bash
python3 "<skill_dir>/fetch_market_context.py" \
  --symbol BTCUSDT \
  --market perp \
  --venue auto \
  --tfs 1d,4h,1h \
  --limit 120 \
  -o /tmp/crypto_ctx.json
```

Then `Read` `/tmp/crypto_ctx.json` (or use stdout). Defaults:

| Flag | Default | Notes |
|------|---------|--------|
| `--market` | `perp` | `spot` for cash markets |
| `--venue auto` | okx (perp) / binance_vision (spot) | see egress table |
| `--tfs` | `1d,4h,1h` | add `15m` only for timing |
| `--limit` | `120` | enough for swings + ATR |

Do **not** pass `--full-candles` into the model context unless needed — default payload keeps `candles_tail` + swings.

### Egress reality (this Cloud VM)

| Source | Typical status | Use for |
|--------|----------------|---------|
| OKX (`www.okx.com`) | OK | Perp klines, funding, OI — **default** |
| Bitget | OK | Perp fallback |
| Binance Vision (`data-api.binance.vision`) | OK | Spot klines |
| Binance main / fapi | Often geo-blocked | Avoid as primary |
| Bybit | Often geo-blocked | Avoid as primary |
| CoinGecko | OK | Quick spot price sanity check only |

If a venue fails, retry `--venue okx` or `--venue bitget`. State which venue’s book you used — never pretend multi-exchange aggregation.

### Screenshots

If the user attaches a chart image: `Read` the image path, extract marked levels/TF, **still fetch** live OHLCV/OI/funding to timestamp the analysis. Call out conflicts between the screenshot and live data.

### Tools to use (cloud)

- **Shell** — run `fetch_market_context.py` / curl fallbacks
- **Read** — JSON context + chart images
- **WebSearch / WebFetch** — only for scheduled events (CPI, options expiry), not as a candle source
- **WriteCanvas** — optional durable bias map for long analyses
- Do **not** claim you opened TradingView or controlled the user’s phone

### Cloud limits (be explicit)

- No true DOM/tape/footprint from this skill — treat order flow as unavailable unless user pastes it
- OI/funding are **venue-specific** (OKX ≠ Binance)
- Script `structure_hint` is a helper, not the final call — agent still applies the full checklist
- No private account balances, positions, or API keys required (public market data only)

---

## Workflow

### 0. Intake + fetch

Collect if missing: symbol, spot vs perp, TFs, goal (bias / entry sketch / critique).

Then run the fetcher. If data incomplete, produce a **conditional** analysis with assumptions.

### 1. Regime (primary)

- Trend up (HH/HL), trend down (LH/LL), or range
- Last structure shift in plain language
- HTF owns bias; LTF for timing — do not start from 1m

Use script swings + `structure_hint` as input, then judge.

### 2. Liquidity and S/R (primary)

Zones, not 1-tick lines: swing H/L, range edges, round numbers, stop pools above highs / below lows. Label support / resistance / flip.

### 3. Risk first (primary)

Every actionable idea needs invalidation, stop logic, R-targets, and explicit **NO TRADE** when mid-range / TF conflict / illiquid / pre-event fog. No invalidation → no direction.

### 4–5. Volume + volatility

Participation vs empty breakouts; compression vs expansion (use `atr14` from fetch). Spot vol ≠ perp vol.

### 6. Crypto positioning (from fetch `positioning`)

| Reading | Hypothesis (not certainty) |
|---------|----------------------------|
| Price ↑ + OI ↑ | Fresh leverage |
| Price ↑ + OI ↓ | Short cover |
| Price ↓ + OI ↑ | Fresh shorts |
| Price ↓ + OI ↓ | Long washout |
| Extreme funding | Crowding — **not** auto-reversal |
| Liquidations | Event/fuel — need acceptance after |

Use `funding_apr_pct_approx` from the script. Pair funding with OI + structure always.

### 7. Secondary tools (timing only)

Candles / RSI / MA / Fib / pattern names only **at zones** after structure+risk. Skip holy-grail indicator stacks.

### 8. Practitioner checks

No-trade zones; breakout = hypothesis until acceptance; liquidity above highs; scenario + anti-scenario; session/events; BTC beta; fees/funding/slippage; journalable one-liner.

### 9. Output format

```markdown
## Bias map
- Instrument / venue / TFs / data timestamp (UTC):
- Regime (HTF → LTF):
- Key zones:

## Working hypothesis
- Idea (or NO TRADE) + why (structure first)
- Confirm / invalidate

## Risk sketch
- Invalidation / R / no-trade note

## Positioning (perp)
- OI + funding APR (venue-named)

## Secondary timing (optional)

## Anti-scenario

## Assumptions / missing data
- e.g. no liquidation feed, single-venue OI
```

One-line disclaimer: framework, not financial advice.

---

## Response style

- Match user language (RU/EN)
- Conditional (“if held / if broken”); prefer **NO TRADE** over forced bias
- No hype, no emojis, no guaranteed targets
- Cite venue + fetch timestamp

## Anti-patterns

- Analyze from memory without a fetch when live price matters
- Lead with RSI/MACD before structure
- Treat funding extremes or liquidations as automatic reversals
- Entries without invalidation
- Claiming Binance OI while data came from OKX
- Presenting script hints as certified signals

## Files in this skill

| File | Role |
|------|------|
| `SKILL.md` | This playbook |
| `fetch_market_context.py` | Cloud data pull + swings/ATR/funding APR |
| `reference.md` | Deeper definitions / matrices |

If the user wants more depth on a subsection, open `reference.md`.
