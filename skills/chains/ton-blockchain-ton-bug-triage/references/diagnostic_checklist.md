# Diagnostic Checklist

Use this reference when a run finished but the result is unclear.

Start by deciding which workflow you were actually exercising.

## Workflow A

- If any tonlib-based script crashes with `KeyError` or similar wrapper errors:
  do not debug the wrapper.
  Switch to `lite-client` for the rest of the session.
  Use `run_liteclient.py` or call `lite-client` directly.

- If `--auto-seqno` fails:
  use manual `--seqno`.
  For the built-in `main-wallet`, seqno starts at `0` and increments by `1` per send.

### Compile Step

- If `compile_tolk.py` fails with a stale-build error:
  rebuild `tolk` first and rerun the exact same command.

- If `compile_tolk.py` succeeds but no code BoC exists:
  inspect the generated `.fif` and rerun the helper before changing the contract source.

### Deploy Step

- If `wallet_send.py --init-boc` succeeded but the account still has empty code/data:
  check too-early observation first.
  Use `account_state.py` after another masterchain advance.

- If the address in `account_state.py` is not the address from `build_stateinit.py`:
  stop and fix the address mismatch before continuing.

### Activation Step

- If the account is active but the expected get-method fails:
  verify the method id and the initial data layout.

- If the contract needs data or libraries and you skipped them in `build_stateinit.py`:
  rebuild `StateInit` with `--data-boc` or `--library-boc`.

### Trigger Step

- If the trigger transaction never appears:
  verify the source wallet `seqno`, the destination address, and the trigger amount.

- If the latest transaction exists but the payload looks wrong:
  dump both:
  `dump_boc.py --boc <original-body.boc>`
  `dump_boc.py --boc <exported-in-msg-body.boc>`

- If `inspect_latest_transaction.py` exports `msg.dataText` instead of `msg.dataRaw`:
  tonlib decoded the payload as text.
  Use the JSON text fields instead of expecting `in-msg-body.boc`.

### Observation Step

- If `transaction-data.boc` dumps cleanly but nothing interesting happened:
  the trigger landed, but the bug did not reproduce.

- If the contract state changed unexpectedly:
  dump `account_state.py` code and data BoCs and compare them to the expected post-state.

## Workflow B

### Before The Effect

- If probing markers are missing entirely:
  the env vars did not reach the node or the patched code path never executed.

- If the probing node died before any honest-node effect:
  the run is invalid.
  Fix self-immunity before drawing conclusions.

### During The Effect

- If honest nodes stayed live and `mc_seqno` kept advancing:
  this is a negative result unless your success condition was something else.

- If a log marker fired but no observable effect followed:
  the patch executed, but it was not sufficient to trigger the bug.

- If an honest node died or stopped producing blocks:
  capture that node’s log, the probing-node marker log, and the `summarize_run.py` output before rerunning.

### After The Effect

- If `summarize_run.py` reports `running` for every validator and no crash markers:
  you do not have a crash repro yet.

- If you need block-level evidence:
  do not assume `lite-client` already exists in the build directory.
  Build it separately or use alternate tooling.

## Valid Negative Result

A negative result is valid when:

- the intended trigger path really executed
- the observation step looked at the correct artifacts
- the network remained healthy enough to make the absence meaningful
- a clean rerun reproduces the same absence

Report that result directly instead of continuing with random parameter churn.
