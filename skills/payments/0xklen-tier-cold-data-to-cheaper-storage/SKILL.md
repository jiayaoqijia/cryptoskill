---
name: tier-cold-data-to-cheaper-storage
description: Use when storage cost is dominated by data nobody reads. Moves rarely-accessed data to colder tiers by measured access age, keeping hot reads fast and cheap.
---

# Tier Cold Data to Cheaper Storage

Most stored bytes are never read again, yet they sit on the most expensive tier. Measure access age, move the cold fraction down a tier or two, and prove the read path still meets its latency budget for what remains hot.

## Procedure

1. Measure access age before moving anything: S3 Storage Lens / `aws s3api list-objects-v2` with `LastModified`, or access-log analysis to get the read distribution.
2. Define the hot window from real reads, not a guess — commonly the last 30 days serves >95% of requests.
3. Choose tiers and their tradeoffs: S3 Standard → Standard-IA (30d min, retrieval fee) → Glacier Instant → Glacier Flexible (minutes-hours) → Deep Archive (12-48h).
4. Automate with a lifecycle transition rule, never a one-off script, so new cold data keeps moving:
   `{"Transitions":[{"Days":30,"StorageClass":"STANDARD_IA"},{"Days":90,"StorageClass":"GLACIER"}],"Expiration":{"Days":400}}`.
5. For databases, move cold rows to a partitioned archive table or a columnar store; keep the hot partition indexed.
6. Check the retrieval cost of the target tier against the request rate — a tier with a per-GB retrieval fee can cost more than it saves on a frequently-read "cold" object.
7. Verify the hot path is untouched: re-run the p99 latency test for recent-object reads.
8. Sample the moved set monthly and reverse any object that was read after transition (a signal the window was wrong).

## Pitfalls

- Transitioning to Glacier objects that a warm cache or backup job still reads, then paying retrieval and latency on every request.
- Minimum storage durations: IA bills 30 days, Glacier 90, Deep Archive 180 — moving freshly-written objects there costs more, not less.
- A one-time migration script that never runs again, so last month's hot data stays on the expensive tier forever.
- Forgetting the small-object overhead: 128KB minimum billable size on IA/Glacier means tiny objects cost more cold than hot.
- Transitioning objects at the bucket root and catching data that must stay instantly readable (configs, manifests).
- Ignoring per-object request pricing on cheap tiers; a high-request pattern on Deep Archive is a cost and latency trap.
- Moving cold data without updating backups, so the restore path now requires an archive retrieval that takes hours.

## Verification

    aws s3api list-objects-v2 --bucket acme --query \
      "Contents[].StorageClass" | sort | uniq -c
    # hot reads still meet budget
    aws s3api head-object --bucket acme --key hot/key | grep -i LastModified

COLD/GLACIER counts grew by the expected volume, hot reads stay on Standard, and the projected monthly bill dropped without a regression on recent-object p99.

Report: "Transitioned <n> GB older than <d>d to <tier> via lifecycle rule; projected saving $<x>/mo; recent-read p99 unchanged at <y>ms."
