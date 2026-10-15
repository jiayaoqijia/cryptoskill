#!/usr/bin/env python3
"""venv_health.py — 工具 venv 健康检查（判例 a0f3be66：re-tools-venv 的 angr
装了但 claripy 缺失/版本错位，做题中途才暴露，现场 pip 手术烧掉十余分钟）。

检查每个已知 venv 的关键包能否真实 import（不是 pip show——装半截的包
show 得到、import 崩），并校验 angr↔claripy 版本配对。

用法：
  python3 venv_health.py            # 全量检查，发现问题 exit 1
  python3 venv_health.py --quick    # 只查 re-tools-venv（angr 链）

输出每个 venv 的包状态表 + 可照抄的修复命令。stdlib only，不经 daemon。
"""
import subprocess
import sys
from pathlib import Path

HOME = Path.home()

# venv → [(import 名, pip 包名或 None(=跟随上一项/内置), 用途)]
# 注意：angr ≥10 把 claripy 内置（from angr import claripy），PyPI 上
# 独立 claripy 止步 9.x——别再把「import claripy 失败」当缺失去装 claripy 10。
VENVS = {
    "re-tools-venv": [
        ("angr", "angr", "符号执行"),
        ("angr.claripy", "angr", "符号引擎（angr≥10 内置，必须随 angr 可用）"),
        ("z3", "z3-solver", "约束求解"),
        ("capstone", "capstone", "反汇编"),
        ("unicorn", "unicorn", "仿真"),
        ("frida", "frida", "动态插桩"),
    ],
    "re-pwn-venv": [
        ("pwn", "pwntools", "pwn 工具链"),
        ("z3", "z3-solver", "约束求解"),
    ],
    "unpacker-venv": [
        ("capstone", "capstone", "反汇编"),
    ],
    "ghidra-rpc-venv": [
        ("pyghidra", "pyghidra", "Ghidra 引擎"),
        ("jpype", "JPype1", "JVM 桥"),
    ],
    "pyghidra-venv": [
        ("pyghidra", "pyghidra", "Ghidra legacy 后路"),
    ],
}

PROBE = (
    "import importlib,json,sys\n"
    "out={}\n"
    "for mod in sys.argv[1:]:\n"
    "    try:\n"
    "        m=importlib.import_module(mod)\n"
    "        out[mod]={'ok':True,'ver':getattr(m,'__version__','?')}\n"
    "    except Exception as e:\n"
    "        out[mod]={'ok':False,'err':type(e).__name__+': '+str(e)[:120]}\n"
    "print(json.dumps(out))\n"
)


def probe(venv: Path, mods: list[str]) -> dict | None:
    py = venv / "bin" / "python"
    if not py.exists():
        py = venv / "Scripts" / "python.exe"  # Windows 布局兜底
    if not py.exists():
        return None
    r = subprocess.run(
        [str(py), "-c", PROBE, *mods],
        capture_output=True, text=True, timeout=120,
    )
    line = r.stdout.strip().splitlines()
    if not line:
        return {m: {"ok": False, "err": f"probe 无输出: {r.stderr[:120]}"}
                for m in mods}
    import json
    return json.loads(line[-1])


def main() -> int:
    quick = "--quick" in sys.argv
    names = ["re-tools-venv"] if quick else list(VENVS)
    problems = 0
    for name in names:
        venv = HOME / name
        checks = VENVS[name]
        if not venv.is_dir():
            print(f"[skip] ~/{name} 不存在")
            continue
        res = probe(venv, [m for m, _, _ in checks])
        if res is None:
            print(f"[skip] ~/{name} 找不到 python 入口")
            continue
        print(f"== ~/{name} ==")
        for mod, pip_name, why in checks:
            st = res.get(mod, {"ok": False, "err": "no result"})
            if st["ok"]:
                print(f"  OK   {mod:<10} {st['ver']:<12} {why}")
            else:
                problems += 1
                print(f"  FAIL {mod:<10} {st['err']}")
                print(f"       修复: ~/{name}/bin/pip install -U {pip_name}")
        # angr 内置 claripy 的自洽检查：angr≥10 走 from angr import claripy，
        # 独立 claripy 包（≤9.x）与 angr 主次版本错位是老布局的坑，只在两边
        # 都是独立包时才查配对
        a, c = res.get("angr"), res.get("claripy")
        if a and c and a.get("ok") and c.get("ok"):
            if a["ver"].split(".")[:2] != c["ver"].split(".")[:2]:
                problems += 1
                print(f"  FAIL angr {a['ver']} 与 claripy {c['ver']} 主次版本不一致")
                print(f"       修复: ~/{name}/bin/pip install "
                      f"\"claripy=={a['ver']}\"")
    if problems:
        print(f"\n{problems} 个问题——做题中途再修就是 a0f3be66 的 35 分钟空转。"
              "现在就按上面的命令补。")
        return 1
    print("\n全部关键包可真实 import。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
