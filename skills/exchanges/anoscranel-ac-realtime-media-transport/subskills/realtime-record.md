---
name: realtime-record
domain: software-engineering/realtime-record
trigger: "Writing the record of a realtime system's connectivity behaviour."
anti_trigger: "Not for the signalling schema, and not for product analytics."
scope: "The written record of candidates, paths, and connection states."
status: seedling
---

# Realtime record

## Standard

The realtime record is the connectivity case file: the STUN and TURN servers configured, the candidate types gathered per call, the selected pair and its relay status, the failure reasons of the pairs that did not connect, the negotiated media descriptions in their exchanged form, and the security provisions verified per release. Because connectivity is situational — the candidate list is a property of two networks on the day — the record is per-call facts plus aggregate trends, never a single permanent truth about "the network".

Its working value mirrors the other records: when a user's call does not connect, the record answers the bounded question — did peers gather candidates, did signalling deliver them, did any pair's checks succeed, was TURN reached, was the failure a refusal or a timeout — and the trend section answers the systemic one. A relayed-call fraction that doubles after launch in one market says network conditions of that market; a sudden zero says the TURN server; a slow climb in a region's failure rates says a firewall change. None of these are visible in the application's ordinary logs.

Secondary sources: <https://webrtcforthecurious.com/> and <https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API>.

## Decision rules

- Record per call the gathered candidate types, the selected pair, the relay status, and the connected path's security provisions.
- Record failure reasons for every prunned pair; a failed check is a diagnosis, not noise.
- Aggregate the relayed-call fraction and failure reasons by region and release; watch the trend, not the day.
- Record the TURN and STUN servers in force per release, since a change of server is a change of connectivity behaviour.
- Keep exchanged session-description dumps from failing cases, because the negotiated intersection is where the defects live.
- Any record store in the client must survive into a support context gracefully — valid debugging data has no business containing raw media or secrets.

## Procedure

1. Define the per-call record: gathered types, candidates exchange outcome, checks outcomes, selected pair, relay status.
2. Define the failure taxonomy, with a reason code per distinct failure mode.
3. Wire the record to the application's diagnostic event path, not to end-user analytics.
4. Aggregate by region and release, and set trend alerts on the relayed fraction and failure-mix changes.
5. Record server configuration per release, and the four security provisions verified.
6. Attach the exchanged descriptions from failing calls as user-consented diagnostics.

## Anti-patterns

- The only connectivity "record" being the client console, gone with the tab.
- Failed pairs discarded because they did not connect, which deletes the diagnosis of why the successful one was the success.
- A relayed-fraction metric that was never defined, so the TURN bill arrives as a hole where a budget was.
- Release notes saying "TURN migrated" nowhere, so a connectivity regression is traced through folklore.
- Raw diagnostics captured in ways that store user media — a debugging path becoming a privacy defect.

## Done checklist

- [ ] Per-call connectivity record defined and populated.
- [ ] Failure taxonomy with reason codes wired.
- [ ] Relayed-fraction and failure-mix trends aggregated by region and release.
- [ ] Server configuration recorded per release.
- [ ] Security provisions verification recorded.
- [ ] Failing-call descriptions captured with consent and without media content.

## Sources

- The stack, explained practically: <https://webrtcforthecurious.com/>
- The API's own events and states: <https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API>
- Getting-started overview: <https://webrtc.org/getting-started/overview/>
