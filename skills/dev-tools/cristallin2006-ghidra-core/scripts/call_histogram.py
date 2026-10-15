#!/usr/bin/env python
"""call_histogram.py - CALL/JMP target histogram from disassembly.

Host-side tool (any Python 3.8+, stdlib only). Use this when the decompiler
output is one giant inlined blob (e.g. a 1747-line main): stop reading
pseudocode, disassemble instead, and count CALL targets. N repeated call
sites to the same address == the algorithm skeleton (dispatcher / per-slot
verifier / library function) is enumerable slot by slot.

Usage:
  python rpc_driver.py @out/disasm.json disassemble <bin>
  python call_histogram.py out/disasm.json [--min 3] [--json out/hist.json]
  python call_histogram.py disasm.txt            # 纯反汇编文本也可以

Input is auto-detected: rpc_driver disassemble JSON (result.listing text,
or a JSON instructions array), or any plain disassembly text.

Exit codes: 0 ok, 1 usage error, 2 no CALL/JMP targets found in input.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

# 覆盖 Ghidra listing (CALL 0x0040a800) 与 objdump 风格 (call 40aba0 <sym>)
TARGET_RE = re.compile(
    r"\b(?:CALL|JMP)\b[^\S\n]+(?:\w+\s+ptr\s+)?\[?(0x[0-9a-fA-F]+|[0-9a-fA-F]{6,16})\b",
    re.I,
)


def extract_text(data):
    """任意输入 -> 待扫描文本。返回 (text, source_kind)。"""
    try:
        d = json.loads(data)
    except ValueError:
        return data, "text"
    node = d.get("result", d) if isinstance(d, dict) else d
    if isinstance(node, dict):
        if isinstance(node.get("listing"), str):
            return node["listing"], "json-listing"
        insns = node.get("instructions")
        if isinstance(insns, list):
            lines = []
            for ins in insns:
                if isinstance(ins, str):
                    lines.append(ins)
                elif isinstance(ins, dict):
                    mn = ins.get("mnemonic", "")
                    ops = ins.get("operands", ins.get("op_str", ""))
                    lines.append("%s %s" % (mn, ops))
            return "\n".join(lines), "json-instructions"
    return data, "text"


def main():
    ap = argparse.ArgumentParser(
        description="CALL/JMP 目标地址直方图：重复调用点 = 可逐槽枚举的算法骨架")
    ap.add_argument("input", help="disassemble 的 @out JSON 或纯反汇编文本")
    ap.add_argument("--min", type=int, default=3,
                    help="高亮为重复调用点的出现次数阈值（默认 3）")
    ap.add_argument("--json", help="JSON 报告输出路径")
    a = ap.parse_args()

    try:
        data = open(a.input, encoding="utf-8", errors="replace").read()
    except OSError as e:
        print("[错误] 无法读取输入文件: %s" % e, file=sys.stderr)
        return 1

    text, kind = extract_text(data)
    hist = Counter(int(m, 16) for m in TARGET_RE.findall(text))
    total = sum(hist.values())

    print("输入格式: %s | CALL/JMP 总数: %d | 不同目标: %d" % (kind, total, len(hist)))
    if not hist:
        print("[结论] 未找到任何 CALL/JMP 目标，检查输入格式。")
        return 2

    rows = sorted(hist.items(), key=lambda kv: (-kv[1], kv[0]))
    print("\n=== 目标地址直方图（按次数降序）===")
    for addr, cnt in rows:
        mark = ""
        if cnt >= a.min:
            mark = "  <== 重复调用点（疑似分发器/校验体/库函数）"
        print("  0x%016x  %6d%s" % (addr, cnt, mark))

    hot = [(ad, c) for ad, c in rows if c >= a.min]
    print("\n[结论] ≥%d 次的目标 %d 个：" % (a.min, len(hot))
          + ("逐槽枚举这些调用点的入参即可暴露算法骨架。" if hot
             else "无明显重复调用点，骨架可能不在 CALL 密度上。"))

    if a.json:
        json.dump(
            {
                "source": kind,
                "total_calls": total,
                "unique_targets": len(hist),
                "threshold": a.min,
                "histogram": [
                    {"target": "0x%x" % ad, "count": c, "repeated": c >= a.min}
                    for ad, c in rows
                ],
            },
            open(a.json, "w", encoding="utf-8"), indent=2, ensure_ascii=False,
        )
        print("JSON -> %s" % a.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
