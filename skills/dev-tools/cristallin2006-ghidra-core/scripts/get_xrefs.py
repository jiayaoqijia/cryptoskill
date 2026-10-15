# Ghidra script to get cross-references to/from an address
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

def find_address_or_function(program, identifier):
    """
    Find an address by parsing string or looking up function name.

    Args:
        program: The Ghidra program
        identifier: Address string (0x...) or function name

    Returns:
        Tuple of (Address, Function or None)
    """
    fm = program.getFunctionManager()

    # Try as address first
    if identifier.startswith("0x") or identifier.startswith("0X"):
        try:
            addr = toAddr(identifier)
            func = fm.getFunctionContaining(addr)
            return (addr, func)
        except:
            pass

    # Try as function name
    for func in fm.getFunctions(True):
        if func.getName() == identifier:
            return (func.getEntryPoint(), func)

    # Try partial match
    for func in fm.getFunctions(True):
        if identifier.lower() in func.getName().lower():
            return (func.getEntryPoint(), func)

    return (None, None)

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

        # Get arguments
        args = _DSH_ARGS
        if not args:
            output_json({
                "status": "error",
                "error": "No address or function specified"
            })
            return

        identifier = args[0]
        direction = args[1] if len(args) > 1 else "both"

        # Find the address
        addr, func = find_address_or_function(program, identifier)
        if addr is None:
            output_json({
                "status": "error",
                "error": "Could not find: " + identifier
            })
            return

        fm = program.getFunctionManager()
        xrefs = []

        # Get references TO this address
        if direction in ["to", "both"]:
            for ref in getReferencesTo(addr):
                from_addr = ref.getFromAddress()
                from_func = fm.getFunctionContaining(from_addr)

                xref_info = {
                    "direction": "to",
                    "from_address": str(from_addr),
                    "to_address": str(addr),
                    "type": str(ref.getReferenceType()),
                    "is_call": ref.getReferenceType().isCall(),
                    "is_jump": ref.getReferenceType().isJump(),
                    "is_data": ref.getReferenceType().isData()
                }
                if from_func:
                    xref_info["from_function"] = from_func.getName()
                if func:
                    xref_info["to_function"] = func.getName()
                xrefs.append(xref_info)

        # Get references FROM this address
        if direction in ["from", "both"]:
            for ref in getReferencesFrom(addr):
                to_addr = ref.getToAddress()
                to_func = fm.getFunctionContaining(to_addr)

                xref_info = {
                    "direction": "from",
                    "from_address": str(addr),
                    "to_address": str(to_addr),
                    "type": str(ref.getReferenceType()),
                    "is_call": ref.getReferenceType().isCall(),
                    "is_jump": ref.getReferenceType().isJump(),
                    "is_data": ref.getReferenceType().isData()
                }
                if func:
                    xref_info["from_function"] = func.getName()
                if to_func:
                    xref_info["to_function"] = to_func.getName()
                xrefs.append(xref_info)

        # If we have a function, also get calling/called functions
        calling_functions = []
        called_functions = []
        if func:
            try:
                from ghidra.util.task import ConsoleTaskMonitor
                monitor = ConsoleTaskMonitor()

                for caller in func.getCallingFunctions(monitor):
                    calling_functions.append({
                        "name": caller.getName(),
                        "address": str(caller.getEntryPoint())
                    })

                for callee in func.getCalledFunctions(monitor):
                    called_functions.append({
                        "name": callee.getName(),
                        "address": str(callee.getEntryPoint())
                    })
            except:
                pass

        result = {
            "status": "success",
            "target": identifier,
            "address": str(addr),
            "function": func.getName() if func else None,
            "direction": direction,
            "xref_count": len(xrefs),
            "xrefs": xrefs
        }

        if func:
            result["calling_functions"] = calling_functions
            result["called_functions"] = called_functions

        output_json(result)

    except Exception as e:
        import traceback
        output_json({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

# Run the script
run()
