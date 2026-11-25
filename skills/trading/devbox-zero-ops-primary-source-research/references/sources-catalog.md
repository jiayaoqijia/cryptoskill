# Primary Source Catalog & Citation Rules

Complete reference for the 22 zero-API-key official primary sources, universal feed parser, and verification utilities implemented in `scripts/research_toolkit.py`.

## 1. All 22 Zero-API-Key Primary Endpoints

| # | Source | CLI Subcommand | Official Endpoint Pattern | Auth / Headers | Practical Rate-Limit Guidance |
| --- | --- | --- | --- | --- | --- |
| 1 | **FRED (St. Louis Fed)** | `fred` | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIES>` | None | Polite polling (`<= 1 req/s`); CSV updates on scheduled macro release dates |
| 2 | **US Treasury Fiscal Data** | `treasury` | `https://api.fiscaldata.treasury.gov/services/api/fiscal_service/...` | None | Public federal API; keep `page[size] <= 100` and cache daily DTS/debt pulls |
| 3 | **US Federal Register** | `fedreg` | `https://www.federalregister.gov/api/v1/documents.json` | None | Generous public JSON API; filter by `conditions[term]` and `per_page` |
| 4 | **ECB Reference FX** | `ecb-fx` | `https://data-api.ecb.europa.eu/service/data/EXR/D.<CUR>.EUR.SP00.A` | None | Published ~16:00 CET on TARGET business days; query `lastNObservations` |
| 5 | **World Bank Open Data** | `worldbank` | `https://api.worldbank.org/v2/country/<ISO3>/indicator/<IND>?format=json` | None | Public REST v2; annual/quarterly updates, avoid rapid tight loops |
| 6 | **SEC EDGAR** | `sec` | `https://data.sec.gov/submissions/CIK<10-DIGIT>.json` | Custom `User-Agent` (app + contact email) | Strict SEC fair-access cap: `<= 10 req/s`; override via `RESEARCH_SEC_USER_AGENT` |
| 7 | **US FDA Drugs@FDA (OpenFDA)** | `openfda` | `https://api.fda.gov/drug/drugsfda.json` | None | `<= 40 req/min` and `1,000 req/day` without an API key |
| 8 | **NIH ClinicalTrials.gov** | `clinicaltrials` | `https://clinicaltrials.gov/api/v2/studies` | None | Public NIH v2 REST API; keep `pageSize <= 50` and throttle bursts |
| 9 | **USGS Earthquakes** | `usgs-quake` | `https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson` | None | Real-time feed; poll at `>= 60s` intervals and use `--min-mag` filters |
| 10 | **Open-Meteo (WMO/NOAA/DWD)** | `weather` | `https://api.open-meteo.com/v1/forecast` | None | Non-commercial free tier (~10,000 calls/day); cache daily coordinate queries |
| 11 | **CISA KEV Catalog** | `kev` | `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` | None | Full JSON catalog (~1 MB); cache locally for hours rather than polling per-query |
| 12 | **arXiv Preprints** | `arxiv` | `https://export.arxiv.org/api/query` | None | Official guidance: `<= 1 req / 3s` single-connection |
| 13 | **GitHub REST API** | `github` | `https://api.github.com/repos/<owner>/<repo>/{releases/latest,tags,actions/runs}` | None | Unauthenticated limit: `60 req/hr` per IP (3 calls per `github` invocation) |
| 14 | **PyPI JSON Registry** | `pkg --ecosystem pypi` | `https://pypi.org/pypi/<package>/json` | None | Public CDN-backed JSON; avoid high-concurrency scraping |
| 15 | **npm Registry** | `pkg --ecosystem npm` | `https://registry.npmjs.org/<package>` | None | Public registry JSON; scoped packages (`@scope/pkg`) URL-encoded automatically |
| 16 | **HuggingFace Hub** | `hf` | `https://huggingface.co/api/models` | None | Public model metadata API; keep `--limit` small (`<= 25`) |
| 17 | **Launch Library 2 (SpaceDevs)** | `launches` | `https://ll.thespacedevs.com/2.2.0/launch/upcoming/` | Browser UA | Strict free-tier cap: `15 req/hr` per IP; cache upcoming schedule snapshots |
| 18 | **DefiLlama Protocol TVL** | `defillama` | `https://api.llama.fi/protocol/<slug>` | None | Public JSON endpoint; large protocol histories (~1–5 MB), avoid tight polling |
| 19 | **Snapshot DAO Governance** | `snapshot` | `https://hub.snapshot.org/graphql` | None | Public GraphQL POST endpoint; query single proposal IDs on demand |
| 20 | **Coinbase Public Spot** | `crypto-spot` | `https://api.coinbase.com/v2/prices/<SYM>-USD/spot` | None | Public spot price feed (`<= 10 req/s`) |
| 21 | **Kraken Public Ticker** | `crypto-spot` | `https://api.kraken.com/0/public/Ticker?pair=<PAIR>` | None | Public ticker cross-check paired with Coinbase; `<= 1 req/s` |
| 22 | **ESPN Public Sports API** | `espn` | `https://site.api.espn.com/apis/site/v2/sports/<sport>/<league>/news` | Browser UA | Public site JSON feed; poll gently for injury/roster updates |

