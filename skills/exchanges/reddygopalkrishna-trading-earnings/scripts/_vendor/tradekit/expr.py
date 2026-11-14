"""A small, safe rule language for screens and strategies.

Examples:
    close > sma(close, 200) and rsi(2) < 10
    cross_above(ema(20), ema(50)) and volume > 1.5 * sma(volume, 50)
    close >= 0.95 * highest(high, 252) and adx(14) > 20

Rules are parsed with Python's ast module and only whitelisted nodes and
functions are allowed - no attribute access, no imports, no eval of user code.
Every expression evaluates to a series (one value per bar). Scalars broadcast.

Fields:    open high low close volume hl2 hlc3 ohlc4 bar_index
Operators: + - * / % **  > >= < <= == !=  and or not
"""

from __future__ import annotations

import ast
import math
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from . import indicators as ind
from .frame import Bars

Value = Any  # float | bool | None | list


class ExprError(ValueError):
    pass


FIELDS = ("open", "high", "low", "close", "volume", "hl2", "hlc3", "ohlc4", "bar_index")


# ------------------------------------------------------------------ function table
# Each entry: name -> (callable(ctx, args) -> series|scalar, signature help)

def _is_series(v) -> bool:
    return isinstance(v, list)


def _src_n(ctx, args, default_n: int, name: str) -> Tuple[List, int]:
    """Accept fn(n), fn(src, n), fn(src) or fn() -> (source series, period)."""
    if not args:
        return ctx.col("close"), default_n
    if len(args) == 1:
        if _is_series(args[0]):
            return args[0], default_n
        return ctx.col("close"), _int(args[0], name)
    if len(args) == 2 and _is_series(args[0]):
        return args[0], _int(args[1], name)
    raise ExprError(f"{name}() expects (period) or (source, period)")


def _int(v, name) -> int:
    if _is_series(v) or v is None:
        raise ExprError(f"{name}(): period must be a number")
    iv = int(v)
    if iv < 1:
        raise ExprError(f"{name}(): period must be >= 1")
    return iv


def _num(v, name, default=None) -> float:
    if v is None:
        return default
    if _is_series(v):
        raise ExprError(f"{name}(): expected a number")
    return float(v)


def _args(args, i, default=None):
    return args[i] if len(args) > i else default


def _f_ma(fn, default_n):
    def run(ctx, args, name):
        src, n = _src_n(ctx, args, default_n, name)
        return fn(src, n)
    return run


def _f_rsi(ctx, args, name):
    src, n = _src_n(ctx, args, 14, name)
    return ind.rsi(src, n)


def _f_atr(ctx, args, name):
    n = _int(_args(args, 0, 14), name)
    return ind.atr(ctx.col("high"), ctx.col("low"), ctx.col("close"), n)


def _f_atr_pct(ctx, args, name):
    a = _f_atr(ctx, args, name)
    return [None if v is None else v / c * 100 for v, c in zip(a, ctx.col("close"))]


def _f_bb(which):
    def run(ctx, args, name):
        if args and _is_series(args[0]):
            src, rest = args[0], args[1:]
        else:
            src, rest = ctx.col("close"), args
        n = _int(_args(rest, 0, 20), name)
        k = _num(_args(rest, 1, 2.0), name, 2.0)
        mid, up, lo = ind.bbands(src, n, k)
        if which == "width":
            return [None if m in (None, 0) or u is None else (u - l) / m * 100 for m, u, l in zip(mid, up, lo)]
        return {"mid": mid, "upper": up, "lower": lo}[which]
    return run


def _f_macd(which):
    def run(ctx, args, name):
        fast = _int(_args(args, 0, 12), name)
        slow = _int(_args(args, 1, 26), name)
        sig = _int(_args(args, 2, 9), name)
        line, s, h = ind.macd(ctx.col("close"), fast, slow, sig)
        return {"line": line, "signal": s, "hist": h}[which]
    return run


def _f_adx(which):
    def run(ctx, args, name):
        n = _int(_args(args, 0, 14), name)
        a, p, m = ind.adx(ctx.col("high"), ctx.col("low"), ctx.col("close"), n)
        return {"adx": a, "plus": p, "minus": m}[which]
    return run


def _f_window(fn, default_field):
    def run(ctx, args, name):
        if not args:
            raise ExprError(f"{name}() needs a period")
        if len(args) == 1:
            return fn(ctx.col(default_field), _int(args[0], name))
        return fn(args[0], _int(args[1], name))
    return run


