#!/usr/bin/env python
"""cone_invert.py - 通用锥形反向传播求解器（铁律 6 阶梯 ①'：peel 无递推段/段非目标时的下一档）。

Host-side tool (any Python 3.8+, stdlib only; 纯本地文件工具，不经 daemon)。

依据（4ccec36c 复盘）：ARX 直线程序里每条语句单独看都是可逆的——
  d = a OP b  已知 d 与任一操作数 ⇒ 反解另一个（+/-/^/全掩码 & 精确反解，
  * 在整除时精确反解，<</>>/|/%/非全掩码 & 有损须人工）；
  d = fn(args) 已知 d 且只缺一个参数 ⇒ 用 CALL_TABLES 里的前向实现爆破该参数
  （默认域 2^16，--brute fn=N 可调；如 _p1(a,b) 已知 b 爆破 a 只要 65536 次）。
既然每语句可逆，整个锥就可以逐语句反向传播，不需要 z3/SMT——这正是
peel_inverse 检出段与求解目标不重合（或无干净递推段）时的机械化下一档。

用法:
  cone_invert.py <recon.txt> --known t8460=3294897108 [--known ...]
      [--calls calls.py] [--brute N | --brute fn=N]... [--max-rounds N]
      [--out solved.json]
  cone_invert.py <reconA.txt> --diff-symbolize <reconB.txt> --out <asym.txt>
      [--min-lit N]
  <recon.txt> 为 ssa_reconstruct.py --out 的直线程序（t = (a) OP (b) / t = fn(args)，
  兼容 t = 字面量 与 t = 变量 两种宽松行）；
  --known 为目标/锚点赋值（十进制或 0x 十六进制），可多次给；
  --calls 指向含 CALL_TABLES = {"fn": callable} 的 python 文件（查表函数前向实现）；
  --brute 设爆破域（全局默认 65536；fn=N 按函数覆盖）；
  --out 把解出的全部变量写 JSON（exact 值 + mod 派生标记）；
  --diff-symbolize 为符号化模式（29bf99c0 判例：只符号化部分输入常量时，
  锥体被残留字面量完全决定 → 全可正算报矛盾 → 误弃本路径）：本 recon 与
  reconB（同输入长度、不同输入值重跑 tracer 得来）按【值集合】diff——
  A 有 B 没有的字面量 = 随输入变化，在 A 的副本里符号化为 IN0..INK 写出；
  按值 diff 不按行号，两份 recon 行数不一致（控制流差异）也能用；
  --min-lit 过滤结构小常量（默认 256，位移量/小掩码不误符号化）。

exit: 0 反推收敛（判词看 stdout：全解出 / 部分解出+缺料清单）;
      1 矛盾——两类判词看 stdout：① 矛盾锥含未知量 = 方程/常量错了
        （铁律 9 信号，禁止续命）；② 矛盾锥全被字面量决定、无未知量 =
        输入符号化不完整（走 --diff-symbolize 补符号化后重跑，不是路径死了）;
      2 用法/输入文件错误。
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

DEF_BIN = re.compile(r"^(\w+) = \((.*)\) ([-+*^&|<>%/]+) \((.*)\)$")
DEF_CALL = re.compile(r"^(\w+) = (\w+)\((.*)\)$")
DEF_LIT = re.compile(r"^(\w+) = (\d+|0[xX][0-9a-fA-F]+)$")
DEF_COPY = re.compile(r"^(\w+) = (\w+)$")
INT_RE = re.compile(r"^\d+$")
HEX_RE = re.compile(r"^0[xX][0-9a-fA-F]+$")

DEFAULT_BRUTE = 65536


class NeedInput(Exception):
    pass


def parse_int(tok):
    tok = (tok or "").strip()
    if INT_RE.fullmatch(tok):
        return int(tok)
    if HEX_RE.fullmatch(tok):
        return int(tok, 16)
    return None


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


def load_defs(path):
    """返回 (defs, order)。defs[name] = ('bin',a,op,b) | ('call',fn,args) |
    ('lit',value) | ('copy',src)。"""
    defs, order = {}, []
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            m = DEF_BIN.match(ln)
            if m:
                defs[m.group(1)] = ("bin", m.group(2), m.group(3), m.group(4))
                order.append(m.group(1))
                continue
            m = DEF_CALL.match(ln)
            if m:
                defs[m.group(1)] = ("call", m.group(2), split_args(m.group(3)))
                order.append(m.group(1))
                continue
            m = DEF_LIT.match(ln)
            if m:
                defs[m.group(1)] = ("lit", parse_int(m.group(2)))
                order.append(m.group(1))
                continue
            m = DEF_COPY.match(ln)
            if m:
                defs[m.group(1)] = ("copy", m.group(2))
                order.append(m.group(1))
    return defs, order


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
    raise NeedInput("未支持运算符 %r" % op)


def invert_op(op, d, known_val, unknown_is_left):
    """d = a OP b：已知 d 与一个操作数，反解另一个。返回 (value, mod)；
    mod 非 None 表示模派生（只保证 value ≡ 真值 (mod mod)）。不可逆抛 NeedInput。"""
    if op == "+":
        return d - known_val, None
    if op == "-":
        return (d + known_val, None) if unknown_is_left else (known_val - d, None)
    if op == "^":
        return d ^ known_val, None
    if op == "*":
        if known_val == 0:
            if d == 0:
                raise NeedInput("零因子：d=0 且已知操作数=0，解不唯一")
            raise NeedInput("矛盾候选：0*x 不可能等于非零 d（请走正向矛盾检查）")
        if d % known_val != 0:
            raise NeedInput("d %% k != 0（%d %% %d）——方程或已知值有误" % (d, known_val))
        return d // known_val, None
    if op == "&":
        if known_val > 0 and (known_val & (known_val + 1)) == 0:
            mod = known_val + 1  # 全 1 掩码：a ≡ d (mod 2^n)
            return d & known_val, mod
        raise NeedInput("& 非全 1 掩码（%d），有损不可逆——该语句需人工" % known_val)
    if op == "<<":
        if d & ((1 << known_val) - 1):
            raise NeedInput("<< %d 的低位非零，反解不唯一——该语句需人工" % known_val)
        return d >> known_val, None
    if op == ">>":
        raise NeedInput(">> 丢失低 %d 位，不可逆——已知另一侧或换锚点" % known_val)
    if op in ("|", "%", "/"):
        raise NeedInput("%s 有损/多值，不可逆——该语句需人工" % op)
    raise NeedInput("未支持运算符 %r" % op)


def load_calls(path):
    spec = importlib.util.spec_from_file_location("cone_calls", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tables = getattr(mod, "CALL_TABLES", None)
    if not isinstance(tables, dict):
        raise NeedInput("%s 里必须有 CALL_TABLES = {\"fn\": callable}" % path)
    return tables


# ---------------------------------------------------------------- diff-symbolize

LIT_TOKEN_RE = re.compile(r"(?<![\w.])(\d+|0[xX][0-9a-fA-F]+)(?![\w.])")


def literal_values(path):
    """文件里全部独立整数字面量的值集合（t1896 这类变量名里的数字不算）。"""
    vals = set()
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            for m in LIT_TOKEN_RE.finditer(ln):
                vals.add(parse_int(m.group(1)))
    return vals


def diff_symbolize(recon_a, recon_b, out_path, min_lit):
    """A 有 B 没有的字面量 = 随输入变化，在 A 的副本里符号化为 IN0..INK。"""
    try:
        set_a = literal_values(recon_a)
        set_b = literal_values(recon_b)
    except OSError as e:
        print("recon 读取失败: %s" % e, file=sys.stderr)
        return 2
    only_a = sorted(v for v in (set_a - set_b) if v is not None and v >= min_lit)
    only_b = sorted(v for v in (set_b - set_a) if v is not None and v >= min_lit)
    if not only_a:
        print("两份 recon 无差异字面量（>= %d）：输入没以字面量形式进入程序"
              "（走 call 参数/控制流），或两份 recon 来自同一输入——"
              "换一个差异更大的输入（同长度）重跑 tracer。" % min_lit)
        return 0
    names = {v: "IN%d" % i for i, v in enumerate(only_a)}

    def repl(m):
        return names.get(parse_int(m.group(1)), m.group(1))

    try:
        with open(recon_a, encoding="utf-8") as fh:
            lines = fh.readlines()
    except OSError as e:
        print("recon 读取失败: %s" % e, file=sys.stderr)
        return 2
    header = ["# diff-symbolize: %s vs %s\n" % (recon_a, recon_b)]
    for v in only_a:
        header.append("# %s = %d (0x%x)\n" % (names[v], v, v))
    body = [LIT_TOKEN_RE.sub(repl, ln) for ln in lines]
    try:
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.writelines(header + body)
    except OSError as e:
        print("--out 写入失败: %s" % e, file=sys.stderr)
        return 2
    print("随输入变化的字面量 %d 个（>= %d）已符号化 -> %s："
          % (len(only_a), min_lit, os.path.abspath(out_path)))
    for v in only_a[:40]:
        print("   %s = %d (0x%x)" % (names[v], v, v))
    if len(only_a) > 40:
        print("   ... 共 %d 个" % len(only_a))
    if only_b:
        print("（参考：B 侧独有字面量 %d 个——同一位置在两 run 的值可交叉验证。）"
              % len(only_b))
    print()
    print("下一步：cone_invert.py %s --known <锚点> [--calls calls.py]" % out_path)
    print("解出 IN<i> 后，用「输入 -> 常量」映射（已知输入实测）把常量换回输入字节。")
    print("注意：按值集合 diff 不按行号，两份 recon 行数不一致也能用；")
    print("行数差来自控制流差异时可能多符号化个别结构常量——多符号化无害，")
    print("漏符号化才会让锥体被残留字面量锁死（29bf99c0 判例）。")
    return 0


def main():
    ap = argparse.ArgumentParser(prog="cone_invert.py")
    ap.add_argument("recon", help="ssa_reconstruct.py --out 的直线程序")
    ap.add_argument("--known", action="append", default=[], metavar="name=value",
                    help="目标/锚点赋值（十进制或 0x），可多次给")
    ap.add_argument("--calls", metavar="calls.py",
                    help="含 CALL_TABLES = {\"fn\": callable} 的 python 文件")
    ap.add_argument("--brute", action="append", default=[], metavar="N|fn=N",
                    help="调用参数爆破域（默认 %d；fn=N 按函数覆盖）" % DEFAULT_BRUTE)
    ap.add_argument("--max-rounds", type=int, default=10000)
    ap.add_argument("--out", metavar="solved.json", help="解出的全部变量写 JSON")
    ap.add_argument("--diff-symbolize", metavar="reconB.txt",
                    help="符号化模式：与 reconB（同长度不同输入）diff，"
                         "把随输入变化的字面量符号化后写入 --out")
    ap.add_argument("--min-lit", type=int, default=256,
                    help="diff 模式参与符号化的最小字面量（默认 256）")
    args = ap.parse_args()

    if args.diff_symbolize:
        if not args.out:
            print("--diff-symbolize 需要 --out 指定符号化版本的输出路径",
                  file=sys.stderr)
            return 2
        return diff_symbolize(args.recon, args.diff_symbolize, args.out,
                              args.min_lit)

    known = {}  # name -> [value, mod]
    for kv in args.known:
        name, sep, val = kv.partition("=")
        v = parse_int(val)
        if not sep or v is None:
            print("--known 格式错（要 name=value，十进制或 0x）: %r" % kv, file=sys.stderr)
            return 2
        known[name.strip()] = [v, None]
    if not known:
        print("缺 --known：反向传播需要至少一个目标/锚点赋值（铁律 9：手握已知答案先当锚）",
              file=sys.stderr)
        return 2

    brute_domain = {"*": DEFAULT_BRUTE}
    for b in args.brute:
        fn, sep, n = b.partition("=")
        if sep:
            if not INT_RE.fullmatch(n.strip()):
                print("--brute 格式错: %r" % b, file=sys.stderr)
                return 2
            brute_domain[fn.strip()] = int(n.strip())
        else:
            if not INT_RE.fullmatch(fn.strip()):
                print("--brute 格式错: %r" % b, file=sys.stderr)
                return 2
            brute_domain["*"] = int(fn.strip())

    try:
        call_tables = load_calls(args.calls) if args.calls else {}
    except (OSError, NeedInput) as e:
        print("calls 加载失败: %s" % e, file=sys.stderr)
        return 2
    try:
        defs, order = load_defs(args.recon)
    except OSError as e:
        print("recon 读取失败: %s" % e, file=sys.stderr)
        return 2
    if not defs:
        print("recon 无可解析语句（要 t = (a) OP (b) / t = fn(args) 格式）", file=sys.stderr)
        return 2

    def getv(tok):
        """操作数求值：返回 (value, mod) 或 None（未知）。"""
        v = parse_int(tok)
        if v is not None:
            return v, None
        ent = known.get(tok)
        return (ent[0], ent[1]) if ent else None

    def match(got, want):
        val, mod = got
        if mod:
            return (val - want[0]) % mod == 0 or (want[0] - val) % mod == 0
        return val == want[0] if not want[1] else (val - want[0]) % want[1] == 0

    unresolved = {}   # name -> 原因（去重，最后报告）
    contradictions = {}   # name -> 矛盾描述（分类判词要用到节点名）
    solved_rounds = 0

    for rnd in range(1, args.max_rounds + 1):
        progress = False
        for name in order:
            node = defs[name]
            tag = node[0]
            if tag == "lit":
                if name not in known:
                    known[name] = [node[1], None]
                    progress = True
                continue
            if tag == "copy":
                src = node[1]
                if name not in known and src in known:
                    known[name] = list(known[src])
                    progress = True
                elif src not in known and name in known:
                    known[src] = list(known[name])
                    progress = True
                continue
            if tag == "bin":
                _t, a, op, b = node
                va, vb = getv(a), getv(b)
                out = known.get(name)
                if out is None:
                    if va and vb:
                        try:
                            known[name] = [apply_op(op, va[0], vb[0]), None]
                        except NeedInput as e:
                            unresolved[name] = str(e)
                        else:
                            progress = True
                    continue
                want = (out[0], out[1])
                if va and vb:
                    try:
                        got = apply_op(op, va[0], vb[0])
                    except NeedInput:
                        continue
                    if not match((got, None), want):
                        contradictions[name] = (
                            "%s = (%s) %s (%s)：前向 %d != 已知 %d"
                            % (name, a, op, b, got, want[0]))
                    continue
                if va is None and vb is None:
                    unresolved[name] = "两个操作数都未知，暂不可反解"
                    continue
                try:
                    val, mod = invert_op(op, want[0],
                                         (va or vb)[0], unknown_is_left=(va is None))
                except NeedInput as e:
                    unresolved[name] = str(e)
                    continue
                target = a if va is None else b
                if target not in known:
                    known[target] = [val, mod]
                    progress = True
                continue
            # call
            _t, fn, call_args = node
            vals = [getv(x) for x in call_args]
            out = known.get(name)
            impl = call_tables.get(fn)
            if out is None:
                if all(vals) and impl is not None:
                    try:
                        known[name] = [int(impl(*[v[0] for v in vals])), None]
                        progress = True
                    except Exception as e:
                        unresolved[name] = "CALL %s 前向求值异常: %s" % (fn, e)
                elif impl is None:
                    unresolved[name] = ("查表函数 %s 无实现——--calls 提供 "
                                        "CALL_TABLES" % fn)
                continue
            want = (out[0], out[1])
            unknown_idx = [i for i, v in enumerate(vals) if v is None]
            if not unknown_idx:
                if impl is not None:
                    got = int(impl(*[v[0] for v in vals]))
                    if not match((got, None), want):
                        contradictions[name] = (
                            "%s = %s(...)：前向 %d != 已知 %d" % (name, fn, got, want[0]))
                continue
            if len(unknown_idx) > 1:
                unresolved[name] = "CALL %s 缺 %d 个参数，暂不可反解" % (fn, len(unknown_idx))
                continue
            if impl is None:
                unresolved[name] = "查表函数 %s 无实现——--calls 提供 CALL_TABLES" % fn
                continue
            i = unknown_idx[0]
            domain = brute_domain.get(fn, brute_domain["*"])
            prefix = [v[0] if v else None for v in vals]
            hits = []
            for cand in range(domain):
                trial = list(prefix)
                trial[i] = cand
                try:
                    got = int(impl(*trial))
                except Exception:
                    continue
                if match((got, None), want):
                    hits.append(cand)
                    if len(hits) > 4:
                        break
            if len(hits) == 1:
                target = call_args[i]
                if target not in known:
                    known[target] = [hits[0], None]
                    progress = True
            elif not hits:
                unresolved[name] = ("CALL %s 爆破域 [0,%d) 无命中——域太小或实现/目标值有误"
                                    % (fn, domain))
            else:
                unresolved[name] = ("CALL %s 爆破多值命中 %s...——不唯一，需更多约束"
                                    % (fn, hits[:4]))
        solved_rounds = rnd
        if not progress:
            break

    print("反向传播收敛于第 %d 轮：已知 %d / 定义 %d 个变量"
          % (solved_rounds, len(known), len(defs)))

    if contradictions:
        # 矛盾分类（29bf99c0 判例）：矛盾节点的依赖锥是否含未知量。
        # 锥体被字面量完全决定（无未知量）却与锚点矛盾 = 输入符号化不完整——
        # 残留的旧输入字面量把锥体锁死在旧输出上；这不是方程错了，补符号化重跑。
        dep_unknown = {}
        for _pass in range(2):
            for n in order:
                nd = defs[n]
                if nd[0] == "bin":
                    toks = (nd[1], nd[3])
                elif nd[0] == "call":
                    toks = tuple(nd[2])
                elif nd[0] == "copy":
                    toks = (nd[1],)
                else:
                    toks = ()
                dep_unknown[n] = any(
                    parse_int(t) is None
                    and (t not in defs or dep_unknown.get(t, False))
                    for t in toks)
        determined = [n for n in contradictions if not dep_unknown.get(n, False)]
        print()
        if len(determined) == len(contradictions):
            print("!! 矛盾，且每个矛盾节点的依赖锥都【不含任何未知量】——"
                  "锥体被字面量完全决定。")
            print("   这通常不是方程错了，而是【输入符号化不完整】：还有随输入变化的")
            print("   字面量顶着旧输入的具体值混在程序里（29bf99c0：只符号化 4 个常量、")
            print("   实际 8+ 个，锥体全可正算报矛盾后误弃本路径）。修复：")
            print("   1) 同长度、不同输入重跑 tracer + ssa_reconstruct 得 reconB.txt")
            print("   2) cone_invert.py <本recon> --diff-symbolize reconB.txt --out asym.txt")
            print("   3) cone_invert.py asym.txt --known <原锚点> [--calls calls.py] 重跑")
        else:
            print("!! 矛盾（方程/常量错了——铁律 9：禁止在同一方程上续命）:")
            if determined:
                print("   （其中 %d 个矛盾节点的锥体不含未知量——若锚点来自外部目标"
                      "而非本程序实测，先考虑符号化不完整：--diff-symbolize 见上。）"
                      % len(determined))
        for c in sorted(contradictions.values())[:20]:
            print("   " + c)
        return 1

    leaves = sorted({tok for n in order for tok in
                     ((defs[n][1], defs[n][3]) if defs[n][0] == "bin"
                      else tuple(defs[n][2]) if defs[n][0] == "call"
                      else (defs[n][1],) if defs[n][0] == "copy" else ())
                     if parse_int(tok) is None and tok not in known and tok not in defs})
    if leaves:
        print()
        print("输入叶子（无定义、未赋值——需要 --known 或实测值，如 flag 字节/种子）:")
        print("   " + ", ".join(leaves[:40]) + (" ..." if len(leaves) > 40 else ""))

    unsolved = [n for n in order if n not in known]
    if unsolved:
        print()
        print("未解出 %d 个变量（含原因去重）:" % len(unsolved))
        reasons = {}
        for n in unsolved:
            reasons.setdefault(unresolved.get(n, "依赖未就绪"), []).append(n)
        for r, ns in list(reasons.items())[:15]:
            print("   [%d 个，如 %s] %s" % (len(ns), ", ".join(ns[:3]), r))
        print()
        print("缺料就补料后重跑；补不了的有损语句（>>/|/非全掩码 &）才轮到人工/z3——")
        print("把本输出与 --out 一起附进 ledger.py stuck --tried。")
    else:
        print("全部已定义变量解出。铁律 7：用【未修改的原程序】验证最终答案——"
              "本脚本的自洽传播不算程序判定。")

    # 缺料警告：语句被卡住的原因即使该变量后来从别的路径解出也要可见——
    # 断链点（缺 CALL_TABLES/爆破域太小）往往正是需要人工补料的位置。
    passive = ("两个操作数都未知", "依赖未就绪")
    blocked = {}
    for n, r in unresolved.items():
        if any(p in r for p in passive):
            continue
        blocked.setdefault(r, []).append(n)
    if blocked:
        print()
        print("缺料警告（反解被卡住的语句，按原因去重）:")
        for r, ns in list(blocked.items())[:15]:
            print("   [%d 处，如 %s] %s" % (len(ns), ", ".join(ns[:3]), r))

    if args.out:
        payload = {n: ({"value": v[0]} if v[1] is None
                       else {"value": v[0], "mod": v[1], "note": "模派生，真值 ≡ value (mod mod)"})
                   for n, v in sorted(known.items())}
        try:
            with open(args.out, "w", encoding="utf-8") as fh:
                json.dump(payload, fh, ensure_ascii=False, indent=1)
            print("已写 %s（%d 项）" % (os.path.abspath(args.out), len(payload)))
        except OSError as e:
            print("--out 写入失败: %s" % e, file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
