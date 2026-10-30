# Heap exploitation — glibc

Bug classes first: overflow (edit past a chunk's bounds), UAF (write/read after
free), double free, arbitrary free, off-by-one. Every attack below composes one
of those with a specific glibc version's checks. Version numbers stated here
are upstream releases; distros backport — always confirm against the target's
actual `malloc.c` (section 6).

## 1. Identify the glibc (before choosing any technique)

```bash
strings libc.so.6 | grep -m1 "GNU C Library"   # exact version banner
./ld-2.35.so --version                          # provided loader reports its glibc
ldd --version                                   # host glibc (local-only targets)
getconf GNU_LIBC_VERSION                        # host glibc, alternate
```

Remote handouts ship `libc.so.6` (+/- `ld-*.so`): match it with pwninit first
(`references/toolchain.md`). No handout: leak a `main_arena`-range pointer and
match offsets against candidates via libc.rip / libc-database.

Symbol probes:

| Probe | Result | Conclusion |
|---|---|---|
| `nm -D libc.so.6 \| grep -w __free_hook` | symbol exists | glibc <= 2.33: hooks are writable targets |
| `nm -D libc.so.6 \| grep -w __malloc_hook` | missing | glibc >= 2.34: hooks removed |
| `strings libc.so.6 \| grep "double free detected in tcache"` | present | >= 2.29 tcache key check |
| gdb: `x/2gx` a freed tcache chunk | fd looks like `(heap>>12) ^ heap` | >= 2.32 safe-linking |

## 2. Defense timeline (what changed when)

| glibc | Change in malloc.c | Exploitation impact |
|---|---|---|
| 2.26 | tcache added: `tcache_perthread_struct` at heap start, 64 bins, 7 chunks each, chunk sizes 0x20-0x410 | a freed chunk you can write = one-step poisoning; fastbins only reached after the tcache bin is full (7) |
| 2.29 | tcache `key` field + "free(): double free detected in tcache 2"; top-chunk sanity "malloc(): corrupted top size"; unsorted/smallbin integrity checks tightened | blind double free dead, House of Force dead, key bypass required |
| 2.32 | safe-linking: tcache and fastbin `fd` stored mangled: `stored = (mem_addr >> 12) ^ next` (`PROTECT_PTR`) | poisoning needs a heap leak; a lone freed tcache chunk leaks `mem>>12` directly |
| 2.34 | `__malloc_hook`/`__free_hook`/`__realloc_hook`/`__memalign_hook` removed | hook overwrites replaced by FSOP / exit handlers / TLS (section 4) |
| 2.24 (older, still relevant) | FILE vtable validation (`IO_validate_vtable`) | FSOP must use real vtables inside `__libc_IO_vtables` |

Also fixed in memory: fastbins cover chunk sizes 0x20-0x80 by default
(`global_max_fast`); smallbins 0x90-0x3f0; largebins >= 0x400; tcache absorbs
any free of chunk size <= 0x410 first.

## 3. Attack catalog (preconditions -> mechanics -> versions)

### 3.1 tcache poisoning — the workhorse (2.26+)

Preconditions: UAF write or heap overflow into the `fd` (first qword of user
data) of a chunk already sitting in a tcache bin.

```
free(p)                                   # p lands in tcache[idx]
*(uint64_t *)p = TARGET                   # glibc < 2.32: write it plain
*(uint64_t *)p = ((uint64_t)p >> 12) ^ TARGET   # glibc >= 2.32 (safe-linking)
malloc(sz) -> p                           # pops p
malloc(sz) -> TARGET                      # pops your address
```

- tcache allocation does no size/consistency check: TARGET needs no fake
  chunk header. Keep it 16-byte aligned (newer 2.3x glibc rejects unaligned
  tcache entries — grep `unaligned tcache chunk` in your malloc.c).
- 2.32+ needs the *page number* of `p` only — a leaked `fd` of a lone freed
  chunk (== `p >> 12`) is already enough.
- Classic TARGETs: `__free_hook` (<= 2.33), a saved return slot on the stack,
  GOT under Partial RELRO (aim at a 16-aligned address covering the entry),
  `tcache_perthread_struct` itself (full bin control).

### 3.2 fastbin dup + fastbin dup into stack

Preconditions: double free `free(a); free(b); free(a)` with the tcache bin for
that size already full (7) so the chunks land in the fastbin (sizes 0x20-0x80);
the "double free or corruption (fasttop)" check only catches immediate
repeats, so a-b-a passes.

Mechanics: fastbin list a->b->a->...; three allocations give you two live
pointers to `a`; edit through one to set its `fd` to FAKE. Further mallocs
walk to FAKE. FAKE needs a matching size field at FAKE+8
("malloc(): memory corruption (fast)") — forge a fake chunk header on the
stack/bss ("into stack"). glibc >= 2.32: mangle the fd exactly like tcache.

### 3.3 tcache stashing unlink attack (smallbin + calloc)