def _f_stoch(which):
    def run(ctx, args, name):
        n = _int(_args(args, 0, 14), name)
        sk = _int(_args(args, 1, 3), name)
        sd = _int(_args(args, 2, 3), name)
        k, d = ind.stoch(ctx.col("high"), ctx.col("low"), ctx.col("close"), n, sk, sd)
        return k if which == "k" else d
    return run


def _f_supertrend(which):
    def run(ctx, args, name):
        n = _int(_args(args, 0, 10), name)
        m = _num(_args(args, 1, 3.0), name, 3.0)
        line, d = ind.supertrend(ctx.col("high"), ctx.col("low"), ctx.col("close"), n, m)
        return line if which == "line" else d
    return run


def _f_keltner(which):
    def run(ctx, args, name):
        n = _int(_args(args, 0, 20), name)
        m = _num(_args(args, 1, 1.5), name, 1.5)
        mid, up, lo = ind.keltner(ctx.col("high"), ctx.col("low"), ctx.col("close"), n, m)
        return {"mid": mid, "upper": up, "lower": lo}[which]
    return run


def _f_shift(ctx, args, name):
    if not args:
        raise ExprError(f"{name}(source, n) needs a source")
    src = args[0] if _is_series(args[0]) else [args[0]] * ctx.n
    n = int(_num(_args(args, 1, 1), name, 1))
    return ind.shift(src, n)


def _f_cross(fn):
    def run(ctx, args, name):
        if len(args) != 2:
            raise ExprError(f"{name}(a, b) takes two arguments")
        a = ctx.broadcast(args[0])
        b = ctx.broadcast(args[1])
        return fn(a, b)
    return run


def _f_rising(direction):
    def run(ctx, args, name):
        src, n = _src_n(ctx, args, 3, name)
        out = [False] * len(src)
        for i in range(n, len(src)):
            w = src[i - n:i + 1]
            if any(v is None for v in w):
                continue
            pairs = zip(w, w[1:])
            out[i] = all(b > a for a, b in pairs) if direction > 0 else all(b < a for a, b in pairs)
        return out
    return run


def _f_scalar_math(fn):
    def run(ctx, args, name):
        if len(args) != 1:
            raise ExprError(f"{name}(x) takes one argument")
        return ctx.map1(args[0], fn)
    return run


def _f_minmax(fn):
    def run(ctx, args, name):
        if len(args) < 2:
            raise ExprError(f"{name}(a, b, ...) takes two or more arguments")
        acc = args[0]
        for b in args[1:]:
            acc = ctx.map2(acc, b, lambda x, y: fn(x, y))
        return acc
    return run


def _f_vwap(ctx, args, name):
    return ind.vwap(ctx.col("high"), ctx.col("low"), ctx.col("close"), ctx.col("volume"), ctx.bars.date)


def _f_obv(ctx, args, name):
    return ind.obv(ctx.col("close"), ctx.col("volume"))


def _f_cci(ctx, args, name):
    return ind.cci(ctx.col("high"), ctx.col("low"), ctx.col("close"), _int(_args(args, 0, 20), name))


def _f_mfi(ctx, args, name):
    return ind.mfi(ctx.col("high"), ctx.col("low"), ctx.col("close"), ctx.col("volume"), _int(_args(args, 0, 14), name))


def _f_rel_volume(ctx, args, name):
    n = _int(_args(args, 0, 50), name)
    avg = ind.sma(ind.shift(ctx.col("volume"), 1), n)
    return [None if a in (None, 0) else v / a for v, a in zip(ctx.col("volume"), avg)]


def _f_pct_from_high(ctx, args, name):
    n = _int(_args(args, 0, 252), name)
    hh = ind.highest(ctx.col("high"), n)
    return [None if h in (None, 0) else (c / h - 1) * 100 for c, h in zip(ctx.col("close"), hh)]


def _f_pct_from_low(ctx, args, name):
    n = _int(_args(args, 0, 252), name)
    ll = ind.lowest(ctx.col("low"), n)
    return [None if l in (None, 0) else (c / l - 1) * 100 for c, l in zip(ctx.col("close"), ll)]


def _f_pct_change(ctx, args, name):
    src, n = _src_n(ctx, args, 1, name)
    return ind.roc(src, n)


