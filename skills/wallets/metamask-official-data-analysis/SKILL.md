---
maturity: experimental
name: data-analysis
description: Structured approach for analyzing metrics, attributing changes, and communicating findings — five phases (collection → filtering → curation → questioning → synthesis), confidence assignment, audience-appropriate artifacts
---

# Data Analysis Skill

Structured approach for analyzing metrics, attributing changes, and communicating findings.

---

## When to Use

- Performance analysis from production metrics
- Attribution of improvements/regressions to code changes
- Creating executive summaries or stakeholder communications
- Any analysis requiring correlation of changes to measured outcomes

---

## Quick Reference

### Five Phases

```
Collection → Filtering → Curation → Questioning → Synthesis
```

| Phase       | Key Question                | Output                              |
| ----------- | --------------------------- | ----------------------------------- |
| Collection  | What are we measuring?      | Baseline, scope, change list        |
| Filtering   | What's signal vs. noise?    | Categorized changes with confidence |
| Curation    | What correlates with what?  | Attribution table                   |
| Questioning | Do we KNOW or BELIEVE this? | Validated claims with caveats       |
| Synthesis   | Who needs to know what?     | Audience-appropriate artifacts      |

### Confidence Assignment

| Level      | Use When                                                         |
| ---------- | ---------------------------------------------------------------- |
| **High**   | Clear mechanism + timing alignment + targets measured population |
| **Medium** | Plausible mechanism but confounded by other changes              |
| **Low**    | Speculative or enabling-only                                     |

### Attribution Table Template

| Change        | Evidence    | Release   | Metric            | Confidence   | Notes                 |
| ------------- | ----------- | --------- | ----------------- | ------------ | --------------------- |
| [Description] | [PR/commit] | [version] | [affected metric] | High/Med/Low | [mechanism or caveat] |

---

## Process

### 1. Collection

```markdown
**Metrics:** [What are you measuring?]
**Population:** [Who? All users, p75, specific cohort? A percentile is not a cohort: "p75 = power users" is an assumption until verified against one]
**Exposure:** [Fraction of the population running a build that contains the change, over the same window, as a number. If it is unknown, no outcome reading is valid]
**Period:** [Measurement window - release tags or dates]
**Source:** [APM, logs, synthetic benchmarks?]
**Baseline:** [Starting values with methodology]
```

Enumerate ALL changes in scope:

- Code changes (PRs, commits)
- Config changes
- External factors (traffic, user growth, infrastructure)

### 2. Filtering

Categorize each change:

- **Direct:** Clear causal path to measured metric
- **Indirect:** Enabling infrastructure (value materializes later)
- **Unknown:** In scope but mechanism unclear
- **Noise:** Unlikely to affect measured metrics

### 3. Curation

Build attribution table:

1. Map changes to metric movements by release. Confirm each change's merge commit is contained in the release whose traffic you read, and segment by release so pre- and post-change clients are never pooled
2. Note co-landed changes (shared attribution)
3. Flag anomalies (improvement without cause, unexplained regression)
4. Separate measured vs. post-cutoff work

### 4. Questioning

Challenge every attribution:

- [ ] "Do we KNOW this, or do we BELIEVE this?"
- [ ] "What would need to be true for this to be wrong?"
- [ ] "Are there alternative explanations?"
- [ ] "Could a change in the population's composition explain it?" Decompose within-unit change from composition before reporting an aggregate

Document what's missing:

- [ ] Unexplained improvements
- [ ] Unexplained regressions
- [ ] Work that SHOULD have helped but didn't
- [ ] Metrics you wish you had

### 5. Synthesis

Create audience-appropriate artifacts:

| Artifact              | Audience        | Focus                                 |
| --------------------- | --------------- | ------------------------------------- |
| Executive Summary     | Leadership      | Hard data, key wins, team recognition |
| Attribution Catalogue | Engineering     | Detailed per-change analysis          |
| Methodology Doc       | Future analysts | Process, assumptions, data sources    |
| Communication Post    | Stakeholders    | Exciting but honest, caveats visible  |

---

## Communication Template

```markdown
**[Metric]: [Before] → [After] ([Change %])**

Population: [Who this measures]
Caveat: [Key limitation]
What's NOT included: [Equally interesting gaps]

Notable contributors:

- [Change 1] — [mechanism]
- [Change 2] — [mechanism]

Bottom line: [One sentence impact statement]
```

---

## Anti-Patterns

| Don't                                    | Do Instead                                       |
| ---------------------------------------- | ------------------------------------------------ |
| Claim causation from correlation         | "Correlates with" or "plausible contributor"     |
| Attribute release total to single change | Note multiple changes, unknown isolated impact   |
| Bury caveats in footnotes                | Caveats are part of the story                    |
| Use superlatives without data            | Let numbers speak                                |
| Hide uncertainty                         | Use qualifiers: "likely," "plausible," "unknown" |

---

## Checklist

Before finalizing:

- [ ] Measurement methodology documented
- [ ] Baseline values recorded with source
- [ ] All changes in scope enumerated
- [ ] Confidence levels assigned with justification
- [ ] Unexplained anomalies noted
- [ ] Limitations explicitly stated
- [ ] What's NOT included documented
- [ ] Uncertainty reflected in language
- [ ] Links/references for all claims
- [ ] Multiple artifacts for different audiences

---
