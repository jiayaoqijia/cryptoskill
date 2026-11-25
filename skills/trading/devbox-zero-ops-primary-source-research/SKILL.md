---
name: primary-source-research
description: >-
  Zero-dependency Python CLI for direct lookup across 22 official zero-API-key
  primary data sources—macroeconomics (FRED CSV series + YoY/MoM threshold base
  rates, US Treasury TGA & national debt, ECB reference FX, World Bank GDP &
  indicators), regulatory & government filings (SEC EDGAR, US Federal Register,
  OpenFDA Drugs@FDA, NIH ClinicalTrials.gov, CISA KEV), science & earth
  observation (arXiv, USGS earthquakes, Open-Meteo WMO/NOAA weather, Launch
  Library 2), developer registries (GitHub, PyPI, npm, HuggingFace), Web3 &
  markets (DefiLlama, Snapshot DAO, Coinbase, Kraken), sports (ESPN), plus
  universal RSS/Atom parsing, plain-HTTP judge-readable URL verification, and
  citation bundle auditing.
---

# primary-source-research

Query 22 official zero-API-key primary data sources, verify plain-HTTP URL readability, and audit citation bundles from a single standard-library Python script (`scripts/research_toolkit.py`).

- **Runtime:** Python 3.8+ standard library only (`urllib`, `json`, `csv`, `xml.etree.ElementTree`, `argparse`). Zero third-party installs.
- **Auth:** Zero API keys required across all 22 primary endpoints. Optional `RESEARCH_SEC_USER_AGENT` env var customizes the SEC EDGAR fair-access `User-Agent` header.
- **Safety default:** Strictly read-only HTTP GET/GraphQL queries plus local citation validation; never modifies remote state or stores credentials.

## When to Use

- Verifying **macroeconomic releases and thresholds** directly from official primary records: **FRED** CSV series (with exact next-month MoM math & historical base rates), **US Treasury** TGA cash balance & Debt to the Penny, **ECB** daily reference FX rates, and **World Bank** country indicators.
- Retrieving **regulatory, corporate, health, and security records**: **SEC EDGAR** filings (`10-K`, `10-Q`, `8-K`, `S-1`), **US Federal Register** rules/orders, **OpenFDA** Drugs@FDA approvals, **NIH ClinicalTrials.gov** trial milestones, and **CISA KEV** exploited vulnerabilities.
- Checking **scientific, earth-observation, and aerospace feeds**: **arXiv** preprints, **USGS** real-time earthquakes, **Open-Meteo** WMO/NOAA/DWD daily weather, and **Launch Library 2** orbital launches.
- Tracking **software, model, Web3, and sports primary state**: **GitHub** releases/tags/Actions, **PyPI** & **npm** package publish timestamps, **HuggingFace Hub** models, **DefiLlama** TVL, **Snapshot** DAO quorum math, cross-checked **Coinbase + Kraken** crypto spot, **ESPN** sports news, and arbitrary **RSS/Atom** feeds.
- Auditing **citation reliability**: checking whether linked URLs are plain-HTTP / judge-readable (`check-url`) without JavaScript or bot walls, and validating research notes + links + attachments (`validate`).

## CLI Usage Examples

Run `scripts/research_toolkit.py` from the skill directory:

