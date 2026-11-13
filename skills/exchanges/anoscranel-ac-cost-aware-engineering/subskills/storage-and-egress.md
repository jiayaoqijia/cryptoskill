---
name: storage-and-egress
domain: software-engineering/storage-and-egress
trigger: "Designing retention and data movement with cost in view."
anti_trigger: "Not for backup policy, and not for vendor pricing negotiation."
scope: "Tiers, retention, and the transfer costs that surprise."
status: seedling
---

# Storage and egress

## Standard

Storage costs are cumulative and egress costs are per transfer, and both are frequently larger than the compute they support. Storage grows because nothing deletes, and egress grows because data is read from where it was written, across a boundary that is priced: a region, a zone, or a network edge.

The engineering levers are retention, tiering, placement, and payload size. Retention deletes what is not needed; tiering moves cold data to slower and cheaper media with a retrieval cost; placement keeps computation near the data so the transfer is internal; and payload size reduces the bytes that must move at all. Each lever has a readability or latency cost, and the record should state which was accepted.

Primary sources: <https://www.finops.org/> and <https://www.cncf.io/>.

## Decision rules

- Record the storage growth rate and the retention policy that bounds it.
- Record the tiering thresholds and the retrieval cost of each tier.
- Record where computation runs relative to where data is stored.
- Record the egress boundaries crossed in the normal request path.
- Record payload sizes and the compression or field-selection applied.
- Record the retrieval cost that a restore or an audit would incur.

## Procedure

1. Record storage volume, growth rate, and retention.
2. Record the tiering policy and each tier's retrieval cost.
3. Map the data path and the boundaries it crosses.
4. Record the egress volume per unit of work.
5. Record compression and payload selection.
6. Record the cost of a full restore from each tier.

## Anti-patterns

- Retaining everything because deletion is risky.
- Tiering without accounting for retrieval cost.
- Running computation in a different region from the data.
- Cross-zone traffic in a hot path.
- Compressing at a ratio that costs more CPU than it saves in transfer.

## Done checklist

- [ ] Storage growth and retention recorded.
- [ ] Tiering and retrieval costs recorded.
- [ ] Data path boundaries recorded.
- [ ] Egress per unit recorded.
- [ ] Payload reduction recorded.
- [ ] Restore cost recorded per tier.

The cross-zone case deserves particular attention because it is invisible in development: a multi-zone deployment that replicates on every write pays for transfer that a single-zone test never generates, and the cost appears only at production volume, where it is attributed to the service rather than to the replication topology.


## Sources

- FinOps storage and transfer guidance: <https://www.finops.org/>
- Cloud native data practice: <https://www.cncf.io/>
- Network and peering reference: <https://www.ietf.org/>
