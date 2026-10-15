#!/usr/bin/env python
"""const_scan.py - rebuild Python constant literals from decompiled Cython C.

Host-side tool (any Python 3.8+, stdlib only). Pure local text scan - no
daemon needed. Motivation (CTF retro): in a Cython-compiled .so a Python list
literal such as L = [173, 7, 131, ...] is NOT a byte string in the binary; in
decompiled C it appears as PyList_New(0x30) followed by 48 constant writes
(PyLong_FromLong(<small int>) inline, or slot writes from the Cython cached
int-object pool, e.g. `puVar25[3] = DAT_00128fe0;`). Searching the .so for
the byte pattern `AD 07` is guaranteed to miss the table. This script
mechanically reconstructs those literals so the constant table is never lost
again.

Two detection modes per function:
  1. Literal rebuild: PyList_New(n) / PyTuple_New(n), then the next n
     constant items (PyLong_FromLong / PyLong_FromString / PyFloat_FromDouble
     / PyBytes_FromString(AndSize) / PyUnicode_FromString, or slot writes
     `ptr[i] = IDENT` / PyList_SET_ITEM / PyTuple_SET_ITEM) inside a window
     of n*4 lines, re-emitted as a Python list/tuple literal. Slot writes
     that reference globals (DAT_xxx) are reported as refs - resolve them via
     the mstate object pool / get_data_at_address to recover the values.
  2. Alert mode: even without PyList_New, >= --min-cluster PyLong_FromLong
     calls with values in 0..255 clustered in one function fire a
     "suspected byte-level constant table (padding table / S-box /
     permutation table)" warning listing the values in order.
PyBytes_FromString / Py_BuildValue call sites are also reported as leads.

Usage:
  python const_scan.py <decompiled.c | decompile-all @out JSON> [--json out.json]
  python const_scan.py chal.p3pf.clean.c --min-cluster 8
  python const_scan.py decompile_all_out.json --json report.json
  python const_scan.py chal.p3pf.clean.c --binary chal.so   # 还原 <DAT_…> 缓存整数的值

Input is auto-detected: JSON containing result.functions[].c_code (or a
single result.c_code, or a top-level functions list) is treated as
decompile-all / decompile-function output; anything else is treated as plain
C text (decompile_all .c sidecar `/* ===== name @ addr ===== */` markers are
used to attribute functions when present).

--binary 值还原（T3 完整版）：列表项里的 <DAT_xxxxxxxx> 是 Cython 缓存
PyLong 对象的指针槽。给出样本路径（须先 rpc_driver.py ensure）后，脚本
经 daemon 读 DAT 槽里的指针，再按 PyLongObject 布局读 ob_digit 还原整数，
预览/字面量直接打印 Python 值。CPython 版本布局自动判别（3.12 lv_tag vs
pre-3.12 ob_size，按全体解析结果投票），可用 --py 强制。默认按 64 位指针
解析（--ptr-size 4 可改）。**边界**：落在 .bss（initialized=False）的引用
是运行期才填充的对象池，静态无文件字节可读——脚本会识别并明确报告，
此类样本改走 ctf-patterns §12 元数据路线或运行期取数。

Exit codes: 0 scan completed（含 --binary 模式下部分/全部引用还原失败——
会附提示），1 usage error (missing file / malformed input)。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

LIST_NEW_RE = re.compile(r"\b(PyList_New|PyTuple_New)\s*\(\s*(0[xX][0-9a-fA-F]+|\d+)")
BYTES_RE = re.compile(r"\b(PyBytes_FromString(?:AndSize)?|PyUnicode_FromString(?:AndSize)?)"
                      r'\s*\(\s*"((?:[^"\\]|\\.)*)"')
BUILDVALUE_RE = re.compile(r'\bPy_BuildValue\s*\(\s*"((?:[^"\\]|\\.)*)"')

LONG_RE = re.compile(r"\bPyLong_FromLong(?:Long)?\s*\(\s*(-?(?:0[xX][0-9a-fA-F]+|\d+))\s*[lL]?\s*\)")
LONG_STR_RE = re.compile(r'\bPyLong_FromString\s*\(\s*"([^"]*)"\s*,\s*[^,]+,\s*(\d+)')
FLOAT_RE = re.compile(r"\bPyFloat_FromDouble\s*\(\s*(-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)")
UNICODE_RE = re.compile(r'\bPyUnicode_FromString(?:AndSize)?\s*\(\s*"((?:[^"\\]|\\.)*)"')
BYTES_ITEM_RE = re.compile(r'\bPyBytes_FromString(?:AndSize)?\s*\(\s*"((?:[^"\\]|\\.)*)"')

SET_ITEM_RE = re.compile(r"\b(PyList_SET_ITEM|PyTuple_SET_ITEM)\s*\("
                         r"\s*\w+\s*,\s*(0[xX][0-9a-fA-F]+|\d+)\s*,\s*([^;()]+?)\s*\)")
SLOT_WRITE_RE = re.compile(r"\b([A-Za-z_]\w*)\s*\[\s*(0[xX][0-9a-fA-F]+|\d+)\s*\]"
                           r"\s*=\s*([A-Za-z_]\w*)\s*;")
DEREF_WRITE_RE = re.compile(r"^\s*\*\s*([A-Za-z_]\w*)\s*=\s*([A-Za-z_]\w*)\s*;")
ALIAS_RE = re.compile(r"^\s*([A-Za-z_]\w*)\s*=\s*([A-Za-z_]\w*)\s*;")

FUNC_MARKER_RE = re.compile(r"/\*\s*=+\s*(.+?)\s*@\s*([0-9a-fA-Fx]+)\s*=+\s*\*/")

DAT_REF_RE = re.compile(r"^DAT_([0-9a-fA-F]{6,16})$")

PREVIEW_ITEMS = 16
CLUSTER_MAX_GAP = 8

RPC_DRIVER = Path(__file__).resolve().parent / "rpc_driver.py"


class RpcError(Exception):
    def __init__(self, message, daemon=False):
        super().__init__(message)
        self.daemon = daemon


def rpc_call(binary, command, *args, timeout=120):
    """subprocess 调同目录 rpc_driver.py；@out 落临时文件再读 JSON
    （铁律 3：大输出必须落文件，不走 stdout 管道）。"""
    fd, out = tempfile.mkstemp(prefix="dsh_cs_", suffix=".json")
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
        raise RpcError("%s 失败: %s" % (command, data.get("message")
                                        or data.get("error")))
    return data.get("result") or {}


def read_bytes(binary, addr, length):
    """经 daemon 读内存；读不出返回 None。"""
    try:
        res = rpc_call(binary, "read-bytes", "0x%x" % addr, str(length))
        return bytes.fromhex(res.get("hex") or "")
    except RpcError:
        return None


def fetch_uninit_blocks(binary):
    """memory-map 里 initialized=False 的块（.bss 等）区间表；失败返回空表。"""
    try:
        res = rpc_call(binary, "memory-map")
        return [(int(s["start"], 16), int(s["end"], 16))
                for s in res.get("segments") or []
                if not s.get("initialized", True)]
    except (RpcError, KeyError, ValueError):
        return []


def in_uninit(blocks, addr):
    return any(lo <= addr <= hi for lo, hi in blocks)


def _parse_pylong(digits):
    """30 bit limb 组装；任一 limb 超界返回 None。"""
    if any(d >= (1 << 30) for d in digits):
        return None
    return sum(d << (30 * i) for i, d in enumerate(digits))


def resolve_cached_int(binary, dat_addr, ptr_size, layout):
    """把 DAT 槽（缓存 PyLong* 的指针）还原成 Python int；失败返回 None。

    layout: "312" = CPython 3.12+ lv_tag（低 2 bit 符号、高位 digit 数）；
            "311" = pre-3.12 ob_size（有符号 ssize_t，绝对值 = digit 数）。
    """
    pb = read_bytes(binary, dat_addr, ptr_size)
    if pb is None or len(pb) < ptr_size:
        return None
    p = int.from_bytes(pb, "little")
    if p == 0:
        return None
    size_off = 2 * ptr_size
    size_len = ptr_size
    hdr = read_bytes(binary, p, size_off + size_len)
    if hdr is None or len(hdr) < size_off + size_len:
        return None
    q = int.from_bytes(hdr[size_off:size_off + size_len], "little", signed=True)
    if layout == "312":
        tag = q & 3
        if tag == 3:  # 非法符号码
            return None
        if tag == 1:
            return 0
        neg = tag == 2
        nd = q >> 3
    else:
        if abs(q) > 4096:  # ob_size 不可能这么大——更像 3.12 lv_tag
            return None
        neg = q < 0
        nd = abs(q)
    if nd == 0:
        return 0
    if nd > 64:
        return None
    raw = read_bytes(binary, p + size_off + size_len, 4 * nd)
    if raw is None or len(raw) < 4 * nd:
        return None
    digits = struct.unpack("<%dI" % nd, raw)
    value = _parse_pylong(digits)
    if value is None:
        return None
    return -value if neg else value


def resolve_refs(binary, literals, ptr_size, py_layout):
    """还原全部字面量里的 <DAT_…> 引用。返回 (stats, layout_used)。

    版本自动判别：两种布局全体试解析，"可还原数多、非零居多"的布局胜出
    （3.12 布局误读 pre-3.12 ob_size 会把大量对象判成 0，反之误读会
    limb 超界解析失败；常量表通常非零居多）。py_layout 为 "311"/"312"
    时跳过投票。
    """
    refs = sorted({it["name"] for lit in literals for it in lit["items"]
                   if it["kind"] == "ref" and DAT_REF_RE.match(it["name"])})
    stats = {"refs": len(refs), "resolved": 0, "layout": py_layout,
             "unresolved": []}
    if not refs:
        return stats, py_layout
    addrs = {name: int(DAT_REF_RE.match(name).group(1), 16) for name in refs}

    if py_layout == "auto":
        votes = {}
        for layout in ("312", "311"):
            ok = nz = 0
            for addr in addrs.values():
                v = resolve_cached_int(binary, addr, ptr_size, layout)
                if v is not None:
                    ok += 1
                    if v != 0:
                        nz += 1
            votes[layout] = (ok, nz)
        # 先比可解析数，再比非零数；并列时偏向 3.12（现代 Cython 目标）
        layout_used = max(("312", "311"),
                          key=lambda l: (votes[l][0], votes[l][1], l == "312"))
        stats["layout"] = layout_used
        stats["votes"] = {l: {"ok": ok, "nonzero": nz}
                          for l, (ok, nz) in votes.items()}
    else:
        layout_used = py_layout

    resolved = {}
    overrides = 0
    other = "311" if layout_used == "312" else "312"
    for name, addr in addrs.items():
        v = resolve_cached_int(binary, addr, ptr_size, layout_used)
        if v == 0:
            alt = resolve_cached_int(binary, addr, ptr_size, other)
            if alt:  # 备选布局给出非零值：投票误判修正（混合/边界样本）
                v = alt
                overrides += 1
        if v is not None:
            resolved[name] = v
    stats["alt_overrides"] = overrides
    for lit in literals:
        for it in lit["items"]:
            if it["kind"] == "ref" and it["name"] in resolved:
                it["kind"] = "int"
                it["value"] = resolved[it["name"]]
                it["resolved_from"] = it["name"]
        if lit["items"]:
            lit["preview"] = render_literal(lit["items"], lit["kind"],
                                            PREVIEW_ITEMS)
            lit["literal"] = render_literal(lit["items"], lit["kind"], None)
        still = sum(1 for it in lit["items"] if it["kind"] == "ref")
        if still == 0 and lit["items"]:
            lit["note"] = None
        elif still:
            lit["note"] = (f"{still}/{len(lit['items'])} 项仍是未解析引用"
                           "（读不到内存或不是 PyLong——可能是 str/bytes 缓存对象）")
    stats["resolved"] = len(resolved)
    stats["unresolved"] = [n for n in refs if n not in resolved]
    # .bss 识别：未解析的 ref 落在 initialized=False 块里 = 运行期才填充的
    # 对象池，静态永远读不出来——这不是 daemon 问题，提示要走元数据路线
    uninit = fetch_uninit_blocks(binary)
    stats["unresolved_in_bss"] = [n for n in stats["unresolved"]
                                  if in_uninit(uninit, addrs[n])]
    return stats, layout_used


def parse_int(token: str) -> int:
    return int(token, 16) if token.lower().startswith("0x") else int(token)


def c_unescape(s: str) -> str:
    """Best-effort C string unescape for display."""
    def rep(m):
        esc = m.group(1)
        table = {"n": "\n", "t": "\t", "r": "\r", "0": "\0", "\\": "\\", '"': '"', "'": "'"}
        if esc.startswith("x"):
            try:
                return chr(int(esc[1:], 16))
            except ValueError:
                return "\\" + esc
        if esc.isdigit():
            try:
                return chr(int(esc, 8))
            except ValueError:
                return "\\" + esc
        return table.get(esc, "\\" + esc)
    return re.sub(r"\\(x[0-9a-fA-F]{1,2}|[0-7]{1,3}|.)", rep, s)


def load_functions(path: str) -> tuple[str, list[dict]]:
    """Return (input_kind, [{name, address, c_code}])."""
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8", errors="replace")
    try:
        data = json.loads(text)
    except ValueError:
        data = None
    if isinstance(data, dict):
        result = data.get("result") if isinstance(data.get("result"), dict) else data
        if isinstance(result.get("functions"), list):
            funcs = [fn for fn in result["functions"]
                     if isinstance(fn, dict) and isinstance(fn.get("c_code"), str)]
            if funcs:
                return "json", [{"name": fn.get("name", "?"),
                                 "address": fn.get("address", "?"),
                                 "c_code": fn["c_code"]} for fn in funcs]
        if isinstance(result.get("c_code"), str):
            return "json", [{"name": result.get("name", "?"),
                             "address": result.get("address", "?"),
                             "c_code": result["c_code"]}]
        print(f"[错误] 输入是 JSON 但找不到 functions[].c_code / result.c_code: {path}",
              file=sys.stderr)
        sys.exit(1)
    # plain text: split on decompile_all .c sidecar markers when present
    lines = text.splitlines()
    funcs = []
    cur = {"name": "<whole-file>", "address": "?", "lines": []}
    for ln in lines:
        m = FUNC_MARKER_RE.search(ln)
        if m:
            if cur["lines"]:
                funcs.append(cur)
            cur = {"name": m.group(1), "address": m.group(2), "lines": []}
        else:
            cur["lines"].append(ln)
    if cur["lines"]:
        funcs.append(cur)
    return "text", [{"name": f["name"], "address": f["address"],
                     "c_code": "\n".join(f["lines"])} for f in funcs]


def match_const_item(line: str):
    """Return item dict if the line builds a constant, else None."""
    m = LONG_RE.search(line)
    if m:
        return {"kind": "int", "value": parse_int(m.group(1))}
    m = LONG_STR_RE.search(line)
    if m:
        try:
            return {"kind": "int", "value": int(m.group(1), int(m.group(2)))}
        except ValueError:
            return {"kind": "int", "value": None, "raw": m.group(1)}
    m = FLOAT_RE.search(line)
    if m:
        return {"kind": "float", "value": float(m.group(1))}
    m = BYTES_ITEM_RE.search(line)
    if m:
        return {"kind": "bytes", "value": c_unescape(m.group(1))}
    m = UNICODE_RE.search(line)
    if m:
        return {"kind": "str", "value": c_unescape(m.group(1))}
    return None


def collect_items(lines: list[str], start: int, n: int):
    """Collect up to n items from lines[start : start + window]."""
    items = []
    # Cython expands each item to ~5 lines (INCREF check + slot write), so
    # n*4 is not enough in the wild; n*8 covers the pooled-constant pattern.
    end = min(len(lines), start + max(n * 8, 64))
    alias: dict[str, str] = {}

    def resolve(name: str) -> str:
        seen = set()
        while name in alias and name not in seen:
            seen.add(name)
            name = alias[name]
        return name

    for i in range(start, end):
        if len(items) >= n:
            break
        line = lines[i]
        m = ALIAS_RE.match(line)
        if m and m.group(1) != m.group(2):
            alias[m.group(1)] = resolve(m.group(2))
            continue
        item = match_const_item(line)
        if item is not None:
            item["line"] = i + 1
            items.append(item)
            continue
        m = SET_ITEM_RE.search(line)
        if m:
            expr = m.group(3).strip()
            inner = match_const_item(expr)
            if inner is None:
                inner = {"kind": "ref", "name": resolve(expr)}
            inner["index"] = parse_int(m.group(2))
            inner["line"] = i + 1
            items.append(inner)
            continue
        m = SLOT_WRITE_RE.search(line)
        if m:
            items.append({"kind": "ref", "name": resolve(m.group(3)),
                          "index": parse_int(m.group(2)), "line": i + 1})
            continue
        m = DEREF_WRITE_RE.match(line)
        if m:
            items.append({"kind": "ref", "name": resolve(m.group(2)),
                          "index": 0, "line": i + 1})
    # de-dup by (index) keeping code order; sort by index when indices exist
    if any("index" in it for it in items):
        seen = set()
        uniq = []
        for it in items:
            key = it.get("index")
            if key in seen:
                continue
            seen.add(key)
            uniq.append(it)
        items = sorted(uniq, key=lambda it: it.get("index", 0))
    return items


def render_literal(items: list[dict], kind: str, limit: int | None = None):
    shown = items if limit is None else items[:limit]

    def fmt(it):
        if it["kind"] == "ref":
            return "<%s>" % it["name"]
        if it["kind"] == "bytes":
            return "b%r" % it["value"]
        if it["kind"] == "str":
            return repr(it["value"])
        return repr(it.get("value"))

    body = ", ".join(fmt(it) for it in shown)
    if limit is not None and len(items) > limit:
        body += ", ..."
    open_c, close_c = ("(", ")") if kind == "tuple" else ("[", "]")
    return open_c + body + close_c


def scan_function(fn: dict, min_cluster: int):
    c_code = fn["c_code"]
    lines = c_code.splitlines()
    literals = []
    leads = []
    consumed_lines = set()

    for i, line in enumerate(lines):
        m = LIST_NEW_RE.search(line)
        if not m:
            continue
        kind = "list" if m.group(1) == "PyList_New" else "tuple"
        n = parse_int(m.group(2))
        items = collect_items(lines, i + 1, n)
        for it in items:
            consumed_lines.add(it["line"])
        n_ref = sum(1 for it in items if it["kind"] == "ref")
        note = None
        if items and n_ref == len(items):
            note = ("全部列表项来自缓存全局对象（Cython int 对象池 / mstate）——"
                    "值未解析：加 --binary <样本> 自动还原（须先 rpc_driver.py ensure），"
                    "或手工对 ref 名做 xref / 在模块 init 函数里找 PyLong_FromLong 初始化")
        elif n_ref:
            note = f"{n_ref}/{len(items)} 项是全局对象引用，需到对象池解析"
        literals.append({
            "function": fn["name"], "address": fn["address"],
            "kind": kind, "declared_len": n, "found_len": len(items),
            "line": i + 1, "complete": len(items) >= n,
            "preview": render_literal(items, kind, PREVIEW_ITEMS),
            "literal": render_literal(items, kind, None),
            "items": items, "note": note,
        })

    for i, line in enumerate(lines):
        m = BYTES_RE.search(line)
        if m and (i + 1) not in consumed_lines:
            leads.append({"function": fn["name"], "line": i + 1,
                          "call": m.group(1), "value": c_unescape(m.group(2))[:80]})
        m = BUILDVALUE_RE.search(line)
        if m:
            leads.append({"function": fn["name"], "line": i + 1,
                          "call": "Py_BuildValue", "format": m.group(1)})

    # alert mode: clustered small-int PyLong_FromLong not consumed by literals
    hits = []
    for i, line in enumerate(lines):
        if (i + 1) in consumed_lines:
            continue
        m = LONG_RE.search(line)
        if m:
            v = parse_int(m.group(1))
            if 0 <= v <= 255:
                hits.append((i + 1, v))
    clusters = []
    cur = []
    for ln, v in hits:
        if cur and ln - cur[-1][0] > CLUSTER_MAX_GAP:
            clusters.append(cur)
            cur = []
        cur.append((ln, v))
    if cur:
        clusters.append(cur)
    alerts = []
    for cl in clusters:
        if len(cl) >= min_cluster:
            alerts.append({
                "function": fn["name"], "kind": "byte_cluster",
                "count": len(cl), "values": [v for _, v in cl],
                "first_line": cl[0][0], "last_line": cl[-1][0],
            })
    return literals, leads, alerts


def main() -> int:
    ap = argparse.ArgumentParser(
        description="从 Cython 反编译 C 重建 Python 常量字面量（列表/元组/bytes），"
                    "并对疑似字节级常量表（填充表/S盒/置换表）告警")
    ap.add_argument("input", help="反编译 C 文本，或 decompile-all/decompile-function 的 @out JSON")
    ap.add_argument("--json", dest="json_out", default=None, help="把完整报告写入 JSON 文件")
    ap.add_argument("--min-cluster", type=int, default=8,
                    help="告警模式：同一聚集内 0..255 小整数 PyLong_FromLong 的最少个数（默认 8）")
    ap.add_argument("--binary", default=None,
                    help="样本路径（须先 rpc_driver.py ensure）：给出后经 daemon "
                         "把 <DAT_…> 缓存 PyLong 引用还原成 Python 整数值")
    ap.add_argument("--py", dest="py_layout", choices=("auto", "311", "312"),
                    default="auto",
                    help="CPython 布局：312=lv_tag（3.12+）/ 311=ob_size（≤3.11）/"
                         "auto=全体投票自动判别（默认）")
    ap.add_argument("--ptr-size", type=int, choices=(4, 8), default=8,
                    help="指针字节数（默认 8，64 位样本）")
    args = ap.parse_args()

    try:
        input_kind, funcs = load_functions(args.input)
    except OSError as e:
        print(f"[错误] 无法读取输入: {e}", file=sys.stderr)
        return 1

    all_literals, all_leads, all_alerts = [], [], []
    for fn in funcs:
        literals, leads, alerts = scan_function(fn, args.min_cluster)
        all_literals.extend(literals)
        all_leads.extend(leads)
        all_alerts.extend(alerts)

    resolve_stats = None
    if args.binary:
        resolve_stats, _ = resolve_refs(args.binary, all_literals,
                                        args.ptr_size, args.py_layout)
    report = {
        "input": args.input, "input_kind": input_kind,
        "functions_scanned": len(funcs),
        "literals": all_literals, "leads": all_leads, "alerts": all_alerts,
    }
    if resolve_stats is not None:
        report["resolve"] = resolve_stats

    print(f"[const_scan] 输入: {args.input}（{input_kind}），扫描函数 {len(funcs)} 个")
    if resolve_stats is not None and resolve_stats["refs"]:
        print(f"[const_scan] 缓存对象引用 {resolve_stats['refs']} 个，"
              f"已还原 {resolve_stats['resolved']} 个"
              f"（CPython 布局: {resolve_stats['layout']}）")
        if resolve_stats["resolved"] == 0:
            n_bss = len(resolve_stats.get("unresolved_in_bss") or [])
            if n_bss:
                print(f"[提示] {n_bss}/{resolve_stats['refs']} 个未解析引用落在 .bss"
                      "（initialized=False，静态无文件字节）——这是运行期才填充的"
                      "对象池，静态还原对它们**原则上不可能**，不是 daemon 问题。"
                      "改走：ctf-patterns §12 元数据（`__Pyx_InitCachedConstants` / "
                      "`_Pyx_PyCode_New` 的 co_varnames）或运行期取数"
                      "（本机 import 后 `dir()`/`__dict__`、gdb 帧槽位）。")
            else:
                print("[提示] 0 个还原成功——先确认 daemon 已拉起"
                      "（rpc_driver.py ensure <binary>）且 --binary 路径与"
                      " ensure 的是同一样本；若布局判别异常可用 --py 311/312 强制。")
    print()

    if all_literals:
        print(f"════ 重建出的常量字面量（{len(all_literals)} 处）════")
        for lit in all_literals:
            state = "完整" if lit["complete"] else f"部分（{lit['found_len']}/{lit['declared_len']}）"
            print(f"  · {lit['kind']} × {lit['declared_len']}  [{state}]  "
                  f"函数 {lit['function']} @ {lit['address']}，PyList/PyTuple_New 在第 {lit['line']} 行")
            print(f"    预览: {lit['preview']}")
            if lit["note"]:
                print(f"    注意: {lit['note']}")
        print()
    else:
        print("════ 未发现 PyList_New/PyTuple_New 常量构造点 ════")
        print()

    if all_alerts:
        print(f"════ 疑似字节级常量表告警（{len(all_alerts)} 处）════")
        print("  （填充表 / S盒 / 置换表特征：函数内聚集的小整数 PyLong_FromLong；")
        print("    Cython 会把列表常量炸成 int 对象，按字节模式搜 .so 必然搜不到）")
        for al in all_alerts:
            vals = ", ".join(str(v) for v in al["values"][:32])
            more = " ..." if al["count"] > 32 else ""
            print(f"  · 函数 {al['function']}：{al['count']} 个 0..255 常量"
                  f"（第 {al['first_line']}..{al['last_line']} 行）")
            print(f"    值: [{vals}{more}]")
        print()

    if all_leads:
        print(f"════ 其他常量线索（PyBytes_FromString / PyUnicode / Py_BuildValue，{len(all_leads)} 处）════")
        for lead in all_leads[:20]:
            extra = lead.get("value", lead.get("format", ""))
            print(f"  · {lead['call']}  函数 {lead['function']} 第 {lead['line']} 行: {extra!r}")
        if len(all_leads) > 20:
            print(f"  ... 其余 {len(all_leads) - 20} 条见 --json 报告")
        print()

    print(f"[结论] 字面量 {len(all_literals)} 处，告警 {len(all_alerts)} 处，线索 {len(all_leads)} 条。"
          "全量值在 --json 报告里。")

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"[const_scan] JSON 报告已写入: {args.json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
