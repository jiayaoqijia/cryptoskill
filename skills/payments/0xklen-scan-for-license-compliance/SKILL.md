---
name: scan-for-license-compliance
description: Use when shipping third-party code and a license policy must be met. Inventories every dependency's license and flags copyleft or unknown terms before release.
---

# Scan for License Compliance

A single GPL dependency linked into a proprietary binary is a legal problem, and "unknown" licenses are the ones lawyers lose sleep over. Inventory licenses from the shipped graph and diff against an explicit allow list.

## Procedure

1. Scan the resolved dependencies, per ecosystem:
   - Node: `npx license-checker --production --json > licenses.json`
   - Python: `pip-licenses --format=json --with-license-file > licenses.json`
   - Go: `go-licenses check ./...` or `go-licenses csv ./...`
   - Rust: `cargo license --json` or `cargo deny check licenses`
   - JVM: `mvn license:aggregate-add-third-party`
2. For deep or mixed trees use ScanCode: `scancode -clpieu --json out.json vendor/` (it reads LICENSE files, not just metadata, and catches missing declarations).
3. Define the policy as data. Allow: MIT, Apache-2.0, BSD-2/3-Clause, ISC, MPL-2.0 (weak copyleft, per-file). Review: LGPL-2.1/3.0 (dynamic linking question). Deny: GPL-2.0/3.0, AGPL-3.0, SSPL, and any `UNKNOWN`/empty license.
4. Compare and fail on deny-list hits or unknowns:
   `cargo deny check licenses` with `[licenses] allow = ["MIT", "Apache-2.0"]`, or filter `licenses.json` with `jq`.
5. Handle transitive hits by traceback: find who pulls the GPL package (`npm ls <pkg>`) and either replace it, drop the feature, or seek legal sign-off in writing.
6. For dual-licensed packages (e.g. `MIT OR Apache-2.0`), record which side you rely on.
7. Ship the attribution file the licenses require (Apache-2.0 NOTICE, MIT copyright lines): generate `THIRD_PARTY_LICENSES` and keep it in the release.
8. Re-run on every dependency change; a new transitive import is how violations enter.

## Pitfalls

- Scanning only direct dependencies misses the transitive package that carries the GPL.
- Dev-only dependencies do not ship, so exclude them with `--production`; reporting them as violations wastes review time.
- A package with no `LICENSE` file may still be licensed by its `package.json` field — check both before marking unknown.
- SPDX expressions with `AND`/`OR` differ from a bare `MIT OR GPL-3.0`; you must actually elect a branch.
- Copying a license into a vendored tree does not satisfy attribution for a distributed binary; the notices travel with the artifact.

## Verification

    go-licenses check ./... && jq '[.[] | select(.licenses=="UNKNOWN")] | length' licenses.json

No deny-listed license and zero `UNKNOWN` entries, with the attribution file regenerated to match.

Report: "Scanned <N> shipped deps: <allowed classes>; 0 deny-listed, 0 unknown; THIRD_PARTY_LICENSES regenerated and attached."
