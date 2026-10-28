# Crypto Valuation — Business Value versus Token Value

Purpose: separate what the business is worth from what the token is worth. Most crypto mistakes come from valuing a token as if it were equity.

## First question: does the token have an enforceable claim?

Rights ladder:

1. Enforceable cash-flow claim (contractual dividend, revenue share, redeemable claim).
2. Active fee switch that distributes fees to holders.
3. Funded buyback/burn with a stated, verifiable funding source.
4. Voting only.
5. Points/airdrop expectation.
6. Wrapped/bridged claim on an issuer.
7. No economic claim.

- Rungs 1–3 may support cash-flow methods (DCF, dividend/FCFF, multiples), with caveats.
- Rungs 4–7 do not support a DCF. Use relative/network/scenario anchors and state `no enforceable cash-flow claim`.

## Valuation bridge

Revenue → gross profit → operating profit → taxes/NWC/capex → FCFF → discount → enterprise value → net debt → equity value → per share/token (only if the instrument has a claim).

For tokens without a claim, stop at: **business value is not accessible through the token**. Then value the token on demand/supply, staking yield, emission share, relative value and narrative.

## Supply basis

- Market cap = float × price; FDV = max supply × price. Put the basis beside every number.
- Reconcile max/total/circulating/effective float; unlock overlay; burns; emissions.
- Never compare one asset's float cap with another's FDV.
- State whether the valuation is pre- or post-dilution.

## Methods

- **DCF/FCF:** only with enforceable cash flow; explicit assumptions, discount rate, terminal value, dilution.
- **Multiples:** P/E, EV/EBITDA, P/S, P/F, FDV/revenue; define numerator, denominator and period; select peers for business similarity, not market cap.
- **Reverse valuation:** what revenue, growth, margin or emission share does the current price imply?
- **Relative:** market cap per emission point, P/F, FDV/revenue, liquidity-adjusted; state why the peer set is comparable.
- **Scenario/expected value:** bear/base/bull; same driver rows; per-token value; return; judgmental probabilities summing to 100%.
- **Sum-of-parts:** multi-segment businesses; state which segment carries the value.
- **Asset-based:** holding companies, REITs, treasury-heavy tokens; mark assets at realizable value.

## Scenario table

| Driver | Bear | Base | Bull | Evidence |
|---|---|---|---|---|
| Revenue / volume | | | | |
| Gross margin / take rate | | | | |
| Emissions / dilution | | | | |
| Multiple / exit anchor | | | | |
| Per-token value | | | | |
| Total return | | | | |
| Probability (judgmental) | | | | |

- Use the same driver rows across cases; add a thesis-break case distinct from downside.
- For power-law assets, require the upside case or state that omitting it truncates the distribution.

## Expected return

E[R] = Σ p_i × R_i, with probabilities summing to 100% and labelled judgmental unless a base rate and method are shown. Compare with the benchmark/hurdle on the same horizon, currency and net-of-fee basis.

Total return identity: `(P1×Q1 + distributions − fees − tax) / (P0×Q0) − 1`; define Q0/Q1; split yield into emission-funded and fee-funded parts. If only price return is computed, say so.

## Sources

- Market data, peer filings, DCF inputs, vesting contracts, emission data, FX.
- Record the basis (float/FDV), period and currency for every multiple.

## Report rules

- Give a range, not a single target. State whether the current price is above/below the base case and what that implies.
- State which method is primary and which are cross-checks.
- No DCF for governance-only tokens; no P/E for tokens without earnings.
- Label every multiple as a proxy when the token has no claim.
- If revenue is undisclosed, show a sensitivity table and say the valuation is a pricing framework, not a fair-value estimate.
