#!/usr/bin/env python
"""apk_oracle.py - 一键真机 oracle：模拟器内逐候选验证 flag，正负对照成对出报告.

把手工约 20 分钟那套流程（SKILL.md §3.2）全自动串起来：
  检测/创建 AVD → emulator-check accel → 无头启动 emulator → 等 sys.boot_completed
  → install -r → monkey 拉起 → 逐候选：清场 → input text → uiautomator 回读确认
  → 点确认按钮 → 判定：先查视图树文本（success/wrong 正则），查不到则走
  Toast 像素通道（exec-out 裸 RGBA 前后帧差分，toast 不进 uiautomator 树）
  → 相同指纹的 toast 自动分组，裁图供人工/多模态复核定性

纪律：
  - oracle 必须成对：报告区分「正例命中 / 负例被拒绝 / toast 待复核 / 无法判定」，
    只有正例命中且近似错值被拒，才能排除「凡输入皆通过」
  - screencap 证据 PNG 一律设备端落盘再 adb pull——禁止 shell > 重定向
    （ghidra-core references/windows-powershell.md）；自动判读用的 exec-out
    裸 RGBA 走 subprocess 管道，不经 shell 重定向，二进制安全
  - 已在线的设备直接复用且收尾不杀；本脚本拉起的 emulator 收尾自动关停

Usage:
  python apk_oracle.py app.apk --candidates "flag{a},flag{b},flag{nope}"
  python apk_oracle.py app.apk --candidates "x,y" --pkg com.reverse.rotad --avd rotad33
  python apk_oracle.py app.apk --candidates "x,y" --success-re "success" --fail-re "wrong"
  python apk_oracle.py app.apk --candidates "x,y" --timeout 300 --json oracle.json

Exit codes: 0 ok（含候选全部"无法判定"，看报告）, 1 usage error, 3 工具缺失, 4 运行时失败。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import struct
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
import zipfile
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _android_tools as T

BUTTON_TEXT_RE = re.compile(r"确定|确认|验证|提交|检查|ok|confirm|check|submit|verify", re.I)


class OracleError(RuntimeError):
    pass


class Device:
    def __init__(self, adb: str, serial: str | None = None):
        self.adb = adb
        self.serial = serial

    def shell(self, cmd: str, timeout: int = 60) -> str:
        argv = [self.adb] + (["-s", self.serial] if self.serial else []) + ["shell", cmd]
        r = T.run_tool(argv, timeout=timeout)
        return r.stdout.strip()

    def exec(self, *args: str, timeout: int = 300) -> tuple[int, str]:
        argv = [self.adb] + (["-s", self.serial] if self.serial else []) + list(args)
        r = T.run_tool(argv, timeout=timeout)
        return r.returncode, (r.stdout + r.stderr).strip()


# ---------------------------------------------------------------- AVD / emulator

def list_avds(emulator: str) -> list[str]:
    r = T.run_tool([emulator, "-list-avds"], timeout=60)
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip() and not ln.startswith("INFO")]


def ensure_avd(name_hint: str | None) -> str:
    emulator = T.emulator()
    avds = list_avds(emulator)
    if name_hint:
        if name_hint in avds:
            return name_hint
        raise OracleError(f"指定 AVD '{name_hint}' 不存在，现有: {avds or '无'}")
    if avds:
        return avds[0]
    avdmanager = T.avdmanager()
    if not avdmanager:
        raise OracleError("无可用 AVD 且 avdmanager 缺失（sdkmanager 'cmdline-tools;latest'）")
    name = "ctfd"
    print(f"[AVD] 无现成 AVD，创建 {name}（android-33 default x86_64）…")
    r = T.run_tool([avdmanager, "create", "avd", "-n", name, "-k",
                    "system-images;android-33;default;x86_64", "-d", "pixel_5"],
                   timeout=300)
    if r.returncode != 0 or name not in list_avds(emulator):
        raise OracleError("AVD 创建失败（缺 system-images;android-33;default;x86_64？"
                          "先 sdkmanager 'system-images;android-33;default;x86_64'）:\n"
                          + (r.stdout + r.stderr)[:500])
    return name


def online_devices(adb: str) -> list[str]:
    r = T.run_tool([adb, "devices"], timeout=60)
    return [ln.split()[0] for ln in r.stdout.splitlines()[1:]
            if ln.strip().endswith("\tdevice")]


def start_emulator(avd: str, timeout: int) -> tuple[subprocess.Popen, str]:
    emulator = T.emulator()
    check = T.emulator_check()
    if check:
        r = T.run_tool([check, "accel"], timeout=60)
        if r.returncode != 0:
            print(f"[警告] emulator-check accel 未通过（{r.stdout.strip()[:120]}），启动可能极慢")
    print(f"[emulator] 无头启动 AVD '{avd}'（-no-window -no-audio）…")
    proc = subprocess.Popen([emulator, "-avd", avd, "-no-window", "-no-audio",
                             "-no-snapshot-save"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    adb = T.adb()
    serial = None
    deadline = time.time() + timeout
    while time.time() < deadline:
        if proc.poll() is not None:
            raise OracleError(f"emulator 进程提前退出（code {proc.returncode}）")
        for s in online_devices(adb):
            if s.startswith("emulator-"):
                serial = s
                break
        if serial:
            dev = Device(adb, serial)
            dev.exec("wait-for-device", timeout=60)
            if dev.shell("getprop sys.boot_completed", timeout=30) == "1":
                print(f"[emulator] {serial} 启动完成")
                return proc, serial
        time.sleep(3)
    proc.kill()
    raise OracleError(f"等待 sys.boot_completed 超时（{timeout}s）")


# ---------------------------------------------------------------- UI 驱动

def dump_ui(dev: Device, local_dir: str, tag: str) -> ET.Element | None:
    """uiautomator dump 到设备端再 pull 解析；偶发 null root 重试一次。"""
    remote = f"/sdcard/__oracle_{tag}.xml"
    for _ in range(2):
        dev.shell(f"uiautomator dump {remote}", timeout=60)
        local = os.path.join(local_dir, f"ui_{tag}.xml")
        rc, _ = dev.exec("pull", remote, local, timeout=60)
        if rc != 0 or not os.path.isfile(local):
            continue
        try:
            return ET.parse(local).getroot()
        except ET.ParseError:
            continue
    return None


def node_center(node: ET.Element) -> tuple[int, int] | None:
    m = re.fullmatch(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", node.get("bounds", ""))
    if not m:
        return None
    l, t, r, b = map(int, m.groups())
    return (l + r) // 2, (t + b) // 2


def find_nodes(root: ET.Element, pred) -> list[ET.Element]:
    return [n for n in root.iter("node") if pred(n)]


def screencap(dev: Device, local_dir: str, tag: str) -> str | None:
    remote = f"/sdcard/__oracle_{tag}.png"
    dev.shell(f"screencap -p {remote}", timeout=60)
    local = os.path.join(local_dir, f"screen_{tag}.png")
    rc, _ = dev.exec("pull", remote, local, timeout=60)
    return local if rc == 0 and os.path.isfile(local) else None


# ---------------------------------------------------------------- Toast 像素通道
# Toast 不在 uiautomator 视图树里（API 33 实测），OCR 无依赖可用。
# 用 adb exec-out screencap（裸 RGBA 流，subprocess 管道二进制安全——
# 被禁的是 shell 的 > 重定向，不是 exec-out 本身）做前后帧像素差：
#   判定「有没有 toast」并裁出 toast 图供人工/多模态复核；
#   相同内容的 toast 像素指纹相同 → 自动把响应相同的候选分组，
#   只需复核每组一张裁图即可给整组定性（oracle 成对纪律的机器化）。

def raw_screencap(dev: Device) -> tuple[int, int, bytes] | None:
    argv = [dev.adb] + (["-s", dev.serial] if dev.serial else []) + ["exec-out", "screencap"]
    try:
        r = subprocess.run(argv, capture_output=True, timeout=60)
    except (subprocess.TimeoutExpired, OSError):
        return None
    if r.returncode != 0 or len(r.stdout) < 12:
        return None
    w, h, fmt = struct.unpack("<III", r.stdout[:12])
    data = r.stdout[12:w * h * 4 + 12]
    if fmt != 1 or len(data) != w * h * 4:
        return None
    return w, h, data


def toast_diff(f0: tuple[int, int, bytes], f1: tuple[int, int, bytes],
               band=(0.45, 0.92), xspan=(0.10, 0.90), min_pixels=400):
    """在中下横带内找前后帧差异区（toast 出没区，避开状态栏/导航栏）。
    返回 (bbox, 差异像素数)；无显著差异返回 None。"""
    w, h, d0 = f0
    if (w, h) != (f1[0], f1[1]):
        return None
    d1 = f1[2]
    y0, y1 = int(h * band[0]), int(h * band[1])
    x0, x1 = int(w * xspan[0]), int(w * xspan[1])
    minx, miny, maxx, maxy = w, h, -1, -1
    changed = 0
    stride = w * 4
    for y in range(y0, y1):
        ra, rb = d0[y * stride:(y + 1) * stride], d1[y * stride:(y + 1) * stride]
        if ra == rb:
            continue
        for x in range(x0, x1):
            p = x * 4
            if ra[p:p + 4] != rb[p:p + 4]:
                changed += 1
                minx, miny = min(minx, x), min(miny, y)
                maxx, maxy = max(maxx, x), max(maxy, y)
    if changed < min_pixels:
        return None
    return (minx, miny, maxx + 1, maxy + 1), changed


def region_hash(frame: tuple[int, int, bytes], box: tuple[int, int, int, int]) -> str:
    w, _, d = frame
    x0, y0, x1, y1 = box
    md = hashlib.md5()
    for y in range(y0, y1):
        md.update(d[y * w * 4 + x0 * 4: y * w * 4 + x1 * 4])
    return md.hexdigest()[:12]


def png_write(path: str, w: int, h: int, rgba: bytes) -> None:
    """最小 PNG 编码（stdlib zlib）：RGBA → PNG，供 toast 裁图落盘。"""
    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data))
    raw = b"".join(b"\x00" + rgba[y * w * 4:(y + 1) * w * 4] for y in range(h))
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)))
        f.write(chunk(b"IDAT", zlib.compress(raw, 6)))
        f.write(chunk(b"IEND", b""))


def crop_png(frame: tuple[int, int, bytes], box: tuple[int, int, int, int],
             path: str, margin: int = 40) -> None:
    w, h, d = frame
    x0, y0, x1, y1 = box
    x0, y0 = max(0, x0 - margin), max(0, y0 - margin)
    x1, y1 = min(w, x1 + margin), min(h, y1 + margin)
    cw, ch = x1 - x0, y1 - y0
    rows = b"".join(d[y * w * 4 + x0 * 4: y * w * 4 + x1 * 4] for y in range(y0, y1))
    png_write(path, cw, ch, rows)


def clear_field(dev: Device, edit: ET.Element) -> None:
    """确定性清场：按回读到的文本长度发 DEL（不赌长按/全选手势）。"""
    cur = edit.get("text", "") or ""
    dev.shell("input keyevent KEYCODE_MOVE_END")
    for _ in range(len(cur) + 8):
        dev.shell("input keyevent KEYCODE_DEL", timeout=15)


def run_candidate(dev: Device, cand: str, outdir: str, idx: int,
                  success_re: re.Pattern, fail_re: re.Pattern) -> dict:
    tag = f"cand{idx}"
    rec = {"candidate": cand, "input_verified": False, "verdict": "无法判定",
           "evidence": [], "screenshot": None}
    root = dump_ui(dev, outdir, tag + "_before")
    if root is None:
        rec["evidence"].append("uiautomator dump 失败（null root 重试后仍失败）")
        return rec
    edits = find_nodes(root, lambda n: "EditText" in (n.get("class") or ""))
    if not edits:
        rec["evidence"].append("界面上没有 EditText")
        return rec
    center = node_center(edits[0])
    if center:
        dev.shell(f"input tap {center[0]} {center[1]}")
        time.sleep(0.5)
    # 重新 dump 拿焦点后的真实文本长度再清场
    root = dump_ui(dev, outdir, tag + "_focus") or root
    edits = find_nodes(root, lambda n: "EditText" in (n.get("class") or "")) or edits
    clear_field(dev, edits[0])
    dev.shell(f"input text '{cand.replace(chr(32), '%s')}'", timeout=60)
    time.sleep(0.5)

    root = dump_ui(dev, outdir, tag + "_typed")
    if root is not None:
        edits = find_nodes(root, lambda n: "EditText" in (n.get("class") or ""))
        got = edits[0].get("text", "") if edits else ""
        rec["input_verified"] = (got == cand)
        rec["evidence"].append(f"回读输入框: {got!r}" + ("（写入确认）" if rec["input_verified"]
                                                       else f"（期望 {cand!r}，写入未确认）"))
    if not rec["input_verified"]:
        rec["evidence"].append("输入未被回读确认 → 本候选无法判定")
        return rec

    if root is None:
        rec["evidence"].append("写入后 dump 失败，无法定位按钮")
        return rec
    buttons = find_nodes(root, lambda n: n.get("clickable") == "true"
                         and ("Button" in (n.get("class") or "")
                              or BUTTON_TEXT_RE.search(n.get("text") or "")))
    if not buttons:
        buttons = find_nodes(root, lambda n: n.get("clickable") == "true")
    if not buttons:
        rec["evidence"].append("界面上没有 clickable 控件")
        return rec
    text_btns = [b for b in buttons if BUTTON_TEXT_RE.search(b.get("text") or "")]
    btn = (text_btns or buttons)[0]
    center = node_center(btn)
    if center is None:
        rec["evidence"].append("按钮 bounds 无法解析")
        return rec
    rec["evidence"].append(f"点击: {btn.get('text') or btn.get('class')} @ {center}")
    frame0 = raw_screencap(dev)          # 点击前基准帧（键盘同状态，隔离 toast）
    dev.shell(f"input tap {center[0]} {center[1]}")
    time.sleep(0.8)
    frame1 = raw_screencap(dev)          # toast 存活期内抢帧（raw 流比 PNG pull 快）
    time.sleep(0.7)

    root = dump_ui(dev, outdir, tag + "_after")
    rec["screenshot"] = screencap(dev, outdir, tag)
    text_all = ""
    if root is not None:
        text_all = " ".join(filter(None, (n.get("text") for n in root.iter("node"))))
        rec["evidence"].append(f"点击后界面文本: {text_all[:300]!r}")
    if success_re.search(text_all):
        rec["verdict"] = "命中 success"
    elif fail_re.search(text_all):
        rec["verdict"] = "被 wrong 拒绝"
    else:
        # 视图树无结果 → Toast 像素通道（toast 不进 uiautomator 树，API 33 实测）
        diff = toast_diff(frame0, frame1) if frame0 and frame1 else None
        if diff:
            box, npx = diff
            rec["toast_box"] = list(box)
            rec["toast_group"] = region_hash(frame1, box)
            crop = os.path.join(outdir, f"toast_{tag}.png")
            try:
                crop_png(frame1, box, crop)
                rec["toast_crop"] = crop
            except OSError:
                pass
            rec["verdict"] = f"toast 出现（指纹 {rec['toast_group']}，机器不可判读文本）"
            rec["evidence"].append(
                f"toast 像素区 {box}（{npx} px 变化）；视图树无 success/wrong——"
                "响应文本在 toast 裁图里，需人工/多模态复核 toast_*.png 定性；"
                "指纹相同的候选响应相同，每组只需复核一张")
        else:
            rec["evidence"].append("success/wrong 关键字与 toast 像素变化均未检出"
                                   "（截图见 screenshot 字段人工复核）")
    return rec


# ---------------------------------------------------------------- 包名探测

def detect_pkg(apk: str) -> str | None:
    apkanalyzer = T.apkanalyzer()
    if apkanalyzer:
        r = T.run_tool([apkanalyzer, "manifest", "application-id", apk], timeout=120)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    aapt2 = T.aapt2()
    if aapt2:
        r = T.run_tool([aapt2, "dump", "badging", apk], timeout=120)
        m = re.search(r"package: name='([^']+)'", r.stdout)
        if m:
            return m.group(1)
    agpy = T.agpy()
    if agpy:
        r = T.run_tool([agpy, "-c",
                        "import sys;from androguard.core.apk import APK;"
                        "print(APK(sys.argv[1]).get_package())", apk], timeout=180)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    return None


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description="一键真机 oracle（android-re §3.2，正负对照成对）")
    ap.add_argument("apk", help="APK 路径")
    ap.add_argument("--candidates", required=True, help="候选列表，英文逗号分隔")
    ap.add_argument("--pkg", help="包名（缺省自动探测：apkanalyzer → aapt2 → androguard）")
    ap.add_argument("--avd", help="指定 AVD 名（缺省：复用第一个；没有则建 ctfd/android-33 x86_64）")
    ap.add_argument("--timeout", type=int, default=300, help="模拟器启动超时秒数（默认 300）")
    ap.add_argument("--success-re", default="success", help="命中判定正则（默认 success，不区分大小写）")
    ap.add_argument("--fail-re", default="wrong", help="拒绝判定正则（默认 wrong，不区分大小写）")
    ap.add_argument("--json", metavar="OUT", help="结论写 JSON 文件")
    ap.add_argument("--outdir", metavar="DIR", help="证据目录（uiautomator XML/截图；默认临时目录）")
    args = ap.parse_args()

    if not os.path.isfile(args.apk):
        print(f"[用法错误] 文件不存在: {args.apk}")
        return T.EXIT_USAGE
    if not zipfile.is_zipfile(args.apk):
        print(f"[用法错误] 不是合法 APK: {args.apk}")
        return T.EXIT_USAGE
    candidates = [c for c in args.candidates.split(",") if c]
    if not candidates:
        print("[用法错误] --candidates 为空")
        return T.EXIT_USAGE
    if len(candidates) < 2:
        print("[警告] 只给了 1 个候选——oracle 必须成对：请追加一个近似错值作负对照，"
              "否则无法排除「凡输入皆通过」。")

    adb = T.adb()
    if not adb:
        return T.missing("adb", "Android SDK platform-tools：sdkmanager 'platform-tools'")
    if not T.emulator():
        return T.missing("emulator", "Android SDK Emulator：sdkmanager 'emulator'")

    try:
        success_re = re.compile(args.success_re, re.I)
        fail_re = re.compile(args.fail_re, re.I)
    except re.error as e:
        print(f"[用法错误] 正则非法: {e}")
        return T.EXIT_USAGE

    pkg = args.pkg or detect_pkg(args.apk)
    if not pkg:
        print("[用法错误] 包名探测失败（apkanalyzer/aapt2/androguard 均不可用），请 --pkg 指定")
        return T.EXIT_NO_TOOL

    started_proc = None
    outdir = args.outdir or tempfile.mkdtemp(prefix="apk-oracle-")
    os.makedirs(outdir, exist_ok=True)
    report = {"apk": os.path.abspath(args.apk), "pkg": pkg, "candidates": [],
              "success_re": args.success_re, "fail_re": args.fail_re, "outdir": outdir}
    try:
        online = online_devices(adb)
        if online:
            serial = online[0]
            print(f"[device] 复用已在线设备 {serial}（收尾不杀）")
        else:
            avd = ensure_avd(args.avd)
            started_proc, serial = start_emulator(avd, args.timeout)
        dev = Device(adb, serial)
        report["serial"] = serial

        rc, out = dev.exec("install", "-r", args.apk, timeout=300)
        if rc != 0 or "Success" not in out:
            raise OracleError(f"安装失败: {out[:300]}")
        print(f"[install] {pkg} 安装成功")
        dev.shell(f"monkey -p {pkg} -c android.intent.category.LAUNCHER 1", timeout=60)
        time.sleep(4)

        for i, cand in enumerate(candidates):
            print(f"[oracle] 候选 {i + 1}/{len(candidates)}: {cand!r}")
            rec = run_candidate(dev, cand, outdir, i, success_re, fail_re)
            report["candidates"].append(rec)
            print(f"         → {rec['verdict']}")

        hits = [r for r in report["candidates"] if r["verdict"] == "命中 success"]
        rejected = [r for r in report["candidates"] if r["verdict"] == "被 wrong 拒绝"]
        toasts = [r for r in report["candidates"] if r["verdict"].startswith("toast 出现")]
        unknown = [r for r in report["candidates"] if r["verdict"] == "无法判定"]
        print("══ oracle 对照表 ══")
        print(f"  正例命中（{len(hits)}）: {[r['candidate'] for r in hits]}")
        print(f"  负例被拒绝（{len(rejected)}）: {[r['candidate'] for r in rejected]}")
        if toasts:
            groups = {}
            for r in toasts:
                groups.setdefault(r["toast_group"], []).append(r)
            print(f"  toast 响应（{len(toasts)} 个候选，{len(groups)} 组，机器不可判读文本）:")
            for g, rs in sorted(groups.items()):
                print(f"    组 {g}: {[r['candidate'] for r in rs]}  ← 复核 {rs[0].get('toast_crop')}")
            print("    判读方法：每组裁一张 toast_*.png 看文本；success 组=正例命中，wrong 组=负例被拒。")
        print(f"  无法判定（{len(unknown)}）: {[r['candidate'] for r in unknown]}")
        if hits and rejected:
            print("  对照成立：有正例命中且有输入被拒，可排除「凡输入皆通过」。")
        elif hits and not rejected:
            print("  [警告] 只有命中没有被拒样本——必须再喂近似错值做负对照（铁律：oracle 成对）。")
        elif not hits and rejected:
            print("  [提示] 全部候选被拒：候选都不对，回 SKILL.md §2 重新定位校验点。")
        elif toasts:
            print("  [提示] 复核 toast 裁图后回填定性；若两组文本是 success/wrong 各一，对照即成立。")
        else:
            print("  [提示] 全部无法判定：人工看 outdir 里的 ui_*.xml / screen_*.png。")
    except OracleError as e:
        print(f"[运行时失败] {e}")
        returncode = T.EXIT_RUNTIME
    else:
        returncode = 0
    finally:
        if started_proc is not None:
            print("[emulator] 关停本脚本拉起的模拟器…")
            try:
                dev.exec("emu", "kill", timeout=30)
                started_proc.wait(timeout=30)
            except Exception:
                started_proc.kill()
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"[JSON] 已写 {args.json}")
    return returncode


if __name__ == "__main__":
    sys.exit(main())
