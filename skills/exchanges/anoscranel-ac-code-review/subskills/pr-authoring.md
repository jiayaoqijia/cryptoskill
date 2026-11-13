---
name: pr-authoring
domain: software-engineering/pr-authoring
trigger: "\"Open a PR\", \"write the PR description\", \"this PR is too big\", \"prepare this for review\", \"stack these PRs\", \"self-review my diff\"."
anti_trigger: "Reviewing someone else's diff (subskills/code-review.md); commit message wording and history repair; branch protection."
scope: "Preparing a change for review: size, description, self-review, review packet"
status: "seedling"
---

# PR Authoring

## Standard

- **Google "Small CLs"**: "100 lines is usually a reasonable size for a CL, and 1000 lines is usually too large." File spread counts too. Right size = one self-contained change, with its tests (https://google.github.io/eng-practices/review/developer/small-cls.html).
- ⚠️ SmartBear/Cisco study: review 200–400 LOC at a time, in 60–90 minutes. Vendor rung, c. 2006.
- Reviewers should respond within one business day at most (https://google.github.io/eng-practices/review/reviewer/speed.html).
- Review mainly spreads knowledge and improves code; defect finding is lower than assumed (Bacchelli & Bird, ICSE 2013).
- **Stacked PRs**: small dependent changes reviewed in order (Graphite, Gerrit, Phabricator).
- **Review packet**: diff + test report + eval result + provenance + rollback note.

## Decision rules

1. One PR = one self-contained change. Aim near 100 changed lines; split above about 400. ⚠️ 400 is a house line between the two sources.
2. Exceptions: whole-file deletions and trusted automated refactors (Google Small CLs).
3. Split by: refactor first, then behaviour; by layer of a stack; by file group that compiles alone.
4. Put mechanical changes (renames, formatting) in their own PR.
5. The description lets a reviewer judge the change without asking you.
6. Self-review the diff before requesting review. Fix what you find.
7. CI green before you request review.
8. Agent-written PRs carry the full review packet, and a human author vouches for the change.

## Procedure

1. Run local gates and tests. Push.
2. Read your own diff in the review tool, top to bottom. Remove debug code, stray files, commented-out code.
3. Count size: `git diff --stat origin/main`. Over the limit → split with rule 3, or stack.
4. Write the description:
   ```markdown
   ## What
   One paragraph.
   ## Why
   Problem and link (REQ, issue, spec, ADR).
   ## How
   Key design points; anything surprising.
   ## Testing
   Tests added or run; manual steps with results.
   ## Risk and rollback
   Blast radius; flag name; how to revert.
   ## Reviewer notes
   Where to start; what to look at hardest.
   ```
5. For agent-written code add: agent and model used, prompt or task file link, eval/test report, files the agent was told not to touch.
6. Add screenshots or recordings for UI changes.
7. Request reviewers from CODEOWNERS. Mark draft if not ready.
8. Answer every comment: fix, or explain and resolve. Push fixes as new commits during review; squash at merge.
9. Re-request review after changes.

## Anti-patterns

- 2000-line PR "because it is all related".
- Description that says "see commits".
- Requesting review on red CI.
- Mixing formatting with logic.
- Force-pushing over reviewed commits mid-review.
- Agent PR with no provenance.

## Done checklist

- [ ] One self-contained change, size within limit or justified.
- [ ] Self-review done.
- [ ] CI green.
- [ ] Description covers what, why, how, testing, risk, rollback.
- [ ] Review packet attached for agent-written code.
- [ ] Every comment answered.

## Sources

- https://google.github.io/eng-practices/review/developer/small-cls.html
- https://google.github.io/eng-practices/review/reviewer/speed.html

