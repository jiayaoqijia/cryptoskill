---
name: contain-a-compromised-signer-key
description: Use when one signing key in a custody set is suspected stolen. Runs an ordered response: freeze spend, rotate the key, drain reachable funds, and prove no in-flight withdrawal is pending.
---

# Contain a compromised signer key

Speed matters more than diagnosis once a key is suspected stolen, but the order of operations decides whether you recover funds or hand them over. This skill sequences freeze, rotate, and drain so the attacker cannot complete a pending withdrawal while you rotate.

## Procedure

1. Stop accepting requests through the compromised path first: pause the policy engine for that signer and revoke any session token or API key bound to it. A pause is reversible; a wrong transfer is not.
2. Read the pending state before touching keys. Any queued or pending transaction signed by the compromised key must be identified:
   `cast nonce $COMPROMISED --block pending --rpc-url $RPC`
   If the attacker has a signed, unbroadcast withdrawal, you are racing it — replace or cancel it at the same nonce.
3. Rotate the key out of the custody set. For a Safe, `swapOwner`; for MPC, have the vendor exclude the share and re-key. Do this before draining, so the drain is not itself drained.
4. Move at-risk funds from any wallet the compromised key can solely control. If it holds an unlimited token allowance, the attacker can pull at any time — revoke allowances and sweep balances together.
5. Rotate every credential the key touched: RPC providers, RPC URLs in config, CI secrets, and any `.env` the key was loaded from.
6. Preserve evidence: the pending-tx hash, the last signed messages, the access logs, and the derivation path. Do not wipe the host before imaging it.
7. Write the timeline with UTC timestamps and the command output behind each step.

## Pitfalls

- Rotating before cancelling a pending withdrawal lets the attacker's transaction land during the window; check nonce state first.
- If the compromised key had an unlimited allowance, sweeping the balance without revoking still leaves the funds pullable in the same block.
- Never paste the compromised key or any seed into a chat, a shell argument, or a log while investigating — reads come from a restricted file; assume every channel is watched.
- Assuming the compromise is one key when the vector was a shared host; rotate the whole set if the host was common.
- Posting a "we are safe" message before confirming no second signer is affected misleads counterparties.
- The attacker may hold a copy of the host, not just the key; rotate on a clean machine.
- If the compromised key is a Safe owner and the other owners exactly meet the threshold, rotate before the attacker proposes a malicious Safe transaction.
- Draining into a wallet that shares a signer with the compromised set does not protect the funds.
- Alert the exchange or bridge whose deposit address the key could reach, so they can flag follow-on deposits.
- Confirm the attacker's address is not already on an allowlist before you assume the guard blocks them.

## Verification

    cast nonce $COMPROMISED --block pending --rpc-url $RPC && cast call $SAFE "getOwners()(address[])" --rpc-url $RPC
    # expect the compromised address gone from owners and no pending nonce left on it

Report the freeze time, the rotation transaction hash, the swept amount, and any pending tx cancelled — each with its command.
