# List functions with zero call-site references (hidden "second function" flag
# hunting), optionally filtered by call-graph reachability from a root.
# @category DSH.Reverse
# @runtime PyGhidra
#
# Dual-mode script:
#   daemon (primary):
#     python rpc_driver.py exec-code <binary> <this file>
#     python rpc_driver.py "@<out.json>" exec-code <binary> <this file>
#     (rpc_driver's own @out writes the daemon JSON reply to disk; exec-code
#     cannot forward script args, so in daemon mode options come from the
#     DSH_UNREF_ARGS env var -- it must be exported BEFORE the daemon starts,
#     e.g. DSH_UNREF_ARGS='--reachable-from main' python rpc_driver.py ensure ...)
#   legacy (driver.py exec):
#     driver.py exec <binary> unreferenced_funcs.py ["@<out>"] [options]
#
# Options:
#   --reachable-from <name|0xaddr>   also BFS the call graph from this root
#                                    (e.g. main) and report unreachable funcs
#   --include-roots                  keep entry/export roots in the list
#   --help                           print this usage as JSON
#
# Output: JSON with unreferenced[] (zero caller functions, thunks/externals/
# entry-export roots excluded unless --include-roots) and, when requested,
# reachability{reachable_count, unreachable[]}. Caveat: indirect calls
# (call reg / vtables / callbacks) leave no call xref, so a "zero-caller"
# function may still be invoked indirectly -- verify before concluding dead.

import sys as _sys

