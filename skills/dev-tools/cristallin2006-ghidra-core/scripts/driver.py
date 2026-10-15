"""PyGhidra driver for the ghidra-core skill.

Replaces the analyzeHeadless-based `run-headless.sh` invocation model. PyGhidra
scripts cannot run under `analyzeHeadless.bat` at all -- that launcher starts a
plain JVM, and Ghidra raises "Ghidra was not started with PyGhidra. Python is not
available" -- so every script invocation has to go through the PyGhidra launcher,
which lives in the Python interpreter of a PyGhidra-enabled environment.

Subcommands
-----------
  import <binary> [--force]
      Import a binary into the workspace project, run auto-analysis, and run
      triage_scan.py to produce out/<name>.triage.json.
  export <binary> [--force]
      Create a persistent, reusable project via Ghidra's own headless importer
      (analyzeHeadless -import). Required before exec/exec-w, since a program
      loaded by PyGhidra itself cannot be saved to the project.
  exec <binary> <script.py> [args...]
      Run a script against the project's program (read-only intent; scripts that
      write must use exec-w).
  exec-w <binary> <script.py> [args...]
      Same, but the project is saved after the script runs.
  list <binary>
      List the programs inside the workspace project.

Script arguments follow the skill's `@out` convention: a first argument of the
form `@<abs-path>` names the JSON output file and is passed through unchanged.

Environment
-----------
  GHIDRA_INSTALL_DIR   Ghidra install (default: the deployment's install)
  DSH_GHIDRA_WS        workspace root (default: ~/.dsh/ghidra-workspace)
  PYGHIDRA_JAVA_HOME   JDK home for the JVM (must be a JDK, not a JRE)
"""
from __future__ import annotations

import argparse
import contextlib
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_config  # noqa: E402 - sibling module, path set above

_IS_NT = os.name == "nt"
DEFAULT_GHIDRA = r"C:\t001s\ghidra_12.1.3_PUBLIC_20260817\ghidra_12.1.3_PUBLIC" if _IS_NT else "/opt/ghidra"
DEFAULT_JAVA_HOME = r"C:\Java" if _IS_NT else "/usr/lib/jvm/java-21-openjdk-amd64"
_JAVA_EXE = "java.exe" if _IS_NT else "java"
DEFAULT_WS = Path(os.path.expanduser("~")) / ".dsh" / "ghidra-workspace"


def _configure_environment() -> Path:
    """Point PyGhidra at the install and a real JDK before it starts the JVM."""
    install = os.environ.get("GHIDRA_INSTALL_DIR") or DEFAULT_GHIDRA
    os.environ["GHIDRA_INSTALL_DIR"] = install
    if not os.environ.get("JAVA_HOME"):
        for candidate in (os.environ.get("PYGHIDRA_JAVA_HOME"), DEFAULT_JAVA_HOME):
            if candidate and (Path(candidate) / "bin" / _JAVA_EXE).is_file():
                os.environ["JAVA_HOME"] = candidate
                break
    if not (Path(install) / "Ghidra").is_dir():
        raise SystemExit(f"Ghidra install not found at {install} (set GHIDRA_INSTALL_DIR)")
    return Path(install)


def workspace() -> Path:
    ws = Path(os.environ.get("DSH_GHIDRA_WS") or DEFAULT_WS)
    for sub in ("projects", "out", "logs"):
        (ws / sub).mkdir(parents=True, exist_ok=True)
    return ws


