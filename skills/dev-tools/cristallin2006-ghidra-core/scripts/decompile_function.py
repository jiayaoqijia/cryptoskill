# Ghidra script to decompile a function to C pseudocode
# @category DSH.Reverse
# @runtime PyGhidra

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
import re
from ghidra.app.decompiler import DecompInterface, DecompileOptions
from ghidra.util.task import ConsoleTaskMonitor

def output_json(data):
    """Write full JSON to the @out file if given, else print between markers."""
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
                        "basic_blocks", "c_code", "bytes"):
                if key in data and data[key] is not None:
                    v = data[key]
                    try:
                        count = len(v)
                    except TypeError:
                        count = 1
                    break
            if "string_count" in data:
                count = data["string_count"]
            elif "function_count" in data:
                count = data["function_count"]
            elif "decompiled_count" in data:
                count = data["decompiled_count"]
            elif "instruction_count" in data:
                count = data["instruction_count"]
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
    """
    Find a function by name or address.

    Args:
        program: The Ghidra program
        identifier: Function name or address string (0x...)

    Returns:
        Function object or None
    """
    fm = program.getFunctionManager()

    # Try as address first
    if identifier.startswith("0x") or identifier.startswith("0X"):
        try:
            addr = toAddr(identifier)
            func = fm.getFunctionAt(addr)
            if func:
                return func
            # Try containing function
            func = fm.getFunctionContaining(addr)
            if func:
                return func
        except:
            pass

    # Try as function name
    for func in fm.getFunctions(True):
        if func.getName() == identifier:
            return func

    # Try partial match
    for func in fm.getFunctions(True):
        if identifier.lower() in func.getName().lower():
            return func

    return None

def split_identifiers(args):
    """Split script args into one or more function identifiers.

    Each decompile run costs a fresh JVM start under PyGhidra, so a caller that wants a
    dozen functions should not be made to launch a dozen processes.  Accept the same
    separators as the plugin's BridgeDecompile (comma, semicolon, whitespace) and keep
    the single-identifier case behaving exactly as before.
    """
    out = []
    for chunk in args:
        for part in re.split(r"[,;\s]+", str(chunk)):
            part = part.strip()
            if part and part not in out:
                out.append(part)
    return out


def decompile_one(program, decompiler, identifier, timeout=60):
    """Decompile one function; return its result dict (never raises)."""
    func = find_function(program, identifier)
    if func is None:
        return {"status": "error", "error": "Function not found: " + identifier,
                "requested": identifier}

    monitor = ConsoleTaskMonitor()
    try:
        results = decompiler.decompileFunction(func, timeout, monitor)
    except Exception as exc:
        return {"status": "error", "error": "decompile failed: " + str(exc),
                "requested": identifier}

    if not results.decompileCompleted():
        return {"status": "error",
                "error": "Decompilation failed: " + str(results.getErrorMessage()),
                "requested": identifier}

    decomp_func = results.getDecompiledFunction()
    c_code = decomp_func.getC() if decomp_func else None
    if not c_code:
        return {"status": "error", "error": "No decompiled code produced",
                "requested": identifier}

    local_vars = []
    high_func = results.getHighFunction()
    if high_func:
        local_symbols = high_func.getLocalSymbolMap()
        if local_symbols:
            for symbol in local_symbols.getSymbols():
                var_info = {
                    "name": symbol.getName(),
                    "type": str(symbol.getDataType()),
                    "size": symbol.getSize(),
                }
                storage = symbol.getStorage()
                if storage:
                    var_info["storage"] = str(storage)
                local_vars.append(var_info)

    return {
        "status": "success",
        "requested": identifier,
        "function_name": func.getName(),
        "address": str(func.getEntryPoint()),
        "signature": str(func.getSignature()),
        "c_code": c_code,
        "local_variables": local_vars,
    }


def run():
    """Main script entry point."""
    try:
        program = currentProgram
        if program is None:
            output_json({
                "status": "error",
                "error": "No program loaded"
            })
            return

        identifiers = split_identifiers(_DSH_ARGS)
        if not identifiers:
            output_json({
                "status": "error",
                "error": "No function specified. Provide one or more function names or "
                         "addresses, separated by commas or spaces."
            })
            return

        # Initialize decompiler once for the whole batch: the DecompInterface is the
        # expensive part, and re-opening it per function is what made batching pointless.
        decompiler = DecompInterface()
        options = DecompileOptions()
        decompiler.setOptions(options)

        if not decompiler.openProgram(program):
            output_json({
                "status": "error",
                "error": "Failed to initialize decompiler"
            })
            return

        try:
            results = [decompile_one(program, decompiler, ident)
                       for ident in identifiers]
        finally:
            decompiler.dispose()

        ok = [r for r in results if r.get("status") == "success"]
        payload = {
            "status": "success" if ok else "error",
            "requested_count": len(identifiers),
            "decompiled_count": len(ok),
            "functions": results,
        }
        # Preserve the single-function shape so existing callers keep working.
        if len(results) == 1:
            payload.update(results[0])
        else:
            payload["function_name"] = ", ".join(r.get("function_name", "?") for r in ok)
            payload["address"] = ", ".join(r.get("address", "?") for r in ok)
            payload["c_code"] = "\n\n".join(
                "/* ===== %s @ %s ===== */\n%s" % (r.get("function_name"), r.get("address"),
                                                  r.get("c_code"))
                for r in ok)
            payload["local_variables"] = []
            if not ok:
                payload["error"] = "; ".join(
                    "%s: %s" % (r.get("requested"), r.get("error")) for r in results)

        output_json(payload)

    except Exception as e:
        import traceback
        output_json({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

# Run the script
run()
