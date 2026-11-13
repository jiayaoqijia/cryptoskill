---
name: independent-audit
domain: skill-authoring/independent-audit
trigger: "Briefing a second hand to check a release before it ships; a claim table the writer should not also judge; an audit that returned 'looks fine' with no evidence"
anti_trigger: "Writing the claim inventory; repairing findings; auditing the repair delta rather than the original claim set"
scope: "Briefing and reading a read-only independent audit of a release claim set, with severities, exact replacements, and a stated coverage limit"
status: "seedling"
---

# Independent Audit

## Standard

- **NIST SP 800-53 Rev. 5, AC-5 Separation of Duties**: authoring and approving are different roles; no single role controls every step. <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
- **SLSA**: verification checks the artifact against recorded evidence, not the author's confidence. <https://slsa.dev>
- ⚠️ House framing: the four-eyes principle, a second independent reader signing off, is a general control idea. No public standard prescribes it for a one-person repository.
- **GNU grep**: a finding rests on an observed line, and an observed line is reproducible. <https://www.gnu.org/software/grep/manual/grep.html>

## Decision rules

1. The auditor is a different agent or person from the writer. ⚠️ A fresh context in the same model reduces anchoring but is not a second pair of eyes.
2. The auditor is read-only: no edits, commits, tags, or pushes.
3. "Verified" means an observed command output or a quoted line, never an impression.
4. Every finding carries file, line, severity, and the exact replacement text. A finding without a replacement is a complaint.
5. Severity: blocker means a false claim, private data, a dead link, or broken structure; major means unproved or misleading; minor means wording.
6. Cap the web fetches and state the cap in the brief. Ten suits a small repository.
7. Coverage is stated: every blocker-class claim, a named sample of the rest, and the files not read.

## Procedure

1. Freeze the tree; pass its file-list hash with it.
2. Write the brief with six fields: scope, file list, definition of verified, output schema, fetch cap, read-only rule.
3. Ask for an independently built inventory. If the writer supplies one, the auditor rebuilds it and reports differences.
4. For each claim: run the proof, paste the output, mark PASS, FAIL, or UNPROVED. UNPROVED is a verdict, not a soft pass.
5. Read for what no claim covers: private paths, stale versions, undescribed files, links inside the changelog.
6. Return findings sorted by severity, with raw output attached.
7. Keep the raw output with the findings, so a later release can re-check the verdict.
8. The writer fixes or accepts with a written reason. A blocker is never accepted.

A usable finding reads `README.md:14`, blocker, "no scripts" over four files in `scripts/`; replace with "four scripts under `scripts/`". A useless one reads "the README is inaccurate".

## Anti-patterns

- **Self-audit with a new prompt.** Same context, stricter tone, same blind spots. Fix: a different hand, or an explicit downgrade of the claim.
- **Auditor fixing as it goes.** Repair contaminates the evidence. Fix: findings only.
- **"Verified" defined as "read it".** Fix: define it as a command output.
- **Sample with no stated coverage.** The audit sounds complete and is not. Fix: name skipped files.
- **Severity inflation.** Everything is critical, so the blockers vanish. Fix: apply the three-level scale.
- **Uncapped fetching.** The audit becomes browsing. Fix: cap fetches and audit the bytes.

## Done checklist

- [ ] Auditor is a different hand from the writer.
- [ ] Brief carries scope, file list, definition, schema, fetch cap, read-only rule.
- [ ] Inventory built or rebuilt by the auditor, differences noted.
- [ ] Every finding has file, line, severity, and replacement text.
- [ ] Coverage stated, including files not read.
- [ ] Raw output kept; every blocker fixed, never accepted.

## Sources

- NIST SP 800-53 Rev. 5, AC-5: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
- SLSA: <https://slsa.dev>
- GNU grep: <https://www.gnu.org/software/grep/manual/grep.html>