def project_root() -> Path:
    """Return a project directory whose path has no '.' element.

    Ghidra's ProjectLocator rejects any path element starting with a dot, and the
    default workspace lives under ~/.dsh, so the projects directory is exposed
    through a junction whose path contains no dot elements. Files physically stay
    in the real workspace.
    """
    ws = workspace()
    projects = ws / "projects"
    if ".dsh" not in projects.parts:
        return projects

    link = Path(os.environ.get("DSH_GHIDRA_WS_LINK") or (Path(os.path.expanduser("~")) / "dsh-ghidra-workspace"))
    link_projects = link / "projects"
    if not link_projects.is_dir():
        if os.name != "nt":
            # symlink the workspace root so Ghidra never sees the ".dsh" element.
            # NOTE: do NOT mkdir(link) first — that would create a real dir and
            # the symlink branch below would never run (observed failure).
            try:
                if link.is_symlink():
                    if link.resolve() != ws.resolve():
                        link.unlink()
                        link.symlink_to(ws, target_is_directory=True)
                elif link.is_dir():
                    link.rmdir()  # only empty dirs: a stale mkdir artifact
                    link.symlink_to(ws, target_is_directory=True)
                elif not link.exists():
                    link.symlink_to(ws, target_is_directory=True)
            except OSError as exc:  # pragma: no cover - environment dependent
                raise SystemExit(
                    f"cannot expose {ws} without a dot element: {exc}. "
                    "Set DSH_GHIDRA_WS to a path with no '.' element."
                ) from exc
        else:
            import subprocess

            if link.exists() or link.is_symlink():
                if link.is_symlink():
                    # A junction/symlink: remove the reparse point only, never
                    # the target (os.unlink on a junction raises PermissionError).
                    os.rmdir(link)
                elif link.is_dir():
                    import shutil

                    shutil.rmtree(link, ignore_errors=True)
                else:
                    link.unlink(missing_ok=True)
            subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(link), str(ws)],
                check=True, capture_output=True, text=True,
            )
    if not (link / "projects").is_dir():
        raise SystemExit(f"junction {link} does not resolve to {ws}")
    return link / "projects"


def project_name_for(binary: Path) -> str:
    """Stable project name derived from the binary's content, as the skill documents."""
    import hashlib

    # Hash in 1 MiB chunks: firmware images can be gigabytes, and read_bytes()
    # would pull the whole file into memory.
    hasher = hashlib.sha256()
    with binary.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            hasher.update(chunk)
    return f"dsh_{hasher.hexdigest()[:16]}"


def script_dir() -> Path:
    return Path(__file__).resolve().parent


def run_script(script: Path, project, program, script_args, echo: bool = True):
    """Run one GhidraScript with currentProgram bound to `program`."""
    import pyghidra

    return pyghidra.ghidra_script(
        path=str(script),
        project=project,
        program=program,
        script_args=list(script_args),
        echo_stdout=echo,
        echo_stderr=echo,
    )


# --------------------------------------------------------------------------- import

def cmd_import(args: argparse.Namespace) -> int:
    import pyghidra

    binary = Path(args.binary).resolve()
    if not binary.is_file():
        raise SystemExit(f"binary not found: {binary}")

    ws = workspace()
    name = project_name_for(binary)
    project_path = project_root()
    gpr = project_path / f"{name}.gpr"

    if gpr.exists() and not args.force:
        print(f"import: project '{name}' already exists (use --force to re-import)")
    elif gpr.exists():
        import shutil

        shutil.rmtree(project_path / f"{name}.rep", ignore_errors=True)
        gpr.unlink(missing_ok=True)
        print(f"import: removed existing project '{name}'")

    print(f"import: project '{name}' from {binary.name}")
    project = pyghidra.open_project(str(project_path), name, create=True)
    try:
        with _open_program(pyghidra, project, binary, create=True) as program:
            # Replaces the Jython preScript: analysis options must be set on a
            # loaded program before analyze() runs.
            applied = analysis_config.configure(program, args.analysis)
            if applied["changed"]:
                print(f"import: analysis profile '{args.analysis}' -> "
                      + ", ".join(f"{k}={'on' if v else 'off'}" for k, v in applied["changed"].items()))

            print("import: analysis")
            log = pyghidra.analyze(program)
            (ws / "logs" / f"{name}.analysis.log").write_text(log or "", encoding="utf-8")

            triage = script_dir() / "triage_scan.py"
            out = ws / "out" / f"{binary.name}.triage.json"
            if not triage.is_file():
                print(f"import: WARNING: triage_scan.py missing at {triage}", file=sys.stderr)
            else:
                print(f"import: triage_scan.py -> {out}")
                stdout, stderr = run_script(triage, project, program, [f"@{out}"])
                if stderr and stderr.strip():
                    (ws / "logs" / f"{name}.triage.stderr.log").write_text(stderr, encoding="utf-8")
                if out.is_file():
                    print(f"import: triage report written: {out}")
                else:
                    print("import: WARNING: triage report missing", file=sys.stderr)
                    return 1

            # NOTE: the program cannot be persisted from here. loader.load()
            # returns it behind a DomainFileProxy that reports read-only, and
            # neither DomainFile.setReadOnly (UnsupportedOperationException on a
            # proxy) nor ProgramDB.setChanged (no such method) clears it, so
            # program.save() raises ghidra.util.ReadOnlyException. The project is
            # therefore usable only for the length of this process.
            #
            # To get a project that outlives the process, create it with
            # Ghidra's own headless importer first -- `driver.py export` does
            # exactly that -- then point exec/exec-w at the same workspace.
            print("import: the program is live for this process only; "
                  "run 'driver.py export' once to persist a reusable project")
    finally:
        project.close()

    print(f"import: done (project {name})")
    return 0


