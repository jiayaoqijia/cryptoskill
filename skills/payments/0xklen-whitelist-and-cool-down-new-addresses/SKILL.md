---
name: whitelist-and-cool-down-new-addresses
description: Use when a wallet allows outbound transfers and you want a new destination to be reversible. Maintains a destination allowlist with a mandatory cooldown before a newly added address can receive.
---

# Whitelist destinations with a cool-down

The last mile of almost every key compromise is a fast transfer to an attacker-chosen address. An allowlist plus a time delay makes that last mile loud and reversible: a new address cannot be paid until people have had time to notice.

## Procedure

1. Maintain an allowlist of destination addresses in the signing layer, keyed by `(chainId, address)`, with metadata: label, owner, added-by, added-at.
2. Enforce the allowlist at the guard or policy engine, not the app. Any transfer to a non-listed address must revert.
   ```solidity
   require(allowlisted[tx.to], "destination not allowlisted");
   ```
3. Give every newly added address a mandatory cool-down before it can receive — 24h for routine counterparties, 72h for treasury-scale amounts. During the window the address is visible but blocked.
4. Require two independent approvals to add an address: the requester cannot be the approver, and the approval must happen after a person verifies the address out of band (a signed message or a callback to a known contact).
5. Record the add event with a hash of the address and the approver id so the audit trail cannot be silently rewritten.
6. Re-verify allowlisted addresses periodically. A counterparty can change custody of an address, and a stale entry is a live risk.

## Pitfalls

- An allowlist that can be edited by the same key that signs transfers provides no delay; the attacker adds their address and pays it in one batch.
- Checking only the first four hex characters ("looks like 0xabcd…") lets an attacker grind a vanity address that shares the prefix.
- Cool-downs stored only in the UI are bypassed by calling the contract directly; the block must live in the enforcement layer.
- Circular: allowlisting the exchange deposit address that itself forwards anywhere means the allowlist no longer bounds risk — treat forwarding addresses as unlisted.
- Forgetting contract-to-contract flows: a permit or a router can move funds to an arbitrary address without an explicit transfer; bound approvals too.
- Removing an allowlisted entry should itself require a cool-down, or an attacker with config access swaps an entry and pays it immediately.
- A whitelist enforced on the transfer path but not the approval path lets a stale approval bypass it.
- The cool-down clock must live on-chain or in the signing service, not in the requesting app's local time.
- When two chains share an address format, key the allowlist by chain id so a testnet address cannot be reused on mainnet.

## Verification

    cast send $TOKEN "transfer(address,uint256)" $NEW_ADDR 1 --account hot --rpc-url $RPC
    # expect a revert "destination not allowlisted" until the cool-down elapses and approvals land

Report the destination, its added-at timestamp, and the revert from the blocked attempt, quoting the command.
