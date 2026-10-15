# Ghidra script to set/update function signature
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
from ghidra.program.model.data import PointerDataType
from ghidra.program.model.symbol import SourceType
from ghidra.app.cmd.function import ApplyFunctionSignatureCmd
from ghidra.app.util.parser import FunctionSignatureParser
from ghidra.program.model.listing import VariableStorage

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

def find_function(program, identifier):
    """Find a function by name or address."""
    fm = program.getFunctionManager()

    if identifier.startswith("0x") or identifier.startswith("0X"):
        try:
            addr = toAddr(identifier)
            func = fm.getFunctionAt(addr)
            if func:
                return func
            func = fm.getFunctionContaining(addr)
            if func:
                return func
        except:
            pass

    for func in fm.getFunctions(True):
        if func.getName() == identifier:
            return func

    for func in fm.getFunctions(True):
        if identifier.lower() in func.getName().lower():
            return func

    return None

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
                "error": "Usage: <function_name|address> <signature>"
            })
            return

        identifier = args[0]
        # Join remaining args in case signature had spaces
        signature_str = " ".join(args[1:])

        func = find_function(program, identifier)
        if func is None:
            output_json({"status": "error", "error": "Function not found: " + identifier})
            return

        old_signature = str(func.getSignature())

        # Parse the signature
        dtm = program.getDataTypeManager()

        try:
            parser = FunctionSignatureParser(dtm, None)
            new_sig = parser.parse(func.getSignature(), signature_str)

            if new_sig is None:
                output_json({
                    "status": "error",
                    "error": "Failed to parse signature: " + signature_str
                })
                return

            # Apply the new signature inside an explicit transaction
            cmd = ApplyFunctionSignatureCmd(
                func.getEntryPoint(),
                new_sig,
                SourceType.USER_DEFINED
            )

            tid = program.startTransaction("Set function signature")
            success = False
            applied = False
            try:
                applied = cmd.applyTo(program)
                success = applied
            finally:
                program.endTransaction(tid, success)

            if applied:
                output_json({
                    "status": "success",
                    "function_name": func.getName(),
                    "address": str(func.getEntryPoint()),
                    "old_signature": old_signature,
                    "new_signature": str(func.getSignature())
                })
            else:
                output_json({
                    "status": "error",
                    "error": "Failed to apply signature: " + str(cmd.getStatusMsg())
                })

        except Exception as parse_error:
            # Try a simpler approach - just set return type and parameters manually
            output_json({
                "status": "error",
                "error": "Signature parsing failed: " + str(parse_error),
                "hint": "Try a simpler signature like 'int function_name(int param1, char* param2)'"
            })

    except Exception as e:
        import traceback
        output_json({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

run()
