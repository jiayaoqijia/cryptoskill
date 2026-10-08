---
name: scrape-legally-and-respect-robots-txt
description: Use when collecting data from websites. Checks robots.txt, terms of service, and applicable law before crawling, and stops when they forbid it.
---

# Scrape Legally and Respect robots.txt

The technical ability to fetch a page is not permission to fetch it. Read the rules first; a crawl that violates them is a liability regardless of how clean the code is.

## Procedure

1. Read `robots.txt` before the first request: `curl -s https://example.com/robots.txt`. Honour `Disallow` for your user-agent and check `Crawl-delay`. Do not fetch a path a rule excludes.
2. Identify yourself honestly. Set a descriptive UA with a contact: `curl -A "research-bot/1.0 (+mailto:you@example.com)" ...`. Never spoof a browser to slip past a block.
3. Read the Terms of Service for the specific prohibition. Search the page: `curl -s https://example.com/tos | grep -inE 'scrap|crawl|robot|automated|bulk'`. "No automated access" means stop.
4. Check the legal frame that applies: unauthorised access can implicate the CFAA (US) and ToS breach can be a contract claim; personal data triggers GDPR/CCPA obligations. When in doubt, use an official API or a licensed dataset instead.
5. Do not defeat controls. Bypassing a login wall, CAPTCHA, or IP block is the line between scraping and unauthorised access.
6. Prefer the API, the bulk export, or the public dataset dump (`data.gov`, Common Crawl) over crawling an HTML site.
7. Log the robots.txt decision and its timestamp in your notes so the choice is auditable.

```bash
curl -s https://example.com/robots.txt | grep -iE 'User-agent|Disallow|Crawl-delay' 
# then verify your path is permitted before building the crawler
```

## Pitfalls

- robots.txt is per-user-agent and per-path; a global `Disallow: /` is not overridden by a friendlier section for another bot.
- A `403` is an answer, not a barrier to route around with a proxy; stop and report it.
- Public availability is not the same as a redistribution licence — the licence lives in the ToS or a header.
- Scraping personal data (names, emails, profiles) has stricter rules than scraping product prices.
- Rate is part of compliance: hammering an allowed path can still breach a `Crawl-delay`.
- A site can change its robots.txt between your crawl planning and your run; re-fetch it at crawl start, not from a cached copy.

## Verification

    curl -s https://example.com/robots.txt; echo "decision logged: allowed=/path per $(date -u)"

Report: "robots.txt permits /path for this UA; ToS has no anti-scraping clause; using official API for the rate-limited endpoint."
