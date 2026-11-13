---
name: late-data-and-upserts
domain: software-engineering/late-data-and-upserts
trigger: "Data arriving after its partition was written."
anti_trigger: "Not for stream watermarks, and not for backfill planning."
scope: "Late-arriving records and the merge/upsert keys that keep them correct."
status: seedling
---

# Late data and upserts

## Standard

Late data arrives after the partition it logically belongs to was already written. The pipeline has three choices, and the choice must be a declared policy, not an accident: wait (delay the partition until a stated cutoff — trades freshness for completeness), hold (write the partition now and buffer late records into a later merge — trades simplicity for an extra stage), or accept (write now, fold late records into tomorrow's run — trades accuracy-in-window for simplicity).

When late records are folded in, the write is an upsert keyed on the dataset's identity: (entity, event time) or (entity, effective period). The key decides correctness. A key on ingestion time duplicates the same late record forever; a key that omits the versioning column merges two revisions into one; a key that does not match the downstream consumer's own identity silently disagrees with every consumer that merges by their own key.

Primary sources: <https://delta.io/> and <https://docs.getdbt.com/>.

## Decision rules

- Declare the late-data policy per source: wait, hold, or accept — with the cutoff stated.
- Define the upsert key from the data's identity, not its arrival: (entity, event time) or (entity, period).
- Record which columns define a revision of the same entity versus a new record.
- Keep a quarantine for records that fail the merge assertion rather than silently dropping them.
- Version the merge logic in the pipeline record; changing a merge key is a schema-level change.
- Compute and publish the late-arrival profile: how late, how often, trending which way.

## Procedure

1. Classify each source by its realistic lateness and declare the policy.
2. Derive the identity key from the data model, and the merge columns with it.
3. Implement the merge with an assertion: key violation quarantines the record.
4. Add late-record accounting: counts of merged revisions per run.
5. Publish the lateness profile to the pipeline's freshness monitoring input.
6. Record the policy, key, and revision columns per dataset.

## Anti-patterns

- Keying by ingestion time and re-late-ingesting the same record.
- Merge keys that differ between producer and consumer of the same dataset.
- Silent drops when a record fails the merge.
- Treating "it arrived late" as an error to alert on when the policy already accepts it.
- Changing a merge key without re-deriving the affected partitions.

## Done checklist

- [ ] Policy declared per source with cutoff.
- [ ] Identity key and revision columns recorded.
- [ ] Merge assertion and quarantine implemented.
- [ ] Late-record counts published.
- [ ] Lateness profile feeding freshness monitoring.
- [ ] Merge-key changes treated as schema changes.

## Sources

- Delta Lake MERGE and Delta tables: <https://delta.io/>
- dbt incremental merge strategies: <https://docs.getdbt.com/>
- PostgreSQL partitioning for late-period writes: <https://www.postgresql.org/docs/current/ddl-partitioning.html>
