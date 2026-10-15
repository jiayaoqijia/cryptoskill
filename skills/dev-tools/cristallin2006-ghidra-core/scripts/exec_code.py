# Execute arbitrary Python 3 (PyGhidra) code against the current program
# @category DSH.Reverse
# @runtime PyGhidra
#
# Usage examples (contents of the code file passed as the first argument):
#   output_json({"status": "success", "funcs": fm.getFunctionCount()})
#   f = find_function("main"); output_json({"sig": str(f.getSignature())})
#   output_json({"blocks": [b.getName() for b in memory.getBlocks()]})
#
# Predefined names in the exec namespace: program, currentProgram, fm,
# listing, memory, toAddr, monitor, find_function(name_or_addr), output_json.

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
import traceback

_output_emitted = False

def output_json(data):
    """Write full JSON to the @out file if given, else print between markers."""
    global _output_emitted
    _output_emitted = True
    if _DSH_OUT_PATH:
        try:
            f = open(_DSH_OUT_PATH, "w")
            try:
                f.write(json.dumps(data))
            finally:
                f.close()
            count = 0
            for key in ("strings", "functions", "instructions", "results",
                        "imports", "symbols", "xrefs", "blocks", "classes",
                        "basic_blocks", "c_code", "bytes", "types"):
                if key in data and data[key] is not None:
                    v = data[key]
                    try:
                        count = len(v)
                    except TypeError:
                        count = 1
                    break
            summary = {
                "status": data.get("status", "success"),
                "out": _DSH_OUT_PATH,
                "count": count
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

def find_function(program, identifier):
    """Find a function by address (0x...), exact name, or name substring."""
    fm = program.getFunctionManager()

    ident = str(identifier)
    if ident.startswith("0x") or ident.startswith("0X"):
        try:
            addr = toAddr(ident)
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

def run():
    try:
        program = currentProgram
        if program is None:
            output_json({"status": "error", "error": "No program loaded"})
            return

        args = _DSH_ARGS
        if not args:
            output_json({
                "status": "error",
                "error": "Usage: <code_file.py>  (optionally preceded by @outfile)"
            })
            return

        code_path = str(args[0])
        try:
            f = open(code_path, "r")
            try:
                src = f.read()
            finally:
                f.close()
        except Exception as e:
            output_json({"status": "error",
                         "error": "cannot read code file %s: %s" % (code_path, e)})
            return

        try:
            mon = monitor
        except NameError:
            from ghidra.util.task import ConsoleTaskMonitor
            mon = ConsoleTaskMonitor()

        namespace = {
            "__builtins__": __builtins__,
            "program": program,
            "currentProgram": program,
            "fm": program.getFunctionManager(),
            "listing": program.getListing(),
            "memory": program.getMemory(),
            "toAddr": toAddr,
            "monitor": mon,
            "find_function": lambda ident: find_function(program, ident),
            "output_json": output_json,
        }

        exec(compile(src, code_path, "exec"), namespace)

        if not _output_emitted:
            output_json({"status": "success", "note": "no explicit output"})

    except Exception as e:
        output_json({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

run()
