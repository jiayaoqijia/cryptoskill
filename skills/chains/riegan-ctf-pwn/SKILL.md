---
name: ctf-pwn
description: Use when a challenge involves binary exploitation: an ELF binary often paired with a remote `nc host port`, the pwn category, stack overflow, ROP, ret2libc, ret2win, SROP, format string bugs, GOT/PLT overwrites, shellcode, glibc heap attacks (tcache, fastbin, UAF, double free, house-of-*), checksec output (NX, PIE, RELRO, canary, seccomp), one_gadget, cyclic offsets, pwninit, or pwntools exploit scripting. Covers mitigation triage, stack/format-string/heap/shellcode playbooks and the gdb toolchain; event workflow, workspace, flag regex and submission live in the `ctf` router skill.
---

# ctf-pwn — ELF binary exploitation

The router (`../ctf/SKILL.md`) owns workspace layout, untrusted-artifact
handling, the remote-connection gate, flag regex and submission. Those rules
apply unchanged here.

## Triage (first 10 minutes, beginner-safe)

Static commands only — they never execute the target:

```bash
file dist/chal                                    # arch, static vs dynamic, stripped
scripts/ctf pwn checksec dist/chal                # mitigations -> references/mitigations.md
readelf -d dist/chal | grep -E 'NEEDED|BIND_NOW'  # deps + RELRO hint (safer than ldd)
readelf -lW dist/chal | grep -E 'GNU_RELRO|GNU_STACK'
nm dist/chal | grep -iE 'win|flag|backdoor|shell' # if not stripped; also: nm -D
strings -n 6 dist/chal | grep -iE 'flag|/bin/sh|seccomp|sandbox|GNU C Library'
```

Then a test run — only after the router gate (podman isolation or user
approval):

```bash
./dist/chal                     # observe: menu? prompt? echo? how is input read?
python3 -c "print('A'*200)" | ./dist/chal    # does long input crash it?
```

Map what you saw to the first attack:

| Observation | First attack | Read |
|---|---|---|
| NX off + input lands on stack/heap | shellcode, jump to it | `references/shellcode.md` |
| No canary, No PIE, NX on | cyclic offset → ret2win, else ret2libc/ROP | `references/stack.md` |
| No canary, PIE on | overflow + partial overwrite, or leak first | `references/stack.md` |
| Canary on | leak canary (format string / byte-by-byte) then overflow | `references/format-string.md` |
| echo reflects `%p` probes | format string: leak → write → GOT | `references/format-string.md` |
| Full RELRO | GOT locked: stack ROP, libc data, heap | `references/mitigations.md` |
| malloc/free menu (add/edit/delete/show) | heap: glibc version → attack catalog | `references/heap.md` |
| statically linked | in-binary syscall ROP | `references/stack.md`, `references/shellcode.md` |
| seccomp filter, execve blocked | ORW chain to read the flag | `references/shellcode.md` |
| remote + libc.so.6 handout | pwninit first, exploit locally against it | `references/toolchain.md` |

## Playbook (expert flow)

1. **Environment first.** Remote handout ships the target's libc (± ld):
   `pwninit` before writing a single offset (`references/toolchain.md`).
   Local-only target: still pin the glibc version — technique choice is
   version-gated (`references/heap.md` section 2).
2. **Find the bug**: audit in Ghidra (workflow in the `ctf-rev` skill),
   exercise it by hand; record allocation sizes, indexes, edit lengths.
3. **Choose by preconditions**, not by habit: leak available? write size?
   glibc version? Use the attack tables in the references (quick index below).
4. **Build against the patched binary** in one script
   (`scripts/solve-template.py`): `--local` while iterating, `--remote host
   port` to ship — same code path.
5. **Cash out**: `system("/bin/sh")` + `io.interactive()` normally; under
   seccomp, ORW chain and grep the flag from the output; check one_gadget
   constraints before hand-rolling chains (`references/toolchain.md`).
6. **Flag**: grep the router flag regex from the tube output; log to
   `work/<event>/flags.md` before anything else.

