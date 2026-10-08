---
name: bound-a-fan-out-query
description: Use when a request fans out to many shards, services or items and one slow member can stall the whole response — caps concurrency, sets a per-call deadline and returns partial results instead of hanging.
---

# Bound a fan-out query

A fan-out across N members has latency equal to the *slowest* member, and memory equal to the sum of all. Unbounded fan-out is how a single sluggish shard turns a fast endpoint into a timeout for everyone. Bound the concurrency, bound the deadline, and decide what a partial answer looks like before you need it.

## Procedure

1. Fan out with a *bounded* concurrency, never one goroutine/thread per item. On a 10k-item fan-out, unbounded parallelism saturates file descriptors and the downstream. Use `SetLimit` (Go), `Semaphore` (Python), or a fixed worker pool:
       g, ctx := errgroup.WithContext(ctx); g.SetLimit(20)
       for _, sh := range shards { sh := sh; g.Go(func() error { return queryShard(ctx, sh) }) }

2. Give each member its own deadline *shorter than* the request deadline, so one slow member fails at its own clock rather than consuming the client's whole budget:
       sctx, cancel := context.WithTimeout(ctx, 300*time.Millisecond)
       defer cancel()

3. Define partial-result semantics up front and return them: if 19 of 20 shards answer and one times out, return the 19 with a flag (`partial: true`, `missing: ["shard-7"]`) rather than failing the whole request. Callers can then choose to show an incomplete count or retry the gap.

4. Cap the *total* work, not just concurrency: a fan-out with no upper bound on shard count is a DoS surface. Reject requests above a limit (e.g. `> 200 shards`) with `413`/`400` instead of trying and timing out.

5. Aggregate with bounded memory: stream and reduce as results arrive rather than collecting all responses then combining. Sum-of-all holds every payload in memory; a streaming reduce holds one.

6. Cancel on first hard error only if the request truly cannot be served partially; otherwise let the group finish and report what is missing. `errgroup`'s first-error cancellation is convenient but throws away good results.

7. Record per-member latency so a slow shard is visible as a *shard* problem, not just a slow endpoint, and so you can shard-key or timeout the offender separately.

## Pitfalls

- `errgroup.Wait()` without setting a limit — unbounded concurrency in a library that looks bounded because it is called "group".
- A per-member timeout equal to the request timeout, so every member gets the full budget and the request times out as a whole.
- Returning an error for one missing member when the product only needed 19 — turning a partial degradation into a full failure.
- Collecting all responses into a slice before reducing, so a large fan-out doubles memory and OOMs an otherwise healthy worker.

## Verification

    # inject 500ms latency into one shard; the endpoint should stay under its deadline
    toxiproxy-cli toxic add -t latency -a latency=500 shard-7
    curl -s -o /dev/null -w '%{http_code} %{time_total}\n' localhost:8080/search?q=x
    # expect 200 with partial:true and time_total < 400ms, not a timeout
    curl -s localhost:8080/search?q=x | jq '{partial, missing}'
    grep fanout_concurrency /etc/app/config.yaml    # concurrency is bounded, not len(shards)

Report: the concurrency cap, the per-member deadline, the partial-result contract, and a fault-injection result where one slow shard degrades to partial instead of a timeout.
