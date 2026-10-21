# Crypto Chart Analysis — Reference

Companion to `SKILL.md`. Use when the agent needs deeper definitions; keep the main skill lean.

## Cloud fetch cheat-sheet

```bash
SKILL=/cursor/stores/self/skills/crypto-chart-analysis
# fallback: /agent/skills/crypto-chart-analysis

# Perp (default OKX)
python3 "$SKILL/fetch_market_context.py" --symbol ETHUSDT --market perp --tfs 1d,4h,1h -o /tmp/crypto_ctx.json

# Spot via Binance Vision
python3 "$SKILL/fetch_market_context.py" --symbol BTCUSDT --market spot --venue binance_vision --tfs 1d,4h

# Bitget perp fallback
python3 "$SKILL/fetch_market_context.py" --symbol BTCUSDT --market perp --venue bitget
```

JSON fields used in analysis: `tfs.*.last`, `tfs.*.atr14`, `tfs.*.swings`, `tfs.*.structure_hint`, `positioning.*`, `fetched_at_utc`, `venue`.

## Textbook lineage (why hierarchy looks like this)

- Dow → Edwards & Magee → Murphy: trend/structure and classical S/R first
- Nison: candlesticks as timing at levels, not standalone
- Wyckoff: effort vs result, accumulation/distribution language, volume stories
- Auction market / Market Profile: value areas, acceptance vs rejection

Practitioner crypto adds: OI, funding, liquidations, fragmented venues, 24/7 sessions.

## Structure vocabulary

| Term | Meaning |
|------|---------|
| HH / HL | Higher high / higher low — bullish structure |
| LH / LL | Lower high / lower low — bearish structure |
| BOS | Break of structure — continuation through a prior swing in trend direction |
| CHoCH | Change of character — first structural clue of regime shift |
| Acceptance | Price holds beyond a level (time/closes/volume), not a wick alone |
| Rejection | Swift failure beyond a level back into prior range |

## OI × price quick matrix

| Price | OI | Working hypothesis |
|-------|-----|--------------------|
| ↑ | ↑ | New longs / leveraged trend |
| ↑ | ↓ | Short covering |
| ↓ | ↑ | New shorts / leveraged sell |
| ↓ | ↓ | Long liquidation / deleveraging |

Always pair with location in structure. Same OI print at range mid ≠ at range edge.

## Funding notes

- Baseline for many perps is slightly positive, not zero
- Extremes → fragility / fuel, not a trade trigger alone
- Annualize: `rate × periods_per_year` (8h funding → ×1095 for rough APR%)
- Alts: hedge flow can distort negative funding; treat with extra caution

## Liquidations

- Measure of forced flow intensity and event risk
- Post-cascade direction is unresolved until new acceptance forms
- Exchange liquidation feeds can be incomplete

## Order flow roles

| Tool | Role | Failure mode |
|------|------|--------------|
| DOM | Resting liquidity now | Spoof / pull |
| Tape | Aggressor prints | Algo slicing noise |
| Footprint | Volume-by-price in bar | Thin bars |
| CVD | Cumulated aggressor delta | Anchoring / reset bias |

Use to raise/lower confidence in a **structural** setup. Do not invent a setup from CVD alone.

## Secondary tools — allowed vs weak

**Allowed after structure:** zone candles, contextual RSI divergence, MA as dynamic S/R, Fib pullback map inside impulse, pattern names as labels.

**Weak as primary:** Elliott/harmonics/Gann, multi-indicator stacks, overbought shorts in strong trends, Fib on every micro-swing.

## Chart checklist (compact)

1. Regime on HTF?
2. Zones + liquidity pools?
3. Invalidation + R?
4. Volume / OI / funding agree or fight?
5. BTC / session / event conflict?
6. Secondary tool only for timing?

## Journal one-liner template

`[TF] [instrument]: [regime]. Idea [L/S/flat] at [zone] because [structure]. Confirm [volume/OI/funding]. Invalid below/above [level]. Anti: if [break] then [flip].`
