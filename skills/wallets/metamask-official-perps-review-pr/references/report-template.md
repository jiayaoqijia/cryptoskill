# Posted review template

Copy the filled example below; replace its illustrative content and keep its order and marks. For a first review, omit “Since last review”. Line findings belong in `artifacts/line-comments.json` with the full problem, evidence and concrete ask; the table is their short index, not a second copy of those comments.

Any blocker, major or confirmed Perps anti-pattern requires `REQUEST_CHANGES`. Otherwise, any minor or four or more nits requires `COMMENT` with concrete asks; no blocker, major or minor and at most three nits permits `APPROVE`. Use ❌ for blocker/major, ⚠️ for minor or NOT_CHECKED, and ✅ for a clean result or resolved item. A NOT_CHECKED gap is not a finding unless the missing evidence is owed by the author.

Keep the frozen head, rule and consumer revisions, every rule's PASS/FINDING/NOT_APPLICABLE/NOT_CHECKED outcome, diff scope, cross-repo evidence and earlier rounds in `artifacts/review-ledger.md`. The posted body has one collapsed “Details for agents” section containing only unanchored findings, NOT_CHECKED rows and the ledger pointer/count. Do not post PASS tables or repeat earlier review prose. Use GitHub-flavoured Markdown with no HTML beyond `details`/`summary`.

```markdown
VERDICT: REQUEST_CHANGES
COMMIT: 0123456789abcdef0123456789abcdef01234567

Submission can continue after the form closes; one secondary help label also needs correction.
⚠️ NOT_CHECKED: the linked runtime recording was unavailable.
Since last review: ✅ resolved `src/amount.ts:18`; ❌ still open `src/submit.ts:42`; 🆕 new `src/form.ts:12`.

| Severity | file:line | Problem | Ask |
|---|---|---|---|
| ❌ Major | src/submit.ts:42 | Submission outlives its form. | Recheck lifetime after the await. |
| ⚠️ Minor | src/form.ts:12 | Secondary help text names a different setting. | Match the label to its linked setting. |

<details>
<summary>Details for agents</summary>

| Status | Item | Evidence or gap | Ask |
|---|---|---|---|
| ⚠️ NOT_CHECKED | Runtime evidence | The linked recording was unavailable. | Supply a readable capture for the UI claim. |

➖ 54 rules not applicable to this diff; full ledger in the run artifacts: `artifacts/review-ledger.md`.

</details>
```
