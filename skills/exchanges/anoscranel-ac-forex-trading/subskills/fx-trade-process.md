---
name: fx-trade-process
domain: investing/fx-trade-process
trigger: "Running a repeatable FX decision process rather than an improvised one."
anti_trigger: "Not for recommending a pair or a direction, and not for portfolio hedging."
scope: "The repeatable decision process: thesis, event calendar, sizing, invalidation."
status: seedling
---

# FX trade process

## Standard

An FX trade is a view on the relative price of two currencies, and the view is only useful if it is expressed in a form that can be falsified. The process starts with the thesis: what the trader believes about the two economies or the two policy paths, and what would have to happen for that belief to be wrong. Most FX losses attributable to process come from trades where no such statement was ever made.

The calendar is the second element. FX is driven by scheduled releases and unscheduled events, and a position that is right on the thesis can be stopped out by a single release it did not account for. Recording the releases due during the intended holding period, and deciding in advance whether to hold through them, converts an unpredictable sequence into a planned one.

Primary sources: <https://www.bis.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Every trade states the pair, the direction, the thesis, and the falsifier before entry.
- The scheduled events during the holding period are listed, with the decision to hold or flatten through each.
- Entry, stop, and target are recorded with the reasoning, not only the levels.
- Position size follows from the stop and the risk budget, not from conviction.
- The maximum holding period is stated, because carry costs accumulate and a thesis can expire.
- Trades are reviewed on the thesis, not on the profit and loss alone.

## Procedure

1. Write the thesis in two sentences and the falsifier in one.
2. List the scheduled events during the intended holding period.
3. Decide the treatment of each event before entry.
4. Set entry, stop, and target with the reasoning recorded.
5. Size the position from the stop and the risk budget.
6. Record the trade, then review it against the thesis at the stated horizon.

## Anti-patterns

- Entering because the chart looked ready, with the thesis written afterwards.
- Ignoring the calendar and being stopped by a release.
- Sizing from conviction rather than from the stop.
- Holding a trade whose thesis has been invalidated because the position is in profit.
- Reviewing only the outcome and not the reasoning.

## Done checklist

- [ ] Thesis and falsifier written before entry.
- [ ] Event calendar for the holding period listed.
- [ ] Event treatment decided.
- [ ] Levels recorded with reasoning.
- [ ] Size derived from stop and budget.
- [ ] Review against the thesis, not only the P&L.

## Sources

- Foreign exchange market context: <https://www.bis.org/>
- Economic releases and policy data: <https://www.federalreserve.gov/>
- Macro series used in the thesis: <https://fred.stlouisfed.org/>
