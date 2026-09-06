"""Shared runtime library for the ton-bug-triage skill scripts.

This module centralizes path resolution, tontester integration, tonlib client
management, and Fift/Tolk helper routines so the leaf scripts stay small and
task-focused.
"""

from __future__ import annotations

import asyncio
import os
import re
import shlex
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


# --- Path and env utilities ---


def resolve_path(base: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = base / path
    return path.resolve()


def parse_env_file(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        if not sep:
            raise ValueError(f"invalid env line: {raw_line!r}")
        env[key] = value
    return env


def new_run_dir(base: Path) -> Path:
    base.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix="run-", dir=base))


def write_wallet_env(
    env_file: Path,
    *,
    repo_root: Path,
    build_dir: Path,
    tonlibjson: Path,
    workdir: Path,
    state_dir: Path,
    main_wallet_base: Path,
    liteclient_config: Path,
    lite_db: Path | None,
    extra: dict[str, str] | None = None,
) -> None:
    lines = [
        f"REPO_ROOT={repo_root}",
        f"BUILD_DIR={build_dir}",
        f"TONLIBJSON={tonlibjson}",
        f"WORKDIR={workdir}",
        f"STATE_DIR={state_dir}",
        f"MAIN_WALLET_BASE={main_wallet_base}",
        f"LITECLIENT_CONFIG={liteclient_config}",
    ]
    if lite_db is not None:
        lines.append(f"LITECLIENT_DB={lite_db}")
    if extra:
        for key, value in sorted(extra.items()):
            lines.append(f"{key}={value}")
    env_file.write_text("\n".join(lines) + "\n")


# --- Runtime resolution ---


@dataclass
class RuntimeConfig:
    repo_root: Path
    build_dir: Path
    tonlibjson: Path | None = None
    config_path: Path | None = None
    workdir: Path | None = None
    state_dir: Path | None = None
    main_wallet_base: Path | None = None
    lite_db: Path | None = None


def ensure_tonapi(repo_root: Path) -> None:
    tonapi_dir = repo_root / "test" / "tontester" / "src" / "tonapi"
    if tonapi_dir.exists():
        return

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "test" / "tontester" / "src")
    subprocess.run(
        [sys.executable, str(repo_root / "test" / "tontester" / "generate_tl.py")],
        check=True,
        env=env,
    )


def add_tontester_to_syspath(repo_root: Path) -> None:
    ensure_tonapi(repo_root)
    path = str(repo_root / "test" / "tontester" / "src")
    if path not in sys.path:
        sys.path.insert(0, path)


def runtime_from_args(args, *, require_config: bool = True) -> RuntimeConfig:
    """Resolve runtime paths from CLI args.

    Resolution order is:
    1. explicit `--wallet-env`
    2. `--run-dir` plus `wallet-env.txt` under that directory
    3. explicit `--repo-root` / `--build` / `--config`

    The returned RuntimeConfig always contains resolved absolute paths. Pass
    `require_config=False` for helpers that do not need a lite-client config.
    """
    wallet_env = getattr(args, "wallet_env", None)
    run_dir = getattr(args, "run_dir", None)
    repo_root_arg = getattr(args, "repo_root", None)
    build_arg = getattr(args, "build", None)
    config_arg = getattr(args, "config", None)

    if wallet_env:
        env_path = Path(wallet_env).resolve()
    elif run_dir:
        env_path = Path(run_dir).resolve() / "wallet-env.txt"
    else:
        env_path = None

    if env_path is not None:
        env = parse_env_file(env_path)
        repo_root = (
            resolve_path(Path.cwd(), repo_root_arg)
            if repo_root_arg is not None
            else Path(env["REPO_ROOT"]).resolve()
        )
        build_overridden = build_arg is not None
        build_dir = (
            resolve_path(repo_root, build_arg)
            if build_overridden
            else Path(env["BUILD_DIR"]).resolve()
        )
        tonlibjson = (
            None
            if build_overridden or "TONLIBJSON" not in env
            else Path(env["TONLIBJSON"]).resolve()
        )
        config_path = (
            resolve_path(repo_root, config_arg)
            if config_arg is not None
            else (Path(env["LITECLIENT_CONFIG"]).resolve() if "LITECLIENT_CONFIG" in env else None)
        )
        workdir = Path(env["WORKDIR"]).resolve() if "WORKDIR" in env else None
        state_dir = (
            resolve_path(repo_root, args.state_dir)
            if getattr(args, "state_dir", None)
            else (Path(env["STATE_DIR"]).resolve() if "STATE_DIR" in env else None)
        )
        main_wallet_base = (
            resolve_path(repo_root, args.wallet_base)
            if getattr(args, "wallet_base", None)
            else (Path(env["MAIN_WALLET_BASE"]).resolve() if "MAIN_WALLET_BASE" in env else None)
        )
        lite_db = Path(env["LITECLIENT_DB"]).resolve() if "LITECLIENT_DB" in env else None
        return RuntimeConfig(
            repo_root=repo_root,
            build_dir=build_dir,
            tonlibjson=tonlibjson,
            config_path=config_path,
            workdir=workdir,
            state_dir=state_dir,
            main_wallet_base=main_wallet_base,
            lite_db=lite_db,
        )

    if repo_root_arg is None or build_arg is None or (require_config and config_arg is None):
        raise SystemExit(
            "pass either --wallet-env/--run-dir or the explicit inputs required by this helper"
        )

    repo_root = resolve_path(Path.cwd(), repo_root_arg)
    build_dir = resolve_path(repo_root, build_arg)
    config_path = resolve_path(repo_root, config_arg) if config_arg is not None else None
    state_dir = resolve_path(repo_root, args.state_dir) if getattr(args, "state_dir", None) else None
    main_wallet_base = (
        resolve_path(repo_root, args.wallet_base)
        if getattr(args, "wallet_base", None)
        else (state_dir / "main-wallet" if state_dir else None)
    )
    return RuntimeConfig(
        repo_root=repo_root,
        build_dir=build_dir,
        tonlibjson=None,
        config_path=config_path,
        state_dir=state_dir,
        main_wallet_base=main_wallet_base,
    )


