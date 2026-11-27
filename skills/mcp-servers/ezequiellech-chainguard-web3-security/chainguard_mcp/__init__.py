"""
ChainGuard MCP — 15-Tool Web3 Security, DeFi Yield, ERC-20 Allowance Revoker, Vault Recovery & Non-Custodial USDT Bridge.
Provides offline deterministic EVM calldata / MCP poisoning / ERC-20 revocation firewalls plus a zero-dependency
Stdio-to-Streamable-HTTP bridge to https://chainguard-studio-production.up.railway.app/mcp.
"""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from typing import Any

DEFAULT_MCP_URL = "https://chainguard-studio-production.up.railway.app/mcp"
STARTER_PASS_URL = (
    "https://chainguard-studio-production.up.railway.app/paygate/pay"
    "?merchant=0x4Ed4D0750453C027FA8398067d5af980Bcc9B6eD"
    "&amount=2&network=base&title=ChainGuard+7-Day+Starter+MCP+Pass&issue_pass=1&billing_days=7"
)
INSTANT_PASS_URL = (
    "https://chainguard-studio-production.up.railway.app/paygate/pay"
    "?merchant=0x4Ed4D0750453C027FA8398067d5af980Bcc9B6eD"
    "&amount=9&network=base&title=ChainGuard+Unlimited+MCP+Pass&issue_pass=1&billing_days=30"
)

_ZW_CHARS = ("\u200b", "\u200c", "\u200d", "\u2060", "\ufeff", "\u202e", "\u202d")
_SOL_KEYPAIR_RE = re.compile(r"\[(?:\s*(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\s*,){63}\s*(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\s*\]")
_SECRET_RE = re.compile(r"\b(?:gh" + r"p|gho|ghu|ghs|ghr|sk_live|whsec)_[A-Za-z0-9]{16,}\b")

REMOTE_TOOL_NAMES: tuple[str, ...] = (
    "check_eip7702_delegation",
    "check_solana_token2022",
    "check_tx_firewall",
    "check_mcp_poisoning",
    "audit_solidity_or_mcp",
    "reclaim_solana_rent",
    "check_frontend_hijack",
    "scan_evm_dust_and_hygiene",
    "build_erc20_approval_revoke",
    "build_evm_dust_to_usdt_sweep",
    "build_cross_chain_consolidation",
    "find_best_defi_yields",
    "analyze_token_alpha",
    "create_usdt_invoice",
    "verify_usdt_invoice",
)


def build_erc20_revoke_calldata(token_address: str, spender: str, network: str = "base") -> dict[str, Any]:
    """Deterministic offline builder for ERC-20 `approve(spender, 0)` allowance revocation calldata."""
    tok = (token_address or "").strip()
    sp = (spender or "").strip()
    if not re.match(r"^0x[a-fA-F0-9]{40}$", tok):
        raise ValueError(f"Invalid ERC-20 token_address: {tok}")
    if not re.match(r"^0x[a-fA-F0-9]{40}$", sp):
        raise ValueError(f"Invalid spender address: {sp}")
    padded_spender = sp[2:].lower().rjust(64, "0")
    zero_amount = "0" * 64
    calldata = f"0x095ea7b3{padded_spender}{zero_amount}"
    return {
        "network": (network or "base").strip().lower(),
        "to": tok,
        "spender": sp,
        "data": calldata,
        "value": "0x0",
        "action": "approve(spender, 0)",
    }


def inspect_tx_calldata(calldata: str, to_address: str = "") -> dict[str, Any]:
    """Deterministic offline pre-flight check for EVM drainer & proxy calldata."""
    data = (calldata or "").strip().lower()
    if data and not data.startswith("0x"):
        data = "0x" + data
    alerts: list[dict[str, Any]] = []
    risk_score = 0

    selector = data[:10] if len(data) >= 10 else ""
    if selector == "0x095ea7b3":
        if "f" * 32 in data[10:]:
            risk_score += 75
            alerts.append({"id": "TX-MAX-APPROVE", "severity": "CRITICAL", "detail": "Unlimited ERC-20 approve(MAX_UINT256) allowance detected."})
        else:
            risk_score += 15
            alerts.append({"id": "TX-APPROVE", "severity": "INFO", "detail": "Finite ERC-20 approve() allowance call."})
    elif selector == "0xa22cb465":
        if data.endswith("0" * 63 + "1") or "0" * 63 + "1" in data[-64:]:
            risk_score += 70
            alerts.append({"id": "TX-SET-APPROVAL-ALL", "severity": "CRITICAL", "detail": "NFT setApprovalForAll(operator, true) grants full collection control."})
    elif selector in {"0xd505accf", "0x8fcbaf0c", "0x30f28b7a"}:
        risk_score += 55
        alerts.append({"id": "TX-PERMIT-SPEND", "severity": "HIGH", "detail": "Gasless Permit/Permit2 approval selector detected."})
    elif selector in {"0x3659cfe6", "0x4f1ef286"}:
        risk_score += 65
        alerts.append({"id": "TX-PROXY-UPGRADE", "severity": "HIGH", "detail": "UUPS/Transparent proxy upgrade selector detected."})

    risk_score = min(100, risk_score)
    verdict = "BLOCK" if risk_score >= 50 else ("WARN" if risk_score >= 25 else "ALLOW")
    return {
        "mode": "offline_preflight",
        "to_address": to_address,
        "selector": selector or None,
        "verdict": verdict,
        "risk_score": risk_score,
        "alerts": alerts,
        "pass_url": INSTANT_PASS_URL,
    }


def _find_line_number(src: str, pattern: str) -> int:
    for idx, line in enumerate((src or "").splitlines(), start=1):
        if re.search(pattern, line, re.IGNORECASE):
            return idx
    return 1


