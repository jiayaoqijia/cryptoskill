---
name: remediation-pass
domain: writing/brand-guidelines
trigger: "Fixing flagged text with minimal edits, separating the auditing role from the remediation role"
anti_trigger: "Detecting recurring style slips (subskills/slip-detection.md); issuing compliance reports and release gates (subskills/sign-off-and-reporting.md)"
scope: "Fix flagged text with minimal edits, separating the auditing role from the remediation role."
status: seedling
---

# Remediation Pass

## Standard

- **AP Stylebook Editorial Revision Standards**: professional practices for executing clean, minimal copyedits based on structured audit findings. <https://www.apstylebook.com/>
- **Microsoft Writing Style Guide**: enterprise editing guidance on preserving author voice while enforcing terminology and formatting standards. <https://learn.microsoft.com/en-us/style-guide/>
- **ISO 24495-1 Plain Language Principles**: international guidelines for revising complex or non-compliant text into clear, usable language. <https://www.iso.org/standard/78907.html>
- **Chicago Manual of Style**: standards for managing tracked changes, corrections, and minimal-intervention editing passes. <https://www.chicagomanualofstyle.org/>
- ⚠️ House convention: the person executing the remediation pass must be separate from the auditor who logged the findings to maintain objective verification integrity.

## Decision rules

1. Enforce strict separation of duties: auditors and remediators must be different individuals or roles to prevent confirmation bias.
2. Map every remediation action directly to the fix category (replace, delete, rephrase, reformat) assigned in the audit log.
3. Apply minimal edits that correct the identified non-compliance without altering the surrounding grammatical structure or technical meaning.
4. Re-run the exact checklist audit pass on remediated text to verify that fixes resolved the issues without introducing new defects.

## Procedure

1. Receive the ranked audit ledger containing exact verbatim quotes, file locations, rule IDs, and fix categories.
2. Assign remediation tasks to a writer or editor who did not participate in the original audit pass.
3. For each finding, locate the offending text in the source file using the logged path and reference details.
4. Apply the designated fix category: substitute banned terminology, remove unverified claims, rephrase awkward phrasing, or reformat layout structures.
5. Ensure edits are minimal, preserving the author's primary intent while achieving strict compliance with the brand specification.
6. Re-run the checklist audit verification pass on all modified files to confirm zero residual defects.
7. Mark findings as resolved in the audit tracking system and submit the cleaned files for final sign-off.

## Anti-patterns

- Permitting the original auditor to perform the remediation pass, compromising objective verification.
- Rewriting entire paragraphs when a simple terminology substitution or minor rephrasing would suffice.
- Applying remediation edits without re-running checklist verification, allowing residual defects to escape.
- Modifying technical meaning or factual claims under the guise of stylistic editing.

## Done checklist

- [ ] Remediation tasks are assigned to personnel independent of the auditing role.
- [ ] Every finding in the audit ledger is addressed according to its designated fix category.
- [ ] Edits are verified as minimal interventions preserving technical intent.
- [ ] Modified files undergo a re-audit checklist verification pass.
- [ ] Residual defects are eliminated before submission.
- [ ] Audit ledger is updated to reflect resolved findings.
- [ ] Cleaned documents are delivered for final sign-off.

## Sources

- AP Stylebook. <https://www.apstylebook.com/>
- Microsoft Writing Style Guide. <https://learn.microsoft.com/en-us/style-guide/>
- ISO 24495-1: Plain language - Part 1: Governing principles and guidelines. <https://www.iso.org/standard/78907.html>
- Chicago Manual of Style. <https://www.chicagomanualofstyle.org/>