def load_install(repo_root: Path, build_dir: Path):
    add_tontester_to_syspath(repo_root)
    from tontester.install import Install

    return Install(build_dir, repo_root)


# --- Subprocess helpers ---


def format_command(cmd: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in cmd)


def run_subprocess(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    capture_output: bool = False,
    text: bool = True,
):
    print(f"running: {format_command(cmd)}")
    if cwd is not None:
        print(f"cwd: {cwd}")
    try:
        return subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            check=True,
            capture_output=capture_output,
            text=text,
        )
    except subprocess.CalledProcessError as exc:
        if capture_output:
            if exc.stdout:
                print(exc.stdout, end="" if exc.stdout.endswith("\n") else "\n")
            if exc.stderr:
                print(exc.stderr, end="" if exc.stderr.endswith("\n") else "\n", file=sys.stderr)
        raise


def build_fift_command(
    repo_root: Path,
    build_dir: Path,
    script_path: Path,
    script_args: list[str] | None = None,
) -> list[str]:
    install = load_install(repo_root, build_dir)
    cmd = [str(install.fift_exe)]
    for include_dir in install.fift_include_dirs:
        cmd += ["-I", str(include_dir)]
    cmd += ["-s", str(script_path)]
    if script_args:
        cmd += script_args
    return cmd


def run_fift_script_command(
    repo_root: Path,
    build_dir: Path,
    script_path: Path,
    *,
    cwd: Path,
    script_args: list[str] | None = None,
    capture_output: bool = False,
):
    cmd = build_fift_command(repo_root, build_dir, script_path, script_args)
    return run_subprocess(
        cmd,
        cwd=cwd,
        capture_output=capture_output,
        text=True,
    )


# --- Tolk build management ---


@dataclass(frozen=True)
class TolkBuildInfo:
    binary: Path
    version: str | None
    build_commit: str | None
    build_date: str | None


def resolve_tolk_binary(build_dir: Path) -> Path:
    return build_dir / "tolk" / "tolk"


def repo_head_commit(repo_root: Path) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        check=True,
        text=True,
        capture_output=True,
    )
    return completed.stdout.strip()


