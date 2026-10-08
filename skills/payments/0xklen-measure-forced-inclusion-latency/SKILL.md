---
name: measure-forced-inclusion-latency
description: Use when an incident plan or SLA depends on the real end-to-end time from submitting a forced-inclusion transaction on L1 to it executing on the L2.
---

# Measure forced inclusion latency

The escape hatch is only as useful as its worst-case latency, and that number is the sum of L1
inclusion, the inbox grace period, and L2 execution — three components you can only get right by
measuring them, not by copying a doc figure.

## Procedure

1. Break the path into timed segments and instrument each:
   - t0: submission of the L1 transaction.
   - t1: L1 inclusion (depends on base fee and priority; ~12 s per block but can stretch under
     congested blocks).
   - t2: end of the inbox grace period (Arbitrum 24 h = 86400 s; zkSync priority queue FIFO with a
     bounded refusal window).
   - t3: L2 execution and the first L2 block that contains it.

2. Capture t0 and t1 from the L1 receipt:

       L1TS=$(cast receipt $L1_TXHASH --rpc-url $L1RPC --field blockNumber)
       cast block $L1TS --rpc-url $L1RPC --field timestamp

3. Capture t3 from the L2: locate the delivered message or the executed call, then read its L2 block
   timestamp.

       cast receipt $L2_TXHASH --rpc-url $L2RPC --field blockNumber

4. Compute the honest worst case, not the happy case. If the sequencer honours the inbox promptly,
   latency is t3 - t1 (minutes). If it does not, latency is grace + t3 - t1, which is the bound you
   must plan against. Report both numbers.

5. Run a sample on a testnet or a fork before relying on it. Arbitrum Sepolia and OP Sepolia both
   expose the same inbox contracts, so the calldata and gas can be rehearsed without mainnet cost:

       anvil --fork-url $L1RPC & cast send $INBOX ... --rpc-url http://127.0.0.1:8545

6. Record per-sample: L1 gas cost, L1 base fee at submission, grace period observed, and L2 execution
   timestamp. Report min, median, and max over at least a handful of samples; a single measurement is
   not a latency estimate.

7. Feed the worst case into the incident runbook and set the retry/escalation triggers from it — if
   your service cannot tolerate a 24 h forced-inclusion bound, the L2 is not a fit for that workload.

## Pitfalls

- Quoting the doc's 24 h as the latency when the sequencer actually includes the delayed inbox in
  seconds; the honest answer is a range with the pessimistic branch flagged.
- Measuring from submission and not from L1 inclusion, which folds gas-market variance into what looks
  like inbox latency.
- Assuming the grace period is a fixed wall-clock constant when it is expressed in L1 blocks on some
  chains (Arbitrum uses L1 blocks, ~6.4 days for withdrawals but the delayed-inbox force window is
  block-based too).
- Ignoring that a forced transaction can itself fail on L2 (out of gas, revert) and that re-entry pays
  the full cost again.
- Treating one testnet sample as representative when L1 congestion dominates the L1-inclusion segment.

## Verification

```bash
# t1 from L1, t3 from L2, grace from the chain's config
L1_INCL=$(cast receipt $L1_TXHASH --rpc-url $L1RPC --field blockNumber)
L2_INCL=$(cast receipt $L2_TXHASH --rpc-url $L2RPC --field blockNumber)
# latency_happy = ts(L2_INCL) - ts(L1_INCL); latency_worst = grace + latency_happy
```

Report the two latency figures (happy-path and grace-bound), the grace period source, and the sample
size behind the numbers.
