---
name: evaluate-sequencer-decentralisation-tradeoffs
description: Use when judging whether an L2's sequencer arrangement meets a trust requirement, by classifying who can order, censor, halt, and upgrade.
---

# Evaluate sequencer decentralisation tradeoffs

"Decentralised sequencer" covers four very different arrangements, and a due-diligence answer is only
useful if it names which one applies and what the operator can still do to a user's transaction.

## Procedure

1. Classify the ordering model. The families are: (a) single centralised sequencer with a known
   operator key; (b) leader-elected / rotating set (e.g. multiple sequencers with a consensus); (c)
   shared sequencer networks where a third-party set orders for many rollups; (d) based sequencing
   where the L1 proposer orders, inheriting L1 censorship resistance; (e) forced-inclusion only,
   where the sequencer orders but anyone can bypass it after a timeout.

2. For each model, answer the four trust questions explicitly: who can reorder, who can censor, who
   can halt liveness, and who can upgrade the bridge/verifier contracts.

3. Read the upgrade authority on L1. A decentralised sequencer behind a single-key proxy admin is
   still a single point of control. Inspect the proxy and its admin:

       cast call $PROXY "admin()(address)" --rpc-url $L1RPC     # EIP-1967
       cast storage $PROXY 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbcf

   Or read the admin slot directly and check whether it is a timelocked Safe or an EOA.

4. Check the escape hatch and its bound. Decentralisation is only real if a censored user can force
   inclusion or exit through L1 within a bounded, published window. Record that window (OP withdrawal
   7 days; Arbitrum delayed inbox 24 h to forceInclusion; zk priority queue).

5. Verify the prover/validator set independently of the sequencer. A zk rollup with a single prover
   is not trustless even with a decentralised sequencer; an optimistic rollup with one bonded
   proposer relies on the fraud-proof game being live and incentivised.

6. Summarise as a matrix with one row per property and the evidence (contract address, slot value,
   doc URL, on-chain parameter) behind each cell. Mark any property you could not verify as unknown,
   not as satisfied.

## Pitfalls

- Reading the marketing label ("shared sequencer") and not the contracts; the actual ordering contract
  is what binds a user.
- Treating a sequencer-set multisig as decentralisation when the set is co-located or upgradeable by
  one party.
- Ignoring upgrade keys: an admin that can swap the verifier can retroactively change finality.
- Confusing DA layer decentralisation with sequencer decentralisation; they are separate risks.
- Assuming the escape hatch works at scale — a forced-inclusion path with a long window and high L1
  gas is not an escape for a retail user mid-attack.

## Verification

```bash
cast call $PROXY "admin()(address)" --rpc-url $L1RPC
cast call $L2_OUTPUT_ORACLE "CHALLENGE_PERIOD()(uint256)" --rpc-url $L1RPC 2>/dev/null || \
  cast call $ROLLUP "confirmPeriodBlocks()(uint64)" --rpc-url $L1RPC
```

Report the ordering-model classification, the upgrade-authority address and whether it is timelocked,
and the forced-inclusion/withdrawal window — each cell backed by the call that produced it.
