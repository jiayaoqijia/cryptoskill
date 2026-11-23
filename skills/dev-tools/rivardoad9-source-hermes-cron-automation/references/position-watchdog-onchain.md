# Position watchdog: price cut/target + on-chain balance change (silent)

Shape built and tested 30 Sep 2026 (job `b27e1e0c569b`, STONK guardrail).

## Shape

- Cron: `no_agent=true`, `schedule="every 1h"`, `script="<name>.py"`, `deliver=origin`.
  Empty stdout = no message, so an hourly job can run all day without spamming.
- The script fires on **three** triggers, not just price:
  1. price breaches the position's **cut level** (the written plan level — never a level moved to feel
     better)
  2. price reaches the target/trim zone
  3. **the on-chain balance of the watched mint changed** → the user learns a buy/sell happened
     without having to tell you
- State file `~/.hermes/data/<name>_state.json` holds `{flag, prev_balance, last_price, last_check}`.
  Alert on price only when `flag` **changes** (`""` → `"cut"` → `""` → `"cut"` fires again). That is
  the dedupe that keeps an hourly job quiet while price sits below the cut for days.
- **Prime `prev_balance` on the first run without alerting.** Compare only when a previous value
  exists, otherwise run #1 "detects" a change from 0 → real balance and pings falsely.
- Sources: the token's own platform API for price when it has one (keyless, no GMGN rate-limit
  exposure); public RPC `getTokenAccountsByOwner` with a mint filter for balance (remember Token-2022
  for reward coins / xStocks).
- **Test twice before scheduling**: run 1 creates state, run 2 must print nothing. Never schedule a
  watchdog you have not personally seen stay silent.
- Reach for this only for positions with a written invalidation level — it is a guardrail tied to a
  plan, not a price-alert subscription.
