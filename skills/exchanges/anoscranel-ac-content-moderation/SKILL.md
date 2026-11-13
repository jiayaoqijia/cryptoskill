---
name: ac-content-moderation
description: 'Running the systems that judge user-generated content: the policy hierarchy from principles to line-level rules, taxonomy design that makes reviewer disagreement measurable, classifiers and thresholds as precision-recall decisions, the moderation queue and reviewer calibration, graduated enforcement actions, appeals as error correction, boundaries with adjacent security surfaces, and the written moderation record. It explains how moderation systems are engineered; it never decides what content is allowed. Use when asking "content moderation", "trust and safety engineering", "moderation queue", "reviewer guidelines", "policy taxonomy", "appeal process", "graduated enforcement", "classifier threshold", "false positive rate". Not for endpoint rate limiting and bot defence (ac-security-engineer), not for detection engineering of security telemetry (ac-security-operations), not for LLM-judge evaluation of model outputs (ac-model-evaluation).'
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Content moderation

## Overview

A content moderation system is the machinery a platform uses to enforce its rules on what users post: the policy hierarchy that makes rules decidable, the classifiers that pre-screen, the queues that route work to reviewers, the enforcement ladder that scales action to severity, and the appeals path that catches the errors all of this makes. The craft is designing each layer so that the error rates, throughput, and fairness of the whole are measurable and reviewable — not deciding the rules themselves.

This skill covers that machinery. The policy is the platform's decision; the engineering makes it enforceable at scale with known error rates. Nothing here determines what content should be allowed — each leaf treats the rules as an input and builds the systems that apply them consistently enough to be audited.

Primary sources: <https://en.wikipedia.org/wiki/Content_moderation> and <https://transparency.meta.com/>.

## When to use

- Designing or reviewing a moderation pipeline for user-generated content.
- Setting classifier thresholds with known precision-recall trade-offs.
- Building reviewer queues, calibration, and inter-rater agreement.
- Designing enforcement ladders and appeal paths.

## When NOT to use

- For rate limiting and bot defence of endpoints (use ac-security-engineer).
- For detection engineering on security telemetry (use ac-security-operations).
- For LLM-judge evaluation of model outputs (use ac-model-evaluation).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/policy-hierarchy.md` | `software-engineering/policy-hierarchy` | Principles, policies, and line-level rules in a decidable chain. |
| `subskills/taxonomy-and-labeling.md` | `software-engineering/taxonomy-and-labeling` | Violation categories that make disagreement measurable. |
| `subskills/classifiers-and-thresholds.md` | `software-engineering/classifiers-and-thresholds` | Pre-screening models as precision-recall decisions. |
| `subskills/queues-and-calibration.md` | `software-engineering/queues-and-calibration` | Routing, reviewer guidance, and inter-rater agreement. |
| `subskills/enforcement-ladders.md` | `software-engineering/enforcement-ladders` | Graduated actions proportionate to severity and history. |
| `subskills/appeals-and-error-correction.md` | `software-engineering/appeals-and-error-correction` | Appeals as the system's error-rate measurement. |
| `subskills/scope-and-boundaries.md` | `software-engineering/moderation-scope` | What the system covers, adjacent surfaces, and regime changes. |
| `subskills/moderation-record.md` | `software-engineering/moderation-record` | The written record: policies, thresholds, outcomes, error rates. |

## Status and honest limits

Moderation outcomes are judgements about human expression under rules that change with law and public pressure; the engineering makes those judgements consistent and measurable, not correct. Classifier thresholds trade acceptable-removal against missed-violations, and no setting makes both zero. Reviewers disagree, systems drift, and adversarial users probe every boundary — the record's error rates are the honest headline of any implementation, and a platform unwilling to measure its own error rate has not engineered moderation; it has merely installed opinion at scale.
