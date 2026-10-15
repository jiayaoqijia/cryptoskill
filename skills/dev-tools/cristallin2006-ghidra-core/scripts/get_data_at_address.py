# Ghidra script to read data at an address with a given type
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

        args = _DSH_ARGS
        if not args:
            output_json({
                "status": "error",
                "error": "Usage: <address> [length|type] [format]"
            })
            return

        address_str = args[0]
        length_or_type = args[1] if len(args) > 1 else "32"
        format_type = args[2] if len(args) > 2 else "hex"

        addr = toAddr(address_str)
        if addr is None:
            output_json({"status": "error", "error": "Invalid address: " + address_str})
            return

        memory = program.getMemory()
        listing = program.getListing()
        dtm = program.getDataTypeManager()

        # Endianness of the target: all multi-byte decoding below is assembled
        # little-endian, so big-endian programs need their bytes reversed first.
        is_be = program.getLanguage().isBigEndian()

        result = {
            "status": "success",
            "address": str(addr),
            "endianness": "big" if is_be else "little"
        }

        # Check if a data type was specified
        data_types = {
            "byte": 1, "char": 1,
            "short": 2, "word": 2,
            "int": 4, "dword": 4, "long": 4, "float": 4,
            "longlong": 8, "qword": 8, "double": 8,
            "pointer": program.getDefaultPointerSize()
        }

        if length_or_type.lower() in data_types:
            # Read as a specific type
            type_name = length_or_type.lower()
            length = data_types[type_name]

            raw_bytes = []
            for i in range(length):
                try:
                    b = memory.getByte(addr.add(i))
                    raw_bytes.append(b & 0xff)
                except:
                    raw_bytes.append(0)

            # le_bytes[i] is the i-th least significant byte, whatever the target
            le_bytes = list(reversed(raw_bytes)) if is_be else raw_bytes

            result["type"] = type_name
            result["length"] = length
            result["bytes"] = " ".join(["%02x" % b for b in raw_bytes])

            # Interpret the value based on type
            if type_name in ["byte", "char"]:
                result["value"] = raw_bytes[0]
                if 32 <= raw_bytes[0] < 127:
                    result["char"] = chr(raw_bytes[0])
            elif type_name in ["short", "word"]:
                result["value"] = le_bytes[0] | (le_bytes[1] << 8)
                result["value_signed"] = result["value"] if result["value"] < 0x8000 else result["value"] - 0x10000
            elif type_name in ["int", "dword", "long"]:
                result["value"] = le_bytes[0] | (le_bytes[1] << 8) | (le_bytes[2] << 16) | (le_bytes[3] << 24)
                result["value_signed"] = result["value"] if result["value"] < 0x80000000 else result["value"] - 0x100000000
            elif type_name in ["longlong", "qword"]:
                value = 0
                for i in range(8):
                    value |= le_bytes[i] << (i * 8)
                result["value"] = value
            elif type_name == "float":
                import struct
                result["value"] = struct.unpack('>f' if is_be else '<f', bytes(bytearray(raw_bytes)))[0]
            elif type_name == "double":
                import struct
                result["value"] = struct.unpack('>d' if is_be else '<d', bytes(bytearray(raw_bytes)))[0]
            elif type_name == "pointer":
                value = 0
                for i in range(length):
                    value |= le_bytes[i] << (i * 8)
                result["value"] = "0x%x" % value
                # Try to resolve what the pointer points to
                ptr_addr = toAddr("0x%x" % value)
                if ptr_addr is not None:
                    func = program.getFunctionManager().getFunctionAt(ptr_addr)
                    if func:
                        result["points_to"] = {"type": "function", "name": func.getName()}
                    else:
                        symbol = program.getSymbolTable().getPrimarySymbol(ptr_addr)
                        if symbol:
                            result["points_to"] = {"type": str(symbol.getSymbolType()), "name": symbol.getName()}

        else:
            # Read raw bytes
            try:
                length = int(length_or_type)
            except:
                length = 32

            # Cap at reasonable limit
            length = min(length, 4096)

            raw_bytes = []
            for i in range(length):
                try:
                    b = memory.getByte(addr.add(i))
                    raw_bytes.append(b & 0xff)
                except:
                    break

            result["length"] = len(raw_bytes)

            if format_type == "hex":
                result["bytes"] = " ".join(["%02x" % b for b in raw_bytes])
            elif format_type == "ascii":
                result["bytes"] = " ".join(["%02x" % b for b in raw_bytes])
                ascii_str = ""
                for b in raw_bytes:
                    if 32 <= b < 127:
                        ascii_str += chr(b)
                    else:
                        ascii_str += "."
                result["ascii"] = ascii_str
            elif format_type == "string":
                # Try to read as null-terminated string
                string_bytes = []
                for b in raw_bytes:
                    if b == 0:
                        break
                    string_bytes.append(b)
                try:
                    result["string"] = bytes(bytearray(string_bytes)).decode('utf-8')
                except:
                    result["string"] = bytes(bytearray(string_bytes)).decode('latin-1')
                result["bytes"] = " ".join(["%02x" % b for b in string_bytes])

        # Check what's defined at this address
        data = listing.getDataAt(addr)
        if data:
            result["defined_data"] = {
                "type": str(data.getDataType()),
                "value": str(data.getValue()) if data.getValue() else None
            }

        inst = listing.getInstructionAt(addr)
        if inst:
            result["instruction"] = inst.toString()

        # Get memory block info
        block = memory.getBlock(addr)
        if block:
            result["memory_block"] = {
                "name": block.getName(),
                "permissions": {
                    "read": block.isRead(),
                    "write": block.isWrite(),
                    "execute": block.isExecute()
                }
            }

        output_json(result)

    except Exception as e:
        import traceback
        output_json({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

run()
