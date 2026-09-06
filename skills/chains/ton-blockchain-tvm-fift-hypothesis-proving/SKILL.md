---
name: tvm-fift-hypothesis-proving
description: Prove or reject TON TVM opcode, crash, gas-accounting, memory, CPU, debug, and RUNVM/RUNVMX resource hypotheses with Fift/Asm.fif probes. Use when testing suspected TVM instruction underpricing, native crashes, exponential resource growth, or runvm behavior in a local TON checkout.
---

# TVM Fift Hypothesis Proving

Use this skill when the job is to turn a suspected TVM resource, crash, or gas-accounting issue into a minimal executable Fift probe and classify the result.

Typical triggers:

- "this opcode crashes TVM"
- "this opcode allocates memory without gas"
- "this instruction is exponential"
- "this gas charge is too low"
- "`RUNVM` or `RUNVMX` can reset accounting"
- "debug output, stack dumps, or Fift tooling can be abused"

If the hypothesis needs validator networking, block production, account state, or transaction replay, use a local-network triage skill instead or combine both workflows.

## Entry Model

Fift is a stack language. Values are pushed first, words consume values from the top of the stack, and `.s` prints the current Fift stack. The top of the printed stack is the last item.

TVM assembler syntax is also stack-shaped:

- Start assembler probes with `"Asm.fif" include`.
- Put TVM code inside `<{ ... }>s` when you want a code slice suitable for `runvmcode` or `gasrunvmcode`.
- Arguments already on the Fift stack become the initial TVM stack.
- `gasrunvmcode` takes a code slice and a gas limit, then returns TVM result values, the exit code, and gas consumed.

Useful public references:

- Fift introduction: https://ton.org/fiftbase.pdf
- TVM description: https://ton.org/tvm.pdf
- In the TON repo, inspect `doc/fiftbase.tex`, `crypto/fift/lib/Fift.fif`, `crypto/fift/lib/Asm.fif`, `crypto/fift/words.cpp`, `crypto/vm/contops.cpp`, and the opcode implementation under `crypto/vm/`.

## Quick Start

Create `probe.fif` in a TON checkout:

```fift
"Asm.fif" include

2 3 <{ ADD DUP MUL }>s 1000000 gasrunvmcode .s cr
```

Run it:

```bash
build/crypto/fift -Icrypto/fift/lib -s probe.fif
```

The TVM program is three opcodes:

1. `ADD` turns `2 3` into `5`.
2. `DUP` duplicates `5`.
3. `MUL` returns `25`.

The stack line has this shape:

```text
25 0 <gas>
```

`25` is the TVM result, `0` is the TVM exit code, and `<gas>` is the gas consumed by this build and global version. With a too-small gas limit, expect an out-of-gas exit such as:

```text
<exception-parameter> -14 <gas>
```

Do not hard-code one gas number across versions. Record the build, global version, exact probe, exit code, and measured gas.

## Workflow

1. Ground the hypothesis in current code.
   Locate the assembler mnemonic and C++ executor with `rg`.
   Identify where gas is charged, where cells or stack entries are allocated, whether the operation is version-gated, and whether the surface is consensus execution, get-method/liteserver, Fift tooling, debug-only code, or host-library code outside TVM.

2. Build the smallest executable probe.
   Start with one opcode or a tiny opcode sequence.
   Keep the first run small enough to finish quickly.
   Scale one parameter at a time.
   Prefer `gasrunvmcode` or explicit `runvmx` modes when the returned gas matters.

3. Measure host resources separately from TVM gas.
   Use `/usr/bin/time -v` for RSS and CPU.
   Use `timeout` for suspected hangs.
   Redirect huge debug output to a file or `/dev/null`.
   Record stack output, exit code, gas, max RSS, user/system time, elapsed time, and the scale parameter.

4. Compare against a charged baseline.
   For cells, compare `BTOS` or `HASHBU` paths against `ENDC`, `ENDC CTOS`, or `ENDC HASHCU`.
   For debug/output claims, compare gas at construction time against host output bytes or RSS.
   For `RUNVM`, distinguish a stack supplied by Fift from a stack built inside TVM and paid by TVM gas.

