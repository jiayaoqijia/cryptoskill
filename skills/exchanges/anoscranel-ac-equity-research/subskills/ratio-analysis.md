---
name: ratio-analysis
domain: investing/ratio-analysis
trigger: "Computing and interpreting financial ratios with their comparability caveats."
anti_trigger: "Not for valuing a company, and not for comparing across industries without adjustment."
scope: "Margins, returns, leverage, and liquidity ratios, with the comparability and accounting caveats."
status: seedling
---

# Ratio analysis

## Standard

Ratios compress a statement into a comparison, and every compression loses information. Gross margin means something different for a software company and a retailer; return on equity is distorted by debt; a current ratio can flatter a company that cannot collect its receivables. The discipline is to compute ratios only after the accounting is understood, and to state the comparison group explicitly.

The useful ratios answer four questions: how profitable is the business per unit of sales, how efficiently it uses capital, how much debt it carries, and whether it can pay what it owes soon. Any ratio that does not map to one of those questions is decoration.

Primary sources: <https://pages.stern.nyu.edu/~adamodar/> and <https://www.sec.gov/edgar/search/>.

## Decision rules

- State the peer group before comparing; a ratio without a comparator is a number, not an analysis.
- Use the same accounting basis across the peer set, or record the differences.
- Return on equity is decomposed into margin, turnover, and leverage before it is interpreted.
- Leverage ratios use net debt, not gross, and say which was used.
- Liquidity ratios are read alongside receivables quality; a high current ratio with slow collections is a warning.
- Every ratio carries its period and its basis: average or ending balance.

## Procedure

1. Choose the four question groups and one or two ratios per group.
2. Compute each ratio from the verified statements, showing the inputs.
3. Decompose return on equity into its three components.
4. Select a peer group and compute the same ratios on the same basis.
5. Identify the ratios where the company differs materially and explain the difference.
6. Record every ratio with period, basis, and peer set.

## Anti-patterns

- Comparing margins across industries without adjustment.
- Reading a high return on equity without checking leverage.
- Using ending balances for ratios that need averages.
- Treating a single year as the trend.
- Choosing the peer group after seeing which comparison flatters.

## Done checklist

- [ ] Four question groups and chosen ratios stated.
- [ ] Each ratio computed with inputs shown.
- [ ] Return on equity decomposed.
- [ ] Peer group stated and computed consistently.
- [ ] Material differences explained.
- [ ] Period, basis, and peer set recorded per ratio.

## Sources

- Financial-data and ratio reference material: <https://pages.stern.nyu.edu/~adamodar/>
- Full-text filing search for source statements: <https://www.sec.gov/edgar/search/>
- Investor education on financial analysis: <https://www.investor.gov/introduction-investing>
