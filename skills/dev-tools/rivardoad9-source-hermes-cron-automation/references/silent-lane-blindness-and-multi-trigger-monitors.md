# Multi-trigger monitors + a lane that must not go blind silently (5 Okt 2026)

Companion to `delta-gated-alerts-and-member-removal.md` (change-gating, tamper-and-restore
verification) and `level-crossing-entry-zone-alerts.md` (single price band, re-arm on exit).
This file covers the two additions that came out of building a watch on one token across two venues.

## A. Multi-trigger lanes: cooldown per trigger, not per run

One lane watching several kinds of change at once — price zone / TP / stop, 24h volume spike,
liquidity drain, holder + top-10 shift, mint-authority flip (worked case: DEUS/XMAQUINA):

- **`state["fired"] = {key: ts}` + `cooled(key, minutes)`** (4 h for price levels, 6 h for volume).
  A single boolean per trigger is not enough — the condition can stay true for hours and would
  re-fire on every tick.
- **Ratio triggers need an absolute floor.** "Volume ≥ 3× median" fires on a dead token at $12 K:
  require `vol24 ≥ 3× median AND vol24 ≥ $20 K`, and skip the ratio trigger until ≥6 readings exist
  (a median built from two samples is noise).
- **Two venues = two sources — report both.** The same token trading on Base ($870 K liq) and Solana
  ($52 K) is not one number; a missing venue is *missing*, never zero.
- **Append every reading to `data/<lane>.jsonl`** (ts + price + vol + liq + holders). It costs
  nothing, and it is the only way to later judge whether the entry/stop levels you published were
  ever actually touched — the alert log alone cannot answer that.
- **Prove the alert path with a copy, never by editing production state.** `sed` the copy's DATA dir
  and level constants, seed its `state.json` with a `last` snapshot just *outside* the band, run it →
  the message renders while live state stays untouched. Expect the copy to lose path-based imports (a
  shared message-styling module imported from the script's own directory) — a copy artifact, not a bug.
- **Run the real script twice in a row before scheduling.** Run #1 writes the state file; run #2 reads
  it back. A writer/reader schema mismatch (storing `vols` as floats but reading them as `{"vol24": …}`
  dicts) explodes only on run #2 and is invisible in a one-shot demo. Then confirm the scheduler
  actually executed it — heartbeat mtime moved, `last_status: ok`, and a manual `cronjob run`
  reporting `status: silent (empty output)` is the *expected success shape*, not a failure.

## B. A lane that goes quiet must not go blind silently

Silent-by-design makes a read failure indistinguishable from "nothing happened". Seen live: a
monitor's Base-chain feed returned nothing on two consecutive runs — heartbeat `px=None`, no message
to the user — while the other venue kept reading fine. Half-blind and mute, with nothing in the chat
to reveal it.

- Write a heartbeat every run (`data/<lane>.last`): timestamp + **per-source** read status
  (`{"ts": …, "sol": {…}, "base": null}`), not a single global ok.
- Count consecutive failures **per source**; after N (≈6 runs ≈ 2 h) print ONE diagnostic line, then
  hold it behind a long cooldown (~12 h) so a permanently dead source doesn't become a new spam lane.
- Keep the no-alert-on-transient-failure rule (`level-crossing-entry-zone-alerts.md`): one empty read
  is not news, six are.

## C. Same discipline for score/grade lanes

A recurring lane that alerts on a *score* has one more failure mode: hard band cutoffs. A score
sitting on a line (health 61 vs the `B ≥ 62` boundary) flips the grade — and the recommendation text
keyed to it — on rounding, then flips back. Grade with a **1-point deadband** (downgrade only when
the score falls a full point below the line, upgrade on touch) and keep the previous grade in the
snapshot so the band is sticky. Diagnosis recipe for the user's inevitable "kenapa jadi C?":
`data/<tool>_history.jsonl` (see the oscillation band) → the boundary in the code → the
`score_parts` decomposition naming the one component that moved (for a token health score this is
usually *alpha* = 7d return − BTC's 7d return, while trend/liquidity stay pinned at full weight).
Detail + worked numbers: `crypto-portfolio-advisory/references/portfolio-risk-monitor.md` §6.
