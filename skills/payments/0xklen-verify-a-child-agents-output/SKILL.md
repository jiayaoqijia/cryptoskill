---
name: verify-a-child-agents-output
description: Use when a subagent or helper reports its task complete. Re-runs the acceptance check and inspects the artifact against the brief, because a child's "done" is a claim to audit, not evidence.
---

# Verify a Child Agent's Output

A child's success message is testimony, and the parent owns the result. Re-derive it: run the check the brief specified, open the artifact, and confirm the count matches the ask.

## Procedure

1. Re-read the brief at `notes/children/<child-id>.brief.md` so you check against what was asked, not against what the child produced.
2. Run the same acceptance command you handed the child, yourself: `python3 tools/validate.py --only foo`. Never trust a pasted summary.
3. Confirm declared totals against actual ones: if the child says "20 skills", run `ls skills/ | wc -l` and compare rather than eyeballing.
4. Open the artifact at its path and read it; a file can pass a linter and still hold the wrong content.
5. Check the boundary the brief set with a read-only `git status --short` and confirm no forbidden file changed.
6. Assert on counts with code, not prose: `grep -c '^## ' skills/foo/SKILL.md` returns 3, not "the headings look fine".
7. Distinguish "ran without error" from "produced the right output" — exit 0 with empty output is a silent failure.
8. If any check disagrees with the child's report, treat the whole report as unverified and re-examine each claim.
9. Record the verdict as a line in `notes/verification.log`: `child-id PASS|FAIL command exit-code`.
10. Re-dispatch only the failed slice, never the whole task.

## Pitfalls

- Accepting a child's summary line ("20/20 valid") without re-running the command that produces it; a header can be typed by hand.
- Reading the diff the child chose to show rather than the artifact on disk, which may carry extra edits.
- Letting the child's confident tone substitute for a passing check.
- Comparing a declared count to a filtered file listing and calling it verified.
- Marking a child verified because no error printed, when the command exited 0 without emitting its expected line.

## Verification

```bash
python3 tools/validate.py --only foo; echo "exit=$?"
# passes when the parent-run check reports the same result the child claimed
```

Report to the user: the child id, the acceptance command you re-ran, its exit code, and any claim that did not hold.
