#!/usr/bin/env python
"""emulate_program.py - Unicorn whole-program emulation harness for PE images.

Host-side tool (Python 3.8+; unicorn required, pefile preferred but optional).
Middle layer between emulate_blob.py (bare blobs, no imports/IO) and
re-dynamic (Wine / real machine): maps a PE into Unicorn, fills the IAT with
stubs, hooks Win32 import handlers, runs main as a function, feeds stdin,
and breaks at success/fail points. Built for console-style flag checkers
(Rust/Go/C++ heavily inlined "main IS the check body" CTF targets); the
case-H ran one input in 0.06s and brute-forced 44 independent slots
in 62s this way.

Scope / known boundaries:
  - x86-64 PE (PE32+) console programs only. 32-bit / GUI / drivers: no.
  - No SEH / C++ / Rust panic-unwind emulation (no real TEB exception chain);
    panics wander and usually end as unmapped-fetch stops.
  - Heavy FP/SSE recomputation is not validated - cross-check final answers
    with a second engine (Wine > real machine > independent Python model),
    per 铁律 10. Qiling is NOT an independent engine (also Unicorn).
  - Anything needing real Win32 semantics (registry, files on disk, network,
    threads, real TLS/CRT init) belongs on re-dynamic, not here.

ABI traps baked in (each one really bit someone, see
references/unicorn-harness.md §3):
  - IO_STATUS_BLOCK.Information is a ULONG_PTR at offset 8 on x64.
  - NtReadFile/NtWriteFile: 4 register args + 5 STACK args (iosb at
    [rsp+0x28], buf [rsp+0x30], len [rsp+0x38]); returns NTSTATUS.
  - HeapReAlloc size is the 4th arg (R9), not R8 (old pointer).
  - core::fmt::Arguments is {pieces:&[&str], fmt, args}, not a {ptr,len} &str.
  - bytes(uc.mem_read(...)) before feeding back into mem_write.

Usage:
  emulate_program.py app.exe --entry 0x<main> [options]
    --stdin "text" | --stdin-file path    stdin bytes fed to ReadFile/NtReadFile
    --break-success 0xaddr[,0xaddr...]    stop + report success on hit
    --break-fail 0xaddr[,0xaddr...]       stop + report fail on hit
    --max-insns N --timeout S --mem-mb N
    --stub-list                           list built-in Win32 stubs, exit
    --trace-api                           print each API call + arg summary
    --strict-api                          unknown API stops the run (default: warn, ret 0)
    --dump-state 0xaddr:len[,...]         dump memory ranges at stop
    --json out.json

Exit codes: 0 emulation finished (read the report), 2 usage error,
3 unicorn missing, 4 harness error (NOT the guest).
"""
from __future__ import annotations

import argparse
import json
import os
import struct
import sys
import time

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

try:
    from unicorn import (
        Uc, UcError,
        UC_ARCH_X86, UC_MODE_64,
        UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED,
        UC_PROT_READ, UC_PROT_WRITE, UC_PROT_EXEC,
    )
    from unicorn.x86_const import (
        UC_X86_REG_RIP, UC_X86_REG_RSP, UC_X86_REG_RAX,
        UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9,
    )
    try:
        from unicorn.x86_const import UC_X86_REG_GS_BASE
    except ImportError:
        UC_X86_REG_GS_BASE = None
except ImportError:
    print("[依赖缺失] 需要 unicorn：pip install unicorn（或进 re-tools-venv）",
          file=sys.stderr)
    sys.exit(3)

try:
    import pefile
except ImportError:
    pefile = None

PAGE = 0x1000

# Fixed layout (same scheme as the case-H harness):
STACK_BASE = 0x20000000
STACK_SIZE = 0x200000
STUB_BASE = 0x50000000
STUB_SIZE = 0x10000          # 16 bytes per stub -> up to 4095 imports
TEB_BASE = 0x7EFDE000
PEB_BASE = 0x7EFDF000
HEAP_HANDLE = 0x12340000
PSEUDO_HANDLE = 0x77         # GetStdHandle/GetCurrentProcess/Thread
FIXED_FILETIME = 0x01D8C000_00000000   # GetSystemTimeAsFileTime 固定值

IMAGE_SCN_MEM_READ = 0x40000000
IMAGE_SCN_MEM_WRITE = 0x80000000
IMAGE_SCN_MEM_EXEC = 0x20000000


class HarnessError(Exception):
    """harness 自身错误（PE 解析/映射/参数），与 guest 异常严格区分。"""


def align_down(v, a=PAGE):
    return v & ~(a - 1)


def align_up(v, a=PAGE):
    return (v + a - 1) & ~(a - 1)


def parse_int(s):
    return int(s, 0)


def parse_addr_list(s):
    out = []
    for tok in s.split(","):
        tok = tok.strip()
        if tok:
            out.append(parse_int(tok))
    return out


def parse_dump_spec(s):
    out = []
    for tok in s.split(","):
        tok = tok.strip()
        if not tok:
            continue
        if ":" not in tok:
            raise argparse.ArgumentTypeError(
                "--dump-state 需要 0xaddr:len，如 0x443340:0x40")
        addr, ln = tok.split(":", 1)
        out.append((parse_int(addr), parse_int(ln)))
    return out


# ---------------------------------------------------------------- PE loading

