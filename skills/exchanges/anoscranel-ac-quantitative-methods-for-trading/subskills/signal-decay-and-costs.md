---
name: signal-decay-and-costs
domain: crypto-trading/signal-decay-and-costs
trigger: "Deciding whether a signal survives its own decay and costs."
anti_trigger: "Not for predicting a signal's returns, and not for venue fee schedules."
scope: "Half-life, capacity, and the cost line a signal must clear."
status: seedling
---

# Signal decay and costs

## Standard

A signal's information edge, if it exists, decays: others find it, the environment shifts, or the anomaly was a window's accident. Decay is measured, not assumed — the same rule measured on later data and compared with earlier data states it honestly. The half-life, the period over which the measured edge halves, is the number that converts a backtest's gross number into something a live trader must defend against.

Costs are the other half of the verdict. Spread, fees, impact, and short-rate financing subtract from every round trip, and a signal whose gross persistence is smaller than its cost line is not a weak signal but an untradeable one. The honest comparison is gross persistence after costs, measured with the venue's actual fee schedule and the book's actual spread, and stated for the intended size rather than a frictionless share.

Primary sources: <https://quant.stackexchange.com/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Measure the signal's decay by re-estimating on later windows and recording the decline.
- Record the half-life estimate and the window it was measured on.
- Compute the full cost per round trip at the intended size, not at a minimum unit.
- Compare gross persistence with the cost line and state the margin.
- Record the capacity question: what size begins to move the entry and exit?
- State the falsifier: the decay level at which the signal is retired.

## Procedure

1. Re-estimate the rule on windows after the original sample.
2. Record the measured decline and the half-life.
3. Compute cost per round trip at intended size: spread, fees, impact.
4. Compare persistence with the cost line; record the margin.
5. Note the size at which impact measurably rises.
6. Write the retirement threshold into the record.

## Anti-patterns

- Presenting a gross backtest number without the cost line.
- Assuming the edge persists because it was published.
- Measuring costs at a size the strategy will never trade.
- Treating decay as noise rather than as the primary finding.
- No retirement threshold, so the signal is held past its evidence.

## Done checklist

- [ ] Decay measured across dated windows.
- [ ] Half-life recorded.
- [ ] Round-trip cost at intended size computed.
- [ ] Persistence compared with the cost line.
- [ ] Capacity estimate noted.
- [ ] Retirement threshold written.

## Sources

- Signal decay and transaction cost discussion: <https://quant.stackexchange.com/>
- Investor education on costs: <https://www.investor.gov/introduction-investing>
- Cost and fee context: <https://www.finra.org/>
