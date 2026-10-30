# Mitigations — reading checksec, choosing the attack surface

## 1. Get the facts

```bash
scripts/ctf pwn checksec ./dist/chal      # same: scripts/ctf checksec ./dist/chal
```

```
[*] './dist/chal'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
    Stripped: No
    FORTIFY:  Enabled           # only when __*_chk calls were compiled in
    RWX:      Has RWX segments  # only when a segment is rwx
```

No-pwntools fallback: `readelf -lW ./chal | grep -E 'GNU_RELRO|GNU_STACK'`
and `readelf -d ./chal | grep -E 'BIND_NOW|FLAGS'`.

## 2. Attack-surface matrix

| checksec line | Meaning | What it kills | First move |
|---|---|---|---|
| `NX: NX disabled` | stack/heap pages executable | nothing | inject shellcode, jump to it (`references/shellcode.md`) |
| `NX: NX enabled` | W^X (GNU_STACK rw-) | shellcode on stack/heap | ROP (`references/stack.md`) or ROP → mprotect → shellcode (`references/shellcode.md`) |
| `PIE: No PIE` | image base fixed (0x400000 amd64) | nothing | absolute addresses; ret2plt |
| `PIE: PIE enabled` | image base randomized per run | hardcoded gadget/symbol addresses | leak first (puts GOT, format string, unsorted bin) or partial overwrite — low 12 bits of any pointer stay fixed |
| `Stack: Canary found` | random canary at fs:0x28 checked before ret | naive saved-RIP overwrite | leak canary (format string `%N$p`, overflow byte-by-byte) or bypass the return path: function pointers, GOT, exit handlers, heap |
| `Stack: No canary` | — | nothing | direct cyclic overflow → `references/stack.md` |
| `RELRO: Partial RELRO` | `.got.plt` writable (lazy binding) | nothing | GOT overwrite (`references/format-string.md`, heap poisoning) |
| `RELRO: Full RELRO` | BIND_NOW; GOT mapped read-only after startup | GOT overwrite | libc data targets (`__free_hook` on glibc ≤ 2.33), FSOP/exit handlers (`references/heap.md`), stack ROP |
| `Stripped: No` | symtab present | — | `nm ./chal` / Ghidra; hunt win/backdoor symbols |
| `Stripped: Stripped` | symtab removed | symbol names | Ghidra; dynsym survives if dynamic (`nm -D ./chal`) |
| `FORTIFY: Enabled` | `__printf_chk`-style wrappers | `%n` with format in writable memory aborts (`*** %n in writable segment detected ***`) | format string is leak-only; get the write elsewhere |
| `RWX: Has RWX segments` | some loadable segment is rwx | nothing | locate it (`readelf -lW`), jump shellcode there |

## 3. Canary specifics

- glibc x86_64 canary ends in a NUL byte (`0x…00`): visible in a `%N$p` dump;
  an overflow copying byte-by-byte stops at that NUL (7 unknown bytes).
- Fork servers (fork after accept) inherit canary, ASLR and heap state across
  connections: brute-force one byte per connection (1/256), crash = wrong
  guess, reconnect and continue (`references/stack.md` section 8).

## 4. PIE / ASLR specifics

- System ASLR randomizes libc, stack and heap even for No-PIE binaries; PIE
  only adds the main image to the shuffle.
- Partial overwrite math: low 12 bits of a code pointer are page offset
  (fixed) → 1-byte saved-RIP overwrite is deterministic within the same page;
  2-byte overwrite leaves 4 unknown bits = 1/16.
- Remote ≠ local: the remote glibc usually differs from yours — match the
  handout libc with pwninit (`references/toolchain.md`) before computing any
  libc offset, or every address is wrong.

## 5. Static vs dynamic

`file ./chal`: "dynamically linked" vs "statically linked".

| | Dynamic | Static |
|---|---|---|
| Retarget | ret2libc / ret2plt (`references/stack.md`) | in-binary ROP: gadgets + `syscall` are all present |
| libc identity | handout libc; ldd target | `strings ./chal \| grep -m1 "GNU C Library"` — static binaries embed the glibc banner |
| Pitfalls | version drift, Full RELRO | stripped, huge gadget space; seccomp common |

Untrusted binaries: prefer `readelf -d` over `ldd` — ldd executes the target's
own loader chain (router rule 2).

## 6. seccomp / sandbox detection

```bash
strace -f ./dist/chal </dev/null 2>&1 | grep -E 'seccomp|prctl'   # pacman -S strace
seccomp-tools dump ./dist/chal                                    # gem install seccomp-tools
```

`seccomp-tools dump` prints the BPF filter line by line. Consequences:

| Filter | Consequence |
|---|---|
| execve blocked, open/read/write allowed (ORW) | `system`/`one_gadget` dead — chain open("/flag") → read → write (`references/shellcode.md` section 3) |
| only read/write (no open) | dump memory with `write(1, addr, n)` if the flag is already mapped, or find an allowed path/file primitive elsewhere |
| open blocked, openat allowed | use `openat(AT_FDCWD=-100, path, 0)` in the ROP/shellcode chain |

Read the actual filter before chaining — do not guess what is allowed.
