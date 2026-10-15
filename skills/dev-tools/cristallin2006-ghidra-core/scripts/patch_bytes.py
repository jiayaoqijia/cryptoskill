# Ghidra script to patch binary bytes at a given address
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

def parse_hex_bytes(hex_string):
    """
    Parse hex string into byte array.

    Supports formats:
    - "48 8b 05" - space-separated hex
    - "488b05" - continuous hex

    Returns: list of byte values (0-255)
    """
    # Remove spaces and normalize
    hex_str = hex_string.replace(" ", "").lower()

    if len(hex_str) % 2 != 0:
        raise ValueError("Hex string must have even number of characters")

    bytes_list = []
    for i in range(0, len(hex_str), 2):
        byte_str = hex_str[i:i+2]
        try:
            byte_val = int(byte_str, 16)
            if byte_val < 0 or byte_val > 255:
                raise ValueError("Byte value out of range: " + byte_str)
            bytes_list.append(byte_val)
        except ValueError:
            raise ValueError("Invalid hex byte: " + byte_str)

    return bytes_list

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
                "error": "Usage: <address> <hex_bytes>"
            })
            return

        address_str = args[0]
        hex_bytes_str = args[1]

        # Validate and parse address
        addr = toAddr(address_str)
        if addr is None:
            output_json({
                "status": "error",
                "error": "Invalid address: " + address_str
            })
            return

        # Validate and parse hex bytes
        try:
            new_bytes = parse_hex_bytes(hex_bytes_str)
        except ValueError as e:
            output_json({
                "status": "error",
                "error": "Invalid hex bytes: " + str(e)
            })
            return

        if len(new_bytes) == 0:
            output_json({
                "status": "error",
                "error": "No bytes to write"
            })
            return

        memory = program.getMemory()

        # Check if address range is valid and writable
        end_addr = addr.add(len(new_bytes) - 1)
        if not memory.contains(addr):
            output_json({
                "status": "error",
                "error": "Address not in memory: " + address_str
            })
            return

        if not memory.contains(end_addr):
            output_json({
                "status": "error",
                "error": "Address range exceeds memory bounds (trying to write %d bytes)" % len(new_bytes)
            })
            return

        block = memory.getBlock(addr)
        if block is None:
            output_json({
                "status": "error",
                "error": "No memory block contains " + address_str
            })
            return
        # A code block is normally flagged non-writable, which is what a binary
        # patch has to overcome -- that flag is a permission, not a protection
        # (its backing bytes are already loaded as read-write). Grant it here and
        # restore it in the finally clause so the change is not left behind.
        granted_write = False
        if not block.isWrite():
            granted_write = True

        # Read old bytes before patching
        old_bytes = []
        for i in range(len(new_bytes)):
            try:
                b = memory.getByte(addr.add(i))
                old_bytes.append(b & 0xff)
            except Exception as e:
                output_json({
                    "status": "error",
                    "error": "Failed to read old bytes at offset %d: %s" % (i, str(e))
                })
                return

        # Start a transaction for writing
        transaction_id = program.startTransaction("Patch bytes at " + address_str)
        success = False
        cleared_units = 0

        try:
            if granted_write:
                block.setWrite(True)

            # Ghidra refuses a memory change that conflicts with a decoded
            # instruction ("Memory change conflicts with instruction at ..."), so
            # drop the code units covering the patch range first. Only the covered
            # span is cleared: an instruction that merely starts inside the range
            # is truncated rather than removed wholesale.
            listing = program.getListing()
            patch_end = addr.add(len(new_bytes) - 1)
            occupied = []
            for i in range(len(new_bytes)):
                cu = listing.getCodeUnitAt(addr.add(i))
                if cu is not None and cu not in occupied:
                    occupied.append(cu)

            for cu in occupied:
                start = cu.getMinAddress()
                end = cu.getMaxAddress()
                truncated_start = start if start.compareTo(addr) < 0 else addr
                truncated_end = end if end.compareTo(patch_end) > 0 else patch_end
                listing.clearCodeUnits(truncated_start, truncated_end, False)
                cleared_units += 1

            # Write new bytes; JPype needs a signed Java byte (0-255 overflows).
            for i, byte_val in enumerate(new_bytes):
                try:
                    signed = byte_val - 256 if byte_val > 127 else byte_val
                    memory.setByte(addr.add(i), signed)
                except Exception as e:
                    raise Exception("Failed to write byte at offset %d: %s" % (i, str(e)))

            success = True

        finally:
            if granted_write:
                try:
                    block.setWrite(False)
                except Exception:
                    pass
            program.endTransaction(transaction_id, success)

        if not success:
            output_json({
                "status": "error",
                "error": "Failed to write bytes (transaction failed)"
            })
            return

        # Verify the write by reading back
        verify_bytes = []
        for i in range(len(new_bytes)):
            b = memory.getByte(addr.add(i))
            verify_bytes.append(b & 0xff)

        # Build result
        result = {
            "status": "success",
            "address": str(addr),
            "bytes_written": len(new_bytes),
            "old_bytes": " ".join(["%02x" % b for b in old_bytes]),
            "new_bytes": " ".join(["%02x" % b for b in new_bytes]),
            "verified_bytes": " ".join(["%02x" % b for b in verify_bytes]),
            "memory_block": str(block.getName()),
            "instructions_cleared": cleared_units,
            "write_permission_granted": granted_write
        }

        # Add context information
        listing = program.getListing()

        # Check if this affects an instruction
        inst = listing.getInstructionContaining(addr)
        if inst:
            result["affected_instruction"] = {
                "address": str(inst.getAddress()),
                "original": inst.toString()
            }

        # Check if in a function
        fm = program.getFunctionManager()
        func = fm.getFunctionContaining(addr)
        if func:
            result["function"] = func.getName()
            result["function_offset"] = addr.subtract(func.getEntryPoint())

        # Add memory block info
        if block:
            result["memory_block"] = block.getName()

        output_json(result)

    except Exception as e:
        import traceback
        output_json({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

run()
