"""Launch a small local TON network from a single build directory.

Use this for single-build smoke tests, contract deploy flows, and any repro
that does not need mixed honest/probing validator binaries.
"""

from __future__ import annotations

import argparse
import asyncio
import time
from pathlib import Path

from ton_triage_lib import (
    add_tontester_to_syspath,
    load_install,
    new_run_dir,
    resolve_path,
    write_wallet_env,
)


def _node_process(node):
    # tontester exposes no public process handle, so liveness checks use the
    # current name-mangled private attribute.
    return getattr(node, "_Node__process", None)


def _node_is_alive(node) -> bool:
    process = _node_process(node)
    return process is not None and process.returncode is None


async def _run(args: argparse.Namespace) -> None:
    if args.validators < 1:
        raise SystemExit("--validators must be at least 1")

    repo_root = resolve_path(Path.cwd(), args.repo_root)
    add_tontester_to_syspath(repo_root)

    from tontester.network import Network
    from tontester.zerostate import SimplexConsensusConfig

    build_dir = resolve_path(repo_root, args.build)
    workdir_base = resolve_path(repo_root, args.workdir)
    workdir = new_run_dir(workdir_base)
    install = load_install(repo_root, build_dir)

    async with Network(install, workdir) as net:
        # tontester does not expose a public base-port setter; this private
        # field controls the first allocated TCP/UDP port for the run.
        net._port = args.base_port - 1  # pylint: disable=protected-access
        if args.enable_simplex:
            simplex = SimplexConsensusConfig()
            net.config.mc_consensus = simplex
            net.config.shard_consensus = simplex
        if args.activate_spam:
            net.config.spam = True

        dht_nodes = [net.create_dht_node() for _ in range(args.dht_nodes)]
        full_nodes = [net.create_full_node() for _ in range(args.validators)]

        for node in full_nodes:
            node.make_initial_validator()
            for dht in dht_nodes:
                node.announce_to(dht)

        for dht in dht_nodes:
            await dht.run()
        for node in full_nodes:
            await node.run()

        print(f"run dir: {workdir}")
        print(f"repo root: {repo_root}")
        print(f"build dir: {build_dir}")
        print(f"base port: {args.base_port}")
        if args.enable_simplex:
            print(
                "simplex config:"
                f" target_block_rate_ms={simplex.target_block_rate_ms}"
                f" slots_per_leader_window={simplex.slots_per_leader_window}"
                f" first_block_timeout_ms={simplex.first_block_timeout_ms}"
                f" max_leader_window_desync={simplex.max_leader_window_desync}"
            )
        for index, dht in enumerate(dht_nodes, start=1):
            print(f"dht{index} log: {dht.log_path}")
        for index, node in enumerate(full_nodes, start=1):
            print(f"node{index} log: {node.log_path}")

        if args.emit_wallet_env:
            lite_config = workdir / args.liteclient_config
            lite_db = workdir / args.lite_db_dir
            lite_db.mkdir(parents=True, exist_ok=True)
            # tontester has no public serializer for the generated liteserver
            # config, so the helper uses the node's private config object here.
            lite_config.write_text(full_nodes[0]._liteserver_config.to_json())  # pylint: disable=protected-access

            env_file = workdir / "wallet-env.txt"
            write_wallet_env(
                env_file,
                repo_root=repo_root,
                build_dir=build_dir,
                tonlibjson=install.tonlibjson,
                workdir=workdir,
                state_dir=workdir / "state",
                main_wallet_base=workdir / "state" / "main-wallet",
                liteclient_config=lite_config,
                lite_db=lite_db,
                extra={
                    "RUNTIME_NODE": "node1",
                    "RUNTIME_ROLE": "baseline",
                },
            )
            print(f"wallet env: {env_file}")

        deadline = time.time() + args.wait_timeout
        last_error: Exception | None = None
        while True:
            if all(not _node_is_alive(node) for node in full_nodes):
                status = ", ".join(f"node{index}:{_node_process(node).returncode}" for index, node in enumerate(full_nodes, start=1))
                raise RuntimeError(f"all validator nodes exited before mc seqno {args.mc_seqno} was reached: {status}")
            try:
                await net.wait_mc_block(seqno=args.mc_seqno)
                break
            except Exception as exc:
                last_error = exc
                if time.time() >= deadline:
                    message = f"timed out waiting for mc seqno {args.mc_seqno}"
                    if last_error is not None:
                        message += f"; last error: {last_error}"
                    raise TimeoutError(message) from last_error
                await asyncio.sleep(0.5)

        print(f"reached mc seqno >= {args.mc_seqno}")

        keep_alive = args.keep_alive
        if keep_alive is None:
            keep_alive = 300 if args.emit_wallet_env else 0
        if keep_alive > 0:
            print(f"keeping network alive for {keep_alive} seconds")
            await asyncio.sleep(keep_alive)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a simple local TON test network with tontester")
    parser.add_argument("--repo-root", required=True, help="Path to the TON repo root")
    parser.add_argument("--build", required=True, help="Build directory to run")
    parser.add_argument(
        "--workdir",
        default="tmp/tontester-basic",
        help="Base working directory for node data",
    )
    parser.add_argument(
        "--base-port",
        type=int,
        default=2001,
        help="First TCP/UDP port to allocate inside the run",
    )
    parser.add_argument("--validators", type=int, default=1, help="Number of validator nodes")
    parser.add_argument("--dht-nodes", type=int, default=1, help="Number of DHT nodes")
    parser.add_argument("--mc-seqno", type=int, default=3, help="Masterchain seqno target")
    parser.add_argument(
        "--wait-timeout",
        type=int,
        default=60,
        help="Timeout in seconds while waiting for the target seqno",
    )
    parser.add_argument(
        "--keep-alive",
        type=int,
        default=None,
        help="Seconds to keep the network running after the target seqno is reached; defaults to 300 with --emit-wallet-env, else 0",
    )
    parser.add_argument(
        "--emit-wallet-env",
        action="store_true",
        help="Write wallet-env.txt and liteclient.config.json into the run directory",
    )
    parser.add_argument(
        "--liteclient-config",
        default="liteclient.config.json",
        help="Filename for lite-client config in the run directory",
    )
    parser.add_argument(
        "--lite-db-dir",
        default="lite-db",
        help="Lite-client DB directory name under the run directory",
    )
    parser.add_argument(
        "--enable-simplex",
        action="store_true",
        help="Enable simplex consensus in the generated zerostate",
    )
    parser.add_argument(
        "--activate-spam",
        action="store_true",
        help="Include the spammer contract in the generated zerostate",
    )

    args = parser.parse_args()
    try:
        asyncio.run(_run(args))
    except KeyboardInterrupt:
        print("interrupted")


if __name__ == "__main__":
    main()
