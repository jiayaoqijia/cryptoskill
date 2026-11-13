---
name: ranking-criteria
domain: software-engineering/architecture-survey
trigger: "Prioritizing improvement candidates across impact, locality, confidence, and effort axes; structuring the final shortlist"
anti_trigger: "Formulating bounded candidates (subskills/candidate-formation.md); assembling the final survey report (subskills/report-discipline.md)"
scope: "Ranking candidates across impact, locality, confidence, and effort axes; prioritizing recurring high-impact problems over broad aesthetic rewrites; shortlist structure."
status: seedling
---

# Ranking Criteria

## Standard

- **Highsmith, _Agile Project Management_ (2009)**: value delivery and risk reduction dictate prioritization order; high-impact structural repairs precede broad aesthetic refinements. <https://www.oreilly.com/library/view/agile-project-management/9780321605908/>
- **IEEE Std 1028-2008**: formal reviews must evaluate findings against standardized criteria to ensure objective ranking and resource allocation. ⚠️ cited without URL.
- ⚠️ House convention: recurring multi-module problems always outrank isolated single-file awkwardness regardless of estimated implementation effort.

## Decision rules

1. If a candidate resolves a recurring structural smell across three or more modules, rank its impact higher than any single-file cosmetic improvement.
2. If two candidates have equivalent impact, rank the one with higher localization (affecting fewer downstream files) above the broader one.
3. If confidence in a finding is marked low due to ambiguous static evidence, penalize its ranking score until verified.
4. If estimated effort exceeds available maintenance capacity without delivering proportional testability or coupling gains, place the candidate in a deferred backlog section.

## Procedure

1. Evaluate each formed candidate across four independent axes: impact (reduction in coupling or testability gain), locality (scope of affected files), confidence (strength of supporting evidence), and effort (estimated refactoring cost).
2. Assign numerical or ordinal weights (High, Medium, Low) to each axis based on observed codebase characteristics.
3. Apply the recurrence weighting rule: elevate multi-module structural findings above localized style adjustments.
4. Sort candidates in descending order of priority, creating a curated shortlist of the top actionable opportunities (typically 3 to 7 candidates depending on repository size).
5. Format the shortlist entries with standardized headers containing title, impact summary, affected modules, estimated risk, and ranking rationale.

## Anti-patterns

- Ranking candidates purely based on personal author preference rather than objective impact and evidence.
- Placing broad, speculative rewrites at the top of the shortlist above verified localized fixes.
- Omitting effort and risk estimates when presenting high-impact candidates.
- Returning an unranked dump of all discovered findings without editorial filtering.

## Done checklist

- [ ] Candidates evaluated across impact, locality, confidence, and effort axes.
- [ ] Recurrence weighting applied to multi-module findings.
- [ ] Shortlist curated with clear descending priority order.
- [ ] Standardized headers applied to each shortlist entry.
- [ ] Low-confidence or low-impact items moved to deferred sections.

## Sources

- Highsmith, Jim. _Agile Project Management: Creating Innovative Products_. 2nd ed., Addison-Wesley Professional, 2009. <https://www.oreilly.com/library/view/agile-project-management/9780321605908/>
- Institute of Electrical and Electronics Engineers. _IEEE Std 1028-2008: IEEE Standard for Software Reviews and Audits_. IEEE, 2008. ⚠️ cited without URL.