def inspect_mcp_text(text: str) -> dict[str, Any]:
    """Deterministic offline scanner for zero-width Unicode poisoning, prompt injection, and leaked keys."""
    body = text or ""
    low = body.lower()
    alerts: list[dict[str, Any]] = []
    risk_score = 0

    zw_count = sum(body.count(ch) for ch in _ZW_CHARS)
    if zw_count > 0:
        risk_score += 55
        zw_line = 1
        for idx, line in enumerate(body.splitlines(), start=1):
            if any(ch in line for ch in _ZW_CHARS):
                zw_line = idx
                break
        alerts.append({"id": "MCP-UNI-ZW", "severity": "CRITICAL", "line": zw_line, "detail": f"Detected {zw_count} invisible zero-width/bidi characters."})

    for phrase in ("ignore previous instructions", "exfiltrate", "system prompt", "private_key", "seed phrase"):
        if phrase in low:
            risk_score += 65
            alerts.append({"id": "MCP-PROMPT-INJECT", "severity": "CRITICAL", "line": _find_line_number(body, re.escape(phrase)), "detail": "Prompt injection or credential exfiltration phrase detected."})
            break

    m_sol = _SOL_KEYPAIR_RE.search(body)
    if m_sol:
        risk_score += 80
        alerts.append({"id": "DRAIN-SOL-BYTES", "severity": "CRITICAL", "line": body[:m_sol.start()].count("\n") + 1, "detail": "Raw 64-byte Solana keypair array exposed."})

    m_sec = _SECRET_RE.search(body)
    if m_sec:
        risk_score += 75
        alerts.append({"id": "SECRET-TOKEN-LEAK", "severity": "CRITICAL", "line": body[:m_sec.start()].count("\n") + 1, "detail": "API token / signing secret pattern detected."})

    risk_score = min(100, risk_score)
    verdict = "BLOCK" if risk_score >= 50 else ("WARN" if risk_score >= 25 else "ALLOW")
    return {
        "mode": "offline_mcp_firewall",
        "verdict": verdict,
        "risk_score": risk_score,
        "alerts": alerts,
        "pass_url": INSTANT_PASS_URL,
    }


def inspect_solidity_text(text: str) -> dict[str, Any]:
    """Deterministic offline static scanner for critical Solidity smart contract vulnerabilities."""
    src = text or ""
    alerts: list[dict[str, Any]] = []
    risk_score = 0

    if re.search(r"\btx\.origin\b", src):
        risk_score += 70
        alerts.append({"id": "SOL-TX-ORIGIN", "severity": "CRITICAL", "line": _find_line_number(src, r"\btx\.origin\b"), "detail": "tx.origin authentication bypass vector detected; use msg.sender."})

    if re.search(r"\bselfdestruct\s*\(", src):
        risk_score += 80
        alerts.append({"id": "SOL-SELFDESTRUCT", "severity": "CRITICAL", "line": _find_line_number(src, r"\bselfdestruct\s*\("), "detail": "selfdestruct() call detected (deprecated/high-risk contract destruction)."})

    if re.search(r"\.delegatecall\s*\(", src):
        risk_score += 55
        alerts.append({"id": "SOL-DELEGATECALL", "severity": "HIGH", "line": _find_line_number(src, r"\.delegatecall\s*\("), "detail": "Low-level delegatecall() shares caller storage; verify trusted target and layout."})

    if re.search(r"\.call\s*\{[^}]*value\s*:", src) and "nonReentrant" not in src:
        risk_score += 65
        alerts.append({"id": "SOL-REENTRANCY", "severity": "CRITICAL", "line": _find_line_number(src, r"\.call\s*\{"), "detail": "External ETH .call{value:} transfer without nonReentrant guard detected."})

    if re.search(r"\.call\s*[\(\{]", src) and not re.search(r"\(\s*bool\b", src) and "require(" not in src:
        risk_score += 40
        alerts.append({"id": "SOL-UNCHECKED-CALL", "severity": "HIGH", "line": _find_line_number(src, r"\.call\s*[\(\{]"), "detail": "Low-level .call() return boolean does not appear checked."})

    risk_score = min(100, risk_score)
    verdict = "BLOCK" if risk_score >= 50 else ("WARN" if risk_score >= 25 else "ALLOW")
    return {
        "mode": "offline_solidity_static",
        "verdict": verdict,
        "risk_score": risk_score,
        "alerts": alerts,
        "pass_url": INSTANT_PASS_URL,
    }


_SCAN_SKIP_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "dist",
    "build",
    ".next",
}
_SCAN_EXTENSIONS = {".sol", ".json", ".yaml", ".yml", ".md"}
_MAX_SCAN_BYTES = 512 * 1024


def scan_directory(root_path: str) -> dict[str, Any]:
    """Recursively scan .sol contracts and MCP/config files in a repository directory."""
    root = os.path.abspath(root_path or ".")
    files_scanned = 0
    findings: list[dict[str, Any]] = []
    max_risk = 0
    severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "INFO": 0}

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in _SCAN_SKIP_DIRS and not d.startswith(".git"))
        for fname in sorted(filenames):
            ext = os.path.splitext(fname)[1].lower()
            if ext not in _SCAN_EXTENSIONS:
                continue
            fpath = os.path.join(dirpath, fname)
            try:
                if os.path.getsize(fpath) > _MAX_SCAN_BYTES:
                    continue
                with open(fpath, "r", encoding="utf-8", errors="replace") as fh:
                    content = fh.read()
            except OSError:
                continue

            files_scanned += 1
            rel_path = os.path.relpath(fpath, root).replace("\\", "/")
            checks = [inspect_mcp_text(content)]
            if ext == ".sol":
                checks.insert(0, inspect_solidity_text(content))

            for chk in checks:
                max_risk = max(max_risk, int(chk.get("risk_score") or 0))
                for al in chk.get("alerts") or []:
                    sev = str(al.get("severity") or "INFO").upper()
                    severity_counts[sev] = severity_counts.get(sev, 0) + 1
                    findings.append(
                        {
                            "file": rel_path,
                            "line": int(al.get("line") or 1),
                            "id": al.get("id"),
                            "severity": sev,
                            "detail": al.get("detail"),
                        }
                    )

    verdict = "BLOCK" if max_risk >= 50 else ("WARN" if max_risk >= 25 else "ALLOW")
    return {
        "mode": "offline_directory_scan",
        "root": root.replace("\\", "/"),
        "files_scanned": files_scanned,
        "verdict": verdict,
        "max_risk_score": max_risk,
        "severity_counts": severity_counts,
        "findings_count": len(findings),
        "findings": findings,
        "pass_url": INSTANT_PASS_URL,
    }


def format_scan_markdown(report: dict[str, Any]) -> str:
    """Format a scan_directory report as a clean GitHub-Flavored Markdown table."""
    verdict = str(report.get("verdict") or "ALLOW")
    files_scanned = int(report.get("files_scanned") or 0)
    max_risk = int(report.get("max_risk_score") or 0)
    findings = list(report.get("findings") or [])
    lines = [
        "## ChainGuard Security Gate Report",
        "",
        f"- **Verdict:** `{verdict}` (max risk score `{max_risk}/100`)",
        f"- **Files scanned:** `{files_scanned}`",
        f"- **Findings:** `{len(findings)}`",
        "",
    ]
    if findings:
        lines.extend(
            [
                "| File | Rule | Severity | Detail |",
                "|---|---|---|---|",
            ]
        )
        for item in findings[:100]:
            f_col = str(item.get("file") or "").replace("|", "\\|")
            r_col = str(item.get("id") or "").replace("|", "\\|")
            s_col = str(item.get("severity") or "").replace("|", "\\|")
            d_col = str(item.get("detail") or "").replace("|", "\\|")
            lines.append(f"| `{f_col}` | `{r_col}` | **{s_col}** | {d_col} |")
        lines.append("")
    else:
        lines.append("No Solidity critical patterns, Unicode smuggling, prompt injections, or leaked keys detected.")
        lines.append("")

    lines.append(
        f"Unlock full remediation patches, embeddable On-Chain Verified SVG Badges, or 24/7 Frontend & Wallet Watchdogs: "
        f"[Verified Badge & Audit ($19)](https://chainguard-studio-production.up.railway.app/#console) | "
        f"[24/7 Watchdog ($9-$29/mo)](https://chainguard-studio-production.up.railway.app/#console) | "
        f"[30-Day Unlimited MCP Pass ($9)]({INSTANT_PASS_URL})"
    )
    return "\n".join(lines)


