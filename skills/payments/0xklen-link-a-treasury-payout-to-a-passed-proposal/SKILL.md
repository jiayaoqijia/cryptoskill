---
name: link-a-treasury-payout-to-a-passed-proposal
description: Use when a DAO treasury signer is asked to release funds. Verifies the payout matches an executed proposal's target, amount, and calldata before the signature is given.
---

# Link a treasury payout to a passed proposal

A treasury multisig that pays on a chat request is a governance bypass. Every draw must be traced to a proposal that actually passed and executed, with the same recipient and the same amount.

## Procedure

1. Get the proposal id or link from the requester, then confirm it executed, not merely passed:
   `cast call $GOV "state(uint256)(uint8)" $ID --rpc-url $RPC`
   Only 7 (Executed), or a queued-and-executed timelock operation, counts.
2. Decode the proposal's calldata and extract the exact `(to, value, data)`:
   `cast calldata-decode "transfer(address,uint256)" <data>`
   For a batch proposal, decode every entry, not just the first.
3. Compare recipient and amount against the payout the signer is asked to approve. Any difference — a different treasury address, a changed amount, a swapped token — means stop.
4. Check the funds are not already moved: query the treasury balance and recent outflows so a duplicate payment is caught:
   `cast call $TOKEN "balanceOf(address)(uint256)" $TREASURY --rpc-url $RPC`
5. Confirm the proposal was for this treasury, not another one; DAOs often have operational and investment safes and a proposal for one does not authorise the other.
6. Record the proposal id, its state, and the decoded payload in the approval log alongside the signature.

7. Match the token and chain too: a proposal paying USDC on mainnet does not authorise USDC on a fork or another chain.
8. Confirm the proposal's executor was the treasury contract itself, not a delegate that would route funds elsewhere.
9. Reject a payout whose only source is a chat screenshot; require the proposal id and read it on-chain.

## Pitfalls

- Accepting a passed off-chain Snapshot vote as authority for an on-chain payment; the treasury executes what the timelock queued, not what the poll liked.
- Matching the proposal title to the payout while ignoring the calldata; a proposal titled "grants" can hide a transfer to the proposer.
- Paying the same executed proposal twice because the request was re-sent; a proposal is a one-shot authorisation.
- Approving a batch where entry three differs from the description; decode all entries.
- A payout to an address that differs from the proposal by one character — always compare full checksummed addresses, never the first and last four.

- A passed proposal still in the timelock queue cannot pay; executing before the ETA reverts and paying by hand bypasses it.
- Trusting a Tally or forum label that says Executed without reading `state(id)` on-chain.
- A USD-denominated request against a token-denominated payout leaves an exchange-rate gap the signer should not bridge.

## Verification

    cast call $GOV "state(uint256)(uint8)" $ID --rpc-url $RPC && cast calldata-decode "transfer(address,uint256)" <data>
    # state 7 and a decoded (to, amount) identical to the payout are both required before signing

Report the proposal id, its state, the decoded recipient and amount, and the treasury balance, with the commands behind them.
