---
name: detect-vote-buying-in-bribe-markets
description: Use when assessing whether DAO votes are being bought, or before relying on a delegation as independent. Correlates bribe-market deposits with delegate voting and flags concentrated paid influence.
---

# Detect vote buying in bribe markets

Bribe markets (Votium, Hidden Hand, Paladin) pay delegates to vote a certain way. That is not always illegitimate, but an undeclared, concentrated dependency means the vote reflects the payer, not the delegate's judgement. Detect and quantify it.

## Procedure

1. Pull the delegate's votes for a gauge or proposal:
   `graphql { votes(first:100, where:{voter:"$DELEGATE"}) { proposal { id } choice } }` against the DAO's subgraph, or read `VoteCast` logs.
2. Pull the same delegate address' bribe receipts from the market. On Votium the claim events are `Claimed` on the vlAURA wrapper; on Hidden Hand read the `BribeDeposited` events for the round.
3. Correlate: for each round, compare the delegate's vote direction with the bribe offering the largest per-gauge payout. A delegate who votes with the top briber in over 80% of rounds is effectively a paid voter.
4. Quantify concentration. Sum bribe value received in the last N rounds and divide by the delegate's estimated monthly operating cost; a ratio above about 1 means the income depends on bribes.
5. Check disclosure: search the delegate's forum thread for a bribe policy. Undisclosed paid voting is the finding, not the payment itself.
6. Detect self-dealing: a party that both deposits bribes and votes through a delegatee it controls is buying its own proposal.
7. Report per-round: bribe payer, amount, delegate vote, and whether the correlation held across rounds.

8. Fetch the delegate statement and check whether bribe income is disclosed; silence is the finding.
9. Compare the delegate's actual vote against their pre-vote stated intention; a flip that matches the top bribe is the signal.
10. Aggregate across delegates: if several top voters side with the same briber, treat it as coordinated paid influence.

## Pitfalls

- Treating every bribe as corruption; disclosed, capped bribe markets are a legitimate incentive design — flag the undisclosed and the concentrated, not the mechanism.
- Correlating a single round and calling it a pattern; delegates often agree with the largest briber by shared interest, not payment.
- Ignoring proxy claimers: the on-chain recipient is a claim contract, and you must walk the transfer to the delegate to attribute it.
- Assuming a bribe changed the vote; unless the delegate's vote differed from their historical lean, the bribe may have bought nothing.
- Missing off-chain payments (tokens sent to a treasury, OTC deals) that never touch the market contract.

- Attribution error: a claim contract receives the bribe and forwards it later, so the immediate recipient is not the voter.
- A delegate who abstains on bribe-heavy gauges may be avoiding the conflict; note abstention, do not treat it as clean.
- Using USD bribe values without the rate and date makes the ratio to operating cost non-reproducible.

## Verification

    graphql { votes(where:{voter:"$DELEGATE"}) { proposal { id snapshot } choice } }
    # join against the market's Claimed/BribeDeposited events per round; >80% agreement is the flag

Report the round-by-round payer, amount, and vote, the agreement rate, and whether a bribe policy is disclosed, with both datasets cited.
