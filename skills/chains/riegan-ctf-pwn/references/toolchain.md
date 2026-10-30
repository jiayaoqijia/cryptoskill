# Toolchain — pwntools idioms, libc matching, gadget tools, gdb

## 1. pwntools tubes

```python
from pwn import *
context.log_level = "info"          # "debug" = full traffic hexdump

io = process("./chal")              # local
io = remote("host", 1337)           # remote — router remote gate first
```

| Idiom | Purpose |
|---|---|
| `io.sendline(b"1")` / `io.send(b"x")` | deliver (sendline appends `\n`) |
| `io.recvuntil(b"choice: ")` | sync to a prompt before the next write |
| `io.sendlineafter(b"name: ", b"aaa")` | recvuntil + sendline in one |
| `io.recvline()` / `io.recv(n)` / `io.recvall(timeout=5)` | line / n bytes / drain |
| `io.clean()` / `io.clean_and_log()` | discard (or print) pending output |
| `io.interactive()` | hand the tube to your terminal — end of exploit |

### Debugging with gdb

```python
context.terminal = ["tmux", "new-window"]        # mandatory for gdb.debug
io = gdb.debug("./chal", gdbscript="b main\ncontinue\n")

io = process("./chal")                            # or attach to a running one
gdb.attach(io, gdbscript="b *0x40123a\ncontinue\n")
```

- `gdb.debug` spawns the target under gdb in a new terminal window and gives
  you the tube; `gdb.attach` attaches to a process you already drove (catch
  state after menu setup).
- `gdbscript` is plain gdb command text. Add `input("pid? ")` pauses in your
  script to attach at the right moment.

### ELF helpers

```python
elf = ELF("./chal")
elf.sym["main"]                        # symbols dict (elf.symbols alias)
elf.plt["puts"], elf.got["puts"]       # PLT stub / GOT slot
next(elf.search(b"/bin/sh\x00"))       # string inside the image
elf.bss(0x100)                         # writable scratch address
elf.libc                               # ldd-resolved local libc (ELF or None)
```

## 2. Match the remote libc first (pwninit)

A remote handout (chal + libc.so.6 ± ld) means every offset must come from
*that* libc, and local testing must run against it:

```bash
cargo install pwninit                  # one-time; needs Rust toolchain
cd work/<event>/<chal>/solve
pwninit --bin ./dist/chal --libc ./dist/libc.so.6
# fetches the matching ld when absent (libc.rip), patchelf-patches a copy of
# the binary, prints how to run it; see pwninit --help (solve template option)
```

Manual equivalent:

```bash
patchelf --print-interpreter ./chal
patchelf --set-interpreter "$PWD/ld-2.35.so" --replace-needed libc.so.6 "$PWD/libc.so.6" ./chal
# or run through the provided loader directly, no patching:
./ld-2.35.so --library-path . ./chal
```

Identify what you have: `strings libc.so.6 | grep -m1 "GNU C Library"`,
`./ld-2.35.so --version`, `ldd --version` (host glibc).

## 3. Gadget and one-shot tools

```bash
scripts/ctf ROPgadget --binary ./chal                        # ships with pwntools
scripts/ctf ROPgadget --binary ./chal --only "pop|ret"
scripts/ctf ROPgadget --binary ./libc.so.6 --string "/bin/sh"
ropper -f ./chal --search "pop rdi"                         # pip install ropper
```

ROPgadget dumps gadgets; the pwntools `ROP` class (`references/stack.md`)
drives the same engine to build chains. Search the libc too — most gadgets
live there.

one_gadget (Ruby) finds `execve("/bin/sh", …)` single-address wins in a libc:

```bash
sudo pacman -S ruby && gem install one_gadget
one_gadget ./libc.so.6
# 0x50a37 execve("/bin/sh", rsp+0x40, environ)
# constraints:
#     [rsp+0x40] == NULL
#     rsp & 0xf == 0
```

Pick a gadget whose constraints (null stack slots/registers, 16-byte rsp
alignment) already hold at your control point; otherwise satisfy them with
setup gadgets (`pop rbx` = 0, a `ret` for alignment) or fall back to the
`pop rdi; system` chain.

seccomp filters:

```bash
gem install seccomp-tools
seccomp-tools dump ./chal
```

## 4. gdb frontends and heap debugging

Bare gdb is preinstalled; heap work wants a frontend:

| Frontend | Install | Run |
|---|---|---|
| pwndbg | `sudo pacman -S pwndbg` | `gdb-pwndbg ./chal` |
| gef | `bash -c "$(curl -fsSL https://gef.blah.cat/sh)"` | `gdb ./chal` (auto-loads) |

| Task | pwndbg | gef |
|---|---|---|
| chunk map | `vis_heap_chunks` (`vis`) | `heap chunks` |
| bins overview | `bins` | `heap bins` |
| fastbin fake-size check | `find_fake_fast <addr>` | — |

Everyday gdb (bare works): `b *0x401234`, `c`, `ni`/`si`,
`x/20gx $rsp`, `x/4gx <chunk>`, `info proc mappings` (frontends: `vmmap`),
`p $rsp % 16` (alignment, `references/stack.md` section 7).

## 5. libc databases

| Need | Where |
|---|---|
| match libc from leaked symbol offsets | https://libc.rip , https://libc.blukat.com |
| offline database | `git clone https://github.com/niklasb/libc-database` → `./find puts 5f0`, `./download <id>` |
| which glibc is this? | `strings libc.so.6 \| grep -m1 "GNU C Library"` |

Version-gated technique selection: `references/heap.md` section 2.
