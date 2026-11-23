# Delta-gated alerts & watchlist-member removal (1 Oct 2026)

Two rules from one session on the holdings watchdog + the re-rating lane. Both are class-level:
they apply to every recurring alert lane on this stack, not to those two scripts.

## A. Alerts must be CHANGE-gated, not schedule-gated

User's standing preference, verbatim: *"alert pola rerating ksih tau klo pas ad perubahan aja"*
— tell me only when something actually changed. Combined with the same day's
*"alert paid ilangin aja"*, the operating rule for every alert lane is:

> A recurring lane may run as often as it likes, but it must only **speak** when a measured
> delta crossed a threshold — never because N hours elapsed.

### Root cause to check FIRST when a lane repeats itself

The re-rating script (`~/.hermes/scripts/pump_alert.py`, cron `0 */3 * * *`, `no_agent`) had
`load_state()`, `save_state()` and a 12h per-(token, jenis) cooldown — but `main()` **never
called `save_state()`**. A defined-but-uncalled persistence helper is indistinguishable from
working dedupe in code review, and behaves like none at all: the same 5 tokens were re-sent
with identical numbers every 3 hours.

**Diagnostic, before touching thresholds:**

```
ls -la ~/.hermes/data/<lane>_state.json     # does the file the code reads even exist?
grep -n "save_state\|load_state" <script>   # defined ≠ called
```

If the state file is missing after several scheduled runs, persistence — not the threshold —
is the bug. Tuning thresholds on top of a broken state write just hides it.

### The pattern: snapshot + named deltas

Per alerting entity store a snapshot and re-send only on measured movement. Thresholds used
(re-rating lane; scale to the lane's volatility):

| Trigger | Threshold |
|---|---|
| 7-day move | ±8 pp vs last alert |
| turnover (vol24 / mcap) | ±5 pp |
| price | ±15% |
| distance from ATH | ±8 pp |
| pattern class changed | any (KATALIS ↔ RERATING ↔ MOMENTUM) |
| **new catalyst headline** | title not in stored `titles[]` — noisiest, most valuable |
| re-entry | entity qualified again after ≥12h out of the pattern |
| min gap | 2h between alerts for the same entity (anti-churn) |

Housekeeping that the pattern needs to work:
- Keep `qualified_last[]` from the previous run, otherwise re-entry cannot be detected.
- Prune snapshots not seen for 7 days so the state file does not grow unbounded.
- **Suppress, don't drop, when the min gap blocks a genuine change**: skip the send but leave
  the snapshot untouched, so the pending change still reports once the gap passes.
- Store the *reasons*, not a boolean. Render them into the message
  (`🔔 yang berubah: 7 hari +18.0% → +28.6% (+10.6 poin)`; first sighting = `BARU muncul di
  radar`). The user gets a delta they can act on instead of numbers they must diff by eye.

### Verification: 3 runs, ~10 min, no user-visible noise

1. **Cold run** — no state file → alert for every qualifying entity (`BARU muncul`).
2. **Immediate re-run** — nothing changed → **zero bytes of stdout**. This silence IS the
   deliverable; quote it as the proof.
3. **Tampered run** — `cp state /tmp/x.json`, then edit ONE entity to an older snapshot
   (`ch7 -= 10`, `ts = now - 5*3600`) and re-run → alert for **only that entity**, with the
   delta named. **Restore the backup afterwards** — leaving test values in production state
   manufactures a spurious alert on the next tick.

Without step 3, runs 1 and 2 are also explained by a filter that never fires, so step 3 is what
separates "I added a filter" from "the filter works".

## B. Removing one asset from a watch lane

Asked to drop PAID from the holdings alerts. Deleting the obvious block is only half of it —
a cut asset resurfaces through stale state and through *other* jobs' prompts that still name it.
Checklist:

1. **Code**: the asset's fetch function, its mint/constant, its threshold block in `CONFIG`, and
   every `mark(state, "<ASSET>_…")` key. Also fix the module docstring and the `--debug` table,
   which still list it.
2. **Stale state, self-healing**: prune the removed asset's keys on each save instead of
   hand-editing the JSON, so a half-migrated state heals itself:
   ```python
   for k in [k for k in list(state.get("alerts", {})) if k.startswith("PAID")]:
       state["alerts"].pop(k, None)
   state.get("last", {}).pop("PAID", None)
   ```
3. **Cron metadata**: rename the jobs so their titles stop claiming the asset
   (`Holdings watchdog (BTC/ONDO/INJ) — 15m`), not just the script.
4. **Sibling prompts**: grep `~/.hermes/cron/jobs.json` for the asset name. The digest and the
   20:00 trade-radar prompt both named it (as a monitored holding, as a "contoh acuan" for low
   caps, and in the fact block) — an LLM job handed `PAID` in its instructions will keep
   mentioning it in the report long after the script stopped emitting it. Replace those with an
   explicit **ban line** (`PAID SUDAH DICUT — JANGAN dibahas, disebut, atau dijadikan contoh`)
   rather than silently deleting the sentence, and add the asset to any "holdings user" list in
   the prompt.
5. **Verify**: re-run the script's `--debug` and confirm the asset is gone from both the table
   and the state file; then re-count occurrences in `jobs.json` — the only surviving mentions
   should be the ban lines themselves.

Related: `references/watchdog-alert-spam-dedupe.md` (time-horizon dedupe, delivery contract),
`references/holdings-watchlist-thresholds.md` (per-asset volatility thresholds + QA order).