def _f_change(ctx, args, name):
    src, n = _src_n(ctx, args, 1, name)
    return ind.change(src, n)


def _f_realized_vol(ctx, args, name):
    n = _int(_args(args, 0, 20), name)
    return ind.realized_vol(ctx.col("close"), n)


def _f_percentile(ctx, args, name):
    if len(args) != 2:
        raise ExprError(f"{name}(source, n) takes two arguments")
    return ind.percentile_rank(ctx.broadcast(args[0]), _int(args[1], name))


FUNCTIONS: Dict[str, Tuple[Callable, str]] = {
    "sma": (_f_ma(ind.sma, 20), "sma([src,] n=20) simple moving average"),
    "ema": (_f_ma(ind.ema, 20), "ema([src,] n=20) exponential moving average"),
    "wma": (_f_ma(ind.wma, 20), "wma([src,] n=20) weighted moving average"),
    "rma": (_f_ma(ind.rma, 14), "rma([src,] n=14) Wilder moving average"),
    "stdev": (_f_ma(ind.stdev, 20), "stdev([src,] n=20) rolling std dev"),
    "zscore": (_f_ma(ind.zscore, 20), "zscore([src,] n=20)"),
    "roc": (_f_ma(ind.roc, 10), "roc([src,] n=10) rate of change %"),
    "slope": (_f_ma(ind.slope, 20), "slope([src,] n=20) regression slope, % per bar"),
    "rsi": (_f_rsi, "rsi([src,] n=14)"),
    "atr": (_f_atr, "atr(n=14) average true range"),
    "atr_pct": (_f_atr_pct, "atr_pct(n=14) ATR as % of close"),
    "bb_upper": (_f_bb("upper"), "bb_upper([src,] n=20, k=2)"),
    "bb_lower": (_f_bb("lower"), "bb_lower([src,] n=20, k=2)"),
    "bb_mid": (_f_bb("mid"), "bb_mid([src,] n=20, k=2)"),
    "bb_width": (_f_bb("width"), "bb_width([src,] n=20, k=2) band width % of mid"),
    "kc_upper": (_f_keltner("upper"), "kc_upper(n=20, mult=1.5) Keltner channel"),
    "kc_lower": (_f_keltner("lower"), "kc_lower(n=20, mult=1.5)"),
    "kc_mid": (_f_keltner("mid"), "kc_mid(n=20, mult=1.5)"),
    "macd": (_f_macd("line"), "macd(fast=12, slow=26, signal=9) MACD line"),
    "macd_signal": (_f_macd("signal"), "macd_signal(fast=12, slow=26, signal=9)"),
    "macd_hist": (_f_macd("hist"), "macd_hist(fast=12, slow=26, signal=9)"),
    "adx": (_f_adx("adx"), "adx(n=14) trend strength"),
    "plus_di": (_f_adx("plus"), "plus_di(n=14)"),
    "minus_di": (_f_adx("minus"), "minus_di(n=14)"),
    "stoch_k": (_f_stoch("k"), "stoch_k(n=14, k=3, d=3)"),
    "stoch_d": (_f_stoch("d"), "stoch_d(n=14, k=3, d=3)"),
    "cci": (_f_cci, "cci(n=20)"),
    "mfi": (_f_mfi, "mfi(n=14) money flow index"),
    "supertrend": (_f_supertrend("line"), "supertrend(n=10, mult=3) line"),
    "supertrend_dir": (_f_supertrend("dir"), "supertrend_dir(n=10, mult=3) +1 up / -1 down"),
    "vwap": (_f_vwap, "vwap() session VWAP (intraday) / cumulative (daily)"),
    "obv": (_f_obv, "obv() on-balance volume"),
    "highest": (_f_window(ind.highest, "high"), "highest([src,] n) rolling max (default high)"),
    "lowest": (_f_window(ind.lowest, "low"), "lowest([src,] n) rolling min (default low)"),
    "shift": (_f_shift, "shift(src, n=1) value n bars ago"),
    "ref": (_f_shift, "ref(src, n=1) alias of shift"),
    "cross_above": (_f_cross(ind.crossed_above), "cross_above(a, b) a crosses above b this bar"),
    "cross_below": (_f_cross(ind.crossed_below), "cross_below(a, b) a crosses below b this bar"),
    "rising": (_f_rising(1), "rising([src,] n=3) strictly rising for n bars"),
    "falling": (_f_rising(-1), "falling([src,] n=3) strictly falling for n bars"),
    "rel_volume": (_f_rel_volume, "rel_volume(n=50) volume / average of prior n bars"),
    "pct_from_high": (_f_pct_from_high, "pct_from_high(n=252) % below n-bar high (<=0)"),
    "pct_from_low": (_f_pct_from_low, "pct_from_low(n=252) % above n-bar low (>=0)"),
    "pct_change": (_f_pct_change, "pct_change([src,] n=1) % change over n bars"),
    "change": (_f_change, "change([src,] n=1) absolute change over n bars"),
    "realized_vol": (_f_realized_vol, "realized_vol(n=20) annualized volatility %"),
    "percentile": (_f_percentile, "percentile(src, n) rank of current value within last n (0-100)"),
    "abs": (_f_scalar_math(abs), "abs(x)"),
    "sqrt": (_f_scalar_math(lambda v: math.sqrt(v) if v >= 0 else None), "sqrt(x)"),
    "log": (_f_scalar_math(lambda v: math.log(v) if v > 0 else None), "log(x)"),
    "max": (_f_minmax(max), "max(a, b, ...) elementwise max"),
    "min": (_f_minmax(min), "min(a, b, ...) elementwise min"),
}


