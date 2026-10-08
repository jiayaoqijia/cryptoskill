---
name: tune-ci-cache-hit-rate
description: Use when CI spends most of its time reinstalling dependencies. Keys caches on content hashes and measures the hit rate so builds reuse work instead of re-fetching it.
---

# Tune CI Cache Hit Rate

A cache that never hits is pure overhead: upload time, storage cost, and no speedup. Key on inputs, measure the hit rate, and evict what the cache cannot reuse.

## Procedure

1. Measure before changing anything. From the last 50 runs, count hits:
   `gh run list --limit 50 --json conclusion,displayTitle` plus each job's log line `Cache restored from key` / `Cache not found`.
2. Key the cache on the lockfile hash, not the branch:
   `key: npm-${{ runner.os }}-${{ hashFiles('**/package-lock.json') }}`
3. Add a `restore-keys` fallback so a near-miss still seeds the cache:
   `restore-keys: npm-${{ runner.os }}-`
4. Cache the right directory. Node: `~/.npm` (download cache) not `node_modules` (platform-specific). Python: `~/.cache/pip`. Cargo: `~/.cargo/registry` and `~/.cargo/git`, not `target/`. Go: `~/go/pkg/mod`.
5. Split immutable from mutable: cache the registry/download layer permanently, and the build output with a per-target key that includes the compiler version.
6. For monorepos, use the tool's own content-addressed remote cache (`nx`, `turbo`, Bazel) so a target hits across branches and machines, not just per-workflow.
7. Invalidate deliberately: bump a `CACHE_VERSION` in the key string when the cache format changes, or poisoned entries persist.
8. Watch the size cap — GitHub evicts the least-recently-used cache over 10 GB per repo, silently turning hits into misses.

## Pitfalls

- Caching `node_modules` across OSes or Node versions serves binaries built for the wrong architecture.
- A key that includes `github.run_id` or the commit SHA of every run never hits; the SHA changes each push.
- Secrets written into a restored cache directory can leak across fork PRs; never cache anything containing credentials.
- `actions/cache` and `actions/setup-node`'s built-in cache can both run and fight; pick one.
- A cache hit that restores a `node_modules` newer than the lockfile hides a missing `npm ci`, so the build diverges from a clean checkout — always run an install step even on hit.

## Verification

    gh run view <id> --log | grep -E 'Cache (restored|not found|saved)' | sort | uniq -c

Inspect the ratio across the last 50 runs; a healthy dependency cache restores on >90% of runs and saves only when the lockfile changed.

Report: "Cache key `<key>` hits <N>/<M> recent runs; job time dropped from <before> to <after> while `npm ci --prefer-offline` still runs on every job."
