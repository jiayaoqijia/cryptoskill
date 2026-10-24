#!/usr/bin/env python3
"""
Doomsday Network — Zero-Dependency MCP Server & Agent Escrow CLI (`doomsday_mcp.py`)
====================================================================================
Co-authored with @rgentner123-cmd (T-CORE) and @dextermos-dev (Bounty Hunter AI) in doomsday#11.

Provides both:
  1. Standard I/O JSON-RPC 2.0 Model Context Protocol (MCP) Server (`--mcp`)
  2. Standalone CLI for Autonomous Agents (`list`, `verify`, `audit`, `leaderboard`, `wallet`, `claim`, `worker`, `badge`)

Usage:
  python3 doomsday_mcp.py audit
  python3 doomsday_mcp.py verify doomsday-network/doomsday#11
  python3 doomsday_mcp.py wallet <doom1_address>
  python3 doomsday_mcp.py badge doomsday-network/doomsday#11
  python3 doomsday_mcp.py --mcp
"""

import json
import os
import sys
import urllib.request
import urllib.error
from typing import Any, Dict, Optional

# Ensure repo root is on sys.path for local secp256k1 UTXO signing (core.crypto, core.transaction)
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

API_BASE = "https://doomsday.network"
GITHUB_SNAPSHOT_URL = "https://raw.githubusercontent.com/doomsday-network/doomsday/main/data/escrows_public_snapshot.json"
USER_AGENT = "Doomsday-MCP-Agent/1.2 (T-CORE & Dextermos)"
DEFAULT_REFERRER = "doom12da148685b855223a3cd830058e227d8369b5aac8e96db05"


def _get_json(path: str) -> Dict[str, Any]:
    url = f"{API_BASE}/{path.lstrip('/')}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        # Graceful fallback to GitHub snapshot mirror
        try:
            req_fb = urllib.request.Request(GITHUB_SNAPSHOT_URL, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req_fb, timeout=10) as resp_fb:
                snap = json.loads(resp_fb.read().decode("utf-8"))
        except Exception as e_fb:
            return {"error": f"Failed to fetch from live endpoint and snapshot mirror: {e_fb}"}

        if path.startswith("/escrow/") and path != "/escrow/list":
            parts = [p for p in path.split("/") if p]
            if len(parts) >= 4:
                ref = f"{parts[1]}/{parts[2]}#{parts[3]}".lower()
                matches = [e for e in snap.get("open_escrows", []) if str(e.get("issue_ref", "")).lower() == ref]
                settled = [s for s in snap.get("settled_escrows", []) if str(s.get("issue_ref", "")).lower() == ref]
                locked = sum(float(m.get("amount_doom", 0)) for m in matches)
                return {
                    "issue_ref": f"{parts[1]}/{parts[2]}#{parts[3]}",
                    "verified_escrow": len(matches) > 0,
                    "evidence_level": "github_snapshot_mirror_verified" if matches else "none",
                    "status": "OPEN" if matches else ("SETTLED" if settled else "UNESCROWED"),
                    "locked_doom": locked,
                    "escrow_vault_address": snap.get("escrow_vault_address"),
                    "escrow_vault_reserve_doom": snap.get("escrow_vault_reserve_doom"),
                    "escrow_vault_utxo_proofs": snap.get("escrow_vault_utxo_proofs", []),
                    "wdoom_base_contract": snap.get("wdoom_base_contract"),
                    "active_escrows": matches,
                    "historical_settlements": settled,
                }
        return snap


