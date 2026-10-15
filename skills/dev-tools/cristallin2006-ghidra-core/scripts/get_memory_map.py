# Ghidra script to get memory map (sections, permissions, addresses)
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

def run():
    """Main script entry point."""
    try:
        program = currentProgram
        if program is None:
            output_json({"status": "error", "error": "No program loaded"})
            return

        memory = program.getMemory()
        blocks = []

        for block in memory.getBlocks():
            block_info = {
                "name": block.getName(),
                "start": str(block.getStart()),
                "end": str(block.getEnd()),
                "size": block.getSize(),
                "permissions": {
                    "read": block.isRead(),
                    "write": block.isWrite(),
                    "execute": block.isExecute()
                },
                "type": str(block.getType()),
                "is_initialized": block.isInitialized(),
                "is_mapped": block.isMapped(),
                "is_loaded": block.isLoaded(),
                "is_overlay": block.isOverlay()
            }

            # Get source info if available
            source = block.getSourceName()
            if source:
                block_info["source"] = source

            # Get comment if any
            comment = block.getComment()
            if comment:
                block_info["comment"] = comment

            blocks.append(block_info)

        # Get image base
        image_base = program.getImageBase()

        # Get address spaces
        address_factory = program.getAddressFactory()
        address_spaces = []
        for space in address_factory.getAddressSpaces():
            space_info = {
                "name": space.getName(),
                "type": str(space.getType()),
                "size": space.getSize(),
                "is_memory_space": space.isMemorySpace(),
                "is_loaded_memory_space": space.isLoadedMemorySpace()
            }
            address_spaces.append(space_info)

        output_json({
            "status": "success",
            "image_base": str(image_base),
            "total_memory_size": memory.getSize(),
            "block_count": len(blocks),
            "memory_blocks": blocks,
            "address_spaces": address_spaces
        })

    except Exception as e:
        import traceback
        output_json({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

run()