def help_text() -> str:
    lines = ["Fields: " + ", ".join(FIELDS), "Functions:"]
    lines += [f"  {sig}" for _, sig in FUNCTIONS.values()]
    return "\n".join(lines)


# ------------------------------------------------------------------ parsing

_ALLOWED = (
    ast.Expression, ast.BoolOp, ast.And, ast.Or, ast.UnaryOp, ast.Not, ast.USub, ast.UAdd,
    ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.Compare, ast.Gt, ast.GtE, ast.Lt, ast.LtE, ast.Eq, ast.NotEq,
    ast.Call, ast.Name, ast.Load, ast.Constant,
)


def compile_expr(text: str) -> ast.Expression:
    if not isinstance(text, str) or not text.strip():
        raise ExprError("empty expression")
    src = " ".join(text.replace("&&", " and ").replace("||", " or ").split())
    src = src.replace(" AND ", " and ").replace(" OR ", " or ").replace(" NOT ", " not ")
    try:
        tree = ast.parse(src, mode="eval")
    except SyntaxError as e:
        raise ExprError(f"syntax error in rule {text!r}: {e.msg}") from None
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED):
            raise ExprError(f"not allowed in rules: {type(node).__name__}")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ExprError("only plain function calls are allowed")
            if node.func.id not in FUNCTIONS:
                raise ExprError(f"unknown function {node.func.id}(). Available: {', '.join(sorted(FUNCTIONS))}")
            if node.keywords:
                raise ExprError(f"{node.func.id}(): use positional arguments only")
        elif isinstance(node, ast.Name) and node.id not in FIELDS and node.id not in FUNCTIONS \
                and node.id not in ("True", "False", "true", "false"):
            raise ExprError(f"unknown name {node.id!r}. Fields: {', '.join(FIELDS)}")
        elif isinstance(node, ast.Constant) and not isinstance(node.value, (int, float, bool)):
            raise ExprError("only numeric constants are allowed")
    return tree


# ------------------------------------------------------------------ evaluation

class _Ctx:
    def __init__(self, bars: Bars):
        self.bars = bars
        self.n = len(bars)
        self._cols: Dict[str, List] = {}
        self._cache: Dict[str, Value] = {}

    def col(self, name: str) -> List:
        if name not in self._cols:
            self._cols[name] = list(range(self.n)) if name == "bar_index" else self.bars.col(name)
        return self._cols[name]

    def broadcast(self, v) -> List:
        return v if _is_series(v) else [v] * self.n

    def map1(self, a, fn) -> Value:
        if _is_series(a):
            return [None if x is None else fn(x) for x in a]
        return None if a is None else fn(a)

    def map2(self, a, b, fn) -> Value:
        if not _is_series(a) and not _is_series(b):
            return None if a is None or b is None else fn(a, b)
        a = self.broadcast(a)
        b = self.broadcast(b)
        out = []
        for x, y in zip(a, b):
            if x is None or y is None:
                out.append(None)
            else:
                try:
                    out.append(fn(x, y))
                except (ZeroDivisionError, OverflowError, ValueError):
                    out.append(None)
        return out


