"""Run a Fift script with the skill's standard TON include paths.

Use this for one-off Fift helpers that emit BoCs or other artifacts without
having to hand-assemble the create-state invocation each time.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from ton_triage_lib import load_install, resolve_path, runtime_from_args


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a Fift script with standard TON include paths")
    parser.add_argument("--wallet-env", help="Path to wallet-env.txt emitted by the network runner")
    parser.add_argument("--run-dir", help="Run directory containing wallet-env.txt")
    parser.add_argument("--repo-root", help="Path to the TON repo root")
    parser.add_argument("--build", help="Build directory containing create-state")
    parser.add_argument("--script", required=True, help="Path to the Fift script to execute")
    parser.add_argument(
        "--cwd",
        help="Working directory for outputs created by the Fift script; defaults to WORKDIR from wallet-env",
    )
    parser.add_argument(
        "script_args",
        nargs=argparse.REMAINDER,
        help="Arguments passed through to the Fift script after '--'",
    )

    args = parser.parse_args()
    runtime = runtime_from_args(args, require_config=False)
    repo_root = runtime.repo_root
    build_dir = runtime.build_dir
    script_path = resolve_path(Path.cwd(), args.script)
    if args.cwd:
        cwd = resolve_path(Path.cwd(), args.cwd)
    elif runtime.workdir is not None:
        cwd = runtime.workdir
    else:
        cwd = Path.cwd().resolve()
    cwd.mkdir(parents=True, exist_ok=True)
    install = load_install(repo_root, build_dir)

    passthrough = args.script_args
    if passthrough[:1] == ["--"]:
        passthrough = passthrough[1:]

    cmd = [str(install.fift_exe)]
    for include_dir in install.fift_include_dirs:
        cmd += ["-I", str(include_dir)]
    cmd += ["-s", str(script_path), *passthrough]

    print("running:", " ".join(cmd))
    print(f"cwd: {cwd}")
    subprocess.run(cmd, cwd=cwd, check=True)


if __name__ == "__main__":
    main()
