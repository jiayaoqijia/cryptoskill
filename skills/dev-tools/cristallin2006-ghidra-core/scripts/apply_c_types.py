# Parse C declarations (struct/union/enum/typedef) into the program's type library
# @category DSH.Reverse
# @runtime PyGhidra
#
# The file may contain multiple declarations, e.g.:
#   struct key_ctx { uint32_t round; char key[16]; };
#   enum flags { F_NONE = 0, F_INIT = 1 };
# stdint names (uint32_t, ...) are pre-typedef'd to Ghidra primitives if the
# parser does not already know them.

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

# stdint typedef prelude mapped onto Ghidra primitive names. Only prepended when
# the source actually mentions the names, so plain files parse unchanged.
_STDINT_PRELUDE = (
    "typedef unsigned char uint8_t;\n"
    "typedef signed char int8_t;\n"
    "typedef unsigned short uint16_t;\n"
    "typedef signed short int16_t;\n"
    "typedef unsigned int uint32_t;\n"
    "typedef signed int int32_t;\n"
    "typedef unsigned long long uint64_t;\n"
    "typedef signed long long int64_t;\n"
)

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
                "count": len(data.get("types_added", []))
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

def _type_paths(dtm):
    """Snapshot all type path names currently in the data type manager."""
    paths = set()
    it = dtm.getAllDataTypes()
    while it.hasNext():
        paths.add(str(it.next().getPathName()))
    return paths

def run():
    try:
        program = currentProgram
        if program is None:
            output_json({"status": "error", "error": "No program loaded"})
            return

        args = _DSH_ARGS
        if not args:
            output_json({
                "status": "error",
                "error": "Usage: <c_decl_file>  (optionally preceded by @outfile)"
            })
            return

        decl_path = str(args[0])
        try:
            f = open(decl_path, "r")
            try:
                src = f.read()
            finally:
                f.close()
        except Exception as e:
            output_json({"status": "error",
                         "error": "cannot read declaration file %s: %s" % (decl_path, e)})
            return

        if any(name in src for name in
               ("uint8_t", "int8_t", "uint16_t", "int16_t",
                "uint32_t", "int32_t", "uint64_t", "int64_t")):
            src = _STDINT_PRELUDE + src

        from java.io import ByteArrayInputStream
        from ghidra.app.util.cparser.C import CParser

        dtm = program.getDataTypeManager()

        before = _type_paths(dtm)

        # CParser(dtm, storeDataType=True, subDTMgrs): parsed types are added to
        # the program DTM with REPLACE_HANDLER and sized with the program's data
        # organization. parse() manages its own transaction on the DTM; the outer
        # program transaction below keeps the change atomic from the script side.
        parser = CParser(dtm, True, None)

        tid = program.startTransaction("Parse C declarations")
        success = False
        parse_error = None
        try:
            parser.parse(ByteArrayInputStream(src.encode("utf-8")))
            success = True
        except Exception as e:
            parse_error = str(e)
        finally:
            program.endTransaction(tid, success)

        after = _type_paths(dtm)
        added = sorted(after - before)

        if not success:
            output_json({
                "status": "error",
                "error": "C parse failed: " + str(parse_error),
                "types_added": added
            })
            return

        output_json({
            "status": "success",
            "file": decl_path,
            "types_added": added,
            "types_added_count": len(added)
        })

    except Exception as e:
        import traceback
        output_json({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

run()
