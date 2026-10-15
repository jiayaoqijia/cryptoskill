#!/usr/bin/env python
"""peel_inverse.py - 掩码依赖图 + 滞后-k 可剥离递推判定（铁律 6 工具形态：先剥离，再考虑 z3/SMT）。

Host-side tool (any Python 3.8+, stdlib only; 纯本地文件工具，不经 daemon)。

依据（858e13b3 复盘 §5.4 / Reverse-chal 实测）：ARX 链的 8 个 32 位掩码满足二阶
递推  mask_i = (mask_{i-2} + F_i(mask_{i-1})) & 0xffffffff，F_i 只依赖更早掩码与
常量 ⇒ 从已知的两个末端掩码逐层反解  mask_{i-2} = (mask_i - F_i(mask_{i-1})) & mask，
完全不需要 SMT。本脚本在 ssa_reconstruct 产出的直线程序上把这种"滞后-2 递推段"
检出来；检不出干净结构（或递推段证伪不是求解目标）时转 cone_invert.py 锥形反推，
仍不通才放行 z3/SMT（或先做 S-box 反查/常量折叠）。

用法: peel_inverse.py <recon.txt> [--min-run N] [--emit-solver peel_solve.py]
  <recon.txt> 为 ssa_reconstruct.py --out 的直线程序；
  --min-run 为判定为递推段的最少连续掩码数（默认 4）；
  --emit-solver 在检出递推段时生成可运行的剥离求解器骨架（填 KNOWN/CALL_TABLES/SEEDS
  后运行即逐层反解 + 前向验证）——检出段的下一步是这条命令，不是直奔 z3/SMT。
exit: 0 判定完成（发现/未发现可剥离段都是正常结论，看 stdout 判词）; 2 用法/输入文件错误。
"""
from __future__ import annotations

import argparse
import os
import re
import sys

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

DEF_BIN = re.compile(r"^(\w+) = \((.*)\) ([-+*^&|<>%/]+) \((.*)\)$")
DEF_CALL = re.compile(r"^(\w+) = (\w+)\((.*)\)$")
MASK_LITERALS = ("4294967295", "0xffffffff")