@contextlib.contextmanager
def _open_program(pyghidra, project, binary: Path, create: bool = False):
    """Yield the program for `binary` in `project`, importing it when needed."""
    from java.io import File  # noqa: N813 - JPype Java class

    found: list[str] = []
    pyghidra.walk_programs(project, lambda domain_file, _program: found.append(domain_file.getPathname()))
    match = next((p for p in found if p.rsplit("/", 1)[-1] == binary.name), None)

    if match is not None:
        program, consumer = pyghidra.consume_program(project, match)
        try:
            yield program
        finally:
            if consumer is not None:
                program.release(consumer)
        return

    if not create:
        raise SystemExit(f"{binary.name} is not in the project")

    print(f"import: loading {binary.name}")
    loader = (pyghidra.program_loader()
              .source(File(str(binary)))
              .project(project)
              .name(binary.name))
    results = loader.load()
    try:
        # program_loader().load() returns LoadResults, not a Program.
        yield results.getPrimaryDomainObject()
    finally:
        results.close()


# ----------------------------------------------------------------------------- exec


def cmd_export(args: argparse.Namespace) -> int:
    """Create a reusable project through Ghidra's own headless importer.

    PyGhidra cannot persist a program it loaded itself (see cmd_import), but
    `analyzeHeadless -import` can, and the resulting flat project is exactly what
    exec/exec-w open. This is the one place the skill still uses analyzeHeadless,
    with a `.java`-free argument list so no script provider is involved.
    """
    import subprocess

    install = Path(os.environ["GHIDRA_INSTALL_DIR"])
    headless = install / "support" / ("analyzeHeadless.bat" if _IS_NT else "analyzeHeadless")
    if not headless.is_file():
        raise SystemExit(f"headless launcher not found at {headless}")

    binary = Path(args.binary).resolve()
    if not binary.is_file():
        raise SystemExit(f"binary not found: {binary}")

    ws = workspace()
    name = project_name_for(binary)
    gpr = project_root() / f"{name}.gpr"
    if gpr.exists() and not args.force:
        print(f"export: project '{name}' already exists (use --force to re-import)")
        return 0
    if gpr.exists():
        import shutil

        shutil.rmtree(project_root() / f"{name}.rep", ignore_errors=True)
        gpr.unlink(missing_ok=True)

    env = dict(os.environ)
    env.setdefault("JAVA_HOME", DEFAULT_JAVA_HOME)
    # Keep Ghidra's own settings inside the workspace, matching the plugin.
    settings = ws / "settings"
    settings.mkdir(parents=True, exist_ok=True)
    for key in ("APPDATA", "LOCALAPPDATA", "USERPROFILE"):
        env[key] = str(settings)
    # Force the project owner identity: the host USERNAME (e.g. Lenovo) must not
    # leak through, or opening a project created by this skill raises
    # NotOwnerException. All projects are owned by "dsh".
    env["USERNAME"] = "dsh"
    env["USERDOMAIN"] = "DSH"

    argv = [str(headless), str(project_root()), name, "-import", str(binary)]
    if args.overwrite:
        argv.append("-overwrite")
    if args.analysis > 0:
        argv += ["-analysisTimeoutPerFile", str(args.analysis)]
    if args.max_cpu:
        argv += ["-max-cpu", str(args.max_cpu)]

    log_path = ws / "logs" / f"{name}.export.log"
    print(f"export: {binary.name} -> project '{name}'")
    completed = subprocess.run(argv, env=env, capture_output=True, text=True, cwd=str(ws))
    log_path.write_text((completed.stdout or "") + "\n--- stderr ---\n" + (completed.stderr or ""),
                        encoding="utf-8")

    if completed.returncode != 0:
        print(f"export: analyzeHeadless exit={completed.returncode} (log {log_path})", file=sys.stderr)
        return completed.returncode
    if not (project_root() / f"{name}.rep").is_dir():
        print(f"export: no project created (log {log_path})", file=sys.stderr)
        return 1

    print(f"export: done - exec/exec-w can now open '{name}' (log {log_path})")
    return 0


