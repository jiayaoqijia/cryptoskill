#!/usr/bin/env python
"""ssa_reconstruct.py - 从 ssa_trace 事件流重建直线程序 + 裸字面量解析（ctf-patterns §12.2 后半链）。

Host-side tool (any Python 3.8+, stdlib only; 纯本地文件工具，不经 daemon)。

为什么需要（858e13b3 复盘 §5.3）：Cython 一旦把值 C 化（PyLong_AsLong /
int.from_bytes / to_bytes 往返），追踪链就断，字面量会以"神奇常数"形式出现在
事件里（状态字节打包、<<4、>>5）。本脚本先把事件流变可读直线程序，再用一个小
公式集合解释每个高频裸字面量（identity / sw / sw<<16 / 位移 / *16，以及两值
打包 sw(a)<<16|sw(b) 四式）；解不出的一律标 ?? 交人工，不猜。

用法:
  ssa_reconstruct.py <trace.json> [--out recon.txt] [--lits lits.json] [--top N]

  <trace.json> 是 ssa_trace.py --out 的产出（{"events": [{"n","op","l","r","v"}]}）。
  直线程序行格式与 peel_inverse.py 的输入约定一致：
    t12 = (t5) + (7)            二元算术/位运算
    u3  = NEG(t8)               一元（NEG/ABS/INV/POW）
    k2  = RNG_getrandbits([8])  RNG 抽样
    b4  = sum([...])            缓存 builtin 观测（BLK:*）
    M1  = CALL__p1([...])       --wrap 方法调用
    u9  = TO_BYTES(t3, [...])   C 化断链点

exit: 0 正常; 2 用法/输入文件错误。
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import sys

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


def sw(x):
    return ((x & 0xFF) << 8) | (x >> 8)


def render(e):
    op, n = e["op"], e["n"]
    l, r = e.get("l"), e.get("r")
    if op.startswith("RNG:"):
        return "%s = RNG_%s(%s)" % (n, op[4:], l)
    if op.startswith("BLK:"):
        return "%s = %s(%s)" % (n, op[4:], l)
    if op.startswith("CALL:"):
        return "%s = %s(%s)" % (n, op, l)
    if op == "TO_BYTES":
        return "%s = TO_BYTES(%s, %s)" % (n, l, r)
    if r is None:
        return "%s = %s(%s)" % (n, op, l)
    return "%s = (%s) %s (%s)" % (n, l, op, r)


def candidates(v):
    yield "identity", v
    yield "sw", sw(v)
    yield "sw<<16", sw(v) << 16
    for k in (4, 5, 8, 16):
        yield "<<%d" % k, v << k
        yield ">>%d" % k, v >> k
    yield "*16", v * 16


def explain_literals(events, pool_size=4000):
    vals = [e["v"] for e in events if isinstance(e.get("v"), int)]
    pool = sorted(set(vals), key=lambda x: -abs(x))[:pool_size]
    lits = collections.Counter()
    for e in events:
        for k in ("l", "r"):
            v = e.get(k)
            if isinstance(v, int) and v > 0xFFFF:
                lits[v] += 1
    idx = {}
    for v in pool:
        for name, c in candidates(v):
            idx.setdefault(c, []).append("%s(%d)" % (name, v))
    inv_sw = {}
    for v in pool:
        inv_sw.setdefault(sw(v), v)
    pool_set = set(pool)

    def pack_hits(L):
        hi, lo = (L >> 16) & 0xFFFF, L & 0xFFFF
        out = []
        for hn, a in (("sw", inv_sw.get(hi)), ("id", hi if hi in pool_set else None)):
            for ln, b in (("sw", inv_sw.get(lo)), ("id", lo if lo in pool_set else None)):
                if a is not None and b is not None:
                    out.append("(%s(%d)<<16)|%s(%d)" % (hn, a, ln, b))
        return out[:3]

    rows = []
    for L, cnt in lits.most_common():
        hits = (idx.get(L, []) or [])[:2] + pack_hits(L)
        rows.append((L, cnt, hits))
    return rows


def main():
    ap = argparse.ArgumentParser(prog="ssa_reconstruct.py")
    ap.add_argument("trace", help="ssa_trace.py --out 的 trace JSON")
    ap.add_argument("--out", help="直线程序落盘路径（不给则只打印统计与字面量报告）")
    ap.add_argument("--lits", help="字面量频次 JSON 落盘路径")
    ap.add_argument("--top", type=int, default=25,
                    help="字面量报告打印条数（默认 25）")
    args = ap.parse_args()

    try:
        with open(args.trace, encoding="utf-8") as fh:
            payload = json.load(fh)
        events = payload["events"]
        if not isinstance(events, list):
            raise TypeError("events 不是数组")
    except (OSError, ValueError, KeyError, TypeError) as e:
        print("trace 读取失败: %s" % e, file=sys.stderr)
        return 2

    lines = [render(e) for e in events]
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
    print("直线程序 %d 行%s" % (len(lines), " -> " + args.out if args.out else ""))
    peel = os.path.join(os.path.dirname(os.path.abspath(__file__)), "peel_inverse.py")
    print("下一步（铁律 6 闸，不是建议）：python3 %s %s —— 任何求逆/z3/SMT 之前先查掩码依赖图，"
          "检出滞后递推段就逐层手工剥离，无干净结构才放行 SMT"
          % (peel, args.out or "<recon.txt> --out 落盘后再跑本步>"))

    rows = explain_literals(events)
    unresolved = sum(1 for _, _, h in rows if not h)
    print("裸字面量(>0xffff): %d 种，已解析 %d / 待人工 %d"
          % (len(rows), len(rows) - unresolved, unresolved))
    for L, cnt, hits in rows[: args.top]:
        if hits:
            print("LIT %-18d x%-3d = %s" % (L, cnt, " | ".join(hits)))
        else:
            print("LIT %-18d x%-3d = ??  (需人工/加公式：可能是两值打包 sw(a)<<16|sw(b))"
                  % (L, cnt))
    if args.lits:
        with open(args.lits, "w", encoding="utf-8") as fh:
            json.dump([{"lit": L, "count": c} for L, c, _ in rows], fh)
        print("lits:", args.lits)
    return 0


if __name__ == "__main__":
    sys.exit(main())
