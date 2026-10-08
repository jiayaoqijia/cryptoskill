---
name: separate-deployer-and-treasury-keys
description: Use when one key both deploys contracts and holds treasury funds. Splits deploy, operational, and treasury roles onto distinct keys so a compromise of any one cannot reach the others.
---

# Separate deployer, operational, and treasury keys

One key that can both upgrade a contract and spend the treasury is a single point of compromise for both. This skill splits roles so each key can do exactly one job, and none of them alone can move significant value.

## Procedure

1. List the roles your system needs: deploy/upgrade, hot operational spend, cold treasury reserve, and admin/ownership of access-controlled contracts. Assign a distinct key or Safe to each.
2. Cap what each role can do:
   - Deployer: no funds beyond gas; ownership of contracts transferred away after deployment.
   - Operational: bounded by the hot-wallet ceiling; cannot upgrade.
   - Treasury: cold, multisig, spends only via full ceremony.
3. After deployment, transfer contract ownership to the treasury Safe so the deployer key is no longer privileged:
   `cast send $CONTRACT "transferOwnership(address)" $TREASURY_SAFE --account deployer --rpc-url $RPC`
4. Verify the deployer no longer holds any admin role:
   `cast call $CONTRACT "owner()(address)" --rpc-url $RPC`
5. Keep the deployer key without funds and, ideally, with its own limited-use RPC that cannot touch the treasury chain's private mempool lightly.
6. Document which key owns which role; an undocumented "spare" admin key is the one that gets forgotten and leaked.

## Pitfalls

- A two-step `transferOwnership` (Ownable2Step) leaves the deployer as pending owner until the recipient calls `acceptOwnership`; the transfer is not done until then.
- Renouncing ownership to `address(0)` to "remove the deployer" also removes your ability to fix the contract; prefer a treasury Safe.
- A deployer key that is also a treasury signer reintroduces the coupling you split; keep the sets disjoint.
- Never store the deployer key or any private key on a shared CI runner as a plain variable; load it from a restricted file or a keystore the job cannot exfiltrate.
- Roles verified once drift; a later "quick fix" grant to the deployer can silently re-privilege it.
- A proxy admin key is a hidden deployer; transfer it to the treasury Safe too, or it can upgrade behind your back.
- If the deployer is a plain EOA in CI, one leaked CI secret upgrades or drains; use a Safe or an HSM.
- Role separation decays without monitoring; alert on any grant to a previously unprivileged address.
- Document the deployer's gas funder separately; topping it up from treasury blurs the roles.

## Verification

    cast call $CONTRACT "owner()(address)" --rpc-url $RPC && cast call $CONTRACT "pendingOwner()(address)" --rpc-url $RPC
    # expect owner == treasury safe and pendingOwner == 0x0; deployer appears in neither

Report the role-to-key mapping and the owner/pendingOwner reads, quoting the commands.
