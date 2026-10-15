"""dsh custom tools for the ghidra-core skill (dsh-patch: additive module).

Ports the skill's four unique capabilities into the daemon:
  - exec_code        — open Ghidra-API escape hatch (unsandboxed exec, by design)
  - triage           — one-shot triage report (ported from triage_scan.py)
  - export_binary    — Original File export with md5 comparison
  - emulate_function — EmulatorHelper P-code emulation

Handlers follow the same contract as upstream tools: (ctx, args) -> dict,
raise on error.
"""

from __future__ import annotations

import json
import os
import re

from ghidra_rpc.server.main import register_handler
from ghidra_rpc.server.tools.modifications import _maybe_swing, ghidra_transaction


# ── shared helpers ────────────────────────────────────────────────────────────

def _to_addr(program, text):
    return program.getAddressFactory().getAddress(str(text))


def _find_function(program, identifier):
    """Three-level lookup: 0x address -> exact name -> name substring."""
    fm = program.getFunctionManager()
    ident = str(identifier)
    if ident.lower().startswith("0x"):
        try:
            addr = _to_addr(program, ident)
            func = fm.getFunctionAt(addr)
            if func:
                return func
            func = fm.getFunctionContaining(addr)
            if func:
                return func
        except Exception:
            pass
    for func in fm.getFunctions(True):
        if func.getName() == ident:
            return func
    for func in fm.getFunctions(True):
        if ident.lower() in func.getName().lower():
            return func
    return None


# ── exec_code ─────────────────────────────────────────────────────────────────

def _handle_exec_code(ctx, args: dict) -> dict:
    """Execute a Python 3 code file inside the daemon with full Ghidra API.

    args: binary, code_file
    The code file runs with these names predefined:
      program, currentProgram, fm, listing, memory, toAddr, monitor,
      find_function(name_or_addr), output_json(data)

    The LAST output_json(...) payload becomes the result; if the code never
    calls output_json, a default success note is returned.

    UNSANDBOXED by design: the code can do anything the JVM can.
    """
    import traceback

    binary = args.get("binary", "")
    code_file = args.get("code_file", "")
    if not code_file:
        raise ValueError("Missing required argument: code_file")

    pi = ctx.get_program(binary)
    program = pi.program

    try:
        with open(code_file, "r", encoding="utf-8") as fh:
            src = fh.read()
    except OSError as e:
        raise ValueError(f"cannot read code file {code_file}: {e}")

    outputs = []

    def output_json(data):
        outputs.append(data)

    def run_code():
        from ghidra.util.task import ConsoleTaskMonitor

        namespace = {
            "__builtins__": __builtins__,
            "program": program,
            "currentProgram": program,
            "fm": program.getFunctionManager(),
            "listing": program.getListing(),
            "memory": program.getMemory(),
            "toAddr": lambda s: _to_addr(program, s),
            "monitor": ConsoleTaskMonitor(),
            "find_function": lambda ident: _find_function(program, ident),
            "output_json": output_json,
        }
        exec(compile(src, code_file, "exec"), namespace)

    try:
        _maybe_swing(ctx, run_code)
    except Exception as e:
        return {"status": "error", "error": str(e),
                "traceback": traceback.format_exc()}

    # A code file may also WRITE to the program; persist like other write ops.
    ctx.save_program(pi)

    if outputs:
        result = outputs[-1]
        if isinstance(result, dict):
            result.setdefault("output_count", len(outputs))
            return result
        return {"status": "success", "value": result,
                "output_count": len(outputs)}
    return {"status": "success", "note": "no explicit output"}


# ── triage ────────────────────────────────────────────────────────────────────

_MAX_STRINGS = 20000
_MAX_QUICK_STRINGS = 50

