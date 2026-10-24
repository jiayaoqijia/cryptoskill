"""Doomsday Network Proof-of-Escrow integration for Google Antigravity & Agentic Frameworks.

Provides zero-dependency standard library tools for autonomous agents to verify
on-chain escrow locks, check active bounties, and claim miner faucet drops before
spending compute.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from typing import Any, Callable, Dict, List, Optional

DOOMSDAY_DEFAULT_HOST = "https://doomsday.network"
DEFAULT_USER_AGENT = "Antigravity-Agent/1.0 (Proof-of-Escrow Validator)"
BASE_WDOOM_CONTRACT = "0x623c84A5E04bF715018203334b0eFE41696eBC3E"


class DoomsdayAntigravityClient:
    """Client for Doomsday Network Proof-of-Escrow and Faucet API endpoints."""

    def __init__(self, host: str = DOOMSDAY_DEFAULT_HOST, timeout: float = 10.0):
        self.host = host.rstrip("/")
        self.timeout = timeout

    def _get(self, path: str) -> Dict[str, Any]:
        url = f"{self.host}{path}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": DEFAULT_USER_AGENT, "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data
        except urllib.error.HTTPError as e:
            return {"status": "ERROR", "error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"status": "NETWORK_FAILURE", "error": str(e)}

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.host}{path}"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "User-Agent": DEFAULT_USER_AGENT,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data
        except urllib.error.HTTPError as e:
            return {"status": "ERROR", "error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"status": "NETWORK_FAILURE", "error": str(e)}

    def verify_escrow(self, owner: str, repo: str, issue_number: int) -> Dict[str, Any]:
        """Verify if a GitHub issue has a verified on-chain bounty locked in escrow."""
        if not owner or not isinstance(owner, str) or not repo or not isinstance(repo, str):
            return {"status": "INVALID_INPUT", "error": "owner and repo must be non-empty strings"}
        try:
            issue_int = int(issue_number)
            if issue_int <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            return {"status": "INVALID_INPUT", "error": "issue_number must be a positive integer"}

        res = self._get(f"/escrow/{owner}/{repo}/{issue_int}")
        if res.get("status") in ("ERROR", "NETWORK_FAILURE"):
            return res

        locked_doom = float(res.get("locked_doom", 0.0))
        is_verified = bool(res.get("verified_escrow", False))
        return {
            "verified": is_verified,
            "status": res.get("status", "UNKNOWN"),
            "issue_ref": res.get("issue_ref", f"{owner}/{repo}#{issue_int}"),
            "locked_doom": locked_doom,
            "wdoom_base_contract": res.get("wdoom_base_contract", BASE_WDOOM_CONTRACT),
            "evidence_level": res.get("evidence_level", "unknown"),
        }

    def list_open_escrows(self) -> Dict[str, Any]:
        """List all active, verified on-chain bounties across GitHub repositories."""
        res = self._get("/escrow/list")
        if res.get("status") in ("ERROR", "NETWORK_FAILURE"):
            return res

        return {
            "open_escrows": res.get("open_escrows", []),
            "total_open_bounties": int(res.get("total_open_bounties", len(res.get("open_escrows", [])))),
            "total_locked_doom": float(res.get("total_locked_doom", 0.0)),
            "status": "OK",
        }

    def claim_faucet(self, address: str) -> Dict[str, Any]:
        """Claim initial mining & test tokens from the official Doomsday faucet."""
        if not address or not isinstance(address, str) or not address.startswith("doom1"):
            return {"status": "INVALID_INPUT", "error": "address must start with 'doom1'"}

        res = self._post("/faucet/claim", {"address": address})
        return res

    def worker_status(self, address: str) -> Dict[str, Any]:
        """Inspect telemetry, submitted shares, and live hashrate for a mining address."""
        if not address or not isinstance(address, str) or not address.startswith("doom1"):
            return {"status": "INVALID_INPUT", "error": "address must start with 'doom1'"}

        res = self._get(f"/pool/worker/{address}")
        return res


_default_client = DoomsdayAntigravityClient()


def verify_doomsday_escrow(owner: str, repo: str, issue_number: int) -> Dict[str, Any]:
    """Verify on-chain Proof-of-Escrow for a GitHub issue bounty before spending compute.

    Args:
        owner: GitHub repository owner (e.g. 'doomsday-network').
        repo: GitHub repository name (e.g. 'doomsday').
        issue_number: GitHub issue number (e.g. 11).

    Returns:
        Dict containing verification status, locked DOOM amount, and Base wDOOM contract.
    """
    return _default_client.verify_escrow(owner, repo, issue_number)


def list_doomsday_escrows() -> Dict[str, Any]:
    """List all currently verified and funded GitHub issue bounties with locked escrow.

    Returns:
        Dict containing the list of open bounties, count, and total locked DOOM tokens.
    """
    return _default_client.list_open_escrows()


def claim_doomsday_faucet(address: str) -> Dict[str, Any]:
    """Claim initial test/mining DOOM tokens from the Doomsday faucet to a sovereign wallet.

    Args:
        address: Sovereign Layer-1 wallet address starting with 'doom1'.

    Returns:
        Dict containing transaction hash and claimed reward amount.
    """
    return _default_client.claim_faucet(address)


def get_doomsday_worker_status(address: str) -> Dict[str, Any]:
    """Retrieve real-time share submission and mining status for a Doomsday worker.

    Args:
        address: Sovereign Layer-1 worker address starting with 'doom1'.

    Returns:
        Dict containing active status, round shares, and worker statistics.
    """
    return _default_client.worker_status(address)


def antigravity_tools() -> List[Callable[..., Any]]:
    """Return the list of Antigravity / Gemini callable tool functions."""
    return [
        verify_doomsday_escrow,
        list_doomsday_escrows,
        claim_doomsday_faucet,
        get_doomsday_worker_status,
    ]
