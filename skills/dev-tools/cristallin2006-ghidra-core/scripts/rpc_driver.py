#!/usr/bin/env python
"""rpc_driver.py - thin dsh wrapper around the ghidra-rpc CLI daemon.

Host-side tool (run with any Python 3, NOT through driver.py exec).

Maps a binary path to its rpc project:
  project = ~/dsh-ghidra-workspace/projects-rpc/dsh_<sha256-16>.gpr
          (junction spelling; the engine must never see a '.dsh' element)
The binary key inside the project is whatever the daemon returns from `load`.

Subcommands:
  ensure <binary> [--timeout N]
                      start daemon if down, load binary if absent (idempotent);
                      prints a heartbeat to stderr while waiting on long
                      start/load steps; --timeout caps each wait step
  status [binary]
  stop   [binary]
  <anything else>     passed through to `ghidra-rpc`, with --project injected;
                      the binary path may be given as first arg and is mapped
                      to its loaded key automatically when unambiguous.
                      `disassemble <binary> <addr> --force` force-disassembles
                      at the exact address (jump-table targets whose case
                      bodies were never disassembled); without --force the
                      read-only next-instruction fallback is unchanged

Environment is self-contained: GHIDRA_INSTALL_DIR / JAVA_HOME /
GHIDRA_RPC_STATE_DIR / LOCALAPPDATA redirection and USERNAME=dsh are set here
with the same defaults as scripts/driver.py.

Any subcommand's JSON output can be written to a file with a leading '@<path>'
argument (skill @out convention).
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

# dsh/Git Bash capture decodes stdout as UTF-8; daemon JSON may carry
# Chinese advice fields — force UTF-8 or a cp936 console emits mojibake.
for _stream in (sys.stdout, sys.stderr):
    if _stream.encoding and _stream.encoding.lower() not in ("utf-8", "utf8"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

HOME = Path(os.path.expanduser("~"))
if os.name == "nt":
    RPC_VENV_PYTHON = HOME / "Desktop" / "src" / "ghidra-bridge" / \
        "ghidra-rpc-venv" / "Scripts" / "python.exe"
    GHIDRA_INSTALL = r"C:\t001s\ghidra_12.1.3_PUBLIC_20260817\ghidra_12.1.3_PUBLIC"
    JAVA_HOME_DEFAULT = r"C:\Java"
else:  # WSL/Linux 部署
    RPC_VENV_PYTHON = HOME / "ghidra-rpc-venv" / "bin" / "python"
    GHIDRA_INSTALL = "/opt/ghidra"
    JAVA_HOME_DEFAULT = "/usr/lib/jvm/java-21-openjdk-amd64"
WS_LINK = HOME / "dsh-ghidra-workspace"  # junction/symlink -> ~/.dsh/ghidra-workspace


def configure_env() -> dict:
    env = dict(os.environ)
    env.setdefault("GHIDRA_INSTALL_DIR", GHIDRA_INSTALL)
    env.setdefault("JAVA_HOME", JAVA_HOME_DEFAULT)
    env.setdefault("GHIDRA_RPC_STATE_DIR", str(WS_LINK / "rpc-state"))
    # endpoint + daemon log live under %LOCALAPPDATA%\ghidra-rpc (Windows
    # transport); keep them inside the dsh workspace sandbox.
    env["LOCALAPPDATA"] = str(WS_LINK / "rpc-localappdata")
    # Project owner identity: all skill-created projects belong to "dsh".
    env["USERNAME"] = "dsh"
    env["USERDOMAIN"] = "DSH"
    (WS_LINK / "rpc-localappdata" / "ghidra-rpc").mkdir(parents=True, exist_ok=True)
    (WS_LINK / "rpc-state").mkdir(parents=True, exist_ok=True)
    (WS_LINK / "projects-rpc").mkdir(parents=True, exist_ok=True)
    return env


def project_for(binary: Path) -> Path:
    hasher = hashlib.sha256()
    with binary.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            hasher.update(chunk)
    return WS_LINK / "projects-rpc" / f"dsh_{hasher.hexdigest()[:16]}.gpr"


def rpc_exe() -> str:
    exe = RPC_VENV_PYTHON.parent / "ghidra-rpc.exe"
    return str(exe) if exe.is_file() else str(RPC_VENV_PYTHON.parent / "ghidra-rpc")


def _parse_rpc_output(stdout: str, stderr: str, returncode: int,
                      cmd: list[str]) -> dict:
    text = (stdout or "").strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = {"ok": False, "error": "cli",
                "message": text or (stderr or "").strip(),
                "exit_code": returncode}
    if not data.get("ok"):
        # Always expose the exact CLI line that failed — a bare click
        # "Missing argument" is meaningless without it.
        data.setdefault("cmd", cmd)
        # Keep the CLI's stderr alongside the server's error text so the
        # original message is never swallowed by the JSON envelope.
        stderr_text = (stderr or "").strip()
        if stderr_text and stderr_text not in str(data.get("message", "")):
            data.setdefault("stderr", stderr_text)
    return data


def run_rpc(env, gpr: Path, argv: list[str], timeout: int | None = None) -> dict:
    # ghidra-rpc's --project is a per-command option: it goes AFTER the
    # subcommand, not before it.
    cmd = [rpc_exe()] + argv + ["--project", str(gpr)]
    proc = subprocess.run(cmd, env=env, capture_output=True, text=True,
                          timeout=timeout)
    return _parse_rpc_output(proc.stdout, proc.stderr, proc.returncode, cmd)


def run_rpc_progress(env, gpr: Path, argv: list[str], timeout: float | None,
                     heartbeat: float = 12.0, label: str = "") -> dict:
    """Like run_rpc, but for long waits (daemon start / binary load+analyze).

    Prints a heartbeat line to stderr every ``heartbeat`` seconds so a big
    binary's first ensure doesn't look dead, and kills the CLI if ``timeout``
    seconds elapse, returning an error with recovery advice. Standard output
    (the JSON result) is unaffected — heartbeats go to stderr only.
    """
    cmd = [rpc_exe()] + argv + ["--project", str(gpr)]
    proc = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)
    step = label or (argv[0] if argv else "rpc")
    started = time.monotonic()
    next_beat = started + heartbeat
    timed_out = False
    while True:
        ret = proc.poll()
        if ret is not None:
            break
        now = time.monotonic()
        if timeout is not None and now - started >= timeout:
            timed_out = True
            proc.kill()
            break
        if now >= next_beat:
            print(f"[ensure] {step}: still waiting "
                  f"({int(now - started)}s elapsed)", file=sys.stderr,
                  flush=True)
            next_beat = now + heartbeat
        time.sleep(0.5)
    out, err = proc.communicate()
    if timed_out:
        return {
            "ok": False,
            "error": "timeout",
            "message": f"'{' '.join(argv)}' did not finish within "
                       f"{int(timeout)}s",
            "advice": ("sample may be too large for one-shot ensure. "
                       "Retry with a larger --timeout, load without analysis "
                       "(passthrough: load <binary> --no-analyze) and analyze "
                       "selectively, or poll `status <binary>` later to check "
                       "whether the daemon finished in the background"),
            "cmd": cmd,
        }
    return _parse_rpc_output(out, err, proc.returncode, cmd)


def emit(data: dict, out_path: str | None) -> int:
    ok = bool(data.get("ok", data.get("status") == "success"))
    text = json.dumps(data, ensure_ascii=False, indent=2)
    print(text)
    if out_path:
        Path(out_path).write_text(text, encoding="utf-8")
    return 0 if ok else 1


def _binary_key(resp: dict) -> str | None:
    result = resp.get("result") or {}
    return result.get("binary")


def ensure_binary(env, binary: Path, timeout: float | None = None,
                  heartbeat: float = 12.0) -> dict:
    """Idempotent: daemon running + binary loaded. Returns the payload dict.

    Long start/load waits print a heartbeat line to stderr every
    ``heartbeat`` seconds. ``timeout`` (seconds) caps each wait step
    (default: 300 s for daemon start, 3600 s for load+analyze).
    """
    if not binary.is_file():
        return {"ok": False, "error": f"binary not found: {binary}"}
    gpr = project_for(binary)

    status = run_rpc(env, gpr, ["status"])
    running = bool((status.get("result") or {}).get("running")
                   or status.get("running"))
    started = False
    if not running:
        start = run_rpc_progress(
            env, gpr, ["start", "--headless", "--detach"],
            timeout=timeout if timeout is not None else 300,
            heartbeat=heartbeat, label="daemon start")
        if not start.get("ok"):
            return {"ok": False, "error": "daemon start failed",
                    "detail": start}
        started = True

    listed = run_rpc(env, gpr, ["list-binaries"])
    binaries = (listed.get("result") or {}).get("binaries", []) or []
    key = next((b["path"] for b in binaries
                if b.get("short_name") == binary.name
                or binary.name in b.get("name", "")), None)
    loaded = False
    if key is None:
        load = run_rpc_progress(
            env, gpr, ["load", str(binary)],
            timeout=timeout if timeout is not None else 3600,
            heartbeat=heartbeat, label="load/analyze")
        if not load.get("ok"):
            hint = ""
            if ".dsh" in str(binary) or str(binary).startswith(str(HOME / ".dsh")):
                hint = (" binary lives under a dotted path element "
                        "(~/.dsh/...) — copy it out of the dsh config tree "
                        "before loading.")
            result = {"ok": False, "error": "load failed" + hint,
                      "detail": load}
            # The ghidra-rpc client's own socket timeout (120 s default for
            # load) can fire before the daemon finishes analysing a large
            # binary; the daemon usually keeps going in the background.
            err_text = (str(load.get("error", "")) + " "
                        + str(load.get("message", ""))).lower()
            if "timeout" in err_text or "timed out" in err_text:
                result["advice"] = (
                    "sample may be too large for the default socket budget. "
                    "The daemon often keeps analysing in the background — "
                    "poll `status <binary>` / retry `ensure` in a minute. "
                    "For a longer upfront budget: passthrough "
                    "`load <binary> --analysis-timeout N` (also raises the "
                    "socket timeout), or `load <binary> --no-analyze` and "
                    "analyse selectively.")
            return result
        key = _binary_key(load)
        loaded = True

    return {
        "ok": True,
        "project": str(gpr),
        "binary_key": key,
        "daemon_started": started,
        "binary_loaded": loaded,
        "analysis_complete": True,
    }


def cmd_ensure(env, binary: Path, out_path, timeout: float | None = None) -> int:
    return emit(ensure_binary(env, binary, timeout=timeout), out_path)


def main(argv: list[str]) -> int:
    args = list(argv)
    out_path = None
    if args and args[0].startswith("@"):
        out_path = args.pop(0)[1:]

    if not args:
        print(__doc__)
        return 2

    env = configure_env()
    sub = args[0]

    if sub == "ensure":
        rest_args = list(args[1:])
        ensure_timeout = None
        if "--timeout" in rest_args:
            i = rest_args.index("--timeout")
            try:
                ensure_timeout = float(rest_args[i + 1])
            except (IndexError, ValueError):
                return emit({"ok": False,
                             "error": "usage: ensure <binary> [--timeout SECONDS]"},
                            out_path)
            del rest_args[i:i + 2]
        if not rest_args:
            return emit({"ok": False,
                         "error": "usage: ensure <binary> [--timeout SECONDS]"},
                        out_path)
        return cmd_ensure(env, Path(rest_args[0]).resolve(), out_path,
                          timeout=ensure_timeout)

    if sub in ("status", "stop"):
        gpr = project_for(Path(args[1]).resolve()) if len(args) > 1 else None
        if gpr is None:
            # allow --project style direct call through to ghidra-rpc
            resp = run_rpc(env, Path(os.environ["GHIDRA_RPC_PROJECT"])
                           if os.environ.get("GHIDRA_RPC_PROJECT") else None, [sub]) \
                if sub == "status" else None
            if resp is None:
                return emit({"ok": False,
                             "error": f"usage: {sub} <binary>  (or set GHIDRA_RPC_PROJECT)"},
                            out_path)
            return emit(resp, out_path)
        return emit(run_rpc(env, gpr, [sub]), out_path)

    # passthrough: <sub> [binary] [rest...] — inject --project, map binary key
    binary = None
    rest = args[1:]
    if rest and not rest[0].startswith("-") and Path(rest[0]).is_file():
        binary = Path(rest[0]).resolve()
        rest = rest[1:]
    if binary is None:
        return emit({"ok": False,
                     "error": f"passthrough needs a binary file as first arg: "
                              f"{sub} <binary> [...]"}, out_path)
    gpr = project_for(binary)

    # 铁律 1 提醒：首次对本样本执行深挖类命令时提示加载 ghidra-static 全文
    #（脚本观测不到 dsh 的 skill 加载状态，退化为每样本提醒一次，不阻断）。
    if sub in ("decompile", "decompile-all", "search-decompiled", "exec-code",
               "emulate-function", "emulate-blob", "pcode", "disassemble"):
        try:
            sha16 = hashlib.sha256(str(binary).encode("utf-8")).hexdigest()[:16]
            marker = WS_LINK / "out" / f".reminded-static-{sha16}"
            if not marker.exists():
                marker.parent.mkdir(parents=True, exist_ok=True)
                marker.write_text("reminded\n", encoding="utf-8")
                print("[提醒] 深挖命令首次命中本样本：确认已用 skill 工具加载 "
                      "ghidra-static 全文（铁律 1）；已加载可忽略，"
                      "本提醒每样本只出现一次", file=sys.stderr)
        except Exception:
            pass

    listed = run_rpc(env, gpr, ["list-binaries"])
    bins = (listed.get("result") or {}).get("binaries", []) or []
    known = any(b.get("short_name") == binary.name
                or binary.name in b.get("name", "") for b in bins)
    if not listed.get("ok") or not known:
        # Daemon down or binary never loaded: auto-ensure instead of dying
        # downstream with click's bare "Missing argument".
        ensured = ensure_binary(env, binary)
        if not ensured.get("ok"):
            return emit({"ok": False,
                         "error": f"auto-ensure failed before '{sub}'",
                         "detail": ensured}, out_path)
        listed = run_rpc(env, gpr, ["list-binaries"])
        bins = (listed.get("result") or {}).get("binaries", []) or []

    def map_key(token):
        """Resolve a binary reference (key/name/short name/file path) to the
        loaded key, or None when unknown/ambiguous."""
        for b in bins:
            if token in (b.get("path"), b.get("name"), b.get("short_name")):
                return b["path"].lstrip("/")
        bn = Path(token).name
        cand = [b for b in bins if bn and bn in b.get("name", "")]
        if len(cand) == 1:
            return cand[0]["path"].lstrip("/")
        return None

    our_key = map_key(str(binary))

    # Multi-binary commands (version-track/function-diff/match-function) take
    # every binary in ONE project. Map each file-path token to its loaded key,
    # loading it into THIS project first when missing, then prepend the anchor
    # binary's own key.
    if sub in ("version-track", "function-diff", "match-function"):
        for i, token in enumerate(rest):
            if token.startswith("-") or not Path(token).is_file():
                continue
            if map_key(token) is None:
                load = run_rpc(env, gpr, ["load", str(Path(token).resolve())],
                               timeout=3600)
                if load.get("ok"):
                    listed = run_rpc(env, gpr, ["list-binaries"])
                    bins = (listed.get("result") or {}).get("binaries", []) or []
        rest = [map_key(t) or t for t in rest]
        if our_key:
            rest = [our_key] + rest
    elif rest:
        k = map_key(rest[0])
        if k:
            rest = [k] + rest[1:]
        elif our_key:
            rest = [our_key] + rest
    elif our_key:
        rest = [our_key]

    resp = run_rpc(env, gpr, [sub] + rest)
    if not resp.get("ok") and "NotRunning" in str(resp.get("error", "")):
        # stop/crash -> restart race: the daemon died between ensure and this
        # command. Re-ensure once and retry the command once.
        ensured = ensure_binary(env, binary)
        if ensured.get("ok"):
            resp = run_rpc(env, gpr, [sub] + rest)
    return emit(resp, out_path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
