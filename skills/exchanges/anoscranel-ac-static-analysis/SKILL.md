---
name: ac-static-analysis
description: "Getting value from tools that read code without running it: what linters and analyzers can and cannot find, rule selection and severity discipline, suppressions with a reason and an expiry, baselines for adopted code, metrics from analysis and their misuse, wiring analysis into review and CI, and the written analysis record. It explains how static analysis is chosen and kept useful; it never recommends a specific tool and never treats a clean report as proof of correctness. Use when asking \"linter\", \"static analysis\", \"code smell\", \"cyclomatic complexity\", \"naming convention\", \"lint suppression\", \"baseline\", \"why did the linter stop finding anything\", \"should I enforce this rule\". Not for runtime debugging (ac-debugging), not for test design (ac-testing), not for security vulnerability assessment (ac-security-engineer)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Static analysis

## Overview

Static analysis reads code and reports patterns — some stylistic, some structural, some pointing at real defects. Its promise is consistency at a scale review cannot reach; its trap is noise, because a tool that reports everything_trainable trains everyone to ignore it. The craft is not running the tool but curating it: choosing rules whose findings a team will act on, ranking severity so real signals are not filed beside stylistic ones, and keeping the suppression path honest so exceptions are visible and temporary.

This skill covers that curation: what analysis can and cannot mechanically find, rule selection discipline, suppression hygiene, baselining when adopting a tool onto existing code, the metrics analysis produces and their failure modes, and wiring into review. The security-vulnerability side of analysis belongs to the security skill; this is about the everyday discipline of mechanical reading.

Primary source: <https://martinfowler.com/>.

## When to use

- When adopting or rescuing a linter or analyzer on a codebase.
- When a team ignores its analysis output and the question is why.
- When deciding whether a rule should be enforced, warned, or dropped.
- When a suppression count is growing and nobody knows why.

## When NOT to use

- For runtime debugging of a live defect (use ac-debugging).
- For test design and coverage (use ac-testing).
- For security vulnerability assessment (use ac-security-engineer).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/what-analysis-finds.md` | `software-engineering/what-analysis-finds` | The shape of mechanically detectable problems. |
| `subskills/rule-selection-and-severity.md` | `software-engineering/rule-selection-and-severity` | Choosing rules a team will act on, and ranking them. |
| `subskills/suppressions-and-baselines.md` | `software-engineering/suppressions-and-baselines` | The honest exception: reason, scope, and expiry. |
| `subskills/metrics-and-their-misuse.md` | `software-engineering/metrics-and-their-misuse` | What complexity measures measure. |
| `subskills/analysis-in-review.md` | `software-engineering/analysis-in-review` | Letting the tool speak before the human reads. |
| `subskills/adopting-onto-existing-code.md` | `software-engineering/adopting-onto-existing-code` | Baselining an existing codebase without a big bang. |
| `subskills/analysis-record.md` | `software-engineering/analysis-record` | The written record of rules, severities, and exceptions. |

## Status and honest limits

Analysis finds what its rules describe, in the shapes its parsers understand; a clean report means no rule fired, not that no defect exists. Tools differ and their rule sets churn — the discipline here is stable, the flag names are not. Nothing here recommends a tool, and the most valuable findings an analysis produces are the ones a team argues about: the argument is the value, and the tool is only the prompt.
