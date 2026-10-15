# Ghidra script to rename a symbol (function, variable, label)
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
from ghidra.program.model.symbol import SourceType

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
                "error": "Usage: <address_or_current_name> <new_name>"
            })
            return

        identifier = args[0]
        new_name = args[1]

        fm = program.getFunctionManager()
        symbol_table = program.getSymbolTable()

        old_name = None
        symbol_type = None
        address = None

        tid = program.startTransaction("Rename symbol " + identifier)
        success = False
        try:
            # Try to find as address first. Accept both 0x-prefixed and bare hex,
            # since Ghidra prints addresses padded to the language's width
            # (e.g. 00102ae0), and a bare address must not fall through to a
            # symbol-name lookup that can never match.
            if re.match(r"^(0[xX])?[0-9a-fA-F]+$", identifier):
                try:
                    addr = toAddr(identifier if identifier.lower().startswith("0x")
                                  else "0x" + identifier)
                except Exception:
                    addr = None
                if addr is not None:
                    # Check if it's a function, else the function containing it
                    func = fm.getFunctionAt(addr) or fm.getFunctionContaining(addr)
                    if func:
                        old_name = func.getName()
                        func.setName(new_name, SourceType.USER_DEFINED)
                        symbol_type = "function"
                        address = str(func.getEntryPoint())
                    else:
                        # Try to rename the primary symbol at this address
                        symbol = symbol_table.getPrimarySymbol(addr)
                        if symbol:
                            old_name = symbol.getName()
                            symbol.setName(new_name, SourceType.USER_DEFINED)
                            symbol_type = str(symbol.getSymbolType())
                            address = str(addr)

            # Fall back to name lookup when the address path found nothing --
            # this also covers symbols whose NAME is pure hex ("cafe", "dead").
            if old_name is None:
                # Try as function name
                for func in fm.getFunctions(True):
                    if func.getName() == identifier:
                        old_name = func.getName()
                        address = str(func.getEntryPoint())
                        func.setName(new_name, SourceType.USER_DEFINED)
                        symbol_type = "function"
                        break

                # Try as symbol name if not found
                if old_name is None:
                    symbols = list(symbol_table.getSymbols(identifier))
                    if symbols:
                        symbol = symbols[0]
                        old_name = symbol.getName()
                        address = str(symbol.getAddress())
                        symbol.setName(new_name, SourceType.USER_DEFINED)
                        symbol_type = str(symbol.getSymbolType())

            success = old_name is not None
        finally:
            program.endTransaction(tid, success)

        if old_name is None:
            output_json({
                "status": "error",
                "error": "Symbol not found: " + identifier
            })
            return

        output_json({
            "status": "success",
            "old_name": old_name,
            "new_name": new_name,
            "address": address,
            "symbol_type": symbol_type
        })

    except Exception as e:
        import traceback
        output_json({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

run()