Attack quick index:

| Attack | Preconditions | Reference |
|---|---|---|
| ret2win | RIP offset + win symbol | `references/stack.md` |
| ret2libc | libc leak or matched handout libc | `references/stack.md` |
| SROP | rax control + `syscall; ret` | `references/stack.md` |
| Stack pivot | tiny overflow, bigger controlled buffer | `references/stack.md` |
| Partial overwrite | no leak, fork server or low-entropy target | `references/stack.md` |
| fmt leak + write | printf(user) | `references/format-string.md` |
| GOT overwrite | Partial RELRO + fmt/heap write | `references/format-string.md` |
| tcache poisoning | UAF/overflow into freed chunk fd | `references/heap.md` |
| unsorted bin leak | free chunk > 0x410 + read-after-free | `references/heap.md` |
| FSOP / exit handlers | libc base + write, hooks gone (>= 2.34) | `references/heap.md` |
| Shellcode | NX off, or mprotect via ROP | `references/shellcode.md` |

## Scripts

- `scripts/solve-template.py` — pwntools exploit skeleton:
  `--remote HOST PORT` / `--libc PATH` / `--gdb`, TODO markers, flag grep.
- `scripts/off.py` — cyclic offset finder: local crash + core dump auto-solve,
  remote pattern send, or pure `0x61616164` → offset lookup.

## References

- `references/mitigations.md` — checksec line-by-line, attack-surface matrix,
  canary/PIE/ASLR specifics, seccomp detection and the ORW consequence,
  static vs dynamic.
- `references/stack.md` — cyclic offsets, ret2win, ret2libc (leak → libc
  database → one_gadget), ROP class, SROP, stack pivot, partial overwrite,
  movaps alignment pitfall.
- `references/format-string.md` — offset finding, reads (`%p`/`%s`), writes
  (`%n`/`%hhn`), `fmtstr_payload`/`FmtStr`, GOT overwrite workflow, recipe.
- `references/heap.md` — glibc version identification, defense timeline
  (2.26 tcache → 2.32 safe-linking → 2.34 hook removal), attack catalog with
  preconditions, poison-null-byte sketch, post-2.34 targets (FSOP, exit
  handlers/TLS), malloc.c source pointers.
- `references/shellcode.md` — shellcraft generation, ORW, sleds, env-var
  shellcode, ROP→mprotect→bss.
- `references/toolchain.md` — pwntools tube/gdb idioms, pwninit/patchelf,
  ROPgadget/ropper/one_gadget/seccomp-tools, pwndbg/gef heap commands, libc
  databases.

## Toolbox

| Tool | Install | Purpose |
|---|---|---|
| pwntools | `scripts/setup.sh` (repo `.venv`) | tubes, ROP, fmtstr, shellcraft, checksec, cyclic, ELF |
| `scripts/ctf` | included | run anything inside the venv (`scripts/ctf pwn checksec ./chal`) |
| pwninit | `cargo install pwninit` | match binary to handout libc/ld (patchelf + libc.rip fetch) |
| patchelf | `sudo pacman -S patchelf` | `--set-interpreter` / `--replace-needed` |
| ROPgadget | ships with pwntools venv | gadget search (`scripts/ctf ROPgadget ...`) |
| ropper | `uv pip install --python .venv/bin/python ropper` | alternative gadget search |
| one_gadget | `sudo pacman -S ruby && gem install one_gadget` | execve gadgets + constraints from libc |
| seccomp-tools | `gem install seccomp-tools` | dump seccomp BPF filters |
| pwndbg | `sudo pacman -S pwndbg` | gdb with heap awareness: `gdb-pwndbg ./chal` |
| gef | `bash -c "$(curl -fsSL https://gef.blah.cat/sh)"` | alternative gdb frontend |
| strace | `sudo pacman -S strace` | syscall trace, seccomp detection |
| libc-database | `git clone https://github.com/niklasb/libc-database` | match libc from leaked symbols |
