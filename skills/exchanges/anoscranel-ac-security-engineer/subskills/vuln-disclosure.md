---
name: vuln-disclosure
domain: security-hardening/vuln-disclosure
trigger: An external researcher reports a security bug, or the product needs a policy saying where to report it and what protection reporters get.
anti_trigger: Responding to a live breach of your own systems (subskills/security-incident.md); prioritising the dependency fix (subskills/cve-triage.md).
scope: security.txt, VDP, intake, CVE request, advisory
status: seedling
---

# Vulnerability Disclosure

## Standard

- **RFC 9116** (April 2022) defines `security.txt`: only **`Contact`** and **`Expires`** are required (Expires SHOULD be under a year ahead); optional fields include Policy, Encryption, Preferred-Languages; unknown fields are ignored. Serve at `/.well-known/security.txt` as `text/plain; charset=utf-8` (https://www.rfc-editor.org/rfc/rfc9116).
- **ISO/IEC 29147:2018** (2nd ed.) remains the current disclosure standard; a revision (AWI 29147) is under way (https://www.iso.org/standard/72311.html).
- CISA's **VDP template** (BOD 20-01 lineage) is the free starting point (cisa.gov/vulnerability-disclosure-policy-template).
- The CVE programme and CNAs remain the coordination substrate; a CRA manufacturer's duty for actively exploited vulnerabilities goes to its CSIRT/ENISA via the Single Reporting Platform (from 11 Sep 2026) — researcher disclosure does not discharge it.

## Decision rules

1. Safe harbour is non-negotiable: without a written commitment not to pursue good-faith research, researchers stay silent and you hear about bugs from attackers.
2. Publish the **policy** before the first report — the intake valve works only if findable when reports arrive.
3. Triage on the clock. ⚠️ These day-counts are house convention, not a standard: acknowledge 24–48h, validate in ~5 business days, disclose after a ~90-day window.
4. Bounty ≠ PSIRT: bounties are market-driven and shallow-bug biased; a PSIRT owns embargo management, root cause, patch delivery, and the CVE — a 24-hour CRA clock is a PSIRT problem.
5. Every externally visible act is **human-gated**: publishing an advisory, requesting a CVE, disclosing details, crediting — propose the text; a human sends it.

## Procedure

1. Add `/.well-known/security.txt`: `Contact: https://example.com/security-policy` (or `mailto:security@example.com`), `Expires:` <1 year with a renewal reminder, `Policy:` the VDP URL, `Preferred-Languages: en`.
2. Publish the policy page: **scope** (in and explicitly out — third-party services, social engineering, DoS), **channel**, **safe-harbour text**, **timelines**, plus bounty status.
3. Intake per report: acknowledge (quote the SLA), assign a named owner, reproduce, set severity in your own context; track centrally — email alone loses reports.
4. Validation: minimal proof of concept on a test instance; confirm impact and blast radius; for a dependency, coordinate with upstream (`subskills/cve-triage.md`) and answer the CRA question: is this product yours on the EU market?
5. Fix and ship; agree the disclosure date with the reporter (default the window); release is human-gated.
6. Request a CVE via the CNA once a fix exists; publish the advisory — severity, affected/fixed versions, workaround, credit (human-gated).
7. If actively exploited in your product, the incident path (`subskills/security-incident.md`) runs in parallel; CRA clocks start at awareness.

## Anti-patterns

- No `security.txt`: reports scatter across generic inboxes and die.
- Validating on production with live data.
- Arguing severity with the reporter instead of rerunning it in your context.

## Done checklist

- [ ] `/.well-known/security.txt` live with Contact + Expires (<1 year, reminder set).
- [ ] Policy page: scope, channel, safe harbour, timelines.
- [ ] Intake triage: named owner, SLA, reproduction, own-context severity.
- [ ] Disclosure date agreed with the reporter; fix ships before disclosure.
- [ ] CVE requested via the CNA when warranted (human-gated); advisory published by a human; credit given.

## Sources

- Primary: RFC 9116 (rfc-editor.org); ISO/IEC 29147 (iso.org, revision under way); CISA VDP template; EU CRA Art. 14 (EUR-Lex). ⚠️ The day-counts are house convention — state them as your own commitments in the policy.
- <https://www.first.org>
- <https://cve.mitre.org>