def _as_posix(path) -> str:
    """Forward-slash form for paths handed to Ghidra's Java option parser.

    analyzeHeadless reads its own arguments through a Java property parser, so a Windows
    backslash is treated as an escape and the path is rejected with
    "Bad argument: C:\\...".  Ghidra accepts forward slashes on Windows.
    """
    return Path(path).as_posix()


def run_java_script(binary: Path, script: Path, script_args, name: str, read_only: bool,
                    extra_script_dirs=()):
    """Run a Java GhidraScript through Ghidra's own headless launcher.

    PyGhidra's `ghidra_script()` cannot run a .java script that lives outside a
    registered script source directory: Ghidra's JavaScriptProvider raises
    "Failed to find source bundle containing script".  `analyzeHeadless -scriptPath`
    registers the directory properly, and this is the same path the reverse-ghidra
    plugin uses for its Bridge*.java scripts, so Java and Python scripts reach the
    project through equivalent means.
    """
    import subprocess

    install = Path(os.environ["GHIDRA_INSTALL_DIR"])
    headless = install / "support" / ("analyzeHeadless.bat" if _IS_NT else "analyzeHeadless")
    if not headless.is_file():
        raise SystemExit(f"headless launcher not found at {headless}")

    ws = workspace()
    env = dict(os.environ)
    env.setdefault("JAVA_HOME", DEFAULT_JAVA_HOME)
    settings = ws / "settings"
    settings.mkdir(parents=True, exist_ok=True)
    for key in ("APPDATA", "LOCALAPPDATA", "USERPROFILE"):
        env[key] = str(settings)
    # Force the project owner identity: the host USERNAME (e.g. Lenovo) must not
    # leak through, or opening a project created by this skill raises
    # NotOwnerException. All projects are owned by "dsh".
    env["USERNAME"] = "dsh"
    env["USERDOMAIN"] = "DSH"

    dirs = [_as_posix(script.parent)]
    dirs += [_as_posix(d) for d in extra_script_dirs if Path(d).is_dir()]
    argv = [str(headless), _as_posix(project_root()), name,
            "-scriptPath", ";".join(dict.fromkeys(dirs)),
            "-process", binary.name,
            "-noanalysis",
            "-postScript", script.name]
    argv += [str(a) for a in script_args]
    if read_only:
        argv.append("-readOnly")

    log_path = ws / "logs" / f"{name}.{script.stem}.java.log"
    completed = subprocess.run(argv, env=env, capture_output=True, text=True, cwd=str(ws))
    text = (completed.stdout or "") + "\n--- stderr ---\n" + (completed.stderr or "")
    log_path.write_text(text, encoding="utf-8")
    print(text)
    if completed.returncode != 0:
        print(f"exec: analyzeHeadless exit={completed.returncode} (log {log_path})",
              file=sys.stderr)
    return completed.returncode


