#!/usr/bin/env python
"""dex_triage.py - 多 dex 枚举与扫描（类/方法/字符串 + 包前缀过滤 + 关键词扫描）.

包 androguard（androguard.core.dex）或 apkanalyzer（dex packages），不手写 DEX 解析。
配合 apk_triage.py 的多 dex 启发式：自有类 <20 的 dex 优先人肉通读。

Usage:
  python dex_triage.py app.apk                          # 全 dex 概览
  python dex_triage.py app.apk --pkg com.reverse        # 只看指定包前缀
  python dex_triage.py app.apk --scan success           # 字符串/类名关键词扫描
  python dex_triage.py classes3.dex --scan flag         # 直接喂 dex 文件
  python dex_triage.py app.apk --pkg com.reverse --list-methods --json out.json

Exit codes: 0 ok, 1 usage error, 3 工具缺失。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _android_tools as T

LIB_PREFIXES = (
    "android.", "androidx.", "kotlin.", "kotlinx.",
    "com.google.", "org.apache.", "com.squareup.",
    "com.bumptech.", "io.reactivex.", "okhttp3.", "okio.",
)
GENERATED_RE = re.compile(r"(^|\.)(R(\$[^.]+)?|BuildConfig|Manifest(\$[^.]+)?)$")


def to_dotted(lname: str) -> str:
    n = lname.strip()
    if n.startswith("L") and n.endswith(";"):
        n = n[1:-1]
    return n.replace("/", ".")


def norm_pkg(prefix: str) -> str:
    p = prefix.strip()
    if p.startswith("L"):
        p = p[1:]
    p = p.rstrip(";").replace("/", ".")
    return p.rstrip(".") + "."


# ---------------------------------------------------------------- androguard 路线

def via_androguard(path: str, is_apk: bool) -> list[dict] | None:
    agpy = T.agpy()
    if not agpy:
        return None
    if is_apk:
        code = (
            "import sys, json, re\n"
            "from androguard.core.apk import APK\n"
            "from androguard.core.dex import DEX\n"
            "a = APK(sys.argv[1])\n"
            "out = []\n"
            "for n in a.get_files():\n"
            "    if not re.fullmatch(r'classes\\d*\\.dex', n):\n"
            "        continue\n"
            "    blob = a.get_file(n)\n"
            "    d = DEX(blob)\n"
            "    out.append({'dex': n, 'size': len(blob),\n"
            "        'classes': [c.get_name() for c in d.get_classes()],\n"
            "        'methods': [c.get_name() + '->' + m.get_name() + m.get_descriptor()\n"
            "                    for c in d.get_classes() for m in c.get_methods()],\n"
            "        'strings': [str(s) for s in d.get_strings()]})\n"
            "json.dump(out, sys.stdout)\n"
        )
        r = T.run_tool([agpy, "-c", code, path], timeout=900)
    else:
        code = (
            "import sys, json\n"
            "from androguard.core.dex import DEX\n"
            "d = DEX(open(sys.argv[1],'rb').read())\n"
            "json.dump([{'dex': sys.argv[1], 'size': len(open(sys.argv[1],'rb').read()),\n"
            "    'classes': [c.get_name() for c in d.get_classes()],\n"
            "    'methods': [c.get_name() + '->' + m.get_name() + m.get_descriptor()\n"
            "                for c in d.get_classes() for m in c.get_methods()],\n"
            "    'strings': [str(s) for s in d.get_strings()]}], sys.stdout)\n"
        )
        r = T.run_tool([agpy, "-c", code, path], timeout=900)
    if r.returncode != 0 or not r.stdout.strip():
        print(f"[降级] androguard 失败: {r.stderr.strip()[:200]}", file=sys.stderr)
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


# ---------------------------------------------------------------- apkanalyzer 路线（无字符串表）

def via_apkanalyzer(apk: str) -> list[dict] | None:
    apkanalyzer = T.apkanalyzer()
    if not apkanalyzer:
        return None
    try:
        zf = zipfile.ZipFile(apk)
    except zipfile.BadZipFile:
        return None
    with zf:
        dex_names = sorted((n for n in zf.namelist() if re.fullmatch(r"classes\d*\.dex", n)),
                           key=lambda n: (len(n), n))
        blobs = [(n, zf.read(n)) for n in dex_names]
    out = []
    with tempfile.TemporaryDirectory(prefix="dextriage-") as td:
        for name, blob in blobs:
            zpath = os.path.join(td, name + ".zip")
            with zipfile.ZipFile(zpath, "w") as z:
                z.writestr("classes.dex", blob)
            r = T.run_tool([apkanalyzer, "dex", "packages", zpath], timeout=600)
            if r.returncode != 0:
                continue
            classes, methods = [], []
            for ln in r.stdout.splitlines():
                if ln.startswith("C "):
                    classes.append(ln.split()[-1])
                elif ln.startswith("M "):
                    parts = ln.split(None, 5)
                    if len(parts) == 6:
                        methods.append(parts[4] + " " + parts[5])
            # apkanalyzer 不给字符串表；strings 退化用类/方法名凑扫描面
            out.append({"size": len(blob), "classes": classes, "methods": methods,
                        "strings": sorted(set(classes + methods)),
                        "dex": name, "strings_note": "apkanalyzer 路线无字符串表，扫描面=类/方法名"})
    return out or None


def main() -> int:
    ap = argparse.ArgumentParser(description="多 dex 枚举与扫描（android-re apk-triage §4）")
    ap.add_argument("input", help="APK 或 .dex 路径")
    ap.add_argument("--pkg", metavar="PREFIX", help="包名前缀过滤（点分或 L 形态均可，如 com.reverse）")
    ap.add_argument("--scan", metavar="KEYWORD", help="关键词扫描（字符串表 + 类/方法名，不区分大小写）")
    ap.add_argument("--list-methods", action="store_true", help="连同方法一起列出（默认只列类）")
    ap.add_argument("--own-only", action="store_true", help="只显示自有类（排除 androidx/kotlin/com.google 等库包）")
    ap.add_argument("--json", metavar="OUT", help="结论写 JSON 文件")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        print(f"[用法错误] 文件不存在: {args.input}")
        return T.EXIT_USAGE
    is_apk = zipfile.is_zipfile(args.input)
    if not is_apk and not args.input.lower().endswith(".dex"):
        print(f"[用法错误] 不是 APK/zip 也不像 .dex: {args.input}")
        return T.EXIT_USAGE

    dexes = via_androguard(args.input, is_apk)
    tool = "androguard"
    if dexes is None:
        if not is_apk:
            return T.missing("androguard", "裸 .dex 枚举需 androguard：pip install androguard；"
                                           "或把 dex 包回 APK 走 apkanalyzer")
        dexes = via_apkanalyzer(args.input)
        tool = "apkanalyzer"
    if dexes is None:
        return T.missing("androguard / apkanalyzer",
                         "androguard: pip install androguard；apkanalyzer 在 SDK cmdline-tools/latest/bin")

    pkg = norm_pkg(args.pkg) if args.pkg else None
    kw = args.scan.lower() if args.scan else None

    report = {"input": os.path.abspath(args.input), "tool": tool,
              "pkg_filter": args.pkg, "scan": args.scan, "dexes": []}
    print(f"══ dex 枚举: {os.path.basename(args.input)}（来源: {tool}，共 {len(dexes)} 个 dex）══")
    for i, d in enumerate(dexes):
        classes = [to_dotted(c) for c in d["classes"]]
        if args.own_only:
            classes = [c for c in classes
                       if not c.startswith(LIB_PREFIXES) and not GENERATED_RE.search(c)]
        if pkg:
            classes = [c for c in classes if c.startswith(pkg)]
        methods = d.get("methods", [])
        if pkg:
            methods = [m for m in methods if to_dotted(m.split("->")[0]).startswith(pkg)]
        scan_hits = []
        if kw:
            hay = list(d.get("strings", [])) + classes + methods
            scan_hits = sorted({h for h in hay if kw in h.lower()})
        entry = {"index": i, "dex": d.get("dex", f"dex#{i}"), "size": d["size"],
                 "class_count_total": len(d["classes"]), "classes_shown": len(classes),
                 "classes": classes, "scan_hits": scan_hits}
        if args.list_methods:
            entry["methods"] = methods
        if d.get("strings_note"):
            entry["strings_note"] = d["strings_note"]
        report["dexes"].append(entry)

        print(f"[{entry['dex']}] {d['size']} 字节, 类 {len(d['classes'])} 个"
              + (f"，过滤后 {len(classes)} 个" if len(classes) != len(d["classes"]) else ""))
        for c in classes[:40]:
            print(f"    C {c}")
        if len(classes) > 40:
            print(f"    … 其余 {len(classes) - 40} 个（用 --json 看全量）")
        if args.list_methods:
            for m in methods[:60]:
                print(f"    M {m}")
            if len(methods) > 60:
                print(f"    … 其余 {len(methods) - 60} 个（用 --json 看全量）")
        if kw:
            print(f"    扫描 '{args.scan}' 命中 {len(scan_hits)} 条:")
            for h in scan_hits[:30]:
                print(f"      {h}")
            if len(scan_hits) > 30:
                print(f"      … 其余 {len(scan_hits) - 30} 条（用 --json 看全量）")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"[JSON] 已写 {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
