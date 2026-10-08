---
name: alert-when-governance-quorum-is-at-risk
description: Use when monitoring an active DAO vote that may fail on quorum or majority. Polls the tally against quorum and projects headroom from unvoted delegate weight.
---

# Alert when governance quorum is at risk

A proposal that quietly fails on quorum burns a week of proposer effort and signals apathy. Watch the tally against the quorum floor through the voting window and alert while there is still time to rally votes.

## Procedure

1. Read the floor once per proposal:
   `cast call $GOV "quorum(uint256)(uint256)" $BLOCK --rpc-url $RPC`
2. Poll the tally on an interval (every 15 minutes is enough for a multi-day vote):
   `cast call $GOV "proposalVotes(uint256)(uint256,uint256,uint256)" $ID --rpc-url $RPC`
3. Compute the two failure conditions separately:
   - quorum shortfall: `for + abstain < quorum`
   - majority loss: `for <= against`
4. Project remaining headroom: take the delegate weights that have not voted (from the delegate list minus `VoteCast` voters) and estimate the maximum achievable for.
5. Fire an alert when either fewer than 24 hours remain and quorum is not reached, or `for <= against` with under 48 hours left and unvoted for-capacity insufficient to close the gap.
6. Escalate only once per condition transition (not every poll) to avoid an alert storm:
   `alertfire "proposal $ID quorum at risk: for+abstain $SUM < $QUORUM, ${HOURS}h left"`
7. Record the final tally and whether the alert was correct, to calibrate the threshold.

## Pitfalls

- Alerting on every poll when the state has not changed; bound the alert to a condition transition or the channel is muted.
- Monitoring only for and ignoring abstain, which counts toward quorum in most governors.
- Using a single close-of-window check that fires when it is already too late; alert at the headroom, not the failure.
- Estimating headroom from token balances rather than `getPastVotes`; only delegated weight can vote.
- Treating a Defeated result as apathy without checking which condition failed; quorum and majority need different mitigations.

## Verification

    cast call $GOV "proposalVotes(uint256)(uint256,uint256,uint256)" $ID --rpc-url $RPC
    # compare for+abstain to quorum and for to against; the alert should fire on a true shortfall only

Report the polled tally, the quorum, the remaining hours, and whether the alert fired, with the poll command behind it.