def cmd_exec(args: argparse.Namespace) -> int:
    binary = Path(args.binary).resolve()
    script = Path(args.script)
    if not script.is_absolute():
        for candidate in (script_dir() / script.name, Path.cwd() / script.name,
                          workspace() / "scripts" / script.name):
            if candidate.is_file():
                script = candidate
                break
    if not script.is_file():
        raise SystemExit(f"script not found: {args.script}")

    ws = workspace()
    name = project_name_for(binary)
    project_path = project_root()
    gpr = project_path / f"{name}.gpr"
    if not gpr.exists():
        raise SystemExit(f"project '{name}' not found - run: {Path(__file__).name} export {binary} "
                         "(import creates a non-persistent project; only export persists it)")

    outer = project_path / f"{name}.exec.log"
    print(f"exec: project={name} script={script.name}")

    if script.suffix.lower() == ".java":
        # Java scripts go through analyzeHeadless; see run_java_script for why.
        rc = run_java_script(binary, script, args.script_args, name, read_only=not args.write,
                             extra_script_dirs=[ws / "scripts"])
        print(f"exec: done (log {ws / 'logs' / (name + '.' + script.stem + '.java.log')})")
        return rc

    import pyghidra

    # PyGhidra writes changes back when the project is saved on close; a read-only
    # pass simply skips the explicit save below.
    with pyghidra.open_project(str(project_path), name, create=False) as project:
        with _open_program(pyghidra, project, binary, create=False) as program:
            stdout, stderr = run_script(script, project, program, args.script_args)
            outer.write_text((stdout or "") + "\n--- stderr ---\n" + (stderr or ""), encoding="utf-8")
            if args.write:
                program.save("ghidra-core script", None)
                print("exec: project saved")
    print(f"exec: done (log {outer})")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    import pyghidra

    binary = Path(args.binary).resolve()
    ws = workspace()
    name = project_name_for(binary)
    rows = []
    with pyghidra.open_project(str(project_root()), name, create=False) as project:
        # walk_programs is callback-based: it opens each program inside its own
        # context, so collect only the cheap facts here.
        pyghidra.walk_programs(
            project,
            lambda domain_file, program: rows.append(
                (str(domain_file.getPathname()), str(program.getLanguageID()))),
        )
    if not rows:
        print(f"list: project '{name}' contains no programs")
    for path, language in rows:
        print(f"  {path}  ({language})")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ghidra-core driver", description=__doc__)
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose JVM output")
    sub = parser.add_subparsers(dest="command", required=True)

    p_import = sub.add_parser("import", help="import + analyze + triage")
    p_import.add_argument("binary")
    p_import.add_argument("--force", action="store_true")
    p_import.add_argument("--analysis", choices=analysis_config.MODES, default="minimal",
                          help="analysis profile: minimal disables the heavy analyzers "
                               "(default), default enables them all")
    p_import.set_defaults(func=cmd_import)

    p_export = sub.add_parser("export", help="create a reusable project via Ghidra's headless importer")
    p_export.add_argument("binary")
    p_export.add_argument("--force", action="store_true")
    p_export.add_argument("--overwrite", action="store_true", help="pass -overwrite to the importer")
    p_export.add_argument("--analysis", type=int, default=600,
                          help="per-file analysis timeout in seconds; 0 skips the flag (default 600)")
    p_export.add_argument("--max-cpu", type=int, default=4)
    p_export.set_defaults(func=cmd_export)

    for cmd, write in (("exec", False), ("exec-w", True)):
        p = sub.add_parser(cmd, help="run a script against the project")
        p.add_argument("binary")
        p.add_argument("script")
        p.add_argument("script_args", nargs=argparse.REMAINDER)
        p.set_defaults(func=cmd_exec, write=write)

    p_list = sub.add_parser("list", help="list programs in the project")
    p_list.add_argument("binary")
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args(argv)
    install = _configure_environment()

    # Force the project owner identity in this process too, before the JVM and
    # Ghidra come up: opening a project owned by someone else raises
    # NotOwnerException, and all skill-created projects belong to "dsh".
    os.environ["USERNAME"] = "dsh"
    os.environ["USERDOMAIN"] = "DSH"

    # The JVM must be up before any ghidra.* import; every pyghidra API call
    # below assumes a started launcher.
    import pyghidra

    if not pyghidra.started():
        pyghidra.start(verbose=args.verbose, install_dir=install)

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