_SUSPICIOUS = {
    "anti_debug": [
        "isdebuggerpresent", "checkremotedebuggerpresent",
        "ntqueryinformationprocess", "ntsetinformationthread",
        "outputdebugstringa", "outputdebugstringw",
        "gettickcount", "queryperformancecounter", "rdtsc"
    ],
    "injection": [
        "virtualallocex", "writeprocessmemory", "createremotethread",
        "openprocess", "ntmapviewofsection", "queueuserapc",
        "setwindowshookex"
    ],
    "crypto": [
        "cryptencrypt", "cryptdecrypt", "cryptacquirecontext",
        "bcryptencrypt", "aes"
    ],
    "network": [
        "internetopen", "internetconnect", "httpsendrequest",
        "winhttpopen", "urldownloadtofile", "socket", "connect",
        "send", "recv", "wsastartup"
    ],
    "persistence": [
        "regsetvalue", "regcreatekey", "createservice", "startservice",
        "schtasks"
    ],
    "dynamic_loading": [
        "loadlibrarya", "loadlibraryw", "getprocaddress", "ldrloaddll"
    ]
}

_VARIANT_SUFFIXES = ("", "a", "w", "ex", "exa", "exw")

_QUICK_STRING_RE = re.compile(
    r"flag|passw|correct|wrong|usage|key|congrat|success|fail", re.IGNORECASE)


def _matches_family(import_name, base):
    name = import_name.lower()
    if not name.startswith(base):
        return False
    return name[len(base):] in _VARIANT_SUFFIXES


