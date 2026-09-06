"""Run the proven wallet-to-wallet smoke flow on a local tontester network.

Use this script when you want a known-good end-to-end helper check before a
more specialized deploy or validator-behavior repro.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import shlex
import subprocess
import sys
import time
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from inspect_latest_transaction import inspect_latest_transaction
from ton_triage_lib import (
    build_tonlib_client,
    normalize_account_address,
    raw_get_account_state_with_timeout,
    resolve_wallet_seqno,
    runtime_from_args,
    wallet_address_from_base,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(line_buffering=True)


def _format_command(cmd: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in cmd)


def _run_command(cmd: list[str], *, cwd: Path | None = None) -> str:
    print(f"running: {_format_command(cmd)}")
    completed = subprocess.run(
        cmd,
        cwd=cwd,
        check=True,
        text=True,
        capture_output=True,
    )
    if completed.stdout:
        print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
    if completed.stderr:
        print(completed.stderr, end="" if completed.stderr.endswith("\n") else "\n", file=sys.stderr)
    return completed.stdout


def _run_json_command(cmd: list[str], *, cwd: Path | None = None) -> dict[str, object]:
    return json.loads(_run_command(cmd, cwd=cwd))


def _runtime_from_wallet_env(wallet_env: Path):
    return runtime_from_args(
        argparse.Namespace(
            wallet_env=str(wallet_env),
            run_dir=None,
            repo_root=None,
            build=None,
            config=None,
            state_dir=None,
            wallet_base=None,
        )
    )


def _require_process_alive(process: subprocess.Popen[str], *, context: str) -> None:
    if process.poll() is not None:
        raise RuntimeError(f"network launcher exited during {context} with status {process.returncode}")


def _launch_network(args: argparse.Namespace) -> tuple[subprocess.Popen[str], Path, Path]:
    if args.validators < 2:
        raise SystemExit("--validators must be at least 2 for this demo")

    cmd = [
        sys.executable,
        "-u",
        str(SCRIPT_DIR / "run_basic_network.py"),
        "--repo-root",
        str(args.repo_root),
        "--build",
        str(args.build),
        "--workdir",
        args.workdir,
        "--base-port",
        str(args.base_port),
        "--validators",
        str(args.validators),
        "--mc-seqno",
        str(args.mc_seqno),
        "--emit-wallet-env",
        "--keep-alive",
        str(args.keep_alive),
    ]
    print(f"running: {_format_command(cmd)}")
    process = subprocess.Popen(
        cmd,
        cwd=args.repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    if process.stdout is None:
        raise RuntimeError("failed to capture launcher stdout")

    run_dir: Path | None = None
    wallet_env: Path | None = None
    deadline = time.time() + args.launch_timeout
    while True:
        line = process.stdout.readline()
        if not line:
            if process.poll() is not None:
                raise RuntimeError(f"network launcher exited early with status {process.returncode}")
            if time.time() >= deadline:
                raise TimeoutError("timed out waiting for network launcher output")
            time.sleep(0.1)
            continue

        print(line, end="")
        if line.startswith("run dir: "):
            run_dir = Path(line.removeprefix("run dir: ").strip())
        elif line.startswith("wallet env: "):
            wallet_env = Path(line.removeprefix("wallet env: ").strip())
        elif line.startswith("reached mc seqno >="):
            break

        if time.time() >= deadline:
            raise TimeoutError("timed out waiting for the launcher to reach the target mc seqno")

    if run_dir is None or wallet_env is None:
        raise RuntimeError("launcher output did not include run dir and wallet env")
    return process, run_dir, wallet_env


def _stop_process(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=10)


def _build_wallet(wallet_env: Path, output_dir: Path, name: str) -> Path:
    wallet_dir = output_dir / name
    wallet_dir.mkdir(parents=True, exist_ok=True)
    _run_command(
        [
            sys.executable,
            str(SCRIPT_DIR / "run_fift_script.py"),
            "--wallet-env",
            str(wallet_env),
            "--script",
            str(SCRIPT_DIR / "fift" / "new-wallet-save-stateinit.fif"),
            "--cwd",
            str(wallet_dir),
            "--",
            "0",
            name,
        ]
    )
    return wallet_dir / name


def _deploy_wallet(wallet_env: Path, dest_addr: str, init_boc: Path, amount: str) -> None:
    _run_command(
        [
            sys.executable,
            str(SCRIPT_DIR / "wallet_send.py"),
            "--wallet-env",
            str(wallet_env),
            f"--dest-addr={dest_addr}",
            "--auto-seqno",
            "--amount",
            amount,
            "--init-boc",
            str(init_boc),
            "--show-seqno",
            "--wait-mc-advance",
            "--wait-timeout",
            "20",
        ]
    )


def _send_from_wallet(
    wallet_env: Path,
    wallet_base: Path,
    dest_addr: str,
    amount: str,
    comment: str,
) -> None:
    _run_command(
        [
            sys.executable,
            str(SCRIPT_DIR / "wallet_send.py"),
            "--wallet-env",
            str(wallet_env),
            "--wallet-base",
            str(wallet_base),
            f"--dest-addr={dest_addr}",
            "--auto-seqno",
            "--amount",
            amount,
            "--comment",
            comment,
            "--show-seqno",
            "--wait-mc-advance",
            "--wait-timeout",
            "20",
        ]
    )


def _verify_seqno_helper(wallet_env: Path, address: str, expected: int) -> dict[str, object]:
    result = _run_json_command(
        [
            sys.executable,
            str(SCRIPT_DIR / "get_method.py"),
            "--wallet-env",
            str(wallet_env),
            f"--address={address}",
            "--method",
            "85143",
        ]
    )
    if result.get("exit_code") != 0 or result.get("top_number") != expected:
        raise RuntimeError(f"unexpected seqno helper result for {address}: {result}")
    return result


async def _wait_for_active(
    client,
    address: str,
    *,
    label: str,
    wait_timeout: float,
    request_timeout: float,
):
    normalized = await normalize_account_address(client, address, request_timeout=request_timeout)
    deadline = asyncio.get_running_loop().time() + wait_timeout
    while True:
        state = await raw_get_account_state_with_timeout(client, normalized.serialized, request_timeout)
        if state.code and state.data and state.last_transaction_id is not None:
            print(
                f"{label} active:"
                f" balance={state.balance}"
                f" last_lt={state.last_transaction_id.lt}"
            )
            return normalized, state
        if asyncio.get_running_loop().time() >= deadline:
            raise TimeoutError(f"timed out waiting for {label} activation")
        await asyncio.sleep(0.5)


async def _wait_for_seqno(
    client,
    address: str,
    *,
    expected: int,
    label: str,
    wait_timeout: float,
    request_timeout: float,
) -> int:
    deadline = asyncio.get_running_loop().time() + wait_timeout
    while True:
        seqno, _method = await resolve_wallet_seqno(client, address, request_timeout=request_timeout)
        if seqno >= expected:
            print(f"{label} seqno now {seqno}")
            return seqno
        if asyncio.get_running_loop().time() >= deadline:
            raise TimeoutError(f"timed out waiting for {label} seqno {expected}")
        await asyncio.sleep(0.5)


async def _wait_for_recipient_transaction(
    client,
    *,
    address: str,
    previous_lt: int,
    expected_source: str,
    expected_comment: str,
    wait_timeout: float,
    request_timeout: float,
) -> dict[str, object]:
    deadline = asyncio.get_running_loop().time() + wait_timeout
    while True:
        tx = await inspect_latest_transaction(client, address, request_timeout=request_timeout)
        transaction = tx["transaction"]
        transaction_id = transaction["transaction_id"]
        current_lt = transaction_id["lt"]
        in_msg = transaction["in_msg"]
        if (
            isinstance(current_lt, int)
            and current_lt > previous_lt
            and isinstance(in_msg, dict)
            and in_msg.get("source") == expected_source
            and in_msg.get("comment") == expected_comment
        ):
            print(
                "recipient transfer observed:"
                f" lt={current_lt}"
                f" comment={expected_comment!r}"
            )
            return tx
        if asyncio.get_running_loop().time() >= deadline:
            raise TimeoutError("timed out waiting for recipient transfer transaction")
        await asyncio.sleep(0.5)


async def _run(args: argparse.Namespace) -> None:
    process: subprocess.Popen[str] | None = None
    client = None
    try:
        process, run_dir, wallet_env = _launch_network(args)
        artifact_dir = run_dir / "wallet-demo"
        artifact_dir.mkdir(parents=True, exist_ok=True)

        wallet_a_base = _build_wallet(wallet_env, artifact_dir, "wallet-a")
        wallet_b_base = _build_wallet(wallet_env, artifact_dir, "wallet-b")
        wallet_a_raw = wallet_address_from_base(wallet_a_base)
        wallet_b_raw = wallet_address_from_base(wallet_b_base)
        print(f"wallet A raw address: {wallet_a_raw}")
        print(f"wallet B raw address: {wallet_b_raw}")

        _require_process_alive(process, context="wallet deployment setup")
        _deploy_wallet(
            wallet_env,
            wallet_a_raw,
            wallet_a_base.with_name(wallet_a_base.name + "-stateinit.boc"),
            args.deploy_amount,
        )
        _require_process_alive(process, context="wallet A deployment")
        _deploy_wallet(
            wallet_env,
            wallet_b_raw,
            wallet_b_base.with_name(wallet_b_base.name + "-stateinit.boc"),
            args.deploy_amount,
        )

        runtime = _runtime_from_wallet_env(wallet_env)
        client = await build_tonlib_client(
            runtime,
            verbosity=args.verbosity,
            request_timeout=args.request_timeout,
        )

        wallet_a_normalized, wallet_a_state = await _wait_for_active(
            client,
            wallet_a_raw,
            label="wallet A",
            wait_timeout=args.wait_timeout,
            request_timeout=args.request_timeout,
        )
        wallet_b_normalized, wallet_b_state = await _wait_for_active(
            client,
            wallet_b_raw,
            label="wallet B",
            wait_timeout=args.wait_timeout,
            request_timeout=args.request_timeout,
        )

        wallet_a_seqno_before = _verify_seqno_helper(wallet_env, wallet_a_raw, expected=0)
        wallet_b_seqno_before = _verify_seqno_helper(wallet_env, wallet_b_raw, expected=0)

        _require_process_alive(process, context="wallet-to-wallet send")
        _send_from_wallet(
            wallet_env,
            wallet_a_base,
            wallet_b_raw,
            args.transfer_amount,
            args.comment,
        )

        sender_seqno_after = await _wait_for_seqno(
            client,
            wallet_a_raw,
            expected=1,
            label="wallet A",
            wait_timeout=args.wait_timeout,
            request_timeout=args.request_timeout,
        )
        recipient_tx = await _wait_for_recipient_transaction(
            client,
            address=wallet_b_raw,
            previous_lt=wallet_b_state.last_transaction_id.lt,
            expected_source=wallet_a_normalized.serialized,
            expected_comment=args.comment,
            wait_timeout=args.wait_timeout,
            request_timeout=args.request_timeout,
        )
        recipient_tx_from_helper = _run_json_command(
            [
                sys.executable,
                str(SCRIPT_DIR / "inspect_latest_transaction.py"),
                "--wallet-env",
                str(wallet_env),
                f"--address={wallet_b_raw}",
            ]
        )
        wallet_a_seqno_after = _verify_seqno_helper(wallet_env, wallet_a_raw, expected=1)

        final_wallet_a_state = await raw_get_account_state_with_timeout(
            client,
            wallet_a_normalized.serialized,
            args.request_timeout,
        )
        final_wallet_b_state = await raw_get_account_state_with_timeout(
            client,
            wallet_b_normalized.serialized,
            args.request_timeout,
        )

        summary = {
            "run_dir": str(run_dir),
            "wallet_env": str(wallet_env),
            "wallet_a": {
                "raw": wallet_a_raw,
                "serialized": wallet_a_normalized.serialized,
                "deploy_balance": wallet_a_state.balance,
                "deploy_last_lt": wallet_a_state.last_transaction_id.lt,
                "seqno_before_send": wallet_a_seqno_before["top_number"],
                "seqno_after_send": wallet_a_seqno_after["top_number"],
                "seqno_after_send_polled": sender_seqno_after,
                "final_balance": final_wallet_a_state.balance,
                "final_last_lt": (
                    final_wallet_a_state.last_transaction_id.lt
                    if final_wallet_a_state.last_transaction_id is not None
                    else None
                ),
            },
            "wallet_b": {
                "raw": wallet_b_raw,
                "serialized": wallet_b_normalized.serialized,
                "deploy_balance": wallet_b_state.balance,
                "deploy_last_lt": wallet_b_state.last_transaction_id.lt,
                "seqno_before_receive": wallet_b_seqno_before["top_number"],
                "final_balance": final_wallet_b_state.balance,
                "final_last_lt": (
                    final_wallet_b_state.last_transaction_id.lt
                    if final_wallet_b_state.last_transaction_id is not None
                    else None
                ),
            },
            "transfer": {
                "amount": args.transfer_amount,
                "comment": args.comment,
                "recipient_transaction": recipient_tx,
                "recipient_transaction_helper": recipient_tx_from_helper,
            },
        }
        summary_path = run_dir / "wallet-demo-summary.json"
        summary_path.write_text(json.dumps(summary, indent=2) + "\n")
        print(f"summary json: {summary_path}")
        print(json.dumps(summary, indent=2))
    finally:
        if client is not None:
            await client.aclose()
        if process is not None:
            _stop_process(process)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a 2-validator local TON network, deploy two wallets, send a comment transfer, and inspect it",
    )
    parser.add_argument("--repo-root", required=True, help="Path to the TON repo root")
    parser.add_argument("--build", required=True, help="Build directory to run")
    parser.add_argument(
        "--workdir",
        default="tmp/tontester-demo-wallet",
        help="Base working directory for run artifacts",
    )
    parser.add_argument("--base-port", type=int, default=3201, help="First TCP/UDP port to allocate")
    parser.add_argument("--validators", type=int, default=2, help="Number of validator nodes")
    parser.add_argument("--mc-seqno", type=int, default=3, help="Initial masterchain seqno target")
    parser.add_argument("--keep-alive", type=int, default=240, help="Seconds to keep the network alive")
    parser.add_argument(
        "--launch-timeout",
        type=float,
        default=90.0,
        help="Timeout while waiting for the launcher to reach the initial mc seqno",
    )
    parser.add_argument(
        "--wait-timeout",
        type=float,
        default=60.0,
        help="Timeout for wallet activation and post-send transaction observation",
    )
    parser.add_argument("--deploy-amount", default="1", help="Amount sent to each wallet on deploy")
    parser.add_argument("--transfer-amount", default="0.1", help="Amount sent from wallet A to wallet B")
    parser.add_argument("--comment", default="skill demo payment", help="Transfer comment payload")
    parser.add_argument("--verbosity", type=int, default=0, help="Tonlib verbosity level")
    parser.add_argument(
        "--request-timeout",
        type=float,
        default=5.0,
        help="Per-request timeout for tonlib calls made by the verifier",
    )

    args = parser.parse_args()
    args.repo_root = Path(args.repo_root).resolve()
    build_path = Path(args.build)
    if not build_path.is_absolute():
        build_path = (args.repo_root / build_path).resolve()
    args.build = build_path
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
