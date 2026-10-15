#!/usr/bin/env python
"""ssa_trace.py - Cython/CPython 扩展 SSA 数据流追踪器（ctf-patterns §12.2 的工具形态）。

Host-side tool (any Python 3.8+, stdlib only; 纯本地 import 工具，不经 daemon)。

核心机制（Reverse-chal 复盘 §3.1 分水岭——该题型前 10 min 架好它，别手读生成 C）：
  ① 进入密码的值包成 int 子类 Sp：每个 + - * ^ & | << >> % // 经 dunder 自动落账
    (名, op, 左, 右, 值)，事件流 = 完整 SSA 数据流，等价于"不用读生成 C"。
  ② Cython 在 import 期缓存 builtins——**import 前**把 sum/chr/zip/range/print 等
    换成记录包装（--observe-builtins），即可全量观测缓存调用；退出前恢复原样。
  ③ random.* 钩子每次抽样落账（op=RNG:*），--pin-urandom 把 os.urandom 钉零、
    --seed 固定种子——配合 ctf-patterns §9 做 mask/key/target 角色判别对照实验。

用法:
  ssa_trace.py <模块文件(.so/.pyd/.py) 或可导入名> [--sys-path DIR]
      [--class CLS --ctor-input SPEC] [--wrap m1,m2]
      [--observe-builtins sum,chr,zip,range,print]
      [--pin-urandom] [--seed N] [--out trace.json]

  SPEC: 'A*48' 重复语法 / 字面字符串 / hex:deadbeef（bytes）。
  --wrap 的方法被包成记录器：调用事件落账（CALL:m），int 返回值转 Sp 续流数据流。
  不带 --class 时只 import 并记录 import 期事件（缓存 builtin / RNG 初始化观测）。

事件: {"n": 名, "op": 算子|RNG:*|BLK:*|CALL:*, "l": 左, "r": 右, "v": 值}，执行序。
exit: 0 正常; 2 用法错; 3 模块加载/实例化失败。
"""
from __future__ import annotations

import argparse
import builtins
import importlib.util
import json
import os
import random
import sys
from collections import Counter

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

EV = []
NAMES = {}
KEEP = []  # 防 GC 复用 id() 导致名字串号
CNT = [0]

RNG_NAMES = ("seed", "getrandbits", "randint", "randrange",
             "random", "choice", "randbytes")
DEFAULT_BUILTINS = ("sum", "chr", "zip", "range", "print")


def _brief(obj, limit=24):
    if isinstance(obj, Sp):
        return NAMES.get(id(obj), "?anon%d" % int(obj))
    if isinstance(obj, bool) or not isinstance(obj, int):
        if isinstance(obj, (bytes, bytearray)):
            return "hex:" + bytes(obj).hex()[:limit]
        return repr(obj)[:limit]
    return int(obj)


def _fresh(prefix):
    CNT[0] += 1
    return "%s%d" % (prefix, CNT[0])


def _register(v, nm):
    KEEP.append(v)
    NAMES[id(v)] = nm
    return v


def _record(op, left, right, value, prefix="t"):
    nm = _fresh(prefix)
    sv = _register(Sp(value), nm)
    EV.append({"n": nm, "op": op, "l": _brief(left),
               "r": None if right is None else _brief(right),
               "v": int(value)})
    return sv


class Sp(int):
    """记录型 int：每个算术/位运算自动向 EV 落账，返回 Sp 续流。"""

    __slots__ = ()

    def _bin(self, op, o, fn):
        if not isinstance(o, int):
            return NotImplemented
        return _record(op, self, o, fn(int(self), int(o)))

    def _un(self, op, fn):
        return _record(op, self, None, fn(int(self)), prefix="u")


def _mk(op, fn):
    return lambda self, o: self._bin(op, o, fn)


