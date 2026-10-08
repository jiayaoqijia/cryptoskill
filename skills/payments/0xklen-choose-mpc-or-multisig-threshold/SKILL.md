---
name: choose-mpc-or-multisig-threshold
description: Use when deciding how a set of keys will control funds. Compares MPC key-shares against an on-chain multisig on verifiability, recovery, and chain support before anyone commits.
---

# Choose between MPC and an on-chain multisig

MPC and multisig solve different halves of the same problem, and picking wrong shows up only at recovery time. This skill forces the decision onto explicit properties — who can verify a signature, how a share is recovered, and which chains the scheme supports — instead of vendor defaults.

## Procedure

1. List the assets and chains the wallet must sign for. On-chain multisig needs contract support per chain; an EVM-only Safe does not cover Solana or Bitcoin, and a chain with no compatible multisig forces MPC or a native threshold scheme.
2. Decide who must verify. A multisig lets any third party re-derive the address and check signatures on a public explorer. MPC produces one ordinary key, so verification is off-chain and ultimately trusts the vendor's protocol.
3. Count the operational cost of a signing round. A 2-of-3 Safe needs two separate devices online per spend; a 2-of-3 MPC can be a single API call — convenient, and also the thing that turns one hot server into a signing party.
4. Set the threshold from the loss model, not habit. `t` of `n` with `t >= 2` and `n - t >= 1` tolerates one lost share without tolerating one compromised share:
   - 2-of-3: one key can be lost or compromised, but not both.
   - 3-of-5: tolerates two losses or one compromise.
5. Write the recovery story for the worst case — all cosigners unavailable. For multisig that is the on-chain owner set plus a fresh deployment; for MPC it is the share backups plus the vendor's recovery protocol.
6. Check exit risk. A Safe can be migrated by its own owners without the vendor; an MPC key cannot be recovered if the vendor dies unless a documented share-export path exists.
7. Record the decision with the rejected option and the reason.

## Pitfalls

- Treating "2-of-3" as portable: a 2-of-3 Safe and a 2-of-3 MPC have different failure modes and cannot be swapped at migration time.
- Assuming MPC shares are independently safe when all three live on the same vendor's cloud — three shares under one provider is a single point of failure with extra steps.
- Forgetting gas: a Safe spend is an on-chain transaction that costs gas and has nonce ordering; an MPC signature is not.
- Choosing MPC on a chain where an on-chain scheme already exists (Bitcoin's native multisig), giving up public verifiability for no reason.
- A vendor's "2-of-3" may be 2-of-3 of *their* parties, not yours; read whose devices form the quorum before trusting the count.
- MPC signing latency and API uptime become your spend latency and uptime; an on-chain Safe only depends on the chain.
- Migrating an MPC vendor is a re-key, not an export, unless share migration is contractually supported.
- For a single-chain EVM treasury, an on-chain Safe is usually simpler to audit and gives public verifiability.

## Verification

    cast call 0x<safe> "getOwners()(address[])" --rpc-url $RPC
    # expect the owner set and threshold to match the documented policy; an MPC key has no such call

Report the scheme, the threshold, and the two properties that decided it — public verifiability and recovery path — with the command outputs that support them.
