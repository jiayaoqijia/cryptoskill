<!-- INTERNAL WORKPAPER — not the user-facing deliverable. Keep this file; deliver a report template. The checklist at the end stays here. -->

# Investment Workpaper — {{asset_or_project}}

**As of (UTC):** {{date_time}} · **Retrieval window:** {{first–last retrieval}}
**Decision lens:** {{screen | compare | value | timing | hold/exit}}
**Horizon / benchmark / numeraire:** {{explicit values or labelled assumptions}}
**Current price:** {{value, price type, venue, timestamp, provider}}
**Investability gate:** {{pass | conditional | fail | insufficient evidence}} — {{which component decided it}}
**Coverage:** {{what was checked, what was not, and why}}

## 1. Asset and instrument map

- Entity/issuer, jurisdiction, legal wrapper:
- Asset class, sector, cycle/life-cycle stage:
- Instrument and rights (token standard, share class, fund unit, bond terms):
- Chain + chain ID + contract address(es) + proxy/implementation:
- Venues and quote assets:
- Peers selected and why:

## 2. Decision frame and suitability

- Decision requested, horizon, benchmark, numeraire:
- User constraints: horizon, tolerable drawdown, liquidity needs, liability currency, jurisdiction/eligibility, existing concentration:
- If absent: `suitability not assessable — requires <inputs>`:
- Behavioral/ownership bias: anchoring, sunk-cost, confirmation, recency, loss aversion; no inferred position size:

## 3. Claims converted into test questions

| Issuer/promotional claim | Testable question | Evidence that would confirm | Evidence that would refute |
|---|---|---|---|

## 4. Evidence ledger

| ID | Claim / metric | Type (fact, issuer claim, estimate, inference) | Value, unit, date | Source, independence, retrieval date | Status / caveat |
|---|---|---|---|---|---|
| K1 | | | | | |

Crypto state claims also record: chain, contract address, function/selector, block, RPC.

## 5. Data conflicts and freshness

| Metric | Source A | Source B | Difference | Chosen basis | Why |
|---|---|---|---|---|---|

## 6. Business and product

{{Customer problem, product, usage, pricing, distribution, revenue model, cost structure, moat. Evidence: traffic, uptime, customers, contracts.}}

## 7. Market and competition

{{Bottom-up market size, structure, 3–5 peers, share, price/latency/uptime/coverage, moat, fork/price-war risk.}}

## 8. Demand and revenue quality

{{Paid vs incentive-farmed, external vs internal, concentration, retention, prepaid/committed vs spot, refund risk.}}

## 9. Unit economics

| Segment | Revenue/unit | Cost/unit | Gross margin | CAC/payback | Note |
|---|---:|---:|---:|---:|---|

{{Revenue bridge: activity → paid activity → gross revenue → incentives → net revenue → gross profit. Miner/validator ROI if relevant. Stress tests.}}

## 10. Team, organization and governance

{{Founders, critical roles, verified track record, key-person, retention/incentives, ownership, board, succession, disclosure.}}

## 11. Funding, cap table and related parties

| Round / holder | Amount / share | Valuation / price | Date | Dilution / rights | Note |
|---|---:|---:|---|---|---|

{{Runway/burn, related entities, conflicts, insider allocation/vesting.}}

## 12. Supply bridge (tokens)

| Basis | Value | Definition used | Source | Date | Difference vs on-chain `totalSupply` explained |
|---|---|---|---|---|---|
| Max | | | | | |
| Total | | | | | |
| Circulating (issuer) | | | | | |
| Circulating (aggregator) | | | | | |
| Effective float | | | | | |
| Treasury-held | | | | | |
| Locked / vesting | | | | | |
| Unclaimed emissions | | | | | |

Market-cap basis: {{…}} · FDV basis: {{…}} · Why the two differ: {{…}}

## 13. Unlocks, emissions and burns

| Month | Tokens unlocking / emitted | % of current float | % of 30-day volume | Cumulative % of float | Beneficiary class | Source |
|---|---|---|---|---|---|---|

{{Burn/buyback funding source; net inflation; emission split.}}

## 14. Rights ladder and value capture

| Claimed right | Rung (1–7) | Implemented in code? | Function / state | Funding source | Enforceability |
|---|---|---|---|---|---|

## 15. Holder concentration and cohorts

| Holder / cohort | Share | Label | Locked/unlocked | Source | Basis |
|---|---:|---|---|---|---|

## 16. Staking, validator and miner flows

{{Net stake/unstake, staking ratio, APR, validator count/top share/take, root cut, miner count/top share/payback.}}

## 17. Protocol and treasury flows

| Period | Protocol buys | Root sells | User net | Cross-subnet | Net price change | Source |
|---|---:|---:|---:|---:|---:|---|

{{Treasury composition/runway; who can move funds; funding source of buybacks.}}

## 18. Governance and control

{{On-chain vs signaling, quorum, turnout, timelock, emergency powers, owner hotkey/multisig, upgrade authority, conviction/takeover.}}

## 19. Technical and market-structure dashboard

| Metric | Value | Read |
|---|---|---|
| Trend / MA20/50/200 | | |
| Relative strength vs benchmark 7/30/90/130d | | |
| RSI/MACD/ROC | | |
| Volatility / max drawdown | | |
| ADV / volume-to-market-cap | | |
| Depth ±2% / slippage at size | | |
| Funding / OI / basis (if perp) | | |
| Beta/correlation vs benchmark | | |

Validation status: {{descriptive only — no validated edge / backtest protocol and trade count}}.

