# Ghidra script to get basic blocks (control flow graph) for a function
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
from ghidra.program.model.block import BasicBlockModel
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
                "error": "Usage: <function_name|address>"
            })
            return

        identifier = args[0]

        func = find_function(program, identifier)
        if func is None:
            output_json({"status": "error", "error": "Function not found: " + identifier})
            return

        # Get basic blocks
        block_model = BasicBlockModel(program)
        listing = program.getListing()
        monitor = ConsoleTaskMonitor()

        blocks = []
        block_iter = block_model.getCodeBlocksContaining(func.getBody(), monitor)

        while block_iter.hasNext():
            block = block_iter.next()

            block_info = {
                "start": str(block.getFirstStartAddress()),
                "end": str(block.getMaxAddress()),
                "name": block.getName(),
                "size": block.getNumAddresses()
            }

            # Get successors (where control can flow to)
            successors = []
            dest_iter = block.getDestinations(monitor)
            while dest_iter.hasNext():
                dest = dest_iter.next()
                dest_addr = dest.getDestinationAddress()
                if dest_addr is not None:
                    succ_info = {
                        "address": str(dest_addr),
                        "type": str(dest.getFlowType())
                    }
                    successors.append(succ_info)
            block_info["successors"] = successors

            # Get predecessors (where control can come from)
            predecessors = []
            src_iter = block.getSources(monitor)
            while src_iter.hasNext():
                src = src_iter.next()
                src_addr = src.getSourceAddress()
                if src_addr is not None:
                    pred_info = {
                        "address": str(src_addr),
                        "type": str(src.getFlowType())
                    }
                    predecessors.append(pred_info)
            block_info["predecessors"] = predecessors

            # Get instructions in this block
            instructions = []
            inst_iter = listing.getInstructions(block, True)
            while inst_iter.hasNext():
                inst = inst_iter.next()
                instructions.append({
                    "address": str(inst.getAddress()),
                    "mnemonic": inst.getMnemonicString(),
                    "text": inst.toString()
                })
            block_info["instruction_count"] = len(instructions)
            block_info["instructions"] = instructions

            blocks.append(block_info)

        # Build edge list for graph visualization
        edges = []
        for block in blocks:
            for succ in block.get("successors", []):
                edges.append({
                    "from": block["start"],
                    "to": succ["address"],
                    "type": succ["type"]
                })

        output_json({
            "status": "success",
            "function_name": func.getName(),
            "address": str(func.getEntryPoint()),
            "block_count": len(blocks),
            "edge_count": len(edges),
            "basic_blocks": blocks,
            "edges": edges
        })

    except Exception as e:
        import traceback
        output_json({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

run()
