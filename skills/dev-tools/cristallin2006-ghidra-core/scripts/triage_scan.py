# One-shot triage scan: metadata, imports/exports, suspicious import groups,
# quick interesting strings, and language/packer hints
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

MAX_STRINGS = 20000
MAX_QUICK_STRINGS = 50

SUSPICIOUS = {
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

# Suffixes that still count as the same API family (A/W/Ex variants)
_VARIANT_SUFFIXES = ("", "a", "w", "ex", "exa", "exw")

QUICK_STRING_RE = re.compile(
    r"flag|passw|correct|wrong|usage|key|congrat|success|fail", re.IGNORECASE)


def matches_family(import_name, base):
    """Case-insensitive match of an import against an API base name,
    tolerating A/W/Ex suffix variants but not unrelated longer names."""
    name = import_name.lower()
    if not name.startswith(base):
        return False
    return name[len(base):] in _VARIANT_SUFFIXES


def emit(data):
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
                "count": data.get("meta", {}).get("function_count", 0)
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


def collect_imports(program):
    """Return dict of library name -> sorted list of imported symbol names."""
    imports = {}
    st = program.getSymbolTable()
    sym_iter = st.getExternalSymbols()
    while sym_iter.hasNext():
        sym = sym_iter.next()
        parent = sym.getParentNamespace()
        lib = parent.getName() if parent is not None else "<unknown>"
        if lib not in imports:
            imports[lib] = []
        name = sym.getName()
        if name not in imports[lib]:
            imports[lib].append(name)
    for lib in imports:
        imports[lib].sort()
    return imports


def collect_exports_and_entries(program):
    """Split external entry points into real exports vs. the likely entry point.

    Ghidra marks both PE-exported symbols and the binary's entry point as
    external entry points, and the symbol table alone cannot fully separate
    them; the well-known entry names are the heuristic split.
    """
    exports = []
    entries = []
    st = program.getSymbolTable()
    mem = program.getMemory()

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
    return exports, entries


def collect_strings(program):
    """Return (total_scanned, total_defined_strings, quick_matches)."""
    listing = program.getListing()
    quick = []
    total_strings = 0
    scanned = 0
    for data in listing.getDefinedData(True):
        scanned += 1
        if scanned > MAX_STRINGS:
            break
        try:
            if not data.hasStringValue():
                continue
        except Exception:
            continue
        total_strings += 1
        if len(quick) >= MAX_QUICK_STRINGS:
            continue
        try:
            value = str(data.getValue())
            if value and QUICK_STRING_RE.search(value):
                quick.append({"address": str(data.getAddress()),
                              "value": value})
        except Exception:
            continue
    return scanned, total_strings, quick


def run():
    try:
        program = currentProgram
        if program is None:
            emit({"status": "error", "error": "No program loaded"})
            return

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
        imports = collect_imports(program)
        result["imports"] = imports
        exports, entries = collect_exports_and_entries(program)
        result["exports"] = exports
        result["entry_points"] = entries
        result["exports_note"] = (
            "exports/entry_points are split from Ghidra's external-entry-point "
            "set by well-known entry names (entry/main/_start/WinMain/...); "
            "a stripped binary may classify its real entry as an export")

        # --- suspicious imports ---
        all_import_names = []
        for lib in imports:
            for name in imports[lib]:
                all_import_names.append((lib, name))

        suspicious = {}
        for category, bases in SUSPICIOUS.items():
            hits = []
            for lib, name in all_import_names:
                for base in bases:
                    if matches_family(name, base):
                        hits.append({"library": lib, "name": name})
                        break
            if hits:
                suspicious[category] = hits
        result["suspicious_imports"] = suspicious

        # --- selfmod / signal-handler warning ---
        # 判例 4307cc95: 自定义信号处理器 + 裸 UD2 时，
        # handler 可改写保存的 RIP 让"非法指令"正常返回 —— Ghidra/IDA 的
        # non-returning/死代码/调用图截断判定全部失真，可达性否定结论必须走
        # conclude --kind negative --proof（铁律 10⑦）。
        signal_apis = ["sigaction", "rt_sigaction", "sigprocmask",
                       "rt_sigprocmask", "sigreturn", "rt_sigreturn",
                       "signal", "siginterrupt", "sigaltstack"]
        sig_hits = []
        for lib, name in all_import_names:
            for base in signal_apis:
                if matches_family(name, base):
                    sig_hits.append({"library": lib, "name": name})
                    break
        ud2_hits = []
        try:
            from ghidra.util.task import ConsoleTaskMonitor
            _mon2 = ConsoleTaskMonitor()
            _ud2 = bytes([0x0F, 0x0B])
            for block in mem.getBlocks():
                if not block.isExecute():
                    continue
                addr = block.getStart()
                bend = block.getEnd()
                while addr is not None and len(ud2_hits) < 20:
                    found = mem.findBytes(addr, bend, _ud2, None, True, _mon2)
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

        # --- clean IAT warning ---
        total_imports = len(all_import_names)
        clean_libs = True
        for lib in imports:
            low = lib.lower()
            if not (low.startswith("kernel32") or low.startswith("ntdll")):
                clean_libs = False
                break
        result["clean_iat_warning"] = bool(clean_libs and total_imports < 15)

        # --- strings ---
        scanned, total_strings, quick = collect_strings(program)
        result["quick_strings"] = {
            "total_strings_scanned": scanned,
            "total_defined_strings": total_strings,
            "scan_capped": scanned > MAX_STRINGS,
            "matches": quick
        }

        # --- language / packer hints ---
        hint_strings = {"go": False, "rust": False, "python": False, "pyx": False}
        go_re = re.compile(r"go\.buildid|runtime\.gopanic")
        rust_re = re.compile(r"panicked at|\.rustc")
        py_re = re.compile(r"PYINSTALLER|pyarmor|python3", re.IGNORECASE)
        pyx_re = re.compile(r"__Pyx_|cython", re.IGNORECASE)

        listing = program.getListing()
        scanned2 = 0
        for data in listing.getDefinedData(True):
            scanned2 += 1
            if scanned2 > MAX_STRINGS:
                break
            try:
                if not data.hasStringValue():
                    continue
                value = str(data.getValue())
            except Exception:
                continue
            if not value:
                continue
            if not hint_strings["go"] and go_re.search(value):
                hint_strings["go"] = True
            if not hint_strings["rust"] and rust_re.search(value):
                hint_strings["rust"] = True
            if not hint_strings["python"] and py_re.search(value):
                hint_strings["python"] = True
            if not hint_strings["pyx"] and pyx_re.search(value):
                hint_strings["pyx"] = True
            if all(hint_strings.values()):
                break

        # Stripped Go binaries may yield no defined strings; the buildinfo
        # magic "\xff Go buildinf:" survives stripping, so scan raw bytes.
        # (Memory.findBytes only has byte[] overloads — pass bytes, not str.)
        if not hint_strings["go"]:
            from ghidra.util.task import ConsoleTaskMonitor
            _mon = ConsoleTaskMonitor()
            _buildinfo = bytes.fromhex("ff 20 47 6f 20 62 75 69 6c 64 69 6e 66 3a")
            for block in mem.getBlocks():
                try:
                    found = mem.findBytes(block.getStart(), block.getEnd(),
                                          _buildinfo, None, True, _mon)
                except Exception:
                    found = None
                if found is not None:
                    hint_strings["go"] = True
                    break

        dotnet = False
        for lib in imports:
            if lib.lower().startswith("mscoree"):
                dotnet = True
                break
        if not dotnet:
            for lib, name in all_import_names:
                if name == "_CorExeMain":
                    dotnet = True
                    break

        upx = False
        for bname in block_names:
            if "UPX" in bname.upper():
                upx = True
                break

        # CPython 扩展模块（Cython/手写 C 扩展）：exports 有 PyInit_*，
        # 或 imports 引 CPython API，或字符串含 __Pyx_（Cython 内部符号）。
        # 命中 = 先走 ctf-patterns §12 元数据路线，别直接啃反编译 C。
        python_ext = hint_strings["pyx"]
        if not python_ext:
            for rec in exports:
                if str(rec.get("name", "")).startswith("PyInit_"):
                    python_ext = True
                    break
        if not python_ext:
            for lib, name in all_import_names:
                if (name.startswith("PyInit_") or name == "Py_Initialize"
                        or name.startswith("PyExc_")):
                    python_ext = True
                    break

        result["lang_hints"] = {
            "go": hint_strings["go"],
            "rust": hint_strings["rust"],
            "dotnet": dotnet,
            "python": hint_strings["python"],
            "python_ext": python_ext,
            "upx": upx
        }

        # --- PE extras (best effort; omitted when not derivable) ---
        exe_format = program.getExecutableFormat() or ""
        if "Portable Executable" in exe_format or exe_format.upper().endswith("(PE)"):
            pe_extras = {}
            tls_section = None
            for bname in block_names:
                if bname.lower() == ".tls" or bname.lower().startswith(".tls$"):
                    tls_section = bname
                    break
            if tls_section is not None:
                pe_extras["tls_section"] = tls_section
                # TLS callbacks imply a non-empty .tls directory; check for
                # defined data referencing callback addresses
                block = mem.getBlock(tls_section)
                if block is not None and block.getSize() > 0:
                    pe_extras["tls_section_size"] = block.getSize()
            if pe_extras:
                result["pe_extras"] = pe_extras

        emit(result)

    except Exception as e:
        import traceback
        emit({"status": "error", "error": str(e),
              "traceback": traceback.format_exc()})


run()
