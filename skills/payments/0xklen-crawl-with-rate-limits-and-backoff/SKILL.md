---
name: crawl-with-rate-limits-and-backoff
description: Use when running a crawler or hitting an API in bulk. Applies polite pacing, bounded concurrency, and exponential backoff so the source stays healthy.
---

# Crawl With Rate Limits and Backoff

A crawler that ignores pacing gets itself blocked, degrades the target, and produces a partial dataset you mistake for a complete one.

## Procedure

1. Cap concurrency low: at most 2–4 simultaneous connections per host. Global parallelism of 50 against one server is a denial-of-service in miniature.
2. Enforce a minimum delay per host, e.g. 1 request every 0.5–2 s, and respect `Crawl-delay` if robots.txt sets a larger one.
3. Honour `Retry-After` exactly on 429/503. Never retry sooner and never treat a 429 as success.
4. Back off exponentially with jitter on 5xx/timeouts:
   ```python
   import time, random
   def backoff(attempt): return min(60, 2**attempt) * (0.5 + random.random())
   ```
5. Retry a bounded number of times (3–5), then record the URL as failed and move on. Infinite retries on a dead endpoint waste the whole budget.
6. Cache every response to disk keyed by URL hash; on re-runs read the cache so you never re-hit the source:
   ```python
   import hashlib, pathlib
   key = hashlib.sha1(url.encode()).hexdigest()
   path = pathlib.Path("cache")/key
   ```
7. Track progress in an append-only log with status per URL, so a crash resumes instead of restarting from zero.

```bash
# smallest polite pattern: one request, sleep, one request
for u in "${urls[@]}"; do curl -s "$u" -o "out/$(echo "$u"|md5).html"; sleep 1; done
```

## Pitfalls

- Counters that resume mid-run often double-count or skip; key the state on URL, not on array index.
- Rotating proxies to evade a rate limit is evasion, not politeness — see the robots/ToS skill.
- A 200 response can still be a soft block (a challenge page); validate the body, not just the status.
- Long sleeps without a timeout can hang a worker forever; add a hard per-request timeout.
- Retrying a non-idempotent POST duplicates writes; only auto-retry GETs.

## Verification

    grep -cE '429|503' crawl.log; grep -c 'FAILED' crawl.log

No unresolved 429s remain and failed URLs are a named, bounded set. Report: "Crawled 12,480 URLs at 2 conns/host, 1 s delay; 7 permanent failures logged; cache hit on re-run: 100%."
