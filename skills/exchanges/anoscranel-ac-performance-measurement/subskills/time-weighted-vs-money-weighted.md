---
name: time-weighted-vs-money-weighted
domain: investing/time-weighted-vs-money-weighted
trigger: "Choosing which return to compute and what it is measuring."
anti_trigger: "Not for predicting returns, and not for tax reporting."
scope: "Two correct returns that answer different questions."
status: seedling
---

# Time-weighted versus money-weighted

## Standard

A time-weighted return removes the effect of cash flows by computing the return of each sub-period and linking them geometrically. It measures the strategy: how a unit of capital performed while it was invested, regardless of how much was added or withdrawn. A money-weighted return, by contrast, is the internal rate of return on the actual cash flows, and it measures the investor's experience, including the effect of having more money invested during the good periods and less during the bad.

The two can diverge sharply, and the divergence is informative. An investor who added heavily before a rise and withdrew before a fall has a money-weighted return above the time-weighted one, because their timing helped. The reverse is the common case: money arrives after good performance and leaves after bad, so the money-weighted return trails. Reporting only the higher number is the most common form of flattering a result.

Primary sources: <https://www.cfainstitute.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record which return is being reported and why that one answers the question.
- Compute the time-weighted return by linking sub-period returns at each cash flow.
- Compute the money-weighted return from the dated cash flows.
- Record the difference between them and what it implies about flow timing.
- Record the cash flows used, with dates and amounts.
- Never present one as if it were the other.

## Procedure

1. Collect the valuation series and every external cash flow with its date.
2. Split the period at each cash flow and compute sub-period returns.
3. Link the sub-periods geometrically for the time-weighted return.
4. Solve for the rate that equates the cash flows to the ending value.
5. Record both figures and the gap between them.
6. State which is being used for which purpose.

## Anti-patterns

- Reporting the money-weighted return as the strategy's result.
- Using time-weighted returns to describe an investor's outcome.
- Ignoring flow timing when comparing two periods.
- Computing either without the cash flow dates.
- Presenting a single figure with no statement of type.

## Done checklist

- [ ] Return type stated.
- [ ] Time-weighted return computed.
- [ ] Money-weighted return computed.
- [ ] Gap recorded with an interpretation.
- [ ] Cash flows recorded with dates.
- [ ] Purpose of each stated.

The gap is also a diagnostic of the decision process: an investor whose money-weighted return consistently trails the time-weighted one is buying after good periods and selling after bad, which is a behavioural finding about the flows rather than about the portfolio, and recording the gap per period makes the pattern visible before it compounds.


## Sources

- Investment performance standards: <https://www.cfainstitute.org/>
- Investor education on measuring returns: <https://www.investor.gov/introduction-investing>
- Market data for benchmarks: <https://fred.stlouisfed.org/>
