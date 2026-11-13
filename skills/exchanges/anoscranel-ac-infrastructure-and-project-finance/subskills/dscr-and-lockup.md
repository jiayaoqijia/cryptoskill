---
name: dscr-and-lockup
domain: investing/dscr-and-lockup
trigger: "Computing coverage ratios and the cash trap a lock-up creates."
anti_trigger: "Not for predicting a project's cash flow, and not for legal advice."
scope: "Coverage ratios, lock-up tests, and the cash trap they create."
status: seedling
---

# DSCR and lock-up

## Standard

Debt service coverage is cash flow available for debt service divided by the debt service due, and it is the ratio on which project debt is sized and monitored. A lock-up test is a higher threshold on the same ratio: when coverage falls below it, cash that would have been distributed to equity is trapped in a reserve account until coverage recovers.

The lock-up is the mechanism that converts a temporary shortfall into an equity problem. The project may still be paying its debt on time, but the equity distribution stops, and an equity investor relying on that distribution faces a liquidity event without any default having occurred. That is why the distance between the lock-up level and the covenant level belongs in the analysis as much as the current ratio does.

Primary sources: <https://www.worldbank.org/> and <https://www.eib.org/>.

## Decision rules

- Record the DSCR definition, including which cash flows are included and which are reserved.
- Record the lock-up threshold and the default threshold separately.
- Compute the current DSCR and the headroom to each threshold.
- Record the historic DSCR range, including the worst year.
- Record the cash trap mechanics and how the trapped cash is released.
- Record any equity cure right that allows a shortfall to be remedied.

## Procedure

1. Read the financing documents for the definitions.
2. Record the thresholds and the definitions behind them.
3. Compute the current ratio and the headroom.
4. Record the historic range.
5. Record the cash trap and release mechanics.
6. Write the analysis with the distance to lock-up stated.

## Anti-patterns

- Using a headline DSCR that excludes reserved amounts.
- Treating lock-up and default as the same threshold.
- Ignoring the historic range, which shows how close the project has come before.
- Assuming trapped cash is lost rather than deferred.
- Overlooking equity cure rights that change the breach path.

## Done checklist

- [ ] DSCR definition recorded.
- [ ] Lock-up and default thresholds recorded.
- [ ] Current ratio and headroom computed.
- [ ] Historic range recorded.
- [ ] Cash trap mechanics recorded.
- [ ] Cure rights recorded.

The definition of cash flow available for debt service is where the analysis is won or lost: a definition that permits additions to a reserve, or that excludes a maintenance allowance, shows a higher ratio than one that does not, and two projects with the same headline coverage can have very different real headroom. The definition belongs in the record, not in a footnote.


## Sources

- Project finance documentation guidance: <https://www.worldbank.org/>
- Infrastructure debt standards: <https://www.eib.org/>
- Investor education on coverage ratios: <https://www.investor.gov/introduction-investing>
