# Binary Audit Workflow

## Command Sequence

```bash
ghidra-rpc load /path/to/binary
ghidra-rpc metadata binary          # arch, bits, format, compiler
ghidra-rpc imports binary           # external dependencies / capabilities
ghidra-rpc exports binary           # relevant for shared libraries
ghidra-rpc strings binary "<term>"  # run with several terms: http, error, password, key, /
ghidra-rpc functions binary         # entry points, named functions, xref-heavy utilities
ghidra-rpc decompile binary main    # start here, work outward
```

## Non-Obvious Tips

**`functions` pagination** — the response includes `total` (all functions) and `count`
(this page), so you know how many pages remain:
```bash
ghidra-rpc functions binary --limit 100 --offset 0
ghidra-rpc functions binary --limit 100 --offset 100
```

**`xrefs-from --no-stack`** — strips `Stack[-0x…]` frame references so the call
graph shows only real callees:
```bash
ghidra-rpc xrefs-from binary <func> --no-stack
```

**Rename propagation** — renaming a function immediately improves the decompiled
output of all its callers, so rename as you go rather than at the end.