Preconditions:
1. chunks resident in a *smallbin* (sizes 0x90-0x3f0) with a corrupted `bk`
   (overflow/UAF) — the smallbin tail's `bk` points at your fake chunk;
2. the fake chunk's `fd` points back at the victim (passes the
   "malloc(): smallbin double linked list corrupted" check);
3. the tcache bin for that size has count < 7 (room to stash);
4. the triggering allocation is `calloc` — calloc bypasses tcache and pulls
   from the smallbin.

Mechanics: while the smallbin still holds chunks and tcache has room,
`_int_malloc` stashes remaining chunks via `tcache_put`, walking your
corrupted `bk` chain — the fake chunk gets inserted into the tcache. The next
plain `malloc(sz)` returns it. Side effect: 16 bytes of tcache metadata are
written at TARGET. Works 2.26+; see how2heap `tcache_stashing_unlink.c`.

### 3.4 unsorted bin leak (libc leak)

Preconditions: read-after-free on a chunk of size > 0x410 (or fill the tcache
first so any free lands in the unsorted bin).

Mechanics: a lone chunk in the unsorted bin has fd and bk both pointing at the
`main_arena` unsorted-bin head inside libc data. Leak one, subtract the
offset for *your* libc (`main_arena` commonly = `&__malloc_hook + 0x10`
pre-2.34; resolve precisely with gdb + debug symbols or libc-database) →
libc base.

### 3.5 unsorted bin attack (write a libc pointer near TARGET)

Preconditions: write on an unsorted chunk's `bk`; any later malloc that
removes/sorts the unsorted bin.

Mechanics: `victim->bk = TARGET - 0x10`; on unlink malloc.c does
`bck->fd = unsorted_chunks(av)` — a `main_arena` pointer lands at TARGET.
Classic use: `global_max_fast` → frees of arbitrary sizes go to "fastbins",
enabling fastbin attacks at any size.