def read_tolk_build_info(build_dir: Path) -> TolkBuildInfo:
    binary = resolve_tolk_binary(build_dir)
    if not binary.exists():
        raise FileNotFoundError(f"tolk compiler not found at {binary}")

    completed = subprocess.run(
        [str(binary), "-v"],
        check=True,
        text=True,
        capture_output=True,
    )
    version = None
    build_commit = None
    build_date = None
    for raw_line in completed.stdout.splitlines():
        line = raw_line.strip()
        if line.startswith("Tolk compiler v"):
            version = line.removeprefix("Tolk compiler v").strip() or None
        elif line.startswith("Build commit:"):
            build_commit = line.removeprefix("Build commit:").strip() or None
        elif line.startswith("Build date:"):
            build_date = line.removeprefix("Build date:").strip() or None

    return TolkBuildInfo(
        binary=binary,
        version=version,
        build_commit=build_commit,
        build_date=build_date,
    )


def ensure_tolk_matches_repo(repo_root: Path, build_dir: Path) -> TolkBuildInfo:
    info = read_tolk_build_info(build_dir)
    head = repo_head_commit(repo_root)
    if info.build_commit != head:
        raise RuntimeError(
            "stale tolk build: "
            f"{info.binary} reports commit {info.build_commit or '<unknown>'}, "
            f"but repo HEAD is {head}; run `ninja -C {build_dir} tolk` and retry"
        )
    return info


# --- Tonlib client and async helpers ---


async def build_tonlib_client(runtime: RuntimeConfig, verbosity: int = 0, request_timeout: float = 5.0):
    add_tontester_to_syspath(runtime.repo_root)
    from tonapi import ton_api
    from tonlib import TonlibClient

    if runtime.config_path is None:
        raise SystemExit("this helper needs a lite-client config; use --wallet-env/--run-dir or pass --config")

    tonlibjson = runtime.tonlibjson
    if tonlibjson is None:
        install = load_install(runtime.repo_root, runtime.build_dir)
        tonlibjson = install.tonlibjson
    config = ton_api.Liteclient_config_global.from_json(runtime.config_path.read_text())
    client = TonlibClient(
        ls_index=0,
        config=config,
        cdll_path=tonlibjson,
        verbosity_level=verbosity,
    )
    await tonlib_call(
        client.init(),
        timeout=request_timeout,
        label="tonlib init",
    )
    return client


def _tonlib_wrapper(client):
    # TonlibClient does not expose raw execute(); the helper scripts rely on the
    # current private wrapper attribute until tonlib provides a public hook.
    wrapper = client._tonlib_wrapper  # pylint: disable=protected-access
    if wrapper is None:
        raise RuntimeError("tonlib client is not initialized")
    return wrapper


async def tonlib_call(awaitable, *, timeout: float, label: str):
    task = asyncio.create_task(awaitable)
    try:
        return await asyncio.wait_for(task, timeout=timeout)
    except asyncio.TimeoutError as exc:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        raise TimeoutError(f"{label} timed out after {timeout:.1f}s") from exc


async def get_masterchain_info_with_timeout(client, timeout: float):
    return await tonlib_call(
        client.get_masterchain_info(),
        timeout=timeout,
        label="get_masterchain_info()",
    )


async def raw_send_message_with_timeout(client, body: bytes, timeout: float):
    return await tonlib_call(
        client.raw_send_message(body),
        timeout=timeout,
        label="raw_send_message()",
    )


async def raw_get_account_state_with_timeout(client, account_address: str, timeout: float):
    return await tonlib_call(
        client.raw_get_account_state(account_address),
        timeout=timeout,
        label="raw_get_account_state()",
    )


async def wait_for_mc_advance(
    client,
    *,
    before_seqno: int,
    wait_timeout: float,
    request_timeout: float,
    poll_interval: float = 0.2,
) -> int:
    deadline = asyncio.get_running_loop().time() + wait_timeout
    while True:
        info = await get_masterchain_info_with_timeout(client, request_timeout)
        if info.last is not None and info.last.seqno > before_seqno:
            return info.last.seqno
        if asyncio.get_running_loop().time() >= deadline:
            raise TimeoutError("timed out waiting for masterchain seqno to advance")
        await asyncio.sleep(poll_interval)


# --- Address and account helpers ---


@dataclass
class NormalizedAddress:
    input_value: str
    serialized: str
    raw: str
    workchain_id: int
    bounceable: bool
    testnet: bool
    addr_hex: str


