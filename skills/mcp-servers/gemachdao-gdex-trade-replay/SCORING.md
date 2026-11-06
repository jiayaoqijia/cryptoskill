# Practice challenges: schema and scoring

This spec is for agents and developers who want to build challenges that existing players
can run. The source of truth is `mcp-server/src/practice/` (`scenarios.ts`, `runner.ts`,
`capsule.ts`). Golden outputs are in `mcp-server/tests/practice.test.ts`.

## Capsule (`GDEX-CHALLENGE:` + base64url(JSON), ≤ 600 chars)

```json
{
  "v": 1,
  "kind": "gdex.practice.challenge",
  "scenario": "eth-short-target-vs-stop-01",
  "rules": "practice-rules/1",
  "source": "practice_fixture | practice_fixture_inspired_by_trade",
  "senderPlan": { "targetPct": "3.0", "stopPct": "2.0" },
  "invite": "<20-char base58 GDEX refCode>"
}
```

The capsule is a strict allow-list:

- `senderPlan` and `invite` are optional, and present only when the sender chose to add them.
- Any other field is rejected, which rules out commands, URLs, bars, wallets and anything else.
- An unknown `scenario`, an unsupported `v` or an unsupported `rules` value fails with an
  "update the skill" message.
- `senderPlan` is validated against the scenario bounds.
- `invite` must be 8–32 base58 characters.
- Decoding reads only the capsule token. Any surrounding text is ignored and never executed.

## Scenario (`gdex.practice.scenario/1`)

| Field | Meaning |
|---|---|
| `id`, `family` | Stable id. Family: `short-target-vs-stop` or `long-target-vs-stop`. |
| `instrument` | Label, venue model (`hyperliquid-perp`), bar interval. |
| `source` | Always `synthetic_fixture` in this release, with a human label. |
| `side` | `long` or `short`. |
| `account` | Practice equity (USD) and leverage. Notional = equity × leverage. |
| `rules` | `practice-rules/1`: risk limit % of equity; min/max stop % and target %. |
| `costModel` | `hl-taker-cost/1`: fee bps per side, slippage bps per side, funding not modeled. |
| `baseline` | The fixed plan every challenger is compared against. |
| `setup` | Bars shown before the decision. |
| `tape` | Bars revealed only after submit. `tape[0].o` is the reference/entry price. |

Shipped scenarios:

| id | Account | Risk limit | Baseline (target / stop) | Bars |
|---|---|---|---|---|
| `eth-short-target-vs-stop-01` | $1,000 at 3x | 8% | 3.0% / 2.0% | 12 setup + 24 tape |
| `btc-long-target-vs-stop-01` | $1,000 at 3x | 8% | 3.0% / 2.0% | 12 setup + 24 tape |

The BTC tape is the ETH tape reflected around its entry, rescaled and rounded to 0.1, so
both fixtures have the same geometry.

## Decision

A decision is `{ targetPct, stopPct }`. Each value is a decimal string with at most 2
decimals, within the scenario bounds; nothing else is accepted. It is validated before
anything is scored.

## Scoring (`practice-rules/1`, `hl-taker-cost/1`)

All arithmetic is exact (bigint, 18 decimals). Rounding happens only at output, half away
from zero. The same scenario, decision and rules version give the same output on any host.

1. **Reference price:** E = `tape[0].o`.
   - Short: target = E·(1 − t), stop = E·(1 + s).
   - Long: target = E·(1 + t), stop = E·(1 − s).
2. **Entry:** fills at E with slippage against the trader. Size = notional / entry fill.
3. **Each bar, in order:**
   1. From the 2nd bar on, if the open is already beyond the stop (or target), exit at the
      open. This is `gap_stop` / `gap_target`; a gap stop can lose more than planned.
   2. If the bar's range touches **both** stop and target, bars cannot show which came first.
      The **stop is taken first** (`stop_ambiguous_same_bar`, flagged `ambiguous`).
   3. Otherwise, the level that was touched exits at that level (`stop` / `target`).
4. **No exit:** `time_exit` at the last bar's close.
5. **Exit slippage:** every exit fills with slippage against the trader.
6. **Fees:** `feeBpsPerSide` on entry notional plus exit notional. The cost model assumes
   9.5 bps = Hyperliquid base taker 4.5 bps + GDEX builder fee 5 bps.
7. **Net:** gross − fees. Funding is not modeled.
8. **Max drawdown:** the worst adverse price while the position is open, valued as a loss
   including the entry fee, in USD and as % of equity.
   - On the exit bar, a stop caps the drawdown at the stop level.
   - Any other exit counts the whole exit bar, because the order inside the bar is unknown.
9. **Breaches** (reported, never hidden):
   - The planned loss at the stop, including costs, is above the risk limit.
   - The realized loss is above the risk limit (for example after a gap).
10. **Comparison:** the player's plan, the baseline, and the sender's plan if present are
    shown side by side with exit, net, drawdown and breaches. Nothing is ranked by P&L alone;
    ties are just equal numbers.

## Golden cases (ETH short)

| Target / stop | Exit | Bar | Net USD | Max DD % | Breaches |
|---|---|---|---|---|---|
| 3.0 / 2.0 (baseline) | target | 9 | 83.22 | 6.18 | 0 |
| 3.0 / 0.9 | stop | 1 | −33.94 | 3.05 | 0 |
| 3.0 / 1.2 | stop | 2 | −42.95 | 3.95 | 0 |
| 2.5 / 1.8 | stop (same-bar ambiguity) | 7 | −60.97 | 5.75 | 0 |
| 5 / 2.2 | gap stop | 11 | −83.90 | 8.04 | 1 (realized) |
| 6 / 4 | time exit | 23 | −81.42 | 11.13 | 2 |
| 3.0 / 5 | target | 9 | 83.22 | 6.18 | 1 (planned) |

## Building a compatible challenge

- Add a new scenario with a **new id**. Never change a shipped tape: old capsules must keep
  scoring the same way.
- Any change to scoring semantics needs a new `rules` version; keep the old one runnable.
  The same goes for a new cost model version.
- Add golden cases for target, stop, same-bar ambiguity, gap, drawdown and no-exit.
- A real historical tape needs verified data rights, availability and time alignment, and
  a `historical_simulation` source label. If the tape could reveal when the original trade
  happened, it needs explicit preview and approval. Never fill gaps with invented candles.
  That is not in this release.
