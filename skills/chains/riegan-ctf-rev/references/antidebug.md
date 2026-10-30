# Anti-debug, anti-vm, packers, obfuscation, emulation

Symptom: binary works standalone but exits/crashes/behaves wrong under gdb or
strace. Or: decompilation is unreadable garbage. Both are defeated, not feared.

## Detect the check first

Under gdb, the usual suspects are visible statically — grep the decompile for:
`ptrace`, `/proc/self/status`, `TracerPid`, `rdtsc`, `0xcc`, `SIGTRAP`,
`ptrace(PTRACE_TRACEME)` self-attach.

| Check | How it works | Defeat |
|---|---|---|
| `ptrace(PTRACE_TRACEME)` self-attach | returns -1/EAGAIN if already traced (i.e., by your gdb); process exits or takes false path | gdb: `catch syscall ptrace` → `set $rax = 0` at return; or patch the `test`/`cmp` after the call; or `set follow-fork-mode`/run under a tracer that hides (catchpoint + reg patch is fastest) |
| `TracerPid` scan | reads `/proc/self/status`, parses `TracerPid:` != 0 | gdb: `catch syscall openat` → when path ends in status, redirect/patch result; simplest: patch the comparison |
| `rdtsc` timing | reads timestamp counter twice around a loop; huge delta = single-stepped/breakpoint hit | patch the delta compare; or in gdb, `set $rax = small` after second rdtsc |
| `int3` scan | scans own .text for 0xCC bytes (software breakpoints!) | use hardware breakpoints in gdb: `hbreak *addr` — places no 0xCC |
| SIGTRAP handler trick | installs SIGTRAP handler, executes `int3`; if handler runs, not traced (gdb intercepts first) | `handle SIGTRAP nostop noprint pass` in gdb, or patch out |
| anti-vm strings | `vmware`, `VBox`, `qemu`, `xen`, `cpuid` leaf 0x40000000 | usually patchable compares; on host we are bare-metal anyway — only matters if challenge expects vm |
| parent/argv checks | `getppid`, `/proc/self/cmdline` for `gdb`/`ltrace` | run under a wrapper that execs it ( argv[0] trick ), or patch |

Order of operations: always `catch syscall ptrace` FIRST on a suspicious
binary — cheapest confirmation.

## Opaque predicates and control-flow flattening

- Opaque predicate: a branch that always goes one way but looks data-dependent
  (`x*x < 0` etc.). Recognize in decompiler: compares of obviously-bounded
  values; NOP or force-register them away.
- Control-flow flattening (OLLVM/ Tigress ): one giant `while(1) switch(state)`
  dispatcher; real basic blocks are cases; `state` variable drives order.
  Decompiler output is a huge switch — unusable directly.
- Deflattening: symbolic execution recovers the state machine. With angr:

```bash
sudo pacman -S python-angr     # or: uv pip install --python .venv/bin/python angr
```

  Sketch: load with angr, hook the dispatcher loop head, symbolically explore
  from entry with the state var concrete-ized per iteration, record the real
  successor chain, emit an unfattened trace. For CTF scale it is usually
  enough to symbolically execute from just before the check with input
  unconstrained and add a success-state constraint (standard angr
  `find`/`avoid` on the win/lose addresses from Ghidra):

```python
import angr
p = angr.Project("binary", auto_load_libs=False)
s = p.factory.entry_state()
sm = p.factory.simgr(s)
sm.explore(find=0x4018f2, avoid=0x401901)   # win, lose addrs from Ghidra
if sm.found:
    print(sm.found[0].posix.dumps(0))       # stdin that wins
```

## Self-modifying code

Code decrypts itself (or its data) at runtime. Static disassembly of the
encoded region is garbage by design.

Method: run to the point AFTER decode, dump memory, analyze the dump.

```
gdb -q ./binary
starti
break *0x4015a0          # address after the decode routine finishes (from Ghidra)
continue
dump binary memory dump.bin 0x401000 0x402000   # the decoded region
# then open dump.bin at the right base in Ghidra (Import File → language,
# set base via Memory map add block at 0x401000)
```

For a full-process dump: `gcore <pid>` or `dump binary memory` over
`info proc mappings` ranges.

## Packers — run to OEP, dump, rebuild

When `upx -d` doesn't apply (custom packer):

1. Static: entry point sits in the packer stub section.
2. Dynamic: break at the moment the stub jumps to the original entry point
   (OEP). Tactics: hardware-breakpoint on the first executed byte of a
   pristine section; break on `mprotect`/` VirtualProtect ` return (the stub
   makes .text writable/executable right before jumping); `catch syscall`
   on the last mmap/mprotect before transfer.
3. Dump the process (`gcore`, or `dump binary memory`).
4. Rebuilding a runnable ELF from the dump: reconstruct section headers and,
   the hard part, the import table (IAT) the packer destroyed. Scylla-style
   tools do this on Windows; on Linux there is no turnkey equivalent.
5. Therefore: PREFER not rebuilding — analyze the dump statically in Ghidra
   (fine without imports) and confirm dynamically in the still-packed
   process under gdb. Reserve full rebuild for when you must re-run the
   unpacked binary.

## Emulation

- Other-arch binaries on this x86_64 host:

```bash
sudo pacman -S qemu-user
qemu-aarch64 -L /usr/aarch64-linux-gnu ./challenge
qemu-arm -g 1234 ./challenge    # gdb remote stub
# another terminal: gdb -q -ex 'set architecture arm' -ex 'target remote :1234' ./challenge
```

- Custom VM challenges (chip8/elf-cpu style): Unicorn engine for scripting
  the challenge CPU itself — see `references/custom-vm.md`.
- Emulating a single x86 function without running the process: qiling or
  unicorn (`uv pip install --python .venv/bin/python unicorn qiling`); map
  the binary, set up a stack, start EIP at the function, feed args in regs.

Untrusted-artifact rule applies doubly to emulated/run challenge code:
`podman run --rm -it -v "$PWD:/chal:Z" --network none` and execute inside.
