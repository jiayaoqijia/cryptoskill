#!/usr/bin/env python
"""axml_decompile.py - 二进制 AndroidManifest.xml（AXML）→ 文本 XML.

铁律 11：不手写 AXML 解析器（实测踩过两个偏移坑）。还原链路按优先级：
  APK 输入：  aapt2 dump xmltree → apkanalyzer manifest print → androguard
  裸 AXML 输入：androguard（aapt2/apkanalyzer 只吃完整 APK）

Usage:
  python axml_decompile.py app.apk                       # 打印文本 Manifest
  python axml_decompile.py AndroidManifest.xml           # 裸二进制 AXML
  python axml_decompile.py app.apk --out manifest.xml
  python axml_decompile.py app.apk --json out.json

Exit codes: 0 ok, 1 usage error, 3 工具缺失。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _android_tools as T


def from_apk_aapt2(apk: str) -> str | None:
    aapt2 = T.aapt2()
    if not aapt2:
        return None
    r = T.run_tool([aapt2, "dump", "xmltree", apk, "--file", "AndroidManifest.xml"], timeout=180)
    if r.returncode != 0 or "N:" not in r.stdout and "E: manifest" not in r.stdout:
        return None
    return r.stdout  # xmltree 是缩进树形态，不是合法 XML，但字段全在


def from_apk_apkanalyzer(apk: str) -> str | None:
    apkanalyzer = T.apkanalyzer()
    if not apkanalyzer:
        return None
    r = T.run_tool([apkanalyzer, "manifest", "print", apk], timeout=300)
    if r.returncode == 0 and "<manifest" in r.stdout:
        return r.stdout
    return None


def axml_via_androguard(path: str, is_apk: bool) -> str | None:
    agpy = T.agpy()
    if not agpy:
        return None
    if is_apk:
        code = (
            "import sys\nfrom androguard.core.apk import APK\n"
            "sys.stdout.write(APK(sys.argv[1]).get_android_manifest_axml().get_xml().decode('utf-8','replace'))\n"
        )
    else:
        code = (
            "import sys\nfrom androguard.core.axml import AXMLPrinter\n"
            "sys.stdout.write(AXMLPrinter(open(sys.argv[1],'rb').read()).get_xml().decode('utf-8','replace'))\n"
        )
    r = T.run_tool([agpy, "-c", code, path], timeout=300)
    if r.returncode == 0 and "<manifest" in r.stdout:
        return r.stdout
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="二进制 AndroidManifest.xml → 文本（包官方工具，不手写解析）")
    ap.add_argument("input", help="APK 路径或裸二进制 AndroidManifest.xml")
    ap.add_argument("--out", metavar="FILE", help="文本写到文件（默认打印到 stdout）")
    ap.add_argument("--json", metavar="OUT", help="结论写 JSON 文件")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        print(f"[用法错误] 文件不存在: {args.input}")
        return T.EXIT_USAGE

    is_apk = zipfile.is_zipfile(args.input)
    text, tool = None, None

    if is_apk:
        text = from_apk_aapt2(args.input)
        if text is not None:
            tool = "aapt2 dump xmltree"
        if text is None:
            text = from_apk_apkanalyzer(args.input)
            if text is not None:
                tool = "apkanalyzer manifest print"
        if text is None:
            text = axml_via_androguard(args.input, True)
            if text is not None:
                tool = "androguard"
        if text is None:
            return T.missing("aapt2 / apkanalyzer / androguard",
                             "aapt2 在 Android SDK build-tools（sdkmanager 'build-tools;37.0.0'）；"
                             "apkanalyzer 在 cmdline-tools；androguard 用 pip install androguard")
    else:
        text = axml_via_androguard(args.input, False)
        if text is not None:
            tool = "androguard"
        if text is None:
            # 裸 AXML 时 aapt2/apkanalyzer 帮不上；也可能是文本 XML 直接给了
            with open(args.input, "rb") as f:
                head = f.read(4096)
            if head.lstrip().startswith(b"<"):
                print("[提示] 输入本身已是文本 XML，原样输出。")
                with open(args.input, "r", encoding="utf-8", errors="replace") as f:
                    text, tool = f.read(), "原文（已是文本）"
            else:
                return T.missing("androguard",
                                 "裸二进制 AXML 只有 androguard 能免解析还原：pip install androguard；"
                                 "或传入完整 APK 走 aapt2/apkanalyzer")

    result = {"input": os.path.abspath(args.input), "is_apk": is_apk, "tool": tool, "xml": text}
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[已写出] {args.out}（来源: {tool}）")
    else:
        print(text)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[JSON] 已写 {args.json}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
