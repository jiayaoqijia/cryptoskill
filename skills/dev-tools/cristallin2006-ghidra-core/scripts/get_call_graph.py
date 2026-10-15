# Ghidra script to generate a caller/callee tree for a function
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

def get_call_graph(program, func, max_depth=3):
    """
    Generate a call graph for a function.

    Args:
        program: The Ghidra program
        func: The function to analyze
        max_depth: Maximum depth for recursive call graph (default 3)

    Returns:
        Dictionary containing callers and callees
    """
    from ghidra.util.task import ConsoleTaskMonitor
    monitor = ConsoleTaskMonitor()

    # Get functions that call this function (callers)
    callers = []
    for caller in func.getCallingFunctions(monitor):
        caller_info = {
            "name": caller.getName(),
            "address": str(caller.getEntryPoint()),
            "signature": str(caller.getSignature()),
            "is_external": caller.isExternal(),
            "is_thunk": caller.isThunk()
        }
        callers.append(caller_info)

    # Get functions that this function calls (callees)
    callees = []
    for callee in func.getCalledFunctions(monitor):
        callee_info = {
            "name": callee.getName(),
            "address": str(callee.getEntryPoint()),
            "signature": str(callee.getSignature()),
            "is_external": callee.isExternal(),
            "is_thunk": callee.isThunk()
        }
        callees.append(callee_info)

    return {
        "callers": callers,
        "callees": callees,
        "caller_count": len(callers),
        "callee_count": len(callees)
    }

def get_recursive_call_graph(program, func, depth=1, max_depth=2, visited=None):
    """
    Generate a recursive call graph with depth levels.

    Args:
        program: The Ghidra program
        func: The function to analyze
        depth: Current depth level
        max_depth: Maximum depth to traverse
        visited: Set of visited function names to avoid cycles

    Returns:
        Dictionary containing nested call graph
    """
    from ghidra.util.task import ConsoleTaskMonitor
    monitor = ConsoleTaskMonitor()

    if visited is None:
        visited = set()

    func_name = func.getName()
    if func_name in visited or depth > max_depth:
        return None

    visited.add(func_name)

    # Get callers recursively
    callers = []
    for caller in func.getCallingFunctions(monitor):
        caller_info = {
            "name": caller.getName(),
            "address": str(caller.getEntryPoint()),
            "depth": depth
        }
        if depth < max_depth and not caller.isExternal():
            nested = get_recursive_call_graph(program, caller, depth + 1, max_depth, visited.copy())
            if nested:
                caller_info["callers"] = nested.get("callers", [])
        callers.append(caller_info)

    # Get callees recursively
    callees = []
    for callee in func.getCalledFunctions(monitor):
        callee_info = {
            "name": callee.getName(),
            "address": str(callee.getEntryPoint()),
            "depth": depth
        }
        if depth < max_depth and not callee.isExternal():
            nested = get_recursive_call_graph(program, callee, depth + 1, max_depth, visited.copy())
            if nested:
                callee_info["callees"] = nested.get("callees", [])
        callees.append(callee_info)

    return {
        "callers": callers,
        "callees": callees
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

        # Get arguments
        args = _DSH_ARGS
        if not args:
            output_json({
                "status": "error",
                "error": "No function name or address specified"
            })
            return

        identifier = args[0]
        recursive = len(args) > 1 and args[1].lower() in ["recursive", "true", "1"]
        max_depth = 2
        if len(args) > 2:
            try:
                max_depth = int(args[2])
            except:
                pass

        # Find the function
        addr, func = find_address_or_function(program, identifier)
        if addr is None or func is None:
            output_json({
                "status": "error",
                "error": "Could not find function: " + identifier
            })
            return

        # Generate call graph
        if recursive:
            call_graph = get_recursive_call_graph(program, func, 1, max_depth)
        else:
            call_graph = get_call_graph(program, func)

        result = {
            "status": "success",
            "function": {
                "name": func.getName(),
                "address": str(func.getEntryPoint()),
                "signature": str(func.getSignature()),
                "size": func.getBody().getNumAddresses(),
                "is_external": func.isExternal(),
                "is_thunk": func.isThunk()
            },
            "recursive": recursive,
            "call_graph": call_graph
        }

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