def _handle_triage(ctx, args: dict) -> dict:
    """One-shot triage report; output shape matches the skill's triage.json."""
    binary = args.get("binary", "")
    pi = ctx.get_program(binary)

    def do_triage():
        program = pi.program
        result = {"status": "success"}

        # --- meta ---
        meta = {
            "program_name": program.getName(),
            "language": str(program.getLanguage().getLanguageID()),
            "compiler": str(program.getCompilerSpec().getCompilerSpecID()),
            "image_base": str(program.getImageBase()),
            "min_address": str(program.getMinAddress()),
            "max_address": str(program.getMaxAddress()),
            "executable_path": program.getExecutablePath(),
            "executable_format": program.getExecutableFormat(),
            "function_count": program.getFunctionManager().getFunctionCount(),
            "memory_blocks": []
        }
        try:
            md5 = program.getExecutableMD5()
            meta["md5"] = md5 if md5 else None
        except Exception:
            meta["md5"] = None

        mem = program.getMemory()
        block_names = []
        for block in mem.getBlocks():
            meta["memory_blocks"].append({
                "name": block.getName(),
                "start": str(block.getStart()),
                "end": str(block.getEnd()),
                "size": block.getSize(),
                "permissions": ("%s%s%s" % (
                    "r" if block.isRead() else "-",
                    "w" if block.isWrite() else "-",
                    "x" if block.isExecute() else "-"))
            })
            block_names.append(block.getName())
        result["meta"] = meta

        # --- imports / exports / entry points ---
        imports = {}
        st = program.getSymbolTable()
        sym_iter = st.getExternalSymbols()
        while sym_iter.hasNext():
            sym = sym_iter.next()
            parent = sym.getParentNamespace()
            lib = parent.getName() if parent is not None else "<unknown>"
            imports.setdefault(lib, [])
            name = sym.getName()
            if name not in imports[lib]:
                imports[lib].append(name)
        for lib in imports:
            imports[lib].sort()
        result["imports"] = imports

        exports = []
        entries = []
        entry_iter = st.getExternalEntryPointIterator()
        while entry_iter.hasNext():
            addr = entry_iter.next()
            sym = st.getPrimarySymbol(addr)
            name = sym.getName() if sym is not None else str(addr)
            rec = {"name": name, "address": str(addr)}
            if name in ("entry", "main", "_start", "WinMain", "DllMain",
                        "wWinMain", "mainCRTStartup", "wWinMainCRTStartup"):
                rec["type"] = "entry_point"
                entries.append(rec)
            else:
                rec["type"] = "export"
                exports.append(rec)
        result["exports"] = exports
        result["entry_points"] = entries
        result["exports_note"] = (
            "exports/entry_points are split from Ghidra's external-entry-point "
            "set by well-known entry names (entry/main/_start/WinMain/...); "
            "a stripped binary may classify its real entry as an export")

        # --- suspicious imports ---
        all_import_names = [(lib, name) for lib in imports for name in imports[lib]]
        suspicious = {}
        for category, bases in _SUSPICIOUS.items():
            hits = []
            for lib, name in all_import_names:
                for base in bases:
                    if _matches_family(name, base):
                        hits.append({"library": lib, "name": name})
                        break
            if hits:
                suspicious[category] = hits
        result["suspicious_imports"] = suspicious

        # --- selfmod / signal-handler warning ---
        # 判例 4307cc95: 自定义信号处理器 + 裸 UD2 时，
        # handler 可改写保存的 RIP 让"非法指令"正常返回 —— non-returning/
        # 死代码/调用图截断判定全部失真。与 legacy triage_scan.py 同构；
        # c50c8812 实测 rpc triage 缺本块导致路由行从未触发。
        signal_apis = ["sigaction", "rt_sigaction", "sigprocmask",
                       "rt_sigprocmask", "sigreturn", "rt_sigreturn",
                       "signal", "siginterrupt", "sigaltstack"]
        sig_hits = []
        for lib, name in all_import_names:
            for base in signal_apis:
                if _matches_family(name, base):
                    sig_hits.append({"library": lib, "name": name})
                    break
        ud2_hits = []
        try:
            from ghidra.util.task import ConsoleTaskMonitor
            _mon_sm = ConsoleTaskMonitor()
            _ud2 = bytes([0x0F, 0x0B])
            for block in mem.getBlocks():
                if not block.isExecute():
                    continue
                addr = block.getStart()
                bend = block.getEnd()
                while addr is not None and len(ud2_hits) < 20:
                    found = mem.findBytes(addr, bend, _ud2, None, True, _mon_sm)
                    if found is None:
                        break
                    ud2_hits.append(str(found))
                    addr = found.add(2)
        except Exception:
            pass
        selfmod_hit = bool(sig_hits or ud2_hits)
        result["selfmod_signal"] = {
            "hit": selfmod_hit,
            "signal_imports": sig_hits,
            "ud2_addresses": ud2_hits,
            "ud2_scan_capped": len(ud2_hits) >= 20,
            "advice": (
                "hit=true: 信号 handler 可能改写保存的 RIP 让非法指令正常返回"
                "（判例 4307cc95，UD2 的 SIGILL handler 推进 RIP，"
                "Ghidra 误判 flag 路径不可达）——non-returning/死代码/可达性"
                "静态判定不可信；下可达性否定结论前 MUST 先查 handler 是否推进"
                "保存的 RIP（ledger.py hypothesis 落账），结论走 "
                "conclude --kind negative --proof（铁律 10⑦）"
            ) if selfmod_hit else ""
        }

        total_imports = len(all_import_names)
        clean_libs = all(lib.lower().startswith(("kernel32", "ntdll"))
                         for lib in imports)
        result["clean_iat_warning"] = bool(clean_libs and total_imports < 15)

        # --- strings (single pass serves quick_strings and lang hints) ---
        listing = program.getListing()
        quick = []
        total_strings = 0
        scanned = 0
        go_re = re.compile(r"go\.buildid|runtime\.gopanic")
        rust_re = re.compile(r"panicked at|\.rustc")
        py_re = re.compile(r"PYINSTALLER|pyarmor|python3", re.IGNORECASE)
        pyx_re = re.compile(r"__pyx_|CyFunction", re.IGNORECASE)
        hints = {"go": False, "rust": False, "python": False, "pyx": False}

        for data in listing.getDefinedData(True):
            scanned += 1
            if scanned > _MAX_STRINGS:
                break
            try:
                if not data.hasStringValue():
                    continue
                value = str(data.getValue())
            except Exception:
                continue
            total_strings += 1
            if not value:
                continue
            if len(quick) < _MAX_QUICK_STRINGS and _QUICK_STRING_RE.search(value):
                quick.append({"address": str(data.getAddress()), "value": value})
            if not hints["go"] and go_re.search(value):
                hints["go"] = True
            if not hints["rust"] and rust_re.search(value):
                hints["rust"] = True
            if not hints["python"] and py_re.search(value):
                hints["python"] = True
            if not hints["pyx"] and pyx_re.search(value):
                hints["pyx"] = True

        result["quick_strings"] = {
            "total_strings_scanned": scanned,
            "total_defined_strings": total_strings,
            "scan_capped": scanned > _MAX_STRINGS,
            "matches": quick
        }

        dotnet = any(lib.lower().startswith("mscoree") for lib in imports)
        if not dotnet:
            dotnet = any(name == "_CorExeMain" for _, name in all_import_names)

        # --- packer detection (dsh-patch: multi-signal; a bare boolean lies) ---
        # Signal 1: section names. Trivially defeated by renaming sections —
        # exactly what CTF authors do — so it can never stand alone.
        upx_signals = []
        upx_sections = [n for n in block_names if "UPX" in n.upper()]
        if upx_sections:
            upx_signals.append({"signal": "section-name",
                                "detail": ",".join(upx_sections)})
        # Signal 2: UPX! magic in the raw file. Survives section renaming;
        # lives in the packheader/stub which may not be mapped into memory.
        magic_hits = []
        try:
            exe_path = str(program.getExecutablePath() or "")
            # Ghidra may report Git-Bash-flavored "/C:/..." paths on Windows
            if len(exe_path) > 3 and exe_path[0] == "/" \
                    and exe_path[2] == ":" and exe_path[3] == "/":
                exe_path = exe_path[1:]
            if exe_path and os.path.isfile(exe_path) \
                    and os.path.getsize(exe_path) < 512 * 1024 * 1024:
                with open(exe_path, "rb") as fh:
                    blob = fh.read()
                off = blob.find(b"UPX!")
                while off != -1 and len(magic_hits) < 8:
                    magic_hits.append(hex(off))
                    off = blob.find(b"UPX!", off + 1)
        except Exception:
            pass
        if magic_hits:
            upx_signals.append({"signal": "magic:UPX!",
                                "detail": "file offsets " + ",".join(magic_hits)})
        # Signal 3: structure — few imports + entry in the last executable
        # block + an uninitialized writable block (UPX0-style hollow section).
        blocks = list(mem.getBlocks())
        exec_blocks = [b for b in blocks if b.isExecute()]
        entry_in_last = False
        if exec_blocks:
            last_exec = exec_blocks[-1]
            lo = last_exec.getStart().getOffset()
            hi = last_exec.getEnd().getOffset()
            for rec in entries + exports:
                try:
                    ea = int(str(rec["address"]), 16)
                except ValueError:
                    continue
                if lo <= ea <= hi:
                    entry_in_last = True
                    break
        hollow_names = [b.getName() for b in blocks
                        if (not b.isInitialized()) and b.isWrite()]
        hollow = bool(hollow_names)
        structural = []
        if total_imports < 10:
            structural.append(f"imports={total_imports}<10")
        if entry_in_last:
            structural.append("entry-in-last-exec-block")
        if hollow:
            structural.append("uninitialized-writable-block")

        # MinGW-w64 (gcc) normally ships .CRT/.tls sections whose standard
        # layout trips both structural signals on fully unpacked binaries.
        # Demote those two signals to hints so they cannot reach the
        # packed-unknown threshold on their own.
        fp_hints = []
        mingw_layout = any(n.lower().startswith((".crt", ".tls"))
                           for n in block_names)
        if mingw_layout:
            kept = []
            for sig in structural:
                if sig in ("entry-in-last-exec-block",
                           "uninitialized-writable-block"):
                    fp_hints.append(
                        f"{sig} 命中，但存在 .CRT/.tls 节——MinGW-w64 标准布局，疑似误报")
                else:
                    kept.append(sig)
            structural = kept

        # ELF 正常布局：.bss 标准族本来就是未初始化可写块，任何带 .bss 的 ELF
        # （含 Cython 扩展 .so）都命中 hollow 信号；.so 的 entry 又常落在最后
        # exec block，两信号凑齐即误报 packed-unknown（Reverse-chal chal.so
        # 复盘 §7）。全部未初始化可写块都是 .bss 标准族名时，把 hollow 信号
        # 降级到 hints（UPX 块名是 UPX0/UPX1，不受影响）。
        if "uninitialized-writable-block" in structural:
            bss_family = {".bss", ".tbss", ".sbss", "common"}
            if hollow_names and all(n.lower() in bss_family
                                    for n in hollow_names):
                structural.remove("uninitialized-writable-block")
                fp_hints.append(
                    "uninitialized-writable-block 命中，但全部未初始化可写块"
                    "都是 .bss 标准族（" + ",".join(hollow_names) +
                    "）——ELF 正常布局，疑似误报")

        if upx_signals:
            packer_verdict = "upx"
        elif len(structural) >= 2:
            packer_verdict = "packed-unknown"
        else:
            packer_verdict = "none"
        result["packer"] = {
            "verdict": packer_verdict,
            "upx_signals": upx_signals,
            "structural_signals": structural,
            "false_positive_hints": fp_hints,
            "advice": (
                "UPX 指纹命中；upx -d 失败（头被篡改）时先跑 re-unpack 的 upx_repair.py"
                if packer_verdict == "upx" else
                "结构特征疑似加壳但无 UPX 指纹——按 re-unpack 流程人工判壳"
                if packer_verdict == "packed-unknown" else
                "verdict=none 不排除壳——节名可改、magic 可抹、结构可伪装；"
                "imports 极少/入口在末节/高熵等任一疑点都要人工复核"),
        }

        # CPython 扩展模块（Cython/手写 C 扩展）：exports 有 PyInit_*，
        # 或 imports 引 CPython API，或字符串含 __pyx_/CyFunction。
        # 命中 = 先走 ctf-patterns §12 元数据路线，别直接啃反编译 C。
        python_ext = hints["pyx"]
        if not python_ext:
            python_ext = any(str(rec.get("name", "")).startswith("PyInit_")
                             for rec in exports)
        if not python_ext:
            python_ext = any(
                name.startswith("PyInit_") or name == "Py_Initialize"
                or name.startswith("PyExc_")
                for _, name in all_import_names)

        result["lang_hints"] = {
            "go": hints["go"], "rust": hints["rust"], "dotnet": dotnet,
            "python": hints["python"], "python_ext": python_ext,
            "upx": packer_verdict == "upx"
        }

        # --- PE extras (best effort) ---
        exe_format = program.getExecutableFormat() or ""
        if "Portable Executable" in exe_format or exe_format.upper().endswith("(PE)"):
            pe_extras = {}
            tls_section = next(
                (b for b in block_names
                 if b.lower() == ".tls" or b.lower().startswith(".tls$")), None)
            if tls_section is not None:
                pe_extras["tls_section"] = tls_section
                block = mem.getBlock(tls_section)
                if block is not None and block.getSize() > 0:
                    pe_extras["tls_section_size"] = block.getSize()
            if pe_extras:
                result["pe_extras"] = pe_extras

        return result

    return _maybe_swing(ctx, do_triage)


