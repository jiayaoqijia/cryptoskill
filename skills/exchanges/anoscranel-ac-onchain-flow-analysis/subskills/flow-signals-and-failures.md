---
name: flow-signals-and-failures
domain: crypto-trading/flow-signals-and-failures
trigger: "Separating flow signals that have evidence from the folklore around them."
anti_trigger: "Not for building a trading strategy, and not for backtesting."
scope: "Which flow signals have evidence versus folklore, and the false positives that retire naive rules."
status: seedling
---

# Flow signals and failures

## Standard

Flow-based signals are popular because they are computable and vivid. The evidence for them is thinner than their popularity suggests. Some have a defensible mechanism and some measured support: venue-level stress shows up in flows during cascades, and cohort changes describe concentration. Others are folklore with a plausible story and no measurement behind them.

The honest treatment is to classify each signal as evidenced, plausible-but-unmeasured, or retired, and to record the specific false positive that makes the distinction. A rule that cannot name its own failure mode has not been tested; it has been believed.

Primary sources: <https://arxiv.org/abs/2608.03616> and <https://ethereum.org/en/developers/docs/>.

## Decision rules

- Each signal is classified: evidenced, plausible-unmeasured, or retired, with the basis recorded.
- A retired signal keeps its retirement reason, so it is not reintroduced later.
- False positives are named: custody rotation, market-maker inventory, OTC settlement, exchange migration.
- Any signal used in a memo carries its classification and its last measurement date.
- Signals that require labels inherit the label's uncertainty.
- No signal is presented as predictive without a stated test and window.

## Procedure

1. List the flow signals in use.
2. For each, find the strongest available evidence, or record that none exists.
3. Name the false positives that would produce the signal without the claimed cause.
4. Classify each signal.
5. Record the classification with the date and the source.
6. Retire the ones that fail, with the reason retained.

## Anti-patterns

- Repeating a flow rule because a chart once looked convincing.
- Treating a mechanism story as evidence.
- Reintroducing a retired signal without new measurement.
- Using a signal in a memo without its classification.
- Ignoring the false positive that the signal cannot distinguish.

## Done checklist

- [ ] Signals listed.
- [ ] Evidence found or absence recorded per signal.
- [ ] False positives named per signal.
- [ ] Classification assigned.
- [ ] Classification dated and sourced.
- [ ] Retirements recorded with reasons.

## Sources

- Empirical measurement of liquidation and flow dynamics: <https://arxiv.org/abs/2608.03616>
- Ethereum developer documentation on ledger data: <https://ethereum.org/en/developers/docs/>
- Investor education on evidence and risk: <https://www.investor.gov/introduction-investing>

A signal that has been retired once should stay retired until someone produces a new measurement with a stated window and a stated test. The temptation to revive a familiar rule during a quiet week is exactly the failure mode this leaf exists to prevent, and the retirement note is the only thing that stops it.