```bash
# 1. Inspect the full 22-source catalog
python scripts/research_toolkit.py list-sources

# 2. FRED macro series lookup + exact YoY threshold & 15-year historical base rate
python scripts/research_toolkit.py fred --series CPIAUCSL --limit 6
python scripts/research_toolkit.py fred \
  --series CPIAUCSL \
  --target-yoy 3.0 \
  --years 15 \
  --out-csv ./cpi_threshold_proof.csv

# 3. US Treasury TGA cash balance, ECB FX, and World Bank GDP growth
python scripts/research_toolkit.py treasury --dataset tga --limit 3
python scripts/research_toolkit.py ecb-fx --currency USD --limit 5
python scripts/research_toolkit.py worldbank --country USA --indicator NY.GDP.MKTP.KD.ZG --limit 5

# 4. SEC EDGAR filings, Federal Register, OpenFDA, ClinicalTrials.gov, and CISA KEV
python scripts/research_toolkit.py sec --cik 0000320193 --form 10-K --limit 3
python scripts/research_toolkit.py fedreg --term "semiconductor export" --limit 3
python scripts/research_toolkit.py openfda --query OZEMPIC --limit 3
python scripts/research_toolkit.py clinicaltrials --query "tirzepatide" --limit 3
python scripts/research_toolkit.py kev --keyword "openssl" --limit 5

# 5. Science, weather, earthquakes, and space launches
python scripts/research_toolkit.py arxiv --query "prompt caching" --limit 3
python scripts/research_toolkit.py usgs-quake --min-mag 5.5 --limit 3
python scripts/research_toolkit.py weather --lat 40.7128 --lon -74.0060 --past-days 3 --forecast-days 3
python scripts/research_toolkit.py launches --search SpaceX --limit 3

# 6. Developer registries, HuggingFace, Web3/markets, sports, and generic Atom/RSS
python scripts/research_toolkit.py github --repo python/cpython
python scripts/research_toolkit.py pkg --ecosystem pypi --name requests
python scripts/research_toolkit.py pkg --ecosystem npm --name typescript
python scripts/research_toolkit.py hf --search Qwen2.5 --limit 3
python scripts/research_toolkit.py defillama --slug aave
python scripts/research_toolkit.py crypto-spot --base BTC
python scripts/research_toolkit.py espn --sport basketball --league nba --limit 3
python scripts/research_toolkit.py rss --url https://github.com/python/cpython/releases.atom --limit 3

# 7. Verify plain-HTTP / judge-readable URL accessibility & validate a citation bundle
python scripts/research_toolkit.py check-url --url https://pypi.org/pypi/requests/json --preview 160
python scripts/research_toolkit.py validate \
  --note-file ./research_note.txt \
  --link https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.KD.ZG?format=json \
  --check-links
```

### Subcommand Reference

| Subcommand | Key Flags & Defaults | Primary Source(s) |
| --- | --- | --- |
| `list-sources` | *(none)* | Structured JSON catalog of all 22 built-in primary sources |
| `fred` | `--series` (req), `--limit 12`, `--target-yoy`, `--out-csv`, `--years 15` | St. Louis Fed FRED CSV + YoY/MoM base-rate calculator |
| `treasury` | `--dataset tga\|debt`, `--limit 5` | US Treasury Fiscal Data API (TGA balance & national debt) |
| `fedreg` | `--term` (req), `--limit 5` | US Federal Register API v1 |
| `ecb-fx` | `--currency USD`, `--limit 10` | European Central Bank daily reference FX rates CSV |
| `worldbank` | `--country USA`, `--indicator NY.GDP.MKTP.KD.ZG`, `--limit 5` | World Bank Open Data v2 |
| `sec` | `--cik` (req), `--form ""`, `--limit 8` | SEC EDGAR official submissions JSON |
| `openfda` | `--query` (req), `--limit 5` | US FDA Drugs@FDA approval & submission records |
| `clinicaltrials` | `--query` (req), `--limit 5` | NIH/NLM ClinicalTrials.gov REST API v2 |
| `usgs-quake` | `--min-mag 5.5`, `--limit 5` | USGS real-time earthquake GeoJSON API |
| `weather` | `--lat` (req), `--lon` (req), `--past-days 5`, `--forecast-days 5` | Open-Meteo WMO/NOAA/DWD daily temperature & precipitation |
| `kev` | `--keyword ""`, `--limit 8` | CISA Known Exploited Vulnerabilities (KEV) JSON catalog |
| `arxiv` | `--query` (req), `--limit 5` | arXiv Atom preprint search API |
| `github` | `--repo owner/repo` (req) | GitHub REST API (latest release, tags, recent Actions runs) |
| `pkg` | `--ecosystem pypi\|npm` (req), `--name` (req) | PyPI JSON API & npm Registry JSON API |
| `hf` | `--search` (req), `--limit 8` | HuggingFace Hub models REST API |
| `launches` | `--search ""`, `--limit 5` | Launch Library 2 (TheSpaceDevs) upcoming orbital launches |
| `defillama` | `--slug` (req) | DefiLlama protocol TVL & 7-day delta |
| `snapshot` | `--id` (req) | Snapshot GraphQL DAO governance tally & quorum math |
| `crypto-spot` | `--base BTC` | Cross-checked Coinbase Spot + Kraken Ticker APIs |
| `espn` | `--sport basketball`, `--league nba`, `--keyword ""`, `--limit 5` | ESPN public sports news JSON feed |
| `rss` | `--url` (req), `--keyword ""`, `--limit 8` | Universal RSS 2.0 / Atom primary feed parser |
| `check-url` | `--url` (req), `--preview 0` | Plain-HTTP / judge-readable accessibility & bot-wall checker |
| `validate` | `--note-file` (req), `--link`, `--file`, `--max-items 3`, `--allow-secondary`, `--check-links` | Research citation bundle hygiene & live link verifier |