5. Classify the result.
   Confirm only when a bounded PoC demonstrates a production-reachable path where TVM gas stays flat or much lower than host memory, CPU, output, or crypto work, and the code path explains why.
   Downrank findings that require Fift debug flags, `DUMP*`, stack trace, `.s`, `.dump`, or `(dump)` unless a production host enables the same sink on untrusted contract output.
   Reject hypotheses with durable negative facts: bounded tuple length, bounded dictionary key depth, memoized cell DAG traversal, explicit linear gas, paid stack movement, or version-gated historical fixes.

6. Preserve reusable conclusions in the requested public artifact.
   Keep private provenance, local report filenames, absolute local paths, and raw huge outputs out of public skill content and public reports.
   Write down exact rejection reasons so future triage can skip known false positives quickly.

## Command Patterns

Run a one-off probe:

```bash
build/crypto/fift -Icrypto/fift/lib -s probe.fif
```

Measure RSS and CPU:

```bash
/usr/bin/time -v build/crypto/fift -Icrypto/fift/lib -s probe.fif >/tmp/probe.out 2>/tmp/probe.time
```

Bound a suspected hang or crash:

```bash
timeout 10s /usr/bin/time -v build/crypto/fift -Icrypto/fift/lib -s probe.fif >/tmp/probe.out 2>/tmp/probe.time
echo "status=$?"
```

Scale a parameter cautiously:

```bash
for n in 8 12 16 20; do
  sed "s/@N@/$n/" probe.template.fif >/tmp/probe.fif
  /usr/bin/time -f "N=$n rss_kb=%M user_s=%U sys_s=%S elapsed_s=%e" \
    build/crypto/fift -Icrypto/fift/lib -s /tmp/probe.fif >/tmp/probe.$n.out
done
```

When defining Fift macros that emit assembler bytes, raw bytes are often safer than calling assembler words outside assembler context:

```fift
x{D8} s,     // EXECUTE
x{5C} s,     // 2DUP
x{ECFF} s,   // SETCONTARGS 15,-1
```

## Fift runvm Words

The Fift host word `runvmx` pops a mode from the Fift stack. `crypto/fift/lib/Fift.fif` defines convenient wrappers:

- `runvmcode`, `gasrunvmcode`, `gas2runvmcode`
  Run a code slice. `gas*` variants take a gas limit and return gas consumed.
  `gas2*` variants also pop a hard gas limit.

- `runvmdict`, `gasrunvmdict`, `gas2runvmdict`
  Run with `c3` initialized from the code and an implicit zero argument.

- `runvm`, `gasrunvm`, `gas2runvm`
  Run with `c3` initialized from the code and `c4` persistent data loaded from the stack and returned.

- `runvmctx`, `gasrunvmctx`, `gas2runvmctx`
  Also load `c7` smart-contract context.

- `runvmctxact`, `gasrunvmctxact`, `gas2runvmctxact`
  Also return `c5` actions.

- `runvmctxactq`, `gasrunvmctxactq`
  Quiet context/action variants that avoid the default operation log bit used by the non-quiet wrappers.

Fift `runvmx` mode bits in `crypto/fift/words.cpp` are:

```text
+1    set c3 to code
+2    push implicit 0 before running code
+4    load c4 from stack and return final c4
+8    load gas limit from stack and return consumed gas
+16   load c7 from stack
+32   return c5 actions
+64   log VM ops to stderr
+128  pop hard gas limit from stack
+256  enable stack trace
+512  enable debug instructions
+1024 load global_version from stack
```

For explicit mode use, a gas-returning code-only run is:

```fift
2 3 <{ ADD }>s 1000000 0x48 runvmx .s cr
```

The TVM opcodes `RUNVM` and `RUNVMX` are different from the Fift host word `runvmx`. Their mode bits live in `crypto/vm/contops.cpp`:

```text
+1    set c3 to code
+2    push implicit 0; only works with +1
+4    load c4 from stack and return final c4
+8    load gas limit from stack and return consumed gas
+16   load c7 from stack
+32   return c5 actions
+64   pop hard gas limit from stack
+128  isolated gas consumption: separate visited cells and reset cheap counters
+256  pop N and return exactly N values on success
```

