# Ghidra script to search for byte patterns/hex signatures
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


def _java_byte_array(values):
    """Build a Java byte[] from a list of Python ints (0..255 or signed)."""
    import jpype

    arr = jpype.JArray(jpype.JByte)(len(values))
    for index, value in enumerate(values):
        arr[index] = value - 256 if value > 127 else value
    return arr

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

def parse_byte_pattern(pattern_str):
    """
    Parse a byte pattern string into bytes and mask.

    Supports formats:
    - "48 8b 05" - space-separated hex
    - "488b05" - continuous hex
    - "48 ?? 05" - with wildcards
    - "48 8b ?5" - partial wildcards

    Returns: (bytes_list, mask_list) where mask is 0xff for exact match, 0x00 for wildcard
    """
    # Remove spaces and normalize
    pattern = pattern_str.replace(" ", "").lower()

    if len(pattern) % 2 != 0:
        raise ValueError("Pattern must have even number of hex characters")

    bytes_list = []
    mask_list = []

    for i in range(0, len(pattern), 2):
        byte_str = pattern[i:i+2]

        if byte_str == "??":
            bytes_list.append(0)
            mask_list.append(0x00)
        elif "?" in byte_str:
            # Partial wildcard (e.g., "?5" or "4?")
            if byte_str[0] == "?":
                bytes_list.append(int(byte_str[1], 16))
                mask_list.append(0x0f)
            else:
                bytes_list.append(int(byte_str[0], 16) << 4)
                mask_list.append(0xf0)
        else:
            bytes_list.append(int(byte_str, 16))
            mask_list.append(0xff)

    return bytes_list, mask_list

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
                "error": "Usage: <byte_pattern> [max_results] [start_address] [end_address]"
            })
            return

        pattern_str = args[0]
        max_results = int(args[1]) if len(args) > 1 else 100
        start_addr_str = args[2] if len(args) > 2 else None
        end_addr_str = args[3] if len(args) > 3 else None

        try:
            bytes_list, mask_list = parse_byte_pattern(pattern_str)
        except ValueError as e:
            output_json({"status": "error", "error": "Invalid pattern: " + str(e)})
            return

        # Convert to Java byte arrays. Jython's `from jarray import array` does not
        # exist under PyGhidra; jpype.JArray builds the same byte[] that
        # Memory.findBytes expects.
        bytes_array = _java_byte_array(bytes_list)
        mask_array = _java_byte_array(mask_list)

        memory = program.getMemory()

        # Determine search range
        if start_addr_str:
            start_addr = toAddr(start_addr_str)
        else:
            start_addr = memory.getMinAddress()

        if end_addr_str:
            end_addr = toAddr(end_addr_str)
        else:
            end_addr = memory.getMaxAddress()

        if start_addr is None or end_addr is None:
            output_json({"status": "error", "error": "Invalid address range"})
            return

        # Search for pattern
        results = []
        listing = program.getListing()
        fm = program.getFunctionManager()

        search_addr = start_addr
        while search_addr is not None and len(results) < max_results:
            if search_addr.compareTo(end_addr) > 0:
                break

            # Search for the pattern
            found_addr = memory.findBytes(
                search_addr,
                bytes_array,
                mask_array,
                True,  # forward
                None   # monitor
            )

            if found_addr is None or found_addr.compareTo(end_addr) > 0:
                break

            # Get context for the match
            result_info = {
                "address": str(found_addr),
                "offset": found_addr.getOffset()
            }

            # Check if in a function
            func = fm.getFunctionContaining(found_addr)
            if func:
                result_info["function"] = func.getName()
                result_info["function_offset"] = found_addr.subtract(func.getEntryPoint())

            # Check if it's an instruction
            inst = listing.getInstructionAt(found_addr)
            if inst:
                result_info["instruction"] = inst.toString()

            # Get the actual bytes at this location
            actual_bytes = []
            for i in range(len(bytes_list)):
                try:
                    b = memory.getByte(found_addr.add(i))
                    actual_bytes.append("%02x" % (b & 0xff))
                except:
                    actual_bytes.append("??")
            result_info["matched_bytes"] = " ".join(actual_bytes)

            # Get memory block info
            block = memory.getBlock(found_addr)
            if block:
                result_info["memory_block"] = block.getName()

            results.append(result_info)

            # Move to next address
            search_addr = found_addr.add(1)

        output_json({
            "status": "success",
            "pattern": pattern_str,
            "pattern_length": len(bytes_list),
            "search_range": {
                "start": str(start_addr),
                "end": str(end_addr)
            },
            "result_count": len(results),
            "truncated": len(results) >= max_results,
            "matches": results
        })

    except Exception as e:
        import traceback
        output_json({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

run()
