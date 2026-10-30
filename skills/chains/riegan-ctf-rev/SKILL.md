---
name: ctf-rev
description: Use when the user says reverse engineering, decompile, crackme, keygen, find the key/password/serial, obfuscated binary, packed binary, stripped binary, custom VM, bytecode, "what does this binary do", .jar/.apk/.NET/PyInstaller/unpack me, anti-debug, or hands over a binary with no remote service and asks for the flag. Static and dynamic RE: triage the binary, pick the language/packing path, decompile with Ghidra, defeat anti-debug, emulate custom VMs.
---

# ctf-rev — reverse engineering

Sibling skills: `ctf` (workspace, flags, submission), `ctf-pwn` (exploitation once
you understand the binary). This skill owns understanding the binary.

Untrusted artifact rule (from router, always in force): analyze statically first;
execute challenge binaries only under `podman` or with explicit user approval.

## Triage (first 5 minutes)

```bash
cd work/<event>/rev-<name>
scripts/ctf python  # venv ready
bash ../../../../skills/ctf-rev/scripts/strings-plus.sh dist/binary | tee triage.txt
file dist/binary
```

Decision table — pick the row, read the matching reference:

| Signal | Likely path | Reference |
|---|---|---|
| `UPX!` in strings / high entropy + few strings | `upx -d`, then re-triage | `references/workflow.md` |
| High entropy, no UPX magic, section names like `UPX0`/random | custom packer → run to OEP, dump | `references/antidebug.md` |
| Go build ID / `go:buildid`, `runtime.main` | Go symbol recovery | `references/languages.md` |
| Rust panic strings (`src/main.rs`, `core::panicking`) | Rust: panic strings reveal logic | `references/languages.md` |
| `.jar` / `META-INF/MANIFEST.MF` | jadx | `references/languages.md` |
| `.dll`/`.exe` + `mscoree`/`_CorExeMain` | .NET → ilspycmd | `references/languages.md` |
| `python3x.dll`, `MEI` prefix | PyInstaller → pyinstxtractor-ng | `references/languages.md` |
| `META-INF/`, `asar`, `pkg` prelude | Electron/Node unpack | `references/languages.md` |
| ELF, stripped, static-looking, big switch on data | custom VM | `references/custom-vm.md` |
| Binary crashes/exits under gdb but runs standalone | anti-debug | `references/antidebug.md` |
| Nothing exotic, plain C ELF | static→dynamic loop | `references/workflow.md` |

Key early questions (answer all before deep diving):
1. Architecture + static/dynamic + stripped? (`readelf -h`, `file`)
2. Imports: libc-only C, C++ (`_Z` symbols, STL), Rust, Go, other?
3. Entropy per section (packed?) — `scripts/strings-plus.sh` reports it.
4. Is there a remote service attached? If yes, after understanding → `ctf-pwn`.

## Playbook

The core loop (full detail in `references/workflow.md`):

```
static pass     strings → xrefs → decompile (Ghidra) → annotate interesting funcs
dynamic pass    run under strace/ltrace/gdb (podman if untrusted), break on the
                funcs found statically, watch data flow, patch branches in gdb
loop            each dynamic observation refines the static model
```

| Attack | Preconditions | Command | Reference |
|---|---|---|---|
| Full triage bundle | ELF/PE file | `skills/ctf-rev/scripts/strings-plus.sh <bin>` | `references/workflow.md` |
| Decompile everything | Ghidra installed | `GHIDRA_INSTALL_DIR=... scripts/ghidra-decompile.sh <bin>` | `references/ghidra.md` |
| Interactive RE | Ghidra GUI | `ghidraRun` → CodeBrowser | `references/ghidra.md` |
| Find main (stripped) | gdb | `gdb -q ./bin` → `starti` → walk to `main` | `references/workflow.md` |
| Trace syscalls/libs | strace/ltrace installed | `strace -f -e trace=openat,read,write ./bin` | `references/workflow.md` |
| Bypass a check live | know the branch | gdb: `set $pc` / `jump`, patch memory | `references/workflow.md` |
| Unpack UPX | upx installed | `upx -d bin -o bin.unpacked` | `references/languages.md` |
| Defeat anti-debug | detected the check | see table in antidebug.md | `references/antidebug.md` |
| De-flatten obfuscation | angr installed | symbolic exec around the flattening dispatcher | `references/antidebug.md` |
| Emulate foreign arch | qemu-user installed | `qemu-x86_64 -g 1234 ./bin` + gdb remote | `references/antidebug.md` |
| Reverse custom VM | found dispatch loop | map opcodes → write emulator | `references/custom-vm.md` |

When to give up on static and go dynamic (heuristics):
- Decompiled output is >60% nonsense or huge flattening switch → dynamic first.
- Packed/self-modifying: static is meaningless until you dump post-decode memory.
- You've annotated >10 functions without finding the check → ltrace/gdb the
  string compare / read path directly.
- The binary phones home or requires env/files → strace shows what it wants.

Found the flag format string or check? Follow router `ctf` for flag logging;
found a memory-safety bug you must exploit? Switch to `ctf-pwn`.

## References

- `references/workflow.md` — the static→dynamic loop: triage signals, finding
  main in stripped ELFs, decompile-first method, note-taking, gdb patching.
- `references/ghidra.md` — install, GUI + headless workflow, the
  decompile-everything recipe, structures, version tracking.
- `references/languages.md` — per-language recovery table: C/C++/Rust/Go/.NET/
  Java/Python/Node/UPX/misc runtimes.
- `references/antidebug.md` — ptrace/timing/int3 checks, packers, control-flow
  flattening, qemu-user emulation, unicorn for custom VMs.
- `references/custom-vm.md` — bytecode dispatch recognition, opcode mapping,
  Python emulator skeleton, encodings.

## Toolbox

| Tool | Install | Purpose |
|---|---|---|
| `gdb` | preinstalled | dynamic analysis, breakpoints, `dump binary memory` |
| `strace` / `ltrace` | `sudo pacman -S strace ltrace` | syscall / library-call tracing |
| `ghidra` | `sudo pacman -S ghidra` (JDK 21 already present) | decompiler, GUI + headless |
| `radare2` (optional) | `sudo pacman -S radare2` | quick CLI RE, `aaa; pdf`, no project setup |
| `jadx` | upstream release tarball → `~/.local/bin` | Java/Android decompile |
| `upx` | `sudo pacman -S upx` | unpack UPX binaries |
| `qemu-user` | `sudo pacman -S qemu-user` | run/emulate foreign-arch binaries |
| `python-angr` (optional) | `sudo pacman -S python-angr` or `uv pip install --python .venv/bin/python angr` | symbolic execution, deflattening |
| `ilspycmd` | `dotnet tool install -g ilspycmd` | .NET decompiler |
| `pyinstxtractor-ng`, `pycdc` | `uv pip install --python .venv/bin/python pyinstxtractor-ng`; pycdc from source | PyInstaller unpack + pyc decompile |
| `scripts/strings-plus.sh` | included | triage bundle (strings, ldd, readelf, entropy) |
| `scripts/ghidra-decompile.sh` + `scripts/ghidra_dump.py` | included, needs Ghidra | headless decompile-to-C dump |