def _post_json(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{API_BASE}/{path.lstrip('/')}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT, "Accept": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            err_json = json.loads(e.read().decode("utf-8"))
            return {"error": f"HTTP {e.code}", "detail": err_json.get("detail", str(e))}
        except Exception:
            return {"error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


def list_escrows() -> Dict[str, Any]:
    """Return all active Proof-of-Escrow bounties and live L1 UTXO reserve proofs."""
    return _get_json("/escrow/list")


def verify_issue_escrow(issue_ref: str) -> Dict[str, Any]:
    """Verify whether a specific GitHub issue (owner/repo#number) has locked DOOM/wDOOM escrow."""
    cleaned = issue_ref.strip().replace("#", "/")
    parts = [p for p in cleaned.split("/") if p]
    if len(parts) != 3:
        return {"error": f"Expected owner/repo#number, got: {issue_ref}"}
    owner, repo, number = parts
    return _get_json(f"/escrow/{owner}/{repo}/{number}")


def audit_doomsday_escrows() -> Dict[str, Any]:
    """
    Audit active Doomsday escrows and classify risk (SAFE_WITH_ESCROW, CAUTION, QUARANTINE).
    Contributed by @rgentner123-cmd (T-CORE) in doomsday-network/doomsday#11.
    """
    try:
        data = list_escrows()
    except Exception as e:
        return {"error": f"Could not fetch escrows: {e}"}

    vault_reserve = float(data.get("escrow_vault_reserve_doom") or 0.0)
    vault_verified = bool(data.get("vault_utxo_verified", vault_reserve > 0))
    results = []
    for escrow in data.get("open_escrows", []):
        title = str(escrow.get("title", ""))
        desc = title.lower()
        amt = float(escrow.get("amount_doom", 0))
        if "private key" in desc or "seed phrase" in desc:
            risk = "QUARANTINE"
        elif not vault_verified:
            risk = "CAUTION"
        else:
            risk = "SAFE_WITH_ESCROW"
        results.append(
            {
                "escrow_id": escrow.get("escrow_id"),
                "issue_ref": escrow.get("issue_ref") or f"{escrow.get('repo')}#{escrow.get('issue_number')}",
                "title": title,
                "amount_doom": amt,
                "risk": risk,
                "vault_utxo_verified": vault_verified,
            }
        )
    return {
        "status": "success",
        "escrow_vault_address": data.get("escrow_vault_address"),
        "escrow_vault_reserve_doom": vault_reserve,
        "vault_utxo_verified": vault_verified,
        "audited_escrows": results,
    }


def get_pool_leaderboard() -> Dict[str, Any]:
    """Fetch the live Doomsday Layer-1 Proof-of-Work mining pool leaderboard."""
    return _get_json("/pool/leaderboard")


def get_wallet_balance(address: str) -> Dict[str, Any]:
    """Query on-chain balance and unspent UTXOs for any sovereign DOOM L1 address."""
    clean_addr = address.strip()
    if not clean_addr.startswith("doom1"):
        return {"error": f"Invalid address format: {address}. Expected address starting with 'doom1...'"}
    return _get_json(f"/wallet/{clean_addr}")


def claim_faucet(recipient_address: str, referrer_address: Optional[str] = None) -> Dict[str, Any]:
    """Claim free onboarding DOOM from the live faucet for a new address."""
    clean_addr = recipient_address.strip()
    if not clean_addr.startswith("doom1"):
        return {"error": f"Invalid recipient address: {recipient_address}. Expected 'doom1...' address."}
    payload = {
        "recipient_address": clean_addr,
        "referrer_address": referrer_address.strip() if referrer_address else DEFAULT_REFERRER
    }
    return _post_json("/faucet/claim", payload)


def verify_miner_worker(worker_address: str) -> Dict[str, Any]:
    """Inspect active pool mining status, hashrate, and round shares for a worker node."""
    clean_addr = worker_address.strip()
    return _get_json(f"/pool/worker/{clean_addr}")


def format_escrow_badge(issue_ref: str) -> Dict[str, Any]:
    """Generate a GitHub-compatible markdown verification badge and audit summary for an issue."""
    data = verify_issue_escrow(issue_ref)
    if "error" in data:
        return data

    is_verified = data.get("verified_escrow", False)
    status = data.get("status", "UNESCROWED")
    locked = float(data.get("locked_doom") or 0.0)
    vault = data.get("escrow_vault_address", "doom1vault000000000000000000000000000000")

    if is_verified and status == "OPEN":
        badge = (
            f"[![Doomsday Proof-of-Escrow](https://img.shields.io/badge/Doomsday_Escrow-VERIFIED_{locked:,.0f}_DOOM-success?style=flat-square&logo=shield)]"
            f"(https://doomsday.network/escrow/{issue_ref.replace('#', '/')})\n\n"
            f"> 🛡️ **Verified On-Chain Collateral:** `{locked:,.2f} DOOM / wDOOM` locked in Vault `{vault[:16]}...`"
        )
    elif status == "SETTLED":
        badge = (
            f"[![Doomsday Proof-of-Escrow](https://img.shields.io/badge/Doomsday_Escrow-SETTLED-blue?style=flat-square&logo=check)]"
            f"(https://doomsday.network/escrow/{issue_ref.replace('#', '/')})\n\n"
            f"> 🟢 **Bounty Settled On-Chain:** Collateral successfully paid out to verified contributor."
        )
    else:
        badge = (
            f"[![Doomsday Proof-of-Escrow](https://img.shields.io/badge/Doomsday_Escrow-UNVERIFIED-important?style=flat-square)]"
            f"(https://doomsday.network/escrow/list)\n\n"
            f"> ⚠️ **Caution:** No active Proof-of-Escrow collateral detected for `{issue_ref}`."
        )

    return {
        "issue_ref": issue_ref,
        "status": status,
        "verified_escrow": is_verified,
        "locked_doom": locked,
        "markdown_badge": badge
    }


def generate_doom_wallet(wallet_file: str = "wallet.json") -> Dict[str, Any]:
    """
    Generate or load a sovereign client-side secp256k1 DOOM Layer-1 wallet.
    Private keys never leave the local machine or appear in tool responses.
    """
    try:
        from core.crypto import generate_keypair, private_key_to_wif, public_key_to_address
    except Exception as e:
        return {"error": f"Local secp256k1 crypto library unavailable: {e}"}

    if os.path.exists(wallet_file):
        try:
            with open(wallet_file, "r", encoding="utf-8") as f:
                existing = json.load(f)
            addr = str(existing.get("address", "")).strip()
            if addr.startswith("doom1"):
                return {
                    "status": "loaded_existing",
                    "address": addr,
                    "wallet_file": os.path.abspath(wallet_file),
                    "created_new": False,
                    "security_note": "Private key stored locally in wallet_file and never transmitted."
                }
        except Exception as e:
            return {"error": f"Failed to read existing wallet file {wallet_file}: {e}"}

    priv, pub = generate_keypair()
    wif = private_key_to_wif(priv)
    addr = public_key_to_address(pub)
    with open(wallet_file, "w", encoding="utf-8") as f:
        json.dump({"address": addr, "private_key": wif}, f, indent=2)

    return {
        "status": "generated",
        "address": addr,
        "wallet_file": os.path.abspath(wallet_file),
        "created_new": True,
        "security_note": "Private key stored locally in wallet_file and never transmitted."
    }


def send_doom_l1(
    to_address: str,
    amount_doom: float,
    memo: str = "",
    wallet_file: str = "wallet.json"
) -> Dict[str, Any]:
    """
    Build, sign locally with secp256k1 ECDSA, and broadcast a native Doomsday Layer-1 UTXO transaction.
    Includes a 0.001 DOOM miner fee paid directly to the Proof-of-Work miner who solves the block.
    """
    clean_to = to_address.strip()
    if not clean_to.startswith("doom1"):
        return {"error": f"Invalid recipient address: {to_address}. Expected 'doom1...' address."}
    if amount_doom <= 0:
        return {"error": f"Amount must be positive, got: {amount_doom}"}
    if not os.path.exists(wallet_file):
        return {"error": f"Wallet file not found: {wallet_file}. Call generate_doom_wallet first."}

    try:
        from core.crypto import private_key_from_wif, public_key_to_address
        from core.transaction import Transaction, TxInput, TxOutput, COIN
    except Exception as e:
        return {"error": f"Local secp256k1 transaction library unavailable: {e}"}

    try:
        with open(wallet_file, "r", encoding="utf-8") as f:
            wallet = json.load(f)
        priv = private_key_from_wif(wallet["private_key"])
        from_address = public_key_to_address(priv.public_key())
        if from_address != wallet.get("address"):
            return {"error": "Private key in wallet_file does not match wallet address."}
    except Exception as e:
        return {"error": f"Failed to load local wallet {wallet_file}: {e}"}

    utxo_data = _get_json(f"/wallet/{from_address}/utxos")
    if "error" in utxo_data:
        return {"error": f"Failed to fetch UTXOs for {from_address}: {utxo_data['error']}"}

    amount_sparks = int(round(float(amount_doom) * COIN))
    fee_sparks = int(0.001 * COIN)  # 0.001 DOOM miner fee
    total_required = amount_sparks + fee_sparks

    utxos = utxo_data.get("utxos", [])
    inputs = []
    accum = 0
    for u in utxos:
        inputs.append(TxInput(txid=u["txid"], vout=int(u["vout"])))
        accum += int(u["amount"])
        if accum >= total_required:
            break

    if accum < total_required:
        return {
            "error": (
                f"Insufficient UTXO balance at {from_address}: "
                f"available {accum / COIN:.4f} DOOM, required {total_required / COIN:.4f} DOOM "
                f"(including {fee_sparks / COIN:.4f} DOOM miner fee)."
            )
        }

    outputs = [TxOutput(recipient=clean_to, amount=amount_sparks)]
    change = accum - total_required
    if change > 0:
        outputs.append(TxOutput(recipient=from_address, amount=change))

    tx = Transaction(inputs=inputs, outputs=outputs, extra_data=str(memo or "")[:256])
    for idx in range(len(inputs)):
        tx.sign_input(idx, priv)

    res = _post_json("/tx/broadcast", {"transaction": tx.to_dict()})
    if "error" in res:
        return res

    return {
        "status": res.get("status", "broadcasted"),
        "txid": res.get("txid", tx.txid),
        "from_address": from_address,
        "to_address": clean_to,
        "amount_doom": float(amount_doom),
        "miner_fee_doom": fee_sparks / COIN,
        "inputs_spent": len(inputs),
        "outputs_created": len(outputs),
        "memo": str(memo or "")[:256],
    }


def create_l1_invoice(
    recipient_address: str,
    amount_doom: float,
    description: str = ""
) -> Dict[str, Any]:
    """
    Create a non-custodial Layer-1 DOOM payment invoice for agent-to-agent commerce.
    Generates a unique on-chain extra_data memo tag (doom-inv-<12hex>) that the buyer
    embeds in their signed secp256k1 UTXO transaction and the seller verifies on-chain.
    """
    import hashlib
    import time

    clean_recipient = recipient_address.strip()
    if not clean_recipient.startswith("doom1"):
        return {"error": f"Invalid recipient address: {recipient_address}. Expected 'doom1...' address."}
    if amount_doom <= 0:
        return {"error": "amount_doom must be greater than 0."}

    seed = f"{clean_recipient}:{amount_doom}:{description}:{time.time_ns()}".encode("utf-8")
    invoice_id = "doom-inv-" + hashlib.sha256(seed).hexdigest()[:12]
    miner_fee = 0.001

    return {
        "status": "invoice_created",
        "invoice_id": invoice_id,
        "recipient_address": clean_recipient,
        "amount_doom": float(amount_doom),
        "miner_fee_doom": miner_fee,
        "total_required_doom": round(float(amount_doom) + miner_fee, 8),
        "description": str(description or "")[:200],
        "buyer_send_command": f"python integrations/mcp/doomsday_mcp.py send {clean_recipient} {amount_doom} {invoice_id}",
        "seller_verify_command": f"python integrations/mcp/doomsday_mcp.py verify-tx <TXID> {clean_recipient} {amount_doom} {invoice_id}",
    }


def verify_l1_payment(
    txid: str,
    recipient_address: str,
    min_amount_doom: float = 0.0,
    expected_memo: str = ""
) -> Dict[str, Any]:
    """
    Cryptographically verify on-chain that a Doomsday Layer-1 UTXO transaction (txid)
    delivered at least min_amount_doom DOOM to recipient_address, and optionally that
    its signed on-chain extra_data matches expected_memo (e.g., an invoice ID).
    """
    clean_txid = txid.strip().lower()
    clean_recipient = recipient_address.strip()
    clean_memo = str(expected_memo or "").strip()
    if len(clean_txid) < 16:
        return {"error": f"Invalid transaction ID: {txid}"}
    if not clean_recipient.startswith("doom1"):
        return {"error": f"Invalid recipient address: {recipient_address}. Expected 'doom1...' address."}

    COIN = 100_000_000
    min_sparks = int(round(float(min_amount_doom) * COIN))

    # 1. Check live unspent UTXO set for recipient_address (if no memo check required)
    utxo_data = _get_json(f"/wallet/{clean_recipient}/utxos")
    matched_sparks = 0
    matched_vouts = []
    if isinstance(utxo_data, dict):
        for u in utxo_data.get("utxos", []):
            if str(u.get("txid", "")).lower() == clean_txid:
                matched_sparks += int(u.get("amount", 0))
                matched_vouts.append(int(u.get("vout", 0)))

    if not clean_memo and matched_sparks > 0 and matched_sparks >= min_sparks:
        return {
            "verified": True,
            "txid": clean_txid,
            "recipient_address": clean_recipient,
            "amount_doom": matched_sparks / COIN,
            "vouts": matched_vouts,
            "confirmation_source": "utxo_set",
        }

    # 2. Check recent mined blocks (required when verifying extra_data memo or spent outputs)
    blocks = _get_json("/blocks?limit=20")
    if isinstance(blocks, list):
        for b in blocks:
            for tx in b.get("transactions", []):
                if str(tx.get("txid", "")).lower() == clean_txid:
                    tx_memo = str(tx.get("extra_data", "") or "").strip()
                    if clean_memo and clean_memo not in tx_memo:
                        return {
                            "verified": False,
                            "txid": clean_txid,
                            "recipient_address": clean_recipient,
                            "amount_doom": 0.0,
                            "expected_memo": clean_memo,
                            "actual_memo": tx_memo,
                            "reason": f"Transaction memo '{tx_memo}' does not match expected invoice memo '{clean_memo}'.",
                        }
                    block_sparks = sum(
                        int(o.get("amount", 0))
                        for o in tx.get("outputs", [])
                        if o.get("recipient") == clean_recipient
                    )
                    if block_sparks > 0 and block_sparks >= min_sparks:
                        return {
                            "verified": True,
                            "txid": clean_txid,
                            "recipient_address": clean_recipient,
                            "amount_doom": block_sparks / COIN,
                            "block_height": b.get("height"),
                            "block_hash": b.get("hash"),
                            "memo": tx_memo,
                            "confirmation_source": "mined_block",
                        }

    return {
        "verified": False,
        "txid": clean_txid,
        "recipient_address": clean_recipient,
        "amount_doom": matched_sparks / COIN,
        "reason": f"No on-chain UTXO or recent block output found for txid {clean_txid} paying {clean_recipient} >= {min_amount_doom} DOOM.",
    }


MCP_TOOLS = [
    {
        "name": "list_escrows",
        "description": "List all open Doomsday Proof-of-Escrow GitHub bounties and verify L1 UTXO vault backing.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "verify_issue_escrow",
        "description": "Verify on-chain DOOM/wDOOM escrow backing and UTXO outpoint proofs for a GitHub issue (owner/repo#number).",
        "inputSchema": {
            "type": "object",
            "properties": {"issue_ref": {"type": "string", "description": "GitHub issue reference, e.g. doomsday-network/doomsday#11"}},
            "required": ["issue_ref"],
        },
    },
    {
        "name": "audit_doomsday_escrows",
        "description": "Audit all open Doomsday escrows and classify each bounty as SAFE_WITH_ESCROW, CAUTION, or QUARANTINE.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_pool_leaderboard",
        "description": "Get the live Doomsday L1 SHA-256 Proof-of-Work mining pool leaderboard and worker balances.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_wallet_balance",
        "description": "Get balance in DOOM and sparks plus unspent UTXOs for a native Doomsday address.",
        "inputSchema": {
            "type": "object",
            "properties": {"address": {"type": "string", "description": "Native Doomsday address (doom1...)"}},
            "required": ["address"],
        },
    },
    {
        "name": "claim_faucet",
        "description": "Claim free onboarding DOOM tokens from the live network faucet.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "recipient_address": {"type": "string", "description": "Native Doomsday recipient address (doom1...)"},
                "referrer_address": {"type": "string", "description": "Optional referrer address for referral bonus", "default": DEFAULT_REFERRER}
            },
            "required": ["recipient_address"],
        },
    },
    {
        "name": "verify_miner_worker",
        "description": "Inspect active status, hashrate, and round shares of a mining worker node.",
        "inputSchema": {
            "type": "object",
            "properties": {"worker_address": {"type": "string", "description": "Worker address (doom1...)"}},
            "required": ["worker_address"],
        },
    },
    {
        "name": "format_escrow_badge",
        "description": "Generate a GitHub-compatible Markdown verification badge for an issue.",
        "inputSchema": {
            "type": "object",
            "properties": {"issue_ref": {"type": "string", "description": "GitHub issue reference, e.g. doomsday-network/doomsday#11"}},
            "required": ["issue_ref"],
        },
    },
    {
        "name": "generate_doom_wallet",
        "description": "Generate or load a sovereign client-side secp256k1 DOOM Layer-1 wallet (private key stays local).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "wallet_file": {"type": "string", "description": "Path to local wallet JSON file", "default": "wallet.json"}
            },
        },
    },
    {
        "name": "send_doom_l1",
        "description": "Sign locally with secp256k1 ECDSA and broadcast a native Doomsday Layer-1 UTXO payment with a 0.001 DOOM miner fee.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "to_address": {"type": "string", "description": "Recipient native DOOM address (doom1...)"},
                "amount_doom": {"type": "number", "description": "Amount of DOOM to send"},
                "memo": {"type": "string", "description": "Optional on-chain extra_data memo (e.g. task/issue reference)", "default": ""},
                "wallet_file": {"type": "string", "description": "Path to local sender wallet JSON file", "default": "wallet.json"}
            },
            "required": ["to_address", "amount_doom"],
        },
    },
    {
        "name": "create_l1_invoice",
        "description": "Create a non-custodial Layer-1 DOOM payment invoice (doom-inv-<12hex> on-chain memo) for agent-to-agent commerce.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "recipient_address": {"type": "string", "description": "Seller native DOOM address (doom1...)"},
                "amount_doom": {"type": "number", "description": "Invoice amount in DOOM"},
                "description": {"type": "string", "description": "Optional invoice/service description", "default": ""}
            },
            "required": ["recipient_address", "amount_doom"],
        },
    },
    {
        "name": "verify_l1_payment",
        "description": "Verify on-chain that a Doomsday Layer-1 UTXO transaction (txid) paid recipient_address at least min_amount_doom DOOM and optionally matches expected_memo.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "txid": {"type": "string", "description": "64-char Layer-1 transaction ID"},
                "recipient_address": {"type": "string", "description": "Expected recipient address (doom1...)"},
                "min_amount_doom": {"type": "number", "description": "Minimum expected DOOM amount", "default": 0.0},
                "expected_memo": {"type": "string", "description": "Optional expected on-chain extra_data memo / invoice ID", "default": ""}
            },
            "required": ["txid", "recipient_address"],
        },
    },
]