# ── export_binary ─────────────────────────────────────────────────────────────

def _handle_export_binary(ctx, args: dict) -> dict:
    """Export the program back to its original file format.

    args: binary, path
    """
    import hashlib
    import os

    binary = args.get("binary", "")
    export_path = args.get("path", "")
    if not export_path:
        raise ValueError("Missing required argument: path")

    pi = ctx.get_program(binary)

    def do_export():
        from java.io import File
        from ghidra.app.util.exporter import OriginalFileExporter
        from ghidra.util.task import ConsoleTaskMonitor

        program = pi.program
        exporter = OriginalFileExporter()
        if not exporter.canExportDomainObject(program):
            raise ValueError(
                "OriginalFileExporter cannot export this program "
                "(no original file bytes)")

        monitor = ConsoleTaskMonitor()
        ok = exporter.export(File(export_path), program, None, monitor)
        if not ok or not os.path.isfile(export_path):
            raise ValueError(
                f"export() returned {ok}; monitor: {monitor.getMessage()}")

        with open(export_path, "rb") as fh:
            blob = fh.read()

        try:
            original_md5 = program.getExecutableMD5()
        except Exception:
            original_md5 = None

        return {
            "status": "success",
            "export_path": os.path.abspath(export_path),
            "size": len(blob),
            "md5": hashlib.md5(blob).hexdigest(),
            "sha256": hashlib.sha256(blob).hexdigest(),
            "original_md5": original_md5,
            "original_path": program.getExecutablePath(),
            "matches_original_md5": (original_md5 is not None
                                     and hashlib.md5(blob).hexdigest() == original_md5)
        }

    return _maybe_swing(ctx, do_export)


