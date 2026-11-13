---
name: activity-timeouts-and-heartbeats
domain: software-engineering/activity-timeouts-and-heartbeats
trigger: "Detecting a stuck step without duplicating its effect."
anti_trigger: "Not for request timeouts, and not for worker health checks alone."
scope: "Detecting a stuck step and retrying it without duplication."
status: seedling
---

# Activity timeouts and heartbeats

## Standard

A workflow needs to distinguish a step that is slow from a step that is dead. A timeout alone cannot: if it fires while the worker is still running, a retry starts a second worker alongside the first, and both proceed. That is the double-execution problem, and heartbeats exist to solve it — the worker reports progress periodically, and the timeout is measured from the last heartbeat rather than from the start.

Two timeouts therefore matter: a heartbeat timeout, which fires when a worker stops reporting, and a start-to-close timeout, which bounds the whole activity regardless of progress. Setting only the second leaves a slow-but-alive worker indistinguishable from a dead one, and setting only the first leaves an activity that reports progress forever without finishing.

Primary sources: <https://aws.amazon.com/builders-library/> and <https://www.enterpriseintegrationpatterns.com/>.

## Decision rules

- Record the heartbeat interval and the heartbeat timeout, with the margin between them.
- Record the start-to-close timeout and whether it is longer than the expected worst case.
- Record what the worker does when it cannot heartbeat, since continuing without reporting is the failure.
- Record whether a retried activity can run concurrently with its predecessor.
- Record the retry policy's interaction with the timeouts, since a long activity with a short timeout never succeeds.
- Record the visibility the heartbeats give, since they double as progress reporting.

## Procedure

1. Record the expected duration and its variance.
2. Set a start-to-close timeout above the worst case.
3. Set a heartbeat interval and timeout with a margin.
4. Make the worker stop on heartbeat failure.
5. Record the concurrency risk on retry.
6. Write the timeout model with both bounds.

## Anti-patterns

- A start-to-close timeout only, which cannot tell slow from dead.
- A heartbeat interval equal to the timeout, which triggers on a single missed beat.
- A worker that continues after failing to heartbeat.
- A retry that starts while the previous attempt is still running.
- Setting a timeout below the normal duration and retrying forever.

## Done checklist

- [ ] Expected duration recorded.
- [ ] Start-to-close timeout recorded.
- [ ] Heartbeat interval and timeout recorded.
- [ ] Worker behaviour on heartbeat failure recorded.
- [ ] Retry concurrency recorded.
- [ ] Progress visibility recorded.

The heartbeat also carries information the timeout cannot: a worker that reports progress slowly and one that reports none are different problems, and a heartbeat payload with a progress marker lets an operator distinguish a stuck step from a slow one without reading worker logs.


## Sources

- Activity and worker practice: <https://aws.amazon.com/builders-library/>
- Workflow patterns: <https://www.enterpriseintegrationpatterns.com/>
- Reliability context: <https://sre.google/>
