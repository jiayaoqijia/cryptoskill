---
name: handle-rpc-rate-limits
description: Use when an RPC endpoint starts returning 429s or JSON-RPC -32005 errors and the workflow must keep running instead of crashing.
---

# Handle RPC rate limits

Rate limiting shows up as an HTTP 429, as an HTTP 200 with JSON-RPC error `-32005` (limit
exceeded), or as a silent cost-budget cap. Back off with jitter, batch reads, and cache
immutable data.

## Procedure

1. Identify the limit kind before reacting. Inspect status code and body, and the rate-limit
   headers where present.

       curl -s -D - -o /tmp/body -X POST "$RPC" -H 'content-type: application/json' \
         --data '{"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]}'
       cat /tmp/body | jq -r '.error.code, .error.message'

   `-32005` / "rate limit exceeded" is a quota error even though the HTTP status is 200.
   Some providers send `x-ratelimit-remaining` and `retry-after`.

2. Back off with full jitter and cap the attempt count. Never retry without jitter — that
   turns one burst into a thundering herd.

       import random, time
       def backoff(attempt, base=0.25, cap=30.0):
           return min(cap, base * 2**attempt) * random.random()

3. Batch independent reads into one JSON-RPC batch array (one HTTP request, N sub-calls) or
   use Multicall3 on-chain — see `batch-reads-with-multicall3`.

       curl -s -X POST "$RPC" -H 'content-type: application/json' --data '[
         {"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]},
         {"jsonrpc":"2.0","id":2,"method":"eth_chainId","params":[]}]'

4. Cache immutable data: chain id, contract bytecode, verified ABI, and any read pinned to a
   block number never change. Re-fetch only what is height-dependent.
5. Narrow `eth_getLogs` ranges: many providers count compute units per scanned block, so a
   10k-block span can cost 10–100× a 1k-block span, and an over-wide range fails as `-32005`.
6. Cap client concurrency (e.g. 5 concurrent requests) so you stay under the per-second limit
   instead of triggering it; ramp only after observing sustained headroom.

## Pitfalls

- Retrying a `-32005` error as if it were a network blip, with no delay, consumes more quota
  and extends the outage.
- A batch of 20 sub-calls can be billed as 20 requests at some providers and as 1 at others;
  do not assume batching is free.
- Caching `eth_blockNumber` or `latest` reads returns stale data; only cache values pinned to a
  block tag.
- Free tiers often cap requests per second *and* compute units per day; solving the short-term
  429 can exhaust the daily budget — track both.
- Ignoring `retry-after` seconds and using your own shorter delay guarantees more 429s.

## Verification

    curl -s -o /dev/null -w '%{http_code}\n' -X POST "$RPC" -H 'content-type: application/json' \
      --data '{"jsonrpc":"2.0","id":1,"method":"eth_blockNumber","params":[]}'

Report the observed limit (status code and error code), the backoff parameters used, and the
number of 429/`-32005` responses during the run.