# ── emulate_function ─────────────────────────────────────────────────────────

def _handle_emulate_function(ctx, args: dict) -> dict:
    """Emulate a function with EmulatorHelper (P-code).

    args: binary, function, registers (dict), memory (dict), max_steps (int)
    Ported from the skill's emulate_function.py, including call-depth tracking
    (calls are followed into callees; only leaving the body at depth 0 counts
    as a return) and skipped_inputs reporting.
    """
    binary = args.get("binary", "")
    func_ident = args.get("function", "")
    register_inputs = args.get("registers") or {}
    memory_inputs = args.get("memory") or {}
    max_steps = int(args.get("max_steps", 10000))

    if not func_ident:
        raise ValueError("Missing required argument: function")

    pi = ctx.get_program(binary)

    def do_emulate():
        from ghidra.app.emulator import EmulatorHelper
        from ghidra.util.task import ConsoleTaskMonitor

        program = pi.program
        func = _find_function(program, func_ident)
        if func is None:
            raise ValueError(f"Function not found: {func_ident}")

        emulator = EmulatorHelper(program)
        monitor = ConsoleTaskMonitor()

        try:
            entry_point = func.getEntryPoint()

            skipped_inputs = []
            for reg_name, value in register_inputs.items():
                try:
                    reg = emulator.getLanguage().getRegister(reg_name)
                    if reg is None:
                        raise ValueError("unknown register: " + str(reg_name))
                    if isinstance(value, str):
                        value = (int(value, 16) if value.lower().startswith("0x")
                                 else int(value))
                    emulator.writeRegister(reg, value)
                except Exception as e:
                    skipped_inputs.append({
                        "kind": "register", "name": str(reg_name),
                        "value": value if isinstance(value, (int, str)) else str(value),
                        "reason": str(e)})

            for addr_str, data in memory_inputs.items():
                try:
                    addr = _to_addr(program, addr_str)
                    if addr is None:
                        raise ValueError("invalid address: " + str(addr_str))
                    if isinstance(data, list):
                        for i, byte_val in enumerate(data):
                            emulator.writeMemoryValue(addr.add(i), 1, byte_val & 0xff)
                    elif isinstance(data, str) and not data.startswith(("0x", "0X")):
                        for i, char in enumerate(data):
                            emulator.writeMemoryValue(addr.add(i), 1, ord(char))
                    else:
                        v = data
                        if isinstance(v, str):
                            v = (int(v, 16) if v.startswith(("0x", "0X")) else int(v))
                        emulator.writeMemoryValue(addr, 4, v)
                except Exception as e:
                    skipped_inputs.append({
                        "kind": "memory", "name": str(addr_str),
                        "value": data if isinstance(data, (int, str)) else str(data),
                        "reason": str(e)})

            emulator.writeRegister(emulator.getPCRegister(), entry_point.getOffset())

            execution_trace = []
            step_count = 0
            call_depth = 0
            stop_reason = "max_steps"

            while step_count < max_steps:
                current_addr = emulator.getExecutionAddress()
                if current_addr is None:
                    stop_reason = "no_execution_address"
                    break

                in_body = func.getBody().contains(current_addr)
                if not in_body and call_depth == 0:
                    stop_reason = "returned"
                    break

                inst = program.getListing().getInstructionAt(current_addr)
                if inst is None:
                    stop_reason = "no_instruction_at_pc"
                    break

                flow = inst.getFlowType()
                is_call = flow.isCall()

                trace_entry = {
                    "step": step_count,
                    "address": str(current_addr),
                    "instruction": inst.toString(),
                    "call_depth": call_depth
                }

                try:
                    success = emulator.step(monitor)
                    if not success:
                        trace_entry["error"] = "Execution failed"
                        execution_trace.append(trace_entry)
                        stop_reason = "execution_error"
                        break
                except Exception as e:
                    trace_entry["error"] = str(e)
                    execution_trace.append(trace_entry)
                    stop_reason = "execution_error"
                    break

                execution_trace.append(trace_entry)
                step_count += 1

                if is_call:
                    call_depth += 1
                elif flow.isTerminal():
                    if call_depth > 0:
                        call_depth -= 1
                    else:
                        stop_reason = "returned"
                        break

            register_states = {}
            lang = emulator.getLanguage()
            proc_name = lang.getProcessor().toString().lower()
            if proc_name.startswith("x86"):
                common_regs = ["RAX", "RBX", "RCX", "RDX", "RSI", "RDI", "RBP", "RSP",
                               "R8", "R9", "R10", "R11", "R12", "R13", "R14", "R15",
                               "RIP", "EAX", "EBX", "ECX", "EDX", "ESI", "EDI",
                               "EBP", "ESP", "EIP"]
            elif proc_name.startswith("arm"):
                common_regs = ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7",
                               "r8", "r9", "r10", "r11", "r12", "sp", "lr", "pc"]
            elif proc_name.startswith("mips"):
                common_regs = ["v0", "v1", "a0", "a1", "a2", "a3", "t0", "t1",
                               "t2", "t3", "t4", "t5", "t6", "t7", "s0", "s1",
                               "s2", "s3", "s4", "s5", "s6", "s7", "t8", "t9",
                               "sp", "fp", "ra", "pc"]
            else:
                common_regs = [r.getName() for r in lang.getRegisters()
                               if not r.isProcessorContext()
                               and r.getMinimumByteSize() >= 4]

            for reg_name in common_regs:
                try:
                    reg = lang.getRegister(reg_name)
                    if reg is not None:
                        value = emulator.readRegister(reg)
                        register_states[reg_name] = "0x%x" % value
                except Exception:
                    pass

            return {
                "status": "success",
                "function_name": func.getName(),
                "entry_point": str(entry_point),
                "steps_executed": step_count,
                "max_steps_reached": step_count >= max_steps,
                "stop_reason": stop_reason,
                "call_depth_at_stop": call_depth,
                "skipped_inputs": skipped_inputs,
                "register_states": register_states,
                "execution_trace": execution_trace[:100],
                "trace_truncated": len(execution_trace) > 100
            }
        finally:
            emulator.dispose()

    return _maybe_swing(ctx, do_emulate)