# dsh family convention: force UTF-8 on both streams (cp936 console mojibake
# lesson). Guarded: inside the rpc daemon the streams may not be reconfigurable.
for _s in (_sys.stdout, _sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# --- DSH @out support (self-contained, no cross-script imports) ---
# If the first script argument starts with '@', it is popped and treated as an
# output file path: the full JSON payload is written there, and stdout only
# carries a short status summary between the markers.
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

import json
import os
import shlex
import traceback

_USAGE = (
    "unreferenced_funcs.py [@out] [--reachable-from <name|0xaddr>] "
    "[--include-roots] [--help]; daemon mode: options via DSH_UNREF_ARGS env "
    "(set before daemon start)"
)


def _emit(data):
    """Daemon exec-code: hand the payload to the injected output_json (the last
    call wins). Legacy/direct: honor @out, else print between markers."""
    try:
        output_json  # noqa: F821 - injected by exec-code / exec_code.py
    except NameError:
        pass
    else:
        output_json(data)  # noqa: F821
        return
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
                "count": data.get("unreferenced_count", 0),
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


def _parse_args(argv):
    """Manual parse (argparse would raise SystemExit inside exec'd code).
    Returns (opts, error)."""
    opts = {"reachable_from": None, "include_roots": False, "help": False}
    i = 0
    while i < len(argv):
        a = str(argv[i])
        if a in ("--help", "-h"):
            opts["help"] = True
        elif a == "--reachable-from":
            if i + 1 >= len(argv):
                return None, "--reachable-from needs a function name or 0x address"
            opts["reachable_from"] = str(argv[i + 1])
            i += 1
        elif a == "--include-roots":
            opts["include_roots"] = True
        else:
            return None, "unknown argument: %s (usage: %s)" % (a, _USAGE)
        i += 1
    return opts, None


def _get_args():
    """Legacy mode: script args (after @out extraction). Daemon mode: exec-code
    forwards no script args, so fall back to the DSH_UNREF_ARGS env var."""
    if _DSH_ARGS:
        return _DSH_ARGS
    env = os.environ.get("DSH_UNREF_ARGS", "").strip()
    if env:
        try:
            return shlex.split(env)
        except ValueError:
            return env.split()
    return []


def _find_function(program, ident):
    """0x address -> exact name -> name substring."""
    fm = program.getFunctionManager()
    ident = str(ident)
    if ident.lower().startswith("0x"):
        try:
            addr = program.getAddressFactory().getAddress(ident)
            func = fm.getFunctionAt(addr)
            if func:
                return func
            func = fm.getFunctionContaining(addr)
            if func:
                return func
        except Exception:
            pass
    for func in fm.getFunctions(True):
        if func.getName() == ident:
            return func
    for func in fm.getFunctions(True):
        if ident.lower() in func.getName().lower():
            return func
    return None


def _thunk_target(func):
    """Resolve one thunk hop to the real function, or None."""
    try:
        if func.isThunk():
            return func.getThunkedFunction(False)
    except Exception:
        pass
    return None


def run():
    try:
        try:
            prog = program  # noqa: F821 - exec-code namespace
        except NameError:
            prog = currentProgram  # noqa: F821 - legacy GhidraScript global
        if prog is None:
            _emit({"status": "error", "error": "No program loaded"})
            return

        try:
            mon = monitor  # noqa: F821
        except NameError:
            from ghidra.util.task import ConsoleTaskMonitor
            mon = ConsoleTaskMonitor()

        opts, err = _parse_args(_get_args())
        if err:
            _emit({"status": "error", "error": err, "usage": _USAGE})
            return
        if opts["help"]:
            _emit({"status": "success", "usage": _USAGE, "doc": __doc__})
            return

        fm = prog.getFunctionManager()
        st = prog.getSymbolTable()

        # thunk maps so call edges through thunks count for the real target
        thunk_to_target = {}
        target_to_thunks = {}
        all_funcs = []
        for func in fm.getFunctions(True):
            all_funcs.append(func)
            tgt = _thunk_target(func)
            if tgt is not None:
                thunk_to_target[func.getEntryPoint().getOffset()] = tgt
                target_to_thunks.setdefault(
                    tgt.getEntryPoint().getOffset(), []).append(func)

        def callers_of(func):
            callers = set()
            for c in func.getCallingFunctions(mon):
                tgt = thunk_to_target.get(c.getEntryPoint().getOffset())
                callers.add(tgt if tgt is not None else c)
            # a thunk forwarding TO func: its callers are func's callers too
            for thunk_fn in target_to_thunks.get(
                    func.getEntryPoint().getOffset(), []):
                for c in thunk_fn.getCallingFunctions(mon):
                    callers.add(c)
            return callers

        skipped = {"thunks": 0, "externals": 0}
        roots = []
        unreferenced = []
        for func in all_funcs:
            if func.isThunk():
                skipped["thunks"] += 1
                continue
            if func.isExternal():
                skipped["externals"] += 1
                continue
            ep = func.getEntryPoint()
            is_root = st.isExternalEntryPoint(ep)
            rec = {
                "name": func.getName(),
                "address": str(ep),
                "size": int(func.getBody().getNumAddresses()),
            }
            if is_root:
                rec["kind"] = "entry_or_export"
                roots.append(rec)
                if not opts["include_roots"]:
                    continue
            if len(callers_of(func)) == 0:
                unreferenced.append(rec)

        result = {
            "status": "success",
            "program": prog.getName(),
            "total_functions": fm.getFunctionCount(),
            "functions_enumerated": len(all_funcs),
            "skipped": skipped,
            "roots_excluded": roots,
            "unreferenced_count": len(unreferenced),
            "unreferenced": unreferenced,
            "caveat": ("zero-caller only means no DIRECT call xref; indirect "
                       "calls (call reg, vtables, TLS callbacks, exception "
                       "handlers) leave no xref -- verify before concluding "
                       "dead code"),
        }

        if opts["reachable_from"]:
            root_fn = _find_function(prog, opts["reachable_from"])
            if root_fn is None:
                _emit({"status": "error",
                       "error": "reachable-from root not found: %s"
                                % opts["reachable_from"]})
                return
            seen = set()
            queue = [root_fn]
            while queue:
                f = queue.pop()
                key = f.getEntryPoint().getOffset()
                if key in seen:
                    continue
                seen.add(key)
                try:
                    for callee in f.getCalledFunctions(mon):
                        tgt = thunk_to_target.get(
                            callee.getEntryPoint().getOffset())
                        t = tgt if tgt is not None else callee
                        if t.isExternal():
                            continue
                        queue.append(t)
                except Exception:
                    pass
            unreachable = []
            for func in all_funcs:
                if func.isThunk() or func.isExternal():
                    continue
                if st.isExternalEntryPoint(func.getEntryPoint()):
                    continue
                if func.getEntryPoint().getOffset() not in seen:
                    unreachable.append({
                        "name": func.getName(),
                        "address": str(func.getEntryPoint()),
                        "size": int(func.getBody().getNumAddresses()),
                    })
            result["reachability"] = {
                "root": root_fn.getName(),
                "root_address": str(root_fn.getEntryPoint()),
                "reachable_count": len(seen),
                "unreachable_count": len(unreachable),
                "unreachable": unreachable,
            }

        _emit(result)

    except Exception as e:
        _emit({"status": "error", "error": str(e),
               "traceback": traceback.format_exc()})


run()
