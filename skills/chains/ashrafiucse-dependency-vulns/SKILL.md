---
name: dependency-vulns
description: Checks project dependencies for known vulnerabilities (CVEs, GHSAs, PYSA, RUSTSEC, etc.) against the OSV.dev database. Finds lockfiles/manifests across npm, pip, Poetry, Bundler, Cargo, Composer, Go modules, Maven, NuGet, and Pub, queries live advisories for the exact installed versions, and also flags absent lockfiles, deprecated packages, and unpinned installs. Use when auditing dependencies or investigating a specific package's vulnerabilities.
license: MIT
---

# Dependency Vulnerabilities

## Step 1 — Automated scan (needs network)

```bash
python3 scripts/osv_scan.py <project_root>
```

Stdlib-only Python; parses lockfiles → queries the OSV.dev batch API → prints per-finding: advisory ID, aliases (CVEs), severity, and fixed versions. Read the script's header for supported manifests.

Interpretation rules:
- A finding is **CRITICAL** if the advisory lists a fix AND the vulnerable code path is plausibly reachable from the app's usage (check `require`/`import` sites), or if it's on the CISA KEV list.
- Unreachable-but-present → **HIGH** (upgrades are cheap insurance).
- No fixed version available → note "no fix released yet; mitigation required" and check for vendor workarounds.

## Step 2 — Manifest hygiene (no network needed)

Check and report:

```bash
rg --files -g 'package.json' -g 'pyproject.toml' -g 'Cargo.toml' -g 'go.mod' \
   -g 'Gemfile' -g 'composer.json' -g 'pom.xml' | head
```

- **No lockfile** for an existing manifest (e.g. `package.json` without `package-lock.json`) → HIGH: builds are non-reproducible, a malicious/patched transitive dep can slip in silently.
- **`latest` / `*` / caret-wide ranges in prod manifests** → MEDIUM: pin via lockfile at minimum.
- **Direct git URLs / tarball URLs** instead of registry versions → HIGH (unpinned supply chain).
- **Install scripts risk**: `postinstall` hooks in npm projects — list which deps have them if `package.json` shows lifecycle scripts.
- **Deprecated/archived packages**: `request`, `node-uuid`, `colors`/`faker` (history of compromise), `querystring`, `mkdirp@0`, `moment` (maintenance mode). Check against current knowledge; see `../cve-research/SKILL.md` for live checks.

## Step 2.5 — Supply-chain hygiene (A08: confusion & typosquats)

- **Dependency confusion**: internal/scoped package names (`@corp/...`, `corp-*`) that resolve on PUBLIC registries → an attacker publishes that name and CI installs theirs. Check each internal-looking name:
```bash
rg -o '"@?[\w.-]+/[\w.-]+"|"[\w.-]+"' package.json | sort -u   # candidate names
npm view <name> versions --json 2>/dev/null || echo "not on public registry (good)"
```
With network: a `npm view` that SUCCEEDS for an internal name = **CRITICAL** (register a namespace/proxy instead). Without network: list internal-looking names for manual verification. Same check for pip (`pip index versions`) and Go private modules (`GOPRIVATE` vs proxy.golang.org reachable names).
- **Typosquat heuristics**: dependency names at edit-distance 1 from popular packages (`reqeusts`, `lodash2`, `expresss`, `colors-2`, `-js` suffixed clones of core names) → HIGH until verified legitimate. Notable real-world families: `event-stream`, `ua-parser-js`, `node-ipc`, `coa`, `rc` hijacks — names matter less than the SHAPE: unpopular package, recently published, exact-near-famous-name.
- **Provenance**: registry-signed provenance / lockfile integrity hashes present? (`package-lock.json` `integrity` fields; pip hashes in requirements; `--locked` usage) — absence → MEDIUM note.

## Step 3 — Runtime EOL check (live, free — endoflife.date)

For each runtime/framework/DB the project pins (from Phase 0 recon), check end-of-life status:

```bash
curl -s https://endoflife.date/api/nodejs.json | jq -r '.[] | "\(.cycle)  eol=\(.eol)  latest=\(.latest)"' | head -5
```

Common products: `python`, `nodejs`, `php`, `ruby`, `go`, `laravel`, `django`, `rails`,
`ubuntu`, `debian`, `alpine`, `postgresql`, `mysql`, `redis`, `mongodb`, `nginx`,
`kubernetes`. Compare the installed major/minor prefix against `eol` dates:

- Installed version past EOL → **HIGH**: no security fixes will ever arrive — upgrade path only
- Within 6 months of EOL → MEDIUM (plan the upgrade)
- Note `latest` in the report so the user sees the gap concretely

## Step 4 — Prioritize output

Group findings: (a) fix available + reachable → do now; (b) fix available → next patch window; (c) no fix → mitigation notes (config workaround, feature flag off, WAF rule, virtual patching).

For each finding give: `package@installed_version`, advisory ID + CVE aliases, severity, fixed-in version, and the exact upgrade command for the package manager in use (`npm install x@^y`, `pip install -U x==y`, etc.).

## Notes

- If there's no network, skip Step 1, do Steps 2–3, and say so in the report.
- If OSV returns errors for one ecosystem, continue with the others — don't abort the whole scan.
- **Optional bridge:** if `osv-scanner`/`npm audit`/`pip-audit` is installed (probe: `../security-audit/scripts/probe_tools.sh`), run it and merge results with the OSV API output — dedupe on `package@version` + advisory ID.
- Language-version vulnerabilities (e.g. outdated Python/OpenSSL) are out of scope here; note runtime versions in the report's Stack section if obviously EOL.
