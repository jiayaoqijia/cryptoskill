---
name: planning
domain: software-engineering/planning
trigger: "\"How long will this take\", \"estimate this\", \"when can we ship\", \"Scrum or Kanban\", \"what are the risks\", \"should we build or buy this\"."
anti_trigger: "Cutting the work into tasks (subskills/task-breakdown.md); choosing the system structure; picking a library version."
scope: "Estimates, forecasts, process and cadence choice, risk list, build-vs-buy"
status: "seedling"
---

# Planning

## Standard

- **Estimates**: story points with Planning Poker (Cohn 2005), #NoEstimates (Zuill), or throughput forecasting from past flow data. Software estimates run late often. ⚠️ Overrun figures vary by study; do not quote one number.
- **Process**: Scrum Guide 2020 (https://scrumguides.org), Kanban Guide (https://kanbanguides.org), XP practices, Shape Up (https://basecamp.com/shapeup) with fixed appetite instead of estimates.
- **Risk**: pre-mortem (Gary Klein, HBR 2007) surfaces failure causes before work starts.
- **Build vs buy**: Wardley mapping. Build what differentiates; buy what is commodity. Spend few "innovation tokens" (McKinley, "Choose Boring Technology", 2015).
- Sustainable pace: crunch loses output within weeks (Robinson, IGDA 2005).

## Decision rules

1. Give a range with a confidence, never a single date. Example: "3–5 weeks, 80% confident."
2. With 10+ finished items of history, forecast from throughput. Without history, use relative sizing and say so.
3. Re-forecast when scope changes by more than one task or when a spike returns.
4. Process choice:
 - Planned increments with a stable team → Scrum-style sprints.
 - Interrupt-driven or ops work → Kanban with WIP limits.
 - Product bets with fixed time → Shape Up appetite.
 - One person → Kanban plus a weekly review.
5. Risks enter a register with likelihood, impact, owner and a trigger. Top three get a mitigation task now.
6. Build when the capability is your differentiator or no vendor meets a hard requirement. Buy or use open source when it is commodity. Record the choice as an ADR.
7. A new technology needs a named reason it beats the boring option.
8. Never plan above sustainable pace. Overtime is a risk, not a plan.

## Procedure

1. List tasks from the breakdown. Size each (S/M/L or points). Spike unknowns first.
2. Forecast:
 - With history: run a Monte Carlo over past weekly throughput. Report 50th and 85th percentile dates.
 - Without history: sum sizes, apply your team's past ratio of actual to estimate. If none exists, widen the range and flag it ⚠️.
3. Run a pre-mortem. Each person writes failure causes alone, then merge.
4. Fill the risk register:
   ```markdown
   | Risk | Likelihood | Impact | Owner | Trigger | Mitigation |
   ```
5. For each component you might buy, score: differentiating? vendor lock-in? total cost over 3 years? exit cost? Decide and write the ADR.
6. Choose cadence with rule 4. Publish range, confidence, assumptions and top risks. Review weekly.

## Anti-patterns

- Single-date promises; padding hidden inside estimates.
- Velocity used as a target (Goodhart).
- Process as ritual ("Scrum-but").
- Building auth or billing in-house with no reason.
- Risk register written once, never read.

## Done checklist

- [ ] Forecast is a range with a confidence level.
- [ ] Assumptions listed.
- [ ] Pre-mortem done; top three risks mitigated or owned.
- [ ] Build-vs-buy choices recorded as ADRs.
- [ ] Cadence chosen and written.
- [ ] Re-forecast trigger stated.

## Sources

- <https://www.si-labs.com/en/articles/spotify-model/>
- https://scrumguides.org · https://kanbanguides.org · https://basecamp.com/shapeup
