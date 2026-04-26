#!/usr/bin/env python3
"""
Phase 1 of TRUST.md design: capability manifest extractor.

For each skill, computes the 10 negative-leaning capability facts:
- auto_invocable
- can_execute_shell
- can_install_code
- can_write_files
- can_browse_web
- can_spawn_subagents
- can_move_funds
- requires_private_key
- requires_hosted_operator
- uses_remote_install_script

Plus the execution_model enum.

Writes results to:
  - skills/{cat}/{name}/TRUST.auto.yaml  (per-skill, bot-owned)
  - docs/capabilities.json               (aggregate, for website)

Usage:
  python3 scripts/extract-capabilities.py            # all skills
  python3 scripts/extract-capabilities.py --dry-run  # no writes
  python3 scripts/extract-capabilities.py --skill skills/defi/uniswap-official-swap-integration
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
CAPABILITIES_JSON = ROOT / "docs" / "capabilities.json"

# === Static patterns ===

# Tools whose presence in `allowed-tools` indicates a capability
TOOL_TO_CAP = {
    "bash": "can_execute_shell",
    "shell": "can_execute_shell",
    "edit": "can_write_files",
    "write": "can_write_files",
    "filewrite": "can_write_files",
    "webfetch": "can_browse_web",
    "websearch": "can_browse_web",
    "fetch": "can_browse_web",
    "browse": "can_browse_web",
    "agent": "can_spawn_subagents",
    "subagent": "can_spawn_subagents",
    "task": "can_spawn_subagents",
}

# Patterns that indicate `can_install_code`
INSTALL_PATTERNS = [
    re.compile(r"\bnpx\s+", re.IGNORECASE),
    re.compile(r"\bnpm\s+install\b", re.IGNORECASE),
    re.compile(r"\bpip\s+install\b", re.IGNORECASE),
    re.compile(r"\bpip3\s+install\b", re.IGNORECASE),
    re.compile(r"\bpoetry\s+add\b", re.IGNORECASE),
    re.compile(r"\bcargo\s+install\b", re.IGNORECASE),
    re.compile(r"\bgo\s+install\b", re.IGNORECASE),
    re.compile(r"\bbrew\s+install\b", re.IGNORECASE),
    re.compile(r"\bapt-get\s+install\b", re.IGNORECASE),
    re.compile(r"\byarn\s+(?:add|install)\b", re.IGNORECASE),
    re.compile(r"\bbun\s+(?:add|install)\b", re.IGNORECASE),
    re.compile(r"\buvx?\s+", re.IGNORECASE),
]

# Patterns that indicate `uses_remote_install_script` (high-blast radius)
REMOTE_INSTALL_PATTERNS = [
    re.compile(r"curl\s+[^|]*\|\s*sh\b", re.IGNORECASE | re.DOTALL),
    re.compile(r"curl\s+[^|]*\|\s*bash\b", re.IGNORECASE | re.DOTALL),
    re.compile(r"wget\s+[^|]*\|\s*sh\b", re.IGNORECASE | re.DOTALL),
    re.compile(r"wget\s+[^|]*\|\s*bash\b", re.IGNORECASE | re.DOTALL),
    re.compile(r"sh\s+<\(curl\b", re.IGNORECASE),
    re.compile(r"bash\s+<\(curl\b", re.IGNORECASE),
]

# Patterns that indicate `can_move_funds`
FUND_MOVE_PATTERNS = [
    re.compile(r"\bsendTransaction\b"),
    re.compile(r"\bsendRawTransaction\b"),
    re.compile(r"\bsigner\.send", re.IGNORECASE),
    re.compile(r"\.signAndSendTransaction\b"),
    re.compile(r"\bplaceOrder\b", re.IGNORECASE),
    re.compile(r"\bcreateOrder\b", re.IGNORECASE),
    re.compile(r"\bswap\b\s*\(", re.IGNORECASE),
    re.compile(r"\bwithdraw\b\s*\(", re.IGNORECASE),
    re.compile(r"\bdeposit\b\s*\(", re.IGNORECASE),
    re.compile(r"\bbridge\b\s*\(", re.IGNORECASE),
    re.compile(r"\btransfer\b\s*\(", re.IGNORECASE),
]

# Patterns indicating the skill needs a private key, mnemonic, or signing material
KEY_REQ_PATTERNS = [
    re.compile(r"\bprivate[_\- ]?key\b", re.IGNORECASE),
    re.compile(r"\bmnemonic\b", re.IGNORECASE),
    re.compile(r"\bseed[_\- ]?phrase\b", re.IGNORECASE),
    re.compile(r"\bSECRET[_\-]?KEY\b"),
    re.compile(r"\bPRIVATE_KEY\b"),
    re.compile(r"\bWALLET[_\-]?(?:SECRET|KEY|PRIVATE)\b"),
    re.compile(r"\bsigner\b", re.IGNORECASE),
    re.compile(r"keystore", re.IGNORECASE),
    re.compile(r"wallet[_\- ]?(?:setup|init|create|import)", re.IGNORECASE),
]

# Endpoints whose presence indicates a hosted operator dependency
HOSTED_OPERATOR_HOSTS = {
    # CEX
    "binance.com", "binance.us", "okx.com", "okex.com",
    "coinbase.com", "kraken.com", "kucoin.com", "bybit.com",
    "gate.io", "gate.com", "bitget.com", "huobi.com", "htx.com",
    "mexc.com", "bitfinex.com", "crypto.com", "gemini.com",
    "upbit.com", "alpaca.markets",
    # Hosted RPCs
    "infura.io", "alchemy.com", "alchemyapi.io", "quicknode.com",
    "moralis.io", "blockdaemon.com", "ankr.com", "tatum.io",
    "helius-rpc.com", "helius.xyz", "nodit.io",
    # Hosted analytics / data
    "dune.com", "duneanalytics.com", "nansen.ai", "messari.io",
    "tenderly.co", "etherscan.io", "blockscout.com",
    "thegraph.com", "covalenthq.com", "0x.org",
    # Onramp / payment
    "moonpay.com", "ramp.network", "circle.com",
    # Hosted DEX aggregators with backend
    "1inch.io", "1inch.api", "0x.org",
    # LLM endpoints (operator sees prompts)
    "openai.com", "anthropic.com", "openrouter.ai", "together.xyz",
    "perplexity.ai", "groq.com",
}

URL_RE = re.compile(r"https?://([a-zA-Z0-9_.-]+)(?:[/:][^\s)\"'`]*)?", re.IGNORECASE)


# === Helpers ===

def parse_frontmatter(text):
    """Parse YAML-ish frontmatter into a dict. Minimal — handles flat keys + lists."""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    body = m.group(1)
    out = {}
    cur_list_key = None
    multi_key = None
    multi_lines = []
    for raw in body.splitlines():
        line = raw.rstrip()
        if multi_key:
            if re.match(r"^[a-zA-Z][\w-]*:", line):
                out[multi_key] = " ".join(multi_lines).strip()
                multi_key = None
                multi_lines = []
            elif line.strip():
                multi_lines.append(line.strip())
                continue
            else:
                continue
        list_m = re.match(r"^\s+-\s+(.+)$", line)
        if list_m and cur_list_key:
            out.setdefault(cur_list_key, []).append(list_m.group(1).strip().strip('"').strip("'"))
            continue
        kv = re.match(r"^([a-zA-Z][\w-]*):\s*(.*)$", line)
        if kv:
            k, v = kv.group(1), kv.group(2).strip().strip('"').strip("'")
            if v in ("|", ">", "|-", ">-"):
                multi_key = k
                multi_lines = []
                cur_list_key = None
            elif v:
                out[k] = v
                cur_list_key = None
            else:
                cur_list_key = k
            continue
        cur_list_key = None
    if multi_key and multi_lines:
        out[multi_key] = " ".join(multi_lines).strip()
    return out


def read_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def gather_text(skill_dir):
    """Return the SKILL.md body text + concatenated text from all sub files."""
    parts = {"skill_md": "", "scripts": "", "references": "", "all": ""}
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        parts["skill_md"] = read_text(skill_md)
    for f in skill_dir.rglob("*"):
        if not f.is_file() or f == skill_md:
            continue
        rel = str(f.relative_to(skill_dir))
        text = read_text(f)
        if rel.startswith("scripts/") or f.suffix in (".py", ".sh", ".js", ".ts", ".mjs"):
            parts["scripts"] += "\n" + text
        elif rel.startswith("references/") or f.suffix in (".md", ".txt"):
            parts["references"] += "\n" + text
    parts["all"] = parts["skill_md"] + "\n" + parts["scripts"] + "\n" + parts["references"]
    return parts


# === Core extractor ===

def extract_capabilities(skill_dir):
    text = gather_text(skill_dir)
    fm = parse_frontmatter(text["skill_md"])

    # Tri-state: every field is true | false | "unknown".
    # Default to "unknown"; flip to bool only on positive evidence.
    caps = {k: "unknown" for k in [
        "auto_invocable", "can_execute_shell", "can_install_code", "can_write_files",
        "can_browse_web", "can_spawn_subagents", "can_move_funds",
        "requires_private_key", "requires_hosted_operator", "uses_remote_install_script",
        "mutable_remote_runtime",
    ]}
    confidence = {k: "low" for k in caps}
    evidence = {k: [] for k in caps}

    # auto_invocable: inverted from `user-invocable`
    ui = fm.get("user-invocable")
    if ui is not None:
        v = str(ui).lower()
        caps["auto_invocable"] = (v in ("false", "no", "0"))
        evidence["auto_invocable"].append(f"frontmatter user-invocable: {ui}")
    # disable-model-invocation override
    dmi = fm.get("disable-model-invocation")
    if dmi is not None:
        v = str(dmi).lower()
        if v in ("true", "yes", "1"):
            caps["auto_invocable"] = False
            evidence["auto_invocable"].append("frontmatter disable-model-invocation: true")

    # tool-based capabilities
    allowed = fm.get("allowed-tools")
    tools_listed = []
    if isinstance(allowed, list):
        tools_listed = [str(t).lower() for t in allowed]
    elif isinstance(allowed, str):
        tools_listed = [t.strip().lower() for t in re.split(r"[,\s]+", allowed) if t.strip()]
    if tools_listed:
        # Set the three tool-based caps based on listed tools
        cap_to_tools = {"can_execute_shell": [], "can_write_files": [],
                        "can_browse_web": [], "can_spawn_subagents": []}
        for t in tools_listed:
            base = t.split("(")[0].split(":")[0].strip().lower()
            mapped = TOOL_TO_CAP.get(base)
            if mapped:
                cap_to_tools[mapped].append(t)
        for cap, ts in cap_to_tools.items():
            caps[cap] = bool(ts)
            if ts:
                evidence[cap].append(f"allowed-tools: {','.join(ts)}")
            else:
                evidence[cap].append("allowed-tools listed; capability not granted")

    # remote install script — high-confidence pattern
    for pat in REMOTE_INSTALL_PATTERNS:
        m = pat.search(text["all"])
        if m:
            caps["uses_remote_install_script"] = True
            caps["can_install_code"] = True
            evidence["uses_remote_install_script"].append(f"pattern: {m.group(0)[:80]}")
            evidence["can_install_code"].append("remote install script implies install")
            break

    # can_install_code — package manager invocations
    if not caps["can_install_code"]:
        for pat in INSTALL_PATTERNS:
            m = pat.search(text["all"])
            if m:
                caps["can_install_code"] = True
                evidence["can_install_code"].append(f"pattern: {m.group(0)[:60]}")
                break

    # can_move_funds
    for pat in FUND_MOVE_PATTERNS:
        m = pat.search(text["all"])
        if m:
            caps["can_move_funds"] = True
            evidence["can_move_funds"].append(f"pattern: {m.group(0)[:60]}")
            break

    # requires_private_key
    for pat in KEY_REQ_PATTERNS:
        m = pat.search(text["all"])
        if m:
            caps["requires_private_key"] = True
            evidence["requires_private_key"].append(f"pattern: {m.group(0)[:60]}")
            break

    # requires_hosted_operator — based on URL extraction
    found_hosts = set()
    for m in URL_RE.finditer(text["all"]):
        host = m.group(1).lower()
        # Strip subdomain to find root domain match
        for known in HOSTED_OPERATOR_HOSTS:
            if host == known or host.endswith("." + known):
                found_hosts.add(known)
    if found_hosts:
        caps["requires_hosted_operator"] = True
        evidence["requires_hosted_operator"] = sorted(found_hosts)

    # === Execution model heuristic ===
    em = "unknown"
    if caps["uses_remote_install_script"] or "polymarket-cli" in text["all"].lower() or "wallet-setup" in text["all"].lower():
        em = "installer_bootstrap"
    elif caps["can_move_funds"] and any("api.binance.com" in h or "okx" in h or "kraken" in h or "kucoin" in h
                                         for h in found_hosts):
        em = "custodial_executor"
    elif caps["can_move_funds"] and caps["requires_private_key"]:
        em = "local_executor"
    elif caps["can_move_funds"] and not caps["requires_private_key"]:
        em = "unsigned_tx_builder"
    elif caps["requires_hosted_operator"] and not caps["can_move_funds"]:
        em = "analysis_only"
    elif not caps["can_move_funds"] and not caps["can_write_files"] and not caps["can_install_code"]:
        em = "read_only"

    # router/orchestrator detection
    if re.search(r"\b(?:adapter|route|orchestrator|router|delegate)\b", text["all"], re.IGNORECASE):
        if caps["can_spawn_subagents"] or "delegates" in text["all"].lower():
            em = "router_orchestrator"

    return caps, evidence, em, fm.get("name", skill_dir.name), sorted(found_hosts)


# === Main ===

def write_trust_auto(skill_dir, caps, evidence, em, hosts, dry_run=False):
    """
    Emit TRUST.auto.yaml per the spec in docs/TRUST.md.
    - execution_modes[]: array of one entry in Phase 1 (multi-mode is Phase 2+).
    - capabilities: per-field {value, confidence, source, evidence}.
    - stage: null in Phase 1 (rosette not yet computed).
    """
    target = skill_dir / "TRUST.auto.yaml"

    def cap_value(k):
        v = caps[k]
        if v == "unknown":
            return "unknown"
        return "true" if v is True else "false"

    def cap_source(k, v):
        # Source classification per the spec
        if v == "unknown":
            return "unknown"
        ev = evidence.get(k, [])
        ev_str = " ".join(ev).lower()
        if "frontmatter" in ev_str or "allowed-tools" in ev_str or "user-invocable" in ev_str:
            return "declared"
        if "pattern:" in ev_str or k == "requires_hosted_operator":
            return "extracted"
        return "inferred"

    def cap_confidence(k, v):
        if v == "unknown":
            return "low"
        src = cap_source(k, v)
        return {"declared": "high", "extracted": "medium", "inferred": "low"}.get(src, "low")

    lines = [
        "# Auto-generated by extract-capabilities.py — do NOT edit by hand.",
        "# Human overlay belongs in TRUST.md (frontmatter) once we ship Phase 3.",
        "schema_version: 1",
        f"generated_at: {datetime.now(timezone.utc).isoformat()}",
        "generator: cryptoskill/extract-capabilities/0.2.0",
        "",
        "# === Stage (derived; null until rosette is computed in Phase 3) ===",
        "stage: null",
        "",
        "# === Execution modes (array; Phase 1 emits exactly one) ===",
        "execution_modes:",
        f"  - id: default",
        f"    label: {em}",
    ]
    if em != "unknown":
        lines.append(f"    description: \"Phase 1 single-mode classification — multi-mode breakdown deferred to Phase 2.\"")
    lines += [
        "",
        "# === Capability manifest (per-field provenance) ===",
        "capabilities:",
    ]
    field_order = [
        "auto_invocable", "can_execute_shell", "can_install_code", "can_write_files",
        "can_browse_web", "can_spawn_subagents", "can_move_funds",
        "requires_private_key", "requires_hosted_operator", "uses_remote_install_script",
        "mutable_remote_runtime",
    ]
    for k in field_order:
        v = caps[k]
        lines.append(f"  {k}:")
        lines.append(f"    value: {cap_value(k)}")
        lines.append(f"    confidence: {cap_confidence(k, v)}")
        lines.append(f"    source: {cap_source(k, v)}")
        ev_list = evidence.get(k, [])
        if ev_list:
            lines.append("    evidence:")
            for e in ev_list[:3]:
                safe = e.replace('"', "'").replace("\n", " ")[:160]
                lines.append(f"      - \"{safe}\"")
    if hosts:
        lines.append("")
        lines.append("detected_hosted_operators:")
        for h in hosts:
            lines.append(f"  - {h}")
    body = "\n".join(lines) + "\n"
    if dry_run:
        return body
    target.write_text(body, encoding="utf-8")
    return body


def iter_skills(specific=None):
    if specific:
        p = Path(specific)
        if not p.is_absolute():
            p = ROOT / p
        if (p / "SKILL.md").exists():
            yield p
        return
    for cat in sorted(SKILLS_DIR.iterdir()):
        if not cat.is_dir():
            continue
        for skill in sorted(cat.iterdir()):
            if skill.is_dir() and (skill / "SKILL.md").exists():
                yield skill


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skill", help="Single skill directory path")
    args = p.parse_args()

    aggregate = {}
    counts = {"total": 0, "model_unknown": 0}
    cap_totals = {k: 0 for k in [
        "auto_invocable", "can_execute_shell", "can_install_code", "can_write_files",
        "can_browse_web", "can_spawn_subagents", "can_move_funds",
        "requires_private_key", "requires_hosted_operator", "uses_remote_install_script",
    ]}
    em_counts = {}

    for skill_dir in iter_skills(args.skill):
        caps, evidence, em, name, hosts = extract_capabilities(skill_dir)
        write_trust_auto(skill_dir, caps, evidence, em, hosts, dry_run=args.dry_run)
        rel = str(skill_dir.relative_to(SKILLS_DIR))
        aggregate[rel] = {"name": name, "execution_model": em, "capabilities": caps,
                          "hosted_operators": hosts}
        counts["total"] += 1
        if em == "unknown":
            counts["model_unknown"] += 1
        em_counts[em] = em_counts.get(em, 0) + 1
        for k, v in caps.items():
            if v is True:
                cap_totals[k] += 1

    if not args.dry_run:
        CAPABILITIES_JSON.write_text(
            json.dumps({
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "skills": aggregate,
                "summary": {
                    "total": counts["total"],
                    "execution_models": em_counts,
                    "capability_counts": cap_totals,
                },
            }, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    log.info(f"Processed {counts['total']} skills")
    log.info(f"Execution models: {em_counts}")
    log.info(f"Capability counts (true): {cap_totals}")


if __name__ == "__main__":
    main()