def format_scan_sarif(report: dict[str, Any], *, tool_version: str = "1.4.1") -> dict[str, Any]:
    """Export a scan_directory report as OASIS SARIF 2.1.0 for GitHub Code Scanning."""
    findings = list(report.get("findings") or [])
    rules_by_id: dict[str, dict[str, Any]] = {}
    results: list[dict[str, Any]] = []
    sev_to_level = {"CRITICAL": "error", "HIGH": "error", "MEDIUM": "warning", "INFO": "note"}
    sev_to_score = {"CRITICAL": "9.0", "HIGH": "7.5", "MEDIUM": "5.0", "INFO": "2.0"}

    for item in findings:
        rule_id = str(item.get("id") or "CHAINGUARD-FINDING")
        sev = str(item.get("severity") or "INFO").upper()
        detail = str(item.get("detail") or "")
        file_uri = str(item.get("file") or "unknown").lstrip("./")
        start_line = max(1, int(item.get("line") or 1))
        level = sev_to_level.get(sev, "warning")

        if rule_id not in rules_by_id:
            rules_by_id[rule_id] = {
                "id": rule_id,
                "name": rule_id.replace("-", "_"),
                "shortDescription": {"text": detail or rule_id},
                "defaultConfiguration": {"level": level},
                "properties": {
                    "security-severity": sev_to_score.get(sev, "5.0"),
                    "tags": ["security", "web3", "solidity", "mcp"],
                },
            }

        results.append(
            {
                "ruleId": rule_id,
                "level": level,
                "message": {"text": detail or rule_id},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": file_uri},
                            "region": {"startLine": start_line},
                        }
                    }
                ],
            }
        )

    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "ChainGuard MCP Security Gate",
                        "version": tool_version,
                        "informationUri": "https://github.com/EzequielLech/chainguard-mcp",
                        "rules": list(rules_by_id.values()),
                    }
                },
                "results": results,
            }
        ],
    }