class PEImage:
    """Loaded PE: sections, imports, image base. pefile preferred; a minimal
    stdlib fallback loader is built in (limitations: PE32+ only, no relocs,
    no delay-load / bound imports, import by ordinal recorded as ord_N)."""

    def __init__(self, path):
        self.path = path
        self.image_base = 0
        self.size_of_image = 0
        self.size_of_headers = 0
        self.machine = 0
        # sections: list of dict(va, vsize, raw, characteristics)
        self.sections = []
        # imports: list of (dll, name, iat_va)
        self.imports = []
        self._load()

    def _load(self):
        try:
            data = open(self.path, "rb").read()
        except OSError as e:
            raise HarnessError("读取 PE 失败: %s" % e)
        if len(data) < 0x40 or data[:2] != b"MZ":
            raise HarnessError("不是 PE 文件（缺 MZ 头）: %s" % self.path)
        if pefile is not None:
            self._load_pefile(data)
        else:
            self._load_minimal(data)
        if self.machine != 0x8664:
            raise HarnessError(
                "仅支持 x86-64 (PE32+)，本样本 Machine=0x%04x；"
                "32 位/其他架构不在本工具边界内" % self.machine)
        if not self.sections:
            raise HarnessError("PE 没有任何节区，文件可能损坏")

    def _load_pefile(self, data):
        pe = pefile.PE(data=data, fast_load=True)
        pe.parse_data_directories()
        self.machine = pe.FILE_HEADER.Machine
        oh = pe.OPTIONAL_HEADER
        self.image_base = oh.ImageBase
        self.size_of_image = oh.SizeOfImage
        self.size_of_headers = oh.SizeOfHeaders
        self._headers = data[:self.size_of_headers]
        for s in pe.sections:
            self.sections.append({
                "va": self.image_base + s.VirtualAddress,
                "vsize": s.Misc_VirtualSize,
                "raw": s.get_data(),
                "characteristics": s.Characteristics,
            })
        for entry in getattr(pe, "DIRECTORY_ENTRY_IMPORT", []) or []:
            dll = entry.dll.decode("ascii", "replace")
            for imp in entry.imports:
                name = (imp.name.decode("ascii", "replace") if imp.name
                        else "ord_%d" % imp.ordinal)
                self.imports.append((dll, name, imp.address))

    def _load_minimal(self, data):
        """精简装载器（无 pefile 时的兜底）。限制：PE32+ only、不处理重定位、
        不处理 delay-load / bound import；IAT 只按 FirstThunk 填充。"""
        u16 = lambda o: struct.unpack_from("<H", data, o)[0]
        u32 = lambda o: struct.unpack_from("<I", data, o)[0]
        u64 = lambda o: struct.unpack_from("<Q", data, o)[0]
        pe_off = u32(0x3C)
        if data[pe_off:pe_off + 4] != b"PE\0\0":
            raise HarnessError("缺 PE 签名（精简装载器）")
        coff = pe_off + 4
        self.machine = u16(coff)
        nsec = u16(coff + 2)
        opt_size = u16(coff + 16)
        opt = coff + 20
        if u16(opt) != 0x20B:
            raise HarnessError("精简装载器仅支持 PE32+（magic 0x20b）")
        self.image_base = u64(opt + 24)
        self.size_of_image = u32(opt + 56)
        self.size_of_headers = u32(opt + 60)
        import_rva, _ = u32(opt + 112 + 8 * 1), u32(opt + 112 + 8 * 1 + 4)
        self._headers = data[:self.size_of_headers]
        sec_off = opt + opt_size
        for i in range(nsec):
            o = sec_off + i * 40
            vsize, va = u32(o + 8), u32(o + 12)
            raw_size, raw_ptr = u32(o + 16), u32(o + 20)
            self.sections.append({
                "va": self.image_base + va,
                "vsize": vsize,
                "raw": data[raw_ptr:raw_ptr + raw_size],
                "characteristics": u32(o + 36),
            })

        def rva2off(rva):
            for s in self.sections:
                base = s["va"] - self.image_base
                if base <= rva < base + max(s["vsize"], len(s["raw"])):
                    # 用 raw 数据反查：简化处理，按节内偏移读文件
                    idx = self.sections.index(s)
                    o = sec_off + idx * 40
                    raw_ptr = u32(o + 16)
                    return raw_ptr + (rva - base)
            return None

        if import_rva:
            o = rva2off(import_rva)
            while o is not None and u32(o + 12) != 0:
                ilt_rva = u32(o) or u32(o + 16)
                name_off = rva2off(u32(o + 12))
                dll = ""
                if name_off is not None:
                    end = data.index(b"\0", name_off)
                    dll = data[name_off:end].decode("ascii", "replace")
                iat_rva = u32(o + 16)
                thunk_off = rva2off(ilt_rva)
                i = 0
                while thunk_off is not None:
                    val = u64(thunk_off + i * 8)
                    if val == 0:
                        break
                    if val & (1 << 63):
                        name = "ord_%d" % (val & 0xFFFF)
                    else:
                        noff = rva2off(val & 0x7FFFFFFF)
                        if noff is None:
                            name = "ord_?"
                        else:
                            end = data.index(b"\0", noff + 2)
                            name = data[noff + 2:end].decode("ascii", "replace")
                    self.imports.append(
                        (dll, name, self.image_base + iat_rva + i * 8))
                    i += 1
                o += 20


# ------------------------------------------------------------------- harness

