---
name: multiples
domain: investing/multiples
trigger: "Using comparable multiples without hiding the assumptions inside them."
anti_trigger: "Not for building a DCF, and not for choosing a peer set to flatter a result."
scope: "Peer selection, multiple choice, and why every multiple embeds a set of assumptions."
status: seedling
---

# Multiples

## Standard

A multiple is a compressed DCF. Price-to-earnings of twenty says the market expects earnings to grow at a rate that justifies paying twenty times today's number; enterprise-value-to-EBITDA says something about capital structure and depreciation; price-to-sales says the market is paying for growth before profitability. Using a multiple without knowing which assumption it embeds is using a conclusion without its premise.

The peer set is the whole analysis. A multiple compared against the wrong companies is a number without meaning, and a peer set chosen after seeing the answer is not analysis at all.

Primary sources: <https://pages.stern.nyu.edu/~adamodar/> and <https://www.sec.gov/edgar/search/>.

## Decision rules

- The peer set is defined by business model, end market, and margin structure — not by market capitalisation alone.
- Each multiple is stated with the metric definition: trailing or forward, adjusted or reported, enterprise or equity.
- Enterprise multiples are used with enterprise-value metrics; equity multiples with equity metrics; never mixed.
- A multiple that differs materially from peers requires an explanation in growth, margin, or risk.
- Negative or near-zero denominators disqualify the multiple; record the disqualification rather than inventing an alternative.
- Peer multiples are recorded with their own dates and market conditions.

## Procedure

1. Define the peer set with the three criteria and record the exclusions.
2. Choose two multiples that fit the business model and explain the choice.
3. Compute the peer median and range on consistent definitions.
4. Compute the subject company's multiples on the same definitions.
5. Explain the difference, or record that it is unexplained.
6. Record dates and market conditions for all inputs.

## Anti-patterns

- Comparing across industries because the companies are large.
- Mixing enterprise and equity multiples in one comparison.
- Using a forward multiple for peers and a trailing one for the subject.
- Choosing the peer set after computing the multiple.
- Treating a low multiple as cheap without asking what assumption it embeds.

## Done checklist

- [ ] Peer set defined with criteria and exclusions.
- [ ] Two multiples chosen and justified.
- [ ] Peer median and range computed on consistent definitions.
- [ ] Subject multiples computed on the same definitions.
- [ ] Differences explained or recorded as unexplained.
- [ ] Dates and market conditions recorded.

## Sources

- Multiples data and reference material: <https://pages.stern.nyu.edu/~adamodar/>
- Full-text filing search for peer metrics: <https://www.sec.gov/edgar/search/>
- Investor education on comparative analysis: <https://www.investor.gov/introduction-investing>
