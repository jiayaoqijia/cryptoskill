---
name: ac-security-operations
description: "Running security as an ongoing operation rather than a build task: detection engineering and rule quality, alert triage and the SOC queue, threat hunting from hypotheses, vulnerability triage and patch sequencing, phishing simulations and awareness, purple-teaming to close detection gaps, backup verification and disaster recovery drills, and the written SecOps record. It covers the operate-the-program layer; it never promises prevention and never recommends a tool. Use when asking \"SecOps\", \"detection engineering\", \"alert fatigue\", \"SOC triage\", \"threat hunting\", \"vulnerability prioritization\", \"patch sequence\", \"phishing simulation\", \"purple team\", \"backup verification\", \"disaster recovery test\", \"mean time to detect\". Not for building security controls into software (ac-security-engineer), not for standards catalogues and compliance editions (ac-security-standards), not for securing one trading account (ac-exchange-account-security)."
license: MIT
metadata:
  domain: security-hardening
status: seedling
---

# Security operations

## Overview

Security engineering builds controls; security operations runs them, every day, against an adversary who changes. The operational questions are different in kind from the engineering ones: which alerts are real, what is worth patching first, whether the backups actually restore, whether the detections would catch the attack that matters, and how the team degrades at three in the morning.

This skill covers that operating layer: how detections are engineered and measured, how a queue is triaged without drowning, how hunts are structured, how vulnerabilities are prioritized when everything cannot be patched at once, how phishing readiness is measured rather than assumed, how purple teaming closes the loop between offense and detection, and how backup and recovery is verified by doing it. It assumes the controls exist and asks whether they work this week.

Primary sources: <https://www.cisa.gov/> and <https://www.nist.gov/>.

## When to use

- When standing up or assessing a security operations capability.
- When alert volume, triage, or detection quality is the problem.
- When prioritizing vulnerabilities or sequencing patches.
- When verifying backups, recovery, or incident readiness by exercise.

## When NOT to use

- For building security into an application (use ac-security-engineer).
- For standards editions and compliance catalogues (use ac-security-standards).
- For securing a personal trading account at an exchange (use ac-exchange-account-security).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/detection-engineering.md` | `security-hardening/detection-engineering` | Writing detections as tested code with measured precision, not grep patterns. |
| `subskills/alert-triage-and-soc.md` | `security-hardening/alert-triage-and-soc` | The queue, its fatigue, and the triage that keeps signal above noise. |
| `subskills/threat-hunting.md` | `security-hardening/threat-hunting` | Hypothesis-driven hunts over telemetry, distinct from alert waiting. |
| `subskills/vulnerability-prioritization.md` | `security-hardening/vulnerability-prioritization` | Ranking by exposure and exploitability, not by CVSS alone. |
| `subskills/phishing-readiness.md` | `security-hardening/phishing-readiness` | Simulations, reporting culture, and what a click rate measures. |
| `subskills/purple-teaming.md` | `security-hardening/purple-teaming` | Attack, detect, and feed the gap back into the detections. |
| `subskills/backup-and-recovery-drills.md` | `security-hardening/backup-and-recovery-drills` | A backup is a restore test; a plan is a drill that ran. |
| `subskills/secops-record.md` | `security-hardening/secops-record` | The written record: detections, metrics, drills, and their dates. |

## Status and honest limits

Security operations measures itself with metrics that are easy to game, and every number in this skill carries a caveat: time-to-detect that ignores the alerts nobody looked at, patch compliance that ignores the one unpatched internet-facing host, click rates that measure the simulation rather than the adversary. The honest operator publishes the metric with its blind spot stated. Nothing here prevents an incident; the work is shortening the time between compromise and notice, and being able to prove what happened afterwards.
