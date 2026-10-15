# Decompile all (optionally filtered) functions to C pseudocode
# Usage: [@out] [filter_regex] [timeout_seconds] [--limit N]
# @category DSH.Reverse
# @runtime PyGhidra

# --- DSH @out support (self-contained, no cross-script imports) ---
# If the first script argument starts with '@', it is popped and treated as an
# output file path: the JSON summary is written there, pseudocode goes to
# '<out>.c', and stdout only carries a short status summary between markers.
_DSH_OUT_PATH = None

def _dsh_extract_out():
    global _DSH_OUT_PATH
    try:
        args = list(getScriptArgs())
    except NameError:
        return []
    if args and str(args[0]).startswith("@"):
        _DSH_OUT_PATH = str(args[0])[1:]
        args = args[1:]
    return args

_DSH_ARGS = _dsh_extract_out()
# --- end DSH @out support ---

import codecs
import json
import re

from ghidra.app.decompiler import DecompInterface, DecompileOptions
from ghidra.util.task import ConsoleTaskMonitor


def emit(data):
    """Write JSON summary to @out file if given, else print between markers."""
    if _DSH_OUT_PATH:
        try:
            f = open(_DSH_OUT_PATH, "w")
            try:
                f.write(json.dumps(data))
            finally:
                f.close()
            summary = {
                "status": data.get("status", "success"),
                "out": _DSH_OUT_PATH,
                "c_out": _DSH_OUT_PATH + ".c",
                "count": data.get("succeeded", 0)
            }
            if data.get("status") == "error":
                summary["error"] = data.get("error")
            print("===JSON_START===")
            print(json.dumps(summary))
            print("===JSON_END===")
        except Exception as write_err:
            print("===JSON_START===")
            print(json.dumps({"status": "error",
                              "error": "failed to write out file: " + str(write_err)}))
            print("===JSON_END===")
    else:
        print("===JSON_START===")
        print(json.dumps(data))
        print("===JSON_END===")


def run():
    try:
        program = currentProgram
        if program is None:
            emit({"status": "error", "error": "No program loaded"})
            return

        args = list(_DSH_ARGS)

        # --limit N (or --limit=N) caps how many functions are decompiled;
        # everything else stays positional: [filter_regex] [timeout_seconds].
        limit = None
        positional = []
        i = 0
        while i < len(args):
            a = str(args[i])
            if a == "--limit":
                if i + 1 >= len(args):
                    emit({"status": "error", "error": "--limit requires a value"})
                    return
                try:
                    limit = int(args[i + 1])
                except (TypeError, ValueError):
                    emit({"status": "error",
                          "error": "Invalid --limit value: %s" % args[i + 1]})
                    return
                i += 2
            elif a.startswith("--limit="):
                try:
                    limit = int(a.split("=", 1)[1])
                except ValueError:
                    emit({"status": "error", "error": "Invalid --limit value: %s" % a})
                    return
                i += 1
            else:
                positional.append(a)
                i += 1

        filter_regex = positional[0] if len(positional) > 0 and positional[0] else None
        timeout = int(positional[1]) if len(positional) > 1 else 30

        name_re = None
        if filter_regex:
            try:
                name_re = re.compile(filter_regex)
            except Exception as e:
                emit({"status": "error",
                      "error": "Invalid filter regex: " + str(e)})
                return

        fm = program.getFunctionManager()
        monitor = ConsoleTaskMonitor()

        decompiler = DecompInterface()
        decompiler.setOptions(DecompileOptions())
        if not decompiler.openProgram(program):
            emit({"status": "error", "error": "Failed to initialize decompiler"})
            return

        sections = []
        total = 0
        succeeded = 0
        failed = []

        try:
            for func in fm.getFunctions(True):
                if func.isThunk() or func.isExternal():
                    continue
                if name_re is not None and not name_re.search(func.getName()):
                    continue
                if limit is not None and total >= limit:
                    break

                total += 1
                fname = func.getName()
                entry = str(func.getEntryPoint())

                try:
                    results = decompiler.decompileFunction(func, timeout, monitor)
                    if not results.decompileCompleted():
                        raise Exception(str(results.getErrorMessage()))

                    decomp_func = results.getDecompiledFunction()
                    c_code = decomp_func.getC() if decomp_func else None
                    if not c_code:
                        raise Exception("No decompiled code produced")

                    sections.append((entry, fname, str(func.getSignature()), c_code))
                    succeeded += 1
                except Exception as func_err:
                    failed.append({"name": fname, "address": entry,
                                   "error": str(func_err)})
        finally:
            decompiler.dispose()

        c_path = None
        if _DSH_OUT_PATH:
            c_path = _DSH_OUT_PATH + ".c"
            cfile = codecs.open(c_path, "w", "utf-8", "replace")
            try:
                cfile.write(u"/* Decompiled by DSH ghidra-core decompile_all.py */\n")
                cfile.write(u"/* Program: %s  total=%d succeeded=%d failed=%d */\n\n"
                            % (program.getName(), total, succeeded, len(failed)))
                for entry, fname, sig, c_code in sections:
                    cfile.write(u"/* ===== %s @ %s ===== */\n" % (fname, entry))
                    cfile.write(u"/* signature: %s */\n" % sig)
                    cfile.write(c_code)
                    if not c_code.endswith("\n"):
                        cfile.write(u"\n")
                    cfile.write(u"\n")
            finally:
                cfile.close()
        else:
            # No @out file: inline pseudocode into the JSON payload
            inline = []
            for entry, fname, sig, c_code in sections:
                inline.append({"name": fname, "address": entry,
                               "signature": sig, "c_code": c_code})

        result = {
            "status": "success",
            "total": total,
            "succeeded": succeeded,
            "failed": len(failed),
            "failed_functions": failed,
            "limit": limit,
            "limit_reached": limit is not None and total >= limit
        }
        if c_path:
            result["c_out"] = c_path
        else:
            result["functions"] = inline
        emit(result)

    except Exception as e:
        import traceback
        emit({"status": "error", "error": str(e),
              "traceback": traceback.format_exc()})


run()
