# Ghidra script to add or update comments at addresses
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
from ghidra.program.model.listing import CodeUnit

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
            output_json({"status": "error", "error": "No program loaded"})
            return

        args = _DSH_ARGS
        if len(args) < 2:
            output_json({
                "status": "error",
                "error": "Usage: <address> <comment> [comment_type]"
            })
            return

        address_str = args[0]
        comment_text = args[1]
        comment_type_str = args[2] if len(args) > 2 else "eol"

        # Map comment type string to Ghidra constant
        comment_types = {
            "eol": CodeUnit.EOL_COMMENT,
            "pre": CodeUnit.PRE_COMMENT,
            "post": CodeUnit.POST_COMMENT,
            "plate": CodeUnit.PLATE_COMMENT,
            "repeatable": CodeUnit.REPEATABLE_COMMENT
        }

        comment_type = comment_types.get(comment_type_str.lower())
        if comment_type is None:
            output_json({
                "status": "error",
                "error": "Invalid comment type. Use: eol, pre, post, plate, or repeatable"
            })
            return

        addr = toAddr(address_str)
        if addr is None:
            output_json({
                "status": "error",
                "error": "Invalid address: " + address_str
            })
            return

        listing = program.getListing()
        code_unit = listing.getCodeUnitAt(addr)

        if code_unit is None:
            # Try to get the code unit containing this address
            code_unit = listing.getCodeUnitContaining(addr)

        if code_unit is None:
            output_json({
                "status": "error",
                "error": "No code unit at address: " + address_str
            })
            return

        # Get old comment if any
        old_comment = code_unit.getComment(comment_type)

        # Set the new comment inside an explicit transaction
        tid = program.startTransaction("Add comment at " + address_str)
        success = False
        try:
            code_unit.setComment(comment_type, comment_text)
            success = True
        finally:
            program.endTransaction(tid, success)

        if not success:
            output_json({
                "status": "error",
                "error": "Failed to set comment (transaction failed)"
            })
            return

        # Get context info
        result = {
            "status": "success",
            "address": str(addr),
            "comment": comment_text,
            "comment_type": comment_type_str,
            "old_comment": old_comment
        }

        # Add instruction context if applicable
        inst = listing.getInstructionAt(addr)
        if inst:
            result["instruction"] = inst.toString()

        # Add function context if applicable
        fm = program.getFunctionManager()
        func = fm.getFunctionContaining(addr)
        if func:
            result["function"] = func.getName()

        output_json(result)

    except Exception as e:
        import traceback
        output_json({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

run()
