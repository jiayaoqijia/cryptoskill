#!/usr/bin/env python
"""Environment self-check for the ghidra-core skill (replaces the old
plugin's ghidra_status/ghidra_capabilities).

Host-side tool (run with any Python 3, NOT through driver.py exec):

  python doctor.py            # human-readable + JSON summary
  python doctor.py "@<path>"  # also write the JSON to <path>

Exit code 0 when every check passes, 1 otherwise.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import driver  # noqa: E402 - reuse the skill's environment resolution

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


def check(label, ok, detail=""):
    return {"check": label, "ok": bool(ok), "detail": detail}


# ── Toolchain registry ────────────────────────────────────────────────────────
# Single source of truth for external-tool availability across the skill
# family.  kind: "path" (explicit file), "which" (PATH lookup), "pyimport"
# (import probe inside the re-tools venv python).
_IS_NT = os.name == "nt"
_IS_LINUX = sys.platform.startswith("linux")
if _IS_NT:
    _RE_TOOLS = Path.home() / "Desktop" / "src" / "re-tools-venv" / "Scripts"
    _TOOLS_DIR = Path.home() / "Desktop" / "src" / "tools"
    _UNP_VENV = Path.home() / "Desktop" / "src" / "unpacker-venv" / "Scripts"
else:  # WSL/Linux 部署：venv 在 $HOME 下，系统工具走 apt/PATH
    _RE_TOOLS = Path.home() / "re-tools-venv" / "bin"
    _TOOLS_DIR = Path.home() / "tools"
    _UNP_VENV = Path.home() / "unpacker-venv" / "bin"
_VENV_PY = "python.exe" if _IS_NT else "python"


_WSL_PY_VENV = "/root/re-pwn-venv"  # WSL Ubuntu 内的 pwn venv


def _wsl_ok():
    proc = subprocess.run(["wsl", "-d", "Ubuntu", "-u", "root", "-e",
                           "bash", "-lc", "true"],
                          capture_output=True, timeout=30)
    return proc.returncode == 0


def _probe(entry):
    import shutil

    kind = entry.kind
    if kind == "path":
        p = Path(entry.path).expanduser()
        return p.is_file(), str(p)
    if kind == "which":
        found = shutil.which(entry.exe)
        return bool(found), found or f"{entry.exe} not on PATH"
    if kind == "pyimport":
        venv = Path(entry.venv) if getattr(entry, "venv", None) else _RE_TOOLS
        py = venv / _VENV_PY
        if not py.is_file():
            return False, f"venv missing ({py})"
        proc = subprocess.run(
            [str(py), "-c", f"import {entry.module}"],
            capture_output=True, text=True, timeout=60)
        ok = proc.returncode == 0
        return ok, f"module {entry.module} in {venv.parent.name}: {'ok' if ok else proc.stderr.strip()[:120]}"
    if kind == "wsl":
        # entry.cmd runs inside `wsl -d Ubuntu -u root bash -lc` on Windows.
        # On Linux the "WSL tools" ARE the native tools — run the same probe
        # directly so the registry entries work unchanged on both platforms.
        if _IS_LINUX:
            proc = subprocess.run(["bash", "-lc", entry.cmd],
                                  capture_output=True, text=True, timeout=60)
            ok = proc.returncode == 0
            out = ((proc.stdout or "") + (proc.stderr or "")).strip().splitlines()
            return ok, "native: " + (out[0][:120] if out else entry.cmd)
        if not _wsl_ok():
            return False, "WSL distro Ubuntu not available"
        proc = subprocess.run(["wsl", "-d", "Ubuntu", "-u", "root", "-e",
                               "bash", "-lc", entry.cmd],
                              capture_output=True, text=True, timeout=60)
        ok = proc.returncode == 0
        out = ((proc.stdout or "") + (proc.stderr or "")).strip().splitlines()
        return ok, "wsl: " + (out[0][:120] if out else entry.cmd)
    raise ValueError(kind)


class _Tool:
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def check(self):
        ok, detail = _probe(self)
        status = "available" if ok else (
            "missing (WARN, tier A)" if self.tier == "A"
            else f"not installed (tier {self.tier}, 按需)")
        return {
            "check": f"tool:{self.name}", "name": self.name, "tier": self.tier,
            "ok": ok, "status": status, "detail": detail,
            "referenced_by": self.refs, "install_hint": self.hint,
        }


TOOL_REGISTRY = [
    # ── Tier A: lightweight, high-frequency, installed ──
    _Tool(name="checksec", tier="A", kind="path",
          path=str(_RE_TOOLS / "checksec.exe"), refs="re-triage",
          hint="pip install checksec.py（进 re-tools-venv）；Windows GBK 控制台跑时前置 PYTHONUTF8=1（rich 进度条 Unicode 崩溃）"),
    _Tool(name="goresym", tier="A", kind="path",
          path=str(_TOOLS_DIR / "goresym" / "GoReSym.exe"), refs="re-triage",
          hint="github.com/mandiant/GoReSym release win64 zip 解压到 tools/goresym/"),
    _Tool(name="pyinstxtractor", tier="A", kind="path",
          path=str(_TOOLS_DIR / "pyinstxtractor" / "pyinstxtractor.py"), refs="re-triage",
          hint="github.com/extremecoders-re/pyinstxtractor 单文件拷到 tools/pyinstxtractor/"),
    _Tool(name="frida", tier="A", kind="path",
          path=str(_RE_TOOLS / "frida.exe"),
          refs="ghidra-core/ghidra-static/vuln-audit/re-unpack",
          hint="pip install frida-tools（进 re-tools-venv）"),
    _Tool(name="z3", tier="A", kind="pyimport", module="z3",
          refs="ghidra-static（ctf-patterns/anti-analysis）",
          hint="pip install z3-solver（进 re-tools-venv）"),
    _Tool(name="rust-demangler", tier="A", kind="pyimport", module="rust_demangler",
          refs="re-triage（rustfilt 的 pip 替代：无 cargo，纯 wheel 支持 _ZN legacy mangling）",
          hint="pip install rust-demangler（进 re-tools-venv）"),
    _Tool(name="upx", tier="A", kind="path",
          path=str(_TOOLS_DIR / "upx" / "upx.exe"), refs="re-triage/re-unpack",
          hint="github.com/upx/upx release win64 zip 解压到 tools/upx/"),
    _Tool(name="unpacker", tier="A", kind="path",
          path=str(_UNP_VENV / "unpacker.exe"), refs="re-unpack",
          hint="python3.12 -m venv unpacker-venv && pip install -e <Unpacker 克隆>"),
    _Tool(name="file", tier="A", kind="which", exe="file",
          refs="re-triage（判型第一步）",
          hint="Git Bash 自带"),
    # ── Android / Java / 字节码族（android-re 主力；多数零成本已装）──
    _Tool(name="jadx", tier="A", kind="path",
          path=str(_TOOLS_DIR / "jadx" / "bin" / "jadx.bat"), refs="android-re",
          hint="github.com/skylot/jadx release zip 解压到 tools/jadx/（消除自写 DEX 解析器的动因）"),
    _Tool(name="apkanalyzer", tier="A", kind="path",
          path=os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\cmdline-tools\latest\bin\apkanalyzer.bat"),
          refs="android-re（官方 smali 反汇编，双源验证的第二来源）",
          hint="Android SDK cmdline-tools 自带"),
    _Tool(name="adb", tier="A", kind="path",
          path=os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe"),
          refs="android-re（安装/驱动/uiautomator/screencap）",
          hint="Android SDK platform-tools 自带"),
    _Tool(name="javac", tier="A", kind="path",
          path=r"C:\Program Files\Common Files\Oracle\Java\javapath\javac.exe",
          refs="android-re（反编译结果编译执行 = 执行级 oracle）",
          hint="JDK 安装后 javapath 自带"),
    _Tool(name="androguard", tier="A", kind="pyimport", module="androguard",
          refs="android-re（DEX 解析 + DAD，交叉验证用）",
          hint="pip install androguard（进 re-tools-venv）"),
    _Tool(name="uncompyle6", tier="A", kind="pyimport", module="uncompyle6",
          refs="re-triage（PyInstaller pyc 反编译，CPython ≤3.8）",
          hint="pip install uncompyle6（进 re-tools-venv）"),
    _Tool(name="decompyle3", tier="A", kind="pyimport", module="decompyle3",
          refs="re-triage（PyInstaller pyc 反编译备选）",
          hint="pip install decompyle3（进 re-tools-venv）"),
    _Tool(name="capstone", tier="A", kind="pyimport", module="capstone",
          refs="ghidra-static/自写脚本（反汇编库）",
          hint="pip install capstone（进 re-tools-venv）"),
    _Tool(name="unicorn", tier="A", kind="pyimport", module="unicorn",
          refs="re-dynamic/re-unpack（CPU 仿真库）",
          hint="pip install unicorn（进 re-tools-venv）"),
    _Tool(name="lief", tier="A", kind="pyimport", module="lief",
          refs="re-triage/自写脚本（PE/ELF/DEX 解析库）",
          hint="pip install lief（进 re-tools-venv）"),
    _Tool(name="pywin32", tier="B", kind="pyimport", module="win32api",
          refs="re-dynamic（Windows GUI 消息驱动：PostMessage 开窗/SendMessage 连点）",
          hint="pip install pywin32（进 re-tools-venv）"),
    # ── Tier B: heavy pip / WSL / rootfs ──
    _Tool(name="angr", tier="B", kind="pyimport", module="angr",
          refs="ghidra-static/re-triage/vuln-audit",
          hint="pip install angr（进 re-tools-venv）"),
    _Tool(name="speakeasy", tier="B", kind="pyimport", module="speakeasy",
          refs="（仿真备选）",
          hint="pip install speakeasy-emulator setuptools<81（进 re-tools-venv；Py3.12 需 distutils shim）"),
    _Tool(name="unipacker", tier="B", kind="pyimport", module="unipacker",
          venv=str(_UNP_VENV), refs="re-unpack",
          hint='pip install "unpacker[unipacker]"（进 unpacker-venv，已钉 setuptools<81）'),
    _Tool(name="ghidriff", tier="B", kind="path",
          path=str(_RE_TOOLS / "ghidriff.exe"),
          refs="ghidra-core（references/headless.md §8）",
          hint="pip install ghidriff（进 re-tools-venv）"),
    _Tool(name="strings(wsl)", tier="B", kind="wsl",
          cmd="command -v strings", refs="re-triage（strings -el 补宽字符）",
          hint="WSL apt install binutils（Git Bash 无 binutils）"),
    _Tool(name="readelf(wsl)", tier="B", kind="wsl",
          cmd="command -v readelf", refs="re-triage/ghidra-static（ELF 分析）",
          hint="WSL apt install binutils"),
    _Tool(name="binwalk(wsl)", tier="B", kind="wsl",
          cmd="command -v binwalk", refs="re-triage（固件/嵌入式解包）",
          hint="WSL apt install binwalk"),
    _Tool(name="gdb(wsl)", tier="B", kind="wsl",
          cmd="command -v gdb", refs="ghidra-static/re-triage（动态调试）",
          hint="WSL apt install gdb"),
    _Tool(name="pwntools(wsl)", tier="B", kind="wsl",
          cmd=f"test -x {_WSL_PY_VENV}/bin/pwn && {_WSL_PY_VENV}/bin/pwn version",
          refs="ghidra-static（pwn 脚本骨架）",
          hint="WSL python3 -m venv ~/re-pwn-venv && pip install pwntools"),
    _Tool(name="ROPgadget(wsl)", tier="B", kind="wsl",
          cmd=f"test -x {_WSL_PY_VENV}/bin/ROPgadget && {_WSL_PY_VENV}/bin/ROPgadget --version",
          refs="ghidra-static（ROP 链）",
          hint="WSL re-pwn-venv pip install ROPgadget"),
    _Tool(name="ropper(wsl)", tier="B", kind="wsl",
          cmd=f"test -x {_WSL_PY_VENV}/bin/ropper && {_WSL_PY_VENV}/bin/ropper --version",
          refs="ghidra-static（ROP 链备选）",
          hint="WSL re-pwn-venv pip install ropper"),
    _Tool(name="one_gadget(wsl)", tier="B", kind="wsl",
          cmd="command -v one_gadget", refs="ghidra-static（libc 一把梭）",
          hint="WSL gem install one_gadget（需 ruby-full）"),
    _Tool(name="seccomp-tools(wsl)", tier="B", kind="wsl",
          cmd="command -v seccomp-tools", refs="ghidra-static（沙箱规则分析）",
          hint="WSL gem install seccomp-tools"),
    _Tool(name="pwndbg/gef(wsl)", tier="B", kind="wsl",
          cmd="test -f /root/.gdbinit && grep -q -e pwndbg -e gef /root/.gdbinit",
          refs="ghidra-static（gdb 增强）",
          hint="WSL: pwndbg git clone+setup.sh，或 gef 单脚本"),
    _Tool(name="qiling(wsl)", tier="B", kind="wsl",
          cmd=f"test -x {_WSL_PY_VENV}/bin/python && {_WSL_PY_VENV}/bin/python -c 'import qiling'",
          refs="ghidra-static/re-triage/re-unpack（免疫反调试仿真/VMProtect64）",
          hint="WSL re-pwn-venv pip install qiling + rootfs ~/qiling-rootfs"),
    _Tool(name="qemu(wsl)", tier="B", kind="wsl",
          cmd="command -v qemu-system-x86_64", refs="re-triage（固件/异架构）",
          hint="WSL apt install qemu-system-x86"),
    _Tool(name="pycdc(wsl)", tier="B", kind="wsl",
          cmd="command -v pycdc", refs="re-unpack（py>=3.9 的 pyc 反编译，uncompyle6/decompyle3 的唯一后继）",
          hint="WSL 源码构建：apt install cmake g++ && git clone zrax/pycdc && cmake -B build && cmake --build build，产物 cp 到 /usr/local/bin"),
    _Tool(name="emulator", tier="B", kind="path",
          path=os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\emulator\emulator.exe"),
          refs="android-re（无头真机 oracle；emulator-check accel 验 WHPX）",
          hint="Android SDK emulator 组件"),
    _Tool(name="sdkmanager+avdmanager", tier="B", kind="path",
          path=os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\cmdline-tools\latest\bin\sdkmanager.bat"),
          refs="android-re（装镜像/建 AVD；长耗时走后台）",
          hint="Android SDK cmdline-tools 自带"),
    _Tool(name="build-tools(aapt2/apksigner/dexdump)", tier="B", kind="path",
          path=os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\build-tools\37.0.0\aapt2.exe"),
          refs="android-re（资源解析/重签/dexdump 第二验证路径）",
          hint="sdkmanager --install \"build-tools;37.0.0\""),
    _Tool(name="android-system-image-33", tier="B", kind="path",
          path=os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\system-images\android-33\default\x86_64\build.prop"),
          refs="android-re（真机 oracle 前提；无它 emulator 起不来）",
          hint="sdkmanager --install \"system-images;android-33;default;x86_64\"（~1GB，后台下载）"),
    _Tool(name="scapy", tier="B", kind="pyimport", module="scapy",
          refs="traffic-analysis（pcap 脚本化解析；本 skill 脚本零依赖，scapy 是进阶备手）",
          hint="pip install scapy（进 re-tools-venv）"),
    _Tool(name="tshark", tier="B", kind="path",
          path=str(_TOOLS_DIR / "wireshark" / "tshark.exe"),
          refs="traffic-analysis（协议分层统计/-z conv/--export-objects 文件提取）",
          hint="Wireshark 4.6.8 安装包 7z 解包到 tools/wireshark/（免安装免管理员；实时抓包依赖 npcap，本机已装）"),
    _Tool(name="editcap", tier="B", kind="path",
          path=str(_TOOLS_DIR / "wireshark" / "editcap.exe"),
          refs="traffic-analysis（pcapng→pcap 转换，pcap_triage.py 拒收 pcapng 时的前置步骤）",
          hint="随 tools/wireshark/ 解包自带"),
    _Tool(name="aircrack-ng(wsl)", tier="B", kind="wsl",
          cmd="command -v aircrack-ng", refs="traffic-analysis（WPA 握手破解/airdecap 二次分析）",
          hint="WSL apt install aircrack-ng"),
    _Tool(name="hashcat(wsl)", tier="B", kind="wsl",
          cmd="command -v hashcat", refs="traffic-analysis（NTLMv2 -m 5600 / WPA -m 22000）",
          hint="WSL apt install hashcat；GPU 场景用 Windows 版官网 zip"),
    # ── Tier C: GUI / plugins / manual ──
    _Tool(name="apktool", tier="C", kind="which", exe="apktool",
          refs="android-re（资源/Manifest 完整还原+回编译）",
          hint="scoop install apktool 或官方 wrapper jar 放 tools/apktool/"),
    _Tool(name="baksmali", tier="C", kind="which", exe="baksmali",
          refs="android-re（官方风格 smali 反汇编/回汇编，改 dex 用）",
          hint="github.com/baksmali/smali release jar + wrapper 脚本"),
    _Tool(name="frida-server-android", tier="C", kind="which", exe="frida-server-android-NOT-INSTALLED",
          refs="android-re（模拟器内 Java 层 hook）",
          hint="frida release android-x86_64 版，版本必须与 host frida 严格一致；push 进模拟器 /data/local/tmp"),
    _Tool(name="dnSpyEx", tier="C", kind="path",
          path=str(_TOOLS_DIR / "dnSpyEx" / "dnSpy.exe"), refs="re-triage（.NET 样本）",
          hint="github.com/dnSpyEx/dnSpy release win64 zip 解压（GUI）"),
    _Tool(name="de4dot", tier="C", kind="path",
          path=str(_TOOLS_DIR / "de4dot" / "de4dot.exe"), refs="re-triage（.NET 混淆）",
          hint="github.com/ViRb3/de4dot-cex release（CLI）"),
    _Tool(name="DIE", tier="C", kind="path",
          path=str(_TOOLS_DIR / "die" / "die" / "diec.exe"),
          refs="re-triage（查壳 GUI/CLI）",
          hint="github.com/horsicq/DIE-engine win64 portable zip；diec 是其 CLI"),
    _Tool(name="x64dbg", tier="C", kind="path",
          path=str(_TOOLS_DIR / "x64dbg" / "release" / "x64" / "x64dbg.exe"),
          refs="ghidra-static（Windows GUI crackme 动态）",
          hint="github.com/x64dbg/x64dbg snapshot zip 解压（GUI 调试器）"),
    _Tool(name="GOOMBA", tier="C", kind="which", exe="GOOMBA-NOT-INSTALLED",
          refs="re-triage（references/anti-analysis.md MBA 化简）",
          hint="不装：gooMBA 实为 Hex-Rays IDA 插件（HexRaysSA/goomba），本机无 IDA 许可；MBA 化简走 manual/angr（SiMBA 的 PyPI 包是占位包）"),
    _Tool(name="golang-loader", tier="C", kind="which", exe="golang-loader-NOT-INSTALLED",
          refs="re-triage（Go 字符串恢复）",
          hint="不装：上游仅 Jython 时代脚本源码无 release；GoReSym（Tier A）已覆盖主场景"),
]


# ── Linux/WSL registry ────────────────────────────────────────────────────────
# Same truth-source role as TOOL_REGISTRY, selected when running on Linux.
# Windows-only GUI/Android-SDK entries are omitted; "wsl" kind probes run
# natively (see _probe), so their cmd bodies are shared verbatim.
TOOL_REGISTRY_LINUX = [
    # ── Tier A ──
    _Tool(name="wine", tier="A", kind="which", exe="wine",
          refs="re-dynamic（WSL 运行 PE 原程序 oracle）", hint="apt install wine"),
    _Tool(name="Xvfb", tier="A", kind="which", exe="Xvfb",
          refs="re-dynamic（WSL GUI oracle）", hint="apt install xvfb"),
    _Tool(name="pydisasm", tier="A", kind="which", exe="pydisasm",
          refs="re-triage（pyc 反编译异常时看真实字节码）",
          hint="pip install xdis（进 re-tools-venv，或确认 /usr/local/bin/pydisasm）"),
    _Tool(name="file", tier="A", kind="which", exe="file",
          refs="re-triage（判型第一步）", hint="apt install file"),
    _Tool(name="checksec", tier="A", kind="path",
          path=str(_RE_TOOLS / "checksec"), refs="re-triage",
          hint="pip install checksec.py（进 re-tools-venv）"),
    _Tool(name="goresym", tier="A", kind="path",
          path=str(_TOOLS_DIR / "goresym" / "goresym"), refs="re-triage",
          hint="github.com/mandiant/GoReSym release linux amd64 解压到 ~/tools/goresym/"),
    _Tool(name="pyinstxtractor", tier="A", kind="path",
          path=str(_TOOLS_DIR / "pyinstxtractor" / "pyinstxtractor.py"), refs="re-triage",
          hint="github.com/extremecoders-re/pyinstxtractor 单文件拷到 ~/tools/pyinstxtractor/"),
    _Tool(name="frida", tier="A", kind="path",
          path=str(_RE_TOOLS / "frida"),
          refs="ghidra-core/ghidra-static/vuln-audit/re-unpack",
          hint="pip install frida-tools（进 re-tools-venv）"),
    _Tool(name="z3", tier="A", kind="pyimport", module="z3",
          refs="ghidra-static（ctf-patterns/anti-analysis）",
          hint="pip install z3-solver（进 re-tools-venv）"),
    _Tool(name="rust-demangler", tier="A", kind="pyimport", module="rust_demangler",
          refs="re-triage", hint="pip install rust-demangler（进 re-tools-venv）"),
    _Tool(name="upx", tier="A", kind="which", exe="upx", refs="re-triage/re-unpack",
          hint="apt install upx-ucl"),
    _Tool(name="unpacker", tier="A", kind="path",
          path=str(_UNP_VENV / "unpacker"), refs="re-unpack",
          hint="python3 -m venv ~/unpacker-venv && pip install -e <Unpacker 克隆>"),
    _Tool(name="jadx", tier="A", kind="path",
          path=str(_TOOLS_DIR / "jadx" / "bin" / "jadx"), refs="android-re",
          hint="github.com/skylot/jadx release zip 解压到 ~/tools/jadx/"),
    _Tool(name="adb", tier="A", kind="which", exe="adb",
          refs="android-re（安装/驱动）", hint="apt install adb"),
    _Tool(name="javac", tier="A", kind="which", exe="javac",
          refs="android-re（反编译结果编译执行 = 执行级 oracle）",
          hint="apt install openjdk-21-jdk-headless"),
    _Tool(name="androguard", tier="A", kind="pyimport", module="androguard",
          refs="android-re（DEX 解析 + DAD，交叉验证用）",
          hint="pip install androguard（进 re-tools-venv）"),
    _Tool(name="uncompyle6", tier="A", kind="pyimport", module="uncompyle6",
          refs="re-triage（PyInstaller pyc 反编译，CPython ≤3.8）",
          hint="pip install uncompyle6（进 re-tools-venv）"),
    _Tool(name="decompyle3", tier="A", kind="pyimport", module="decompyle3",
          refs="re-triage（PyInstaller pyc 反编译备选）",
          hint="pip install decompyle3（进 re-tools-venv）"),
    _Tool(name="capstone", tier="A", kind="pyimport", module="capstone",
          refs="ghidra-static/自写脚本（反汇编库）",
          hint="pip install capstone（进 re-tools-venv）"),
    _Tool(name="unicorn", tier="A", kind="pyimport", module="unicorn",
          refs="re-dynamic/re-unpack（CPU 仿真库）",
          hint="pip install unicorn（进 re-tools-venv）"),
    _Tool(name="lief", tier="A", kind="pyimport", module="lief",
          refs="re-triage/自写脚本（PE/ELF/DEX 解析库）",
          hint="pip install lief（进 re-tools-venv）"),
    # ── Tier B ──
    _Tool(name="angr", tier="B", kind="pyimport", module="angr",
          refs="ghidra-static/re-triage/vuln-audit",
          hint="pip install angr（进 re-tools-venv）"),
    _Tool(name="speakeasy", tier="B", kind="pyimport", module="speakeasy",
          refs="（仿真备选）",
          hint="pip install speakeasy-emulator setuptools<81（进 re-tools-venv）"),
    _Tool(name="unipacker", tier="B", kind="pyimport", module="unipacker",
          venv=str(_UNP_VENV), refs="re-unpack",
          hint='pip install "unpacker[unipacker]"（进 unpacker-venv）'),
    _Tool(name="ghidriff", tier="B", kind="path",
          path=str(_RE_TOOLS / "ghidriff"),
          refs="ghidra-core（references/headless.md §8）",
          hint="pip install ghidriff（进 re-tools-venv）"),
    _Tool(name="strings", tier="B", kind="which", exe="strings",
          refs="re-triage（strings -el 补宽字符）", hint="apt install binutils"),
    _Tool(name="readelf", tier="B", kind="which", exe="readelf",
          refs="re-triage/ghidra-static（ELF 分析）", hint="apt install binutils"),
    _Tool(name="gdb", tier="B", kind="which", exe="gdb",
          refs="ghidra-static/re-triage（动态调试）", hint="apt install gdb"),
    _Tool(name="pwntools", tier="B", kind="wsl",
          cmd=f"test -x {_WSL_PY_VENV}/bin/pwn && {_WSL_PY_VENV}/bin/pwn version",
          refs="ghidra-static（pwn 脚本骨架）",
          hint="python3 -m venv ~/re-pwn-venv && pip install pwntools"),
    _Tool(name="ROPgadget", tier="B", kind="wsl",
          cmd=f"test -x {_WSL_PY_VENV}/bin/ROPgadget && {_WSL_PY_VENV}/bin/ROPgadget --version",
          refs="ghidra-static（ROP 链）", hint="~/re-pwn-venv pip install ROPgadget"),
    _Tool(name="ropper", tier="B", kind="wsl",
          cmd=f"test -x {_WSL_PY_VENV}/bin/ropper && {_WSL_PY_VENV}/bin/ropper --version",
          refs="ghidra-static（ROP 链备选）", hint="~/re-pwn-venv pip install ropper"),
    _Tool(name="one_gadget", tier="B", kind="wsl",
          cmd="command -v one_gadget", refs="ghidra-static（libc 一把梭）",
          hint="gem install one_gadget（需 ruby-full）"),
    _Tool(name="seccomp-tools", tier="B", kind="wsl",
          cmd="command -v seccomp-tools", refs="ghidra-static（沙箱规则分析）",
          hint="gem install seccomp-tools"),
    _Tool(name="pwndbg/gef", tier="B", kind="wsl",
          cmd="test -f /root/.gdbinit && grep -q -e pwndbg -e gef /root/.gdbinit",
          refs="ghidra-static（gdb 增强）",
          hint="pwndbg git clone+setup.sh，或 gef 单脚本"),
    _Tool(name="qiling", tier="B", kind="wsl",
          cmd=f"test -x {_WSL_PY_VENV}/bin/python && {_WSL_PY_VENV}/bin/python -c 'import qiling'",
          refs="ghidra-static/re-triage/re-unpack（免疫反调试仿真）",
          hint="~/re-pwn-venv pip install qiling + rootfs ~/qiling-rootfs"),
    _Tool(name="qemu", tier="B", kind="which", exe="qemu-system-x86_64",
          refs="re-triage（固件/异架构）", hint="apt install qemu-system-x86"),
    _Tool(name="qemu-user", tier="B", kind="which", exe="qemu-riscv64",
          refs="re-dynamic（foreign-arch ELF 直接运行：qemu-<arch>；含 qemu-aarch64）",
          hint="apt install qemu-user"),
    _Tool(name="gdb-multiarch", tier="B", kind="which", exe="gdb-multiarch",
          refs="re-dynamic（跨架构调试：qemu -g 1234 + target remote）",
          hint="apt install gdb-multiarch"),
    _Tool(name="wabt", tier="B", kind="which", exe="wasm2wat",
          refs="re-triage（WASM 路由：wasm-decompile/wasm2wat/wasm-objdump）",
          hint="apt install wabt"),
    _Tool(name="wasmtime", tier="B", kind="which", exe="wasmtime",
          refs="re-dynamic（WASM 跑一下看看；pip 包之外的独立 CLI）",
          hint="wasmtime.dev/install.sh，产物 symlink 到 /usr/local/bin"),
    _Tool(name="binwalk", tier="B", kind="which", exe="binwalk",
          refs="re-triage（固件/嵌入式解包、嵌套文件系统识别）",
          hint="apt install binwalk（或 pip install binwalk 进 re-tools-venv）"),
    _Tool(name="pycdc", tier="B", kind="which", exe="pycdc",
          refs="re-unpack（py>=3.9 的 pyc 反编译）",
          hint="源码构建 zrax/pycdc（cmake+g++），产物 cp 到 /usr/local/bin"),
    _Tool(name="scapy", tier="B", kind="pyimport", module="scapy",
          refs="traffic-analysis（pcap 脚本化解析）",
          hint="pip install scapy（进 re-tools-venv）"),
    _Tool(name="tshark", tier="B", kind="which", exe="tshark",
          refs="traffic-analysis（协议分层统计/-z conv/--export-objects）",
          hint="apt install tshark"),
    _Tool(name="editcap", tier="B", kind="which", exe="editcap",
          refs="traffic-analysis（pcapng→pcap 转换）",
          hint="apt install wireshark-common"),
    _Tool(name="aircrack-ng", tier="B", kind="which", exe="aircrack-ng",
          refs="traffic-analysis（WPA 握手破解/airdecap 二次分析）",
          hint="apt install aircrack-ng"),
    _Tool(name="hashcat", tier="B", kind="which", exe="hashcat",
          refs="traffic-analysis（NTLMv2 -m 5600 / WPA -m 22000）",
          hint="apt install hashcat"),
    # ── Tier C ──
    _Tool(name="apktool", tier="C", kind="which", exe="apktool",
          refs="android-re（资源/Manifest 完整还原+回编译）",
          hint="apt install apktool 或官方 wrapper jar"),
    _Tool(name="baksmali", tier="C", kind="which", exe="baksmali",
          refs="android-re（smali 反汇编/回汇编，改 dex 用）",
          hint="github.com/baksmali/smali release jar + wrapper 脚本"),
    _Tool(name="frida-server-android", tier="C", kind="which", exe="frida-server-android-NOT-INSTALLED",
          refs="android-re（模拟器/真机内 Java 层 hook）",
          hint="frida release android-x86_64 版，版本必须与 host frida 严格一致"),
]


def main() -> int:
    out_path = None
    if len(sys.argv) > 1 and sys.argv[1].startswith("@"):
        out_path = sys.argv[1][1:]

    results = []

    # 1. Ghidra install + launchers
    try:
        install = driver._configure_environment()
        headless = install / "support" / ("analyzeHeadless.bat" if _IS_NT else "analyzeHeadless")
        gui = install / ("ghidraRun.bat" if _IS_NT else "ghidraRun")
        ok = headless.is_file() and gui.is_file()
        results.append(check("ghidra_install", ok,
                             f"install={install} headless={headless.is_file()} "
                             f"gui={gui.is_file()}"))
    except SystemExit as exc:
        results.append(check("ghidra_install", False, str(exc)))
        install = None

    # 2. Java
    java_home = None
    try:
        install = install or driver._configure_environment()
        java_home = os_environ_java()
        java_exe = Path(java_home) / "bin" / ("java.exe" if _IS_NT else "java") if java_home else None
        if java_exe and java_exe.is_file():
            proc = subprocess.run([str(java_exe), "-version"],
                                  capture_output=True, text=True, timeout=30)
            ver_line = (proc.stderr or proc.stdout or "").splitlines()[0]
            results.append(check("java", proc.returncode == 0,
                                 f"JAVA_HOME={java_home} version={ver_line}"))
        else:
            results.append(check("java", False,
                                 f"java.exe not found under JAVA_HOME={java_home}"))
    except Exception as exc:
        results.append(check("java", False, str(exc)))

    # 3. pyghidra venv
    venv_python = (Path.home() / "Desktop" / "src" / "ghidra-bridge" /
                   "pyghidra-venv" / "Scripts" / "python.exe") if _IS_NT else \
        (Path.home() / "pyghidra-venv" / "bin" / "python")
    if not venv_python.is_file():
        results.append(check("pyghidra_venv", False,
                             f"venv python not found at {venv_python}"))
    else:
        try:
            proc = subprocess.run(
                [str(venv_python), "-c",
                 "import importlib.metadata, pyghidra; "
                 "print(importlib.metadata.version('pyghidra'))"],
                capture_output=True, text=True, timeout=60)
            ver = (proc.stdout or "").strip()
            ok = proc.returncode == 0 and ver
            results.append(check("pyghidra_venv", bool(ok),
                                 f"python={venv_python} pyghidra={ver or proc.stderr.strip()[:200]}"))
        except Exception as exc:
            results.append(check("pyghidra_venv", False, str(exc)))

    # 4. Workspace writable (+ junction resolves)
    try:
        ws = driver.workspace()
        probe = ws / "out" / ".doctor-probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        link = driver.project_root()
        results.append(check("workspace", True,
                             f"ws={ws} projects(via junction)={link}"))
    except Exception as exc:
        results.append(check("workspace", False, str(exc)))

    # 5. Existing projects
    try:
        projects_dir = driver.project_root()
        projects = sorted(p.stem for p in projects_dir.glob("*.gpr"))
        results.append(check("projects", True,
                             f"count={len(projects)} names={projects}"))
    except Exception as exc:
        results.append(check("projects", False, str(exc)))

    # 6. ghidra-rpc venv (engine environment)
    rpc_venv_python = (Path.home() / "Desktop" / "src" / "ghidra-bridge" /
                       "ghidra-rpc-venv" / "Scripts" / "python.exe") if _IS_NT else \
        (Path.home() / "ghidra-rpc-venv" / "bin" / "python")
    if not rpc_venv_python.is_file():
        results.append(check("rpc_venv", False,
                             f"venv python not found at {rpc_venv_python}"))
    else:
        results.append(check("rpc_venv", True, f"python={rpc_venv_python}"))

    # 7. ghidra-rpc importable + version (editable install of engine/)
    if rpc_venv_python.is_file():
        try:
            proc = subprocess.run(
                [str(rpc_venv_python), "-c",
                 "import importlib.metadata, ghidra_rpc; "
                 "print(importlib.metadata.version('ghidra-rpc')); "
                 "print(ghidra_rpc.__file__)"],
                capture_output=True, text=True, timeout=60)
            lines = (proc.stdout or "").strip().splitlines()
            ver = lines[0] if lines else ""
            loc = lines[1] if len(lines) > 1 else ""
            ok = proc.returncode == 0 and ver and "engine" in loc.replace("/", "\\")
            results.append(check("rpc_package", bool(ok),
                                 f"version={ver} location={loc}"
                                 + ("" if ok else " (expected editable install from skill engine/)")))
        except Exception as exc:
            results.append(check("rpc_package", False, str(exc)))

    # 8. daemon start/stop smoke (slow: one JVM cold start, ~30-60 s)
    if "--quick" not in sys.argv:
        try:
            import rpc_driver  # sibling script
            env = rpc_driver.configure_env()
            probe_gpr = rpc_driver.WS_LINK / "projects-rpc" / "doctor_probe.gpr"
            start = rpc_driver.run_rpc(env, probe_gpr,
                                       ["start", "--headless", "--detach"], timeout=300)
            if not start.get("ok"):
                results.append(check("rpc_daemon", False,
                                     f"start failed: {str(start)[:200]}"))
            else:
                status = rpc_driver.run_rpc(env, probe_gpr, ["status"], timeout=60)
                running = bool((status.get("result") or {}).get("running"))
                stop = rpc_driver.run_rpc(env, probe_gpr, ["stop"], timeout=120)
                stopped = bool((stop.get("result") or {}).get("status") == "stopped") \
                    or stop.get("ok")
                ok = running and stopped
                results.append(check("rpc_daemon", ok,
                                     f"start=ok running={running} stop_ok={stopped}"))
                # probe project is empty; remove it
                import shutil
                shutil.rmtree(probe_gpr.parent / "doctor_probe.rep",
                              ignore_errors=True)
                (probe_gpr.parent / "doctor_probe.gpr").unlink(missing_ok=True)
        except Exception as exc:
            results.append(check("rpc_daemon", False, str(exc)))

    # ── Toolchain layer (external tools referenced by the skill family) ──
    # The single source of truth for tool availability. Tier A missing = warn
    # (never fails the run; only Ghidra-core failures do). Tier B/C missing =
    # informational "not installed (按需)".
    toolchain = [t.check() for t in (TOOL_REGISTRY_LINUX if _IS_LINUX else TOOL_REGISTRY)]
    tier_a = [t for t in toolchain if t["tier"] == "A"]
    tier_b = [t for t in toolchain if t["tier"] == "B"]
    tier_c = [t for t in toolchain if t["tier"] == "C"]

    def _avail(ts):
        return f"{sum(1 for t in ts if t['ok'])}/{len(ts)}"

    all_ok = all(r["ok"] for r in results)
    resources = {}
    if _IS_LINUX:
        try:
            for line in Path("/proc/meminfo").read_text().splitlines():
                if line.startswith("MemAvailable:"):
                    resources["mem_available_mib"] = int(line.split()[1]) // 1024
                    break
            processes = subprocess.run(["ps", "-eo", "args="], capture_output=True,
                                       text=True, timeout=5, check=True).stdout.splitlines()
            resources["ghidra_rpc_daemons"] = sum(
                "ghidra_rpc.daemon" in line for line in processes)
            if resources.get("ghidra_rpc_daemons", 0) > 2:
                resources["warning"] = "Ghidra RPC daemon 超过 2 个；批量题先复用或清理闲置实例"
            elif resources.get("mem_available_mib", 0) < 4096:
                resources["warning"] = "可用内存低于 4 GiB；暂停并行导入/分析"
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            resources["warning"] = f"资源读数不可用: {exc}"
    summary = {
        "status": "ok" if all_ok else "fail",
        "checks": results,
        "toolchain": toolchain,
        "resources": resources,
        "toolchain_summary": {
            "tier_A": _avail(tier_a),
            "tier_B": _avail(tier_b),
            "tier_C": _avail(tier_c),
            "tier_A_missing": [t["name"] for t in tier_a if not t["ok"]],
            "note": "tier A 缺失=warn（按 hint 补装）；tier B/C 缺失=按需，不算问题；"
                    "exit code 只反映 Ghidra 核心环境",
        },
    }
    text = json.dumps(summary, ensure_ascii=False, indent=2)
    print(text)
    # human-readable one-liner
    print(f"toolchain: tier A {_avail(tier_a)}"
          + (f" (missing: {', '.join(summary['toolchain_summary']['tier_A_missing'])})"
             if summary["toolchain_summary"]["tier_A_missing"] else "")
          + f" | tier B {_avail(tier_b)} | tier C {_avail(tier_c)}",
          file=sys.stderr)
    if out_path:
        Path(out_path).write_text(text, encoding="utf-8")
    _print_cheatsheet()
    return 0 if all_ok else 1


def _print_cheatsheet() -> None:
    """本机化命令速查（stderr）：SKILL.md 的路径约定是通式，这里给出本机
    实际展开值——agent 应照抄这里的拼写，不要从通式手工换算。"""
    import shutil
    py = "python3" if (not _IS_NT and shutil.which("python3")) else "python"
    sk = Path(__file__).resolve().parent
    try:
        ws = driver.workspace()
    except Exception:
        ws = Path.home() / ".dsh" / "ghidra-workspace"
    venv_py = _RE_TOOLS / _VENV_PY
    lines = [
        "",
        "──── 本机命令速查（可粘贴，值为本机实测展开）────",
        f"PY={py}   SK={sk}   WS={ws}",
        f"VENV_PY={venv_py}" + ("" if venv_py.is_file() else "  (不存在，先建 venv)"),
        f"  分诊:   {py} \"{sk / 'rpc_driver.py'}\" ensure <sample> && "
        f"{py} \"{sk / 'rpc_driver.py'}\" \"@{ws / 'out' / 'triage.json'}\" triage <sample>",
        f"  台账:   {py} \"{sk / 'ledger.py'}\" status <sample>",
        f"  体检:   {py} \"{sk / 'doctor.py'}\" --quick",
    ]
    print("\n".join(lines), file=sys.stderr)


def os_environ_java():
    import os
    return os.environ.get("JAVA_HOME") or driver.DEFAULT_JAVA_HOME


if __name__ == "__main__":
    raise SystemExit(main())
