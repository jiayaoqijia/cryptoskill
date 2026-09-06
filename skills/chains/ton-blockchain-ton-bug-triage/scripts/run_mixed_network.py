"""Launch a mixed-build local TON network with baseline and probing nodes.

Use this for Workflow B experiments where honest and patched validator binaries
must coexist in one tontester run.
"""

from __future__ import annotations

import argparse
import asyncio
import re
import time
from dataclasses import dataclass
from pathlib import Path

from ton_triage_lib import (
    add_tontester_to_syspath,
    load_install,
    new_run_dir,
    resolve_path,
    write_wallet_env,
)


@dataclass(frozen=True)
class LogSpec:
    target: str
    pattern: str


def _probing_env_from_args(
    probing_target_addr: str | None,
    raw_assignments: list[str],
) -> dict[str, str]:
    env: dict[str, str] = {}
    if probing_target_addr:
        env["TON_PROBING_TARGET_ADDR"] = probing_target_addr
    for raw in raw_assignments:
        key, sep, value = raw.partition("=")
        if not sep:
            raise SystemExit(f"invalid --probing-env assignment {raw!r}; expected KEY=VALUE")
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            raise SystemExit(f"invalid probing env key {key!r}")
        env[key] = value
    return env


def _parse_log_spec(raw: str) -> LogSpec:
    selector, sep, pattern = raw.partition(":")
    if sep and (selector == "any" or re.fullmatch(r"node\d+", selector)):
        target = selector
    elif sep and (selector == "any" or selector.startswith("node")):
        raise SystemExit(f"invalid log selector {selector!r}; expected any or nodeN")
    else:
        target = "any"
        pattern = raw
    if not pattern:
        raise SystemExit(f"invalid log selector: {raw!r}")
    return LogSpec(target=target, pattern=pattern)


def _parse_node_name(raw: str, node_count: int) -> str:
    if not re.fullmatch(r"node\d+", raw):
        raise SystemExit(f"invalid node name {raw!r}; expected node1, node2, ...")
    index = int(raw[4:])
    if index < 1 or index > node_count:
        raise SystemExit(f"node {raw!r} is out of range for {node_count} validator nodes")
    return raw


def _validate_log_specs(specs: list[LogSpec], node_count: int) -> None:
    for spec in specs:
        if spec.target != "any":
            _parse_node_name(spec.target, node_count)


def _node_process(node):
    # tontester exposes no public process handle, so liveness checks use the
    # current name-mangled private attribute.
    return getattr(node, "_Node__process", None)


def _node_is_alive(node) -> bool:
    process = _node_process(node)
    return process is not None and process.returncode is None


def _node_status_line(name: str, node) -> str:
    process = _node_process(node)
    if process is None:
        return f"{name}: not-started"
    if process.returncode is None:
        return f"{name}: alive"
    return f"{name}: exited({process.returncode})"


def _poll_log_updates(
    node_logs: dict[str, Path],
    offsets: dict[str, int],
    tails: dict[str, str],
    tail_size: int,
) -> dict[str, str]:
    updates: dict[str, str] = {}
    for name, path in node_logs.items():
        if not path.exists():
            updates[name] = ""
            continue
        size = path.stat().st_size
        if size < offsets[name]:
            offsets[name] = 0
            tails[name] = ""
        with path.open("rb") as handle:
            handle.seek(offsets[name])
            chunk = handle.read()
        offsets[name] = size
        text = chunk.decode("utf-8", errors="ignore")
        combined = tails[name] + text
        tails[name] = combined[-tail_size:]
        updates[name] = combined
    return updates


def _match_log_spec(spec: LogSpec, updates: dict[str, str]) -> bool:
    if spec.target == "any":
        return any(spec.pattern in text for text in updates.values())
    return spec.pattern in updates.get(spec.target, "")


