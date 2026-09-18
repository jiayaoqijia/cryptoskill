---
repo: metamask-extension
parent: extension-lifecycle-decoupling
---

## MV3 MetaMask Specifics

| Assumption | Reality |
|------------|---------|
| SW eviction triggers lock | No `onSuspend` lock handler — SW eviction does NOT trigger lock |
| Timers lost on SW restart | Auto-lock uses Chrome Alarms API — persists across SW restarts. Snap cronjobs run on in-memory timers, but `CronjobController` keeps each event's next run date in state, and `init()` reschedules from it. A recurring job that came due while the worker was down runs at once, and a one-off background event that came due is dropped |
| State lost on SW restart | Wallet state persists in `chrome.storage.local`, with an IndexedDB backup |
| SW evicts frequently during active use | A keepalive writes `chrome.storage.session.set` on a short interval, and each `chrome.*`/`browser.*` call resets the 30s idle timer. Cold starts are frequent: about 5.3 per Chromium UI page open in July 2026 production telemetry, from causes that include browser launch and extension reload. Whether idle termination is also among them is not established. **Re-verify before relying on it — see below.** See `mv3-service-worker` knowledge for mechanism and verification discipline |

### Re-verify the keepalive before reasoning from it

This row is the only one that depends on a *current implementation detail* rather than on
absent handlers or persistent storage, and it is the one that inverts if the implementation
moves. If the interval grows past the idle timeout, or the keepalive is removed, the honest
answer flips from "the idle timer is reset" to "eviction happens routinely" — and a skill that
still asserts the first would be worse than no skill.

Confirm it in the target repo before drawing conclusions:

```bash
# the keepalive writer and its cadence — symbol names, not line numbers
grep -rn "saveTimestamp\|SAVE_TIMESTAMP_INTERVAL_MS" app/
```

Two things make the conclusion hold, and both must still be true:

1. The interval is **well under the ~30s idle timeout** (last verified: `2 * 1000` ms).
2. The callback performs an **extension API call** — `chrome.storage.session.set` — since it
   is the API call that resets the timer, not the timer firing.

If either has changed, treat active-session eviction as live and re-derive the rest of this
table's consequences.

*Verified against `metamask-extension` at `c31416a4781` (2026-09-14), in `app/service-worker.ts`:
`SAVE_TIMESTAMP_INTERVAL_MS = 2 * 1000`, `setInterval(saveTimestamp, …)`,
`saveTimestamp` calling `chrome.storage.session.set`.*

## Common Pitfalls

| Mistake | Correct Approach |
|---------|-----------------|
| "SW evicts N times/day → event fires N times/day" | Check if application code has handler for eviction |
| Assume frequency from platform behavior | Grep for actual handler chains in `background.js`, `app-state-controller.ts` |
| Conflate platform restart with application reset | Check which state is persisted vs re-initialized |
| "Keepalive uses `chrome.alarms`" | It does not — keepalive works by making an extension API call (`chrome.storage.session.set`) on a sub-idle-timeout interval. `chrome.alarms` is used separately, for auto-lock timers that must persist across SW restart |
| Citing this skill's keepalive claim without re-checking | It is the one row here that tracks a live implementation detail. Run the grep above; the conclusion inverts if the interval or the API call changes |
