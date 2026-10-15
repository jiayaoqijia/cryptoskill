# Ghidra script to list all functions in a program
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

        # Get arguments: [filter_pattern, limit, offset]
        args = _DSH_ARGS
        filter_pattern = None
        limit = 100  # Default limit to prevent massive responses
        offset = 0

        if args:
            # First arg can be filter pattern or "limit:N" or "offset:N"
            for arg in args:
                if arg.startswith("limit:"):
                    limit = int(arg.split(":")[1])
                elif arg.startswith("offset:"):
                    offset = int(arg.split(":")[1])
                elif arg != "":
                    filter_pattern = arg

        filter_regex = re.compile(filter_pattern) if filter_pattern else None

        # Collect functions
        fm = program.getFunctionManager()
        functions = []
        total_count = 0
        skipped = 0

        for func in fm.getFunctions(True):  # True = forward order
            name = func.getName()

            # Apply filter if specified
            if filter_regex and not filter_regex.search(name):
                continue

            total_count += 1

            # Handle offset
            if skipped < offset:
                skipped += 1
                continue

            # Handle limit
            if len(functions) >= limit:
                continue  # Keep counting total but don't add more

            func_info = {
                "name": name,
                "address": str(func.getEntryPoint()),
                "size": func.getBody().getNumAddresses(),
                "signature": str(func.getSignature()),
                "calling_convention": str(func.getCallingConventionName()),
                "is_external": func.isExternal(),
                "is_thunk": func.isThunk()
            }

            # Add parameter info
            params = []
            for param in func.getParameters():
                params.append({
                    "name": param.getName(),
                    "type": str(param.getDataType()),
                    "ordinal": param.getOrdinal()
                })
            func_info["parameters"] = params

            functions.append(func_info)

        output_json({
            "status": "success",
            "total_count": total_count,
            "returned_count": len(functions),
            "offset": offset,
            "limit": limit,
            "has_more": total_count > offset + len(functions),
            "functions": functions
        })

    except Exception as e:
        output_json({
            "status": "error",
            "error": str(e)
        })

# Run the script
run()
