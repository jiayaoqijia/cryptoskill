---
name: scheduled-autonomy
description: Run scheduled research or prepare strategy steps with durable claims, stable operation IDs, receipt reconciliation and human confirmation. Triggers: daily DCA, recurring buy, scheduled strategy, due steps, execution journal.
---

# Scheduled strategy execution

Read `docs/wallet-safety.md`. Saved plans and execution claims are local. Scheduling does not
create spending authority or guarantee exactly-once execution of arbitrary external actions.

1. Generate a strategy plan and review its assets, chain, sizes and timing.
2. Save it with `chaingpt_strategy_save_plan`.
3. Prefer scheduled research/unsigned preparation with a human confirming and executing transfers.
4. For an explicitly authorized agent-wallet action, call `chaingpt_strategy_due_steps claim=true`.
   Pass the returned operationId unchanged to the signer. Keep the confirmation hook enabled.
5. Re-run risk/quote/health checks as appropriate. Restricted signers reject opaque protocol calls;
   use the unsigned builder and external wallet for those operations.
6. Broadcast once and immediately mark the result with its transaction hash. Report pending versus
   confirmed accurately. Completed journal entries are immutable.

A crash leaves the step IN FLIGHT. Reconcile with the same operationId; never execute it using a
new id. Pending transactions keep their native and token reservations until resolved. A policy
refusal is final for this tick. Do not widen caps, delete a claim or disable the guard to continue.

Unattended fund movement requires a separately reviewed executor and approval boundary. This skill
ships no instruction to disable per-action confirmation. The generic scheduler cannot infer that
new operation IDs represent duplicate human intentions, or make external wallet execution atomic.
