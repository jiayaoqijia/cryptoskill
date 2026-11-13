---
name: heuristic-evaluation
domain: software-engineering/design-taste
trigger: "Run a heuristic evaluation; Nielsen pass on this flow; check this against the ten heuristics; usability review with severity"
anti_trigger: "The general critique order and hosting (subskills/critique-protocol.md); scoring dimensions with the 0-10 rubric (subskills/rubric-scoring.md); automated axe scans"
scope: "Nielsen's ten heuristics run as an evidence protocol inside this skill, including severity ratings"
status: seedling
---
# Heuristic Evaluation

## Standard

- **Nielsen's 10 Usability Heuristics**: the canonical list, from visibility of status to help and documentation (https://www.nngroup.com/articles/ten-usability-heuristics/).
- **NN/g, "How to Conduct a Heuristic Evaluation"**: independent evaluators, two passes, merged findings; three to five evaluators find most problems (https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/).
- **NN/g severity ratings**: rate by frequency, impact, and persistence on a 0 to 4 scale (https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/).
- The heuristics are a review lens, not a conformance gate (NN/g, same articles).

## Decision rules

1. If a problem fits no heuristic, record it as "other". The list is a lens, not a whitelist.
2. If evaluators disagree on which heuristic applies, log both. Deduplicate at merge time.
3. Severity is frequency times impact times persistence. A blocker on the top task rates critical even when rare.
4. If the same flaw appears on five screens, file one finding with five instances, not five findings.
5. If there is no evidence, there is no finding. Attach a screenshot, a quote, or a step trace.
6. If evaluators work together first, independence dies. Passes stay solo until the merge.
7. Score severity against the user's task, never against the team's taste.

## Procedure

1. Write down the users, the tasks, and the screens in scope.
2. Each evaluator passes twice: once for the flow, once for individual elements.
3. Log every violation: identifier, location, description, heuristic, evidence.
4. Work alone. No conferring during the passes.
5. Merge the logs. Deduplicate identical findings and keep every attested instance.
6. Rate each finding 0 to 4 with the NN/g anchors, and write the reason beside the number.
7. Rank fixes by severity first, then by repair effort.
8. Report one table of findings, a severity summary, and the top three fixes.

## Anti-patterns

- Debating during the pass. Fix: independent first, merge after.
- Arguing heuristic names. Fix: log both and move on.
- "It feels wrong" with no evidence. Fix: attach a screenshot or drop the finding.
- Inflating severity to force action. Fix: rate against the anchors.
- One evaluator declaring completion. Fix: three to five where possible.
- Findings with no screen named. Fix: location is required.

## Done checklist

- [ ] Users, tasks, and scope written down.
- [ ] Every finding carries location, description, heuristic, and evidence.
- [ ] Independent passes merged and deduplicated.
- [ ] Each finding rated 0-4 with a written reason.
- [ ] The top fixes ranked and named.

## Sources

- https://www.nngroup.com/articles/ten-usability-heuristics/
- https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/
- https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/