async def normalize_account_address(
    client,
    address: str,
    *,
    request_timeout: float = 5.0,
) -> NormalizedAddress:
    from tonapi import tonlib_api

    wrapper = _tonlib_wrapper(client)
    unpack_req = tonlib_api.UnpackAccountAddressRequest(account_address=address)
    unpacked = unpack_req.parse_result(
        await tonlib_call(
            wrapper.execute(unpack_req),
            timeout=request_timeout,
            label="unpackAccountAddress",
        )
    )

    packed_req = tonlib_api.PackAccountAddressRequest(account_address=unpacked)
    serialized = packed_req.parse_result(
        await tonlib_call(
            wrapper.execute(packed_req),
            timeout=request_timeout,
            label="packAccountAddress",
        )
    ).account_address

    raw = f"{unpacked.workchain_id}:{unpacked.addr.hex()}"
    return NormalizedAddress(
        input_value=address,
        serialized=serialized,
        raw=raw,
        workchain_id=unpacked.workchain_id,
        bounceable=unpacked.bounceable,
        testnet=unpacked.testnet,
        addr_hex=unpacked.addr.hex(),
    )


def wallet_address_from_base(wallet_base: Path) -> str:
    addr_path = wallet_base.with_suffix(".addr")
    raw = addr_path.read_bytes()
    if len(raw) == 32:
        workchain_id = 0
        addr = raw
    elif len(raw) == 36:
        addr = raw[:32]
        workchain_id = int.from_bytes(raw[32:], "big", signed=True)
    else:
        raise RuntimeError(f"unexpected wallet address file size for {addr_path}: {len(raw)} bytes")
    return f"{workchain_id}:{addr.hex()}"


# --- Smart contract and TVM ---


def tvm_number_entry(value: int):
    from tonapi import tonlib_api

    return tonlib_api.Tvm_stackEntryNumber(
        number=tonlib_api.Tvm_numberDecimal(number=str(value)),
    )


def stack_entry_to_json(entry):
    return entry.to_dict()


def first_stack_number(run_result) -> int | None:
    if not run_result.stack:
        return None
    first = run_result.stack[0]
    number = getattr(first, "number", None)
    if number is None:
        return None
    decimal = getattr(number, "number", None)
    if decimal is None:
        return None
    return int(decimal)


async def resolve_wallet_seqno(client, wallet_address: str, *, request_timeout: float = 5.0) -> tuple[int, str]:
    attempts: list[str] = []
    for method in ("seqno", "85143"):
        try:
            _normalized, _info, result = await run_get_method(
                client,
                wallet_address,
                method,
                request_timeout=request_timeout,
            )
        except Exception as exc:
            attempts.append(f"{method}: {exc}")
            continue

        seqno = first_stack_number(result)
        if seqno is not None:
            return seqno, method
        attempts.append(f"{method}: top of stack was not numeric")

    joined = "; ".join(attempts) if attempts else "no methods attempted"
    raise RuntimeError(f"failed to resolve wallet seqno for {wallet_address}: {joined}")


async def load_smc(client, address: str, *, request_timeout: float = 5.0):
    from tonapi import tonlib_api

    normalized = await normalize_account_address(client, address, request_timeout=request_timeout)
    wrapper = _tonlib_wrapper(client)
    request = tonlib_api.Smc_loadRequest(
        account_address=tonlib_api.AccountAddress(account_address=normalized.serialized)
    )
    info = request.parse_result(
        await tonlib_call(
            wrapper.execute(request),
            timeout=request_timeout,
            label="smc.load",
        )
    )
    return normalized, info


def method_id(method: str):
    from tonapi import tonlib_api

    try:
        return tonlib_api.Smc_methodIdNumber(number=int(method, 0))
    except ValueError:
        return tonlib_api.Smc_methodIdName(name=method)


async def run_get_method(
    client,
    address: str,
    method: str,
    stack_numbers: list[int] | None = None,
    *,
    request_timeout: float = 5.0,
):
    from tonapi import tonlib_api

    normalized, info = await load_smc(client, address, request_timeout=request_timeout)
    wrapper = _tonlib_wrapper(client)
    request = tonlib_api.Smc_runGetMethodRequest(
        id=info.id,
        method=method_id(method),
        stack=[tvm_number_entry(value) for value in (stack_numbers or [])],
    )
    try:
        result = request.parse_result(
            await tonlib_call(
                wrapper.execute(request),
                timeout=request_timeout,
                label="smc.runGetMethod",
            )
        )
        return normalized, info, result
    finally:
        forget = tonlib_api.Smc_forgetRequest(id=info.id)
        await tonlib_call(
            wrapper.execute(forget),
            timeout=request_timeout,
            label="smc.forget",
        )
