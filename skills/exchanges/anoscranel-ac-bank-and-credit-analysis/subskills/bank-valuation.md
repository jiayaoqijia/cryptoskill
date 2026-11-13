---
name: bank-valuation
domain: investing/bank-valuation
trigger: "Valuing a bank through return on equity and price to book."
anti_trigger: "Not for non-bank companies, and not for predicting the share price."
scope: "Return on equity, price to book, and why earnings multiples mislead for a leveraged lender."
status: seedling
---

# Bank valuation

## Standard

A bank is valued through its equity, and the two numbers that matter are return on equity and the price paid for book value. The relationship is simple in form: a bank earning above its cost of equity should trade above book, one earning below should trade below, and the gap scales with the spread and its durability. Earnings multiples mislead because bank earnings include provisions that can be smoothed, and because leverage magnifies small changes in return on assets.

The useful question is not "is it cheap on book" but "what return on equity does this book sustainably earn, and what is that worth relative to the cost of capital". A bank trading at half of book is saying the market expects returns below cost, or losses that have not been recognised, or both.

Primary sources: <https://www.federalreserve.gov/> and <https://pages.stern.nyu.edu/~adamodar/>.

## Decision rules

- Start from sustainable return on equity, not from the latest quarter's earnings.
- Compute price to book and state the implied return expectation.
- Compare the implied return with the cost of equity estimated for the bank.
- Adjust book value for unrecognised losses where disclosure permits.
- Use earnings multiples only alongside book, never alone.
- Record the assumptions about the credit cycle that the valuation depends on.

## Procedure

1. Compute return on equity over a full cycle, not a single year.
2. Compute price to book at the current price.
3. Estimate the cost of equity and state its inputs.
4. Derive the return implied by the price-to-book ratio and compare.
5. Adjust book for unrecognised losses if the data allows.
6. Record the valuation with its cycle assumption.

## Anti-patterns

- Valuing a bank on a price-to-earnings multiple alone.
- Using peak-cycle return on equity as sustainable.
- Ignoring unrecognised credit losses in book value.
- Comparing price to book across banks with different loan books.
- Assuming the cost of equity from a single source without its date.

## Done checklist

- [ ] Cycle return on equity computed.
- [ ] Price to book computed.
- [ ] Cost of equity estimated with inputs stated.
- [ ] Implied return derived and compared.
- [ ] Book adjusted for unrecognised losses where possible.
- [ ] Cycle assumption recorded.

## Sources

- Federal Reserve bank data: <https://www.federalreserve.gov/>
- Valuation reference material and cost-of-capital data: <https://pages.stern.nyu.edu/~adamodar/>
- Investor education on bank shares: <https://www.investor.gov/introduction-investing>
