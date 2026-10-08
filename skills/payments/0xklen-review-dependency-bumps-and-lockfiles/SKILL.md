---
name: review-dependency-bumps-and-lockfiles
description: Use when a PR changes a lockfile or dependency version. Reads the changelog, checks for a major bump, and audits the new transitive tree before approving.
---

# Review dependency bumps and lockfiles

A one-line version change in a lockfile can pull in a hundred new transitive packages and a breaking API change. The diff is small; the blast radius is not.

## Procedure

1. Identify direct version changes, ignoring lock noise: `git diff origin/main...HEAD -- package.json pyproject.toml Cargo.toml go.mod`.
2. Classify each by semver: patch and minor are usually safe; a major bump (`1.x` to `2.x`, `^0.x` caveat) needs the changelog read for breaking changes.
3. Read the upstream release notes for the specific range you are moving across — not the latest tag, the entries between old and new. Look for renamed APIs, dropped runtime versions, and new required config.
4. Count the transitive growth: `npm ls --all | wc -l` before and after, or `pipdeptree --warn silence | grep -c .`. A small direct bump that adds a large subtree deserves scrutiny.
5. Audit the new tree for known CVEs: `npm audit --audit-level=high` or `pip-audit`, and require high/critical findings be resolved or explicitly accepted.
6. Confirm the lockfile change matches the manifest: a hand-edited lockfile with a version that contradicts the manifest will fail `npm ci`.
7. Check the bump is not on the critical path of a security fix that should be expedited separately.

## Pitfalls

- Approving a lockfile-only diff without noticing a new postinstall script in a transitive package.
- A `^` range in the manifest that resolves to different versions on the next `npm install`, so the lockfile pin is the only protection.
- A major bump hidden by a caret: `^0.9.0` to `^0.10.0` is breaking by Go/npm convention for 0.x.
- Auditing only direct dependencies and missing a vulnerable transitive package.

## Verification

    npm ci && npm audit --audit-level=high
    # Python:
    pip install -r requirements.txt && pip-audit

    # Prove the lockfile matches the manifest:
    npm ci --dry-run   # non-zero exit means they disagree

Report each direct bump with its semver class, the count of new transitive packages, and any high/critical advisories. A major bump without a changelog pass is blocking.

## Worked example

`package.json` moves `axios` from `^0.27.0` to `^1.6.0` — a major bump. The changelog shows the error object shape and `params` serialization changed. The lockfile adds three transitive packages and `npm audit` is clean. The reviewer flags the error-shape change as requiring an update in `api/errors.ts`, which the PR never touched, and blocks until it is handled.