# ── import_raw ────────────────────────────────────────────────────────────────

def _handle_import_raw(ctx, args: dict) -> dict:
    """Import a raw memory dump (layer_dump output) as a new program.

    args: binary (donor program key/name — supplies language+compiler spec),
          path (dump file), base (hex VA the dump was taken from),
          name (optional program name), entry (optional list of hex VAs to
          seed as functions; default = base when analyze is on),
          analyze (default true).

    Use case: decrypted-layer dumps are noise in the original program's
    decompilation; re-importing them at their real VA gives xrefs and a
    decompiler view on the plaintext layer (WP-style reload pipeline).
    """
    path = args.get("path", "")
    base = args.get("base", "")
    if not path or not base:
        raise ValueError("Missing required arguments: path, base")
    try:
        base_addr = int(str(base), 0)
    except ValueError:
        raise ValueError(f"base must be an integer (hex ok): {base!r}")
    entries = args.get("entry") or []
    if isinstance(entries, (str, int)):
        entries = [entries]
    try:
        entries = [int(str(e), 0) for e in entries]
    except ValueError as e:
        raise ValueError(f"entry must be integer(s) (hex ok): {e}")
    analyze = bool(args.get("analyze", True))

    key = ctx.load_raw_dump(path, base_addr, args.get("binary", ""),
                            name=args.get("name") or None,
                            entries=entries,
                            analyze=analyze)
    pi = ctx.programs.get(key) or ctx.get_program(key)
    seeded = entries or ([base_addr] if analyze else [])
    return {
        "status": "success",
        "program_key": key,
        "name": pi.name,
        "base": hex(base_addr),
        "size": pi.program.getMemory().getBlock("dump").getSize(),
        "seeded_entries": [hex(e) for e in seeded],
        "analysis_complete": pi.analysis_complete,
    }


register_handler("exec_code", _handle_exec_code)
register_handler("triage", _handle_triage)
register_handler("export_binary", _handle_export_binary)
register_handler("emulate_function", _handle_emulate_function)
register_handler("import_raw", _handle_import_raw)
