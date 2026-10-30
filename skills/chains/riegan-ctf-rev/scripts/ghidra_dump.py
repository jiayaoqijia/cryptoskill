#!/usr/bin/env python
# ghidra_dump.py — runs INSIDE Ghidra (analyzeHeadless -postScript, or the
# Script Manager GUI). NOT a standalone CLI: it uses Ghidra-script globals
# (currentProgram, monitor) injected by the Ghidra script engine; there is no
# --help because Ghidra calls it, not a shell.
#
# Syntax is the Python 2/3 intersection: it executes under Ghidra 10.x/11.x
# Jython (Python 2.7) and under PyGhidra (CPython 3) unchanged. No f-strings,
# no print-as-statement-only constructs, no 3-only builtins.
# `python3 -m py_compile` on this file is a SYNTAX-ONLY check — it does not
# and must not execute any Ghidra API call.
#
# What it does: iterates every function in the current program and prints
# decompiled C for each, separated by '// FUNC <name> <entry>' headers, so the
# whole program can be grepped offline. Optional arg (Ghidra script arg):
# an absolute output file path; default prints to stdout.

import os

# Ghidra script API (provided by the harness; unresolved when read standalone)
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

OUT_PATH = None
args = getScriptArgs()          # noqa: F821 — Ghidra global
if args and len(args) > 0 and len(args[0]) > 0:
    OUT_PATH = args[0]


def decompile_all(program, out):
    ifc = DecompInterface()
    ifc.openProgram(program)
    mon = ConsoleTaskMonitor()
    fm = program.getFunctionManager()
    funcs = fm.getFunctions(True)  # iterate in address order
    count = 0
    for f in funcs:
        if mon.isCancelled():
            break
        name = f.getName()
        entry = f.getEntryPoint()
        out.write("// FUNC %s %s\n" % (name, entry))
        res = ifc.decompileFunction(f, 60, mon)
        if res.decompileCompleted():
            out.write(res.getDecompiledFunction().getC())
        else:
            out.write("// DECOMPILE FAILED: %s\n" % res.getErrorMessage())
        out.write("\n\n")
        count += 1
    ifc.dispose()
    return count


if OUT_PATH is not None:
    fh = open(OUT_PATH, "w")
    n = decompile_all(currentProgram, fh)          # noqa: F821 — Ghidra global
    fh.close()
    println("ghidra_dump.py: wrote %d functions to %s" % (n, OUT_PATH))  # noqa: F821
else:
    n = decompile_all(currentProgram, stdout)      # noqa: F821 — Ghidra global
    println("ghidra_dump.py: dumped %d functions" % n)                    # noqa: F821
