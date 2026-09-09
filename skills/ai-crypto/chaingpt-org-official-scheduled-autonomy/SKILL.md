---
name: scheduled-autonomy
description: Run trading/DeFi strategies on a schedule — DCA every morning, grid rebalances, recurring health checks — using saved plans + the execution journal (due_steps/mark_step) + Claude Code scheduled agents, with the agent wallet executing inside hard policy caps. Triggers - run this daily, schedule a DCA, recurring buy, set and forget, autonomous strategy, cron strategy, execute my plan on a schedule, walk away.
---

# Scheduled Autonomy — strategies that run while the user sleeps

The full loop for hands-off strategy execution. Three layers make it safe:
1. **The plan** is explicit and saved to disk (what to do, when).
2. **The execution journal** makes runs idempotent (crashes and re-runs never double-buy).
3. **The agent-wallet policy gate** caps what any single run, or day, can spend — `maxTxValueWei` per tx, `maxDailySpendWei` + `maxDailyTxCount` per rolling 24h. The schedule cannot exceed the policy even if it fires a thousand times.

## The loop (memorize this shape)

```text
ONE-TIME SETUP
  1. chaingpt_strategy_dca_plan ...                 # produces steps + a JSON payload
  2. chaingpt_risk_token / chaingpt_research_token  # pre-flight the asset ONCE
  3. chaingpt_strategy_save_plan name=eth-dca type=dca payload=<the JSON>
  4. Agent wallet ready: chaingpt_agent_wallet_status
     → recommend the "DCA bot" policy template (single chain, single router, small caps)
  5. Create the schedule (see below)

EVERY SCHEDULED TICK (this is the prompt the schedule runs)
  1. chaingpt_strategy_due_steps name=eth-dca       # what's due? nothing → done, exit
  2. For each due step:
       a. chaingpt_dex_quote ...                    # fresh quote, sanity-check price impact
       b. execute:
          - agent-wallet mode: chaingpt_agent_wallet_sign_and_send (policy gate decides)
          - user-signs mode:   chaingpt_dex_build_swap_tx acknowledgeMainnet=true → present tx
       c. chaingpt_strategy_mark_step name=eth-dca stepId=<id> txHash=<hash>   # IMMEDIATELY
  3. Report: step(s) executed, spend vs daily cap, next step time
```

## Creating the schedule (Claude Code)

Use Claude Code's scheduled agents (`/schedule`) or any cron that invokes `claude`:

```text
/schedule create "eth-dca tick" --cron "0 9 * * *" --prompt
  "Run one tick of the saved plan 'eth-dca': call chaingpt_strategy_due_steps name=eth-dca;
   if nothing is due, stop. For each due step: fresh chaingpt_dex_quote (abort the step and
   mark it skipped with a note if price impact > 1%), execute via the agent wallet
   (chaingpt_agent_wallet_sign_and_send, memo 'eth-dca step <id>'), then immediately
   chaingpt_strategy_mark_step with the tx hash. Finish with a one-line summary."
```

Cadence note: schedule ticks MORE often than the plan cadence if you want catch-up behavior (a daily plan + daily tick that fails once skips a day; a daily plan + 6-hourly tick self-heals). `due_steps` returns everything overdue, so catch-up is automatic — the daily-spend cap bounds how much catch-up can execute at once.

## Hard rules

- **Mark immediately after execution.** An executed-but-unmarked step is returned again next tick. The journal is the only memory the schedule has.
- **Never mark before the tx is sent.** A marked-but-unexecuted step is silently lost money on the table.
- **Already-marked refusal means double-fire.** If `mark_step` says the step is already recorded, do NOT overwrite — investigate why the tick ran twice.
- **The policy gate's refusal is final.** If `sign_and_send` is refused (daily cap reached, kill switch on), mark NOTHING, report the refusal, and stop. Never coach the user into widening caps mid-run; that decision belongs to a non-scheduled session.
- **Pre-flight the asset once at setup, and re-check risk weekly** (`chaingpt_risk_token`) for long-running plans — tokens get compromised after launch too.
- Plans + journal are local files (`~/.chaingpt-mcp/plans/`). Nothing is uploaded.

## Failure handling

| Situation | Behavior |
|---|---|
| RPC/quote upstream down | Skip the tick (steps stay due; next tick catches up) |
| Price impact above the user's threshold | `mark_step status=skipped note="impact 2.3%"` — a skipped step is a decision, not a failure |
| Policy refusal (caps/kill switch) | Stop the tick, report, leave steps due |
| Plan complete | `due_steps` says COMPLETE — tell the user to remove the schedule |

## Modes

- **Agent-wallet mode (fully autonomous):** the wallet signs inside policy caps. Pair with the `dca-base` policy template. The PreToolUse mainnet guard will ask for confirmation in interactive sessions; for headless scheduled runs, the policy gate + velocity caps are the (deliberate) safety boundary — set `CHAINGPT_GUARD=off` ONLY in the scheduled environment, never globally.
- **User-signs mode (semi-autonomous):** the tick prepares unsigned transactions and the summary asks the user to sign. Zero custody risk; the user is the scheduler's hands.

Solana plans (v1.19+): same loop with `chaingpt_dex_jupiter_quote` → `chaingpt_dex_jupiter_build_swap_tx` → `chaingpt_agent_wallet_solana_sign_and_send` → `chaingpt_strategy_mark_step`. The lamport velocity caps (`policy.solana.maxDailySpendLamports` / `maxDailyTxCount`) are the third safety layer, exactly like the wei caps on EVM.

Related: `skills/strategy/SKILL.md` (planners), `skills/agent-wallet/SKILL.md` (policy gate), `reference/scheduled-autonomy.md` (10-minute end-to-end walkthrough).
