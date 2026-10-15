"""Navigation tools (GUI-only): goto function/address in Ghidra UI."""

from __future__ import annotations

from ghidra_rpc.server.main import register_handler


def _handle_goto(ctx, args: dict) -> dict:
    """Navigate the Ghidra GUI to a function or address."""
    binary = args.get("binary", "")
    target = args.get("target", "")
    target_type = args.get("target_type", "function")

    if not target:
        raise ValueError("Missing required argument: target")

    # GUI-only check
    if not hasattr(ctx, "goto"):
        raise RuntimeError(
            "The 'goto' command is only available in GUI mode. "
            "Start the daemon without --headless to use it."
        )

    return ctx.goto(binary, target, target_type)


register_handler("goto", _handle_goto)
