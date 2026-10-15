#!/usr/bin/env python
"""dex_disasm.py - Dalvik 反汇编（包官方 apkanalyzer，内置自检）.

铁律 11：绝不手写 opcode 表/反汇编器——上次手写 DEX 反汇编器出过多塞一个
opcode 表条目、if-lt 被读成 if-ne 的静默偏移事故。本脚本只包官方
apkanalyzer（dex code，smali 输出带行号/局部变量名）。

--selftest：用内置 fixture（javac --release 11 预编译的 Fx.class，base64 内嵌）
现场 d8 出 dex → apkanalyzer 反汇编 → 断言输出包含预期 opcode 序列
（含条件跳转 if-gez/if-le——正是上次被读错的那类 opcode）。自检不过 exit 2
并打印「工具输出与预期不符，禁止引用」；fixture 无法构建（缺 d8）exit 3。

Usage:
  python dex_disasm.py app.apk --class com.reverse.rotad.ROT14
  python dex_disasm.py app.apk --class com.reverse.rotad.ROT14 --method "rot14(Ljava/lang/String;)Ljava/lang/String;"
  python dex_disasm.py classes3.dex --class com.reverse.rotad.ROT14 --json out.json
  python dex_disasm.py --selftest

Exit codes: 0 ok, 1 usage error, 2 自检失败（输出禁止引用）, 3 工具缺失。
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import tempfile
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _android_tools as T

# 内置自检 fixture：Fx.java（javac --release 11）→ Fx.class
#   public class Fx {
#       public static int clamp(int v) {
#           if (v < 0) return -1;      // if-gez
#           if (v > 100) return 1;     // if-le
#           return v % 26;             // rem-int/lit8
#       }
#   }
FIXTURE_CLASS_B64 = (
    "yv66vgAAADcAEAoAAgADBwAEDAAFAAYBABBqYXZhL2xhbmcvT2JqZWN0AQAGPGluaXQ+AQADKClW"
    "BwAIAQACRngBAARDb2RlAQAPTGluZU51bWJlclRhYmxlAQAFY2xhbXABAAQoSSlJAQANU3RhY2tN"
    "YXBUYWJsZQEACkNvdXJjZUZpbGUBAAdGeC5qYXZhACEABwACAAAAAAACAAEABQAGAAEACQAAAB0A"
    "AQABAAAABSq3AAGxAAAAAQAKAAAABgABAAAAAQAJAAsADAABAAkAAAA9AAIAAQAAABManAAFAqwa"
    "EGSkAAUErBoQGnCsAAAAAgAKAAAADgADAAAAAwAGAAQADgAFAA0AAAAEAAIGBwABAA4AAAACAA8="
)
FIXTURE_CLASS = "Fx"
FIXTURE_METHOD = "clamp(I)I"
# 预期 opcode 序列（mnemonic 子串断言）：覆盖条件跳转 + 常量 + 算术，
# 正是手写 opcode 表偏移事故中会静默错位的那几类
FIXTURE_EXPECT = ["if-gez", "if-le", "rem-int/lit8", "const/4", "return"]


def norm_class(name: str) -> str:
    """接受点分或 L 形态，统一给 apkanalyzer 的点分形态。"""
    n = name.strip()
    if n.startswith("L") and n.endswith(";"):
        n = n[1:-1]
    return n.replace("/", ".")


def disasm(apkanalyzer: str, apk_or_zip: str, cls: str, method: str | None) -> tuple[int, str]:
    argv = [apkanalyzer, "dex", "code", "--class", cls]
    if method:
        argv += ["--method", method]
    argv.append(apk_or_zip)
    r = T.run_tool(argv, timeout=600)
    return r.returncode, r.stdout + r.stderr


def selftest() -> int:
    print("[自检] fixture: Fx.clamp(I)I（内置预编译 class → d8 → apkanalyzer）")
    apkanalyzer = T.apkanalyzer()
    if not apkanalyzer:
        return T.missing("apkanalyzer", "SDK cmdline-tools：sdkmanager 'cmdline-tools;latest'")
    d8 = T.d8()
    if not d8:
        return T.missing("d8", "SDK build-tools：sdkmanager 'build-tools;37.0.0'")
    with tempfile.TemporaryDirectory(prefix="dexselftest-") as td:
        with open(os.path.join(td, "Fx.class"), "wb") as f:
            f.write(base64.b64decode(FIXTURE_CLASS_B64))
        r = T.run_tool([d8, "--min-api", "21", "Fx.class"], timeout=300, cwd=td)
        if not os.path.isfile(os.path.join(td, "classes.dex")):
            print(f"[自检] d8 未产出 classes.dex: {r.stderr.strip()[:300]}")
            return T.EXIT_NO_TOOL
        zpath = os.path.join(td, "fx.zip")
        with zipfile.ZipFile(zpath, "w") as z:
            z.write(os.path.join(td, "classes.dex"), "classes.dex")
        rc, out = disasm(apkanalyzer, zpath, FIXTURE_CLASS, FIXTURE_METHOD)
    if rc != 0:
        print(f"[自检] apkanalyzer 调用失败:\n{out[:500]}")
        print("工具输出与预期不符，禁止引用。")
        return T.EXIT_SELFTEST
    missing_ops = [op for op in FIXTURE_EXPECT if op not in out]
    if missing_ops:
        print(f"[自检] 反汇编缺预期 opcode: {missing_ops}")
        print("──── 实际输出 ────")
        print(out)
        print("工具输出与预期不符，禁止引用。")
        return T.EXIT_SELFTEST
    print(f"[自检] 通过：预期 opcode {FIXTURE_EXPECT} 全部命中，apkanalyzer 输出可引用。")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Dalvik 反汇编（包 apkanalyzer dex code，不手写 opcode 表）")
    ap.add_argument("input", nargs="?", help="APK 或 .dex 路径（--selftest 时省略）")
    ap.add_argument("--class", dest="cls", metavar="CLASS", help="类名（点分或 L 形态）")
    ap.add_argument("--method", metavar="SIG", help='方法签名，形如 name(Ljava/lang/String;I)V')
    ap.add_argument("--json", metavar="OUT", help="结论写 JSON 文件")
    ap.add_argument("--selftest", action="store_true", help="内置 fixture 自检（不反汇编业务 dex）")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if not args.input or not args.cls:
        print("[用法错误] 需要 <apk|dex> 与 --class（或改用 --selftest）")
        return T.EXIT_USAGE
    if not os.path.isfile(args.input):
        print(f"[用法错误] 文件不存在: {args.input}")
        return T.EXIT_USAGE

    apkanalyzer = T.apkanalyzer()
    if not apkanalyzer:
        return T.missing("apkanalyzer", "SDK cmdline-tools：sdkmanager 'cmdline-tools;latest'")

    cls = norm_class(args.cls)
    target = args.input
    tmp = None
    if not zipfile.is_zipfile(args.input):
        if not args.input.lower().endswith(".dex"):
            print(f"[用法错误] 不是 APK/zip 也不像 .dex: {args.input}")
            return T.EXIT_USAGE
        # 裸 .dex：包一层 zip 喂 apkanalyzer（官方工具不吃裸 dex）
        tmp = tempfile.TemporaryDirectory(prefix="dexdisasm-")
        target = os.path.join(tmp.name, "wrapped.zip")
        with zipfile.ZipFile(target, "w") as z:
            z.write(args.input, "classes.dex")

    try:
        rc, out = disasm(apkanalyzer, target, cls, args.method)
    finally:
        if tmp is not None:
            tmp.cleanup()

    if rc != 0 or re.search(r"^\s*ERROR", out, re.M):
        # apkanalyzer 报错时把 --method 形态提示一起给
        print(out.strip() or "[apkanalyzer 无输出]")
        if args.method:
            print("[提示] --method 签名必须是 smali 形态，如 "
                  "\"rot14(Ljava/lang/String;)Ljava/lang/String;\"；"
                  "不带 --method 可先整类反汇编再对照 dex packages 输出确认签名。")
        return T.EXIT_RUNTIME

    print(out)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"input": os.path.abspath(args.input), "class": cls,
                       "method": args.method, "tool": "apkanalyzer dex code",
                       "smali": out}, f, ensure_ascii=False, indent=2)
        print(f"[JSON] 已写 {args.json}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