_BINOPS = {
    "__xor__": ("^", lambda a, b: a ^ b), "__rxor__": ("^", lambda a, b: b ^ a),
    "__and__": ("&", lambda a, b: a & b), "__rand__": ("&", lambda a, b: b & a),
    "__or__": ("|", lambda a, b: a | b), "__ror__": ("|", lambda a, b: b | a),
    "__add__": ("+", lambda a, b: a + b), "__radd__": ("+", lambda a, b: b + a),
    "__sub__": ("-", lambda a, b: a - b), "__rsub__": ("-", lambda a, b: b - a),
    "__mul__": ("*", lambda a, b: a * b), "__rmul__": ("*", lambda a, b: b * a),
    "__lshift__": ("<<", lambda a, b: a << b), "__rlshift__": ("<<", lambda a, b: b << a),
    "__rshift__": (">>", lambda a, b: a >> b), "__rrshift__": (">>", lambda a, b: b >> a),
    "__mod__": ("%", lambda a, b: a % b), "__rmod__": ("%", lambda a, b: b % a),
    "__floordiv__": ("//", lambda a, b: a // b),
}
for _attr, (_sym, _fn) in _BINOPS.items():
    setattr(Sp, _attr, _mk(_sym, _fn))

Sp.__neg__ = lambda self: self._un("NEG", lambda a: -a)
Sp.__abs__ = lambda self: self._un("ABS", abs)
Sp.__invert__ = lambda self: self._un("INV", lambda a: ~a)


def _sp_pow(self, o, m=None):
    if not isinstance(o, int):
        return NotImplemented
    v = pow(int(self), int(o), m) if m is not None else pow(int(self), int(o))
    return _record("POW", self, o, v, prefix="u")


def _sp_to_bytes(self, *a, **k):
    r = int.to_bytes(int(self), *a, **k) if a else int.to_bytes(int(self))
    EV.append({"n": _fresh("u"), "op": "TO_BYTES", "l": _brief(self),
               "r": [_brief(x) for x in a], "v": "hex:" + r.hex()})
    return r


def _sp_bit_length(self):
    return int(self).bit_length()


Sp.__pow__ = _sp_pow
Sp.to_bytes = _sp_to_bytes
Sp.bit_length = _sp_bit_length
# 比较/哈希/布尔必须保持 int 原语义，否则控制流与 dict/set 被破坏
Sp.__index__ = lambda self: int(self)


def _wrap_rng(name):
    orig = getattr(random, name)

    def w(*a, **k):
        r = orig(*a, **k)
        if isinstance(r, int) and not isinstance(r, bool):
            return _record("RNG:" + name, [_brief(x) for x in a], None, r,
                           prefix="k")
        EV.append({"n": _fresh("k"), "op": "RNG:" + name,
                   "l": [_brief(x) for x in a], "r": None, "v": _brief(r)})
        return r
    return w


def _wrap_builtin(name):
    orig = getattr(builtins, name)

    def w(*a, **k):
        r = orig(*a, **k)
        if isinstance(r, int) and not isinstance(r, bool):
            return _record("BLK:" + name, [_brief(x) for x in a], None, r,
                           prefix="b")
        EV.append({"n": _fresh("b"), "op": "BLK:" + name,
                   "l": [_brief(x) for x in a], "r": None, "v": _brief(r)})
        return r
    return w


def _wrap_method(cls, mname):
    orig = getattr(cls, mname)

    def w(self, *a, **k):
        r = orig(self, *a, **k)
        if isinstance(r, int) and not isinstance(r, bool):
            return _record("CALL:" + mname, [_brief(x) for x in a], None, r,
                           prefix="M")
        EV.append({"n": _fresh("M"), "op": "CALL:" + mname,
                   "l": [_brief(x) for x in a], "r": None, "v": _brief(r)})
        return r
    setattr(cls, mname, w)
    return orig


def _parse_input(spec):
    if spec.startswith("hex:"):
        return bytes.fromhex(spec[4:])
    if "*" in spec:
        ch, _, n = spec.rpartition("*")
        if n.isdigit():
            return ch * int(n)
    return spec


def _load_module(spec, extra_paths):
    for p in extra_paths:
        sys.path.insert(0, p)
    looks_like_file = (os.path.sep in spec or "/" in spec
                       or spec.endswith((".so", ".pyd", ".py")))
    if looks_like_file and os.path.isfile(spec):
        path = os.path.abspath(spec)
        name = os.path.basename(path).split(".")[0]
        mspec = importlib.util.spec_from_file_location(name, path)
        if mspec is None or mspec.loader is None:
            raise ImportError("无法从文件创建 module spec: %s" % path)
        mod = importlib.util.module_from_spec(mspec)
        mspec.loader.exec_module(mod)
        return mod
    return __import__(spec)


def main():
    ap = argparse.ArgumentParser(
        description="Cython/CPython 扩展 SSA 数据流追踪器（详见 docstring）")
    ap.add_argument("module", help="模块文件路径（.so/.pyd/.py）或可导入名")
    ap.add_argument("--sys-path", action="append", default=[],
                    help="附加导入搜索路径（可重复）")
    ap.add_argument("--class", dest="cls", help="要实例化的类名")
    ap.add_argument("--ctor-input",
                    help="构造参数：'A*48' 重复 / 字面串 / hex:…（bytes）")
    ap.add_argument("--wrap", default="",
                    help="逗号分隔的方法名，包成记录器（int 返回值转 Sp 续流）")
    ap.add_argument("--observe-builtins", default="",
                    help="逗号分隔的 builtin 名，import 前替换为记录包装；"
                         "空 = 不替换，'default' = %s" % ",".join(DEFAULT_BUILTINS))
    ap.add_argument("--no-rng", action="store_true", help="不钩 random.*")
    ap.add_argument("--pin-urandom", action="store_true",
                    help="os.urandom 钉零（§9 角色判别对照实验用）")
    ap.add_argument("--seed", type=int, help="import 前 random.seed(N)")
    ap.add_argument("--out", help="事件流 JSON 落盘路径")
    args = ap.parse_args()

    saved_builtins = {}
    saved_rng = {}
    saved_urandom = None
    try:
        blk_names = ([n.strip() for n in args.observe_builtins.split(",")
                      if n.strip()] if args.observe_builtins else [])
        if args.observe_builtins == "default":
            blk_names = list(DEFAULT_BUILTINS)
        for n in blk_names:
            if hasattr(builtins, n):
                saved_builtins[n] = getattr(builtins, n)
                setattr(builtins, n, _wrap_builtin(n))
        if not args.no_rng:
            for n in RNG_NAMES:
                if hasattr(random, n):
                    saved_rng[n] = getattr(random, n)
                    setattr(random, n, _wrap_rng(n))
        if args.pin_urandom:
            saved_urandom = os.urandom
            os.urandom = lambda n: b"\x00" * n
        if args.seed is not None:
            random.seed(args.seed)

        mod = _load_module(args.module, args.sys_path)

        result = None
        if args.cls:
            cls = getattr(mod, args.cls, None)
            if cls is None:
                print("模块 %s 没有类 %s" % (args.module, args.cls),
                      file=sys.stderr)
                return 3
            wrapped = []
            for m in [m.strip() for m in args.wrap.split(",") if m.strip()]:
                if hasattr(cls, m):
                    wrapped.append((m, _wrap_method(cls, m)))
            try:
                value = (_parse_input(args.ctor_input)
                         if args.ctor_input is not None else None)
                obj = cls(value) if args.ctor_input is not None else cls()
            finally:
                for m, orig in wrapped:
                    setattr(cls, m, orig)
            result = {k: ("%s=%d" % (NAMES.get(id(v), "?"), int(v))
                          if isinstance(v, Sp) else _brief(v, 64))
                      for k, v in vars(obj).items()} \
                if hasattr(obj, "__dict__") else _brief(obj, 64)

        payload = {"module": args.module, "events": EV, "result": result}
        if args.out:
            with open(args.out, "w", encoding="utf-8") as fh:
                json.dump(payload, fh, ensure_ascii=False)
        hist = Counter(e["op"] for e in EV)
        print("events: %d  ops: %s"
              % (len(EV), dict(hist.most_common(12))))
        if result is not None:
            print("result:", json.dumps(result, ensure_ascii=False)[:200])
        if args.out:
            print("trace:", args.out)
        return 0
    except (ImportError, AttributeError, TypeError) as e:
        print("加载/实例化失败: %s" % e, file=sys.stderr)
        return 3
    finally:
        for n, f in saved_builtins.items():
            setattr(builtins, n, f)
        for n, f in saved_rng.items():
            setattr(random, n, f)
        if saved_urandom is not None:
            os.urandom = saved_urandom


if __name__ == "__main__":
    sys.exit(main())
