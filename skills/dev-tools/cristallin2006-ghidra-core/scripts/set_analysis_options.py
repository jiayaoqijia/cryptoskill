# Ghidra preScript to configure analysis options before auto-analysis runs
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


def run():
    """Deprecated: kept for reference only."""
    import json
    print("===JSON_START===")
    print(json.dumps({
        "status": "deprecated",
        "note": "PyGhidra 流程下无 preScript 钩子，本脚本不会生效；"
                "请用 driver.py import --analysis minimal|default 或 analysis_config.py"
    }))
    print("===JSON_END===")
    return

    # --- reference implementation below (unreachable) ---
    args = _DSH_ARGS
    mode = args[0].lower() if args else "default"

    if mode == "minimal":
        # Disable slow analyzers to speed up import of large binaries.
        # Strings, symbols, functions, and basic disassembly still work.
        heavy_analyzers = [
            "Decompiler Parameter ID",
            "Stack",
            "Aggressive Instruction Finder",
            "Condense Filler Bytes",
            "DWARF",
            "PDB Universal",
            "PDB",
            "Demangler GNU",
            "Demangler Microsoft",
            "Non-Returning Functions - Discovered",
            "Embedded Media",
            "GCC Exception Handlers",
            "Windows x86 PE Exception Handling",
        ]
        for name in heavy_analyzers:
            try:
                setAnalysisOption(currentProgram, name, "false")
            except:
                pass  # Analyzer may not exist for this architecture

run()
