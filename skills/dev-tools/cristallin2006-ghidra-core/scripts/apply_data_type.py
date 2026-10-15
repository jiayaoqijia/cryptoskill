# Apply a data type (e.g. a struct from apply_c_types.py) at an address
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
            summary = {
                "status": data.get("status", "success"),
                "out": _DSH_OUT_PATH,
                "count": data.get("size", 0)
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

def find_data_type(dtm, name):
    """Exact-path lookup first, then a case-insensitive name match across all
    categories (longest-path wins ties by first-seen order)."""
    dt = dtm.getDataType(name)
    if dt is not None:
        return dt, "exact"

    lowered = name.lower()
    it = dtm.getAllDataTypes()
    while it.hasNext():
        cand = it.next()
        if cand.getName().lower() == lowered:
            return cand, "name-match"
    return None, None

def run():
    try:
        program = currentProgram
        if program is None:
            output_json({"status": "error", "error": "No program loaded"})
            return

        args = _DSH_ARGS
        if len(args) < 2:
            output_json({
                "status": "error",
                "error": "Usage: <address> <type_name>  (optionally preceded by @outfile)"
            })
            return

        address_str = str(args[0])
        type_name = str(args[1])

        addr = toAddr(address_str)
        if addr is None:
            output_json({"status": "error",
                         "error": "Invalid address: " + address_str})
            return

        dtm = program.getDataTypeManager()
        dt, how = find_data_type(dtm, type_name)
        if dt is None:
            output_json({
                "status": "error",
                "error": "Data type not found: " + type_name,
                "hint": "define it first with apply_c_types.py"
            })
            return

        size = dt.getLength()
        if size <= 0:
            output_json({"status": "error",
                         "error": "Type has no fixed size: " + type_name})
            return

        listing = program.getListing()
        end = addr.add(size - 1)

        tid = program.startTransaction("Apply data type " + type_name)
        success = False
        try:
            listing.clearCodeUnits(addr, end, False)
            data = listing.createData(addr, dt)
            success = data is not None
        finally:
            program.endTransaction(tid, success)

        if not success:
            output_json({"status": "error",
                         "error": "createData failed at " + address_str})
            return

        components = []
        if hasattr(dt, "getNumComponents"):
            for i in range(dt.getNumComponents()):
                comp = dt.getComponent(i)
                components.append({
                    "name": comp.getFieldName(),
                    "offset": comp.getOffset(),
                    "length": comp.getLength(),
                    "type": str(comp.getDataType())
                })

        output_json({
            "status": "success",
            "type": str(dt.getPathName()),
            "type_lookup": how,
            "address": str(addr),
            "size": size,
            "components": components
        })

    except Exception as e:
        import traceback
        output_json({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

run()
