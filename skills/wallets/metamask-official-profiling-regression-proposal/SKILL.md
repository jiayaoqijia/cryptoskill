---
name: profiling-regression-proposal
description: >-
  Proposes follow-up actions for an already-classified Hermes CPU-profile
  regression using only the profiling evidence supplied by the caller. Use
  after deterministic tooling has identified a slow scenario and correlated
  hot-frame paths with files from recently merged pull requests.
maturity: stable
---

# Profiling Regression Proposal

Produce a short, evidence-bound proposal after deterministic profiling tooling
has already classified a run. This skill interprets evidence; it does not decide
whether a regression exists.

## When To Use

Use this skill only when the caller supplies structured evidence containing:

- findings produced by a deterministic threshold;
- hot frames extracted from generated CPU-profile reports;
- recently merged pull requests separated by whether their changed files
  overlap those hot-frame paths.

Do not use source-tree searches, repository knowledge, issue history, PR titles,
or general performance heuristics as additional evidence.

## Workflow

1. Treat the supplied evidence object as the only source of truth.
2. Do not change, second-guess, or reapply the caller's regression threshold.
3. Mention a file, function, timing, ratio, run, or owner only when it appears
   in the evidence.
4. Connect a pull request to a finding only when the caller places it in the
   profile-overlap collection. A title that mentions the affected feature is
   not evidence.
5. A changed file may be discussed only when its path already occurs in a hot
   frame from the generated profile.
6. Pull requests in the no-profile-overlap collection may be named only to say
   the supplied profile cannot implicate them.
7. Do not infer source files, behavior, ownership, causes, or fixes from
   unsymbolicated frames.
8. Several scenarios crossing the threshold in one run are one run-level
   anomaly, not automatically several independent bugs.
9. If no pull request overlaps a profiled path, say so and stop. Do not choose a
   likely culprit.
10. Describe every proposed action as a hypothesis to validate by rerunning the
    same profile, never as a confirmed root cause.

## Output

Return Slack mrkdwn:

- first line:
  `*AI proposal (profiling evidence only; not a root cause)*`;
- at most six bullets;
- one sentence per bullet;
- pull-request links formatted as `<url|#number>`;
- no general disclaimer beyond the required first line.

Good:

> PR #123 changed a file that appears as a hot frame; rerun the same scenario
> with that change isolated and compare the frame's self time.

Not allowed:

> PR #123 is the cause because its title mentions Perps.

The title is routing context, not profiling evidence.

## Failure behavior

Return no proposal when the evidence is missing or malformed. Never fill gaps
with repository knowledge or generic optimization advice.
