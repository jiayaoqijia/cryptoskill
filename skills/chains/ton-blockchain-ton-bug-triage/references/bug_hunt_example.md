# Workflow B Example: Mixed Network Negative Result

Use this example when validating a potential consensus bug with a mixed network and you need a concrete model for a valid negative result.

## Scenario Summary

- Workflow: `Workflow B — trigger via validator behavior`
- Potential bug: `skip_intervals_` dereference on `lower_bound() == end()` in the Simplex pool path
- Goal: construct conditions where the probing node reorders SkipCerts and withholds proposals inside a leader window
- Observed result: the network continued to produce blocks to masterchain seqno `300`; no liveness failure was observed in this setup

This is a useful outcome because the probing path executed and the honest nodes stayed healthy.

The exact node counts, ports, seqno targets, and probing windows here are investigation-specific. Reuse the structure of the experiment, not the exact numbers.

## Setup

1. Build the repo.
2. Snapshot the clean baseline build:
   copy `build/` to `vanilla-build/` before probing changes.
3. Patch the probing build only:
   - `validator/consensus/simplex/pool.cpp`
     add SkipCert reordering logic and probing markers.
   - `validator/consensus/simplex/consensus.cpp`
     log consensus config and leader-window transitions.
   - `validator/consensus/block-producer.cpp`
     add proposal withholding gated by env vars.
4. Rebuild the probing build.

## Probing Inputs

The verified env-var shape was:

- `TON_PROBING_REORDER_SKIP_CERTS=1`
- `TON_PROBING_WITHHOLD_PROPOSALS=1`
- `TON_PROBING_WITHHOLD_START=3`
- `TON_PROBING_WITHHOLD_END=7`

The probing node was treated as self-immune:

- the run was only considered valid if the probing node stayed alive until the honest-node effect was ruled in or ruled out

## Example Run

```bash
python3 /path/to/skill/scripts/run_mixed_network.py \
  --repo-root /path/to/repo \
  --build /path/to/repo/vanilla-build \
  --probing-build /path/to/repo/build \
  --workdir /path/to/repo/tmp/tontester-mixed-probe-lw10 \
  --base-port 2201 \
  --normal-nodes 3 \
  --probing-nodes 1 \
  --dht-nodes 1 \
  --enable-simplex \
  --simplex-slots-per-leader-window 10 \
  --simplex-first-block-timeout-ms 200 \
  --simplex-target-block-rate-ms 300 \
  --probing-env TON_PROBING_REORDER_SKIP_CERTS=1 \
  --probing-env TON_PROBING_WITHHOLD_PROPOSALS=1 \
  --probing-env TON_PROBING_WITHHOLD_START=3 \
  --probing-env TON_PROBING_WITHHOLD_END=7 \
  --mc-seqno 300 \
  --require-node-alive node4
```

If you were testing for a crash instead of a liveness negative result, add explicit stop conditions such as:

```bash
  --success-log 'any:Signal: 6' \
  --require-node-alive node4
```

Use `--require-node-dead nodeX` only when the victim is known in advance.

## Evidence Collected

- probing-node logs confirmed the reordering and withholding markers fired
- honest-node logs showed the network continued to process blocks
- the mixed run reached masterchain seqno `300`
- the probing node stayed alive long enough to make the result meaningful

This combination is a valid negative result.

## What Made The Result Valid

- the trigger path was real, not hypothetical
- the probing node did not die first
- the success condition was chosen before the run
- the absence of a crash or stall was observed over a meaningful interval

## Common Failure Modes In This Pattern

- probing markers missing:
  env vars did not reach the node or the patch never executed

- probing node dies first:
  invalid run; fix self-immunity

- relying only on `mc_seqno` for a crash claim:
  insufficient; pair it with explicit log or process conditions

For a broader list of patch shapes, read `probing_patterns.md`.

For post-run triage, read `diagnostic_checklist.md`.
