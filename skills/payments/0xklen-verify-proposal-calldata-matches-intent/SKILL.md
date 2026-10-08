---
name: verify-proposal-calldata-matches-intent
description: Use when reviewing a proposal before voting, or auditing one after. Decodes every calldata entry and diffs it against the written description so hidden actions are caught.
---

# Verify proposal calldata matches intent

The description is a claim; the calldata is what runs. A proposer can write "grant X" and encode a transfer to Y, and the vote passes on the prose. Decode everything and diff.

## Procedure

1. Fetch the proposal's targets, values, and calldatas from the `ProposalCreated` event or the governor:
   `cast call $GOV "getActions(uint256)(address[],uint256[],bytes[],bytes32)" $ID --rpc-url $RPC`
2. Count them. If the description mentions N actions and there are N+K calldatas, the extra K are the finding.
3. Decode each calldata against the target's ABI:
   `cast calldata-decode "transfer(address,uint256)" <data>`
   For unknown selectors, resolve with `cast 4byte <selector>` and confirm against the verified source.
4. Write the decoded action list next to the description sentence it claims to implement. Mark any action with no corresponding sentence, and any sentence with no action.
5. Pay special attention to `upgradeTo`/`upgradeToAndCall`, `grantRole`, `approve`, and `setImplementation` entries; these change future behaviour, not just the balance.
6. Check the executor (timelock) address: a proposal targeting a short-delay or unguarded contract bypasses the intended dwell time.
7. Publish the decoded diff in the vote forum before the snapshot block.

8. Recompute the description hash and confirm it matches the one in `ProposalCreated`; a rewritten description invalidates the mapping.
9. For a batch, verify the array lengths of targets, values, and calldatas are equal; a mismatch is malformed and should abort.
10. Flag any calldata whose selector is not in the target's verified ABI; an unknown selector is an unconditional stop.

## Pitfalls

- Decoding only calldata[0]; a batch proposal hides the payload in a later entry.
- Trusting a decoded "transfer" without checking the token contract; a transfer on a fake token that mimics the real one moves nothing real but grants approvals.
- Reading the description's rendered Markdown, which can hide text behind collapsible sections or images; read the raw description hash.
- Assuming a selector means what it says; verify it against the verified source at the target address, not a four-byte registry that anyone can seed.
- Missing a `delegatecall` entry — a proxy upgrade routed through `delegatecall` executes foreign code with the treasury's storage.

- Trusting `getActions` to return what executed; after execution a governor may clear storage, so read the event instead.
- Assuming a value of 0 means no ETH moves; a token transfer carries its value in calldata, not the `value` field.
- Overlooking a `sweep` or `rescueTokens` entry that drains a contract the proposal merely claims to configure.

## Verification

    cast call $GOV "getActions(uint256)(address[],uint256[],bytes[],bytes32)" $ID --rpc-url $RPC
    # then cast calldata-decode each entry; every entry must map to a sentence in the description

Report the count of calldata entries, the decoded action list, and the one-line mapping to the description, with the raw calldatas quoted.
