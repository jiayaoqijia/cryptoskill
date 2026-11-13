---
name: ac-compliance-program-engineering
description: "Running a compliance program as engineering work rather than a document shelf: choosing a framework like SOC 2 or ISO 27001, mapping its controls to named engineering owners, building evidence into the pipeline so audits sample from what exists, the trust-criteria oversell trap, remediation that closes findings without reopening them, and the written compliance record. It explains how an engineering team prepares for and passes a controls audit; it never renders an audit opinion and never legal advice. Use when asking \"SOC 2 Type II\", \"ISO 27001 certification\", \"compliance readiness\", \"audit evidence collection\", \"control owner\", \"policy as code\", \"compliance automation\", \"audit findings remediation\", \"continuous compliance\". Not for security hardening technique itself (ac-security-engineer), not for which standard exists and its editions (ac-security-standards), not for the technical audit-trail design (ac-audit-logging)."
license: MIT
metadata:
  domain: security-hardening
status: seedling
---

# Compliance program engineering

## Overview

A compliance framework — SOC 2, ISO 27001 — lists controls that an auditor samples and verifies. Passing the audit means showing that each control exists, is owned, operates, and leaves evidence the auditor can inspect. For an engineering team this is a systems problem: the control must be built into the pipeline, the evidence it produces must be collected automatically where possible, and the owner must be a named engineer rather than a policy binder. Teams that treat compliance as a document layer fail the audit on the evidence step, because the binder describes a control that the running system does not implement.

This skill covers the program from the engineering side: choosing the framework and scope, mapping controls to owners and pipelines, making evidence a by-product of normal operation, the writing of policies that state what the system actually enforces, and closing findings. The security techniques behind each control belong to ac-security-engineer, the standards catalogue to ac-security-standards, and the design of tamper-evident trails to ac-audit-logging.

Primary sources: <https://www.aicpa-cima.com/topic/standards-attestation-reporting/soc-2> and <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>.

## When to use

- When preparing for a SOC 2 or ISO-type controls audit for the first time.
- When mapping framework controls to engineering owners and pipelines.
- When making control evidence automatic rather than a pre-audit scramble.
- When closing audit findings so they stay closed.

## When NOT to use

- For the security techniques a control requires (use ac-security-engineer).
- For which standard exists and which edition is current (use ac-security-standards).
- For designing tamper-evident audit logs (use ac-audit-logging).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/framework-and-scope.md` | `security-hardening/framework-and-scope` | Choosing the framework and drawing the audited boundary honestly. |
| `subskills/control-to-owner-mapping.md` | `security-hardening/control-to-owner-mapping` | Every control mapped to a named engineer and its pipeline. |
| `subskills/evidence-from-the-pipeline.md` | `security-hardening/evidence-from-the-pipeline` | Evidence as a by-product of normal operation, sampled not staged. |
| `subskills/policies-that-match.md` | `security-hardening/policies-that-match` | Policies stating what the system enforces, nothing more. |
| `subskills/readiness-review.md` | `security-hardening/readiness-review` | Reproducing the audit internally before the auditor arrives. |
| `subskills/findings-and-remediation.md` | `security-hardening/findings-and-remediation` | Closing a finding at the cause, with the re-test to prove it. |
| `subskills/compliance-record.md` | `security-hardening/compliance-record` | The written record: scope, mappings, evidence index, findings, dates. |

## Status and honest limits

An audit opinion belongs to the auditor; this skill prepares the ground and never renders one. Framework texts change, and every mapping here is dated against the edition current at the time. The deepest limit is honest: passing a controls audit demonstrates that stated controls operate and produce evidence — not that the system is free of every risk, only that it enforces what it says it enforces. Teams overselling this fact to customers create the gap that the record must never paper over.
