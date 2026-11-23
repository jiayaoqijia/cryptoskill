# Watchlist threshold calibration (holdings monitor, 27 Sep 2026)

Pattern: a **silent** `no_agent` watchdog that only prints when something material happens, plus a daily
agent digest whose numbers come from the same script. Both jobs point at one script so the numbers can
never disagree (`~/.hermes/scripts/holdings_watch.py`, state in `~/.hermes/data/holdings_watch_state.json`).

Design that works:
- Script has `--debug` (prints the full table, for the digest job and for testing) and default mode
  (prints **only** triggered alerts → empty stdout = silent cron = no message).
- State file stores last values + a `last_alert[<key>]` timestamp per alert type, with a cooldown
  (6h used here). Without it the same crash re-alerts every tick.
- Track *the tokens the user actually holds* (BTC, ONDO, INJ, PAID at the time), not a generic watchlist.

## Thresholds must scale with the asset's own volatility

A single % threshold either spams on memecoins or stays silent on BTC. Used here:

| Class | 24h move | Extra conditions |
|---|---|---|
| BTC (low beta) | ±5% | new 30d high/low |
| Large alt (ONDO, INJ) | ±8% | new 30d high/low, agreed exit/support levels |
| Small-cap meme (PAID, ~$27M) | ±15% | **−20% in 6h** · liquidity drop >25% vs last check · mcap band (<$18M / >$45M) |

The liquidity-drop rule is the important one for memecoins: LP-pull and dev-dump show up as liquidity
leaving *before* price fully reacts. For tokens where the LP is burned/blackholed, a liquidity collapse
means the pool is being drained by sellers, not rugged.

## Scheduled-event countdowns

Unlocks and dated catalysts are alertable conditions: ONDO's unlock cliff was wired as pings at
H−30/−14/−7/−3/−1. Do the same for any dated catalyst the position depends on.

## QA before declaring it live (all four, in order)

1. `--debug` → table renders, numbers sane
2. normal run with no trigger → **silent** (that is the whole point of the watchdog)
3. run twice → cooldown suppresses the duplicate
4. clear the state for one alert type → re-run → alert renders correctly (this is the only way to see
   the real message format before the user does)

## Digest job

Agent job (`enabled_toolsets: [terminal, web]`, `continuity: true`) that (a) runs the script in `--debug`
and quotes its numbers verbatim, (b) web-searches each asset for material news, (c) prints actions
**only** when an agreed level was hit. Put an explicit anti-fabrication line in the prompt ("kalau
tidak ada berita material, tulis 'nggak ada berita material' — jangan dipaksa atau dikarang") and
require the agent to flag rows where the script reported a data-fetch failure.

Verification habit that paid off: after the test run, spot-check the digest's news claims against
primary sources before repeating them to the user. One check turned a vague mention into a dated,
verifiable catalyst (Hyperliquid AQAv2 payout) and one small error was caught (token age off by a day).
