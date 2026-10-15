#!/usr/bin/env python
"""pyinstaller_extract.py - PyInstaller 解包一条龙（五题复盘 B3）。

Host-side tool (Python 3.8+, stdlib only; decompilers run as subprocesses).

流水线：
  1. 分诊：文件尾扫描 PyInstaller CArchive cookie magic，解析 cookie 得到
     PyInstaller 版本（2.0 / 2.1+）与打包用 Python 版本，解析 TOC 找入口脚本。
  2. 解包：子进程调 pyinstxtractor（~/Desktop/src/tools/pyinstxtractor/）。
  3. 反编译：读入口 pyc 的 4 字节 magic 判断 bytecode 版本，自动选调：
       py < 3.7        -> uncompyle6（re-tools-venv）
       3.7 <= py <=3.8 -> decompyle3（re-tools-venv，对 3.7/3.8 语法更准）
       py >= 3.9       -> pycdc（Windows tools/pycdc 或 WSL 源码构建，自动探测；未安装则给提示，不视为失败）
  4. 全程 UTF-8 JSON 输出。

用法：
  pyinstaller_extract.py <binary> [--check] [--out DIR] [--all] [--no-decompile]

  --check        只分诊：是否 PyInstaller、版本、入口 pyc 名，不解包
  --out DIR      解包输出目录（默认 <binary所在目录>/<binary名>_pyinst/），
                 pyinstxtractor 会在其中再建 <binary名>_extracted/
  --all          反编译全部 .pyc（默认只反编译入口 pyc）
  --no-decompile 只解包不反编译

Exit codes: 0 ok, 1 usage/io error, 2 闸门拦截（非 PyInstaller 样本拒绝跑全流程）。
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import struct
import subprocess
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    _s.reconfigure(encoding="utf-8", errors="replace")

HOME = Path(os.path.expanduser("~"))
_IS_NT = os.name == "nt"
if _IS_NT:
    PYINSTXTRACTOR = HOME / "Desktop" / "src" / "tools" / "pyinstxtractor" / "pyinstxtractor.py"
    VENV_SCRIPTS = HOME / "Desktop" / "src" / "re-tools-venv" / "Scripts"
    _EXE = ".exe"
    _PY = "python.exe"
else:  # WSL/Linux 部署
    PYINSTXTRACTOR = HOME / "tools" / "pyinstxtractor" / "pyinstxtractor.py"
    VENV_SCRIPTS = HOME / "re-tools-venv" / "bin"
    _EXE = ""
    _PY = "python"
VENV_PY = VENV_SCRIPTS / _PY
# 这两个包没有 __main__（python -m 不可行），必须走 venv 的 console script
DECOMPILERS = {
    "uncompyle6": VENV_SCRIPTS / f"uncompyle6{_EXE}",
    "decompyle3": VENV_SCRIPTS / f"decompyle3{_EXE}",
}
PYCDC_CANDIDATES = ([
    HOME / "Desktop" / "src" / "tools" / "pycdc" / "pycdc.exe",
    HOME / "Desktop" / "src" / "tools" / "pycdc.exe",
] if _IS_NT else []) + [
    shutil.which("pycdc") or "",
]

PYINST_MAGIC = b"MEI\x0c\x0b\x0a\x0b\x0e"
PYINST20_COOKIE_SIZE = 24
PYINST21_COOKIE_SIZE = 24 + 64

# pyc magic（前两字节小端 uint16，第 3-4 字节恒为 \r\n）-> bytecode 版本。
# 数值取自 CPython Lib/importlib/_bootstrap_external.py。
PYC_MAGICS = {
    62211: (2, 7),
    3150: (3, 0), 3160: (3, 1), 3180: (3, 2), 3230: (3, 3), 3310: (3, 4),
    3350: (3, 5), 3351: (3, 5), 3379: (3, 6), 3394: (3, 7), 3413: (3, 8),
    3425: (3, 9), 3439: (3, 10), 3495: (3, 11), 3531: (3, 12), 3571: (3, 13),
}


def jout(obj: dict, indent=None) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=indent))


# ---------------------------------------------------------------- triage

def _find_cookie(f, file_size: int) -> int:
    """从文件尾向前分块 rfind cookie magic，返回偏移；-1 = 未找到。"""
    search_chunk = 8192
    end_pos = file_size
    while True:
        start_pos = end_pos - search_chunk if end_pos >= search_chunk else 0
        chunk_size = end_pos - start_pos
        if chunk_size < len(PYINST_MAGIC):
            return -1
        f.seek(start_pos, os.SEEK_SET)
        offs = f.read(chunk_size).rfind(PYINST_MAGIC)
        if offs != -1:
            return start_pos + offs
        end_pos = start_pos + len(PYINST_MAGIC) - 1
        if start_pos == 0:
            return -1


def triage(binary: Path) -> dict:
    """只读分诊：magic / PyInstaller 版本 / Python 版本 / 入口脚本名。"""
    result = {
        "binary": str(binary),
        "is_pyinstaller": False,
        "pyinstaller_version": None,
        "python_version": None,
        "cookie_pos": None,
        "toc_entries": 0,
        "entry_scripts": [],
        "entry_pyc": None,
        "note": None,
    }
    file_size = binary.stat().st_size
    if file_size < len(PYINST_MAGIC) + PYINST20_COOKIE_SIZE:
        result["note"] = "file too small for a pyinstaller archive"
        return result

    with binary.open("rb") as f:
        cookie_pos = _find_cookie(f, file_size)
        if cookie_pos == -1:
            result["note"] = "missing MEI cookie magic"
            return result

        f.seek(cookie_pos + PYINST20_COOKIE_SIZE, os.SEEK_SET)
        pyinst21 = b"python" in f.read(64).lower()
        cookie_size = PYINST21_COOKIE_SIZE if pyinst21 else PYINST20_COOKIE_SIZE

        f.seek(cookie_pos, os.SEEK_SET)
        if pyinst21:
            (magic, pkg_len, toc, toc_len, pyver, pylibname) = struct.unpack(
                "!8sIIii64s", f.read(PYINST21_COOKIE_SIZE))
        else:
            (magic, pkg_len, toc, toc_len, pyver) = struct.unpack(
                "!8siiii", f.read(PYINST20_COOKIE_SIZE))

        pymaj, pymin = (pyver // 100, pyver % 100) if pyver >= 100 else (pyver // 10, pyver % 10)
        tail = file_size - cookie_pos - cookie_size
        overlay_size = pkg_len + tail
        overlay_pos = file_size - overlay_size
        toc_pos = overlay_pos + toc

        entries = []
        if 0 <= toc_pos < file_size and 0 < toc_len <= file_size:
            f.seek(toc_pos, os.SEEK_SET)
            parsed = 0
            try:
                while parsed < toc_len:
                    (entry_size,) = struct.unpack("!i", f.read(4))
                    name_len = struct.calcsize("!iIIIBc")
                    (_pos, _cs, _us, _flag, type_cmprs, name) = struct.unpack(
                        "!IIIBc{}s".format(entry_size - name_len),
                        f.read(entry_size - 4))
                    name = name.decode("utf-8", errors="replace").rstrip("\0")
                    entries.append((type_cmprs, name))
                    parsed += entry_size
            except (struct.error, ValueError):
                result["note"] = "TOC truncated/unparseable; partial entry list returned"

    scripts = [name for t, name in entries if t == b"s"]
    result.update({
        "is_pyinstaller": True,
        "pyinstaller_version": "2.1+" if pyinst21 else "2.0",
        "python_version": f"{pymaj}.{pymin}",
        "cookie_pos": cookie_pos,
        "toc_entries": len(entries),
        "entry_scripts": scripts,
        "entry_pyc": (scripts[0] + ".pyc") if scripts else None,
    })
    return result


# ------------------------------------------------------------- decompile

def pyc_version(pyc: Path):
    """读 pyc 头 4 字节 -> (maj, min)；未知 magic 返回 None。"""
    with pyc.open("rb") as f:
        head = f.read(4)
    if len(head) < 4 or head[2:4] != b"\r\n":
        return None
    magic = struct.unpack("<H", head[:2])[0]
    if magic in PYC_MAGICS:
        return PYC_MAGICS[magic]
    # 版本内小版本号会递增 magic（如 3.12.x 3531..3536），就近归入同一大版本
    known = sorted(PYC_MAGICS)
    below = [m for m in known if m <= magic]
    if below:
        return PYC_MAGICS[below[-1]]
    return None


def _win_to_wsl(p: str) -> str:
    """C:\\Users\\x -> /mnt/c/Users/x（供 wsl pycdc 读 Windows 侧文件）。"""
    p = str(Path(p).resolve())
    if len(p) >= 2 and p[1] == ":":
        return "/mnt/" + p[0].lower() + p[2:].replace("\\", "/")
    return p.replace("\\", "/")


def find_pycdc() -> tuple[str, str] | None:
    """返回 (mode, ref)：mode='win' ref=exe 路径；mode='wsl' 走 WSL 的 pycdc。
    Linux 下 pycdc 原生可用，只走直接调用（等价 'win' 分支）。"""
    for c in PYCDC_CANDIDATES:
        if c and Path(c).is_file():
            return ("win", str(c))
    if not _IS_NT and shutil.which("pycdc"):
        return ("win", shutil.which("pycdc"))
    if not _IS_NT:
        return None
    r = run_cmd(["wsl", "-d", "Ubuntu", "-u", "root", "--",
                 "bash", "-lc", "command -v pycdc"], timeout=30)
    if r["returncode"] == 0 and r["stdout"]:
        return ("wsl", r["stdout"].splitlines()[-1].strip())
    return None


def choose_decompiler(ver) -> dict:
    """按 bytecode 版本选反编译器；返回 {tool, reason}，tool=None 表示无可用。"""
    if ver is None:
        return {"tool": None,
                "reason": "pyc magic 无法识别，放弃自动选调；请人工确认 bytecode 版本"}
    if ver >= (3, 9):
        return {"tool": "pycdc",
                "reason": (f"py {ver[0]}.{ver[1]} >= 3.9：uncompyle6/decompyle3 "
                           "不支持，需 pycdc（Decompyle++）")}
    if ver >= (3, 7):
        return {"tool": "decompyle3",
                "reason": f"py {ver[0]}.{ver[1]}：decompyle3 对 3.7/3.8 语法还原更准"}
    return {"tool": "uncompyle6",
            "reason": f"py {ver[0]}.{ver[1]} <= 3.6（含 2.x）：走 uncompyle6"}


def run_cmd(cmd: list[str], timeout: int = 300, cwd: Path | None = None) -> dict:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout,
                           cwd=str(cwd) if cwd else None)
        return {"returncode": p.returncode, "stdout": p.stdout.strip(),
                "stderr": p.stderr.strip()}
    except subprocess.TimeoutExpired:
        return {"returncode": -1, "stdout": "", "stderr": f"timeout {timeout}s"}
    except OSError as e:
        return {"returncode": -1, "stdout": "", "stderr": str(e)}


def decompile_one(pyc: Path, decom_dir: Path) -> dict:
    """反编译单个 pyc，产物固定为 decom_dir/<stem>.py，回报实际路径。"""
    ver = pyc_version(pyc)
    choice = choose_decompiler(ver)
    out_py = decom_dir / (pyc.stem + ".py")
    rec = {"pyc": str(pyc), "bytecode_version":
           f"{ver[0]}.{ver[1]}" if ver else None,
           "decompiler": choice["tool"], "reason": choice["reason"],
           "ok": False, "output": None}

    if choice["tool"] in DECOMPILERS:
        exe = DECOMPILERS[choice["tool"]]
        if not exe.is_file():
            rec["error"] = f"decompiler missing: {exe}"
            return rec
        # 两者 -o 语义不同：decompyle3 要求已存在的目录；统一传目录，
        # 产物固定为 <dir>/<pyc stem>.py
        decom_dir.mkdir(parents=True, exist_ok=True)
        r = run_cmd([str(exe), "-o", str(decom_dir), str(pyc)])
        rec["returncode"] = r["returncode"]
        if r["stderr"]:
            rec["stderr"] = r["stderr"][-2000:]
        rec["ok"] = r["returncode"] == 0 and out_py.is_file() and out_py.stat().st_size > 0
        if rec["ok"]:
            rec["output"] = str(out_py)
    elif choice["tool"] == "pycdc":
        found = find_pycdc()
        if found:
            mode, ref = found
            if mode == "wsl":
                r = run_cmd(["wsl", "-d", "Ubuntu", "-u", "root", "--",
                             "pycdc", _win_to_wsl(str(pyc))])
                rec["decompiler"] = "pycdc(wsl)"
            else:
                r = run_cmd([ref, str(pyc)])
            if r["returncode"] == 0 and r["stdout"]:
                out_py.write_text(r["stdout"], encoding="utf-8")
                rec["ok"] = True
                rec["output"] = str(out_py)
            rec["returncode"] = r["returncode"]
            if r["stderr"]:
                rec["stderr"] = r["stderr"][-2000:]
        else:
            rec["hint"] = ("pycdc 未安装：Windows 侧放 ~/Desktop/src/tools/pycdc/pycdc.exe，"
                           "或 WSL 源码构建 Decompyle++（cmake+g++，本脚本自动探测）；"
                           "也可在线 https://pylingual.io 兜底")
    return rec


# ------------------------------------------------------------- pipeline

def cmd_check(args) -> int:
    binary = Path(args.binary)
    if not binary.is_file():
        jout({"ok": False, "error": f"binary not found: {binary}"})
        return 1
    r = triage(binary)
    r["ok"] = True
    if not r["is_pyinstaller"]:
        r["verdict"] = "非 PyInstaller 样本（或无 cookie）——不要跑解包流程"
    else:
        r["verdict"] = (f"PyInstaller {r['pyinstaller_version']} / Python "
                        f"{r['python_version']}，入口 {r['entry_pyc']}")
    jout(r, indent=2)
    return 0


def cmd_run(args) -> int:
    binary = Path(args.binary)
    if not binary.is_file():
        jout({"ok": False, "error": f"binary not found: {binary}"})
        return 1

    info = triage(binary)
    if not info["is_pyinstaller"]:
        # 闸门：非 PyInstaller 样本禁止跑解包流水线
        jout({"ok": False, "gate": "not_pyinstaller",
              "error": f"{binary.name} 缺少 MEI cookie magic，非 PyInstaller 样本；"
                       "确认样本类型（upx？nuitka？）后换对应管线"})
        return 2
    if not PYINSTXTRACTOR.is_file():
        jout({"ok": False, "error": f"pyinstxtractor not found: {PYINSTXTRACTOR}"})
        return 1
    if not VENV_PY.is_file():
        jout({"ok": False, "error": f"venv python not found: {VENV_PY}"})
        return 1

    out_dir = (Path(args.out) if args.out
               else binary.parent / (binary.name + "_pyinst")).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # pyinstxtractor 把解包目录建在自身 cwd，必须显式指定
    extract = run_cmd([str(VENV_PY), str(PYINSTXTRACTOR), str(binary.resolve())],
                      timeout=600, cwd=out_dir)
    extracted_dir = out_dir / (binary.name + "_extracted")
    result = {"ok": True, "triage": info, "out_dir": str(out_dir),
              "extracted_dir": str(extracted_dir),
              "pyinstxtractor": {
                  "returncode": extract["returncode"],
                  "tail": extract["stdout"].splitlines()[-5:] if extract["stdout"] else [],
              },
              "extracted_ok": extracted_dir.is_dir(),
              "decompiled": []}

    if not result["extracted_ok"]:
        result["ok"] = False
        result["error"] = ("pyinstxtractor 未产出解包目录，请检查其输出"
                           f"（stderr: {extract['stderr'][-500:]}）")
        jout(result, indent=2)
        return 1

    if not args.no_decompile:
        if args.all:
            targets = sorted(extracted_dir.rglob("*.pyc"))
        else:
            targets = [extracted_dir / (n + ".pyc") for n in info["entry_scripts"]]
            targets = [t for t in targets if t.is_file()]
            if not targets:
                # 入口名对不上时兜底取解包根目录的顶层 pyc
                targets = sorted(extracted_dir.glob("*.pyc"))[:1]
                result["fallback"] = "入口 pyc 未按预期落位，退而解包根目录首个 pyc"
        decom_dir = out_dir / "decompiled"
        for pyc in targets:
            result["decompiled"].append(decompile_one(pyc, decom_dir))

    jout(result, indent=2)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="PyInstaller 解包一条龙：magic 分诊 -> pyinstxtractor -> 按版本选反编译器")
    ap.add_argument("binary", help="待解包的 exe")
    ap.add_argument("--check", action="store_true",
                    help="只分诊（是否 PyInstaller / 版本 / 入口 pyc 名），不解包")
    ap.add_argument("--out", help="解包输出目录（默认 <binary名>_pyinst/）")
    ap.add_argument("--all", action="store_true",
                    help="反编译全部 .pyc（默认只反编译入口 pyc）")
    ap.add_argument("--no-decompile", action="store_true", help="只解包不反编译")
    args = ap.parse_args()
    return cmd_check(args) if args.check else cmd_run(args)


if __name__ == "__main__":
    sys.exit(main())
