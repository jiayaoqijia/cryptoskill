---
name: ctf-re-bridge
description: Hands-on binary reversing loop for CTF executables and firmware. Use when you have a binary (ELF, Mach-O, PE, firmware blob, APK native lib) and need triage, function listing, decompilation, patching, or custom-VM emulation — via the r2 MCP server, Ghidra headless, and the LIEF/capstone/keystone/unicorn Python kit in ctf-solver/.venv. Pairs with ctf-reverse (technique catalog).
license: MIT
compatibility: Requires radare2 6.x with r2mcp built from source (this machine: Xcode toolchain clang + MacOSX SDK sysroot, see §6), Ghidra 12.1.4 + GhidraMCP 2.0 for headless decompile, and ctf-solver/.venv with lief/capstone/keystone/unicorn.
allowed-tools: Bash Read Write Edit Glob Grep Task WebFetch WebSearch Skill
metadata:
  user-invocable: "true"
  argument-hint: "[binary path | firmware image]"
---

# CTF RE Bridge — binary to decompilation loop

r2 answers "what is this" in seconds. Ghidra answers "what does it do" in minutes. Python answers "now run it my way". Use all three, in that order. Do not start Ghidra before r2 triage tells you the binary is worth it.

## 0. Environment (this machine's facts)

- `r2` / `r2pm`: `/opt/homebrew/bin` (radare2 6.2.6). r2mcp binary: `~/.local/share/radare2/prefix/bin/r2mcp`, invoked as `r2pm -r r2mcp` (default mode, ~32 tools). NOTE: `-R`/`-m` modes drop `open_file`/`analyze` — useless for real work. Default mode is safe enough: dangerous `run_*` tools need `-r`, permissive mode needs `-p`; neither is enabled.
- Compiler shims (`cc/gcc/make` in /usr/bin) are broken Xcode stubs — no Command Line Tools. If you must compile C: toolchain clang at `/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang` with `--sysroot=<MacOSX.sdk>`, `make` from `brew install make` (gnubin on PATH), `git` from `/opt/homebrew/bin`. Rebuilding r2mcp needs all three (see build log in the phase-2 notes).
- MCP entry `r2` in `.agents/mcp.json` sets PATH so the server finds `r2mcp`.
- Ghidra: `/opt/homebrew/share/ghidra_12.1.4_PUBLIC` (`GHIDRA_INSTALL_DIR`), GhidraMCP 2.0 extension installed, decompiler natives built via `./support/gradle/gradlew buildNatives` with `JAVA_HOME=/opt/homebrew/opt/openjdk@21`. GhidraMCP is pinned to Ghidra **12.1.4** — do not "upgrade" Ghidra without checking the extension release first.
- Python kit: `ctf-solver/.venv/bin/python` has `lief`, `capstone`, `keystone` (needs brew `keystone` dylib + `setuptools` for distutils), `unicorn`. Verify: `python -c "import lief,capstone,keystone,unicorn"`.

## 1. Triage (r2, < 60 seconds)

```
open_file <abs path>  ->  analyze  ->  show_info
```

Read `show_info` first: arch/bits/endian, format, stripped?, packed?, canary/NX/PIE. Then in parallel: `list_strings` (regex `flag|key|pass|secret|http`), `list_imports` (`ptrace`, `syscall`, `mmap`, crypto imports = anti-debug/VM/custom-crypto smells), `list_entrypoints`, `list_functions {"count": true}`.

Decision:
- < 50 functions, unstripped C → stay in r2, decompile each interesting function.
- C++ / Objective-C / Rust / Go, or > 200 functions → Ghidra (§3).
- Entropy high + tiny import table + UPX/MEzzo strings → packer: `unblob` the outer layer or find the unpacking stub first; do not waste Ghidra time on packed code.
- Firmware/blob (no headers) → `unblob` carve first, then loop per extracted ELF.

## 2. r2 deep loop

`list_functions` (paginate: `max_length` 50) → `decompile_function` (pdc, address as `0x...`) → `disassemble_function` when pdc output is unclear → `xrefs_to` on interesting constants → `lookup_address` on mystery pointers. Rename globals as you learn them (`rename_function` is available in default mode — use it; names compound across turns).

Custom crypto / encoding: lift the transform into Python with capstone (`Cs(CS_ARCH_X86, CS_MODE_64)`) to confirm semantics, then reimplement decrypt in pure Python. Never hand-simulate more than ~20 instructions.

## 3. Ghidra headless (when r2 is not enough)

```
GHIDRA_INSTALL_DIR=/opt/homebrew/share/ghidra_12.1.4_PUBLIC \
uvx --python 3.13 --from "ghidra-mcp[headless] @ git+https://github.com/LaurieWired/GhidraMCP" \
  ghidra-mcp --headless --binary /abs/path/to/binary --project /tmp/ghidra-proj
```

Use for: virtual-function-heavy C++, exception-flow, structure recovery, type propagation. `--project DIR` persists renames between runs. If it errors about the decompiler binary, natives were not built — rerun `buildNatives` (§0).

GUI fallback: only if headless blocks on something exotic. GUI kills agent autonomy — prefer to extract and emulate instead (§4).

## 4. Emulation & patching (the hard-binary toolkit)

- **Custom VM / bytecode**: map sections with LIEF, emulate the handler loop in unicorn, dump the trace. This is the highest-yield hard-RE pattern in this workspace.
- **Assemble patches / shellcode**: keystone (`Ks(KS_ARCH_X86, KS_MODE_64).asm(b"...")`) — verified working, e.g. `mov rax,0x4141` → `48c7c041410000`.
- **Parse/patch headers**: LIEF (`lief.parse`), rebuild and test. Keep the original (`cp binary binary.orig`) — every patch gets a diff check (`r2 -Q -c 'pv' ...` or sha256 before/after).

## 5. Failure branches

- **r2mcp won't start / `r2mcp: command not found`**: `r2pm -l | grep r2mcp` empty → rebuild per §0 toolchain notes; non-empty but not on PATH → check `R2PM_BINDIR` (`~/.local/share/radare2/prefix/bin`) is installed via `make user-install`.
- **Stripped + no strings**: `list_all_strings` (whole-binary scan) → `search` for magic constants → entrypoint-first analysis (`list_entrypoints`, decompile from there).
- **Anti-debug (`ptrace`, `is_debugger`)**: patch the check in a COPY (LIEF or r2 `w` in a scratch copy — never the evidence original), or emulate the guarded region in unicorn.
- **Go/Rust binaries**: function count explodes — filter `list_functions {"filter": "main\\."}` and read from `main.main`.
- **APK native libs**: extract `.so` from the APK (unzip), treat as ELF; Java/Kotlin layer needs jadx (not installed — Phase 2 covers native only, say so and stop).

## Verify the stack

```bash
r2 -v && r2pm -r r2mcp -t | wc -l
./ctf-solver/.venv/bin/python -c "import lief,capstone,keystone,unicorn; print('pykit ok')"
ls /opt/homebrew/share/ghidra_12.1.4_PUBLIC/Ghidra/Features/Decompiler/os/  # want mac_* dir
```
