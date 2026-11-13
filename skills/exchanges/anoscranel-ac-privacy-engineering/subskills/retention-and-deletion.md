---
name: retention-and-deletion
domain: software-engineering/retention-and-deletion
trigger: "Implementing retention schedules and deletion that actually propagates."
anti_trigger: "Not for legal retention obligations, and not for backup design."
scope: "Retention schedules, and deletion that reaches derived stores."
status: seedling
---

# Retention and deletion

## Standard

A retention schedule states how long each class of data is kept and what happens at the end of that period. Implementing it means a job that runs on a schedule, an audit that shows what it deleted, and a deletion that reaches the copies — the cache, the search index, the warehouse table, the log store, and the backup whose restore would resurrect the record.

That last point is the one most often skipped. A deletion that removes the row from the primary database but leaves it in a nightly export has not deleted it, and a restore from backup will bring it back. The honest design either excludes the deleted records from restores or applies the deletion log at restore time, and the record should state which.

Primary sources: <https://ico.org.uk/> and <https://www.nist.gov/privacy-framework>.

## Decision rules

- Record the retention period per data class and the trigger that starts it.
- Record every store the class exists in, including derived and exported copies.
- Record the deletion job, its schedule, and its failure handling.
- Record the audit trail that proves a deletion occurred.
- Record the backup retention and whether restores replay deletions.
- Record the exceptions: data held under a legal obligation, and who approved the exception.

## Procedure

1. Record the retention period and trigger per class.
2. Enumerate the stores containing the class.
3. Implement the deletion job with idempotent, auditable execution.
4. Record the audit output and where it is kept.
5. Record the backup restore procedure and its deletion replay.
6. Record approved exceptions with their basis.

## Anti-patterns

- Deleting from the primary store and leaving the warehouse copy.
- A deletion job whose failures are silent.
- Backups that restore deleted records without the deletion log.
- Exceptions granted verbally and never recorded.
- Retention periods copied from a template without the trigger defined.

## Done checklist

- [ ] Period and trigger recorded per class.
- [ ] All stores enumerated.
- [ ] Deletion job scheduled with failure handling.
- [ ] Audit trail recorded.
- [ ] Backup restore deletion replay recorded.
- [ ] Exceptions recorded with approval.

The deletion job's audit trail is also its defence: a log showing what was deleted and when is what allows the organisation to answer a challenge, and a job that deletes without recording cannot distinguish a successful run from one that silently matched nothing.


## Sources

- Retention and erasure guidance: <https://ico.org.uk/>
- NIST privacy framework: <https://www.nist.gov/privacy-framework>
- Records management standards: <https://www.nationalarchives.gov.uk/>
