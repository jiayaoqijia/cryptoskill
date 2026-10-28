#!/usr/bin/env python
"""_android_tools.py - android-re scripts 共享的 Android SDK 工具探测与调用层.

共享调用层（不是入口脚本）。使用已验证的解码实现，不用临时 parser
替代未经验证的 DEX/AXML 语义。工具缺失时明确降级（exit 3）。

环境变量覆盖（优先级高于默认路径）：
  ANDROID_SDK_ROOT / ANDROID_HOME  SDK 根目录
  APKANALYZER / AAPT2 / APKSIGNER / ADB / EMULATOR / AVDMANAGER  单工具全路径
  AGPY                             androguard venv 的 python.exe
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys

for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

EXIT_USAGE = 1
EXIT_SELFTEST = 2
EXIT_NO_TOOL = 3
EXIT_RUNTIME = 4


def find_sdk() -> str | None:
    for env in ("ANDROID_SDK_ROOT", "ANDROID_HOME"):
        p = os.environ.get(env)
        if p and os.path.isdir(p):
            return p
    local = os.environ.get("LOCALAPPDATA")
    if local:
        cand = os.path.join(local, "Android", "Sdk")
        if os.path.isdir(cand):
            return cand
    if os.name != 'nt':
        for cand in (os.path.expanduser('~/Android/Sdk'),os.path.expanduser('~/Android/sdk'),'/opt/android-sdk'):
            if os.path.isdir(cand):return cand
    return None


def native_name(name: str) -> str:
    return re.sub(r'\.(bat|exe)$','',name,flags=re.I) if os.name != 'nt' else name


def _build_tools_dir(tool_name: str) -> str | None:
    """build-tools 下按版本号从高到低找第一个含目标工具的目录。"""
    sdk = find_sdk()
    if not sdk:
        return None
    bt_root = os.path.join(sdk, "build-tools")
    if not os.path.isdir(bt_root):
        return None
    versions = sorted(
        (d for d in os.listdir(bt_root) if re.fullmatch(r"[0-9.]+", d)),
        key=lambda s: [int(x) for x in s.split(".")],
        reverse=True,
    )
    for ver in versions:
        cand = os.path.join(bt_root, ver, native_name(tool_name))
        if os.path.isfile(cand):
            return cand
    return None


def find_tool(env_var: str, sdk_rel: str | None, build_tool: str | None,
              path_names: tuple[str, ...] = ()) -> str | None:
    p = os.environ.get(env_var)
    if p and os.path.isfile(p):
        return p
    sdk = find_sdk()
    if sdk and sdk_rel:
        parent,leaf=os.path.split(sdk_rel)
        cand = os.path.join(sdk,parent,native_name(leaf))
        if os.path.isfile(cand):
            return cand
        if parent.replace('\\','/').startswith('cmdline-tools/latest/'):
            root=os.path.join(sdk,'cmdline-tools')
            if os.path.isdir(root):
                for version in sorted((v for v in os.listdir(root) if re.fullmatch(r'\d+(?:\.\d+)*',v)),key=lambda v:tuple(map(int,v.split('.'))),reverse=True):
                    cand=os.path.join(root,version,'bin',native_name(leaf))
                    if os.path.isfile(cand):return cand
    if build_tool:
        cand = _build_tools_dir(build_tool)
        if cand:
            return cand
    for name in path_names:
        if os.name != 'nt' and name.lower().endswith(('.exe','.bat')):continue
        w = shutil.which(name)
        if w:
            return w
    return None


def apkanalyzer() -> str | None:
    return find_tool("APKANALYZER", os.path.join("cmdline-tools", "latest", "bin", "apkanalyzer.bat"),
                     None, ("apkanalyzer", "apkanalyzer.bat"))


def aapt2() -> str | None:
    return find_tool("AAPT2", None, "aapt2.exe", ("aapt2", "aapt2.exe"))


def apksigner() -> str | None:
    return find_tool("APKSIGNER", None, "apksigner.bat", ("apksigner", "apksigner.bat"))


def d8() -> str | None:
    return find_tool("D8", None, "d8.bat", ("d8", "d8.bat"))


def adb() -> str | None:
    return find_tool("ADB", os.path.join("platform-tools", "adb.exe"), None, ("adb", "adb.exe"))


def emulator() -> str | None:
    return find_tool("EMULATOR", os.path.join("emulator", "emulator.exe"), None, ("emulator", "emulator.exe"))


def emulator_check() -> str | None:
    sdk = find_sdk()
    if sdk:
        cand = os.path.join(sdk, "emulator", native_name("emulator-check.exe"))
        if os.path.isfile(cand):
            return cand
    return None


def avdmanager() -> str | None:
    return find_tool("AVDMANAGER", os.path.join("cmdline-tools", "latest", "bin", "avdmanager.bat"),
                     None, ("avdmanager", "avdmanager.bat"))


def agpy() -> str | None:
    """androguard venv 的解释器；返回前实测 import 可用。"""
    cands = []
    p = os.environ.get("AGPY")
    if p:
        cands.append(p)
    cands.append(os.path.expanduser(os.path.join("~", "Desktop", "src", "re-tools-venv",
                                                 "Scripts", "python.exe")))
    cands.append(os.path.expanduser(os.path.join("~", "re-tools-venv", "bin", "python")))
    cands.append(sys.executable)
    for c in cands:
        if not c or not os.path.isfile(c):
            continue
        try:r = subprocess.run([c, "-c", "import androguard"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
        except (OSError,subprocess.TimeoutExpired):continue
        if r.returncode == 0:
            return c
    return None


def jadx() -> str | None:
    p=os.environ.get('JADX') or shutil.which('jadx')
    if p and os.path.isfile(p):return p
    p=os.path.expanduser(os.path.join('~','tools','jadx','bin','jadx.bat' if os.name=='nt' else 'jadx'))
    return p if os.path.isfile(p) else None


def dexdump() -> str | None:
    return find_tool('DEXDUMP',None,'dexdump.exe',('dexdump','dexdump.exe'))


def run_tool(argv: list[str], timeout: int = 300, cwd: str | None = None) -> subprocess.CompletedProcess:
    """统一调工具：.bat 走 cmd /c；UTF-8 捕获输出；超时不抛栈。"""
    if argv[0].lower().endswith(".bat"):
        argv = [os.environ.get("COMSPEC", "cmd.exe"), "/c"] + argv
    try:
        return subprocess.run(argv, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout, cwd=cwd)
    except subprocess.TimeoutExpired as e:
        return subprocess.CompletedProcess(argv, 124,
                                           e.stdout if isinstance(e.stdout, str) else "",
                                           f"[超时 {timeout}s] {argv[0]}")
    except OSError as e:
        return subprocess.CompletedProcess(argv, 127, "", f"[调用失败] {e}")


def missing(tool: str, hint: str) -> int:
    print(f"[工具缺失] {tool} 在当前发现范围不可用，此后端未运行；可选择其他已验证工具。")
    print(f"  装法：{hint}")
    print("  或用环境变量指定全路径后重试（见 _android_tools.py 头注释）。")
    return EXIT_NO_TOOL
