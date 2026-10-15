#!/usr/bin/env python
"""frame_map.py - 栈帧槽位归属表（判例H 复盘 §9.6）。

Host-side tool (any Python 3.8+, stdlib only). 伪码的 local_XXXX 命名不可信：
重叠栈槽会同名（同一个 local_3e8 既是 256 字节 S 盒又是 Vec）。本工具抛开
伪码，直接从反汇编按 RSP 偏移重建栈布局：每个槽位的首次写入（指令地址 +
写入宽度）与后续读取全部归账，同槽被两种不兼容宽度使用即标可疑——那就是
伪码重叠命名的真身。

数据来源：rpc_driver.py -> basic-blocks（定函数范围）+ 分页 disassemble
（--count 上限 1000，自动翻页；请求地址落入未反汇编间隙时 daemon 自动
前跳，分页按实际返回推进）。

Usage:
  python rpc_driver.py ensure <binary>          # daemon 未起时先 ensure
  python frame_map.py <binary> <func-addr> [--json out]

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
from collections import Counter
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

RPC_DRIVER = Path(__file__).resolve().parent / "rpc_driver.py"
PAGE = 1000  # disassemble --count 上限


class RpcError(Exception):
    def __init__(self, message, daemon=False):
        super().__init__(message)
        self.daemon = daemon


def rpc_call(binary, command, *args, timeout=300):
    """subprocess 调同目录 rpc_driver.py；@out 落临时文件再读 JSON
    （铁律 3：大输出必须落文件，不走 stdout 管道）。"""
    fd, out = tempfile.mkstemp(prefix="dsh_fm_", suffix=".json")
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


def fetch_function(binary, func):
    """basic-blocks 定函数范围 + 分页 disassemble，返回 (bb, insns)。"""
    bb = rpc_call(binary, "basic-blocks", func, "-l", "2000")
    blocks = bb.get("blocks") or []
    if not blocks:
        raise RpcError("函数没有基本块（地址有误或未完成分析）: %s" % func)
    ranges = sorted((int(b["start"], 16), int(b["end"], 16)) for b in blocks)
    lo, hi = ranges[0][0], ranges[-1][1]
    insns, addr = [], lo
    while addr <= hi:
        res = rpc_call(binary, "disassemble", "0x%x" % addr,
                       "-n", str(PAGE), "--with-instructions")
        page = res.get("instructions") or []
        if not page:
            break
        for ins in page:
            x = int(ins["address"], 16)
            if any(s <= x <= e for s, e in ranges):
                insns.append(ins)
        nxt = int(page[-1]["address"], 16) + int(page[-1].get("length") or 1)
        if nxt <= addr:
            break
        addr = nxt
        if len(page) < PAGE:
            break
    return bb, insns


SLOT_RE = re.compile(
    r"(byte|word|dword|qword|xmmword) ptr \[RSP(?: \+ 0x([0-9a-fA-F]+))?\]")
BARE_SLOT_RE = re.compile(r"\[RSP(?: \+ 0x([0-9a-fA-F]+))?\]")
SUB_RSP_RE = re.compile(r"^RSP,0x([0-9a-fA-F]+)$")
WIDTHS = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16}
WRITE_MN = {"MOV", "MOVDQA", "MOVDQU", "MOVAPS", "MOVUPS", "MOVSS", "MOVSD",
            "MOVNTDQ", "MOVNTI", "XCHG"}


def scan_slots(insns):
    """返回 (frame_size, {offset: slot})；slot 记首写/写次数/读次数/宽度集。"""
    slots, frame = {}, None
    for ins in insns:
        mn, ops = ins.get("mnemonic", ""), ins.get("operands") or ""
        if frame is None and mn == "SUB":
            m = SUB_RSP_RE.match(ops.strip())
            if m:
                frame = int(m.group(1), 16)
        m = SLOT_RE.search(ops)
        if m:
            off = int(m.group(2) or "0", 16)
            width = WIDTHS[m.group(1)]
        else:
            m = BARE_SLOT_RE.search(ops)
            if not m:
                continue
            off, width = int(m.group(1) or "0", 16), None
        is_write = mn in WRITE_MN and "[RSP" in ops.split(",", 1)[0]
        s = slots.setdefault(off, {"first_write": None, "writes": 0,
                                   "reads": 0, "widths": Counter()})
        if width:
            s["widths"][width] += 1
        if is_write:
            s["writes"] += 1
            if s["first_write"] is None:
                s["first_write"] = (int(ins["address"], 16), mn, width)
        else:
            s["reads"] += 1
    return frame, slots


def main():
    ap = argparse.ArgumentParser(
        description="栈帧槽位归属表：按 RSP 偏移重建栈布局，标出多宽度可疑槽")
    ap.add_argument("binary", help="样本路径（须经 rpc_driver.py ensure 加载）")
    ap.add_argument("func", help="函数地址（如 0x40b2e0）或函数名")
    ap.add_argument("--json", help="JSON 报告输出路径")
    a = ap.parse_args()
    if not Path(a.binary).is_file():
        print("[错误] 样本文件不存在: %s" % a.binary, file=sys.stderr)
        return 1

    try:
        bb, insns = fetch_function(a.binary, a.func)
    except RpcError as e:
        print("[错误] %s" % e, file=sys.stderr)
        if e.daemon:
            print("[提示] Ghidra daemon 不可达或样本未加载，先执行：", file=sys.stderr)
            print("  python %s ensure %s" % (RPC_DRIVER, a.binary), file=sys.stderr)
            return 3
        return 2

    frame, slots = scan_slots(insns)
    print("=== 栈帧归属: %s @ %s ===" % (bb.get("name", a.func),
                                      bb.get("address", a.func)))
    print("指令 %d 条 | 帧大小: %s | 栈槽 %d 个"
          % (len(insns), ("0x%x" % frame) if frame is not None else "未识别 SUB RSP",
             len(slots)))

    suspect = []
    print("\n偏移区间          首写指令                 写    读    宽度")
    for off in sorted(slots):
        s = slots[off]
        ws = sorted(s["widths"])
        fw = s["first_write"]
        fw_txt = ("0x%x %s/%s" % (fw[0], fw[1],
                  {1: "byte", 2: "word", 4: "dword", 8: "qword",
                   16: "xmmword"}.get(fw[2], "?")) if fw else "-（只读未写）")
        span_hi = off + ((fw[2] if fw else None) or (max(ws) if ws else 1))
        mark = ""
        if len(ws) > 1:
            mark = "  <== 可疑：同槽 %s 种宽度" % "/".join(map(str, ws))
            suspect.append((off, ws, fw_txt))
        print("+0x%04x..+0x%04x  %-24s %-4d  %-4d  {%s}%s"
              % (off, span_hi, fw_txt, s["writes"], s["reads"],
                 ",".join(map(str, ws)), mark))

    print("\n=== 汇总 ===")
    print("可疑槽位 %d 个（同槽多宽度 = 伪码重叠命名高发区，按区间重新归账）。"
          % len(suspect))
    for off, ws, fw in suspect:
        print("  +0x%x 宽度%s 首写 %s" % (off, ws, fw))
    if a.json:
        json.dump({"function": bb.get("name"), "frame_size": frame,
                   "slots": [{"offset": "0x%x" % o,
                              "first_write": slots[o]["first_write"],
                              "writes": slots[o]["writes"],
                              "reads": slots[o]["reads"],
                              "widths": sorted(slots[o]["widths"]),
                              "suspect": len(slots[o]["widths"]) > 1}
                             for o in sorted(slots)]},
                  open(a.json, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print("JSON -> %s" % a.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