async def _wait_for_log_conditions(
    *,
    node_map: dict[str, object],
    node_logs: dict[str, Path],
    success_specs: list[LogSpec],
    failure_specs: list[LogSpec],
    require_alive: list[str],
    require_dead: list[str],
    wait_timeout: float,
    poll_interval: float,
) -> None:
    deadline = time.time() + wait_timeout
    offsets = {name: 0 for name in node_logs}
    max_pattern = max((len(spec.pattern) for spec in success_specs + failure_specs), default=1)
    tails = {name: "" for name in node_logs}
    matched_success = [False] * len(success_specs)
    tail_size = max(max_pattern + 128, 256)

    while True:
        updates = _poll_log_updates(node_logs, offsets, tails, tail_size)

        for spec in failure_specs:
            if _match_log_spec(spec, updates):
                raise RuntimeError(f"observed failure marker {spec.target}:{spec.pattern}")

        for index, spec in enumerate(success_specs):
            if not matched_success[index] and _match_log_spec(spec, updates):
                matched_success[index] = True

        dead_ready = all(not _node_is_alive(node_map[name]) for name in require_dead)
        success_ready = all(matched_success) if success_specs else True

        if require_dead and dead_ready and success_ready:
            return

        if success_specs and success_ready and not require_dead:
            return

        for name in require_alive:
            if not _node_is_alive(node_map[name]):
                raise RuntimeError(f"{name} died before the success condition was reached")

        if time.time() >= deadline:
            status = ", ".join(_node_status_line(name, node_map[name]) for name in sorted(node_map))
            raise TimeoutError(f"timed out waiting for log conditions; node status: {status}")

        await asyncio.sleep(poll_interval)


async def _wait_for_seqno_or_fail(
    *,
    reference_node,
    target_seqno: int,
    node_map: dict[str, object],
    node_logs: dict[str, Path],
    failure_specs: list[LogSpec],
    require_alive: list[str],
    wait_timeout: float,
    poll_interval: float,
) -> None:
    deadline = time.time() + wait_timeout
    offsets = {name: 0 for name in node_logs}
    max_pattern = max((len(spec.pattern) for spec in failure_specs), default=1)
    tails = {name: "" for name in node_logs}
    tail_size = max(max_pattern + 128, 256)
    client = await reference_node.tonlib_client()
    last_error: Exception | None = None

    while True:
        updates = _poll_log_updates(node_logs, offsets, tails, tail_size)

        if not _node_is_alive(reference_node):
            status = ", ".join(_node_status_line(name, node_map[name]) for name in sorted(node_map))
            raise RuntimeError(f"reference node died before masterchain seqno {target_seqno} was reached; {status}")

        for name in require_alive:
            if not _node_is_alive(node_map[name]):
                raise RuntimeError(f"{name} died before masterchain seqno {target_seqno} was reached")

        for spec in failure_specs:
            if _match_log_spec(spec, updates):
                raise RuntimeError(f"observed failure marker {spec.target}:{spec.pattern}")

        remaining = deadline - time.time()
        if remaining <= 0:
            status = ", ".join(_node_status_line(name, node_map[name]) for name in sorted(node_map))
            message = f"timed out waiting for mc seqno {target_seqno}; node status: {status}"
            if last_error is not None:
                message += f"; last tonlib error: {last_error}"
            raise TimeoutError(message)

        request_timeout = min(max(poll_interval * 2, 1.0), remaining)
        request = asyncio.create_task(client.get_masterchain_info())
        try:
            info = await asyncio.wait_for(request, timeout=request_timeout)
            if info.last is not None and info.last.seqno >= target_seqno:
                return
            last_error = None
        except asyncio.TimeoutError:
            request.cancel()
            try:
                await request
            except asyncio.CancelledError:
                pass
            last_error = TimeoutError(f"get_masterchain_info() timed out after {request_timeout:.1f}s")
        except Exception as exc:
            last_error = exc

        await asyncio.sleep(poll_interval)


def _simplex_config(args: argparse.Namespace, SimplexConsensusConfig):
    return SimplexConsensusConfig(
        target_block_rate_ms=args.simplex_target_block_rate_ms,
        slots_per_leader_window=args.simplex_slots_per_leader_window,
        first_block_timeout_ms=args.simplex_first_block_timeout_ms,
        max_leader_window_desync=args.simplex_max_leader_window_desync,
    )


