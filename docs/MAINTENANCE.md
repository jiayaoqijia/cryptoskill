# Registry maintenance

The repository stores third-party bundles in `skills/<category>/<slug>/`.
`SOURCE.md` holds attribution and classification. `TRUST.md`, when present,
is a local review overlay. Neither is replaced by upstream files.

Python 3.12+ and Node.js 20+ are required. Install the registry's own libraries:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm ci --ignore-scripts
npx playwright install chromium
```

Refresh existing sources, discover new skills within configured repositories,
and rebuild every derived artifact:

```sh
bash scripts/run-bot.sh
```

Additional modes:

```sh
# Include GitHub search and missing watchlist projects.
bash scripts/run-bot.sh --discover-github
# Fetch and validate, without writing bundles, reports, or generated files.
bash scripts/run-bot.sh --dry-run
# Refresh a single GitHub source, or existing entries only.
bash scripts/run-bot.sh --repo moonpay/skills
bash scripts/run-bot.sh --no-discover
# Rebuild from local files without network requests.
.venv/bin/python scripts/refresh-registry.py
# Run regression and browser tests.
.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v
npm test
```

`CRYPTOSKILL_PYTHON` overrides the runner's Python executable. The shell runner
otherwise uses `.venv/bin/python` when available. `GITHUB_TOKEN` or `GH_TOKEN`
enables authenticated GitHub API discovery; tokens are sent only to the GitHub
API. GitHub archives and git revision checks also work without API credentials.
Search can exhaust the unauthenticated rate limit; repository refreshes continue.

## Fetch and update behavior

`scripts/auto-update.py` delegates to `scripts/sync_sources.py`. The inventory
comes from recorded GitHub and ClawHub attribution, the curated repository list,
and watchlist `skills_repo` entries. GitHub sources are resolved to immutable
commit SHAs; ClawHub downloads are pinned to a version after checking the owner.
The public [ClawHub API](https://docs.openclaw.ai/clawhub/api) also supports
GitHub handoffs. Such entries currently require an explicit GitHub source mapping
and are reported without silently following a new source.

Updates include bundled references, scripts, libraries and dependency manifests.
They never execute upstream code or independently upgrade an upstream bundle's
dependencies. The registry's own npm, Python and Actions dependencies are tracked
by Dependabot separately.

Each changed bundle is staged, checked with the existing registry risk gate,
and swapped into place. This applies to official and community entries alike;
the gate is an automated heuristic, not an audit. Invalid paths, oversized
bundles and ambiguous skill matches are rejected. Existing local changes are
preserved. Old upstream files are removed only if a previous successful sync
recorded ownership; preexisting untracked overlays remain intact.

`scripts/source-lock.json` records upstream revisions, skill paths and file
hashes after successful installation. A completed repository scan and matching
local hashes allow subsequent runs to skip unchanged archives. Failed downloads
or rejected bundles do not advance their pins. Unknown licenses are recorded as
`NOASSERTION`, and available upstream license files accompany imported bundles.

`docs/sync-report.json` records each entry's outcome: `added`, `updated`,
`unchanged`, `local_changes`, `unavailable`, `blocked`, `unresolved`,
`listing_only`, or `skipped`. Website-only listings and sources without an
identifiable skill are retained and reported. The report describes the latest
run, so `--repo` intentionally reports other sources as skipped.
`docs/discovery-report.json` records API discovery candidates and query failures.
LLM suggestions no longer create synthetic SKILL.md files or official badges.

## Generated artifacts and scheduling

The build order is catalog → scores → capability manifests → score history →
HTML pages and sitemap → homepage and README statistics. Canonical YAML libraries
are required before generation, so missing dependencies cannot silently remove
trust panels. Source dates advance only when bundle content changes.

`.github/workflows/auto-update.yml` runs every six hours at minute 17 and can be
started manually. It installs pinned dependencies, tests the updater, refreshes
the registry, tests the website, and commits **skills and generated artifacts
together**. Overlapping scheduled runs are serialized. The workflow takes effect
after these changes reach the default branch and GitHub Actions is enabled.
The local runner never commits or pushes.

The website is published by GitHub Pages from `main:/docs` at
`https://cryptoskill.org`. After a scheduled bot commit, the workflow explicitly
requests a Pages build using its `pages: write` permission. GitHub does not
automatically trigger Pages builds for commits pushed with `GITHUB_TOKEN`.
See [GitHub's publishing-source documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

The former `scripts/auto-update.yml` was outside GitHub's workflow directory,
and the old shell runner used Linux-only `sed` calls and could publish partial
results after an error. Both are replaced by the shared build entry point.
`--skip-openclaw` remains an alias for `--skip-clawhub`; `--no-push` is accepted
for compatibility but is unnecessary. Other legacy discovery/security bypass
flags are replaced by the modes documented above.

## Curated platform sources

`scripts/curated-sources.json` records explicit repositories, classifications,
classification evidence, and hosted MCP endpoints. The scheduled updater includes
these sources. Refresh just this collection without replacing the full-run report:

```sh
bash scripts/run-bot.sh --curated --report-path docs/targeted-sync-report.json
```

`--repo` can also be repeated to select several repositories. Community entries
in the curated file carry `official: false`, including the Fomo/Cope Capital and
Robinhood community clients. pump.fun and GMGN use their project repositories.

Robinhood's official hosted Trading MCP has a registry-maintained connection
guide. `hosted_sources.py` checks that Robinhood's public documentation still
names the configured endpoint and writes `docs/hosted-mcp-status.json`. It never
logs into accounts or invokes trading tools. Documentation changes require review
rather than silently replacing the service URL. Its HTTP endpoint is propagated
to the catalog so the site shows a usable MCP connection command.

The seed-phrase detector now checks the English BIP-39 wordlist and checksum,
with a conservative fallback for explicitly labelled seed assignments. It no
longer treats every sequence of twelve ordinary English words as a credential.
Other languages and non-BIP-39 seed schemes are outside that detector's scope.