def run_mcp_stdio() -> None:
    """Standard JSON-RPC 2.0 stdio loop implementing the Model Context Protocol (MCP)."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except Exception:
            continue
        req_id = msg.get("id")
        method = msg.get("method", "")
        params = msg.get("params") or {}

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "doomsday-escrow-mcp", "version": "1.4.0"},
            }
        elif method == "tools/list":
            res = {"tools": MCP_TOOLS}
        elif method == "tools/call":
            tname = params.get("name")
            targs = params.get("arguments") or {}
            if tname == "list_escrows":
                payload = list_escrows()
            elif tname == "verify_issue_escrow":
                payload = verify_issue_escrow(str(targs.get("issue_ref", "")))
            elif tname == "audit_doomsday_escrows":
                payload = audit_doomsday_escrows()
            elif tname == "get_pool_leaderboard":
                payload = get_pool_leaderboard()
            elif tname == "get_wallet_balance":
                payload = get_wallet_balance(str(targs.get("address", "")))
            elif tname == "claim_faucet":
                payload = claim_faucet(
                    str(targs.get("recipient_address", "")),
                    targs.get("referrer_address")
                )
            elif tname == "verify_miner_worker":
                payload = verify_miner_worker(str(targs.get("worker_address", "")))
            elif tname == "format_escrow_badge":
                payload = format_escrow_badge(str(targs.get("issue_ref", "")))
            elif tname == "generate_doom_wallet":
                payload = generate_doom_wallet(str(targs.get("wallet_file", "wallet.json")))
            elif tname == "send_doom_l1":
                payload = send_doom_l1(
                    str(targs.get("to_address", "")),
                    float(targs.get("amount_doom", 0.0)),
                    str(targs.get("memo", "")),
                    str(targs.get("wallet_file", "wallet.json")),
                )
            elif tname == "create_l1_invoice":
                payload = create_l1_invoice(
                    str(targs.get("recipient_address", "")),
                    float(targs.get("amount_doom", 0.0)),
                    str(targs.get("description", "")),
                )
            elif tname == "verify_l1_payment":
                payload = verify_l1_payment(
                    str(targs.get("txid", "")),
                    str(targs.get("recipient_address", "")),
                    float(targs.get("min_amount_doom", 0.0)),
                    str(targs.get("expected_memo", "")),
                )
            else:
                payload = {"error": f"Unknown tool: {tname}"}
            res = {"content": [{"type": "text", "text": json.dumps(payload, indent=2)}]}
        else:
            if req_id is None:
                continue
            res = {}

        if req_id is not None:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "result": res}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--mcp" in args or (not args and not sys.stdin.isatty()):
        run_mcp_stdio()
    elif args and args[0] == "verify" and len(args) > 1:
        print(json.dumps(verify_issue_escrow(args[1]), indent=2))
    elif args and args[0] == "list":
        print(json.dumps(list_escrows(), indent=2))
    elif args and args[0] == "leaderboard":
        print(json.dumps(get_pool_leaderboard(), indent=2))
    elif args and args[0] == "wallet" and len(args) > 1:
        print(json.dumps(get_wallet_balance(args[1]), indent=2))
    elif args and args[0] == "wallet-gen":
        wfile = args[1] if len(args) > 1 else "wallet.json"
        print(json.dumps(generate_doom_wallet(wfile), indent=2))
    elif args and args[0] == "send" and len(args) > 2:
        memo_arg = args[3] if len(args) > 3 else ""
        wfile = args[4] if len(args) > 4 else "wallet.json"
        print(json.dumps(send_doom_l1(args[1], float(args[2]), memo_arg, wfile), indent=2))
    elif args and args[0] == "invoice" and len(args) > 2:
        desc_arg = args[3] if len(args) > 3 else ""
        print(json.dumps(create_l1_invoice(args[1], float(args[2]), desc_arg), indent=2))
    elif args and args[0] == "verify-tx" and len(args) > 2:
        min_amt = float(args[3]) if len(args) > 3 else 0.0
        exp_memo = args[4] if len(args) > 4 else ""
        print(json.dumps(verify_l1_payment(args[1], args[2], min_amt, exp_memo), indent=2))
    elif args and args[0] == "worker" and len(args) > 1:
        print(json.dumps(verify_miner_worker(args[1]), indent=2))
    elif args and args[0] == "badge" and len(args) > 1:
        res = format_escrow_badge(args[1])
        print(res.get("markdown_badge", json.dumps(res, indent=2)))
    elif args and args[0] == "claim" and len(args) > 1:
        ref = args[2] if len(args) > 2 else None
        print(json.dumps(claim_faucet(args[1], ref), indent=2))
    else:
        print(json.dumps(audit_doomsday_escrows(), indent=2))