class ChainGuardRemoteClient:
    """Thin JSON-RPC 2.0 client for the hosted ChainGuard Firewall & PayGate MCP server."""

    def __init__(self, mcp_url: str = DEFAULT_MCP_URL, api_key: str = "", timeout_s: float = 20.0) -> None:
        self.mcp_url = mcp_url.strip() or DEFAULT_MCP_URL
        self.api_key = (api_key or os.environ.get("CHAINGUARD_API_KEY", "")).strip()
        self.timeout_s = float(timeout_s)

    def post_jsonrpc(self, payload: dict[str, Any]) -> tuple[int, dict[str, Any] | None]:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "chainguard-mcp/1.3.1",
        }
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        req = urllib.request.Request(
            self.mcp_url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                raw = resp.read().decode("utf-8").strip()
                if resp.status == 202 or not raw:
                    return resp.status, None
                return resp.status, json.loads(raw)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(body)
                return exc.code, parsed
            except Exception:
                return exc.code, {
                    "jsonrpc": "2.0",
                    "id": payload.get("id"),
                    "error": {"code": -32000, "message": body or f"HTTP {exc.code}"},
                }

    def list_tools(self) -> list[dict[str, Any]]:
        _, res = self.post_jsonrpc({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
        return list(((res or {}).get("result") or {}).get("tools") or [])


def _full_tools_schema() -> list[dict[str, Any]]:
    return [
        {
            "name": "check_eip7702_delegation",
            "description": (
                "Inspect a single EVM externally owned account (EOA) via live eth_getCode RPC to detect active Pectra EIP-7702 delegation hijacks (0xef0100...23-byte designator). "
                "Read-only, non-destructive lookup on Ethereum, Base, Arbitrum, or Polygon (5 free calls/hour per IP or unlimited with X-API-Key). "
                "Returns JSON with `address`, `network`, `delegated` (boolean), `delegate_contract` (0x address or null), `risk_score` (0-100), and `verdict` (`PASS`, `WARN`, `BLOCK`). "
                "Use this tool for targeted single-address EOA code checks; use `scan_evm_dust_and_hygiene` for full 8-chain token balance and dust discovery."
            ),
            "annotations": {
                "title": "Check EIP-7702 EOA Delegation Hijack",
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": True,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "address": {
                        "type": "string",
                        "description": "42-character hexadecimal EVM wallet address (`0x` followed by 40 hex chars) to inspect for EIP-7702 bytecode delegation.",
                    },
                    "network": {
                        "type": "string",
                        "default": "base",
                        "enum": ["base", "ethereum", "arbitrum", "polygon"],
                        "description": "Target EVM chain for live `eth_getCode` inspection (`base`, `ethereum`, `arbitrum`, or `polygon`). Defaults to `base`.",
                    },
                },
                "required": ["address"],
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "address": {"type": "string"},
                    "network": {"type": "string"},
                    "delegated": {"type": "boolean"},
                    "verdict": {"type": "string"},
                    "risk_score": {"type": "integer"},
                },
                "required": ["address", "network", "verdict"],
            },
        },
        {
            "name": "check_solana_token2022",
            "description": (
                "Inspect a Solana SPL or Token-2022 mint account via live Solana mainnet RPC and RugCheck to detect `PermanentDelegate` drain authorities, arbitrary `TransferHook` programs, active `FreezeAuthority`/`MintAuthority`, and hidden transfer fee basis points. "
                "Read-only, non-destructive analysis (5 free calls/hour per IP or unlimited with X-API-Key). "
                "Returns JSON with `mint`, `program`, `permanent_delegate`, `transfer_hook`, `freeze_authority`, `risk_score` (0-100), and `verdict` (`PASS`, `WARN`, `BLOCK`). "
                "Use this tool for deep Solana mint extension inspection; use `analyze_token_alpha` when you also need DexScreener price, liquidity, and 24h volume."
            ),
            "annotations": {
                "title": "Inspect Solana SPL / Token-2022 Mint Security",
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": True,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "mint": {
                        "type": "string",
                        "description": "Base58-encoded Solana SPL or Token-2022 mint address (32-44 characters, e.g. `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`).",
                    },
                },
                "required": ["mint"],
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "mint": {"type": "string"},
                    "verdict": {"type": "string"},
                    "risk_score": {"type": "integer"},
                },
                "required": ["mint", "verdict"],
            },
        },
        {
            "name": "check_tx_firewall",
            "description": (
                "Perform a read-only pre-flight security check on an unsigned EVM transaction (`to`, `calldata`, `network`) before signing or broadcasting. "
                "Screens 4-byte function selectors against unlimited ERC-20 `approve(MAX_UINT256)` (`0x095ea7b3`), NFT `setApprovalForAll(true)` (`0xa22cb465`), Permit2 drainer signatures (`0xd505accf`), UUPS proxy upgrades (`0x3659cfe6`), and verifies whether the spender is an unverified EOA via `eth_getCode`. "
                "Does not broadcast any transaction. Returns JSON with `verdict` (`ALLOW`, `WARN`, `BLOCK`), `risk_score` (0-100), decoded `selector`, and actionable `alerts`."
            ),
            "annotations": {
                "title": "Pre-Flight EVM Transaction & Drainer Firewall",
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": True,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "42-character hexadecimal target contract or recipient address (`0x...`) of the unsigned EVM transaction.",
                    },
                    "network": {
                        "type": "string",
                        "default": "base",
                        "enum": ["base", "arbitrum", "polygon", "ethereum", "optimism", "bsc"],
                        "description": "EVM network identifier where the transaction will be executed (`base`, `arbitrum`, `polygon`, `ethereum`, `optimism`, `bsc`). Defaults to `base`.",
                    },
                    "calldata": {
                        "type": "string",
                        "default": "0x",
                        "description": "Hex-encoded transaction input data starting with `0x` (e.g. `0x095ea7b3...`). Pass `0x` for native value transfers.",
                    },
                },
                "required": ["to"],
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "verdict": {"type": "string"},
                    "risk_score": {"type": "integer"},
                    "alerts": {"type": "array"},
                },
                "required": ["verdict", "risk_score"],
            },
        },
        {
            "name": "check_mcp_poisoning",
            "description": (
                "Scan untrusted runtime text, MCP tool descriptions, or prompt payloads for invisible zero-width/bidirectional Unicode smuggling (`U+200B`..`U+202E`), prompt-injection override directives, and exposed 64-byte Solana keypairs or private keys. "
                "Purely read-only static text inspection with zero code execution (5 free calls/hour per IP or unlimited with X-API-Key). "
                "Returns JSON with `verdict` (`ALLOW`, `WARN`, `BLOCK`), `risk_score` (0-100), and matched `findings`. "
                "Use this tool for runtime prompt and tool-description hygiene; use `audit_solidity_or_mcp` for full Solidity smart contract or JSON config file audits."
            ),
            "annotations": {
                "title": "Scan Text for MCP Poisoning & Unicode Smuggling",
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": False,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Raw untrusted text, MCP tool description, or prompt string to scan for invisible Unicode characters, prompt injection, and leaked secrets.",
                    },
                },
                "required": ["text"],
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "verdict": {"type": "string"},
                    "risk_score": {"type": "integer"},
                },
                "required": ["verdict", "risk_score"],
            },
        },
        {
            "name": "audit_solidity_or_mcp",
            "description": (
                "Run a read-only static security and token-efficiency audit on Solidity smart contract source code (`.sol`) or MCP server JSON configuration files. "
                "Detects reentrancy, `tx.origin` auth, unchecked external calls, uninitialized proxies, and redundant prompt token bloat without executing the submitted code (5 free calls/hour per IP or unlimited with X-API-Key). "
                "Returns JSON with `risk_score` (0-100), `severity_counts`, `findings` (with remediation patches), and `estimated_savings_usd`. "
                "Use this tool for source-code and config auditing; use `check_mcp_poisoning` for fast runtime prompt-injection screening."
            ),
            "annotations": {
                "title": "Static Audit for Solidity Contracts & MCP Configs",
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": False,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Full Solidity smart contract source code (`pragma solidity ...`) or JSON/YAML MCP server configuration content to audit statically.",
                    },
                    "target_type": {
                        "type": "string",
                        "default": "auto",
                        "enum": ["auto", "solidity", "mcp"],
                        "description": "Analyzer mode: `solidity` for EVM smart contracts, `mcp` for agent configurations, or `auto` to auto-detect from syntax. Defaults to `auto`.",
                    },
                },
                "required": ["content"],
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "risk_score": {"type": "integer"},
                    "findings": {"type": "array"},
                },
                "required": ["risk_score"],
            },
        },
        {
            "name": "reclaim_solana_rent",
            "description": (
                "Scan a Solana wallet via live mainnet RPC for empty 0-balance SPL and Token-2022 token accounts (~0.002039 SOL trapped rent per account) and optionally construct an unsigned base64 `CloseAccount` batch transaction. "
                "Read-only and non-custodial: never broadcasts or signs transactions (unlimited free calls; user receives +88% net reclaimed SOL when they sign and broadcast, with a 12% atomic recovery fee). "
                "Returns JSON with `wallet`, `empty_closable_accounts`, `reclaimable_sol`, `estimated_net_user_sol`, and `unsigned_tx_base64` (up to 15 accounts per atomic tx)."
            ),
            "annotations": {
                "title": "Scan & Build Solana Trapped Rent Reclaim Transaction",
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": True,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "wallet": {
                        "type": "string",
                        "description": "Base58-encoded Solana wallet public key (32-44 chars) to scan for empty 0-balance SPL and Token-2022 token accounts.",
                    },
                    "build_tx": {
                        "type": "boolean",
                        "default": True,
                        "description": "When `true` (default) and closable empty accounts exist, fetches a recent mainnet blockhash and includes `unsigned_tx_base64` ready for wallet signing.",
                    },
                },
                "required": ["wallet"],
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "wallet": {"type": "string"},
                    "empty_closable_accounts": {"type": "integer"},
                    "reclaimable_sol": {"type": "number"},
                },
                "required": ["wallet", "empty_closable_accounts", "reclaimable_sol"],
            },
        },
        {
            "name": "check_frontend_hijack",
            "description": (
                "Inspect a live DeFi web application HTTPS URL and optional EIP-1967 proxy contract for supply-chain hijack indicators: missing Content-Security-Policy (CSP), external `<script>` tags lacking Subresource Integrity (`integrity=\"sha384-...\"`), suspicious third-party domains, and EIP-1967 implementation slot state. "
                "Read-only inspection over HTTPS and EVM RPC (5 free calls/hour per IP or unlimited with X-API-Key). "
                "Returns JSON with `url`, `hijack_risk_score` (0-100), `verdict` (`PASS`, `WARN`, `BLOCK`), `scripts_analyzed`, `missing_sri_count`, and `proxy_implementation`."
            ),
            "annotations": {
                "title": "Inspect DeFi Frontend & EIP-1967 Proxy Integrity",
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": True,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Full `https://` URL of the DeFi web application frontend to inspect for script integrity and HTTP security headers (e.g. `https://app.uniswap.org`).",
                    },
                    "proxy": {
                        "type": "string",
                        "default": "",
                        "description": "Optional 42-character EVM EIP-1967 proxy contract address (`0x...`) to read its on-chain implementation slot (`0x360894...`). Leave empty to skip proxy check.",
                    },
                    "network": {
                        "type": "string",
                        "default": "base",
                        "enum": ["base", "ethereum", "arbitrum", "polygon", "optimism", "bsc"],
                        "description": "EVM network for reading the optional EIP-1967 proxy contract (`base`, `ethereum`, `arbitrum`, `polygon`, `optimism`, `bsc`). Defaults to `base`.",
                    },
                },
                "required": ["url"],
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "url": {"type": "string"},
                    "hijack_risk_score": {"type": "integer"},
                    "verdict": {"type": "string"},
                },
                "required": ["url", "hijack_risk_score", "verdict"],
            },
        },
        {
            "name": "scan_evm_dust_and_hygiene",
            "description": (
                "Scan an EVM wallet across up to 8 chains (`base`, `arbitrum`, `optimism`, `polygon`, `ethereum`, `bsc`, `linea`, `avalanche`) to discover all ERC-20 token holdings priced in USD, identify sweepable non-stablecoin dust tokens, and summarize open unlimited router approvals. "
                "Read-only, zero-connect multi-chain portfolio lookup with unlimited free calls. "
                "Returns JSON with `address`, `total_sweepable_usd`, `stable_balances_usd`, per-token `holdings` (`token_address`, `symbol`, `amount_raw`, `usd_value`, `network`), and `approval_risks`. "
                "Use this tool to discover token balances and `amount_raw` before calling `build_evm_dust_to_usdt_sweep`, `build_cross_chain_consolidation`, or `build_erc20_approval_revoke`."
            ),
            "annotations": {
                "title": "Scan Multi-Chain EVM Portfolio Dust & Allowances",
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": True,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "address": {
                        "type": "string",
                        "description": "42-character hexadecimal EVM wallet address (`0x...`) to scan for ERC-20 dust balances and open router allowances.",
                    },
                    "networks": {
                        "type": "string",
                        "default": "base,arbitrum,optimism,polygon",
                        "description": "Comma-separated list of EVM networks to scan (choose from `base`, `arbitrum`, `optimism`, `polygon`, `ethereum`, `bsc`, `linea`, `avalanche`).",
                    },
                },
                "required": ["address"],
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "address": {"type": "string"},
                    "total_sweepable_usd": {"type": "number"},
                    "stable_balances_usd": {"type": "number"},
                },
                "required": ["address", "total_sweepable_usd"],
            },
        },
        {
            "name": "build_erc20_approval_revoke",
            "description": (
                "Construct unsigned non-custodial EVM calldata (`approve(spender, 0)`, selector `0x095ea7b3`) to revoke an open ERC-20 token allowance granted to a router or spender contract on any of 8 EVM networks. "
                "Read-only calldata generator: never signs or broadcasts transactions (unlimited free calls, 0% fee). "
                "Returns JSON with `network`, `to` (token contract), `spender`, `data` (68-byte hex calldata), `value` (`0x0`), and `eip5792_call` ready for wallet signing."
            ),
            "annotations": {
                "title": "Build ERC-20 Allowance Revocation Calldata",
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": False,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "token_address": {
                        "type": "string",
                        "description": "42-character hexadecimal ERC-20 token contract address (`0x...`) whose allowance will be reset to zero.",
                    },
                    "spender": {
                        "type": "string",
                        "description": "42-character hexadecimal router or spender contract address (`0x...`) whose spending permission is being revoked.",
                    },
                    "network": {
                        "type": "string",
                        "default": "base",
                        "enum": ["base", "arbitrum", "optimism", "polygon", "ethereum", "bsc", "linea", "avalanche"],
                        "description": "Target EVM chain where the ERC-20 allowance exists. Defaults to `base`.",
                    },
                },
                "required": ["token_address", "spender"],
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "network": {"type": "string"},
                    "to": {"type": "string"},
                    "spender": {"type": "string"},
                    "data": {"type": "string"},
                    "value": {"type": "string"},
                },
                "required": ["network", "to", "data"],
            },
        },
        {
            "name": "build_evm_dust_to_usdt_sweep",
            "description": (
                "Build unsigned non-custodial SAME-CHAIN swap calldata (exact-amount ERC-20 `approve` + audited KyberSwap/OpenOcean router swap) converting an ERC-20 token into USDT or USDC on the SAME EVM network (`base`, `arbitrum`, `optimism`, `polygon`, `ethereum`, `bsc`, `linea`, or `avalanche`). "
                "Read-only calldata builder: does not sign or broadcast transactions (unlimited free calls; embeds a 1.00% on-chain integrator fee). "
                "Returns JSON with `approve_tx`, `swap_tx`, `eip5792_calls`, `estimated_out_usd`, and `provider`. "
                "Use this tool when input token and output stablecoin remain on the SAME chain; use `build_cross_chain_consolidation` when bridging between two DIFFERENT chains."
            ),
            "annotations": {
                "title": "Build Same-Chain ERC-20 Dust-to-USDT/USDC Swap Calldata",
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": True,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "network": {
                        "type": "string",
                        "default": "base",
                        "enum": ["base", "arbitrum", "optimism", "polygon", "ethereum", "bsc", "linea", "avalanche"],
                        "description": "Single EVM chain on which both `token_in` and the output `target_stable` reside. Defaults to `base`.",
                    },
                    "token_in": {
                        "type": "string",
                        "description": "42-character hexadecimal ERC-20 contract address (`0x...`) of the token to swap on `network`.",
                    },
                    "amount_in_raw": {
                        "type": "string",
                        "description": "Exact input amount in atomic base units (wei/smallest integer unit as a decimal string, e.g. `1000000000000000000` for 1.0 18-decimal token).",
                    },
                    "sender": {
                        "type": "string",
                        "description": "42-character hexadecimal EVM wallet address (`0x...`) that owns `token_in` and will receive the output USDT/USDC.",
                    },
                    "target_stable": {
                        "type": "string",
                        "default": "USDT",
                        "enum": ["USDT", "USDC"],
                        "description": "Destination stablecoin symbol on the same network (`USDT` or `USDC`). Defaults to `USDT`.",
                    },
                },
                "required": ["token_in", "amount_in_raw", "sender"],
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "network": {"type": "string"},
                    "provider": {"type": "string"},
                    "estimated_out_usd": {"type": "number"},
                    "swap_tx": {"type": "object"},
                },
                "required": ["network", "provider", "swap_tx"],
            },
        },
        {
            "name": "build_cross_chain_consolidation",
            "description": (
                "Build unsigned non-custodial CROSS-CHAIN bridge and swap calldata via LI.FI Diamond moving an ERC-20 or native token from `from_network` to a DIFFERENT destination `to_network` (settling in `USDC`, `USDT`, or destination `NATIVE` gas across `base`, `arbitrum`, `optimism`, `polygon`, `ethereum`, `bsc`, `linea`, `avalanche`). "
                "Read-only calldata builder: does not sign or broadcast transactions (unlimited free calls; includes a 1.00% atomic integrator fee). "
                "Returns JSON with `from_network`, `to_network`, `approve_tx`, `bridge_tx`, `estimated_out_usd`, and `execution_duration_sec`. "
                "Use this tool only when bridging across two DIFFERENT networks; use `build_evm_dust_to_usdt_sweep` for same-chain swaps."
            ),
            "annotations": {
                "title": "Build Cross-Chain Bridge & Consolidation Calldata (LI.FI)",
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": True,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "from_network": {
                        "type": "string",
                        "enum": ["base", "arbitrum", "optimism", "polygon", "ethereum", "bsc", "linea", "avalanche"],
                        "description": "Source EVM chain where the token currently resides (must differ from `to_network`).",
                    },
                    "to_network": {
                        "type": "string",
                        "default": "base",
                        "enum": ["base", "arbitrum", "optimism", "polygon", "ethereum", "bsc", "linea", "avalanche"],
                        "description": "Destination EVM chain to receive the bridged stablecoin or native gas. Defaults to `base`.",
                    },
                    "token_in": {
                        "type": "string",
                        "description": "42-character hexadecimal ERC-20 token contract address (`0x...`) on `from_network` (or `0x0000000000000000000000000000000000000000` for native gas).",
                    },
                    "amount_in_raw": {
                        "type": "string",
                        "description": "Input token amount in atomic base units (wei integer formatted as a decimal string, e.g. `10000000` for 10 USDC).",
                    },
                    "sender": {
                        "type": "string",
                        "description": "42-character hexadecimal EVM wallet address (`0x...`) initiating the bridge on `from_network` and receiving funds on `to_network`.",
                    },
                    "target_stable": {
                        "type": "string",
                        "default": "USDC",
                        "enum": ["USDC", "USDT", "NATIVE"],
                        "description": "Output asset on `to_network`: `USDC`, `USDT`, or `NATIVE` (for emergency cross-chain gas refuel). Defaults to `USDC`.",
                    },
                },
                "required": ["from_network", "token_in", "amount_in_raw", "sender"],
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "from_network": {"type": "string"},
                    "to_network": {"type": "string"},
                    "provider": {"type": "string"},
                    "estimated_out_usd": {"type": "number"},
                },
                "required": ["from_network", "to_network", "provider"],
            },
        },
        {
            "name": "find_best_defi_yields",
            "description": (
                "Query live DeFiLlama yield pools across Base, Arbitrum, Solana, Ethereum, Optimism, Polygon, and BSC ranked by risk-adjusted sustainable APY and TVL safety score. "
                "Read-only market scan (5 free calls/hour per IP returning top 3 pools; full top-25 available via X-API-Key or $0.02 USDC x402 API). "
                "Returns JSON with `count`, `chain_filter`, `asset_filter`, and `pools` array (`project`, `symbol`, `chain`, `apy_total`, `apy_base`, `tvl_usd`, `safety_score`, `il_risk`)."
            ),
            "annotations": {
                "title": "Find Risk-Adjusted DeFi Yield Pools",
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": True,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "chain": {
                        "type": "string",
                        "default": "Base",
                        "description": "Blockchain filter (e.g. `Base`, `Arbitrum`, `Solana`, `Ethereum`, `Optimism`, `Polygon`, `BSC`, or `all`). Defaults to `Base`.",
                    },
                    "asset": {
                        "type": "string",
                        "default": "USDC",
                        "description": "Token symbol substring filter (e.g. `USDC`, `USDT`, `ETH`, `SOL`, or empty string for any asset). Defaults to `USDC`.",
                    },
                    "min_tvl_usd": {
                        "type": "number",
                        "default": 1000000,
                        "description": "Minimum pool Total Value Locked (TVL) in USD required for inclusion. Defaults to `1000000` ($1M).",
                    },
                    "no_il_only": {
                        "type": "boolean",
                        "default": True,
                        "description": "When `true` (default), restricts results to single-sided lending/staking or correlated pools with zero impermanent loss risk.",
                    },
                },
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "count": {"type": "integer"},
                    "pools": {"type": "array"},
                },
                "required": ["count", "pools"],
            },
        },
        {
            "name": "analyze_token_alpha",
            "description": (
                "Aggregate live DexScreener market metrics (USD price, liquidity, FDV, 24h volume, 24h buy/sell order-flow ratio) with GoPlus ERC-20 honeypot/tax checks (for EVM `0x...` tokens) or Token-2022/RugCheck checks (for Solana base58 mints). "
                "Read-only composite market + security lookup (5 free calls/hour per IP or unlimited with X-API-Key). "
                "Returns JSON with `chain`, `market` (`price_usd`, `liquidity_usd`, `fdv_usd`, `volume_24h_usd`, `buy_pressure_pct`), `security`, `combined_risk_score` (0-100), and `verdict` (`PASS`, `WARN`, `BLOCK`). "
                "Use this tool for pre-trade market + security evaluation; use `check_solana_token2022` when you only need raw Solana mint authority inspection without market data."
            ),
            "annotations": {
                "title": "Analyze Token Market Alpha & Honeypot Risk",
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": True,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "token": {
                        "type": "string",
                        "description": "42-character EVM ERC-20 contract address (`0x...`) or 32-44 character base58 Solana mint address to analyze.",
                    },
                    "network": {
                        "type": "string",
                        "default": "",
                        "description": "Optional chain hint (`base`, `arbitrum`, `ethereum`, `polygon`, `bsc`, `solana`). Leave empty to auto-detect from address format and DexScreener top pair.",
                    },
                },
                "required": ["token"],
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "chain": {"type": "string"},
                    "verdict": {"type": "string"},
                    "combined_risk_score": {"type": "integer"},
                    "market": {"type": "object"},
                },
                "required": ["verdict", "combined_risk_score"],
            },
        },
        {
            "name": "create_usdt_invoice",
            "description": (
                "Create a new non-custodial multi-chain USDT/USDC payment invoice and hosted checkout page on Polygon, BSC, Arbitrum, Base, Ethereum, or Solana settling 100% directly to `merchant_wallet` with 0% platform custody. "
                "State-changing operation creating a single-use `pending` invoice record (unlimited free calls, no authentication required). "
                "Supports recurring SaaS subscriptions via optional `customer_ref` and `billing_days`. "
                "Returns JSON with `ok` (boolean), `checkout_url` (hosted payment page), and `invoice` (`invoice_id`, `status`, `amount_usd`, `network`, `merchant_wallet`, `expires_at`)."
            ),
            "annotations": {
                "title": "Create Non-Custodial USDT/USDC Checkout Invoice",
                "readOnlyHint": False,
                "destructiveHint": False,
                "idempotentHint": False,
                "openWorldHint": True,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Human-readable product, order, or subscription plan title displayed on the hosted checkout page (2-140 chars).",
                    },
                    "amount_usd": {
                        "type": "number",
                        "description": "Exact invoice price denominated in USD (settled 1:1 in USDT or USDC on-chain, e.g. `19.0`). Must be >= `0.01`.",
                    },
                    "network": {
                        "type": "string",
                        "default": "polygon",
                        "enum": ["polygon", "bsc", "base", "arbitrum", "ethereum", "solana"],
                        "description": "Settlement blockchain network (`polygon`, `bsc`, `base`, `arbitrum`, `ethereum`, or `solana`). Defaults to `polygon`.",
                    },
                    "merchant_wallet": {
                        "type": "string",
                        "description": "Merchant's self-custody receiving wallet address (`0x...` for EVM chains or base58 public key for `solana`). Funds transfer directly here.",
                    },
                    "webhook_url": {
                        "type": "string",
                        "default": "",
                        "description": "Optional HTTPS URL to receive an HMAC-SHA256 signed `invoice.paid` POST webhook upon on-chain settlement.",
                    },
                    "ttl_minutes": {
                        "type": "integer",
                        "default": 60,
                        "description": "Invoice expiration window in minutes (`5` to `43200`). After `ttl_minutes`, unpaid invoices cannot be settled. Defaults to `60`.",
                    },
                    "customer_ref": {
                        "type": "string",
                        "default": "",
                        "description": "Optional external customer identifier (e.g. email, user ID, or Telegram ID) for tracking recurring subscription status.",
                    },
                    "billing_days": {
                        "type": "integer",
                        "default": 0,
                        "description": "Optional subscription duration in days (e.g. `30` for monthly, `365` for annual). Pass `0` for one-time purchases.",
                    },
                },
                "required": ["title", "amount_usd", "network", "merchant_wallet"],
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "ok": {"type": "boolean"},
                    "checkout_url": {"type": "string"},
                    "invoice": {"type": "object"},
                },
                "required": ["ok"],
            },
        },
        {
            "name": "verify_usdt_invoice",
            "description": (
                "Verify and settle a confirmed on-chain USDT/USDC transaction hash (`tx_hash`) against a PayGate `invoice_id` via live JSON-RPC receipt log inspection. "
                "Idempotent state-changing operation (unlimited free calls, anti-replay enforced): confirms recipient address, token contract, and minimum USD amount, transitions the invoice to `paid`, extends recurring `subscription_expires_at` if configured, and dispatches any configured webhook. "
                "Returns JSON with `ok` (boolean), `already_paid` (boolean), and updated `invoice` object."
            ),
            "annotations": {
                "title": "Verify & Settle On-Chain USDT/USDC Invoice Payment",
                "readOnlyHint": False,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": True,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "invoice_id": {
                        "type": "string",
                        "description": "Unique PayGate invoice identifier returned by `create_usdt_invoice` (e.g. `inv_a1b2c3d4e5f6`).",
                    },
                    "tx_hash": {
                        "type": "string",
                        "description": "Confirmed on-chain transaction hash (`0x...` 66-char hex on EVM chains or base58 signature on Solana) transferring USDT/USDC to the invoice's `merchant_wallet`.",
                    },
                },
                "required": ["invoice_id", "tx_hash"],
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "ok": {"type": "boolean"},
                    "invoice": {"type": "object"},
                },
                "required": ["ok"],
            },
        },
    ]


