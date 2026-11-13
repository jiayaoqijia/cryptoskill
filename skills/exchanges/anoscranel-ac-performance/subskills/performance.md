---
name: performance
domain: software-engineering/performance
trigger: "\"This is slow\", \"profile this\", \"p99 latency is too high\", \"set a performance budget\", \"load test this API\", \"is this N+1\", \"will this scale\"."
anti_trigger: "Browser-side Core Web Vitals, bundle and render cost (subskills/web-performance.md); setting SLOs and alerts; instrumenting traces."
scope: "Measure-first latency/throughput work: budgets, profiling, flame graphs, load tests"
status: "seedling"
---

# Performance

## Standard

- **Knuth (1974)**: "premature optimization is the root of all evil. Yet we should not pass up our opportunities in that critical 3%" (https://dl.acm.org/doi/10.1145/356635.356640). The rule is "measure first", not "never optimise".
- **Budget first**: a written, measurable budget per critical path turns "is this premature?" into a lookup.
- **Percentiles, not averages**: p50, p95, p99. The average hides the slow users.
- **Test types**: smoke (1–5 virtual users, checks the script), load (expected peak), stress (above peak), spike (sudden surge), soak (hours at moderate load: leaks, connection exhaustion).
- **Flame graphs** (Brendan Gregg): width = share of samples on a stack (https://www.brendangregg.com/flamegraphs.html).
- **Agent code**: performance inefficiencies are among the most common flaws in LLM-generated code (arXiv 2503.06327).

## Decision rules

1. No optimisation without a budget and a measurement that breaches it.
2. Budget numbers come from your own SLA. ⚠️ "p95 ≤ 300 ms API, ≤ 500 ms page" is a practitioner magnitude, not a standard.
3. Optimise in this order: algorithm and data structure → database queries and indexes → network round trips → caching → micro-optimisation.
4. An N+1 query loop is a design defect. Fix it whenever found.
5. Cache only reads, only after a profile proves the read is hot. Never cache a correctness-critical write. Every cache needs an invalidation rule.
6. Change one thing at a time. Re-measure after each change. No gain → revert.
7. Stop when the path meets its budget. Speed past the budget is not worth the complexity.
8. CI gate: a load-smoke on the critical path with a p95 threshold and an error-rate threshold. Breach fails the build.
9. Soak-test before a major release. ⚠️ "At least one hour" is a house minimum.

## Procedure

1. Write the budget: path, percentile, threshold, workload (requests per second, data size).
2. Reproduce the slowness with realistic data volume. Toy data hides O(n²).
3. Measure the baseline p50, p95, p99 and throughput.
4. Profile:
   ```bash
   py-spy record -o flame.svg -- python app.py
   go test -cpuprofile cpu.out -bench . && go tool pprof -http=:8080 cpu.out
   node --cpu-prof app.js
   ```
5. Read the widest stacks. List the top three.
6. For databases: log slow queries; run `EXPLAIN ANALYZE`; count queries per request.
7. Fix the top hot spot only. Re-profile. Record before and after numbers.
8. Load test the path:
   ```js
   // k6
   export const options = { thresholds: {
     http_req_duration: ['p(95)<300'], http_req_failed: ['rate<0.01'] } };
   ```
9. Add the load-smoke to CI with the same thresholds.

## Anti-patterns

- Optimising by intuition; reporting averages.
- Load testing with toy data.
- Caching to mask a missing index.
- Trusting an agent's claimed speedup without re-measuring.

## Done checklist

- [ ] Budget written with percentile and workload.
- [ ] Baseline and after numbers recorded.
- [ ] Profile shows the fixed hot spot is gone.
- [ ] Load-smoke with thresholds runs in CI.
- [ ] Soak run before major release.

## Sources

- <https://web.dev/learn/performance>
- <https://sre.google>
- https://dl.acm.org/doi/10.1145/356635.356640 · https://grafana.com/docs/k6/latest/