## 20. Liquidity and exit

Exit at {{size}} USD / {{token units}}: venues {{…}}, snapshot {{UTC}}, participation {{% ADV}} and {{% book depth}}, days to exit {{…}}, all-in round-trip cost {{bps}}, withdrawal/off-ramp {{…}}, locked/vesting {{no executable exit before …}}.

## 21. Community, news and sentiment

| Channel | Metric | Value | Date | Read |
|---|---|---|---|---|
| X | followers / engagement | | | |
| Discord/Telegram | members / online / velocity | | | |
| GitHub | stars/forks/issues/contributors/commits | | | |
| Governance | proposals/turnout/quorum | | | |
| News | tier-1/trade/project, tone, independent confirmations | | | |

Social/news are signals, not evidence; label `verified` / `company claim` / `media` / `social`.

## 22. Catalyst calendar

| Date | Event | Status | Why it matters | Source | Monitor |
|---|---|---|---|---|---|

## 23. Legal and regulatory

{{Issuer/jurisdiction, token classification, MiCA/other, KYC/AML, sanctions, transfer restrictions, tax, venue eligibility. Not legal advice.}}

## 24. Security, audits and incidents

| Firm / contest | Date | Audited commit | In scope | Out of scope | Critical/high | Remediation | Re-audit | Bounty |
|---|---|---|---|---|---|---|---|---|

| Ability | Function | Holder type | Threshold | Timelock | Renounced? | Evidence |
|---|---|---|---|---|---|---|

| Date | Mechanism | Loss | Recovery | Root cause | Fix verified | Recurred? | Post-mortem |
|---|---|---|---|---|---|---|---|

## 25. Valuation bridge

- Methods selected and rejected, with reasons:
- Assumptions, discount rate, terminal value, dilution/debt/cash:
- Float-basis value: {{…}} · FDV-basis value: {{…}}
- Reverse valuation — what the current price implies:
- Total return: `(P1×Q1 + distributions − fees − tax)/(P0×Q0) − 1`, with Q0/Q1 defined:
- Yield split: emission-funded {{…}} / fee-funded {{…}}
- Sensitivity table:

## 26. Scenarios and expected return

| Driver | Bear | Base | Bull | Thesis-break | Upside |
|---|---|---|---|---|---|
| Revenue / volume | | | | | |
| Gross margin / take rate | | | | | |
| Emission / dilution | | | | | |
| Multiple / exit anchor | | | | | |
| Per-token value | | | | | |
| Total return | | | | | |
| Probability (judgmental) | | | | | |

E[R] = Σ p_i × R_i; probabilities sum to 100%; label judgmental.

## 27. Risk matrix and stress tests

| Risk | Likelihood | Impact | Evidence | Loss floor / mechanism | Monitor |
|---|---|---|---|---|---|

| Shock | Impact | Result |
|---|---|---|
| Revenue −50% | | |
| Benchmark −30% | | |
| Emissions +20% | | |
| Liquidity −50% | | |
| Exploit/key compromise | | |

## 28. Red team, falsification and monitoring

| Thesis condition / metric | Threshold or event | Source | Check date / frequency | Effect on conclusion |
|---|---|---|---|---|

{{Pre-mortem; strongest counter-thesis; what would change the conclusion.}}

## 29. Unknowns and verification limits

{{Unverified claims, missing data, source conflicts, access limits, and how each would change the conclusion. Separate gate-relevant unknowns from confidence-reducing ones.}}

## 30. Sources

{{Full list with title, URL, publication/effective date and retrieval date. No discovery snippet cited as if the page was read.}}

## 31. Lens coverage matrix

| Lens | Covered? | Key finding | Evidence | Confidence |
|---|---|---|---|---|
| Decision/suitability | | | | |
| Business/product | | | | |
| Market/competition | | | | |
| Demand/revenue/unit economics | | | | |
| Team/org | | | | |
| Instrument rights | | | | |
| Token economics | | | | |
| Ownership/flows/control | | | | |
| Technical/market structure | | | | |
| Community/news/catalysts | | | | |
| Legal/security | | | | |
| Valuation | | | | |
| Risk/portfolio | | | | |
| Decision/monitoring | | | | |

## 32. Completeness and delivery check

- [ ] Every lens covered or marked not material/not assessable with a reason.
- [ ] Investability gate stated; failure not offset by score, narrative, community or technical signal.
- [ ] Critical unknown handled as `insufficient evidence`, not `conditional`.
- [ ] Supply basis reconciled and labelled wherever market cap or FDV appears.
- [ ] Unlock/emission overhang measured against float and volume.
- [ ] Privileged control mapped; audit scope bound to the deployed commit; incidents reviewed.
- [ ] Rights and value capture located in code or labelled documents-only; burn/buyback funding source stated.
- [ ] Demand quality separates paid from incentive-farmed/internal activity; TVL double-counting stated.
- [ ] Unit economics and customer concentration addressed or marked unknown.
- [ ] Technical dashboard and liquidity/exit at stated size included; no validated edge claimed.
- [ ] Community/news labelled as signal, not evidence; catalyst calendar dated.
- [ ] Legal/regulatory/security addressed or marked not assessed with jurisdiction.
- [ ] Valuation bridge/scenarios/expected return present; no DCF for no-cash-flow tokens.
- [ ] Risk matrix/stress tests/pre-mortem present.
- [ ] Report language, mode, length and PDF production match the contract; no internal checklist or placeholder in the delivered file.
