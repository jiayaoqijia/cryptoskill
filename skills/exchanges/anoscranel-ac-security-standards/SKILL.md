---
name: ac-security-standards
description: "Security-standards reference: which security standard exists, which edition is current, what its levels require, and what done means for a hardening pass — OWASP Top 10, OWASP ASVS levels, OWASP LLM and Agentic Top 10, NIST SSDF status, EU CRA dates, EN 301 549. Use when asking \"which OWASP/NIST standard applies\", \"what does ASVS level X require\", \"what is the current Top 10 edition\", \"what does done mean for a hardening pass\", \"where does this control sit in the lifecycle\". Not for doing the hardening work itself — threat-modelling a feature, fixing a security defect, triaging a CVE, responding to an incident; those craft tasks sit outside this skill (use ac-security-engineer); general SE-lifecycle standards (use ac-software-engineering-standards)."
license: MIT
metadata:
  domain: security-hardening
---

# Security Standards

## Overview

The reference layer, not the workshop. One leaf maps the domain's standards: names, current editions, dates, and what each governs. One leaf defines done for a hardening pass: the artifacts and evidence that must exist when the work finishes. It states where authority lives; it never says how to do the work.

## When to use

- "Which OWASP/NIST standard applies" and "is the 2025 edition current" questions.
- "What does ASVS level X require" — level intent, chapter shape, per-level targets.
- "What is the current Top 10 edition" — edition and date checks, including the LLM and Agentic lists.
- "What does done mean for a hardening pass" — the artifacts and evidence owed at hand-off.
- "Where does this control sit in the lifecycle" — specifying, designing, building, verifying, operating, responding.

## When not to use

- Performing any security task: threat models, code fixes, scans, CVE triage, incident response, disclosure. Those are craft tasks outside this skill.
- Selecting or implementing a control. This skill names the authority and the finish line; the craft sits outside it.

## Lifecycle frame

Security work rides the software lifecycle: specify (requirements with abuse cases) → design (threat model, trust boundaries) → build (defences per control class) → verify (level-chosen review, tests, scans) → release (gates, done criteria) → operate (logging, triage) → respond (incident first hour, disclosure). NIST SSDF groups its practices as Prepare the Organization, Protect the Software, Produce Well-Secured Software, Respond to Vulnerabilities. A control ask belongs to exactly one phase; this skill locates the phase, never performs the phase's work.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/standards-map.md` | Which security standard applies, with edition and date | "which OWASP/NIST standard applies" |
| `subskills/done-criteria.md` | What a completed hardening pass must deliver | "what does done mean for a hardening pass" |

## See also

- `subskills/standards-map.md` — the authorities.
- `subskills/done-criteria.md` — the finish lines.
