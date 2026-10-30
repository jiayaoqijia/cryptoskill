# RE workflow — the static → dynamic loop

Core idea: static analysis builds a model, dynamic analysis tests it. Never do
only one. Crackmes almost always reduce to "find the function that validates
input, understand the transform, invert or bypass it."

## 1. Static first pass (never execute yet)

```bash
file binary                        # arch, static/dynamic, stripped
readelf -h binary                  # entry point, machine, type
readelf -d binary | head -30       # interpreter, needed libs, RELRO bits
ldd binary                         # (careful: runs the loader) prefer readelf -d for untrusted
strings -n 6 binary | less         # messages, formats, paths, wrong/right hints
strings -n 6 binary | grep -aiE 'flag|key|passw|correct|wrong|win|denied'
readelf -s binary | less           # symbols: stripped? dynsym still has imports
objdump -d -M intel binary | less  # disassembly when Ghidra is overkill
```

Or run the bundle: `skills/ctf-rev/scripts/strings-plus.sh binary`.

### Packed detection

- Entropy > 7.0 per section (bundle reports it) + almost no strings → packed.
- `strings binary | grep -a UPX` → `upx -d` (see `references/languages.md`).
- Section names `UPX0/UPX1/UPX2`, or nonsense names, tiny `ep` section → packer.
- Entry point in a late section, rest high-entropy → custom packer →
  `references/antidebug.md` (run to OEP, dump, rebuild).

### Symbols vs stripped — what imports tell you

| Import/symbol pattern | Language | Notes |
|---|---|---|
| `printf`, `malloc`, `strcmp`, libc only | C | easiest path |
| `__libc_start_main` absent, `_start` odd | static or raw asm | check `readelf -h` type + size |
| `_Z...` mangled symbols, `_Unwind_`, `operator new` | C++ | demangle: `c++filt _ZN...`; vtables/RTTI below |
| `rust_begin_unwind`, `_ZN4core9panicking...`, panic strings with `src/main.rs:LINE` | Rust | panic locations are free debug info |
| `runtime.main`, `main.main`, `go:buildid`, pclntab header bytes | Go | symbols recoverable even "stripped" |
| `__cxa_atexit`, `_initterm` | C++ static init | global ctors run before main |

### Finding main in a stripped ELF

Non-PIE/PIE both: in the disassembly of `_start` (at the entry point from
`readelf -h`), glibc's `_start` loads `main` into `rdi` and calls
`__libc_start_main` (directly or via PLT). The pattern:

```
mov  rdi, <addr of main>      ; lea rdi, [rip+off] for PIE
call __libc_start_main@plt
```

That `<addr>` is `main`. Works even fully stripped — `_start` is never stripped
because the loader needs the entry point.

Dynamic alternative with gdb:

```
gdb -q ./binary
starti                    # stop at real entry (ld.so), before main
info proc mappings        # where things landed
# set a breakpoint on the address you computed from _start, or:
catch syscall write       # often the fastest way to find the output path
```

## 2. Decompile-first methodology

Read the decompilation, not the assembly, whenever you have a choice
(`references/ghidra.md`). Order of operations:

1. Open in Ghidra, let auto-analysis finish.
2. Window → Defined Strings → find "correct/wrong/flag" → double-click →
   in the decompiler, find the string's usage address, right-click the
   parameter → References → Show References to Address → jump to the
   cross-reference (xref) — that function is the validator.
3. Rename functions/variables as you understand them (`L` key). Ghidra
   annotates every xref, so names propagate understanding.
4. Note-taking on functions: keep a scratch file in the challenge dir:

```markdown
## FUN_00401370  →  check_license(char *input)
- reads 0x20 bytes from stdin
- xor with byte at 0xdeadb (key "sup3rs3cr3t")
- memcmp vs .rodata:0x402014 (len 0x20) — patch jne at 0x4013fa
```

   Record: address, guessed signature, what it touches, the patch point.
   These notes ARE the solve — the writeup writes itself from them.

5. Define types for structures you've reconstructed (Ghidra: File → Create
   Structure from selection / see `references/ghidra.md`); decompiled output
   improves dramatically once a struct is applied.

If the decompiler chokes (thunks, weird calling conventions), fall back to
`objdump -d -M intel --start-address=0x... --stop-address=0x...`.

## 3. Dynamic confirmation

Install once (document, don't auto-run): `sudo pacman -S strace ltrace`.

```bash
strace -f ./binary                       # what files/syscalls it touches
strace -f -e trace=openat,open,read,write ./binary
ltrace -f ./binary                       # library calls: strcmp, memcmp reveal the check
ltrace -i ./binary                       # + instruction pointer per call
```

`ltrace` on a static binary shows nothing — use gdb catchpoints instead.

gdb on interesting functions (found statically):

```
gdb -q ./binary
break *0x401370            # validator found via strings xref
run
x/s $rdi                  # SysV arg1, x/d $rdi for ints
x/32bx $rsi               # raw bytes of arg2
info registers rdi rsi rdx rcx r8 r9
```

Break on libc funcs that do the comparison: `break strcmp`, `break memcmp`,
`break strncmp` — at hit, `x/s $rdi` and `x/s $rsi` show both sides. For
static binaries use `catch syscall` or break on the address from the
decompilation.

### Patching branches in gdb before binary patching

Always verify in the debugger first — a wrong binary patch costs a rebuild and
a re-triage:

```
# at the conditional jump, e.g. 0x4013fa:  jne 0x401420
# option A: flip flags outcome by skipping the jump
set $pc = 0x401420          # jump taken, unconditionally
# option B: neuter the jump in memory only
set {char}0x4013fa = 0x90  # NOP the jne (then restore: set to 0x75)
# option C: force a register/value used in the compare
set $rax = 1
continue
```

Only patch the file on disk (`seek` the byte with a python one-liner or
`xxd`) after gdb proves the branch flip produces the win path.

### Dynamic for untrusted binaries

Run under isolation per the router rule:

```bash
podman run --rm -it -v "$PWD:/chal:Z" --network none archlinux bash
# inside: copy of binary + gdb/strace (install inside container)
```

## 4. Loop and escalation

- Each dynamic run answers one hypothesis from notes.md. Update, repeat.
- Stuck >30 min statically → go dynamic; stuck dynamically → decompile the
  exact address that misbehaved.
- Obfuscated/flattened/anti-debug → `references/antidebug.md`.
- Custom VM dispatch found → `references/custom-vm.md`.
- Memory-corruption angle (validator is `strcpy`-ish, remote service) →
  `ctf-pwn`.
