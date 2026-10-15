# Ghidra script to get disassembly for a function or address range
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

# CommentType compatibility: Ghidra >= 11 uses CommentType enum, older uses int
try:
    from ghidra.program.model.listing import CommentType
    EOL_COMMENT_TYPE = CommentType.EOL
except ImportError:
    from ghidra.program.model.listing import CodeUnit as _CU
    EOL_COMMENT_TYPE = _CU.EOL_COMMENT


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
        if not args:
            output_json({
                "status": "error",
                "error": "Usage: <function_name|address> [end_address] [max_instructions]"
            })
            return

        identifier = args[0]
        end_addr_str = args[1] if len(args) > 1 else None
        max_instructions = int(args[2]) if len(args) > 2 else 500

        listing = program.getListing()
        instructions = []

        # Check if this is a range (start-end) or function/single address
        if end_addr_str and end_addr_str.startswith("0x"):
            # Address range mode
            start_addr = toAddr(identifier)
            end_addr = toAddr(end_addr_str)

            if start_addr is None or end_addr is None:
                output_json({"status": "error", "error": "Invalid address range"})
                return

            inst_iter = listing.getInstructions(start_addr, True)
            count = 0
            while inst_iter.hasNext() and count < max_instructions:
                inst = inst_iter.next()
                if inst.getAddress().compareTo(end_addr) > 0:
                    break

                inst_info = {
                    "address": str(inst.getAddress()),
                    "mnemonic": inst.getMnemonicString(),
                    "operands": inst.toString().split(" ", 1)[1] if " " in inst.toString() else "",
                    "bytes": " ".join(["%02x" % (b & 0xff) for b in inst.getBytes()]),
                    "length": inst.getLength()
                }

                # Add flow info
                flows = inst.getFlows()
                if flows:
                    inst_info["flows_to"] = [str(f) for f in flows]

                instructions.append(inst_info)
                count += 1

            output_json({
                "status": "success",
                "mode": "range",
                "start_address": str(start_addr),
                "end_address": str(end_addr),
                "instruction_count": len(instructions),
                "instructions": instructions
            })
        else:
            # Function mode
            func = find_function(program, identifier)
            if func is None:
                output_json({"status": "error", "error": "Function not found: " + identifier})
                return

            body = func.getBody()
            inst_iter = listing.getInstructions(body, True)

            count = 0
            while inst_iter.hasNext() and count < max_instructions:
                inst = inst_iter.next()

                inst_info = {
                    "address": str(inst.getAddress()),
                    "mnemonic": inst.getMnemonicString(),
                    "operands": inst.toString().split(" ", 1)[1] if " " in inst.toString() else "",
                    "bytes": " ".join(["%02x" % (b & 0xff) for b in inst.getBytes()]),
                    "length": inst.getLength()
                }

                # Add comment if present
                comment = inst.getComment(EOL_COMMENT_TYPE)
                if comment:
                    inst_info["comment"] = comment

                # Add flow info
                flows = inst.getFlows()
                if flows:
                    inst_info["flows_to"] = [str(f) for f in flows]

                instructions.append(inst_info)
                count += 1

            output_json({
                "status": "success",
                "mode": "function",
                "function_name": func.getName(),
                "address": str(func.getEntryPoint()),
                "signature": str(func.getSignature()),
                "instruction_count": len(instructions),
                "truncated": count >= max_instructions,
                "instructions": instructions
            })

    except Exception as e:
        import traceback
        output_json({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

run()