def _offline_tools_schema() -> list[dict[str, Any]]:
    return [
        {
            "name": "check_tx_firewall",
            "description": (
                "Perform a read-only offline pre-flight security check on an unsigned EVM transaction (`to`, `data`) before signing. "
                "Screens 4-byte selectors for unlimited `approve(MAX_UINT256)` (`0x095ea7b3`), NFT `setApprovalForAll(true)` (`0xa22cb465`), Permit2 drainer calls (`0xd505accf`), and UUPS proxy upgrades (`0x3659cfe6`). "
                "Returns JSON with `verdict` (`ALLOW`, `WARN`, `BLOCK`), `risk_score` (0-100), and `alerts`."
            ),
            "annotations": {
                "title": "Offline Pre-Flight EVM Transaction Firewall",
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": False,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "42-character hexadecimal target contract address (`0x...`).",
                    },
                    "data": {
                        "type": "string",
                        "description": "Hex-encoded transaction calldata starting with `0x` (e.g. `0x095ea7b3...`).",
                    },
                },
                "required": ["data"],
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "verdict": {"type": "string"},
                    "risk_score": {"type": "integer"},
                    "alerts": {"type": "array"},
                },
                "required": ["verdict", "risk_score"],
            },
        },
        {
            "name": "check_mcp_poisoning",
            "description": (
                "Scan untrusted text, MCP tool descriptions, or prompts offline for invisible zero-width/bidirectional Unicode smuggling (`U+200B`..`U+202E`), prompt injection directives, and exposed 64-byte Solana keypairs or API keys. "
                "Read-only deterministic text scanner with zero network calls. "
                "Returns JSON with `verdict` (`ALLOW`, `WARN`, `BLOCK`), `risk_score` (0-100), and `alerts`."
            ),
            "annotations": {
                "title": "Offline MCP Poisoning & Unicode Smuggling Scanner",
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": False,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Raw untrusted text, MCP tool description, or prompt string to scan.",
                    },
                },
                "required": ["text"],
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "verdict": {"type": "string"},
                    "risk_score": {"type": "integer"},
                    "alerts": {"type": "array"},
                },
                "required": ["verdict", "risk_score"],
            },
        },
        {
            "name": "build_erc20_approval_revoke",
            "description": (
                "Construct unsigned non-custodial EVM calldata (`approve(spender, 0)`, selector `0x095ea7b3`) offline to revoke an open ERC-20 token allowance on any EVM network. "
                "Read-only calldata generator: never signs or broadcasts transactions. "
                "Returns JSON with `network`, `to`, `spender`, `data` (68-byte hex calldata), and `value` (`0x0`)."
            ),
            "annotations": {
                "title": "Build ERC-20 Allowance Revocation Calldata",
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": False,
            },
            "inputSchema": {
                "type": "object",
                "properties": {
                    "token_address": {
                        "type": "string",
                        "description": "42-character hexadecimal ERC-20 token contract address (`0x...`) whose allowance will be reset to zero.",
                    },
                    "spender": {
                        "type": "string",
                        "description": "42-character hexadecimal router or spender contract address (`0x...`) whose spending permission is being revoked.",
                    },
                    "network": {
                        "type": "string",
                        "default": "base",
                        "description": "Target EVM chain identifier (e.g. `base`, `arbitrum`, `polygon`, `ethereum`). Defaults to `base`.",
                    },
                },
                "required": ["token_address", "spender"],
            },
            "outputSchema": {
                "type": "object",
                "properties": {
                    "network": {"type": "string"},
                    "to": {"type": "string"},
                    "spender": {"type": "string"},
                    "data": {"type": "string"},
                    "value": {"type": "string"},
                },
                "required": ["network", "to", "data"],
            },
        },
    ]


