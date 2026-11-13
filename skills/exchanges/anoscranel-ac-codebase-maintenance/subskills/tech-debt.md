---
name: tech-debt
domain: software-engineering/tech-debt
trigger: "\"Where is our tech debt\", \"what should we fix first\", \"start a debt register\", \"we inherited this legacy code\", \"find the hotspots\", \"how big is this codebase\"."
anti_trigger: "Executing a refactoring recipe (subskills/refactoring.md); cutting complexity in one function (subskills/simplification.md); upgrading libraries (subskills/dependency-management.md)."
scope: "Debt register, interest-based priority, legacy-code entry, codebase metrics"
status: "seedling"
---

# Tech Debt

## Standard

- **Metaphor**: Ward Cunningham, 1992: a little debt speeds delivery if paid back promptly.
- **Technical Debt Quadrant** (Fowler, https://martinfowler.com/bliki/TechnicalDebtQuadrant.html): deliberate/inadvertent × reckless/prudent. It classifies origin, not repair.
- Manage debt as a ledger with explicit acceptance decisions (Kruchten et al., ICSE 2012).
- **Hotspots**: change frequency × complexity finds the costly code (CodeScene method). Change effort tracks churn and coupling (Nagappan & Ball, ICSE 2005).
- Developers undervalue future cost, so repayment must be scheduled (arXiv:1901.07024).
- ⚠️ Cost figures such as Stripe's ~33 % of time on debt are vendor-funded.

## Decision rules

1. Debt that matters is debt in code you change often. Cold code with high complexity can wait.
2. Priority score = interest (extra hours per month it costs) ÷ principal (hours to fix). Fix highest first.
3. Do not pay debt when the code is low-churn, slated for deletion, or when repayment costs more than the interest over its remaining life.
4. Every deliberate shortcut gets a register entry at the time it is taken.
5. Reserve a fixed share of each cycle for debt. ⚠️ The share (often 10–20 %) is practitioner convention, not a standard.
6. Legacy entry: understand before changing. Add tests at seams, then change (Feathers).
7. Metrics are trends inside one codebase, never targets.

## Procedure

1. Size the codebase: `scc` or `tokei` or `cloc.` for lines by language.
2. Find churn: 
   ```bash
   git log --since=12.months --name-only --format= | sort | uniq -c | sort -rn | head -30
   ```
3. Find complexity per file: `lizard -s cyclomatic_complexity src/` or `radon cc`.
4. Cross the two lists. Files high on both are hotspots.
5. Find knowledge risk: `git shortlog -sn -- <path>`. A hotspot with one author is bus-factor debt (target ≥3 people who know it; ⚠️ practitioner target).
6. Create or update `docs/debt.md`:
   ```markdown
   | ID | Where | What | Quadrant | Interest/mo | Principal | Score | Trigger to pay | Owner |
   ```
7. Score with rule 2. Pick the top items for the reserved share.
8. For each chosen item, plan the fix as refactoring steps under tests.
9. For legacy entry: run the app, read entry points, write characterization tests at the seams you will touch, then change.
10. Review the register each cycle. Close paid items. Delete items for deleted code.

## Anti-patterns

- "Rewrite it all" as the debt plan.
- Register with no interest estimate.
- Paying debt in cold code because it looks ugly.
- Debt work hidden inside feature PRs with no record.
- Complexity score used as a team target.

## Done checklist

- [ ] Hotspot list from churn × complexity.
- [ ] Register has interest, principal, score, trigger and owner per item.
- [ ] Top items scheduled in the reserved share.
- [ ] Knowledge-risk hotspots flagged.
- [ ] Register reviewed this cycle.

## Sources

- <https://martinfowler.com/bliki/TechnicalDebtQuadrant.html>
- <https://docs.enterprise.codescene.io/versions/1.5.2/guides/technical/hotspots.html>
- <https://www.iso.org/standard/78176.html> S5.1, S6.1
- https://martinfowler.com/bliki/TechnicalDebtQuadrant.html
