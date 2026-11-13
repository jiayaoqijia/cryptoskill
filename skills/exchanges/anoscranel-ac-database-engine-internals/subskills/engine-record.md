---
name: engine-record
domain: software-engineering/engine-record
trigger: "Writing the record of an engine's structure and configuration for a workload."
anti_trigger: "Not for the query tuning record (ac-query-and-index-design)."
scope: "The written record of structures, config, and amplification for a workload."
status: seedling
---

# Engine record

## Standard

An engine record states the storage structure, its configuration, and the three amplification numbers measured for a specific workload. Its purpose is to make visible the design commitment a configuration represents: what the log guarantees, what the merge schedule means for latency, what the pool holds, and what each knob was turned to trade.

The record also anchors diagnosis. A slow-write or fast-fill symptom becomes interpretable only against a stated configuration: a B-tree with undersized pools, an LSM with an unthrottled merge, a tombstone-heavy workload without a reclaim schedule. When the record is written, the next occurrence of a degradation question begins from a measurement rather than a guess.

Primary sources: <https://postgresql.org/docs/current/runtime-config-resource.html> and <https://github.com/facebook/rocksdb/wiki/RocksDB-Tuning-Guide>.

## Decision rules

- The record states the engine's storage structure with citations of its documentation.
- The configuration is recorded with the operating points of the main knobs.
- The three amplification numbers are recorded for the workload, with measurement dates.
- The written record includes the log's durability contract as stated by the implementation.
- Each tuning knob is annotated with the amplification it trades.
- Reading the record, a reviewer can reconstruct the diagnosis of the last degradation.

## Procedure

1. Record the storage structure and its documentation by name.
2. Record the operating points of the main tuning knobs.
3. Measure the three amplification numbers for the workload.
4. Record the log's durability contract.
5. Annotate each knob with its trade.
6. Review at each degradation or configuration change and record the delta.

## Anti-patterns

- Configuration recorded without the principle it was chosen to serve.
- Amplification numbers recorded without their workload.
- A durability label recorded without citing the implementation's statement.
- Knobs annotated with each other rather than with the amplification they trade.
- No delta review after a change, so the record equals a stale snapshot.

## Done checklist

- [ ] Structure and documentation recorded.
- [ ] Knob operating points recorded.
- [ ] Three amplification numbers recorded with dates.
- [ ] Log durability contract cited.
- [ ] Each knob annotated with its trade.
- [ ] Delta recorded at every change.

The record earns its keep at the moment a vendor changes a default: amplification numbers measured under the old default cannot be compared with new ones without a note, so the record should note the engine version and the default set in force when each measurement was taken, and should re-measure after any version change rather than assuming the old currency still holds.

## Sources

- PostgreSQL configuration documentation as the model of stated contracts: <https://postgresql.org/docs/current/runtime-config-resource.html>
- RocksDB tuning guide for the amplification-trading model: <https://github.com/facebook/rocksdb/wiki/RocksDB-Tuning-Guide>
- Pre-registration practice for review conditions: <https://osf.io/prereg/>
