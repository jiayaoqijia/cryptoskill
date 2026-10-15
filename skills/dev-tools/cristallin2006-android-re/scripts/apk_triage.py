#!/usr/bin/env python
"""apk_triage.py - APK 一条命令分诊（签名 / Manifest / 逐 dex 自有类统计 / 可疑 API / flag 全扫）.

分诊结论对照 android-re `references/apk-triage.md`：
  - 签名版本判定（§3）：apksigner verify --print-certs 为准；缺失时退 META-INF zip 启发式
  - Manifest 关键字段（§2）：apkanalyzer manifest print（官方 AXML 还原）+ aapt2 badging
  - 多 dex 启发式（§4）：真逻辑常在极小 dex——逐 dex 统计自有类数，升序标注
  - flag 全扫（§5）：所有 dex + resources.arsc + assets 全扫，不只扫 classes.dex

Usage:
  python apk_triage.py app.apk
  python apk_triage.py app.apk --json triage.json
  python apk_triage.py app.apk --own-limit 15      # 每个 dex 列出的自有类条数上限

Exit codes: 0 分诊完成, 1 usage error, 3 必需工具缺失（已优雅降级的不算）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _android_tools as T

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"

# 库包前缀（点分形态；对应 apk-triage.md §4 的 L 前缀表，可按需扩）
LIB_PREFIXES = (
    "android.", "androidx.", "kotlin.", "kotlinx.",
    "com.google.", "org.apache.", "com.squareup.",
    "com.bumptech.", "io.reactivex.", "okhttp3.", "okio.",
    "org.jetbrains.", "org.intellij.", "com.android.",
)

SUSPICIOUS_APIS = {
    "动态加载": [b"DexClassLoader", b"PathClassLoader", b"InMemoryDexClassLoader", b"loadDex"],
    "命令执行": [b"Runtime;->exec", b"Runtime.exec", b"ProcessBuilder", b"/system/bin/su"],
    "网络": [b"HttpURLConnection", b"okhttp3", b"Socket;->", b"usesCleartextTraffic"],
    "加解密/摘要": [b"javax/crypto/Cipher", b"MessageDigest", b"Base64;->", b"SecretKeySpec"],
    "native 边界": [b"System;->loadLibrary", b"loadLibrary", b"getDeclaredMethod"],
}

# R/BuildConfig/Manifest 是 aapt 产物，不算业务自有类
GENERATED_RE = re.compile(r"(^|\.)(R(\$[^.]+)?|BuildConfig|Manifest(\$[^.]+)?)$")

FLAG_RE = re.compile(rb"[A-Za-z0-9_]{1,32}\{[\x20-\x7e]{4,128}\}")
FLAG_NOISE_RE = re.compile(r'^D8\{"backend"')  # d8 编译器标记串，dex 内必有，非 flag


def is_own(dotted: str) -> bool:
    return not dotted.startswith(LIB_PREFIXES) and not GENERATED_RE.search(dotted)


def to_dotted(lname: str) -> str:
    n = lname.strip()
    if n.startswith("L") and n.endswith(";"):
        n = n[1:-1]
    return n.replace("/", ".").replace("$", "$")


# ---------------------------------------------------------------- 签名

def signature_info(apk: str, zf: zipfile.ZipFile) -> dict:
    apksigner = T.apksigner()
    info = {"tool": None, "v1": None, "v2": None, "v3": None, "v3.1": None,
            "certs": [], "verdict": "未知"}
    if apksigner:
        r = T.run_tool([apksigner, "verify", "--print-certs", "--verbose", apk], timeout=180)
        out = r.stdout + r.stderr
        info["tool"] = "apksigner"
        for m in re.finditer(r"Verified using (v[\d.]+) scheme \([^)]*\): (true|false)", out):
            info[m.group(1)] = (m.group(2) == "true")
        info["certs"] = re.findall(r"Signer #\d+ certificate DN: (.+)", out)
        if "DOES NOT VERIFY" in out or "does not verify" in out:
            info["verdict"] = "未通过签名校验（疑似未签名/被改动）→ 若 v1 未签名可改写重签（SKILL.md §4）"
        elif any(info[k] for k in ("v1", "v2", "v3", "v3.1")):
            schemes = [k for k in ("v1", "v2", "v3", "v3.1") if info[k]]
            info["verdict"] = f"已签名（{'+'.join(schemes)}）"
            if info["v1"] is False and (info["v2"] or info["v3"]):
                info["verdict"] += "；纯 v2+ 签名 → 改动必破签名，patch 走 frida"
        else:
            info["verdict"] = "apksigner 无有效输出，结合 META-INF 判断"
    if info["tool"] is None or info["verdict"] == "未知":
        names = set(zf.namelist())
        meta = {n.upper() for n in names if n.upper().startswith("META-INF/")}
        has_manifest = "META-INF/MANIFEST.MF" in meta
        has_cert = any(re.fullmatch(r"META-INF/[^/]+\.(RSA|DSA|EC)", n) for n in meta)
        if info["tool"] is None:
            info["tool"] = "zipfile-META-INF 启发式（apksigner 缺失）"
            if has_manifest and has_cert:
                info["verdict"] = "META-INF 有 MANIFEST.MF + 证书块 → v1 签名痕迹（v2+ 未知，缺 apksigner）"
                info["v1"] = True
            else:
                info["verdict"] = ("META-INF 无 CERT.RSA/MANIFEST.MF → 疑似 v1 未签名"
                                   "（可改写重签，SKILL.md §4；v2+ 需 apksigner 确认）")
                info["v1"] = False
    return info


# ---------------------------------------------------------------- Manifest

def manifest_info(apk: str) -> dict:
    info = {"tool": None, "package": None, "versionCode": None, "versionName": None,
            "debuggable": None, "usesCleartextTraffic": None,
            "application_class": None, "permissions": [], "exported_activities": []}
    xml_text = None
    aapt2 = T.aapt2()
    if aapt2:
        r = T.run_tool([aapt2, "dump", "badging", apk], timeout=180)
        if r.returncode == 0 and r.stdout:
            info["tool"] = "aapt2"
            m = re.search(r"package: name='([^']+)' versionCode='([^']*)' versionName='([^']*)'", r.stdout)
            if m:
                info["package"], info["versionCode"], info["versionName"] = m.groups()
            info["permissions"] = re.findall(r"uses-permission: name='([^']+)'", r.stdout)
    apkanalyzer = T.apkanalyzer()
    if apkanalyzer:
        r = T.run_tool([apkanalyzer, "manifest", "print", apk], timeout=300)
        if r.returncode == 0 and "<manifest" in r.stdout:
            xml_text = r.stdout
            info["tool"] = (info["tool"] or "") + "+apkanalyzer"
    if xml_text is None:
        agpy = T.agpy()
        if agpy:
            code = (
                "import sys\nfrom androguard.core.apk import APK\n"
                "a=APK(sys.argv[1])\nsys.stdout.write(a.get_android_manifest_axml().get_xml().decode('utf-8','replace'))\n"
            )
            r = T.run_tool([agpy, "-c", code, apk], timeout=300)
            if r.returncode == 0 and "<manifest" in r.stdout:
                xml_text = r.stdout
                info["tool"] = (info["tool"] or "") + "+androguard"
    if xml_text:
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            root = None
        if root is not None:
            if info["package"] is None:
                info["package"] = root.get("package")
                info["versionCode"] = root.get(ANDROID_NS + "versionCode")
                info["versionName"] = root.get(ANDROID_NS + "versionName")
            app = root.find("application")
            if app is not None:
                dbg = app.get(ANDROID_NS + "debuggable")
                info["debuggable"] = (dbg == "true") if dbg is not None else False
                cleartext = app.get(ANDROID_NS + "usesCleartextTraffic")
                info["usesCleartextTraffic"] = (cleartext == "true") if cleartext is not None else None
                info["application_class"] = app.get(ANDROID_NS + "name")
                for act in app.findall("activity"):
                    if act.get(ANDROID_NS + "exported") == "true":
                        info["exported_activities"].append(act.get(ANDROID_NS + "name"))
            if not info["permissions"]:
                info["permissions"] = [
                    p.get(ANDROID_NS + "name") for p in root.findall("uses-permission")
                    if p.get(ANDROID_NS + "name")
                ]
    return info


# ---------------------------------------------------------------- 逐 dex 自有类统计

def dex_stats_androguard(apk: str) -> list[dict] | None:
    agpy = T.agpy()
    if not agpy:
        return None
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
        "                'classes': [c.get_name() for c in d.get_classes()]})\n"
        "json.dump(out, sys.stdout)\n"
    )
    r = T.run_tool([agpy, "-c", code, apk], timeout=600)
    if r.returncode != 0 or not r.stdout.strip():
        return None
    try:
        raw = json.loads(r.stdout)
    except json.JSONDecodeError:
        return None
    stats = []
    for entry in raw:
        dotted = [to_dotted(n) for n in entry["classes"]]
        own = sorted(n for n in dotted if is_own(n))
        stats.append({"dex": entry["dex"], "size": entry["size"],
                      "class_count": len(dotted), "own_classes": own, "tool": "androguard"})
    return stats


def dex_stats_apkanalyzer(apk: str, zf: zipfile.ZipFile) -> list[dict] | None:
    """无 androguard 时：逐 dex 抽成单 dex zip 喂 apkanalyzer dex packages。"""
    apkanalyzer = T.apkanalyzer()
    if not apkanalyzer:
        return None
    dex_names = sorted((n for n in zf.namelist() if re.fullmatch(r"classes\d*\.dex", n)),
                       key=lambda n: (len(n), n))
    stats = []
    with tempfile.TemporaryDirectory(prefix="apktriage-") as td:
        for name in dex_names:
            blob = zf.read(name)
            zpath = os.path.join(td, name + ".zip")
            with zipfile.ZipFile(zpath, "w") as z:
                z.writestr("classes.dex", blob)
            r = T.run_tool([apkanalyzer, "dex", "packages", zpath], timeout=600)
            if r.returncode != 0:
                stats.append({"dex": name, "size": len(blob), "class_count": None,
                              "own_classes": None,
                              "tool": "apkanalyzer（该 dex 解析失败）"})
                continue
            dotted = [ln.split()[-1] for ln in r.stdout.splitlines() if ln.startswith("C ")]
            own = sorted(n for n in dotted if is_own(n))
            stats.append({"dex": name, "size": len(blob), "class_count": len(dotted),
                          "own_classes": own, "tool": "apkanalyzer"})
    return stats


# ---------------------------------------------------------------- 扫描面

def scan_bytes(zf: zipfile.ZipFile) -> dict:
    flags, apis = {}, {}
    for name in zf.namelist():
        if not (re.fullmatch(r"classes\d*\.dex", name)
                or name == "resources.arsc"
                or name.startswith("assets/")):
            continue
        try:
            blob = zf.read(name)
        except (KeyError, RuntimeError):
            continue
        for m in FLAG_RE.finditer(blob):
            flag = m.group(0).decode("utf-8", "replace")
            if FLAG_NOISE_RE.match(flag):
                continue
            # 括号内无 ≥3 连续单词字符 → 疑似二进制随机碰撞，标注降信度
            content = flag[flag.index("{") + 1:-1]
            conf = bool(re.search(r"[A-Za-z0-9_]{3,}", content))
            flags.setdefault(flag, {"locations": set(), "low_confidence": not conf})
            flags[flag]["locations"].add(name)
        for cat, needles in SUSPICIOUS_APIS.items():
            hits = {n.decode() for n in needles if n in blob}
            if hits:
                apis.setdefault(cat, {}).setdefault(name, set()).update(hits)
    return {
        "flags": [{"flag": k, "locations": sorted(v["locations"]),
                   "low_confidence": v["low_confidence"]} for k, v in sorted(flags.items())],
        "suspicious_apis": {cat: {entry: sorted(h) for entry, h in sorted(per.items())}
                            for cat, per in apis.items()},
    }


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description="APK 一条命令分诊（android-re §1）")
    ap.add_argument("apk", help="APK 路径")
    ap.add_argument("--json", metavar="OUT", help="结论写 JSON 文件")
    ap.add_argument("--own-limit", type=int, default=15, help="每 dex 列出的自有类条数（默认 15，0=全列）")
    args = ap.parse_args()

    if not os.path.isfile(args.apk):
        print(f"[用法错误] 文件不存在: {args.apk}")
        return T.EXIT_USAGE
    try:
        zf = zipfile.ZipFile(args.apk)
    except zipfile.BadZipFile:
        print(f"[用法错误] 不是合法 zip/APK: {args.apk}")
        return T.EXIT_USAGE

    report = {"apk": os.path.abspath(args.apk)}
    with zf:
        names = zf.namelist()
        report["has_lib"] = any(n.startswith("lib/") for n in names)
        report["dex_files"] = sorted((n for n in names if re.fullmatch(r"classes\d*\.dex", n)),
                                     key=lambda n: (len(n), n))
        report["signature"] = signature_info(args.apk, zf)
        report["manifest"] = manifest_info(args.apk)
        stats = dex_stats_androguard(args.apk) or dex_stats_apkanalyzer(args.apk, zf)
        if stats is None:
            stats = [{"dex": n, "size": zf.getinfo(n).file_size, "class_count": None,
                      "own_classes": None, "tool": "无（androguard/apkanalyzer 均缺失）"}
                     for n in report["dex_files"]]
        stats.sort(key=lambda s: (len(s["own_classes"]) if s["own_classes"] is not None else 10 ** 9,
                                  s["size"]))
        report["dex_stats"] = stats
        report.update(scan_bytes(zf))

    # ---- 人类可读输出
    sig, man = report["signature"], report["manifest"]
    print(f"══ APK 分诊: {os.path.basename(args.apk)} ══")
    print(f"[结构] dex: {', '.join(report['dex_files']) or '无'} | lib/: {'有（注意原生逻辑→ghidra-static）' if report['has_lib'] else '无（纯 DEX）'}")
    print(f"[签名] {sig['verdict']}（来源: {sig['tool']}）")
    if sig["certs"]:
        print(f"       证书: {sig['certs'][0]}")
    print(f"[Manifest] package={man['package']} version={man['versionName']}({man['versionCode']}) "
          f"debuggable={man['debuggable']} cleartext={man['usesCleartextTraffic']}（来源: {man['tool'] or '无'}）")
    if man["application_class"]:
        print(f"       自定义 Application: {man['application_class']}（校验可能提前跑，优先看）")
    if man["exported_activities"]:
        print(f"       exported activity: {', '.join(a for a in man['exported_activities'] if a)}")
    print(f"       权限({len(man['permissions'])}): {', '.join(man['permissions'][:10])}"
          + (" …" if len(man["permissions"]) > 10 else ""))
    print("[多 dex 启发式] 按自有类数升序（真逻辑常在极小 dex，优先人肉通读自有类 <20 的 dex）:")
    for st in report["dex_stats"]:
        own_n = "?" if st["own_classes"] is None else len(st["own_classes"])
        marker = "  ← 优先看" if isinstance(own_n, int) and 0 < own_n < 20 else ""
        print(f"  {st['dex']}: {st['size']} 字节, {st['class_count'] if st['class_count'] is not None else '?'} 类, "
              f"自有类 {own_n}（{st['tool']}）{marker}")
        if st["own_classes"]:
            shown = st["own_classes"] if args.own_limit == 0 else st["own_classes"][:args.own_limit]
            for n in shown:
                print(f"      {n}")
            if args.own_limit and len(st["own_classes"]) > args.own_limit:
                print(f"      … 其余 {len(st['own_classes']) - args.own_limit} 个（--own-limit 0 全列）")
    if report["flags"]:
        print(f"[flag 全扫] 命中 {len(report['flags'])} 条（逐个过真机 oracle 正负对照）:")
        for f in report["flags"]:
            note = "   （低信度：疑似二进制随机碰撞）" if f.get("low_confidence") else ""
            print(f"      {f['flag']}   @ {', '.join(f['locations'])}{note}")
    else:
        print("[flag 全扫] 无直接命中 → flag 可能逐段拼接/变换，转 SKILL.md §2 校验点定位")
    if report["suspicious_apis"]:
        print("[可疑 API]")
        for cat, per in report["suspicious_apis"].items():
            flat = sorted({h for s in per.values() for h in s})
            locs = sorted(per)
            print(f"      {cat}: {', '.join(flat)}  @ {', '.join(locs[:4])}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"[JSON] 已写 {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