def handle_mcp_message(
    msg: dict[str, Any],
    *,
    mcp_url: str = DEFAULT_MCP_URL,
    api_key: str = "",
    offline: bool = False,
    client: ChainGuardRemoteClient | None = None,
) -> dict[str, Any] | None:
    """Handle one JSON-RPC 2.0 MCP message locally for discovery/stdio inspection or bridged on tools/call."""
    method = str(msg.get("method") or "")
    rpc_id = msg.get("id")
    params = msg.get("params") or {}

    if method.startswith("notifications/"):
        return None

    if method == "ping":
        return {"jsonrpc": "2.0", "id": rpc_id, "result": {}}

    if method == "initialize":
        req_proto = str(params.get("protocolVersion") or "2025-06-18")
        supported = {"2025-06-18", "2025-03-26", "2024-11-05"}
        return {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": {
                "protocolVersion": req_proto if req_proto in supported else "2025-06-18",
                "capabilities": {
                    "tools": {"listChanged": False},
                    "resources": {"subscribe": False, "listChanged": False},
                    "prompts": {"listChanged": False},
                },
                "serverInfo": {"name": "chainguard-mcp", "version": "1.3.1"},
                "instructions": (
                    f"ChainGuard Web3 Security, DeFi Yield, ERC-20 Revoker & USDT Gateway MCP (15 tools). "
                    f"Remote Streamable-HTTP MCP: {mcp_url} | $2 7-Day Starter Pass: {STARTER_PASS_URL} | $9 Monthly Pass: {INSTANT_PASS_URL}"
                ),
            },
        }

    if method == "tools/list":
        if not offline and client is not None:
            _, res = client.post_jsonrpc(msg)
            return res
        return {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": {"tools": _offline_tools_schema() if offline else _full_tools_schema()},
        }

    if method == "resources/list":
        return {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": {
                "resources": [
                    {
                        "uri": "chainguard://pass",
                        "name": "ChainGuard $2 Starter & $9 Unlimited MCP Pass",
                        "description": "1-Click USDC/USDT checkout for 7-day ($2) or 30-day ($9) unlimited remote MCP & API calls.",
                        "mimeType": "text/plain",
                    }
                ]
            },
        }

    if method == "resources/read":
        uri = str(params.get("uri") or "")
        return {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": {
                "contents": [
                    {
                        "uri": uri or "chainguard://pass",
                        "mimeType": "text/plain",
                        "text": f"7-Day Starter Pass ($2): {STARTER_PASS_URL}\n30-Day Unlimited Pass ($9): {INSTANT_PASS_URL}",
                    }
                ]
            },
        }

    if method == "prompts/list":
        return {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": {
                "prompts": [
                    {
                        "name": "preflight_scan_tx",
                        "description": "Inspect EVM calldata for unlimited approvals, Permit2 drainers, or proxy upgrades.",
                    }
                ]
            },
        }

    if method == "prompts/get":
        return {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": {
                "description": "Pre-flight EVM transaction security inspection prompt.",
                "messages": [
                    {
                        "role": "user",
                        "content": {
                            "type": "text",
                            "text": "Call check_tx_firewall with the target contract address and calldata before signing.",
                        },
                    }
                ],
            },
        }

    if not offline and method == "tools/call":
        rpc_client = client or ChainGuardRemoteClient(mcp_url=mcp_url, api_key=api_key)
        try:
            _, res = rpc_client.post_jsonrpc(msg)
            return res
        except Exception as exc:
            name = str(params.get("name") or "")
            args = params.get("arguments") or {}
            if name == "check_tx_firewall":
                out = inspect_tx_calldata(str(args.get("data") or args.get("calldata") or ""), str(args.get("to") or ""))
                return {"jsonrpc": "2.0", "id": rpc_id, "result": {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]}}
            if name == "check_mcp_poisoning":
                out = inspect_mcp_text(str(args.get("text") or ""))
                return {"jsonrpc": "2.0", "id": rpc_id, "result": {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]}}
            if name == "build_erc20_approval_revoke":
                out = build_erc20_revoke_calldata(
                    str(args.get("token_address") or ""),
                    str(args.get("spender") or ""),
                    str(args.get("network") or "base"),
                )
                return {"jsonrpc": "2.0", "id": rpc_id, "result": {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]}}
            return {"jsonrpc": "2.0", "id": rpc_id, "error": {"code": -32001, "message": f"Remote MCP unreachable: {exc}"}}

    if method == "tools/call":
        name = str(params.get("name") or "")
        args = params.get("arguments") or {}
        if name == "check_tx_firewall":
            out = inspect_tx_calldata(str(args.get("data") or args.get("calldata") or ""), str(args.get("to") or ""))
            return {"jsonrpc": "2.0", "id": rpc_id, "result": {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]}}
        if name == "check_mcp_poisoning":
            out = inspect_mcp_text(str(args.get("text") or ""))
            return {"jsonrpc": "2.0", "id": rpc_id, "result": {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]}}
        if name == "build_erc20_approval_revoke":
            out = build_erc20_revoke_calldata(
                str(args.get("token_address") or ""),
                str(args.get("spender") or ""),
                str(args.get("network") or "base"),
            )
            return {"jsonrpc": "2.0", "id": rpc_id, "result": {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rpc_id, "error": {"code": -32601, "message": f"Unknown offline tool: {name}"}}

    return {"jsonrpc": "2.0", "id": rpc_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}
