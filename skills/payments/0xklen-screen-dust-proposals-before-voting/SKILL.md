---
name: screen-dust-proposals-before-voting
description: Use when a governor is being spammed with low-quality or tiny-threshold proposals, and to decide which proposals deserve attention. Filters by proposer, threshold, and payload risk.
---

# Screen dust proposals before voting

A governor with a low proposal threshold accumulates junk proposals that dilute attention and can hide a malicious one. Screen by proposer history and payload before spending vote weight on any of them.

## Procedure

1. Read the proposer threshold; a low or zero threshold is the root cause:
   `cast call $GOV "proposalThreshold()(uint256)" --rpc-url $RPC`
2. Enumerate recent proposals from the `ProposalCreated` event and group by proposer:
   `cast logs --from-block $START --address $GOV "ProposalCreated(uint256,address,address[],uint256[],string[],bytes[],uint256,uint256,string)" --rpc-url $RPC`
3. Rank by: proposer's first-seen date, number of proposals in the window, and whether any previously passed. A brand-new address filing five proposals in a day is the spam pattern.
4. Decode each candidate's calldata (`cast calldata-decode`) and drop any that touch treasury, role, or upgrade selectors unless accompanied by a proper forum post.
5. Check quorum reachability cheaply: a dust proposal from an unknown proposer almost never reaches it, so voting is wasted unless it is genuinely close.
   `cast call $GOV "proposalVotes(uint256)(uint256,uint256,uint256)" $ID --rpc-url $RPC`
6. If the governor allows a cancel threshold, propose raising `proposalThreshold` after the spam subsides rather than voting each dust item down.

7. Check whether the proposer has ever been delegated to; a proposer with weight can pass a stealth proposal under low turnout.
8. Watch for proposals sharing a calldata hash with a previously defeated one; a resubmission is a repeat attempt.
9. Keep a short list of known-good proposers so routine items are not re-screened every cycle.

## Pitfalls

- Voting against dust proposals, which still costs gas and validates them; sometimes abstaining is cheaper.
- Ignoring the spam because it cannot pass, while one dust proposal carries the actual malicious payload; decode, do not dismiss.
- Setting `proposalThreshold` so high that legitimate small holders cannot propose; balance against spam.
- Assuming a proposal's proposer is a human; many are bot relayers acting for a delegate, so group by the delegate behind them.
- Screening by title only; the malicious proposal is often the one with the most reassuring name.

- Treating a proposal as harmless because it is 'just' a parameter change; large fee or quorum changes are governance captures.
- Ignoring the proposal bond rule; if the governor refunds the deposit, spam is free and must be filtered socially.
- Confusing a low-poll proposal with dust; a low vote count is not itself spam — the payload and proposer are.

## Verification

    cast logs --address $GOV "ProposalCreated(...)" --rpc-url $RPC | grep -c $PROPOSER
    # a proposer count well above the median, from a fresh address, is the spam signal

Report the proposer-threshold value, the per-proposer counts, and which proposals were decoded and dropped, with the log query behind them.
