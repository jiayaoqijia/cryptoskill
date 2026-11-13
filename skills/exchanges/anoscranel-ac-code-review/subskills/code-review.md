---
name: code-review
domain: software-engineering/code-review
trigger: "\"Review this PR\", \"look over my diff\", \"is this change OK to merge\", \"what should I check in this review\", \"approve or request changes\"."
anti_trigger: "Preparing your own change for review (subskills/pr-authoring.md); governing agent-written code as a whole; security sign-off on a control is out of scope for this tree."
scope: "Reviewing someone's diff: what to check, comment labels, response time, approve rules"
status: "seedling"
---

# Code Review

## Standard

- **Google eng-practices, "What to look for"**: design, functionality, complexity, tests, naming, comments, style, documentation (https://google.github.io/eng-practices/review/reviewer/looking-for.html).
- **Approve rule**: approve once the change definitely improves overall code health, even if it is not perfect (https://google.github.io/eng-practices/review/reviewer/standard.html).
- **Speed**: "One business day is the maximum time it should take to respond" (https://google.github.io/eng-practices/review/reviewer/speed.html). No 4-hour rule exists.
- **Comment labels**: Conventional Comments — `praise`, `nitpick`, `suggestion`, `issue`, `todo`, `question`, `thought`, `chore`, decorated `(blocking)` or `(non-blocking)` (https://conventionalcomments.org).
- **Tests are reviewed too**: does a test "actually fail when the code is broken"? (looking-for.html).

## Decision rules

1. Review in this order: design → functionality → tests → complexity → naming and comments → style. Stop at the first blocking design problem and say so.
2. Mark every comment blocking or non-blocking. Style points a linter can catch are non-blocking; ask for the lint rule instead.
3. Approve when the change improves code health and has no blocking issue. Do not hold a change hostage for polish.
4. Request changes for: wrong behaviour, vacuous or missing tests, a hard-to-undo design, unexplained complexity, a broken public contract.
5. Diff over about 400 changed lines → ask for a split first. ⚠️ House line between Google (100 good, 1000 too large) and SmartBear (200–400 LOC per sitting; vendor, c. 2006).
6. Respond within one business day, or send a first-pass note with an ETA.
7. Agent-written diffs: the reviewer must not be the same model that wrote them. Require the review packet: diff, test report, provenance, rollback note.
8. Merge to protected main stays **human-gated**.

## Procedure

1. Read the description and linked issue. Restate the intent in one line; if you cannot, ask the author.
2. CI red → return it without review.
3. Read the whole diff once for shape, then file by file.
4. For each test, break the code in your head. Would the test fail? If not, flag `issue (blocking)`.
5. Run the change locally when it has UI, data or migration risk.
6. Write labelled comments:
   ```text
   issue (blocking): this retries on 4xx too; a 400 loops forever.
   suggestion (non-blocking): extract parse_header() for reuse.
   question: why 30 s here and 5 s in the client?
   ```
7. Summarise: verdict, blocking count, what you did not review.
8. After fixes, re-review the changed parts.

## Anti-patterns

- "LGTM" with no sign of reading.
- Style debates a formatter should settle.
- Unlabelled comments.
- Line-by-line review of a 2000-line diff instead of asking for a split.
- Same-model self-review of agent code.

## Done checklist

- [ ] Intent restated; CI green.
- [ ] Design, behaviour and tests checked; each test can fail.
- [ ] Every comment labelled blocking or non-blocking.
- [ ] Verdict and unreviewed areas stated.
- [ ] Responded within one business day.

## Sources

- Google eng-practices URLs and conventionalcomments.org, as cited above
- <https://go.dev/blog>
- <https://google.github.io/eng-practices/review/reviewer/looking-for.html>
