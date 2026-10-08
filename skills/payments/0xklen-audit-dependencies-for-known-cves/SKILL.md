---
name: audit-dependencies-for-known-cves
description: Use when checking a project for vulnerable dependencies. Scans the resolved dependency graph against advisory databases and separates reachable risk from noise.
---

# Audit Dependencies for Known CVEs

A vulnerability report is only actionable once you know which resolved version is affected, whether the affected code path runs, and whether a fix exists.

## Procedure

1. Resolve the full graph first — scanners read lockfiles, not `package.json` ranges:
   `npm ci` then `npm audit --json > audit.json`
   Python: `pip-audit -r requirements.txt --format=json`. Rust: `cargo audit --json`. Go: `govulncheck ./...`.
2. Prefer a database-agnostic scanner for coverage across ecosystems:
   `osv-scanner -r .` reads `package-lock.json`, `go.mod`, `Cargo.lock`, and `requirements.txt`.
3. Container images: `grype dir:. -o table` or `trivy image --severity HIGH,CRITICAL myimg:latest`.
4. For each finding record: package, installed version, fixed version, CVSS, and path (`npm ls lodash` shows the requirer).
5. Cut noise by reachability. `govulncheck` and `pip-audit --fix --dry-run` distinguish called functions from mere presence. A CVE in an unused transitive dev dependency is not shipping risk.
6. Triage with a threshold, e.g. block the release on CVSS >= 7.0 with a fix available; track the rest in a dated exception file with an owner and expiry.
7. Apply fixes bottom-up: `npm audit fix` (never `--force` blindly), `pip-audit --fix`, `cargo update -p crate`.
8. Re-run the scanner and confirm the count drops. Store the JSON as a build artifact for trend tracking.

## Pitfalls

- `npm audit` reports the dev-only tree too; a build-tool CVE cannot be exploited at runtime unless the tool runs on untrusted input.
- Advisory data lags. A "0 vulnerabilities" result is "none known yet", not "safe".
- `npm audit fix --force` jumps to a semver-major and can break the build; read the diff first.
- Pinning an old version to silence a warning trades a known bug for a known CVE. Upgrade instead.
- Scanners miss vendored or git-URL dependencies that never enter the lockfile.

## Verification

    osv-scanner -r . --format=json | jq '[.results[].packages[].vulnerabilities[]] | length'

Exit code 0 with a count of 0 (or only accepted exceptions) is a pass. Compare the number against `audit.json` from the previous run to show the direction of travel.

Report: "<N> advisories, <M> reachable and fixable, all upgraded to <versions>; `osv-scanner -r .` now exits clean."
