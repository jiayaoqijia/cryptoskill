#!/usr/bin/env python
"""Launch the Ghidra GUI detached, optionally opening a workspace project.

Host-side tool (run with the pyghidra-venv python, NOT through driver.py exec):

  python launch_gui.py                      # bare GUI
  python launch_gui.py --open <binary>      # open the project of <binary>
  python launch_gui.py --project dsh_<hash> # open a project by name

Prints a JSON result (PID, log path) and exits immediately; the GUI keeps
running detached. With a leading '@<path>' argument the JSON is also written
to that file (skill @out convention).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import driver  # noqa: E402 - reuse the skill's environment resolution


def emit(data, out_path=None):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    print(text)
    if out_path:
        Path(out_path).write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", nargs="?", default=None,
                        help="optional @<path> for the JSON result")
    parser.add_argument("--open", dest="binary", default=None,
                        help="binary whose dsh_<hash> project should be opened")
    parser.add_argument("--project", dest="project", default=None,
                        help="project name (dsh_<hash>) to open directly")
    args = parser.parse_args()

    out_path = None
    if args.out and args.out.startswith("@"):
        out_path = args.out[1:]

    try:
        install = driver._configure_environment()
        ws = driver.workspace()
        ghidra_run = install / ("ghidraRun.bat" if os.name == "nt" else "ghidraRun")
        if not ghidra_run.is_file():
            emit({"status": "error", "error": f"ghidraRun launcher not found at {ghidra_run}"},
                 out_path)
            return 1

        argv = [str(ghidra_run)]
        project_name = None
        if args.binary:
            binary = Path(args.binary).resolve()
            if not binary.is_file():
                emit({"status": "error", "error": f"binary not found: {binary}"}, out_path)
                return 1
            project_name = driver.project_name_for(binary)
        elif args.project:
            project_name = args.project

        if project_name:
            gpr = driver.project_root() / f"{project_name}.gpr"
            if not gpr.is_file():
                emit({"status": "error",
                      "error": f"project '{project_name}' not found at {gpr} "
                               f"(run driver.py export first)"}, out_path)
                return 1
            # GhidraRun takes a single non -D argument: the full path of the
            # .gpr file (see GhidraRun.processArguments/openProject).
            argv.append(driver._as_posix(gpr))

        log_path = ws / "logs" / "gui-launch.log"
        log_file = open(str(log_path), "ab")

        env = dict(os.environ)
        env.setdefault("JAVA_HOME", driver.DEFAULT_JAVA_HOME)
        # GUI runs outside the dsh sandbox: keep the REAL user profile so the
        # operator sees their own Ghidra settings, but pin the owner identity so
        # projects created headless (owner "dsh") open without NotOwnerException.
        env["USERNAME"] = "dsh"
        env["USERDOMAIN"] = "DSH"

        creationflags = 0
        if os.name == "nt":
            creationflags = (subprocess.DETACHED_PROCESS
                             | subprocess.CREATE_NEW_PROCESS_GROUP)
        proc = subprocess.Popen(
            argv, stdout=log_file, stderr=subprocess.STDOUT,
            close_fds=True, creationflags=creationflags, env=env,
            cwd=str(ws),
        )
        log_file.close()

        emit({
            "status": "success",
            "pid": proc.pid,
            "command": argv,
            "project": project_name,
            "log": str(log_path),
            "note": "GUI launched detached; close it with taskkill /PID <pid> "
                    "or from the GUI itself",
        }, out_path)
        return 0

    except Exception as exc:
        emit({"status": "error", "error": str(exc)}, out_path)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
