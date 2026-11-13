---
name: decumulation-arithmetic
domain: investing/decumulation-arithmetic
trigger: "Working the arithmetic that connects a withdrawal rate to portfolio longevity."
anti_trigger: "Not for predicting returns, and not for personal advice."
scope: "Withdrawal rates, portfolio longevity, and the arithmetic that connects spending to horizon."
status: seedling
---

# Decumulation arithmetic

## Standard

The arithmetic is simple and the conclusions are not. A withdrawal rate is the annual amount spent divided by the portfolio value; the portfolio's longevity depends on the return earned, the inflation applied to spending, and the sequence in which returns arrive. Two portfolios with the same average return can have different lifetimes because of order alone.

The useful exercise is not to find a single safe rate but to see the sensitivity. A withdrawal rate that works at a five percent real return with twenty-five years of horizon fails badly at a two percent return, and the honest record states the range rather than a point. An assumed return above what a balanced portfolio has historically produced is not a plan; it is a hope with a spreadsheet.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://www.irs.gov/>.

## Decision rules

- State the withdrawal rate, the assumed real return, the inflation assumption, and the horizon, all four.
- Compute longevity across a range of returns, not a single estimate.
- Express spending in real terms so inflation is handled explicitly.
- Treat any assumed return above the portfolio's long-run evidence as a flagged assumption.
- Include a stress case with a poor first decade.
- Record every assumption with its source or its status as a judgement.

## Procedure

1. Record portfolio value, planned annual spending, and the resulting withdrawal rate.
2. Set a real return range and an inflation assumption with sources.
3. Project longevity at each point in the range.
4. Add a stress case with poor early returns.
5. Identify the assumptions to which the answer is most sensitive.
6. Write the findings with the range and the sensitivities.

## Anti-patterns

- Quoting a safe withdrawal rate as universal.
- Assuming returns that exceed the portfolio's own evidence.
- Ignoring inflation by projecting nominal spending.
- Presenting one projection as the answer.
- Using a long horizon without a stress case.

## Done checklist

- [ ] Withdrawal rate computed and stated.
- [ ] Real return range and inflation assumption recorded.
- [ ] Longevity projected across the range.
- [ ] Stress case included.
- [ ] Sensitive assumptions identified.
- [ ] Findings written with range and sensitivities.

## Sources

- Investor education on retirement income: <https://www.investor.gov/introduction-investing>
- Tax and account context: <https://www.irs.gov/>
- Inflation data: <https://fred.stlouisfed.org/>

The arithmetic also exposes a useful asymmetry: reducing spending by a small percentage extends the portfolio's life by more than the same percentage applied to returns, because spending is the controllable variable. A record that shows both sensitivities lets the reader see which lever actually moves the outcome.
