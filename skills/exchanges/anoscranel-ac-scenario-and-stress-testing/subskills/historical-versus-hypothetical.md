---
name: historical-versus-hypothetical
domain: investing/historical-versus-hypothetical
trigger: "Choosing between replaying a known episode and constructing a new one."
anti_trigger: "Not for predicting a repeat, and not for portfolio construction."
scope: "What a repeat of a known episode can and cannot tell you."
status: seedling
---

# Historical versus hypothetical

## Standard

A historical scenario replays the moves of a known episode across the portfolio's current holdings. Its strength is credibility: nobody can argue that the moves are impossible, because they happened. Its weakness is that the portfolio's current composition is not the one that experienced them, and the episode's correlations were specific to the assets and structures that existed then.

A hypothetical scenario constructs moves that have not occurred, which allows it to target the portfolio's own vulnerabilities. Its weakness is that credibility must be argued rather than demonstrated, and the argument is where the flattery or the alarmism enters. The two are complementary: history provides the severity and the correlation evidence, and the hypothetical applies them to conditions the portfolio actually faces.

Primary sources: <https://www.bis.org/> and <https://fred.stlouisfed.org/>.

## Decision rules

- For a historical scenario, record the episode, its dates, and the moves by asset class.
- Record how the portfolio's composition today differs from the composition then.
- For a hypothetical, record the construction logic and the source of each move.
- Record which correlations are taken from history and which are assumed.
- Record the scenario's severity against the historical distribution.
- Record what the scenario cannot test, given its construction.

## Procedure

1. Choose the episode or the construction logic.
2. Record the moves per asset class.
3. Note composition differences for a historical replay.
4. Record assumed versus observed correlations.
5. Place the scenario in the severity distribution.
6. Write the limits of what it tests.

## Anti-patterns

- Replaying a historical episode on a portfolio that did not exist then, without noting the difference.
- Constructing a hypothetical without stating where the moves come from.
- Assuming historical correlations applied throughout the episode.
- Treating a passed historical test as protection against a new scenario.
- Choosing severity to produce a preferred conclusion.

## Done checklist

- [ ] Episode or logic recorded.
- [ ] Moves recorded per asset class.
- [ ] Composition differences noted.
- [ ] Correlation sources recorded.
- [ ] Severity placed.
- [ ] Limits written.

The composition point deserves particular emphasis because it is where a replay misleads: a portfolio holding instruments that did not exist during the episode, or hedges that were not in place then, will produce a result that is neither a repeat nor a new scenario, and the record should state which of its components are replays and which are extrapolations.


## Sources

- Stress testing and financial stability work: <https://www.bis.org/>
- Historical market data series: <https://fred.stlouisfed.org/>
- Investor education on scenario analysis: <https://www.investor.gov/introduction-investing>
