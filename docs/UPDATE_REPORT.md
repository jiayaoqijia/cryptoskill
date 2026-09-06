# Registry refresh — 2026-09-06

Refreshed 391 existing skill bundles and added 418 real upstream bundles.
The generated catalog contains **1,759 entries across 14 categories**, including
138 MCP server entries. Imports include bundled references, scripts, library
files and upstream dependency manifests. Eighty executable bits were corrected
against pinned upstream archives.

## Source coverage

- 297 GitHub repositories checked: 221 fetched, 76 unavailable.
- 258 recorded ClawHub sources checked.
- 826 successful source pins, covering 4,432 files.
- 17 bundles were already unchanged.
- 558 existing entries have no fetchable GitHub/ClawHub skill source.
- 183 existing entries have no unique upstream SKILL.md match.
- 121 existing entries could not be fetched or failed publisher verification.
- 181 updates/additions were blocked by validation or the existing security gate
  (71 existing entries preserved; 110 prospective additions not installed).
- GitHub discovery found 15 candidate repositories before its unauthenticated
  search rate limit was reached. Remaining discovery queries are explicitly
  recorded as skipped.

These are fetch and heuristic validation outcomes, not independent audits.
Detailed per-entry results are in [sync-report.json](sync-report.json);
search outcomes are in [discovery-report.json](discovery-report.json).

## Implementation

The updater reads recorded source attribution, fetches immutable revisions,
validates staged bundles, preserves local overlays, and records successful file
hashes in `scripts/source-lock.json`. Reference-only changes and removed files
owned by previous syncs are handled. Unchanged repositories can skip archive
fetches after a completed scan and matching local hashes. Failed updates do not
advance source pins. Generated catalog classification now comes from SOURCE.md,
and source dates feed freshness scoring.

The rebuild regenerates scores, trust manifests, pages, category indexes,
sitemap and aggregate statistics. Related-skill links now work across categories.
Playwright was updated to 1.63.0; registry Python dependencies are pinned to
ruamel.yaml 0.19.1 and rfc8785 0.1.4. GitHub Actions use current v7 releases,
with weekly Dependabot updates configured for all three dependency ecosystems.

## Verification

- 21 Python regression tests passed.
- 23 Playwright browser/data tests passed.
- All 1,759 canonical trust manifests parsed successfully.
- All 4,432 recorded file hashes matched the installed files.
- All catalog detail pages exist.
- 18,895 related-skill links checked; none broken.
- npm dependency audit: no reported vulnerabilities.
- Existing QuantaBot files were preserved byte-for-byte. The preexisting
  `quantaBot`/`quantabot` case collision remains; this case-insensitive checkout
  exposes one physical directory, and its existing detail page was preserved.

## Continuing updates

Run `bash scripts/run-bot.sh`, or add `--discover-github` for broader discovery.
The six-hour workflow is in `.github/workflows/auto-update.yml` and activates
when these changes reach the default branch with Actions enabled. It tests before
committing skills and generated artifacts together. The website publishes from `main:/docs`; scheduled bot commits explicitly request
a Pages rebuild.

See [MAINTENANCE.md](MAINTENANCE.md) for setup and supported command options.
