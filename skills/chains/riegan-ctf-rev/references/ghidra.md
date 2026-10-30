# Ghidra — install, GUI, headless decompile dump

## Install

```bash
sudo pacman -S ghidra        # JDK 21 already on this host
# set once per shell (or in ~/.bashrc):
export GHIDRA_INSTALL_DIR=/usr/share/ghidra   # pacman layout; verify with:
pacman -Ql ghidra | grep analyzeHeadless
```

Ghidra 11.x ships Jython-2.7-based scripting AND PyGhidra (CPython 3) support;
the bundled `ghidra_dump.py` here is written in syntax valid under both
(no f-strings, no walrus, prints via commas).

## GUI workflow (CodeBrowser)

```bash
ghidraRun                     # launcher script from the package
# File → Import File → binary → accept defaults → Analyze → Yes, all options
```

Auto-analysis options that matter (Analysis → Auto Analyze):
- **Decompiler Parameter ID** — recovers function signatures, worth the time.
- **Demangler** (GNU) — on by default; makes C++ `_ZN...` names readable.
- **Aggressive Instruction Finder** — only for code the disassembler missed
  (packed blobs); slow, use targeted instead.

Daily-driver keys/flows:

| Task | How |
|---|---|
| Find entry/main | Symbol Tree → Exports → `entry`; read the `__libc_start_main` call arg |
| Decompiler | Window → Decompile (default right pane); `F5` equivalent is automatic |
| String → code | Defined Strings window → double-click → right-click xref in decompiler → References → Show References to Address |
| Rename | press `L` on a function/label — do this constantly |
| Set function signature | press `F` on the function — fix args, decompile improves |
| Retype variable | right-click variable in decompiler → Auto Create Structure / Retype Variable |
| Struct/array types | Data Type Manager → create Structure; on data: right-click → Create Array; apply struct to a pointer → fields appear in decompiler |
| Patch instruction | right-click instruction in listing → Patch Instruction; then File → Export Program to write the binary |
| Bookmarks / notes | right-click → Add Bookmark; the Notes window is your in-tool notepad |

Version tracking between patch levels ( organizers ship `v1`, `v2` after a fix):
- File → New Project → **Version Tracking** project.
- With program A open: Tools → Version Tracking → Mark for Compare → open B →
  Compare and Auto-Merge. Diff highlights changed functions — often the fixed
  bug is a one-function diff. For quick one-offs, `radare2`'s
  `radiff2 -A binary1 binary2` or plain `cmp`/bindiff-style eyeballing of the
  Ghidra decompile dump (below) also works.

Exporting decompiled C manually: in Decompile window toolbar → the export
button (or File → Export Program → format C/C++) exports the current function
only — for whole-program dumps use headless below.

## Headless decompile dump (the recipe)

Two pieces in `scripts/`:

- `scripts/ghidra-decompile.sh <binary>` — wrapper: creates a temp Ghidra
  project, imports the binary, runs `ghidra_dump.py` as `-postScript`, streams
  all decompiled functions to stdout (or a file with `-o`).
- `scripts/ghidra_dump.py` — runs INSIDE Ghidra's script engine (Jython 2 for
  Ghidra 10.x, Jython/PyGhidra for 11+). It is deliberately written in
  intersection syntax.

```bash
export GHIDRA_INSTALL_DIR=/usr/share/ghidra
skills/ctf-rev/scripts/ghidra-decompile.sh dist/binary > decomp.c
skills/ctf-rev/scripts/ghidra-decompile.sh dist/binary -o decomp.c
grep -n 'FUNC ' decomp.c | less          # function index
grep -n -i 'flag\|check\|valid' decomp.c
```

Why dump everything: grep-ability. Regex over the whole program's C beats
clicking through 200 functions in the GUI; use the GUI for the handful of hits.

Raw headless invocation (what the wrapper does), for scripting into solvers:

```bash
"$GHIDRA_INSTALL_DIR/support/analyzeHeadless" /tmp/ghidra_proj proj \
    -import binary -scriptPath skills/ctf-rev/scripts \
    -postScript ghidra_dump.py -deleteProject
```

Ghidra 11+ note: PyGidra/PyGhidra scripts (`.py` with `# PyGhidra` header or
run via `pyghidraRun`) get real CPython 3 and pip libs; classic
`analyzeHeadless -postScript` with a plain `.py` still runs Jython unless the
script declares PyGhidra. `ghidra_dump.py` stays Jython-compatible so it works
in both 10.x and 11.x under `-postScript`.

## Post-script ideas

Ghidra scripts in Java or Python can automate: rename `FUN_` by string xref,
dump `.data`/`.rodata` as arrays, iterate instructions. Script Manager →
create new → templates are generated for you. Keep bespoke scripts in the
challenge `solve/` dir and pass its dir via `-scriptPath`.