Do not mix these two mode tables. Fift `+256` means stack trace; TVM `RUNVM` `+256` means exact return count.

## Crash Hypotheses

Treat a crash as a native process failure, such as SIGSEGV, SIGABRT, failed `CHECK`, or another unhandled host failure. A TVM exception, an out-of-gas result, an invalid-opcode result, or a Fift `abort"` is not a crash.

Crash triage steps:

1. Run the smallest probe without Fift stack trace, debug instructions, post-run `.s` dumps of huge values, or verbose VM logs.
2. Bound the run with `timeout`.
3. Capture exit status and stderr. Typical shell statuses are `124` for timeout, `134` for abort, and `139` for segfault.
4. If the process really crashes, rerun under a debugger or sanitizer build only after the minimal non-debug PoC is stable.
5. Classify as tooling-only if the crash requires Fift display, dump, trace, or debug-only paths instead of ordinary TVM execution.

Useful rejection: "the program returned exit code `-14`" means out of gas, not native crash.

## Exponential Resource Hypotheses

A real exponential finding needs both measurements and code support. Do not infer exponential behavior from one slow run.

Measure at least four scale points. Keep all other variables fixed and record:

```text
N gas max_rss_kb user_s sys_s elapsed_s exit_code output_bytes
```

Confirm only if resource growth substantially outpaces gas and the implementation lacks a cap or memoization. Common caps and guards:

- TVM cells are limited to 1023 bits and 4 refs.
- Dictionary keys are capped at `DictionaryBase::max_key_bits = 1023`; most dictionary opcodes follow one key path, not the whole tree.
- `CDATASIZE*` and `SDATASIZE*` use visited-cell accounting, so shared DAGs are counted physically, not logically, when the code path uses that storage-stat walker.
- Tuples are bounded by length 255; tuple operations charge tuple gas and become interesting mainly when fed into recursive display, serialization, or debug sinks.
- Stack movement and continuation calls commonly charge for stack depth beyond the free depth.

A host-only exponential sink can still matter for tools, liteservers, or indexers, but do not describe it as consensus TVM gas abuse unless ordinary contract execution reaches it.

## Incorrect Gas Hypotheses

## Common False Positives

`BTOS` is cheap by design. In current code it pops a builder, finalizes it with `finalize_novm()`, and returns a slice view with `NoVm()`. It does not run the normal `ENDC` cell-create accounting. The important bounds are that a builder is one TVM cell, so it is capped at 1023 bits and 4 refs, and repeated use still pays the opcodes needed to build, keep, move, hash, serialize, or commit values. A report that only says "`BTOS` is cheaper than `ENDC CTOS`" is not enough. Look for unbounded transient memory growth per gas unit on a production path.

The first 10 Ed25519 `CHKSIGNU` or `CHKSIGNS` calls are intentionally cheap. `register_chksgn_call()` tracks a per-VM counter, records the first 10 as free gas, and charges `chksgn_gas_price` after that. This is not by itself a bug.

`RUNVM` does not let a contract multiply the first-10-CHKSGN allowance for free. By default, child VMs inherit and return the parent's `chksgn_counter` and `free_gas_consumed`. With TVM `RUNVM` mode `+128`, the child uses isolated gas and resets cheap counters, but the parent first consumes accumulated free gas before resetting. A valid bypass must demonstrate more than the intended allowance in one production execution without that accounting catching up.

Fift debug and dump paths are usually not consensus issues. Findings that require Fift `runvmx` mode `+256`, mode `+512`, debug opcodes, stack trace, `.s`, `.dump`, `(dump)`, or large post-run display are tooling/debug findings unless a production service exposes the same sink to untrusted input.

Historical nested-continuation free-gas reports need a current-version bypass. Continuation nested-jump native recursion and free nested jump gas are historical for current `global_version >= 9`.

## Evidence Standard

A useful result includes:

- TON commit or build identity
- global version used
- exact Fift probe
- exact command
- stack output
- exit code
- gas consumed
- max RSS and CPU time when resource use is part of the claim
- scale table for non-constant hypotheses
- source lines for the charge, allocation, traversal, or reset behavior
- classification: confirmed, rejected, tooling-only, version-gated, or needs network-level repro
