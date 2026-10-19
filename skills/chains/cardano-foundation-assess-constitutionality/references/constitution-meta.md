# Constitution Version

The constitutional text this skill reasons over is mirrored from Intersect's repository of
record ([IntersectMBO/cardano-constitution](https://github.com/IntersectMBO/cardano-constitution))
into `../../docs/sources/cardano-constitution/`, one directory per enacted version. This skill
targets the version below. Every assessment must state these values so a reader can tell
exactly which text the reasoning rests on.

| Field | Value |
|---|---|
| Version directory | `cardano-constitution-2/` |
| Anchor URI | `ipfs://bafkreieyuknozbtewyurfqoagvplvykadn6a4u6wglupavdz46bbsnnl6e` |
| Anchor hash | `b368bdad83c727bbfe86425575233fb914eb76d05d89497f7790cf007fd95f52` |
| Guardrails script hash | `fa24fb305126805cf2164c161d852a0e7330cf988f1fe558cf7d4a64` |
| Governance action | `gov_action1jxne7hynfd7frcczwumd2eggps4kvy0msjztz9t0mutpy870ksgqqp6vp3p` |
| Ratified epoch | 608 |
| Enacted epoch | 609 |

The anchor, hash, guardrails script and epochs are read from that action's on-chain record
(`proposal_list` by `proposal_id`; the anchor is in `proposal_description`). The upstream
`README.md` in the version directory leaves the epochs as "XXX", and the transaction it names
(`8c653ee5…`) is the previous Constitution's action, which this one cites as its predecessor. Version directories are immutable once enacted; an
amendment arrives as a new sibling directory, which the weekly source refresh picks up
automatically.

## Why this matters

The Constitution is amendable through `NewConstitution` governance actions. If one has been
enacted since the version above, that text is superseded and any finding derived from it may
be wrong. This skill cannot check that itself, so it never claims the version is current. It
states the version and hands the reader the check.

## Verifying currency

This skill does not make network calls. Ask the user to run the check and paste the result
back, or point them at it so they can confirm independently:

```sh
curl -s "https://api.koios.rest/api/v1/proposal_list?proposal_type=eq.NewConstitution&select=proposal_id,ratified_epoch,enacted_epoch,expiration,proposal_description" \
  | jq '[.[] | {proposal_id, ratified_epoch, enacted_epoch, expiration,
               hash: .proposal_description.contents[1].anchor.dataHash}]
        | sort_by(.enacted_epoch // 0) | reverse'
```

Compare the anchor hash of the latest enacted entry with the table above; a matching hash is
stronger than a matching epoch. Also look for an entry with a `ratified_epoch` but no
`enacted_epoch` yet: a ratified Constitution is enacted at the next epoch boundary.

Interpreting the result:

- **`enacted_epoch` is 609** — the mirrored version is current. Proceed normally.
- **`enacted_epoch` is greater than 609** — a newer Constitution is in force. This version is
  stale. Say so plainly, stop, and do not issue findings from superseded text. Check whether
  `../../docs/sources/cardano-constitution/` already holds a newer version directory; retargeting
  this skill at it is a repo maintenance task, not something to work around mid-assessment.
- **Check not run, or the command failed** — proceed, but stamp the report
  `Constitution currency: unverified` alongside the version table. Never silently assume
  currency.

An `enacted_epoch` below 609 should not occur; if it does, treat the discrepancy itself as
the finding and stop.
