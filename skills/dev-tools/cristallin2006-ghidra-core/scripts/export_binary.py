# Export the (possibly patched) program back to its original file format
# @category DSH.Reverse
# @runtime PyGhidra
#
# Uses ghidra.app.util.exporter.OriginalFileExporter, so the result is the
# original binary layout with in-memory modifications applied (file offsets,
# not VAs). Replaces the GUI "File -> Export Program -> Original File" step.

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

import hashlib
import json
import os

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
                "error": "Usage: <export_file_path>  (optionally preceded by @outfile)"
            })
            return

        export_path = str(args[0])

        from java.io import File
        from ghidra.app.util.exporter import OriginalFileExporter
        from ghidra.util.task import ConsoleTaskMonitor

        exporter = OriginalFileExporter()

        if not exporter.canExportDomainObject(program):
            output_json({
                "status": "error",
                "error": "OriginalFileExporter cannot export this program "
                         "(no original file bytes)"
            })
            return

        # 12.1 signature: export(File, DomainObject, AddressSetView, TaskMonitor).
        # This exporter does not support address restriction, so addrSet is unused.
        monitor = ConsoleTaskMonitor()
        ok = exporter.export(File(export_path), program, None, monitor)
        if not ok or not os.path.isfile(export_path):
            output_json({
                "status": "error",
                "error": "export() returned %s; log: %s" % (ok, monitor.getMessage())
            })
            return

        with open(export_path, "rb") as f:
            blob = f.read()

        try:
            original_md5 = program.getExecutableMD5()
        except Exception:
            original_md5 = None

        output_json({
            "status": "success",
            "export_path": os.path.abspath(export_path),
            "size": len(blob),
            "md5": hashlib.md5(blob).hexdigest(),
            "sha256": hashlib.sha256(blob).hexdigest(),
            "original_md5": original_md5,
            "original_path": program.getExecutablePath(),
            "matches_original_md5": (original_md5 is not None
                                     and hashlib.md5(blob).hexdigest() == original_md5)
        })

    except Exception as e:
        import traceback
        output_json({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

run()
