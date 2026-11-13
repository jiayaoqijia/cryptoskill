---
name: cancellation
domain: software-engineering/cancellation
trigger: "Designing tasks to stop when asked, without leaving work half-done."
anti_trigger: "Not for timeout budgets around remote calls, and not for runtime choice."
scope: "What cancellation means, what it skips, and designing to be cancelled."
status: seedling
---

# Cancellation

## Standard

Cancellation is cooperative: someone signals a stop, and the task stops only at the points where it checks. Everything between the signal and the next check still runs, so a task that never checks — or that checks once per gigabyte — is uncancellable in practice. The design work is choosing the checkpoints: frequent enough that a request abort stops promptly, few enough that the work between them is small and safe to abandon.

The deeper problem is what cancellation skips. A cancelled task stops before its cleanup sections, before its second store was updated, before the notification was sent — and code designed to run to completion leaves half-finished state behind. The two honest designs are checkpoint-and-undo: write the task so every checkpoint leaves state consistent, record what was done in a journal, or make the operation idempotent so the caller's retry completes it safely; and shielded regions: sections the cancellation cannot interrupt, kept short, for exactly the steps that must not be skipped, such as commit-and-acknowledge.

Primary sources: <https://martinfowler.com/> and <https://dl.acm.org/>.

## Decision rules

- Record the cancellation checkpoints and the maximum work skipped between them.
- Record the state left behind at each checkpoint: consistent, journaled, or idempotent.
- Record every shielded region and why it must not be interrupted, with a length bound.
- Record what cancellation does to shared resources: connections returned, locks released.
- Record the observable behaviour the caller sees on cancel: error, silence, or partial result.
- Test cancellation at each checkpoint boundary, not only at one.

## Procedure

1. Identify the task types that must be cancellable.
2. Choose checkpoints so skipped work is bounded.
3. Design each checkpoint's abandonment as consistent, journaled, or idempotent.
4. Mark shielded regions with a reason and a length limit.
5. Verify resource release on every cancellation path.
6. Test cancel-and-retry at each checkpoint.

## Anti-patterns

- A task that checks cancellation only between large work units.
- Cleanup code placed after the cancellation check, thus never run when cancelled.
- Shielded regions that are entire functions, immune to cancellation in practice.
- Locks held across awaits and released only at the end, held forever on cancel.
- A caller retried against a non-idempotent half-completed operation.

## Done checklist

- [ ] Checkpoints chosen with bounded skipped work.
- [ ] Abandonment behaviour per checkpoint.
- [ ] Shielded regions justified and bounded.
- [ ] Resource release verified on cancel.
- [ ] Caller-visible behaviour defined.
- [ ] Cancel-and-retry tested at every checkpoint.

## Sources

- Concurrency and cancellation patterns: <https://martinfowler.com/>
- Concurrency literature: <https://dl.acm.org/>
- Runtime references: <https://www.distributed-systems.net/>
