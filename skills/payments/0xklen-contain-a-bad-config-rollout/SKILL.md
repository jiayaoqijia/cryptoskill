---
name: contain-a-bad-config-rollout
description: Use when a config or flag push (not a deploy) causes errors — detects it as the cause, reverts the config fast, and freezes further pushes while the bad value is purged from every consumer.
---

# Contain a bad config rollout

Modern incidents are frequently config, not code: a flag flipped, a rate limit lowered, a routing table edited. Config deploys are often faster, less reviewed and less observable than code deploys, so a bad one spreads everywhere before anyone connects the change to the symptom.

## Procedure

1. Prove it is config, not code: the binary did not change, but behaviour did. Diff the *effective* config against the previous version. Keep a version/hash of config at every consumer and a timeline of changes:
       diff <(curl -s localhost:8080/admin/config) config/last-known-good.yaml
       git -C config-repo log --since="30 min ago" --oneline
2. Revert the config first — it is usually faster than a code rollback and does not need a build. Ship the previous known-good value through the same pipeline (so the pipeline itself is exercised), not by hand-editing a file on one host.

3. Purge the bad value everywhere: consumers cache config (env at boot, TTL in memory, edge CDN). A revert to the source does nothing until the caches expire or are actively invalidated. Push an invalidation, then confirm each consumer reports the old hash:
       curl -s -X POST localhost:9090/config/invalidate?key=rate_limit
       for p in $REPLICAS; do curl -s "http://$p:9090/admin/config" | jq -r '.rate_limit'; done

4. Freeze further config pushes immediately: block the `config-repo` (require review) and pause the sync from the flag service, so a second bad value does not land while you are reverting the first.

5. Distinguish cheap-revert from needs-migration: some config changes (a shard key, a serialization format) are not safely reversible because data already written under the new value. Identify those and treat them as code changes with a forward fix, not a revert.

6. Find the *review gap* that let it through and close it: config changes that touch money, auth, routing or limits should require review and a canary. Add a schema/range validator to the config pipeline so an out-of-range value is rejected at push time.

7. Add a canary for config: apply to 1% of consumers, watch error rate for 5 minutes, then widen. A config change that can be canaried like code gets caught at 1%, not 100%.

## Pitfalls

- Reverting the source while consumers hold a cached bad value for its full TTL, so the incident persists for minutes after the "fix".
- Hand-editing one host to restore service and calling it done, leaving the other N-1 hosts on the bad value and the next sync re-applying it.
- Rolling back config that already caused irreversible effects (a flag that sent notifications), so the revert restores the flag but not the 50k emails.
- No config versioning, so you cannot name the previous value or prove which change caused the symptom.

## Verification

    # the revert must propagate to every consumer and the error rate must fall
    git -C config-repo revert --no-edit <bad-sha> && git -C config-repo push
    for p in $REPLICAS; do curl -s "http://$p:9090/admin/config" | jq -r '.config_hash'; done | sort -u | wc -l
    # expect 1 (all replicas on the same, good hash)
    curl -s 'localhost:9090/api/v1/query?query=rate(http_requests_total{code=~"5.."}[1m])' | jq '.data.result[].value'

Report: the config diff that caused it, the revert pushed through the pipeline, the invalidation result showing every replica on one hash, and the review/canary change added so the same class cannot spread silently again.
