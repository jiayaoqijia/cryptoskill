# Probing Patterns

Use this reference for `Workflow B — trigger via validator behavior`.

The rule for every probing patch is the same:

- gate it behind explicit `TON_PROBING_*` environment variables
- log a single-line marker when it fires
- make the probing node self-immune so the run is not invalidated by the probe crashing first

## Shared Pattern

Use this structure no matter which file you patch:

1. Read one or more `TON_PROBING_*` env vars at process startup or at the decision point.
2. Exit early unless the env var is explicitly enabled.
3. Log a stable marker that is easy to grep.
4. Skip or neutralize the mutation when the target is the probing node itself.

Self-immunity can be based on:

- local validator id
- local ADNL id
- local node role or index
- a target address or peer id from `TON_PROBING_TARGET_ADDR` or similar env vars

Do not hide the guard. Log when the guard causes the node to skip the mutation.

## Withhold Messages Or Proposals

Use this when you want to drop or suppress a message that would normally be sent.

Likely source files:

- `validator/consensus/block-producer.cpp`
- `validator/consensus/simplex/*.cpp`
- `validator/full-node*.cpp`

Useful env vars:

- `TON_PROBING_WITHHOLD_PROPOSALS=1`
- `TON_PROBING_WITHHOLD_START=<slot-offset>`
- `TON_PROBING_WITHHOLD_END=<slot-offset>`

Log shape:

- `TON_PROBING withholding proposal slot=<n> target=<peer> reason=<...>`

Self-immunity:

- do not withhold the messages that keep the probing node alive or synchronized
- if a slot range would starve the probing node first, skip the mutation and log that skip

## Send Malformed Data Or Packets

Use this when the bug depends on a malformed TL object, invalid BoC, corrupted proof, or broken serialization.

Likely source files:

- `validator/impl/*.cpp`
- `validator/full-node-*.cpp`
- `adnl/*.cpp`

Useful env vars:

- `TON_PROBING_SEND_BAD_PACKET=1`
- `TON_PROBING_BAD_PACKET_KIND=<name>`

Log shape:

- `TON_PROBING send bad packet kind=<name> peer=<peer>`

Self-immunity:

- never feed the malformed object back into the probing node’s own validation path
- if the same packet is reflected locally, short-circuit that reflection in probing mode

## Reorder Protocol Messages

Use this when the bug depends on out-of-order processing.

Likely source files:

- `validator/consensus/simplex/pool.cpp`
- `validator/consensus/simplex/consensus.cpp`
- queue or broadcast handlers near the message type you are targeting

Useful env vars:

- `TON_PROBING_REORDER_SKIP_CERTS=1`
- `TON_PROBING_REORDER_BUFFER=<count>`

Log shape:

- `TON_PROBING reorder <message-kind> buffered=<n> released=<n>`

Self-immunity:

- do not reorder the probing node’s own critical recovery or catch-up path
- if reordering would deadlock the probing node before the honest nodes see the mutation, skip it

## Delay Responses

Use this when the bug depends on timeouts, races, or delayed votes.

Likely source files:

- consensus handlers
- block download or catch-up paths
- message dispatch or retry logic

Useful env vars:

- `TON_PROBING_DELAY_MS=<milliseconds>`
- `TON_PROBING_DELAY_KIND=<message-kind>`

Log shape:

- `TON_PROBING delay kind=<message-kind> ms=<value>`

Self-immunity:

- do not delay the probing node’s own minimum liveness path
- if the delay would obviously kill the probing node first, clamp or skip it

## Produce Invalid Blocks Or Proofs

Use this when the goal is to test honest-node rejection or crash handling for invalid consensus artifacts.

Likely source files:

- `validator/consensus/block-producer.cpp`
- `validator/impl/block*.cpp`
- proof construction or acceptance paths

Useful env vars:

- `TON_PROBING_INVALID_BLOCK=1`
- `TON_PROBING_INVALID_FIELD=<name>`

Log shape:

- `TON_PROBING invalid block field=<name> block=<id>`

Self-immunity:

- do not let the probing node accept or execute the invalid artifact as if it were honest input
- keep the probing node alive long enough to see honest-node rejection, crash, or fork symptoms

## Recommended Run Conditions

When using `run_mixed_network.py`, pair the patch with explicit conditions:

- `--success-log` for the expected probing marker or honest-node effect
- `--failure-log` for invalid-run markers
- `--require-node-alive nodeN` for the probing node when self-immunity matters
- `--require-node-dead nodeN` only when the target effect is honest-node death and the victim is known

Use `scripts/summarize_run.py` after the run even if you already tailed logs manually.
