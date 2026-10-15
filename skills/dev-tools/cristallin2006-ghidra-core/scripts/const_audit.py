#!/usr/bin/env python
"""const_audit.py - 伪码常量对照审计（判例H 复盘 §9.6）。

Host-side tool (any Python 3.8+, stdlib only). 反编译器的常量渲染会漂移：
判例H 样本 255 处小整数被渲染成地址（&DAT_00000006 实为长度 6）——
必须机械化对照，不许肉眼认账。

三类审计：
  A) &DAT_0000xxxx  小整数渲染成地址：直接给出真实小整数值；
  B) DAT_00xxxxxxxx 数据引用：read-bytes 读该地址 16 字节，输出
     "伪码渲染文本 vs 实际字节" 对照行；地址不可读时按 memory-map
     区分 .bss 未初始化全局（合法）与真正的渲染漂移；
  C) (xxx **)0xXXXXXX 指针化字面值：读该地址及前 4 字节上下文，
     落在 ASCII 串中部先判"中部嫌疑"，再 xrefs-to 查反汇编——存在
     真实 LEA/imm 引用则降级为「合法常量（字符串中部指针）」（如
     判例H 中 0x442f99 = "FLAG{" 的 "LAG{" 后缀 needle，0x40bffd
     的 LEA 真实立即数，非漂移）；反汇编找不到对应立即数才标漂移。

Usage:
  python rpc_driver.py ensure <binary>          # daemon 未起时先 ensure
  python const_audit.py <binary> <func-addr> [--json out]

Exit codes: 0 ok, 1 usage error, 2 分析失败, 3 daemon 不可达（先 ensure）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

RPC_DRIVER = Path(__file__).resolve().parent / "rpc_driver.py"


class RpcError(Exception):
    def __init__(self, message, daemon=False):
        super().__init__(message)
        self.daemon = daemon


def rpc_call(binary, command, *args, timeout=300):
    """subprocess 调同目录 rpc_driver.py；@out 落临时文件再读 JSON
    （铁律 3：大输出必须落文件，不走 stdout 管道）。"""
    fd, out = tempfile.mkstemp(prefix="dsh_ca_", suffix=".json")
    os.close(fd)
    cmd = [sys.executable, str(RPC_DRIVER), "@" + out, command, str(binary)]
    cmd += [str(a) for a in args]
    proc = None
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        raw = Path(out).read_text(encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        raise RpcError("rpc_driver 调用超时（%ds），daemon 可能未就绪" % timeout, True)
    except OSError as e:
        raise RpcError("rpc_driver 调用失败: %s" % e, True)
    finally:
        try:
            os.unlink(out)
        except OSError:
            pass
    if not raw.strip():
        tail = (((proc.stderr or "") + (proc.stdout or "")).strip()[:400]
                if proc else "")
        raise RpcError("rpc_driver 无 JSON 输出。%s" % tail, True)
    try:
        data = json.loads(raw)
    except ValueError:
        raise RpcError("rpc_driver 输出不是 JSON: %s" % raw[:300], True)
    if not data.get("ok"):
        blob = json.dumps(data, ensure_ascii=False)
        daemon = any(k in blob for k in ("auto-ensure", "NotRunning", "daemon",
                                         "load failed", "binary not found"))
        raise RpcError("%s 失败: %s" % (command, data.get("message")
                                        or data.get("error")), daemon)
    return data.get("result") or {}


SMALL_ADDR_RE = re.compile(r"&DAT_0000([0-9a-fA-F]{4})\b")
DATA_RE = re.compile(r"\bDAT_00(?!00)([0-9a-fA-F]{6})\b")
PTRCAST_RE = re.compile(r"\*\s*\*+\s*\)\s*0x([0-9a-fA-F]{5,8})\b")


def ascii_view(bs):
    return "".join(chr(b) if 32 <= b < 127 else "." for b in bs)


def read_hex(binary, addr, length):
    """返回 bytes；读不出返回 None。"""
    try:
        res = rpc_call(binary, "read-bytes", "0x%x" % addr, str(length))
        return bytes.fromhex(res.get("hex") or "")
    except RpcError:
        return None


def fetch_segments(binary):
    """memory-map 段表；失败时返回空表（判定退化为 可读/不可读）。"""
    try:
        res = rpc_call(binary, "memory-map")
        return [(int(s["start"], 16), int(s["end"], 16),
                 s.get("name", "?"), bool(s.get("initialized", True)))
                for s in res.get("segments") or []]
    except (RpcError, KeyError, ValueError):
        return []


def has_code_ref(binary, addr):
    """xrefs-to 检查该地址是否被真实指令（LEA/立即数）引用过（审计问题 5）。

    指向字符串中部的合法指针（Rust/Go two-way、memchr、后缀比较的 needle）
    在反汇编里必有真实 LEA/imm 引用；只有伪码里出现地址、反汇编里找不到
    对应立即数时才是渲染漂移。返回 (是否被引用, 来源描述)；查询失败按
    无引用处理（保守，不误抑制漂移判定）。
    """
    try:
        res = rpc_call(binary, "xrefs-to", "0x%x" % addr)
    except RpcError:
        return False, None
    for r in res.get("xrefs") or []:
        if r.get("from_function"):
            return True, "%s @ %s (%s)" % (r["from_function"],
                                           r.get("from_address"),
                                           r.get("type"))
    return False, None


def unreadable_verdict(segments, addr):
    """read-bytes 失败时区分 .bss 未初始化全局与真正的渲染漂移。"""
    for lo, hi, name, init in segments:
        if lo <= addr <= hi:
            if not init:
                return "BSS 未初始化全局（%s 段，引用合法，运行时才赋值）" % name
            return "不可读（落在 %s 段但读取失败，需人工核对）" % name
    return "漂移（地址不在任何段内，渲染值不可信）"


def main():
    ap = argparse.ArgumentParser(
        description="伪码常量对照审计：小整数嫌疑 + DAT_ 引用逐条字节对照")
    ap.add_argument("binary", help="样本路径（须经 rpc_driver.py ensure 加载）")
    ap.add_argument("func", help="函数地址（如 0x40b2e0）或函数名")
    ap.add_argument("--json", help="JSON 报告输出路径")
    a = ap.parse_args()
    if not Path(a.binary).is_file():
        print("[错误] 样本文件不存在: %s" % a.binary, file=sys.stderr)
        return 1

    try:
        dec = rpc_call(a.binary, "decompile", a.func)
    except RpcError as e:
        print("[错误] %s" % e, file=sys.stderr)
        if e.daemon:
            print("[提示] Ghidra daemon 不可达或样本未加载，先执行：", file=sys.stderr)
            print("  python %s ensure %s" % (RPC_DRIVER, a.binary), file=sys.stderr)
            return 3
        return 2

    c_code = dec.get("c_code") or ""
    segments = fetch_segments(a.binary)
    lines = c_code.split("\n")
    print("=== 常量审计: %s @ %s（伪码 %d 行）==="
          % (dec.get("name", a.func), dec.get("address", a.func), len(lines)))

    small, data_refs, ptr_casts = [], {}, {}
    for ln, line in enumerate(lines, 1):
        for m in SMALL_ADDR_RE.finditer(line):
            small.append((ln, m.group(0), int(m.group(1), 16)))
        for m in DATA_RE.finditer(line):
            data_refs.setdefault(int(m.group(1), 16), [ln, m.group(0), 0])
            data_refs[int(m.group(1), 16)][2] += 1
        for m in PTRCAST_RE.finditer(line):
            v = int(m.group(1), 16)
            if v >= 0x10000:
                ptr_casts.setdefault(v, [ln, "0x%x" % v, 0])
                ptr_casts[v][2] += 1

    report = {"small_int_suspects": [], "data_refs": [], "ptr_casts": []}

    print("\n--- A) 小整数渲染成地址（&DAT_0000xxxx）: %d 处 ---" % len(small))
    for ln, txt, val in small:
        print("  行 %-5d %-18s 判定: 小整数嫌疑——该处字面值很可能是小整数 %d (0x%x)，不是地址"
              % (ln, txt, val, val))
        report["small_int_suspects"].append(
            {"line": ln, "rendered": txt, "likely_value": val})

    print("\n--- B) DAT_00xxxxxxxx 数据引用对照: %d 个地址 ---" % len(data_refs))
    for addr in sorted(data_refs):
        ln, txt, cnt = data_refs[addr]
        bs = read_hex(a.binary, addr, 16)
        if bs is None:
            verdict = unreadable_verdict(segments, addr)
            actual = None
        else:
            verdict = "对照行（可读，请按语义核对）"
            actual = bs.hex()
        print("  行 %-5d %-14s x%d  判定: %s" % (ln, txt, cnt, verdict))
        if bs is not None:
            print("           实际字节: %s  |%s|" % (bs.hex(), ascii_view(bs)))
        report["data_refs"].append({"line": ln, "rendered": txt, "count": cnt,
                                    "verdict": verdict, "actual_hex": actual})

    print("\n--- C) 指针化字面值（字符串中部指针/渲染漂移甄别）: %d 个 ---" % len(ptr_casts))
    for addr in sorted(ptr_casts):
        ln, txt, cnt = ptr_casts[addr]
        ctx = read_hex(a.binary, addr - 4, 20) if addr >= 4 else None
        bs = ctx[4:] if ctx is not None else read_hex(a.binary, addr, 16)
        if bs is None:
            verdict, actual = unreadable_verdict(segments, addr), None
        else:
            mid = (ctx is not None and 32 <= ctx[3] < 127 and 32 <= ctx[4] < 127)
            if mid:
                refd, src = has_code_ref(a.binary, addr)
                verdict = ("合法常量（字符串中部指针，反汇编存在真实引用 %s）" % src
                           if refd else
                           "漂移嫌疑：落在 ASCII 数据中部且反汇编中无对应立即数，"
                           "真实地址很可能在附近")
            else:
                verdict = "对照行（可读，请按语义核对）"
            actual = bs.hex()
        print("  行 %-5d %-10s x%d  判定: %s" % (ln, txt, cnt, verdict))
        if bs is not None:
            print("           实际字节: %s  |%s|" % (bs.hex(), ascii_view(bs)))
        report["ptr_casts"].append({"line": ln, "rendered": txt, "count": cnt,
                                    "verdict": verdict, "actual_hex": actual})

    print("\n=== 汇总 ===")
    print("小整数嫌疑 %d 处 | DAT_ 对照 %d 个地址 | 指针化字面值 %d 个。"
          % (len(small), len(data_refs), len(ptr_casts)))
    print("所有「漂移/嫌疑」条目的字面值禁止直接引用，按实际字节重新归账。")
    if a.json:
        json.dump(report, open(a.json, "w", encoding="utf-8"),
                  indent=2, ensure_ascii=False)
        print("JSON -> %s" % a.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
