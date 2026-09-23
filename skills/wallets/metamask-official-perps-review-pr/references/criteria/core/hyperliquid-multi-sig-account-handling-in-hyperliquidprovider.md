# HyperLiquid Multi-Sig Account Handling in HyperLiquidProvider

Every user-scoped exchange write in `HyperLiquidProvider` needs both a proactive info probe placed right before the write and a message classifier in its `catch`; HyperLiquid rejects every single-signer write for a multi-sig account, and neither guard alone is sufficient.

- **Catch-path classifier without proactive probe** — burns a doomed write on every entry
  for a multi-sig account. The error is caught, but the round-trip and any side-effects
  (recording premature state, logging) have already occurred.
- **Proactive probe without catch-path classifier** — can race the multi-sig conversion
  window and fails open: the probe returns normal, the write fires during the transition,
  and the error is unhandled.
- **Probe placed too early** — placing the probe immediately after `userAbstraction` (rather
  than immediately before the write) means already-unified multi-sig accounts are probed on
  every call, and the probe result can cause the account to be recorded as `enabled: false`
  before the unified path has had a chance to short-circuit. The correct placement is
  **after** the already-compatible short-circuit, the defer branch, and the unknown-mode
  bail — right before the write that would otherwise fail.