async def _run(args: argparse.Namespace) -> None:
    total_nodes = args.normal_nodes + args.probing_nodes
    if total_nodes < 1:
        raise SystemExit("the mixed network needs at least one full node")
    if args.probing_nodes < 1 and (args.probing_env or args.probing_target_addr):
        raise SystemExit("--probing-env/--probing-target-addr require at least one probing node")

    success_specs = [_parse_log_spec(spec) for spec in args.success_log]
    failure_specs = [_parse_log_spec(spec) for spec in args.failure_log]
    _validate_log_specs(success_specs, total_nodes)
    _validate_log_specs(failure_specs, total_nodes)
    require_alive = [_parse_node_name(name, total_nodes) for name in args.require_node_alive]
    require_dead = [_parse_node_name(name, total_nodes) for name in args.require_node_dead]

    repo_root = resolve_path(Path.cwd(), args.repo_root)
    add_tontester_to_syspath(repo_root)

    from tontester.network import Network
    from tontester.zerostate import SimplexConsensusConfig

    baseline_build_dir = resolve_path(repo_root, args.build)
    probing_build_dir = resolve_path(repo_root, args.probing_build)
    workdir_base = resolve_path(repo_root, args.workdir)
    workdir = new_run_dir(workdir_base)

    baseline = load_install(repo_root, baseline_build_dir)

    async with Network(baseline, workdir) as net:
        # tontester does not expose a public base-port setter; this private
        # field controls the first allocated TCP/UDP port for the run.
        net._port = args.base_port - 1  # pylint: disable=protected-access
        if args.enable_simplex:
            simplex = _simplex_config(args, SimplexConsensusConfig)
            net.config.mc_consensus = simplex
            net.config.shard_consensus = simplex
        if args.activate_spam:
            net.config.spam = True

        dht_nodes = [net.create_dht_node() for _ in range(args.dht_nodes)]
        full_nodes = []
        full_node_installs = []
        full_node_roles = []
        for _ in range(args.normal_nodes):
            full_nodes.append(net.create_full_node())
            full_node_installs.append(baseline)
            full_node_roles.append("baseline")

        if args.probing_nodes > 0:
            probing = load_install(repo_root, probing_build_dir)
            probing_env = _probing_env_from_args(args.probing_target_addr, args.probing_env)
            for _ in range(args.probing_nodes):
                full_nodes.append(
                    net.create_full_node(
                    install=probing,
                    env=probing_env,
                )
                )
                full_node_installs.append(probing)
                full_node_roles.append("probing")

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
        print(f"baseline build: {baseline_build_dir}")
        print(f"probing build: {probing_build_dir}")
        print(f"base port: {args.base_port}")
        if args.enable_simplex:
            print(
                "simplex config:"
                f" target_block_rate_ms={simplex.target_block_rate_ms}"
                f" slots_per_leader_window={simplex.slots_per_leader_window}"
                f" first_block_timeout_ms={simplex.first_block_timeout_ms}"
                f" max_leader_window_desync={simplex.max_leader_window_desync}"
            )
        active_probing_env = _probing_env_from_args(args.probing_target_addr, args.probing_env)
        if active_probing_env:
            summary = ", ".join(f"{key}={value}" for key, value in sorted(active_probing_env.items()))
            print(f"probing env: {summary}")
        for index, dht in enumerate(dht_nodes, start=1):
            print(f"dht{index} log: {dht.log_path}")
        node_logs = {}
        node_map = {}
        for index, node in enumerate(full_nodes, start=1):
            name = f"node{index}"
            node_logs[name] = node.log_path
            node_map[name] = node
            print(f"{name} log: {node.log_path}")

        if args.emit_wallet_env:
            lite_config = workdir / args.liteclient_config
            lite_db = workdir / args.lite_db_dir
            lite_db.mkdir(parents=True, exist_ok=True)
            # tontester has no public serializer for the generated liteserver
            # config, so the helper uses the node's private config object here.
            lite_config.write_text(full_nodes[0]._liteserver_config.to_json())  # pylint: disable=protected-access
            env_install = full_node_installs[0]
            env_role = full_node_roles[0]

            env_file = workdir / "wallet-env.txt"
            write_wallet_env(
                env_file,
                repo_root=repo_root,
                build_dir=env_install.build_dir,
                tonlibjson=env_install.tonlibjson,
                workdir=workdir,
                state_dir=workdir / "state",
                main_wallet_base=workdir / "state" / "main-wallet",
                liteclient_config=lite_config,
                lite_db=lite_db,
                extra={
                    "RUNTIME_NODE": "node1",
                    "RUNTIME_ROLE": env_role,
                },
            )
            print(f"wallet env: {env_file}")

        if success_specs or require_dead:
            await _wait_for_log_conditions(
                node_map=node_map,
                node_logs=node_logs,
                success_specs=success_specs,
                failure_specs=failure_specs,
                require_alive=require_alive,
                require_dead=require_dead,
                wait_timeout=args.wait_timeout,
                poll_interval=args.poll_interval,
            )
            print("success condition reached")
        else:
            await _wait_for_seqno_or_fail(
                reference_node=full_nodes[0],
                target_seqno=args.mc_seqno,
                node_map=node_map,
                node_logs=node_logs,
                failure_specs=failure_specs,
                require_alive=require_alive,
                wait_timeout=args.wait_timeout,
                poll_interval=args.poll_interval,
            )
            print(f"reached mc seqno >= {args.mc_seqno}")

        keep_alive = args.keep_alive
        if keep_alive is None:
            keep_alive = 300 if args.emit_wallet_env else 0
        if keep_alive > 0:
            print(f"keeping network alive for {keep_alive} seconds")
            await asyncio.sleep(keep_alive)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a mixed-build local TON network with tontester",
    )
    parser.add_argument("--repo-root", required=True, help="Path to the TON repo root")
    parser.add_argument("--build", default="build", help="Baseline build directory")
    parser.add_argument(
        "--probing-build",
        default="build-probing",
        help="Probing build directory (can be the same as --build)",
    )
    parser.add_argument(
        "--workdir",
        default="tmp/tontester-mixed-builds",
        help="Base working directory for node data",
    )
    parser.add_argument(
        "--base-port",
        type=int,
        default=2001,
        help="First TCP/UDP port to allocate inside the run",
    )
    parser.add_argument("--normal-nodes", type=int, default=3, help="Number of baseline full nodes")
    parser.add_argument("--probing-nodes", type=int, default=1, help="Number of probing full nodes")
    parser.add_argument("--dht-nodes", type=int, default=1, help="Number of DHT nodes")
    parser.add_argument("--mc-seqno", type=int, default=100, help="Masterchain seqno target")
    parser.add_argument(
        "--wait-timeout",
        type=int,
        default=120,
        help="Timeout in seconds while waiting for seqno or log-based success conditions",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=0.2,
        help="Polling interval for log-based success conditions",
    )
    parser.add_argument(
        "--success-log",
        action="append",
        default=[],
        metavar="NODE:TEXT",
        help="Stop successfully when this substring appears; use node1:..., node2:..., or any:...",
    )
    parser.add_argument(
        "--failure-log",
        action="append",
        default=[],
        metavar="NODE:TEXT",
        help="Fail immediately when this substring appears; use node1:..., node2:..., or any:...",
    )
    parser.add_argument(
        "--require-node-alive",
        action="append",
        default=[],
        metavar="NODE",
        help="Fail if this node dies before success; repeat as needed",
    )
    parser.add_argument(
        "--require-node-dead",
        action="append",
        default=[],
        metavar="NODE",
        help="Require this node to die before success; repeat as needed",
    )
    parser.add_argument(
        "--enable-simplex",
        action="store_true",
        help="Enable simplex (new consensus) in genesis config (config param 30).",
    )
    parser.add_argument(
        "--simplex-target-block-rate-ms",
        type=int,
        default=1000,
        help="Simplex target_block_rate_ms; used with --enable-simplex",
    )
    parser.add_argument(
        "--simplex-slots-per-leader-window",
        type=int,
        default=4,
        help="Simplex slots_per_leader_window; used with --enable-simplex",
    )
    parser.add_argument(
        "--simplex-first-block-timeout-ms",
        type=int,
        default=1000,
        help="Simplex first_block_timeout_ms; used with --enable-simplex",
    )
    parser.add_argument(
        "--simplex-max-leader-window-desync",
        type=int,
        default=2,
        help="Simplex max_leader_window_desync; used with --enable-simplex",
    )
    parser.add_argument(
        "--activate-spam",
        action="store_true",
        help="Include the spammer smart contract in the generated zerostate",
    )
    parser.add_argument(
        "--probing-target-addr",
        dest="probing_target_addr",
        help="Target account address (base64 or 0:HEX) used by probing logic",
    )
    parser.add_argument(
        "--keep-alive",
        type=int,
        default=None,
        help="Seconds to keep the network running after reaching the success condition; defaults to 300 with --emit-wallet-env, else 0",
    )
    parser.add_argument(
        "--probing-env",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Extra environment variable to pass to probing nodes; repeat as needed",
    )
    parser.add_argument(
        "--liteclient-config",
        default="liteclient.config.json",
        help="Filename for liteclient config in the run directory",
    )
    parser.add_argument(
        "--emit-wallet-env",
        action="store_true",
        help="Write wallet-env.txt and liteclient.config.json in the run workdir",
    )
    parser.add_argument(
        "--lite-db-dir",
        default="lite-db",
        help="Lite-client DB directory name (under workdir)",
    )

    args = parser.parse_args()
    try:
        asyncio.run(_run(args))
    except KeyboardInterrupt:
        print("interrupted")


if __name__ == "__main__":
    main()
