#!/usr/bin/env python
"""decomp_lint.py - mechanical "physical exam" for decompiled pseudocode.

Host-side tool (any Python 3.8+, stdlib only). Runs BEFORE reading any
pseudocode: mechanically screens out untrustworthy decompiler output so the
agent never quotes poisoned C as evidence. Two verdicts:

  - fatal functions: pseudocode must NOT be quoted (jumptable not recovered,
    indirect JMP rendered as CALL, too many branches, ...). Read the bytes
    and decode rel32 tables by hand instead.
  - render traps: literals at those spots are untrustworthy (vectorized
    auVar rendering, CONCAT/SUB16 splits, small integers rendered as
    &DAT_0000xxxx addresses, ...) and must be cross-checked against bytes.

尾调用甄别（审计 A5）：Ghidra 的 "Could not recover jumptable" 同时被
函数尾声的尾调用触发（ADD RSP,imm / POP×N / LEAVE 之后 JMP reg），
不是跳转表；此时同一条 JMP 还会带出 "Treating indirect jump as call"
与 "Too many branches"（同一注释行内）。给 --binary 后，本工具对
「fatal 警告全部来自间接跳转族」的函数走 rpc 取每个 jumptable 警告
地址附近的反汇编：所有地址都是 JMP reg 紧邻尾声序列（允许中间夹
MOV/MOVZX 传参）→ 判为尾调用（良性），不计入 fatal，单列一类输出；
任一地址取不到反汇编或不像尾声 → 维持 fatal。不给 --binary 或 daemon
不可达 → 降级为旧行为（全部 jumptable 警告计 fatal）并打印提示。

Usage:
  python rpc_driver.py @out/all.c decompile-all <bin>
  python decomp_lint.py out/all.c [--json out/lint.json] [--top 40]
  python decomp_lint.py out/all.c --binary <bin>   # 启用尾调用甄别（先 ensure）
  python decomp_lint.py some_plain.c        # non-JSON input: whole-file scan

Exit codes: 0 no fatal functions, 1 usage error,
2 fatal functions found (read stdout; do not quote their pseudocode).
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

# 反编译器告警 → 严重级（fatal=该函数伪码不可直接引用；warn=需抽查；info=备注）
WARNINGS = [
    ("Could not recover jumptable", "fatal", "跳转表未恢复：必须读表字节手工解 rel32"),
    ("Treating indirect jump as call", "fatal", "间接 JMP 被渲染成 CALL：语义错误"),
    ("Too many branches", "fatal", "分支过多未恢复：同上"),
    ("Removing unreachable block", "warn", "不可达块被删：可能有死代码/混淆"),
    ("Subroutine does not return", "info", "noreturn 桩（通常是 panic）"),
    ("unrecognized", "fatal", "指令未识别"),
]

# 危险渲染：出现即表示"该处的字面值不可信，必须回字节核对"
RENDER_TRAPS = [
    (r"\bauVar\d+", "向量化渲染：按语义读，勿按字面"),
    (r"\bSUB16\d\d?\(", "位域/向量拆分：字面值不可信"),
    (r"\bSUB8[14]\(", "字节拆分：字面值不可信"),
    (r"CONCAT\d\d?\(", "拼接渲染：字面值不可信"),
    (r"&DAT_0000[0-9a-f]{4}\b", "小整数量被渲染成地址（长度/常量漂移高发）"),
    (r"\(\.\.\.\)\(&DAT_\w+ \+ \*\(int \*\)", "未恢复跳转表调用点"),
    (r"-\s*\(\s*\w+\s*==\s*'", "字节比较向量化：语义是 memcmp，非取负"),
    (r"\bundefined\d?\b", "类型未恢复（噪声，修类型后应消失）"),
]

MAXLEN_RE = re.compile(r"memcpy\([^;]*?,\s*0x([0-9a-f]+)\)", re.I)
JT_WARN_RE = re.compile(r"Could not recover jumptable at (0x[0-9a-fA-F]+)")

# 间接跳转族 fatal 警告：尾调用场景下同一条 JMP reg 会同时带出这三条
_INDIRECT_FATAL = {"Could not recover jumptable",
                   "Treating indirect jump as call",
                   "Too many branches"}

RPC_DRIVER = Path(__file__).resolve().parent / "rpc_driver.py"

# 尾调用甄别：JMP reg 之前允许出现的「尾声/传参」指令（审计 A5 口径：
# ADD RSP,imm / POP×N / LEAVE 为尾声标志，MOV 系传参可夹在中间）
_EPILOGUE_PASS = {"MOV", "MOVZX", "MOVSXD", "NOP", "XCHG"}
_LOOKBACK = 8    # 从 JMP 往前最多看 8 条
_WINDOW = 0x100  # 反汇编回取窗口


class RpcError(Exception):
    pass


def rpc_call(binary, command, *args, timeout=120):
    """subprocess 调同目录 rpc_driver.py；@out 落临时文件再读 JSON
    （铁律 3：大输出必须落文件，不走 stdout 管道）。自包含，不跨脚本 import。"""
    fd, out = tempfile.mkstemp(prefix="dsh_lint_", suffix=".json")
    os.close(fd)
    cmd = [sys.executable, str(RPC_DRIVER), "@" + out, command, str(binary)]
    cmd += [str(a) for a in args]
    proc = None
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        raw = Path(out).read_text(encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        raise RpcError("rpc_driver 调用超时（%ds），daemon 可能未就绪" % timeout)
    except OSError as e:
        raise RpcError("rpc_driver 调用失败: %s" % e)
    finally:
        try:
            os.unlink(out)
        except OSError:
            pass
    if not raw.strip():
        tail = (((proc.stderr or "") + (proc.stdout or "")).strip()[:400]
                if proc else "")
        raise RpcError("rpc_driver 无 JSON 输出。%s" % tail)
    try:
        data = json.loads(raw)
    except ValueError:
        raise RpcError("rpc_driver 输出不是 JSON: %s" % raw[:300])
    if not data.get("ok"):
        raise RpcError("%s 失败: %s" % (command, data.get("message")
                                        or data.get("error")))
    return data.get("result") or {}


def is_tailcall_at(binary, jt_addr):
    """jumptable 警告地址处的 JMP reg 是否紧邻尾声序列（= 尾调用，良性）。

    警告地址即未恢复间接跳转本身。取该地址前 _WINDOW 字节的反汇编，
    定位 JMP：必须是 JMP reg（非内存间接）；往前最多 _LOOKBACK 条内
    须出现尾声标志（POP / LEAVE / ADD RSP,imm），且中间只夹传参类指令。
    任一环节不符或取不到反汇编 → 抛 RpcError 由调用方维持 fatal。"""
    addr = int(jt_addr, 16)
    # 分页前推：daemon 遇未定义间隙会停页，请求地址落间隙时自动前跳到
    # 下一条已定义指令（同 jt_resolve.fetch_function 的翻页口径）
    insns, cur = [], max(addr - _WINDOW, 0)
    for _ in range(8):
        res = rpc_call(binary, "disassemble", "0x%x" % cur,
                       "-n", "64", "--with-instructions")
        page = [x for x in (res.get("instructions") or [])
                if int(x["address"], 16) <= addr]
        if not page:
            break
        insns = [x for x in insns
                 if int(x["address"], 16) < int(page[0]["address"], 16)] + page
        if int(page[-1]["address"], 16) >= addr:
            break
        nxt = int(page[-1]["address"], 16) + int(page[-1].get("length") or 1)
        cur = nxt if nxt > cur else cur + 1
    idx = next((i for i, x in enumerate(insns)
                if int(x["address"], 16) == addr), None)
    if idx is None:
        return False
    jmp = insns[idx]
    if (jmp.get("mnemonic") or "").upper() != "JMP":
        return False
    ops = (jmp.get("operands") or "").strip()
    if not ops or "[" in ops:
        return False  # 必须是 JMP reg，内存间接跳转仍按跳转表对待
    for ins in reversed(insns[max(0, idx - _LOOKBACK):idx]):
        mnem = (ins.get("mnemonic") or "").upper()
        iops = (ins.get("operands") or "").strip().upper()
        if mnem in ("POP", "LEAVE"):
            return True
        if mnem == "ADD" and iops.startswith("RSP,"):
            return True
        if mnem in _EPILOGUE_PASS:
            continue  # 传参类指令可夹在 JMP 与尾声之间
        return False  # 夹着非尾声/非传参指令 → 不像尾调用
    return False


def lint(text):
    rows = []
    for name, sev, why in WARNINGS:
        n = text.count(name)
        if n:
            rows.append((sev, name, n, why))
    return rows


def traps(text):
    out = []
    for pat, why in RENDER_TRAPS:
        n = len(re.findall(pat, text))
        if n:
            out.append((pat, n, why))
    return out


def load_functions(path):
    """decompile-all JSON -> function list; 非 JSON 输入降级为整体单块扫描。"""
    text = open(path, encoding="utf-8", errors="replace").read()
    try:
        funcs = json.loads(text)["result"]["functions"]
        if isinstance(funcs, list):
            return funcs, "json"
    except (ValueError, KeyError, TypeError):
        pass
    return [{"address": "-", "name": "<whole-file>", "c_code": text}], "text"


def main():
    ap = argparse.ArgumentParser(
        description="反编译伪码体检器：fatal 函数清单 + 危险渲染计数")
    ap.add_argument("allc", help="decompile-all 的 @out JSON，或任意 .c 文本")
    ap.add_argument("--binary",
                    help="样本路径（须经 rpc_driver.py ensure 加载）；给出后对"
                         "「仅 jumptable 警告」的 fatal 函数做尾调用甄别（审计 A5）")
    ap.add_argument("--json", help="JSON 报告输出路径")
    ap.add_argument("--top", type=int, default=40, help="fatal 清单最多打印条数")
    a = ap.parse_args()

    funcs, mode = load_functions(a.allc)
    if mode == "text":
        print("[提示] 输入不是 decompile-all JSON，已降级为整体单块扫描。")
    print("函数总数: %d" % len(funcs))

    rpc_bin = None
    if a.binary:
        if Path(a.binary).is_file():
            rpc_bin = a.binary
        else:
            print("[提示] --binary 指定的样本不存在: %s；跳过尾调用甄别，沿用旧口径。"
                  % a.binary)
    else:
        print("[提示] 未给 --binary：jumptable 类 fatal 未做尾调用甄别"
              "（尾调用会被计入 fatal，口径偏保守）。加 --binary <bin> 启用甄别。")

    sev_rank = {"fatal": 0, "warn": 1, "info": 2}
    per = []
    gcount = Counter()
    gtraps = Counter()
    for f in funcs:
        c = f.get("c_code") or ""
        w = lint(c)
        t = traps(c)
        for s, n, cnt, _ in w:
            gcount[n] += cnt
        for pat, cnt, _ in t:
            gtraps[pat] += cnt
        if w:
            worst = min(sev_rank[s] for s, _, _, _ in w)
            per.append([worst, f["address"], f["name"], len(c), w, t, c])

    # 审计 A5：fatal 警告全部来自间接跳转族的函数，走 rpc 做尾调用甄别
    fatal, tailcalls = [], []
    tailcall_warns = 0
    rpc_broken = False
    for p in per:
        worst, addr, name, sz, w, t, c = p
        fatal_names = {n for s, n, _, _ in w if s == "fatal"}
        if (worst == 0 and fatal_names and fatal_names <= _INDIRECT_FATAL
                and rpc_bin and not rpc_broken):
            jts = JT_WARN_RE.findall(c)
            try:
                if jts and all(is_tailcall_at(rpc_bin, j) for j in jts):
                    tailcalls.append(p)
                    tailcall_warns += len(jts)
                    continue
            except RpcError as e:
                rpc_broken = True
                print("[提示] rpc 不可达（%s）；其余函数降级为旧口径，"
                      "jumptable 警告全部计 fatal。" % e)
        if worst == 0:
            fatal.append(p)

    print("\n=== 全样本告警汇总 ===")
    for n, cnt in gcount.most_common():
        sev = next(s for k, s, _ in WARNINGS if k == n)
        note = ""
        if n == "Could not recover jumptable" and tailcall_warns:
            note = "（其中 %d 处已判尾调用，不计入 fatal）" % tailcall_warns
        print("  [%-5s] %-34s %d%s" % (sev, n, cnt, note))

    print("\n=== fatal 函数（伪码不可直接引用）: %d / %d ===" % (len(fatal), len(funcs)))
    for _, addr, name, sz, w, _, _ in sorted(fatal)[: a.top]:
        tags = ",".join(n for s, n, _, _ in w if s == "fatal")
        print("  %s  %-14s size=%-6d %s" % (addr, name, sz, tags))

    if tailcalls:
        print("\n=== 尾调用（良性，JMP reg 紧邻尾声序列；不计入 fatal）: %d ==="
              % len(tailcalls))
        for _, addr, name, sz, _, _, _ in sorted(tailcalls)[: a.top]:
            print("  %s  %-14s size=%-6d" % (addr, name, sz))

    print("\n=== 危险渲染计数（字面值必须回字节核对）===")
    for pat, cnt in gtraps.most_common():
        why = next(w for p, w in RENDER_TRAPS if p == pat)
        print("  %-46s %-6d %s" % (pat[:46], cnt, why))

    if a.json:
        json.dump(
            {
                "functions": len(funcs),
                "warnings": dict(gcount),
                "render_traps": dict(gtraps),
                "fatal_functions": [
                    {"address": ad, "name": nm, "size": sz,
                     "warnings": [n for _, n, _, _ in w]}
                    for _, ad, nm, sz, w, _, _ in sorted(fatal)
                ],
                "tailcall_functions": [
                    {"address": ad, "name": nm, "size": sz}
                    for _, ad, nm, sz, _, _, _ in sorted(tailcalls)
                ],
            },
            open(a.json, "w", encoding="utf-8"), indent=2, ensure_ascii=False,
        )
        print("\nJSON -> %s" % a.json)

    if fatal:
        print("\n[结论] 存在 %d 个 fatal 函数：这些伪码不可直接引用，回字节核对。"
              % len(fatal))
        if tailcalls:
            print("       另有 %d 个尾调用函数已剔除（良性，不占 fatal 基线）。"
                  % len(tailcalls))
        return 2
    print("\n[结论] 无 fatal 函数；注意上方危险渲染计数处仍需回字节核对。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
