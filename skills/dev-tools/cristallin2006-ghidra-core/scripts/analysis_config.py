"""Analysis-option configuration for the ghidra-core skill (PyGhidra).

The Jython-era `set_analysis_options.py` ran as a Ghidra `-preScript`, an
analyzeHeadless-only hook with no PyGhidra equivalent. Under PyGhidra the same
job is done through the program's analysis properties, which must be read and
written *after* the program is loaded but *before* `pyghidra.analyze()` runs --
so this lives here as a helper the driver calls, not as a standalone script.

Verified on Ghidra 12.1.3: `analysis_properties()` exposes 147 options for 31
analyzers, each analyzer's own name is a top-level boolean enable switch.
"""
from __future__ import annotations

# Analyzers whose cost is usually not worth paying for a first-pass triage.
# Matched exactly against the top-level option names the program reports, so an
# analyzer this Ghidra does not ship is simply skipped rather than guessed at.
HEAVY_ANALYZERS = (
    "Aggressive Instruction Finder",
    "Decompiler Parameter ID",
    "Decompiler Switch Analysis",
    "DWARF",
    "Demangler GNU",
    "Function ID",
    "Stack",
    "Create Address Tables",
)

MODES = ("default", "minimal")


def describe(program) -> dict:
    """Report the analyzer switches this program exposes."""
    import pyghidra

    opts = pyghidra.analysis_properties(program)
    names = [str(n) for n in opts.getOptionNames()]
    top = sorted({n.split(".", 1)[0] for n in names})
    enabled = []
    for name in top:
        try:
            if opts.getBoolean(name, True):
                enabled.append(name)
        except Exception:  # noqa: BLE001 - non-boolean top-level options exist
            continue
    return {
        "option_count": len(names),
        "analyzer_count": len(top),
        "analyzers": top,
        "enabled": enabled,
        "heavy_present": [n for n in HEAVY_ANALYZERS if n in top],
    }


def configure(program, mode: str = "minimal") -> dict:
    """Apply an analysis profile to a freshly loaded program.

    `minimal` disables the heavy analyzers to get a fast first pass; `default`
    turns them back on. Returns the switches that actually changed.
    """
    if mode not in MODES:
        raise ValueError(f"unknown analysis mode {mode!r}; expected one of {MODES}")

    import pyghidra

    opts = pyghidra.analysis_properties(program)
    available = {str(n).split(".", 1)[0] for n in opts.getOptionNames()}

    changed = {}
    # Option writes are program mutations and Ghidra rejects them outside a
    # transaction (db.NoTransactionException).
    with pyghidra.transaction(program, f"ghidra-core analysis profile {mode}"):
        for name in HEAVY_ANALYZERS:
            if name not in available:
                continue
            want = mode == "default"
            try:
                current = bool(opts.getBoolean(name, True))
            except Exception:  # noqa: BLE001 - not a boolean switch in this build
                continue
            if current != want:
                opts.setBoolean(name, want)
                changed[name] = want
    return {"mode": mode, "changed": changed}
