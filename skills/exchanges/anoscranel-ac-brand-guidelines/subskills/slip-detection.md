---
name: slip-detection
domain: writing/brand-guidelines
trigger: "Detecting recurring style slips, terminology drift, absolute claims, and machine tells across text"
anti_trigger: "Running corpus audits across a document set (subskills/corpus-audit.md); fixing flagged text in remediation passes (subskills/remediation-pass.md)"
scope: "Detect recurring style slips, terminology drift, absolute claims, and machine tells across text."
status: seedling
---

# Slip Detection

## Standard

- **ISO 24495-1 Plain Language Principles**: research-backed analysis of recurring structural and cognitive hurdles in professional writing. <https://www.iso.org/standard/78907.html>
- **Microsoft Writing Style Guide**: enterprise standards for identifying terminology drift, jargon creep, and unverified superlative claims. <https://learn.microsoft.com/en-us/style-guide/>
- **AP Stylebook**: professional editorial guidelines for spotting inconsistent capitalization, punctuation drift, and stylistic anomalies. <https://www.apstylebook.com/>
- **GOV.UK Content Design Standards**: guidance on detecting artificial tone shifts and machine-generated patterns in public publications. <https://www.gov.uk/guidance/style-guide>
- ⚠️ House convention: machine tells and unapproved absolute claims in regulated or technical text carry high compliance risk and must be flagged with explicit attribution cautions.

## Decision rules

1. Monitor multi-team documentation repositories for terminology drift where different groups adopt divergent synonyms for identical concepts.
2. Flag unapproved superlatives and absolute claims (for example: "industry-leading", "flawless", "zero downtime") unless substantiated by verified metrics.
3. Identify artificial machine tells (overused transitional phrases, redundant summaries, robotic cadence) across AI-assisted drafts.
4. Scan for inconsistent capitalization and formatting across headings, user interface labels, and product feature names.

## Procedure

1. Review aggregate corpus audit logs to identify recurring failure patterns and systemic slip categories.
2. Run targeted term searches across documentation repositories to map instances of terminology drift between teams.
3. Audit text blocks for unapproved absolute claims and superlatives, verifying whether compliance evidence exists.
4. Inspect writing cadence and structural transitions to detect artificial machine tells and formulaic phrasing.
5. Check heading hierarchies, button labels, and feature names for inconsistent capitalization and punctuation.
6. Compile detected slip patterns into a diagnostic analysis report for training and guideline refinement.
7. Feed slip patterns back into checklist construction to prevent recurrence in future content releases.

## Anti-patterns

- Treating recurring slips as isolated typos rather than diagnosing systemic terminology or training gaps.
- Allowing unapproved absolute claims to pass into customer-facing documentation without verification.
- Ignoring machine tells in AI-assisted drafts, leading to homogeneous and unnatural brand voices.
- Failing to track cross-team terminology drift, resulting in fragmented and confusing user experiences.

## Done checklist

- [ ] Aggregate audit logs are analyzed for recurring slip patterns.
- [ ] Terminology drift between writing teams is mapped and reported.
- [ ] Unapproved superlatives and absolute claims are flagged with attribution cautions.
- [ ] Machine tells and robotic phrasing patterns are identified in text samples.
- [ ] Inconsistent capitalization and formatting anomalies are cataloged.
- [ ] Diagnostic analysis report is prepared for stakeholders.
- [ ] Slip patterns are fed back into checklist maintenance.

## Sources

- ISO 24495-1: Plain language - Part 1: Governing principles and guidelines. <https://www.iso.org/standard/78907.html>
- Microsoft Writing Style Guide. <https://learn.microsoft.com/en-us/style-guide/>
- AP Stylebook. <https://www.apstylebook.com/>
- GOV.UK Style Guide. <https://www.gov.uk/guidance/style-guide>