Version: unsorted integrity checks (`bck->fd != victim` → "malloc():
corrupted unsorted chunks") were tightened around 2.28-2.29 — before that the
bk-only overwrite runs as-is; on newer glibc satisfy the check or use another
write. Verify in your malloc.c.

### 3.6 largebin attack (write a chunk address anywhere)

Preconditions: control of `bk`/`bk_nextsize` of a chunk being sorted into a
largebin (>= 0x400) plus a size-ordered insert of a second chunk.

Mechanics: insertion does `victim->bk_nextsize->fd_nextsize = victim`-style
stores — a heap/libc pointer gets written at attacker-chosen addresses (up to
two writes per insert). Use to smash `global_max_fast`, `mp_.tcache_bins`,
`_IO_list_all`, or any single-pointer target. Partially hardened across 2.3x;
mechanics still viable — see how2heap `large_bin_attack.c` for your version.

### 3.7 Double free post-2.29 (tcache key) and House of Botcake

The `key` field (second qword of `tcache_entry`) equals the tcache pointer
while in the bin; `free()` walks the bin and aborts on match ("free(): double
free detected in tcache 2", 2.29+). Bypasses:

- UAF write: zero/alter `key` between frees (8 bytes at mem+8).
- free the same memory under two different chunk sizes (shrink overlap).
- House of Botcake (needs tcache full + adjacent chunks A|B, B victim):

```
1. fill tcache for size X (7 entries)
2. free(A); free(B)        # tcache full -> both to unsorted; A+B consolidate
3. malloc one X            # from tcache -> count 6, room again
4. free(B)                 # B's key was never set (it never was in tcache)
                           # -> tcache_put(B) succeeds
5. B is now in tcache AND inside the big unsorted chunk:
   malloc(X) -> B ; malloc(big) -> chunk overlapping B -> overlap primitive
```

### 3.8 FSOP — FILE structure oriented programming (post-2.34 staple)

Trigger: `exit()` → `_IO_cleanup` → `_IO_flush_all` walks `_IO_list_all` and
calls each FILE's vtable OVERFLOW. Build a fake FILE and make the list reach
it (overwrite `_IO_list_all` via a largebin/unsorted write, or corrupt
`stdout`/`stderr` fields in libc data).

- vtable must point inside `__libc_IO_vtables` (2.24+): use real tables —
  `_IO_str_jumps`, `_IO_wfile_jumps`.
- `_IO_str_jumps` route: `_IO_strfile` extends FILE with callable pointers
  `_s._allocate_buffer`/`_s._free_buffer`; drive `_IO_str_overflow` (rdi =
  size you shape) or `_IO_str_finish` (rdi = `_IO_buf_base` you set) — point
  the callable at `system` with `"/bin/sh"` as the shaped argument.
- wide-data route ("House of Apple" family): vtable = `_IO_wfile_jumps`;
  `_IO_wfile_overflow` → `_IO_wdoallocbuf` →
  `fp->_wide_data->_doallocate(fp)` with rdi = fp — point the fake FILE's
  start at a `"/bin/sh"` string.
- Needs libc base (combine with the unsorted leak). Conceptual here — pin
  exact struct offsets from your libc's libio headers/writeups.

### 3.9 exit handlers / TLS dtor_list (post-2.34)

`exit()` runs `__run_exit_handlers` over the `initial` list (libc data) and
the TLS `dtor_list` (filled by `__cxa_atexit`); entries are
`{mangled_func, arg, map, next}` and handlers run as `func(arg, status)`.
Function pointers are stored `PTR_MANGLE`d on x86_64:
`stored = rol(func ^ guard, 0x11)`, guard = TLS `fs:0x30` — which sits
directly above the stack canary (`fs:0x28`).

Exploit: leak the guard (stack over-read past the canary, or any TLS/stack
leak) → forge `rol(system ^ guard, 0x11)` with `arg` = pointer to `"/bin/sh"`
→ overwrite a dtor_list entry or `initial` slot with your write primitive →
arbitrary call on exit.

### 3.10 Off-by-one / poison null byte → chunk overlap (sketch)

One stray NUL past your chunk clears bits of the *next* chunk's size LSB. Two
classic variants (verify arithmetic against how2heap `poison_null_byte.c` for
your glibc):

- **Clear PREV_INUSE (0x211 → 0x200)**: glibc believes the previous chunk is
  free and trusts the victim's `prev_size` — which your overflow pre-wrote.
  Free the victim → backward consolidation into a fake chunk you crafted in
  the previous chunk's data. The fake chunk's fd/bk must satisfy unlink
  integrity (`fd->bk == p && bk->fd == p`); result: a chunk overlapping the
  still-live neighbor.
- **Shrink size (0x511 → 0x500)**: allocations carve the shrunk chunk; the
  untracked 0x10 sliver plus a forged `prev_size` on the remainder lets a
  later free consolidate over a live chunk → overlap.

A non-NUL off-by-one that *grows* a size by 0x10 is simpler: the next malloc
of the corrupted chunk returns a chunk overlapping its neighbor's header.

### 3.11 House of ... one-liners

| House | One-liner | Status/era |
|---|---|---|
| Spirit | `free()` a fake chunk you planted in bss/stack (valid aligned size); next malloc returns it | works via tcache (no header checks); needs arbitrary free |
| Einherjar | off-by-NUL clears PREV_INUSE; fake prev_size consolidates backward into a fake chunk | overlap; must pass unlink checks |
| Lore | corrupt smallbin `bk` so malloc returns a stack-adjacent fake chunk | satisfy the 2.29+ fd check |
| Orange | no free needed: abuse top chunk via sysmalloc, old top → unsorted bin, then FSOP | original targets 2.23-era; feeds FSOP sections |
| Force | set top size to -1 and malloc to an arbitrary address | dead since 2.29 (top size sanity) |
| Roman | no-leak chain: 12-bit partial overwrites across fastbin/unsorted/FILE | builds on partial-overwrite math |

### 3.12 Leak summary

| Read | Gives |
|---|---|
| freed tcache chunk `fd` (2.32+) | `mem >> 12` when it is alone in the bin → heap base |
| freed unsorted chunk fd/bk | `main_arena`-range pointer → libc base |
| any chunk pointer the program prints | heap base directly |
| `tcache_perthread_struct` entries[] | heap base (struct is heap chunk #1) |

## 4. Structures to know (grep names in malloc.c)

- `tcache_perthread_struct` — heap chunk #1: chunk size 0x250 on 2.26-2.29
  (uint8 counts[64]), 0x290 on 2.30+ (uint16 counts[64]); entries[64] after.
  Overflow into it from an adjacent allocation = control of every bin.
- `main_arena` (libc data, not exported): unsorted/small/large bin heads.
- `mp_` (`struct malloc_par`): `tcache_bins`, `tcache_count`, `tcache_max`,
  `mmap_threshold`.
- Functions carrying the checks: `_int_malloc`, `_int_free`, `tcache_get`,
  `tcache_put`, `unlink_chunk` (macro pre-2.28), `sysmalloc` (top chunk),
  `malloc_consolidate`. Failure strings go through `malloc_printerr` — grep
  the message to locate the check.

## 5. Debugging

pwndbg: `vis_heap_chunks` (`vis`), `bins`, `find_fake_fast`; gef:
`heap chunks`, `heap bins` — see `references/toolchain.md`.

## 6. Sources

- glibc malloc.c by tag: https://sourceware.org/git/?p=glibc.git;a=blob;f=malloc/malloc.c
  (mirror: https://elixir.bootlin.com/glibc/latest/source/malloc/malloc.c)
- how2heap — per-version working PoCs: https://github.com/shellphish/how2heap
- Heap Exploitation book: https://heap-exploitation.dhavalkapil.com
- libc-database: https://github.com/niklasb/libc-database
