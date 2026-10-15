#!/usr/bin/env python
"""noreturn_fix.py — non-returning 误判的机械化修复（铁律 10⑦ 的下半截）。

铁律 10⑦ 只教「判定不可信」，本脚本补「怎么修」（判例 4307cc95：
UD2 的 SIGILL handler 推进保存的 RIP 让「非法指令」正常返回，Ghidra 把
UD2 判 non-returning → 调用图截断 → 调用者消失/代码染灰，agent 误判
「flag 路径不可达」白走 86 min）。

两种损伤，两个开关：
  a) 函数级：callee 被标 NoReturn → 所有调用者的 CALL 之后被视为不可达。
     修复 = 清标志：--fix <func>
  b) 指令级：UD2/INT3 落在函数体中间、fall-through 被切断 → 其后的真实
     代码显示为死代码。修复 = 补 fall-through override：--flow <insn-addr>

用法：
  python noreturn_fix.py <binary>                  # 体检：列 NoReturn 函数 + 流切断点
  python noreturn_fix.py <binary> --fix 0x401000   # 清该函数 NoReturn 标志
  python noreturn_fix.py <binary> --flow 0x40115d  # UD2 处补 fall-through 到下一条
  python noreturn_fix.py <binary> --flow-clear 0x40115d   # 撤销 override

修后验证（脚本只修视图，不替你验证）：
  1. decompile 原调用者，确认 CALL 之后的代码回来了；
  2. UD2 之后的代码若仍是未定义字节，用 rpc disassemble <next> --force 补反汇编；
  3. 「已修复」本身也是结论——落 ledger.py observe 并配一条能证伪它的命令
     （decompiler-pitfalls 质量门 #6）。

exit: 0 成功 / 1 用法错 / 2 目标未找到 / 3 daemon 不可达（先 rpc_driver ensure）。
注意：合法 no-return 函数（exit/abort/__stack_chk_fail）清标志无害但无收益，
体检报告里它们 terminal 不含 UD2/INT3——只修含 UD2/INT3 的。
"""
from __future__ import annotations

import argparse
import json
import os
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
    """subprocess 调同目录 rpc_driver.py；@out 落临时文件再读 JSON（铁律 3）。"""
    fd, out = tempfile.mkstemp(prefix="dsh_nr_", suffix=".json")
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


_LIST_CODE = r'''
noreturn = []
flowcuts = []
for f in fm.getFunctions(True):
    terms = []
    for ins in listing.getInstructions(f.getBody(), True):
        mn = str(ins.getMnemonicString())
        ft = ins.getFallThrough()
        if ins.getFlowType().isTerminal() or mn in ("UD2", "INT3"):
            terms.append({"addr": str(ins.getAddress()), "mn": mn,
                          "fallthrough": str(ft) if ft else None})
        if mn in ("UD2", "INT3") and ft is None:
            nxt = ins.getAddress().add(ins.getLength())
            flowcuts.append({"func": f.getName(), "addr": str(ins.getAddress()),
                             "mn": mn, "next": str(nxt),
                             "next_undefined": listing.getCodeUnitAt(nxt) is None})
    if f.hasNoReturn():
        noreturn.append({"func": f.getName(), "entry": str(f.getEntryPoint()),
                         "terminal": terms[-3:]})
output_json({"status": "success",
             "noreturn_functions": noreturn,
             "flow_cuts": flowcuts,
             "hint": "terminal 含 UD2/INT3 的才可疑（exit/abort 合法 no-return）；"
                     "修：--fix <entry> 清标志，--flow <addr> 补 fall-through"})
'''

_FIX_CODE = r'''
f = find_function(%(func)r)
if f is None:
    output_json({"status": "error", "error": "function not found: %(func)s"})
else:
    before = bool(f.hasNoReturn())
    tx = program.startTransaction("noreturn-fix")
    ok = False
    try:
        f.setNoReturn(False)
        ok = True
    finally:
        program.endTransaction(tx, ok)
    output_json({"status": "success", "func": f.getName(),
                 "entry": str(f.getEntryPoint()),
                 "noReturn_before": before, "noReturn_after": bool(f.hasNoReturn()),
                 "next": "重新 decompile 各调用者确认 CALL 之后代码恢复；"
                         "修复结论落 ledger.py observe"})
'''

_FLOW_CODE = r'''
results = []
tx = program.startTransaction("flow-override")
ok = False
try:
    for spec, clear in %(ops)s:
        ins = listing.getInstructionAt(toAddr(spec))
        if ins is None:
            results.append({"addr": spec, "status": "error",
                            "error": "no instruction at address"})
            continue
        if clear:
            ins.clearFallThroughOverride()
            results.append({"addr": spec, "status": "cleared"})
        else:
            nxt = ins.getAddress().add(ins.getLength())
            ins.setFallThrough(nxt)
            results.append({"addr": spec, "mn": str(ins.getMnemonicString()),
                            "status": "ok", "fallthrough": str(nxt)})
    ok = True
finally:
    program.endTransaction(tx, ok)
output_json({"status": "success", "results": results,
             "next": "override 之后若下游仍是未定义字节：rpc disassemble <next> --force；"
                     "再 decompile 验证调用图恢复"})
'''


def main():
    ap = argparse.ArgumentParser(
        description="non-returning 误判修复：体检 / 清 NoReturn / 补 fall-through")
    ap.add_argument("binary", help="目标二进制（rpc 已加载或可 ensure 的路径）")
    ap.add_argument("--fix", metavar="FUNC", help="清该函数的 NoReturn 标志")
    ap.add_argument("--flow", action="append", default=[], metavar="ADDR",
                    help="在该指令补 fall-through override 到下一条（可重复）")
    ap.add_argument("--flow-clear", action="append", default=[], metavar="ADDR",
                    help="撤销该指令的 fall-through override（可重复）")
    ap.add_argument("--keep-code", action="store_true", help="保留生成的 pyghidra 代码")
    args = ap.parse_args()

    modes = bool(args.fix) + bool(args.flow) + bool(args.flow_clear)
    if modes > 1 and args.fix:
        print("FATAL: --fix 与 --flow/--flow-clear 分开跑（修完一批看一次效果）",
              file=sys.stderr)
        return 1

    if args.fix:
        code = _FIX_CODE % {"func": args.fix}
    elif args.flow or args.flow_clear:
        ops = [(a, False) for a in args.flow] + [(a, True) for a in args.flow_clear]
        code = _FLOW_CODE % {"ops": repr(ops)}
    else:
        code = _LIST_CODE

    fd, code_path = tempfile.mkstemp(prefix="dsh_nr_", suffix=".py")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(code)
    try:
        result = rpc_call(args.binary, "exec-code", code_path)
    except RpcError as e:
        print(f"FATAL: {e}", file=sys.stderr)
        return 3 if e.daemon else 2
    finally:
        if args.keep_code:
            print(f"code file: {code_path}")
        else:
            try:
                os.unlink(code_path)
            except OSError:
                pass

    if result.get("status") == "error":
        print(json.dumps(result, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
