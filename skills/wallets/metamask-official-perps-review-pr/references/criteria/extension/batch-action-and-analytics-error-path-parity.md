# Batch-Action and Analytics Error-Path Parity

Sibling batch-action handlers (`handleCloseAllPositions`, `handleCancelAllOrders`) share one error contract: the same catch and soft-failure analytics in every sibling, each new branch covered by a test.

- **Asymmetric catch blocks across sibling handlers** — if one batch-action handler emits `PerpsError` + `trackPerpsErrorScreenViewed` on transport throw, every parallel handler in the same component must do the same. Diff all `catch` branches in the file before declaring analytics parity.
- **Soft-failure branch without error-screen-view** — a `{ success: false }` (or equivalent `result?.success` check) branch that fires `batchActionError` but not an error-screen-view event is incomplete. Before signing off on error analytics, grep sibling components that own the same `{ success: boolean }` shape and verify their soft-failure branches are symmetric (`git grep -l 'success.*boolean\|{ success:' -- '*.tsx' '*.ts'`).
- **New analytics branch ships without a test** — every new `catch` block or `if (!result?.success)` branch that emits an analytics event must have a corresponding unit test covering that branch. Missing coverage surfaces as a hard gate failure later; add the test in the same commit as the analytics change.
