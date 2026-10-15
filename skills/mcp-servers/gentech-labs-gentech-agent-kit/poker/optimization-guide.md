# Tournament Poker Agent — Optimization Guide

## Architecture: Why Daemon Over Cron Watchdog

S8 Playground uses a cron watchdog (8s polling, 30s clock) — works fine with margin.
S7 Tournament proved cron breaks under tight time constraints:

| Factor | S8 Playground | S7 Tournament | Impact |
|--------|:------------:|:-------------:|--------|
| Action clock | 30s | **20s** | Less polling margin |
| Cron gap | ~4s | ~4s | Can miss 1/5 of clock |
| Cost per hand | Free | **MON tokens** | Missed hand = wasted money |
| API field | `message` | **`message` + `reasoning`** | Old script → 400 errors |

**Solution:** Continuous daemon, polls every 3s at table / 8s in queue. Zero gaps.

## Hard Restrictions

1. **No auto-rebuy** — costs MON. Daemon logs but never funds.
2. **PID file guard** — prevents duplicate daemon instances.
3. **3s minimum poll** — don't poll faster than 3s.
4. **4s deadline buffer** — safe-action (<4s remaining) defaults to check > call > fold.

## Optimization History

| Date | Change | Why |
|------|--------|-----|
| Jul 19 | Cron → Daemon | 20s clock too fast. Missed A2o UTG hand (auto-fold). |
| Jul 19 | Added `reasoning` field | Tournament API requires it. Old script → 400 error. |
| Jul 19 | Adaptive polling | Reduce API load when waiting, catch every table action. |

## Future Improvements

| Improvement | Effort | Impact |
|-------------|:------:|:------:|
| Stack-depth raise sizing | Medium | High |
| Blind-level tracking | Low | Medium |
| Opponent VPIP/PFR tracking | High | High |
| ICM push/fold decisions | High | Very High |
| Auto-rebuy config toggle | Low | Medium |