class ProgramEmu:
    def __init__(self, args):
        self.args = args
        self.pe = PEImage(args.pe)
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.stub_by_addr = {}     # stub va -> (dll, name)
        self.stub_by_name = {}     # name -> stub va
        self.heap_top = 0
        self.heap_limit = 0
        self.stdin_data = b""
        self.stdin_pos = 0
        self.stdout = bytearray()
        self.api_counts = {}
        self.api_log = []
        self.tls = {}              # slot index -> value
        self.init_once = {}        # INIT_ONCE addr -> ("pending"/"done", ctx)
        self.last_error = 0
        self._warned_api = set()
        self.stop = None
        self.stop_kind = None      # success / fail / exit / limit / guest-error
        self.insns = 0
        self.t0 = time.monotonic()
        self.guest_err = None
        self._va_top = 0           # VirtualAlloc bump
        self._cmdline_a = 0
        self._cmdline_w = 0

    # ---- memory / image setup (harness-side errors raise HarnessError) ----

    def setup(self):
        uc = self.uc
        try:
            self._map_image()
            uc.mem_map(STACK_BASE, STACK_SIZE, UC_PROT_READ | UC_PROT_WRITE)
            mem_mb = max(1, self.args.mem_mb)
            heap_base = 0x30000000
            heap_size = mem_mb * 0x100000
            uc.mem_map(heap_base, heap_size, UC_PROT_READ | UC_PROT_WRITE)
            self.heap_top = heap_base + 0x1000
            self.heap_limit = heap_base + heap_size
            self._va_top = heap_base + heap_size  # VirtualAlloc 从堆区上方另起
            uc.mem_map(STUB_BASE, STUB_SIZE, UC_PROT_READ | UC_PROT_EXEC)
            uc.mem_write(STUB_BASE, b"\xc3" * STUB_SIZE)  # 全部预填 ret
            self._map_teb()
            self._fill_iat()
        except UcError as e:
            raise HarnessError("内存映射失败（非 guest 错误）: %s" % e)
        if len(self.stub_by_addr) * 16 >= STUB_SIZE - 16:
            raise HarnessError("导入数量超过桩区容量（%d）" % (STUB_SIZE // 16))

    def _map_image(self):
        """按节 Characteristics 求每页权限并集，连续同权限段一次 map。"""
        uc = self.uc
        ib = self.pe.image_base
        total = align_up(self.pe.size_of_image)
        page_perm = {}

        def set_range(va, size, perm):
            for p in range(align_down(va), align_up(va + size), PAGE):
                page_perm[p] = page_perm.get(p, 0) | perm

        set_range(ib, self.pe.size_of_headers, UC_PROT_READ)
        for s in self.pe.sections:
            perm = 0
            if s["characteristics"] & IMAGE_SCN_MEM_READ:
                perm |= UC_PROT_READ
            if s["characteristics"] & IMAGE_SCN_MEM_WRITE:
                perm |= UC_PROT_WRITE
            if s["characteristics"] & IMAGE_SCN_MEM_EXEC:
                perm |= UC_PROT_EXEC | UC_PROT_READ
            if perm == 0:
                perm = UC_PROT_READ
            set_range(s["va"], max(s["vsize"], len(s["raw"])), perm)

        p = align_down(ib)
        while p < align_down(ib) + total:
            perm = page_perm.get(p, UC_PROT_READ)
            q = p + PAGE
            while q < align_down(ib) + total and page_perm.get(q, UC_PROT_READ) == perm:
                q += PAGE
            uc.mem_map(p, q - p, perm)
            p = q

        uc.mem_write(ib, self.pe._headers)
        for s in self.pe.sections:
            if s["raw"]:
                uc.mem_write(s["va"], s["raw"])
            if s["vsize"] > len(s["raw"]):
                uc.mem_write(s["va"] + len(s["raw"]),
                             b"\0" * (s["vsize"] - len(s["raw"])))

    def _map_teb(self):
        """伪造 TEB/PEB 并让 GS 指向 TEB，使常见 GS:[0x30]/GS:[0x60] 读不炸。"""
        uc = self.uc
        uc.mem_map(TEB_BASE, PAGE, UC_PROT_READ | UC_PROT_WRITE)
        uc.mem_map(PEB_BASE, PAGE, UC_PROT_READ | UC_PROT_WRITE)
        uc.mem_write(TEB_BASE + 0x30, struct.pack("<Q", TEB_BASE))   # TEB.Self
        uc.mem_write(TEB_BASE + 0x60, struct.pack("<Q", PEB_BASE))   # TEB.PEB
        uc.mem_write(PEB_BASE + 0x10, struct.pack("<Q", self.pe.image_base))
        uc.mem_write(PEB_BASE + 0x30, struct.pack("<Q", HEAP_HANDLE))  # ProcessHeap
        if UC_X86_REG_GS_BASE is not None:
            try:
                uc.reg_write(UC_X86_REG_GS_BASE, TEB_BASE)
            except UcError:
                print("[提示] 当前 unicorn 不支持写 GS_BASE，"
                      "GS 段访问可能异常", file=sys.stderr)

    def _fill_iat(self):
        uc = self.uc
        for i, (dll, name, iat_va) in enumerate(self.pe.imports):
            stub = STUB_BASE + (i + 1) * 16
            self.stub_by_addr[stub] = (dll, name)
            self.stub_by_name.setdefault(name, stub)
            uc.mem_write(iat_va, struct.pack("<Q", stub))

    # ---- arg helpers ----

    def a(self, i):
        regs = {1: UC_X86_REG_RCX, 2: UC_X86_REG_RDX,
                3: UC_X86_REG_R8, 4: UC_X86_REG_R9}
        return self.uc.reg_read(regs[i])

    def stack_q(self, off):
        sp = self.uc.reg_read(UC_X86_REG_RSP)
        return struct.unpack("<Q", self.uc.mem_read(sp + off, 8))[0]

    def ret(self, val):
        self.uc.reg_write(UC_X86_REG_RAX, val & 0xFFFFFFFFFFFFFFFF)

    # ---- bump allocator ----

    def bump(self, size, zero=True):
        if size <= 0:
            size = 1
        p = align_up(self.heap_top, 16)
        self.heap_top = p + size + 16
        if self.heap_top > self.heap_limit:
            raise HarnessError(
                "堆 bump 分配器耗尽（%d MB，--mem-mb 可调大）；"
                "若分配尺寸异常巨大，先复查 handler 参数序" % self.args.mem_mb)
        if zero:
            try:
                self.uc.mem_write(p, b"\0" * min(size, 0x100000))
            except UcError as e:
                raise HarnessError("堆分配写零失败: %s" % e)
        return p

    # ---- stdin / stdout ----

    def feed_stdin(self, buf, n):
        n = max(0, n)
        chunk = self.stdin_data[self.stdin_pos:self.stdin_pos + n]
        self.stdin_pos += len(chunk)
        if chunk:
            self.uc.mem_write(buf, chunk)
        return len(chunk)

    def capture_stdout(self, buf, n):
        if n <= 0:
            return
        try:
            self.stdout += bytes(self.uc.mem_read(buf, n))
        except UcError:
            pass

    # ---- import dispatch ----

    def handle_import(self, dll, name):
        self.api_counts[name] = self.api_counts.get(name, 0) + 1
        if self.args.trace_api:
            line = "  [api] %s!%s(rcx=%#x rdx=%#x r8=%#x r9=%#x)" % (
                dll, name, self.a(1), self.a(2), self.a(3), self.a(4))
            self.api_log.append(line)
            print(line)
        h = getattr(self, "api_" + name, None)
        if h is None:
            fb = self.API_FALLBACKS.get(name)
            if fb is not None:
                h = lambda: fb(self)
        if h is not None:
            h()
            return
        msg = "未实现 API %s!%s" % (dll, name)
        if self.args.strict_api:
            self.stop = "strict-api: %s" % msg
            self.stop_kind = "harness-limit"
            self.uc.emu_stop()
            return
        if name not in self._warned_api:
            self._warned_api.add(name)
            print("  [警告] %s，按返回 0 继续（--strict-api 可改为止停）"
                  "（同名后续调用不再重复警告）" % msg, file=sys.stderr)
        self.api_log.append("  [unimplemented] %s!%s -> 0" % (dll, name))
        self.ret(0)

    # --- CRT memory/string helpers ---
    def api_memcpy(self):
        dst, src, n = self.a(1), self.a(2), self.a(3)
        if n:
            self.uc.mem_write(dst, bytes(self.uc.mem_read(src, n)))
        self.ret(dst)

    api_memmove = api_memcpy

    def api_memset(self):
        dst, c, n = self.a(1), self.a(2), self.a(3)
        if n:
            self.uc.mem_write(dst, bytes([c & 0xFF]) * n)
        self.ret(dst)

    def api_memcmp(self):
        p1, p2, n = self.a(1), self.a(2), self.a(3)
        b1 = bytes(self.uc.mem_read(p1, n)) if n else b""
        b2 = bytes(self.uc.mem_read(p2, n)) if n else b""
        d = 0
        for x, y in zip(b1, b2):
            if x != y:
                d = x - y
                break
        self.ret(d)

    def api_strlen(self):
        p, n = self.a(1), 0
        while self.uc.mem_read(p + n, 1) != b"\0":
            n += 1
            if n > 0x1000000:
                raise HarnessError("strlen 扫了 16MB 没见到 NUL，指针可疑")
        self.ret(n)

    # --- heap ---
    def api_GetProcessHeap(self):
        self.ret(HEAP_HANDLE)

    def api_HeapAlloc(self):
        self.ret(self.bump(self.a(3)))

    def api_HeapReAlloc(self):
        # HeapReAlloc(hHeap, flags, lpMem, dwBytes): 大小是第 4 参（R9），不是 R8！
        old_p, sz = self.a(3), self.a(4)
        if sz > self.heap_limit:
            raise HarnessError(
                "HeapReAlloc 请求 %#x 字节，异常巨大——复查是否拿错参数"
                "（大小在 R9，旧指针在 R8）" % sz)
        p = self.bump(sz, zero=False)
        self.uc.mem_write(p, b"\0" * min(sz, 0x100000))
        if old_p:
            try:
                self.uc.mem_write(p, bytes(self.uc.mem_read(old_p, sz)))
            except UcError:
                pass  # 旧块尺寸未知，越界就截断，保持 harness 不炸
        self.ret(p)

    def api_HeapFree(self):
        self.ret(1)

    def api_HeapSize(self):
        self.ret(0x1000)  # 谎报一个固定尺寸；精确语义不在本层

    # --- virtual memory ---
    def api_VirtualAlloc(self):
        addr, size = self.a(1), self.a(2)
        size = align_up(max(size, 1))
        if addr == 0:
            addr = align_up(self._va_top)
            self._va_top = addr + size
        try:
            self.uc.mem_map(align_down(addr), size,
                            UC_PROT_READ | UC_PROT_WRITE)
        except UcError as e:
            raise HarnessError("VirtualAlloc(%#x, %#x) 映射失败: %s"
                               % (addr, size, e))
        self.uc.mem_write(addr, b"\0" * min(size, 0x100000))
        self.ret(addr)

    def api_VirtualFree(self):
        self.ret(1)

    def api_VirtualProtect(self):
        old = self.a(4)
        if old:
            try:
                self.uc.mem_write(old, struct.pack("<I", 0x40))
            except UcError:
                pass
        self.ret(1)

    # --- handles / stdio ---
    def api_GetStdHandle(self):
        self.ret(PSEUDO_HANDLE)

    def api_GetConsoleMode(self):
        # 报"不是控制台"：Rust std 因此走 ReadFile/WriteFile 路径
        self.last_error = 50  # ERROR_NOT_SUPPORTED
        self.ret(0)

    def api_SetConsoleMode(self):
        self.ret(1)

    def api_ReadFile(self):
        # ReadFile(h, buf, n, &read, ov)
        buf, n, pread = self.a(2), self.a(3), self.a(4)
        got = self.feed_stdin(buf, n)
        if pread:
            self.uc.mem_write(pread, struct.pack("<I", got))
        if self.args.trace_api:
            print("  [ReadFile] -> %d bytes" % got)
        self.ret(1)

    def api_ReadConsoleA(self):
        buf, n, pread = self.a(2), self.a(3), self.a(4)
        got = self.feed_stdin(buf, n)
        if pread:
            self.uc.mem_write(pread, struct.pack("<I", got))
        self.ret(1)

    def api_ReadConsoleW(self):
        buf, n, pread = self.a(2), self.a(3), self.a(4)
        got = self.feed_stdin(buf, n)
        data = bytes(self.uc.mem_read(buf, got)).decode(
            "utf-8", "ignore").encode("utf-16-le")[:n]
        self.uc.mem_write(buf, data)
        if pread:
            self.uc.mem_write(pread, struct.pack("<I", len(data) // 2))
        self.ret(1)

    def api_WriteFile(self):
        # WriteFile(h, buf, n, &written, ov)
        buf, n, pwritten = self.a(2), self.a(3), self.a(4)
        self.capture_stdout(buf, n)
        if pwritten:
            self.uc.mem_write(pwritten, struct.pack("<I", n))
        self.ret(1)

    api_WriteConsoleA = api_WriteFile

    def api_WriteConsoleW(self):
        buf, n, pwritten = self.a(2), self.a(3), self.a(4)
        try:
            raw = bytes(self.uc.mem_read(buf, n * 2))
            self.stdout += raw.decode("utf-16-le", "replace").encode("utf-8")
        except UcError:
            pass
        if pwritten:
            self.uc.mem_write(pwritten, struct.pack("<I", n))
        self.ret(1)

    def api_NtReadFile(self):
        # NTSTATUS NtReadFile(h, event, apc, apcctx, &iosb, buf, len, &off, key)
        # 4 寄存器参 + 5 栈参：iosb=[rsp+0x28] buf=[rsp+0x30] len=[rsp+0x38]
        iosb, buf, ln = (self.stack_q(o) for o in (0x28, 0x30, 0x38))
        got = self.feed_stdin(buf, ln)
        if iosb:
            # IO_STATUS_BLOCK { Status; Information(ULONG_PTR, 偏移 8) }
            self.uc.mem_write(iosb, struct.pack("<QQ", 0, got))
        if self.args.trace_api:
            print("  [NtReadFile] -> %d bytes" % got)
        self.ret(0)  # STATUS_SUCCESS

    def api_NtWriteFile(self):
        iosb, buf, ln = (self.stack_q(o) for o in (0x28, 0x30, 0x38))
        self.capture_stdout(buf, ln)
        if iosb:
            self.uc.mem_write(iosb, struct.pack("<QQ", 0, ln))
        self.ret(0)

    def api_FlushFileBuffers(self):
        self.ret(1)

    def api_CloseHandle(self):
        self.ret(1)

    # --- InitOnce（Rust std Once 依赖；返回 0 会让调用方无限重试空转） ---
    def api_InitOnceBeginInitialize(self):
        # BOOL InitOnceBeginInitialize(PINIT_ONCE once, DWORD flags,
        #                              PVOID *lpContext, PVOID *lpParameter)
        once, lp_ctx = self.a(1), self.a(3)
        state, ctx = self.init_once.get(once, ("new", 0))
        if state == "done":
            # 已完成：*lpContext 非空告诉调用方"不用你初始化"
            if lp_ctx:
                self.uc.mem_write(lp_ctx, struct.pack("<Q", ctx or 2))
            self.ret(1)
            return
        # 未完成：标记 pending，*lpContext = NULL（fPending=TRUE，调用方负责跑初始化）
        self.init_once[once] = ("pending", 0)
        try:
            self.uc.mem_write(once, struct.pack("<Q", 1))
        except UcError:
            pass
        if lp_ctx:
            self.uc.mem_write(lp_ctx, struct.pack("<Q", 0))
        self.ret(1)

    def api_InitOnceComplete(self):
        # BOOL InitOnceComplete(PINIT_ONCE once, DWORD flags, PVOID lpContext)
        once, ctx = self.a(1), self.a(3)
        self.init_once[once] = ("done", ctx)
        try:
            self.uc.mem_write(once, struct.pack("<Q", (ctx | 2) & 0xFFFFFFFFFFFFFFFF))
        except UcError:
            pass
        self.ret(1)

    def api_RtlNtStatusToDosError(self):
        # NTSTATUS -> Win32 error code 的粗略映射，够用即可
        status = self.a(1) & 0xFFFFFFFF
        self.ret({0: 0, 0xC000000F: 2, 0xC0000034: 2,
                  0xC0000005: 998}.get(status, 87))

    # --- msvcrt 分配器族（windows-gnu 目标常见） ---
    def api_malloc(self):
        self.ret(self.bump(self.a(1)))

    def api_calloc(self):
        self.ret(self.bump(self.a(1) * self.a(2)))

    def api_realloc(self):
        old_p, sz = self.a(1), self.a(2)
        p = self.bump(sz, zero=False)
        if old_p:
            try:
                self.uc.mem_write(p, bytes(self.uc.mem_read(old_p, sz)))
            except UcError:
                pass
        self.ret(p)

    def api_free(self):
        self.ret(0)

    def api_strncmp(self):
        p1, p2, n = self.a(1), self.a(2), self.a(3)
        d = 0
        for i in range(min(n, 0x100000)):
            x = self.uc.mem_read(p1 + i, 1)[0]
            y = self.uc.mem_read(p2 + i, 1)[0]
            if x != y:
                d = x - y
                break
            if x == 0:
                break
        self.ret(d)

    def api_fwrite(self):
        # fwrite(ptr, size, nmemb, stream)：并入 stdout 捕获（stderr 也接住）
        ptr, size, nmemb = self.a(1), self.a(2), self.a(3)
        total = size * nmemb
        if 0 < total <= 0x1000000:
            self.capture_stdout(ptr, total)
        self.ret(nmemb)

    def api_exit(self):
        self.stop = "exit(code=%d)" % (self.a(1) & 0xFFFFFFFF)
        self.stop_kind = "exit"
        self.uc.emu_stop()

    api__cexit = api_exit
    api_TerminateProcess = api_exit

    def api_abort(self):
        self.stop = "guest 调用 abort()（疑似 panic/断言失败路径）"
        self.stop_kind = "guest-error"
        self.uc.emu_stop()

    api__amsg_exit = api_abort

    def api_Sleep(self):
        self.ret(0)

    # --- debug / timing ---
    def api_IsDebuggerPresent(self):
        self.ret(0)

    def api_CheckRemoteDebuggerPresent(self):
        pbool = self.a(3)
        if pbool:
            try:
                self.uc.mem_write(pbool, b"\0\0")
            except UcError:
                pass
        self.ret(1)

    def api_GetSystemTimeAsFileTime(self):
        p = self.a(1)
        if p:
            self.uc.mem_write(p, struct.pack("<Q", FIXED_FILETIME))

    api_GetSystemTimePreciseAsFileTime = api_GetSystemTimeAsFileTime

    def api_GetTickCount(self):
        self.ret(0x123456)

    api_GetTickCount64 = api_GetTickCount

    def api_QueryPerformanceCounter(self):
        p = self.a(1)
        if p:
            self.uc.mem_write(p, struct.pack("<Q", 0x100000))
        self.ret(1)

    def api_QueryPerformanceFrequency(self):
        p = self.a(1)
        if p:
            self.uc.mem_write(p, struct.pack("<Q", 10000000))
        self.ret(1)

    # --- sync / TLS (no-op + 简单槽) ---
    def _noop1(self):
        self.ret(1)

    def api_TlsAlloc(self):
        slot = 0
        while slot in self.tls:
            slot += 1
        self.tls[slot] = 0
        self.ret(slot)

    def api_TlsGetValue(self):
        self.ret(self.tls.get(self.a(1), 0))

    def api_TlsSetValue(self):
        self.tls[self.a(1)] = self.a(2)
        self.ret(1)

    def api_TlsFree(self):
        self.tls.pop(self.a(1), None)
        self.ret(1)

    # --- module / proc address ---
    def _module_handle(self):
        return self.pe.image_base

    def api_GetModuleHandleA(self):
        self.ret(self._module_handle())

    api_GetModuleHandleW = api_GetModuleHandleA
    api_GetModuleHandleExA = api_GetModuleHandleA
    api_GetModuleHandleExW = api_GetModuleHandleA

    def api_GetProcAddress(self):
        name_ptr = self.a(2)
        if name_ptr == 0 or name_ptr < 0x10000:  # 按序号导入
            self.ret(0)
            return
        try:
            raw = bytes(self.uc.mem_read(name_ptr, 256))
            name = raw.split(b"\0", 1)[0].decode("ascii", "replace")
        except UcError:
            self.ret(0)
            return
        self.ret(self.stub_by_name.get(name, 0))

    def api_GetModuleFileNameA(self):
        buf, n = self.a(2), self.a(3)
        s = os.path.basename(self.args.pe).encode() + b"\0"
        s = s[:n]
        if buf and n:
            self.uc.mem_write(buf, s)
        self.ret(len(s) - 1)

    def api_GetModuleFileNameW(self):
        buf, n = self.a(2), self.a(3)
        s = (os.path.basename(self.args.pe) + "\0").encode("utf-16-le")
        s = s[:n * 2]
        if buf and n:
            self.uc.mem_write(buf, s)
        self.ret(len(s) // 2 - 1)

    def api_LoadLibraryA(self):
        self.ret(self._module_handle())

    api_LoadLibraryW = api_LoadLibraryA
    api_LoadLibraryExA = api_LoadLibraryA
    api_LoadLibraryExW = api_LoadLibraryA

    def api_FreeLibrary(self):
        self.ret(1)

    def api_GetCommandLineA(self):
        if not self._cmdline_a:
            self._cmdline_a = self.bump(0x100)
            self.uc.mem_write(self._cmdline_a,
                              os.path.basename(self.args.pe).encode() + b"\0")
        self.ret(self._cmdline_a)

    def api_GetCommandLineW(self):
        if not self._cmdline_w:
            self._cmdline_w = self.bump(0x200)
            self.uc.mem_write(
                self._cmdline_w,
                (os.path.basename(self.args.pe) + "\0").encode("utf-16-le"))
        self.ret(self._cmdline_w)

    # --- last error ---
    def api_GetLastError(self):
        self.ret(self.last_error)

    def api_SetLastError(self):
        self.last_error = self.a(1) & 0xFFFFFFFF
        self.ret(0)

    # --- process exit ---
    def api_ExitProcess(self):
        self.stop = "ExitProcess(code=%d)" % (self.a(1) & 0xFFFFFFFF)
        self.stop_kind = "exit"
        self.uc.emu_stop()

    def api_RtlExitUserProcess(self):
        self.api_ExitProcess()

    # 名字 -> 方法 的查表分派（含临界区/SRW/异常过滤等 no-op 一族）
    API_FALLBACKS = {}  # 在类定义后填充

    # ---- hooks ----

    def hooks(self):
        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad_mem)

    def on_code(self, uc, address, size, _):
        self.insns += 1
        if self.insns > self.args.max_insns:
            self.stop = "max-insns (%d)" % self.args.max_insns
            self.stop_kind = "limit"
            uc.emu_stop()
            return
        if self.insns % 65536 == 0 and \
                time.monotonic() - self.t0 > self.args.timeout:
            self.stop = "timeout (%ss 墙钟)" % self.args.timeout
            self.stop_kind = "limit"
            uc.emu_stop()
            return
        if STUB_BASE < address < STUB_BASE + STUB_SIZE and \
                (address - STUB_BASE) % 16 == 0:
            ent = self.stub_by_addr.get(address)
            if ent is not None:
                try:
                    self.handle_import(*ent)
                except HarnessError as e:
                    self.stop = "harness: %s" % e
                    self.stop_kind = "harness-error"
                    uc.emu_stop()
                except UcError as e:
                    # handler 里 mem_read/write 炸了：guest 给了坏指针
                    self.stop = ("guest-error: API handler %s 内 %s"
                                 "（guest 传了坏指针？）" % (ent[1], e))
                    self.stop_kind = "guest-error"
                    uc.emu_stop()
            # 未登记的桩地址（或 STUB_BASE 本身）：预填的 ret 直接弹回
            return
        if address in self.args.break_success_set:
            self.stop = "success breakpoint hit @ 0x%x" % address
            self.stop_kind = "success"
            uc.emu_stop()
            return
        if address in self.args.break_fail_set:
            self.stop = "fail breakpoint hit @ 0x%x" % address
            self.stop_kind = "fail"
            uc.emu_stop()
            return

    def on_bad_mem(self, uc, access, address, size, value, _):
        # UC_MEM_{READ,WRITE,FETCH}_UNMAPPED = 19/20/21
        what = {19: "read", 20: "write", 21: "fetch"}.get(access, str(access))
        pc = uc.reg_read(UC_X86_REG_RIP)
        if access == 21 and address < 0x10000:
            self.stop = ("ret-flyout (RIP 取指飞到 %#x，main 正常 return 到 NULL "
                         "哨兵或空函数指针；若成功输出已打印，这就是正常终点)"
                         % address)
        else:
            self.stop = ("guest-error: unmapped %s @ %#x (size %d, RIP=%#x)"
                         % (what, address, size, pc))
        self.stop_kind = "guest-error"
        uc.emu_stop()
        return False

    # ---- run ----

    def run(self):
        args = self.args
        self.stdin_data = args.stdin_bytes
        sp = STACK_BASE + STACK_SIZE - 0x1000
        uc = self.uc
        uc.reg_write(UC_X86_REG_RSP, sp)
        uc.mem_write(sp, b"\0" * 0x800)
        uc.reg_write(UC_X86_REG_RCX, 0)
        uc.reg_write(UC_X86_REG_RDX, 0)
        uc.mem_write(sp, struct.pack("<Q", 0))  # return-to-NULL 哨兵
        try:
            uc.emu_start(args.entry, 0,
                         timeout=int(args.timeout * 1_000_000),
                         count=args.max_insns + 1)
        except UcError as e:
            self.guest_err = e
        if self.stop is None:
            if self.guest_err is None:
                self.stop = "finished (until 地址 0 处正常停住)"
                self.stop_kind = "finished"
            else:
                self.stop = "guest exception: %s" % self.guest_err
                self.stop_kind = "guest-error"
        return self.report()

    def report(self):
        final_rip = None
        try:
            final_rip = self.uc.reg_read(UC_X86_REG_RIP)
        except UcError:
            pass
        dumps = []
        for addr, ln in self.args.dump_state:
            try:
                data = bytes(self.uc.mem_read(addr, ln))
                dumps.append({"addr": "0x%x" % addr, "len": ln,
                              "hex": data.hex()})
            except UcError as e:
                dumps.append({"addr": "0x%x" % addr, "len": ln,
                              "error": str(e)})
        stdout_txt = bytes(self.stdout).decode("utf-8", "replace")
        rep = {
            "pe": self.args.pe,
            "image_base": "0x%x" % self.pe.image_base,
            "entry": "0x%x" % self.args.entry,
            "instructions": self.insns,
            "elapsed_sec": round(time.monotonic() - self.t0, 3),
            "stop_kind": self.stop_kind,
            "stop_reason": self.stop,
            "final_rip": ("0x%x" % final_rip) if final_rip is not None else None,
            "api_counts": dict(sorted(self.api_counts.items())),
            "stdout": stdout_txt,
            "dumps": dumps,
        }

        print("=== 整程序仿真报告 ===")
        print("  PE          : %s (ImageBase=0x%x)" %
              (self.args.pe, self.pe.image_base))
        print("  entry       : 0x%x" % self.args.entry)
        print("  执行指令数  : %d" % self.insns)
        print("  耗时        : %.3fs" % rep["elapsed_sec"])
        print("  停止类别    : %s" % self.stop_kind)
        print("  停止原因    : %s" % self.stop)
        print("  RIP 终值    : %s" % rep["final_rip"])
        print("  API 调用    : %s" % (
            ", ".join("%s x%d" % kv for kv in rep["api_counts"].items()) or "无"))
        if stdout_txt:
            print("  stdout 捕获 :")
            for line in stdout_txt.splitlines():
                print("    | %s" % line)
        for d in dumps:
            if "hex" in d:
                print("  dump %s:%d: %s" % (d["addr"], d["len"], d["hex"]))
            else:
                print("  dump %s:%d: [读取失败] %s"
                      % (d["addr"], d["len"], d["error"]))
        if self.guest_err is not None:
            print("  [guest 异常] %s（guest 执行炸了，非 harness 问题）"
                  % self.guest_err)

        if self.args.json:
            with open(self.args.json, "w", encoding="utf-8") as f:
                json.dump(rep, f, indent=2, ensure_ascii=False)
            print("  JSON -> %s" % self.args.json)
        return 0


# no-op / 恒真一族：临界区、SRW、异常过滤、环境杂项
for _n in ("InitializeCriticalSection", "InitializeCriticalSectionAndSpinCount",
           "EnterCriticalSection", "LeaveCriticalSection",
           "DeleteCriticalSection", "TryEnterCriticalSection",
           "AcquireSRWLockExclusive", "ReleaseSRWLockExclusive",
           "AcquireSRWLockShared", "ReleaseSRWLockShared",
           "TryAcquireSRWLockExclusive", "TryAcquireSRWLockShared",
           "SetUnhandledExceptionFilter", "AddVectoredExceptionHandler",
           "RemoveVectoredExceptionHandler", "SetThreadStackGuarantee",
           "SetConsoleCtrlHandler", "FreeEnvironmentStringsW",
           "FreeEnvironmentStringsA", "GetCurrentProcess", "GetCurrentThread",
           "GetCurrentProcessId", "GetCurrentThreadId", "SetErrorMode",
           "InitializeSListHead", "RtlCaptureContext",
           ):
    ProgramEmu.API_FALLBACKS[_n] = ProgramEmu._noop1

# GetCurrentProcessId/GetCurrentThreadId 返回 id 更有意义，但恒 1 也够 console 程序用

STUB_LIST = sorted(
    [n[4:] for n in dir(ProgramEmu) if n.startswith("api_")]
    + list(ProgramEmu.API_FALLBACKS))


def main():
    ap = argparse.ArgumentParser(
        description="整程序 Unicorn 仿真 harness：PE 装载 + IAT 桩 + Win32 stub "
                    "+ stdin 投喂 + 成功/失败断点（console 型校验程序专用）")
    ap.add_argument("pe", nargs="?", help="待仿真 PE 文件（x86-64 PE32+）")
    ap.add_argument("--entry", type=parse_int,
                    help="入口地址（绝对 VA，通常是从 runtime 里抠出来的 main）")
    ap.add_argument("--stdin", dest="stdin_text", help="喂给标准输入的文本")
    ap.add_argument("--stdin-file", help="从文件读 stdin 字节（与 --stdin 互斥）")
    ap.add_argument("--break-success", type=parse_addr_list, default=[],
                    metavar="0xADDR[,...]", help="命中即停，报告 success")
    ap.add_argument("--break-fail", type=parse_addr_list, default=[],
                    metavar="0xADDR[,...]", help="命中即停，报告 fail")
    ap.add_argument("--max-insns", type=parse_int, default=50000000,
                    help="指令数上限（默认 50M）")
    ap.add_argument("--timeout", type=float, default=120,
                    help="超时秒数，墙钟+Unicorn 双保险（默认 120）")
    ap.add_argument("--mem-mb", type=int, default=256,
                    help="堆区大小 MB，bump 分配器（默认 256）")
    ap.add_argument("--stub-list", action="store_true",
                    help="列出内建 Win32 stub 清单后退出")
    ap.add_argument("--trace-api", action="store_true",
                    help="打印每次 API 调用与寄存器参数摘要")
    ap.add_argument("--strict-api", action="store_true",
                    help="遇到未实现 API 止停报错（默认警告并返回 0）")
    ap.add_argument("--dump-state", type=parse_dump_spec, default=[],
                    metavar="0xADDR:LEN[,...]", help="停止时 dump 指定内存")
    ap.add_argument("--json", help="JSON 报告输出路径")
    a = ap.parse_args()

    if a.stub_list:
        print("内建 stub 清单（%d 个）：" % len(STUB_LIST))
        for n in STUB_LIST:
            print("  %s" % n)
        return 0

    # ---- harness 自身错误（参数/文件问题），与 guest 错误严格区分 ----
    if not a.pe:
        print("[用法错误] 缺少 PE 文件参数（或先用 --stub-list）", file=sys.stderr)
        return 2
    if a.entry is None:
        print("[用法错误] 必须给 --entry 0x<main地址>", file=sys.stderr)
        return 2
    if a.stdin_text is not None and a.stdin_file is not None:
        print("[用法错误] --stdin 与 --stdin-file 互斥", file=sys.stderr)
        return 2
    if a.stdin_file is not None:
        try:
            a.stdin_bytes = open(a.stdin_file, "rb").read()
        except OSError as e:
            print("[harness 错误] --stdin-file 读取失败: %s" % e, file=sys.stderr)
            return 4
    elif a.stdin_text is not None:
        a.stdin_bytes = a.stdin_text.encode("utf-8") + b"\n"
    else:
        a.stdin_bytes = b""
    a.break_success_set = set(a.break_success)
    a.break_fail_set = set(a.break_fail)

    try:
        emu = ProgramEmu(a)
        emu.setup()
    except HarnessError as e:
        print("[harness 错误] %s（非 guest 问题）" % e, file=sys.stderr)
        return 4

    emu.hooks()
    return emu.run()


if __name__ == "__main__":
    sys.exit(main())
