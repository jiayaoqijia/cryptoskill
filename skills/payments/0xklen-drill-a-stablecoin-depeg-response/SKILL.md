---
name: drill-a-stablecoin-depeg-response
description: Use when preparing for the day a held stablecoin breaks its peg. Runs a tabletop against price feeds, triggers, and pre-agreed actions so the response is practised, not improvised.
---

# Drill a stablecoin depeg response

A depeg is not a moment to invent a plan; it is a moment to execute a rehearsed one. Run the drill against live feeds and pre-agreed thresholds so every actor knows their trigger and their action before capital is at risk.

## Procedure

1. Define the trigger: median price across sources below 0.995 for 30 continuous minutes, or a redemption queue exceeding one business day.
2. Name the responders and the decision owner; a depeg is economic, so the owner is a treasury/capital role, not an engineer.
3. Enumerate the actions in order with the pre-authorisation for each:
   - Pause new settlement into the at-risk coin.
   - Shift receivables to a second issuer or a native asset.
   - Execute the redemption rehearsal path (from `test-stablecoin-redemption-under-stress`).
   - Hedge or exit via the market only if depth supports the size.
4. Rehearse with a fired alert on the real feed and a timed walkthrough: who is paged, how long to the first action.
5. Record decision latency and the exit capacity you actually have at T+0.
6. Rehearse the opposite failure too: a false alarm (a 20-minute wobble) must not trigger a full exit that itself moves the market.
7. After the drill, list gaps — missing relationship, unverified whitelist, untested PSM redemption — each with an owner.

## Pitfalls

- A trigger measured on a single venue, so one manipulated pool fires or hides the alarm.
- No pre-authorisation: during a real depeg everyone waits for a meeting and the exit window closes.
- Firing the response on a wobble and selling the bottom, turning a non-event into a loss.
- Assuming the market is the exit when the drill shows depth supports only a fraction of your size.
- Treating the drill as an engineering exercise when redemption, KYC, and banking are the real gates.
- Running the drill only with engineers present and discovering at the real event that treasury and legal are the blocking approvers.

## Verification

    python3 -c "print(round((first_action_ts - alert_ts)/60,1))"   # minutes alert -> first action
    # target: under the decision window you set (e.g. 15 minutes)

Report the trigger definition, the decision owner, the rehearsed time-to-first-action, and the identified gaps with owners.
