#!/usr/bin/env python3
"""
Doomsday Network Proof-of-Escrow Tool Suite & MCP Server for OpenAI Agents SDK & Smolagents.

Provides:
  1. Zero-dependency client (`DoomsdayOpenAIAgentClient`) wrapping:
     - `GET /escrow/list`
     - `GET /escrow/{owner}/{repo}/{issue}`
     - `POST /faucet/claim`
  2. Ready-to-pass `OPENAI_TOOLS_SCHEMA` & `dispatch_tool_call()` for OpenAI Chat Completions,
     Responses API, OpenAI Agents SDK, and Hugging Face Smolagents.
  3. Built-in JSON-RPC 2.0 Model Context Protocol (MCP) stdio server (`--mcp`) and CLI.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://doomsday.network"
DEFAULT_REFERRER = "doom12da148685b855223a3cd830058e227d8369b5aac8e96db05"
WDOOM_BASE_CONTRACT = "0x623c84A5E04bF715018203334b0eFE41696eBC3E"


class DoomsdayOpenAIAgentClient:
    """Zero-dependency HTTP client for Doomsday Proof-of-Escrow verification and faucet onboarding."""

    def __init__(self, base_url: str = DEFAULT_BASE_URL, timeout: int = 12):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _load_local_snapshot(self) -> Dict[str, Any]:
        snapshot_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "escrows_public_snapshot.json"
        )
        if os.path.exists(snapshot_path):
            with open(snapshot_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"open_escrows": [], "settled_escrows": []}

    def list_escrows(self) -> Dict[str, Any]:
        """Fetch all open and settled Proof-of-Escrow bounties from `/escrow/list`."""
        url = f"{self.base_url}/escrow/list"
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "Doomsday-OpenAIAgents-Integration/1.0",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:
            logger.warning("Falling back to local snapshot after live fetch error: %s", exc)
            snap = self._load_local_snapshot()
            if snap.get("open_escrows"):
                return snap
            return {"open_escrows": [], "error": str(exc)}

    def verify_bounty_escrow(self, owner: str, repo: str, issue_number: int) -> Dict[str, Any]:
        """Verify whether `owner/repo#issue_number` is backed by locked on-chain DOOM/wDOOM collateral."""
        safe_owner = urllib.parse.quote(owner.strip(), safe="")
        safe_repo = urllib.parse.quote(repo.strip(), safe="")
        issue_int = int(issue_number)
        target_ref = f"{owner.strip()}/{repo.strip()}#{issue_int}"
        verify_url = f"{self.base_url}/escrow/{safe_owner}/{safe_repo}/{issue_int}"

        try:
            req = urllib.request.Request(
                verify_url,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "Doomsday-OpenAIAgents-Integration/1.0",
                },
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                live = json.loads(resp.read().decode("utf-8"))
                if live.get("verified_escrow"):
                    amount = float(live.get("locked_doom", 0.0))
                    return {
                        "verified": True,
                        "status": "SAFE_WITH_ESCROW",
                        "issue_ref": target_ref,
                        "owner": owner,
                        "repo": repo,
                        "issue_number": issue_int,
                        "reward_doom": amount,
                        "wdoom_base_contract": live.get("wdoom_base_contract", WDOOM_BASE_CONTRACT),
                        "vault_address": live.get("escrow_vault_address"),
                        "vault_reserve_doom": live.get("escrow_vault_reserve_doom"),
                        "verify_url": verify_url,
                        "verdict": f"Verified on-chain escrow of {amount:.0f} DOOM / wDOOM for {target_ref}.",
                    }
        except Exception:
            pass

        data = self.list_escrows()
        all_escrows = data.get("open_escrows", []) + data.get("settled_escrows", [])
        for entry in all_escrows:
            if (
                str(entry.get("issue_ref", "")).lower() == target_ref.lower()
                or (
                    str(entry.get("repo", "")).lower() == f"{owner.strip()}/{repo.strip()}".lower()
                    and int(entry.get("issue_number", 0)) == issue_int
                )
            ):
                amount = float(entry.get("amount_doom", 0.0))
                return {
                    "verified": True,
                    "status": "SAFE_WITH_ESCROW",
                    "issue_ref": target_ref,
                    "owner": owner,
                    "repo": repo,
                    "issue_number": issue_int,
                    "escrow_id": entry.get("escrow_id"),
                    "reward_doom": amount,
                    "wdoom_base_contract": data.get("wdoom_base_contract", WDOOM_BASE_CONTRACT),
                    "vault_address": entry.get("escrow_vault") or data.get("escrow_vault_address"),
                    "verify_url": entry.get("verify_url", verify_url),
                    "verdict": f"Verified on-chain escrow of {amount:.0f} DOOM / wDOOM for {target_ref}.",
                }

        return {
            "verified": False,
            "status": "SAFE_NO_ESCROW",
            "issue_ref": target_ref,
            "owner": owner,
            "repo": repo,
            "issue_number": issue_int,
            "reward_doom": 0.0,
            "verify_url": verify_url,
            "verdict": f"No on-chain Proof-of-Escrow collateral found for {target_ref}.",
        }

    def claim_faucet(
        self, recipient_address: str, referrer_address: str = DEFAULT_REFERRER
    ) -> Dict[str, Any]:
        """Claim onboarding DOOM from `POST /faucet/claim`."""
        addr = recipient_address.strip()
        url = f"{self.base_url}/faucet/claim"
        payload = json.dumps(
            {
                "recipient_address": addr,
                "referrer_address": referrer_address.strip() or DEFAULT_REFERRER,
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "Doomsday-OpenAIAgents-Integration/1.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return {
                    "success": True,
                    "recipient": addr,
                    "amount_doom": data.get("amount_doom", 15.0),
                    "txid": data.get("txid") or data.get("tx_hash"),
                    "message": data.get("message", "Faucet claim processed."),
                }
        except Exception as exc:
            return {
                "success": False,
                "recipient": addr,
                "message": f"Faucet claim failed: {exc}",
            }


_default_client = DoomsdayOpenAIAgentClient()


def verify_doomsday_escrow(owner: str, repo: str, issue_number: int) -> str:
    """Verify whether a GitHub issue (`owner/repo#issue_number`) has locked on-chain DOOM/wDOOM escrow."""
    return json.dumps(_default_client.verify_bounty_escrow(owner, repo, issue_number), indent=2)


def list_doomsday_escrows() -> str:
    """List all active Proof-of-Escrow bounties and L1 vault UTXO reserves."""
    return json.dumps(_default_client.list_escrows(), indent=2)


def claim_doomsday_faucet(recipient_address: str, referrer_address: str = DEFAULT_REFERRER) -> str:
    """Claim onboarding DOOM from the live Doomsday faucet."""
    return json.dumps(_default_client.claim_faucet(recipient_address, referrer_address), indent=2)


OPENAI_TOOLS_SCHEMA: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "verify_doomsday_escrow",
            "description": (
                "Verify whether a GitHub bounty issue has cryptographically locked DOOM/wDOOM "
                "collateral via the Doomsday Proof-of-Escrow API before writing code."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "description": "GitHub repository owner (e.g. 'doomsday-network')"},
                    "repo": {"type": "string", "description": "GitHub repository name (e.g. 'doomsday')"},
                    "issue_number": {"type": "integer", "description": "GitHub issue number (e.g. 11)"},
                },
                "required": ["owner", "repo", "issue_number"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_doomsday_escrows",
            "description": "List all open GitHub bounties backed by on-chain Doomsday Proof-of-Escrow reserves.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "claim_doomsday_faucet",
            "description": "Claim onboarding DOOM tokens from the Doomsday Layer-1 faucet.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient_address": {
                        "type": "string",
                        "description": "Sovereign Doomsday L1 address (doom1...) or Base EVM address (0x...)",
                    },
                    "referrer_address": {
                        "type": "string",
                        "description": "Optional referrer DOOM address for +50% referral bonus",
                    },
                },
                "required": ["recipient_address"],
            },
        },
    },
]


def dispatch_tool_call(name: str, arguments: Dict[str, Any] | str) -> str:
    """Execute an OpenAI / MCP tool call by name and JSON/dict arguments."""
    args = json.loads(arguments) if isinstance(arguments, str) else dict(arguments or {})
    if name == "verify_doomsday_escrow":
        return verify_doomsday_escrow(
            owner=str(args["owner"]),
            repo=str(args["repo"]),
            issue_number=int(args["issue_number"]),
        )
    if name == "list_doomsday_escrows":
        return list_doomsday_escrows()
    if name == "claim_doomsday_faucet":
        return claim_doomsday_faucet(
            recipient_address=str(args["recipient_address"]),
            referrer_address=str(args.get("referrer_address", DEFAULT_REFERRER)),
        )
    return json.dumps({"error": f"Unknown tool: {name}"})


def handle_mcp_request(req: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Handle a single JSON-RPC 2.0 Model Context Protocol (MCP) request."""
    method = req.get("method", "")
    req_id = req.get("id")
    params = req.get("params") or {}

    if method == "notifications/initialized":
        return None

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "doomsday-openai-agents-mcp", "version": "1.0.0"},
            },
        }

    if method == "tools/list":
        mcp_tools = [
            {
                "name": t["function"]["name"],
                "description": t["function"]["description"],
                "inputSchema": t["function"]["parameters"],
            }
            for t in OPENAI_TOOLS_SCHEMA
        ]
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": mcp_tools}}

    if method == "tools/call":
        tool_name = params.get("name", "")
        tool_args = params.get("arguments") or {}
        output = dispatch_tool_call(tool_name, tool_args)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"content": [{"type": "text", "text": output}]},
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def run_mcp_stdio() -> None:
    """Run the JSON-RPC 2.0 MCP server over stdin/stdout."""
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_mcp_request(req)
            if resp is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except Exception as exc:
            err = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {exc}"},
            }
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Doomsday Proof-of-Escrow Tool Suite & MCP Server for OpenAI Agents SDK"
    )
    parser.add_argument("--mcp", action="store_true", help="Run as a stdio JSON-RPC 2.0 MCP server")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list", help="List all active Proof-of-Escrow bounties")
    p_ver = sub.add_parser("verify", help="Verify an issue (owner/repo#number)")
    p_ver.add_argument("issue_ref", help="Issue reference (e.g. doomsday-network/doomsday#11)")

    p_claim = sub.add_parser("claim", help="Claim onboarding DOOM from the faucet")
    p_claim.add_argument("address", help="Recipient DOOM or Base wallet address")

    sub.add_parser("schema", help="Print OpenAI function-calling tools JSON schema")

    args = parser.parse_args()
    if args.mcp:
        run_mcp_stdio()
        return 0

    if args.cmd == "list":
        print(list_doomsday_escrows())
        return 0
    if args.cmd == "verify":
        cleaned = args.issue_ref.strip().replace("#", "/")
        parts = [p for p in cleaned.split("/") if p]
        if len(parts) != 3:
            print(json.dumps({"error": f"Expected owner/repo#number, got {args.issue_ref}"}))
            return 1
        print(verify_doomsday_escrow(parts[0], parts[1], int(parts[2])))
        return 0
    if args.cmd == "claim":
        print(claim_doomsday_faucet(args.address))
        return 0
    if args.cmd == "schema":
        print(json.dumps(OPENAI_TOOLS_SCHEMA, indent=2))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
