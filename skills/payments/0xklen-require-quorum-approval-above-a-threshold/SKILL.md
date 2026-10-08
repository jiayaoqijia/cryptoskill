---
name: require-quorum-approval-above-a-threshold
description: Use when large transfers need more than one operator's sign-off. Enforces a per-amount quorum where the requester cannot approve their own request and approvals are bound to the exact payload.
---

# Require quorum approval above a threshold

A single approver on a large transfer is a rubber stamp. This skill binds approvals to the exact transaction hash and separates requester from approver, so an approval cannot be reused for a different payload.

## Procedure

1. Set the approval threshold in the signing service or guard so the check runs where funds move, not in the requesting UI. Common shape: anything above `X` needs `2` approvers, above `Y` needs `3`.
2. Bind each approval to the transaction hash, not to an amount or a free-text memo:
   `approver_signs(keccak256(abi.encode(chainId, to, value, data, nonce)))`
   A reused approval for a re-parameterised transaction must fail.
3. Require the approver to be a different identity than the requester, and check it in code, not by convention.
4. Display the decoded payload to each approver independently; each approver recomputes the hash rather than trusting the requester's summary.
5. Expire approvals after a short window — commonly 30 minutes — so a stale approval cannot be attached to a transaction built later.
6. Log every approval with approver id, payload hash, and timestamp, and emit an alert when a request collects approvals from the same device fingerprint.
7. After execution, verify the approval set is consumed and cannot be replayed.

## Pitfalls

- Approvals keyed to an amount rather than a hash let the requester swap the destination after approval; always bind to the full payload.
- A single person holding two approver identities (two accounts, one human) defeats the quorum; enforce distinct humans, not distinct keys.
- Requester==approver blocked in the UI only is bypassed by the API; enforce in the service.
- An approval with no expiry can be replayed days later when attention has moved on.
- Counting a "reply-all yes" email as approval is not a signed, hash-bound artifact; the artifact must be verifiable.
- Approvals collected over a chat tool that auto-threads are not hash-bound; the approver must sign, not type "yes".
- A quorum of keys on one laptop is one approver in disguise; require distinct devices.
- If the threshold lives in a config a single admin can edit, the quorum is bypassable; protect the config like funds.
- Log the rejection when requester equals approver, not just the acceptance.

## Verification

    # two approvals for the same payload hash should execute; a third for a mutated payload must reject
    grep -c "payload_hash=$HASH" approvals.log && cast send ... --rpc-url $RPC
    # expect each approval hash to match the executed tx and the mutated one to be refused

Report the threshold table, the payload hash, and the approver ids with distinct-fingerprint evidence, quoting the log lines.
