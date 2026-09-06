"""Fetch the latest account transaction and export useful artifacts.

Use this after deploy or trigger messages when you need transaction details,
decoded comments, or raw BoCs for deeper inspection.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from ton_triage_lib import (
    build_tonlib_client,
    normalize_account_address,
    raw_get_account_state_with_timeout,
    resolve_path,
    runtime_from_args,
    tonlib_call,
)


def _message_data_type(msg_data) -> str:
    data = msg_data.to_dict()
    raw_type = data.get("@type", msg_data.__class__.__name__)
    return str(raw_type)


def _decode_comment_body(body: bytes) -> str | None:
    if len(body) < 4 or body[:4] != b"\x00\x00\x00\x00":
        return None
    payload = body[4:].rstrip(b"\x00")
    if not payload:
        return ""
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError:
        return None


def _write_bytes_artifact(out_dir: Path | None, filename: str, data: bytes) -> str | None:
    if out_dir is None or not data:
        return None
    path = out_dir / filename
    path.write_bytes(data)
    return str(path)


def _message_data_to_json(
    msg_data,
    *,
    out_dir: Path | None,
    artifact_prefix: str,
) -> dict[str, object]:
    result: dict[str, object] = {"type": _message_data_type(msg_data)}

    text = getattr(msg_data, "text", None)
    if isinstance(text, bytes):
        result["text_hex"] = text.hex()
        try:
            result["text_utf8"] = text.decode("utf-8")
        except UnicodeDecodeError:
            pass
        else:
            result["comment"] = result["text_utf8"]

    body = getattr(msg_data, "body", None)
    if isinstance(body, bytes):
        result["body_len"] = len(body)
        result["body_hex"] = body.hex()
        body_file = _write_bytes_artifact(out_dir, f"{artifact_prefix}-body.boc", body)
        if body_file is not None:
            result["body_file"] = body_file
        comment = _decode_comment_body(body)
        if comment is not None:
            result["comment"] = comment

    init_state = getattr(msg_data, "init_state", None)
    if isinstance(init_state, bytes):
        result["init_state_len"] = len(init_state)
        init_state_file = _write_bytes_artifact(out_dir, f"{artifact_prefix}-init-state.boc", init_state)
        if init_state_file is not None:
            result["init_state_file"] = init_state_file

    return result


def _account_address_value(account_address) -> str | None:
    if account_address is None:
        return None
    return account_address.account_address


def _message_to_json(
    message,
    *,
    out_dir: Path | None,
    artifact_prefix: str,
) -> dict[str, object] | None:
    if message is None:
        return None

    result: dict[str, object] = {
        "hash_hex": message.hash.hex(),
        "source": _account_address_value(message.source),
        "destination": _account_address_value(message.destination),
        "value": message.value,
        "fwd_fee": message.fwd_fee,
        "ihr_fee": message.ihr_fee,
        "created_lt": message.created_lt,
        "body_hash_hex": message.body_hash.hex(),
    }

    if message.msg_data is not None:
        result["msg_data"] = _message_data_to_json(
            message.msg_data,
            out_dir=out_dir,
            artifact_prefix=artifact_prefix,
        )
        comment = result["msg_data"].get("comment")
        if comment is not None:
            result["comment"] = comment

    return result


def _transaction_to_json(transaction, *, out_dir: Path | None) -> dict[str, object]:
    transaction_id = transaction.transaction_id
    result = {
        "address": _account_address_value(transaction.address),
        "utime": transaction.utime,
        "transaction_id": {
            "lt": transaction_id.lt if transaction_id is not None else None,
            "hash_hex": transaction_id.hash.hex() if transaction_id is not None else None,
        },
        "fee": transaction.fee,
        "storage_fee": transaction.storage_fee,
        "other_fee": transaction.other_fee,
        "data_len": len(transaction.data),
        "in_msg": _message_to_json(
            transaction.in_msg,
            out_dir=out_dir,
            artifact_prefix="in-msg",
        ),
        "out_msgs": [
            _message_to_json(
                message,
                out_dir=out_dir,
                artifact_prefix=f"out-msg-{index}",
            )
            for index, message in enumerate(transaction.out_msgs, start=1)
        ],
    }
    if isinstance(transaction.data, bytes):
        result["data_hex"] = transaction.data.hex()
        data_file = _write_bytes_artifact(out_dir, "transaction-data.boc", transaction.data)
        if data_file is not None:
            result["data_file"] = data_file
    return result


async def inspect_latest_transaction(
    client,
    address: str,
    *,
    request_timeout: float = 5.0,
    out_dir: Path | None = None,
) -> dict[str, object]:
    normalized = await normalize_account_address(client, address, request_timeout=request_timeout)
    state = await raw_get_account_state_with_timeout(
        client,
        normalized.serialized,
        request_timeout,
    )
    if state.last_transaction_id is None:
        raise RuntimeError(f"account {normalized.raw} has no transactions yet")

    transactions = await tonlib_call(
        client.raw_get_transactions(
            normalized.serialized,
            state.last_transaction_id.lt,
            state.last_transaction_id.hash,
        ),
        timeout=request_timeout,
        label="raw_get_transactions()",
    )

    latest = None
    for transaction in transactions.transactions:
        transaction_id = transaction.transaction_id
        if transaction_id is None:
            continue
        if (
            transaction_id.lt == state.last_transaction_id.lt
            and transaction_id.hash == state.last_transaction_id.hash
        ):
            latest = transaction
            break

    if latest is None:
        raise RuntimeError(
            "latest transaction id was not present in raw_get_transactions() result"
        )

    return {
        "address_input": address,
        "address_serialized": normalized.serialized,
        "address_raw": normalized.raw,
        "balance": state.balance,
        "last_transaction_id": {
            "lt": state.last_transaction_id.lt,
            "hash_hex": state.last_transaction_id.hash.hex(),
        },
        "transaction": _transaction_to_json(latest, out_dir=out_dir),
    }


async def _run(args: argparse.Namespace) -> None:
    runtime = runtime_from_args(args)
    out_dir = resolve_path(Path.cwd(), args.out_dir) if args.out_dir else None
    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
    client = await build_tonlib_client(runtime, verbosity=args.verbosity, request_timeout=args.request_timeout)
    try:
        result = await inspect_latest_transaction(
            client,
            args.address,
            request_timeout=args.request_timeout,
            out_dir=out_dir,
        )
    finally:
        await client.aclose()

    if out_dir is not None:
        result["out_dir"] = str(out_dir)
        (out_dir / "latest-transaction.json").write_text(json.dumps(result, indent=2) + "\n")

    print(json.dumps(result, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch the latest account transaction through tonlib")
    parser.add_argument("--wallet-env", help="Path to wallet-env.txt emitted by the network runner")
    parser.add_argument("--run-dir", help="Run directory containing wallet-env.txt")
    parser.add_argument("--repo-root", help="Path to the TON repo root")
    parser.add_argument("--build", help="Build directory containing tonlibjson")
    parser.add_argument("--config", help="Lite-client config JSON path")
    parser.add_argument("--state-dir", help="Optional state dir for helper defaults")
    parser.add_argument(
        "--address",
        required=True,
        help="TON account address accepted by tonlib; use --address=<value> for raw forms like -1:...",
    )
    parser.add_argument("--out-dir", help="Optional output directory for raw transaction and message artifacts")
    parser.add_argument("--verbosity", type=int, default=0, help="Tonlib verbosity level")
    parser.add_argument(
        "--request-timeout",
        type=float,
        default=5.0,
        help="Per-request timeout for tonlib address, state, and transaction queries",
    )

    args = parser.parse_args()
    asyncio.run(_run(args))


if __name__ == "__main__":
    main()
