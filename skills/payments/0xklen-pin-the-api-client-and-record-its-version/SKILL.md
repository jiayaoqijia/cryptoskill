---
name: pin-the-api-client-and-record-its-version
description: Use when a project ships an SDK or generated client for a third-party API. Pin the exact version, record it at runtime, and read the changelog before bumping — clients break parsers across minors.
---

# Pin the API client and record its version

An SDK on a floating range pulls a breaking minor on a fresh install, passes locally, and fails
in CI. Pin it, record it, and read the changelog before you move it.

## Procedure

1. Pin to an exact version in the lockfile: `pip install client==2.3.1`, `npm ci` against a locked `package-lock.json`, or a committed `go.sum`.
2. Record the active version at runtime and in startup logs:
   ```python
   import client
   log.info("api_client=%s api_version=%s", client.__version__, API_VERSION)
   ```
3. Before any bump, read the client changelog for breaking changes in auth, pagination, or field names.
4. Diff the generated types/models between the old and new client; a removed type is breaking.
5. Prefer a thin hand-written client where a heavy SDK hides the retries and timeouts you must control.
6. Keep the client version and the API version side by side in the README.
7. Re-run the contract/schema tests after a bump, before deploy.

## Pitfalls

- Floating ranges (`^2`, `latest`) pull a breaking minor on a clean install and pass locally.
- Auto-merge bots land client bumps without anyone reading the changelog.
- Two services sharing a lockfile can hold incompatible pins; coordinate the bump.
- SDK defaults for retries, timeouts, and proxies change silently between minors.
- A generated client regenerated from a newer spec drifts from the API version you pinned.

## Verification

    python -c "import client; print(client.__version__)"
    grep -E 'client==' requirements.txt    # both show the same pinned version

Report: "client 2.3.1, API v2, changelog reviewed 2026-10-01; contract tests green."
