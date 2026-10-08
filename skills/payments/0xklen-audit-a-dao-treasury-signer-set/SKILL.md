---
name: audit-a-dao-treasury-signer-set
description: Use when reviewing who can move a DAO treasury, or after a signer change. Compares the multisig's on-chain owners and threshold against the governance-approved roster.
---

# Audit a DAO treasury signer set

The treasury multisig is only as legitimate as the signer set governance approved. A signer silently swapped in, or a threshold lowered by one, changes who controls the funds without a vote.

## Procedure

1. Read the current owners and threshold:
   `cast call $SAFE "getOwners()(address[])" --rpc-url $RPC`
   `cast call $SAFE "getThreshold()(uint256)" --rpc-url $RPC`
2. Fetch the governance-approved roster: the proposal that last set the signer set, decoded from its calldata.
   `cast call $GOV "getActions(uint256)(address[],uint256[],bytes[],bytes32)" $ID --rpc-url $RPC`
3. Diff the two sets: any owner not in the approved list, or a missing approved owner, is a finding.
4. Check no two owners are controlled by one key: compare against a known cluster map, and flag duplicate hardware-wallet addresses or an owner that is an EOA of a current signer's hot key.
5. Verify the threshold still matches the approved value; a threshold reduced from 4/7 to 3/7 is a governance change even if the owners are identical.
6. Confirm the Safe is the timelock's beneficiary, not a rogue parallel treasury: the address the governor pays must equal this Safe.
7. Re-run after every `AddedOwner`/`RemovedOwner`/`ChangedThreshold` event; alert on any that does not trace to an executed proposal.

8. Check each owner is still an active signer, not a departed member or a revoked key; a stale owner is a standing point of compromise.
9. Confirm no owner is a contract that cannot sign (e.g. the governor's own timelock); a non-signing owner quietly lowers the effective threshold.
10. Record the audit block and the proposal id that last authorised the set, so the check is reproducible later.

## Pitfalls

- Auditing owners but not the threshold; the same owners with a lower threshold is a weaker control.
- Assuming the owners are the governance council when the founding team holds the keys from before the DAO existed.
- Missing a signer module: a Safe with an enabled module (e.g. a recovery or spending-limit module) can move funds without the normal threshold.
- Treating the Safe address as canonical without checking the governor's target; a proposal to pay a different, similarly-named Safe is the attack.
- Ignoring signer rotation history; a signer added and removed within a term may still hold a copy of the config.

- A Safe whose owners include the deployer EOA from before governance existed still grants that key standing weight.
- Trusting the Safe UI's owner list; read `getOwners()` on-chain, since a pending owner change is not yet applied.
- A module-enabled Safe can be drained through the module without any owner signing; check `getModulesPaginated`.

## Verification

    cast call $SAFE "getOwners()(address[])" --rpc-url $RPC && cast call $SAFE "getThreshold()(uint256)" --rpc-url $RPC
    # owners set and threshold must equal the decoded roster from the executed proposal

Report the owner set, the threshold, the approved roster, and any diff or non-governance signer change, with the events cited.
