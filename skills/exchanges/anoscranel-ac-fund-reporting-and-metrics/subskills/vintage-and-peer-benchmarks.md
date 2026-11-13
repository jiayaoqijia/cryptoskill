---
name: vintage-and-peer-benchmarks
domain: investing/vintage-and-peer-benchmarks
trigger: "Choosing a comparison that does not flatter the fund."
anti_trigger: "Not for predicting which vintage will be best, and not for constructing a benchmark product."
scope: "Vintage year, peer universe selection, and the comparison that is fair."
status: seedling
---

# Vintage and peer benchmarks

## Standard

A vintage year groups funds by the year they began investing, and it exists because market conditions at deployment dominate early performance. A fund that deployed in a boom looks different from one that deployed into a correction, and comparing them on return is comparing two different environments. Vintage matching is the minimum condition for a fair comparison.

The second condition is universe selection. Peer universes are assembled by data providers from funds that choose to report, which introduces survivorship and self-selection: the funds that stop reporting are usually the ones that did badly. A universe assembled by the manager, or filtered by minimum size, is a marketing document rather than a benchmark, and the record should state who assembled it and which funds are in it.

Primary sources: <https://www.cfainstitute.org/> and <https://www.nber.org/>.

## Decision rules

- Record the fund's vintage year and the definition used.
- Record the peer universe, its provider, and its inclusion criteria.
- Record the percentile and the number of funds in the comparison.
- Record whether the universe includes funds that stopped reporting.
- Record the strategy and geography filters applied.
- Where the comparison is manager-selected, record that rather than treating it as independent.

## Procedure

1. Record vintage and the deployment period.
2. Identify the peer universe and its source.
3. Record inclusion criteria and the fund count.
4. Record the percentile and its date.
5. Check for survivorship in the universe.
6. Write the comparison with its provenance.

## Anti-patterns

- Comparing funds across vintages without adjustment.
- Accepting a universe whose composition is not disclosed.
- Ignoring survivorship bias in a self-reported universe.
- Treating a percentile as a measure of skill.
- Using a universe filtered to funds of similar size as if it were the whole market.

## Done checklist

- [ ] Vintage recorded.
- [ ] Universe and provider recorded.
- [ ] Inclusion criteria recorded.
- [ ] Fund count recorded.
- [ ] Survivorship checked.
- [ ] Comparison provenance written.

A further filter to check is whether the universe includes funds that are still raising: a peer set drawn only from closed funds omits the ones that failed to raise a successor, which is a survivorship effect that no amount of vintage matching corrects, and the provider's methodology note is the only place it appears.

## Sources

- Investment performance standards: <https://www.cfainstitute.org/>
- Research on private markets: <https://www.nber.org/>
- Fund disclosure context: <https://www.sec.gov/investor>