# 生成的剥离求解器骨架模板（%RECON%/%RUNS%/%KNOWN% 由 emit 时替换）。
# 设计约束：纯 stdlib、可独立运行；求逆用 f0/f1 探针判定介入形式
# （+1 ⇒ 减法反解；^1 ⇒ 异或反解；其余判非线性交人工），反解完前向重放验证。
SOLVER_TEMPLATE = r'''#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""peel_solve.py - peel_inverse.py --emit-solver 生成的滞后-2 递推剥离求解器骨架。
源直线程序: %RECON%

机械三步：
  1) KNOWN：填入每个递推段【段末两个掩码】的目标值（来自你的约束/目标输出）。
  2) CALL_TABLES：段内表达式若含查表调用（如 p2/S-box），在此填实现，
     签名：函数名 -> callable(*args)，参数按 recon 行内顺序给入。
  3) SEEDS：段内用到的随机源/种子变量（getrandbits 等），从该轮 trace 抄实测值填入。
运行: python3 peel_solve.py  → 逐层反解段内全部掩码 + 前向重放验证。
注意：本脚本的自洽验证不是程序判定——最终 flag 按铁律 7 用【未修改的原程序】验证。
"""
import re
import sys

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

RECON = %RECON%
RUNS = %RUNS%
MASK = 0xFFFFFFFF

KNOWN = %KNOWN%
CALL_TABLES = {}
SEEDS = {}

DEF_BIN = re.compile(r"^(\w+) = \((.*)\) ([-+*^&|<>%/]+) \((.*)\)$")
DEF_CALL = re.compile(r"^(\w+) = (\w+)\((.*)\)$")


class NeedInput(Exception):
    pass


def load_defs(path):
    defs = {}
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if not ln:
                continue
            m = DEF_BIN.match(ln)
            if m:
                defs[m.group(1)] = ("bin", m.group(2), m.group(3), m.group(4))
                continue
            m = DEF_CALL.match(ln)
            if m:
                defs[m.group(1)] = ("call", m.group(2), m.group(3))
    return defs


def split_args(s):
    args, depth, cur = [], 0, ""
    for ch in s:
        if ch == "," and depth == 0:
            args.append(cur.strip())
            cur = ""
            continue
        cur += ch
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
    if cur.strip():
        args.append(cur.strip())
    return args


def apply_op(op, a, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "^":
        return a ^ b
    if op == "&":
        return a & b
    if op == "|":
        return a | b
    if op == "<<":
        return a << b
    if op == ">>":
        return a >> b
    if op == "%":
        return a % b
    if op == "/":
        return a // b
    raise NeedInput("未支持运算符 %r——该段需人工，带判词 ledger.py stuck" % op)


def ev(name, defs, env, memo):
    if name in env:
        return env[name]
    if name in memo:
        return memo[name]
    if re.fullmatch(r"\d+", name or ""):
        return int(name)
    if re.fullmatch(r"0[xX][0-9a-fA-F]+", name or ""):
        return int(name, 16)
    if name in SEEDS:
        return SEEDS[name]
    node = defs.get(name)
    if node is None:
        raise NeedInput("未定义变量 %s——若是该轮 trace 的随机源/种子，把实测值填进 SEEDS" % name)
    if node[0] == "call":
        _tag, fn, argstr = node
        table = CALL_TABLES.get(fn)
        if table is None:
            raise NeedInput("查表函数 %s 无实现——在 CALL_TABLES 填入（如 S-box: lambda x: ...）" % fn)
        v = int(table(*[ev(a, defs, env, memo) for a in split_args(argstr)]))
    else:
        _tag, a, op, b = node
        v = apply_op(op, ev(a, defs, env, memo), ev(b, defs, env, memo))
    memo[name] = v
    return v


def peel_run(defs, run):
    last2, last1 = run[-2], run[-1]
    vals = {last2: KNOWN[last2], last1: KNOWN[last1]}
    for i in range(len(run) - 3, -1, -1):
        mi2, mi1, mi = run[i], run[i + 1], run[i + 2]
        f0 = ev(mi, defs, {mi1: vals[mi1], mi2: 0}, {})
        f1 = ev(mi, defs, {mi1: vals[mi1], mi2: 1}, {})
        if (f1 - f0) & MASK == 1:
            vals[mi2] = (vals[mi] - f0) & MASK
        elif (f0 ^ 1) == f1:
            vals[mi2] = vals[mi] ^ f0
        else:
            raise NeedInput("%s 对 %s 非线性介入（f1-f0=%d）——该段需人工，带判词 ledger.py stuck"
                            % (mi, mi2, (f1 - f0) & MASK))
    for i in range(2, len(run)):
        chk = ev(run[i], defs, {run[i - 1]: vals[run[i - 1]], run[i - 2]: vals[run[i - 2]]}, {})
        if chk != vals[run[i]]:
            raise NeedInput("前向验证失败于 %s（%d != %d）——KNOWN 值或 CALL_TABLES 实现有误"
                            % (run[i], chk, vals[run[i]]))
    return vals


def main():
    missing = [k for k in KNOWN if KNOWN[k] is None]
    if missing:
        print("先填 KNOWN（每段段末两个掩码的目标值）: " + ", ".join(missing), file=sys.stderr)
        return 2
    defs = load_defs(RECON)
    try:
        for run in RUNS:
            vals = peel_run(defs, run)
            print("段 %s .. %s 反解完成（%d 项），前向验证通过:" % (run[0], run[-1], len(run)))
            for name in run:
                print("   %s = %d (0x%08x)" % (name, vals[name], vals[name]))
    except NeedInput as e:
        print("需人工补料: %s" % e, file=sys.stderr)
        return 2
    print()
    print("全部段恢复完成。铁律 7：用【未修改的原程序】验证最终 flag——本脚本自洽验证不算数。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


def direct_mask_deps(name, defs, masks, acc=None, seen=None):
    """展开表达式树，遇到**其它掩码变量**就当叶子记下并停止展开（只算直接依赖）。"""
    acc = set() if acc is None else acc
    seen = set() if seen is None else seen
    if name in seen or name not in defs:
        return acc
    seen.add(name)
    a, _op, b = defs[name]
    for tok in (a, b):
        if not tok or tok.isdigit():
            continue
        if tok in masks and tok != name:
            acc.add(tok)          # 叶子：不再展开
        else:
            direct_mask_deps(tok, defs, masks, acc, seen)
    return acc


def main():
    ap = argparse.ArgumentParser(prog="peel_inverse.py")
    ap.add_argument("recon", help="ssa_reconstruct.py --out 的直线程序")
    ap.add_argument("--min-run", type=int, default=4,
                    help="判定为递推段的最少连续掩码数（默认 4）")
    ap.add_argument("--emit-solver", metavar="OUT.py",
                    help="检出递推段时生成可运行剥离求解器骨架到 OUT.py")
    args = ap.parse_args()

    try:
        with open(args.recon, encoding="utf-8") as fh:
            src = [l.strip() for l in fh if l.strip()]
    except OSError as e:
        print("recon 读取失败: %s" % e, file=sys.stderr)
        return 2

    defs = {}
    for ln in src:
        m = DEF_BIN.match(ln)
        if m:
            defs[m.group(1)] = (m.group(2), m.group(3), m.group(4))
            continue
        m = DEF_CALL.match(ln)
        if m:
            defs[m.group(1)] = (m.group(3), m.group(2), None)

    masks = [n for n, (a, op, b) in defs.items()
             if op == "&" and b in MASK_LITERALS]
    print("掩码变量（& 0xffffffff）: %d" % len(masks))
    if not masks:
        print("可剥离判定: 无掩码变量——输入不是含 & 0xffffffff 的直线程序？"
              "先跑 ssa_trace.py -> ssa_reconstruct.py。")
        return 0

    dep_masks = {m: direct_mask_deps(defs[m][0], defs, masks) for m in masks}
    print("掩码间依赖:")
    for m in masks:
        ds = sorted(dep_masks[m], key=masks.index)
        print("   %-10s <- %s" % (m, ds if ds else "(无其它掩码，含种子/常量)"))

    # 找「滞后-2 递推段」：连续若干掩码，第 i 个恰好依赖前两个
    runs, cur = [], []
    for i, m in enumerate(masks):
        if i >= 2 and dep_masks[m] == {masks[i - 1], masks[i - 2]}:
            if not cur:
                cur = [masks[i - 2], masks[i - 1]]
            cur.append(m)
        else:
            if len(cur) >= args.min_run:
                runs.append(cur)
            cur = []
    if len(cur) >= args.min_run:
        runs.append(cur)

    print()
    print("可剥离判定:")
    if runs:
        for r in runs:
            print("   滞后-2 递推段 (%d 项): %s" % (len(r), " -> ".join(r)))
            print("      => mask_{i-2} = (mask_i - F_i(mask_{i-1})) & 0xffffffff，"
                  "从段末两个已知掩码逐层反解，无需 z3/SMT")
        if args.emit_solver:
            known = {}
            for r in runs:
                known[r[-2]] = None
                known[r[-1]] = None
            body = (SOLVER_TEMPLATE
                    .replace("%RECON%", repr(os.path.abspath(args.recon)))
                    .replace("%RUNS%", repr(runs))
                    .replace("%KNOWN%", repr(known)))
            try:
                with open(args.emit_solver, "w", encoding="utf-8") as fh:
                    fh.write(body)
            except OSError as e:
                print("骨架写入失败: %s" % e, file=sys.stderr)
                return 2
            print()
            print("已生成剥离骨架: %s" % os.path.abspath(args.emit_solver))
            print("   填 KNOWN（每段段末两个掩码的目标值）/ CALL_TABLES（查表函数）"
                  "/ SEEDS（种子实测值）后运行，即逐层反解 + 前向验证。")
            print("   骨架使用闸（4ccec36c：骨架 head 一眼弃用、0 填 0 跑，"
                  "z3 长征 91 min 交卷丢 flag）：0 次填写/运行 = 未过闸；")
            print("   主张「检出段与目标不重合/不适用」须 conclude 带证据"
                  "（剥离后目标仍不可达，或扰动实验证明检出段纯 RNG/常量-only）才放行 SMT；")
            print("   递推段确实不是目标 ⇒ 转 cone_invert.py 锥形反推（每语句可逆就无需 SMT）。")
        else:
            print()
            print("下一步（闸的输出是命令不是建议）:")
            print("   python3 %s %s --emit-solver peel_solve.py"
                  % (os.path.abspath(sys.argv[0]), args.recon))
            print("   → 生成可运行剥离骨架：填 KNOWN（段末两掩码目标值）"
                  "/ CALL_TABLES（查表函数）后运行，逐层反解 + 前向验证。")
            print("   检出递推段后直奔 z3/SMT = 违规（判例：47246ce9——检出后 0 次剥离，"
                  "z3 模型连修 4 次未收敛，47 min 无 flag）。")
            print("   骨架生成后 0 次填写/运行同样 = 未过闸（判例：4ccec36c——骨架 head 一眼")
            print("   弃用，z3 长征 91 min 后把 peel 路径写进 stuck 交卷）；递推段确实不是目标")
            print("   ⇒ 转 cone_invert.py 锥形反推，别直接跳 SMT。")
    else:
        cone = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "cone_invert.py")
        print("   未发现干净的滞后-2 结构 ⇒ 下一步 cone_invert.py 锥形反推：")
        print("   python3 %s %s --known <目标变量=值> [--calls calls.py]" % (cone, args.recon))
        print("   每语句可逆（+/-/^/全掩码 & 精确反解，查表调用爆破 2^16）就无需 SMT；")
        print("   cone 反推也走不通（有损语句聚集）才考虑 z3/SMT（或先做 S-box 反查/常量折叠）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
