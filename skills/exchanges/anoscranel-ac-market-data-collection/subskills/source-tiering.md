---
name: source-tiering
domain: crypto-trading/source-tiering
trigger: "Free vs paid (vendor tiering example: a data vendor with $29-$699 monthly tiers and no free API); rate limits; terms-of-service boundaries; when the only source is a web page that must be scraped - and how to record that provenance."
anti_trigger: "Not for the analysis itself, not for the trade record or risk budget."
scope: "Free vs paid (vendor tiering example: a data vendor with $29-$699 monthly tiers and no free API); rate limits; terms-of-service boundaries; when the only source is a web page that must be scraped - and how to record that provenance."
status: seedling
---

# Source Tiering

## Standard
Market data pipelines frequently rely on a hybrid of free public APIs, commercial vendor feeds ($29 to $699+ monthly tiers), and direct web page scraping when structured APIs are absent. Pipelines must implement transparent source tiering, strictly respect rate limits and terms of service, and document complete provenance records whenever data is harvested via web scraping.

Primary sources for the claims in this step: <https://www.cloudflare.com/learning/bots/what-is-a-bot/> and <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>.

## Decision rules
- **Vendor tier awareness:** Pipelines interacting with tiered APIs (e.g., platforms with $29, $199, and $699 monthly subscription tiers) must handle feature gating, rate quotas, and pagination limits gracefully without crashing.
- **Scraping fallback protocol:** When an exchange or data provider offers no free programmatic API, verified web scraping is permitted provided it respects robots.txt directives, enforces request pacing, and records raw HTML snapshots.
- **Provenance metadata:** Every scraped or API-derived record must store exact provenance attributes including source URL, HTTP status code, retrieval timestamp, and extraction method.
- **Zero-cost preference:** Pipelines must exhaust free public API tiers and high-reliability open data endpoints before routing collection through paid subscription infrastructure.

## Procedure
1. Inventory available data sources for the target market variable, categorizing them into free public APIs, commercial vendor feeds, and scraped web pages.
2. Evaluate rate limits, pricing tiers, authentication requirements, and historical depth constraints for each candidate source.
3. Implement adapter modules that abstract source-specific retrieval logic while outputting a standardized internal data schema.
4. For scraped web sources, capture raw HTML payloads alongside extracted structured data to enable downstream auditing.
5. Embed source identifier tags and retrieval metadata directly into every persisted record header.
6. Establish automated monitoring for source availability, HTTP error rates, and quota consumption thresholds.

## Anti-patterns
- **Hardcoding paid dependencies:** Relying exclusively on expensive proprietary vendor feeds without fallback routes to free public endpoints.
- **Unmetered web scraping:** Harvesting web pages at high frequencies without request pacing, triggering IP blocks and CAPTCHA walls.
- **Untracked data provenance:** Storing cleaned numerical values without retaining records of their original source URL or API endpoint.
- **Violating terms of service:** Bypassing explicit exchange or vendor rate-limiting mechanisms via unauthorized credential sharing or scraping prohibited endpoints.

## Done checklist
- [ ] Data sources are categorized by availability, pricing tier, and reliability metrics.
- [ ] Retrieval adapters standardize incoming payloads into uniform internal data schemas.
- [ ] Web scraping fallback routines capture raw HTML snapshots and enforce strict rate pacing.
- [ ] Provenance metadata (source URL, retrieval timestamp, HTTP status) is stored with every record.

## Sources
- Requests Library Documentation. (2026). HTTP client configuration, timeouts, and header management for Python. Retrieved from https://docs.python-requests.org/
- Beautiful Soup Documentation. (2026). Parsing HTML and XML documents for data extraction. Retrieved from https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- CoinGlass Analytics. (2026). Commercial derivatives data tiers and API access limitations. Retrieved from https://www.coinglass.com/
- Cloudflare. (2026). Understanding web scraping protection, rate limiting, and bot management. Retrieved from https://www.cloudflare.com/learning/bots/what-is-a-bot/
