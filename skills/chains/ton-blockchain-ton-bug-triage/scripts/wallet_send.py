"""Build and optionally send a wallet-signed external message.

Use this when you want the helper to resolve wallet seqno, construct the query,
and send it. If you already have a serialized external message BoC, use
`send_boc.py` instead.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import subprocess
from pathlib import Path

from ton_triage_lib import (
    build_tonlib_client,
    get_masterchain_info_with_timeout,
    load_install,
    new_run_dir,
    raw_send_message_with_timeout,
    resolve_path,
    resolve_wallet_seqno,
    runtime_from_args,
    wait_for_mc_advance,
    wallet_address_from_base,
)


def _wallet_base_path(args: argparse.Namespace, runtime) -> Path:
    wallet_base = args.wallet_base
    if wallet_base is None:
        if runtime.main_wallet_base is None:
            raise SystemExit("pass --wallet-base or use --wallet-env/--run-dir with MAIN_WALLET_BASE")
        wallet_base = str(runtime.main_wallet_base)
    return resolve_path(runtime.repo_root, wallet_base)


def _build_query(args: argparse.Namespace, runtime, out_dir: Path, wallet_base_path: Path) -> Path:
    install = load_install(runtime.repo_root, runtime.build_dir)
    wallet_script = runtime.repo_root / "crypto" / "smartcont" / "wallet.fif"
    save_base = out_dir / "wallet-query"

    cmd = [str(install.fift_exe)]
    for include_dir in install.fift_include_dirs:
        cmd += ["-I", str(include_dir)]
    cmd += ["-s", str(wallet_script), str(wallet_base_path), args.dest_addr]
    cmd += [str(args.seqno), args.amount]

    for extra in args.extra or []:
        cmd += ["-x", extra]
    if args.no_bounce:
        cmd.append("-n")
    if args.force_bounce:
        cmd.append("-b")
    if args.body_boc:
        cmd += ["-B", str(resolve_path(Path.cwd(), args.body_boc))]
    if args.comment:
        cmd += ["-C", args.comment]
    if args.init_boc:
        # wallet.fif uses -I for init-state input after the script path; this is
        # unrelated to the Fift include-path -I flags added above.
        cmd += ["-I", str(resolve_path(Path.cwd(), args.init_boc))]
    if args.send_mode is not None:
        cmd += ["-m", str(args.send_mode)]
    cmd.append(str(save_base))

    print("running:", " ".join(cmd))
    print(f"cwd: {out_dir}")
    subprocess.run(cmd, cwd=out_dir, check=True)
    return save_base.with_suffix(".boc")


async def _run(args: argparse.Namespace) -> None:
    runtime = runtime_from_args(args, require_config=(not args.dry_run or args.auto_seqno))
    wallet_base_path = _wallet_base_path(args, runtime)

    if args.auto_seqno:
        client = await build_tonlib_client(runtime, verbosity=args.verbosity, request_timeout=args.request_timeout)
        try:
            wallet_address = wallet_address_from_base(wallet_base_path)
            seqno, method = await resolve_wallet_seqno(
                client,
                wallet_address,
                request_timeout=args.request_timeout,
            )
        finally:
            await client.aclose()

        args.seqno = seqno
        print(f"wallet address: {wallet_address}")
        print(f"auto seqno method: {method}")
        print(f"auto seqno: {args.seqno}")

    if args.out_dir:
        out_dir = resolve_path(Path.cwd(), args.out_dir)
    elif runtime.workdir is not None:
        out_dir = new_run_dir(runtime.workdir / "wallet-send")
    else:
        out_dir = new_run_dir(Path.cwd() / "wallet-send")
    out_dir.mkdir(parents=True, exist_ok=True)

    query_boc = _build_query(args, runtime, out_dir, wallet_base_path)
    print(f"query boc: {query_boc}")
    body = query_boc.read_bytes()
    print(f"query boc sha256: {hashlib.sha256(body).hexdigest()}")

    if args.dry_run:
        return

    client = await build_tonlib_client(runtime, verbosity=args.verbosity, request_timeout=args.request_timeout)
    try:
        before_seqno = None
        if args.show_seqno:
            info = await get_masterchain_info_with_timeout(client, args.request_timeout)
            if info.last is not None:
                before_seqno = info.last.seqno
                print(f"mc seqno before: {before_seqno}")
        elif args.wait_mc_advance:
            info = await get_masterchain_info_with_timeout(client, args.request_timeout)
            if info.last is not None:
                before_seqno = info.last.seqno

        await raw_send_message_with_timeout(client, body, args.request_timeout)
        print("raw_send_message: ok")

        if args.wait_mc_advance and before_seqno is not None:
            advanced = await wait_for_mc_advance(
                client,
                before_seqno=before_seqno,
                wait_timeout=args.wait_timeout,
                request_timeout=args.request_timeout,
            )
            print(f"mc seqno advanced to: {advanced}")
        elif args.wait_seconds > 0:
            await asyncio.sleep(args.wait_seconds)

        if args.show_seqno:
            info = await get_masterchain_info_with_timeout(client, args.request_timeout)
            if info.last is not None:
                print(f"mc seqno after: {info.last.seqno}")
    finally:
        await client.aclose()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build and optionally send a wallet-signed transfer or deployment message"
    )
    parser.add_argument("--wallet-env", help="Path to wallet-env.txt emitted by the network runner")
    parser.add_argument("--run-dir", help="Run directory containing wallet-env.txt")
    parser.add_argument("--repo-root", help="Path to the TON repo root")
    parser.add_argument("--build", help="Build directory containing create-state and tonlibjson")
    parser.add_argument("--config", help="Lite-client config JSON path")
    parser.add_argument("--state-dir", help="Optional state dir for helper defaults")
    parser.add_argument(
        "--wallet-base",
        help="Wallet file base without .pk/.addr; defaults to MAIN_WALLET_BASE from wallet-env",
    )
    parser.add_argument(
        "--dest-addr",
        required=True,
        help="Destination account address; use --dest-addr=<value> for raw forms like -1:...",
    )
    parser.add_argument("--seqno", type=int, help="Wallet seqno to sign with")
    parser.add_argument(
        "--auto-seqno",
        action="store_true",
        help="Resolve the source wallet seqno with tonlib before signing",
    )
    parser.add_argument("--amount", required=True, help="Amount accepted by wallet.fif, e.g. 0.1")
    parser.add_argument("--body-boc", help="Optional body BOC for the internal message")
    parser.add_argument("--init-boc", help="Optional StateInit BOC for deployment")
    parser.add_argument("--comment", help="Optional wallet comment payload")
    parser.add_argument(
        "--extra",
        action="append",
        help="Extra currency amount in <amount>*<currency-id> form; repeat as needed",
    )
    parser.add_argument("--send-mode", type=int, help="SENDRAWMSG mode")
    parser.add_argument("--no-bounce", action="store_true", help="Clear the bounce flag")
    parser.add_argument("--force-bounce", action="store_true", help="Force the bounce flag")
    parser.add_argument("--out-dir", help="Directory for generated query artifacts")
    parser.add_argument("--dry-run", action="store_true", help="Build the query but do not send it")
    parser.add_argument(
        "--wait-seconds",
        type=float,
        default=0.0,
        help="Optional delay after send before a final seqno read",
    )
    parser.add_argument(
        "--wait-mc-advance",
        action="store_true",
        help="Wait until masterchain seqno advances after the send; useful as a liveness hint, not proof of inclusion",
    )
    parser.add_argument(
        "--wait-timeout",
        type=float,
        default=10.0,
        help="Timeout for --wait-mc-advance",
    )
    parser.add_argument(
        "--request-timeout",
        type=float,
        default=5.0,
        help="Per-request timeout for tonlib calls such as getMasterchainInfo, seqno lookup, and raw_send_message",
    )
    parser.add_argument("--verbosity", type=int, default=0, help="Tonlib verbosity level")
    parser.add_argument("--show-seqno", action="store_true", help="Print masterchain seqno before and after send")

    args = parser.parse_args()
    if args.no_bounce and args.force_bounce:
        raise SystemExit("cannot set both --no-bounce and --force-bounce")
    if args.auto_seqno and args.seqno is not None:
        raise SystemExit("pass either --seqno or --auto-seqno, not both")
    if not args.auto_seqno and args.seqno is None:
        raise SystemExit("pass either --seqno or --auto-seqno")
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
