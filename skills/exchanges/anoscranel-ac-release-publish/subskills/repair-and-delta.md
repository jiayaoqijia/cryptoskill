---
name: repair-and-delta
domain: skill-authoring/repair-and-delta
trigger: "Fixing audit findings before a release; a sweep that missed cases; a repair that may have broken something it did not touch"
anti_trigger: "Producing the original audit findings; deciding whether the release may ship; publishing the repaired tree"
scope: "Repairing findings from evidence with a logged removal list, widening a sweep from the corpus's own patterns, and auditing the repair delta"
status: "seedling"
---

# Repair and Delta Audit

## Standard

- **GNU grep**: a pattern matches exactly the lines its expression describes, so the expression defines the sweep's width. <https://www.gnu.org/software/grep/manual/grep.html>
- **git diff**: the delta is a first-class artifact; review the change, not the whole tree. <https://git-scm.com/docs/git-diff>
- **NIST SP 800-53 Rev. 5, AC-5 (separation of duties)**: authoring and reviewing a change are separate duties. ⚠️ Applying that control to fix review is house convention, not AC-5 text. <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
- ⚠️ House observation: repair-introduced defects have been the largest class in the audits this project has run. The delta audit exists for that class.

## Decision rules

1. Repair only from a finding: quote it, open the line, replace the exact string.
2. No opportunistic edits: every extra edit is unaudited surface.
3. Log every removal with file, line, old text, and reason. A deletion is the change nobody can reconstruct.
4. A sweep is as wide as its regex: build the pattern from the styles present in the corpus, not the ones you expect.
5. A second hand greps with a pattern it chose; a hit only that pattern finds proves the first sweep was too narrow.
6. The delta audit answers two questions: what did the repair break, and which findings remain.
7. Assume the fix broke something; that is the base rate. A behaviour change reopens the claim set.

## Procedure

1. Sort findings by severity; work the blockers first.
2. For each: open the file at the line, read the paragraph, apply the exact replacement.
3. Re-run the proof, then append to the repair log: finding id, file, line, old and new strings, proof output.
4. Re-run the gate suite; a repair that fails a gate is a regression, not a finding.
5. Build the sweep from the corpus: list the styles it uses for citations, tags, and cross references, write one alternation, run it, and read every hit before replacing anything.
6. Have a second hand search the same scope with a pattern of their own, then compare hit sets.
7. Hand the diff, the log, and the open findings to a reviewer who did not repair.
8. Delta audit: for each hunk, ask what else the change touched. Look for lost punctuation, merged lines, broken tables, and invalidated counts.
9. Fix regressions, then audit only the new changes.

In practice: `[12]`, `see S3`, and `(above)` are three styles and one pattern: `\[[0-9]+\]|\bS[0-9]+\b|\(above\)`. A sweep for `[12]` alone covers a third and reports success.

## Anti-patterns

- **Search and replace across the tree.** It edits sentences nobody reviewed. Fix: one finding, one exact string.
- **One sweep treated as complete.** Three passes in a row can each miss a tag style. Fix: a second pattern from a second hand.
- **The auditor repairing.** The finder hides its own fix. Fix: writer repairs, third read audits the delta.

## Done checklist

- [ ] Every repair traces to a finding and an exact string.
- [ ] Every repair re-proved; every removal logged with old text.
- [ ] Gate suite re-run after the last repair.
- [ ] Sweep pattern built from the corpus's own styles.
- [ ] Second pattern run by a second hand; hit sets compared.
- [ ] Diff reviewed by someone who did not repair; regressions fixed and re-audited.

## Sources

- GNU grep: <https://www.gnu.org/software/grep/manual/grep.html>
- git diff: <https://git-scm.com/docs/git-diff>
- NIST SP 800-53 Rev. 5, AC-5: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