## Output Schema

Every subcommand emits UTF-8 JSON to `stdout` (and structured `{ "error", "command" }` JSON to `stderr` with exit code `1` on failure). Every source query returns a canonical `source_url` for direct citation.

### `worldbank` / `ecb-fx` / `pkg`

```json
{
  "country": "USA",
  "indicator": "NY.GDP.MKTP.KD.ZG",
  "source_url": "https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.KD.ZG?format=json&per_page=10",
  "observations": [
    {
      "year": "2024",
      "value": 2.7962,
      "indicator": "GDP growth (annual %)",
      "country": "United States"
    }
  ]
}
```

### `fred` (with optional `--target-yoy`)

```json
{
  "series": "CPIAUCSL",
  "source_url": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL",
  "observations_total": 948,
  "latest_date": "2026-10-01",
  "latest_value": 318.42,
  "latest_mom_pct": 0.21,
  "latest_yoy_pct": 2.74,
  "recent_observations": [{ "date": "2026-10-01", "value": 318.42 }],
  "threshold_analysis": {
    "base_date_for_next_yoy": "2025-11-01",
    "base_value_for_next_yoy": 310.12,
    "target_yoy_pct": 3.0,
    "required_next_value": 319.4236,
    "required_next_mom_pct": 0.3152,
    "next_calendar_month": 11,
    "lookback_count": 15,
    "historical_hits_gte_required": 4,
    "base_rate_pct": 26.67,
    "csv_path": "./cpi_threshold_proof.csv"
  }
}
```

### `check-url`

```json
{
  "url": "https://pypi.org/pypi/requests/json",
  "status": 200,
  "content_type": "application/json",
  "sample_bytes": 65536,
  "clean_text_len": 65536,
  "plain_http_readable": true,
  "judge_readable": true,
  "needs_attachment": false,
  "js_or_bot_wall": false
}
```

### `validate`

```json
{
  "valid": true,
  "item_count": 2,
  "note_chars": 142,
  "file_bytes": 0,
  "link_checks": [],
  "issues": []
}
```

## Source Catalog & Citation Rules

Read [references/sources-catalog.md](references/sources-catalog.md) before bulk polling or publishing research reports:

- Complete table of all 22 official zero-API-key endpoint patterns and per-provider rate limits
- Retry/backoff rules (`Retry-After` handling on HTTP `429`/`5xx`)
- Primary-source citation hygiene, ISO-date anchoring, and plain-HTTP fallback archiving rules

## Operational Caveats

- **Public rate limits:** Unauthenticated GitHub (`60 req/hr`), Launch Library 2 (`15 req/hr`), OpenFDA (`40 req/min`), and SEC EDGAR (`10 req/s`) enforce strict fair-access limits. Cache responses locally when running repeated research loops.
- **SEC EDGAR User-Agent compliance:** Set `RESEARCH_SEC_USER_AGENT="YourOrg/1.0 (contact@yourdomain.com)"` when running production SEC lookups so requests carry your own fair-access contact string.
- **Plain-HTTP verification vs. browser rendering:** `check-url` intentionally uses plain HTTP without JavaScript execution or cookies so you know whether automated readers, reviewers, or archiving scripts can fetch the cited page directly.

## Ecosystem & Resources

- **Open-Source Toolkits on GitHub:** [devbox-zero-ops on GitHub](https://github.com/devbox-zero-ops) — zero-dependency CLI utilities and open-source developer tools.
- **Free Browser Developer Suite:** [XiaheAI Hub](https://devbox-zero-ops.github.io/xiaheai-hub/) — local, zero-tracking web calculators and developer workflows.
- **Commercial White-Label Source Bundle:** [XiaheAI ZeroSuite Pro](https://devbox-zero-ops.github.io/xiaheai-hub/pro.html) — full multi-tool self-hostable source kit for teams.