_BIN = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Mod: lambda a, b: a % b,
    ast.Pow: lambda a, b: a ** b,
}
_CMP = {
    ast.Gt: lambda a, b: a > b,
    ast.GtE: lambda a, b: a >= b,
    ast.Lt: lambda a, b: a < b,
    ast.LtE: lambda a, b: a <= b,
    ast.Eq: lambda a, b: a == b,
    ast.NotEq: lambda a, b: a != b,
}


def _truth(v) -> bool:
    return bool(v) if v is not None else False


def _eval(node, ctx: _Ctx) -> Value:
    key = ast.dump(node)
    if key in ctx._cache:
        return ctx._cache[key]
    val = _eval_inner(node, ctx)
    ctx._cache[key] = val
    return val


def _eval_inner(node, ctx: _Ctx) -> Value:
    if isinstance(node, ast.Expression):
        return _eval(node.body, ctx)
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in ("True", "true"):
            return True
        if node.id in ("False", "false"):
            return False
        if node.id in FUNCTIONS:  # bare function name, e.g. "obv" or "vwap"
            fn, _ = FUNCTIONS[node.id]
            return fn(ctx, [], node.id)
        return ctx.col(node.id)
    if isinstance(node, ast.UnaryOp):
        v = _eval(node.operand, ctx)
        if isinstance(node.op, ast.Not):
            return [not _truth(x) for x in v] if _is_series(v) else not _truth(v)
        if isinstance(node.op, ast.USub):
            return ctx.map1(v, lambda x: -x)
        return v
    if isinstance(node, ast.BinOp):
        return ctx.map2(_eval(node.left, ctx), _eval(node.right, ctx), _BIN[type(node.op)])
    if isinstance(node, ast.BoolOp):
        vals = [_eval(v, ctx) for v in node.values]
        is_and = isinstance(node.op, ast.And)
        if not any(_is_series(v) for v in vals):
            return all(_truth(v) for v in vals) if is_and else any(_truth(v) for v in vals)
        cols = [ctx.broadcast(v) for v in vals]
        if is_and:
            return [all(_truth(c[i]) for c in cols) for i in range(ctx.n)]
        return [any(_truth(c[i]) for c in cols) for i in range(ctx.n)]
    if isinstance(node, ast.Compare):
        left = _eval(node.left, ctx)
        result = None
        for op, comp in zip(node.ops, node.comparators):
            right = _eval(comp, ctx)
            part = ctx.map2(left, right, _CMP[type(op)])
            if part is None:
                part = False
            if _is_series(part):
                part = [bool(p) if p is not None else False for p in part]
            if result is None:
                result = part
            else:
                if _is_series(result) or _is_series(part):
                    a, b = ctx.broadcast(result), ctx.broadcast(part)
                    result = [x and y for x, y in zip(a, b)]
                else:
                    result = result and part
            left = right
        return result
    if isinstance(node, ast.Call):
        fn, _ = FUNCTIONS[node.func.id]
        args = [_eval(a, ctx) for a in node.args]
        return fn(ctx, args, node.func.id)
    raise ExprError(f"unsupported syntax {type(node).__name__}")


def evaluate(text_or_tree, bars: Bars) -> List:
    """Evaluate a rule over all bars. Returns a list (len == len(bars))."""
    tree = compile_expr(text_or_tree) if isinstance(text_or_tree, str) else text_or_tree
    ctx = _Ctx(bars)
    v = _eval(tree, ctx)
    return ctx.broadcast(v)


def evaluate_last(text_or_tree, bars: Bars):
    if len(bars) == 0:
        return None
    return evaluate(text_or_tree, bars)[-1]


class Evaluator:
    """Evaluate many rules on the same bars, sharing indicator computations."""

    def __init__(self, bars: Bars):
        self.ctx = _Ctx(bars)

    def series(self, text_or_tree) -> List:
        tree = compile_expr(text_or_tree) if isinstance(text_or_tree, str) else text_or_tree
        return self.ctx.broadcast(_eval(tree, self.ctx))

    def last(self, text_or_tree):
        s = self.series(text_or_tree)
        return s[-1] if s else None


def as_bool(series: Sequence) -> List[bool]:
    return [_truth(v) for v in series]