### Auxiliary Subcommands

| Subcommand | Purpose | Notes |
| --- | --- | --- |
| `rss` | Parse any official RSS 2.0 or Atom feed (e.g., GitHub `releases.atom`, central bank press feeds, government bulletins) | Normalizes RFC 2822 RSS dates into UTC ISO-8601 |
| `check-url` | Simulate a plain-HTTP reader (no JS execution, no cookies) to verify citation accessibility | Flags HTTP errors, Cloudflare/CAPTCHA walls (`js_or_bot_wall`), and PDFs needing local archival |
| `validate` | Audit a research note + citation URLs + local evidence files | Checks ISO-date anchoring (`YYYY-MM-DD`), URL hygiene, duplicate links, primary-source compliance, attachment types/size, and optional live `--check-links` |
| `list-sources` | Emit machine-readable JSON catalog of all 22 primary sources | Useful for autonomous agent tool discovery |

## 2. Retry & Backoff Behavior

`http_get_text()` retries only transient errors (`HTTP 429`, `HTTP 5xx`, or socket timeouts) up to 2 times:
- Honors numeric and HTTP-date `Retry-After` headers when `<= 30s`; fails fast if the server requests a cooldown `> 30s`.
- Never retries client errors (`400`, `401`, `403`, `404`), surfacing the exact HTTP error immediately.

## 3. Primary-Source Citation Best Practices

1. **Prefer primary machine-readable records over secondary commentary:** Cite the exact official document URL (`source_url`, `doc_url`, `html_url`, `url`) returned by the registry or agency rather than social posts, blogs, or betting/prediction-market aggregators.
2. **Anchor every fact with an explicit UTC/ISO date (`YYYY-MM-DD`):** Series like FRED (`CPIAUCSL`), US Treasury TGA, and SEC filings revise or update on fixed schedules; include the exact observation date and retrieval date.
3. **Verify plain-HTTP readability before citing:** Run `check-url --url <URL>` on every external reference. If `plain_http_readable` is `false` (403, bot challenge, JS-only SPA) or `needs_attachment` is `true` (large PDF), archive a local CSV/PDF extract and cite both the canonical URL and the archived artifact.
4. **Show arithmetic explicitly for threshold questions:** For macro thresholds (e.g., whether next month's CPI YoY stays `>= 3.0%`), use `fred --target-yoy 3.0 --out-csv proof.csv` so the required MoM change and historical calendar-month base rate are reproducible from the raw FRED CSV.
5. **Maintain neutral, factual reporting:** Keep notes strictly descriptive (date, metric, source URL, methodology) without directive or manipulative phrasing.
