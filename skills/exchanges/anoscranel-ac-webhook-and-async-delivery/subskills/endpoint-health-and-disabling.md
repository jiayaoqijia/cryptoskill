---
name: endpoint-health-and-disabling
domain: software-engineering/endpoint-health-and-disabling
trigger: "Stopping delivery to an endpoint that keeps failing."
anti_trigger: "Not for monitoring the sender, and not for load balancing."
scope: "Disabling a failing endpoint and the path back to enabled."
status: seedling
---

# Endpoint health and disabling

## Standard

An endpoint that always returns an error consumes the sender's retry capacity indefinitely and generates log volume with no prospect of success. Most sender systems therefore disable an endpoint after sustained failure, which stops the waste and creates a new problem: the receiver may not know it was disabled, and events emitted during the disabled period are lost unless a fetch path exists.

The disabling policy should be stated in the delivery contract with its thresholds, its notification, and its re-enablement path. The re-enablement path matters most: an endpoint that requires a support request to restore is one that stays broken longer, and a receiver that must poll to discover its own state is one that cannot act quickly.

Primary sources: <https://csrc.nist.gov/> and <https://sre.google/>.

## Decision rules

- Record the disabling threshold and the period over which it is measured.
- Record how the receiver is notified, by email, dashboard, or an API it can query.
- Record the re-enablement path and whether the receiver can trigger it.
- Record what happens to events emitted while disabled, and whether they are retrievable.
- Record the test endpoint or probe that lets a receiver confirm it is enabled.
- Record the automatic re-enable attempt and its backoff, if any.

## Procedure

1. Record the failure threshold and window.
2. Record notification channels.
3. Record the re-enablement path and who can trigger it.
4. Record handling of events during the disabled period.
5. Record the probe a receiver can use.
6. Write the policy with its recovery path.

## Anti-patterns

- Disabling without notifying the receiver.
- Re-enablement that requires a manual support ticket.
- Events during the disabled period silently dropped with no fetch path.
- Auto re-enabling on a fixed schedule, which resumes hammering a broken endpoint.
- No way for a receiver to check its own status.

## Done checklist

- [ ] Threshold and window recorded.
- [ ] Notification recorded.
- [ ] Re-enablement path recorded.
- [ ] Disabled-period event handling recorded.
- [ ] Probe recorded.
- [ ] Auto re-enable policy recorded.

The threshold should account for the receiver's deploy cycle: an endpoint that fails for the duration of a rolling deploy is behaving normally, and a threshold that disables after five minutes of failures will disable every receiver that deploys, which is a policy that punishes routine operation.


## Sources

- Security and availability controls: <https://csrc.nist.gov/>
- Reliability practice: <https://sre.google/>
- Delivery reliability context: <https://sre.google/workbook/table-of-contents/>
