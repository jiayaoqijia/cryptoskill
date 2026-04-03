#!/usr/bin/env python3
"""CryptoSkill Evaluation Framework — Phase 1: Static + Security + Depth Scorer.

Walks all skill directories in skills/*/, computes:
  - Static Score  (0-40): documentation, completeness, freshness, provenance, structure
  - Security Score (0-20): credential safety, code safety, permission scope, supply chain
  - Depth Score   (0-40): actionability, specificity, examples, error handling, integration

Outputs composite score (0-100) and grade (A/B/C/D/F) to docs/skills.json.

Usage:
    python3 scripts/score-skills.py                          # score all skills
    python3 scripts/score-skills.py skills/defi/uniswap-*    # specific skills
    python3 scripts/score-skills.py --dry-run                # preview without writing
"""

import argparse
import glob as glob_mod
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
SKILLS_JSON = REPO_ROOT / "docs" / "skills.json"

# Categories where fund movement occurs (Track A candidates, but we use
# Track B heuristic for Phase 1)
FUND_MOVING_CATEGORIES = {"exchanges", "defi", "trading", "wallets", "payments"}

# Credential / secret patterns — be careful to avoid flagging docs examples
# Private key: 0x followed by exactly 64 hex chars (not placeholder text)
RE_PRIVATE_KEY = re.compile(
    r"(?<![a-zA-Z0-9])0x[0-9a-fA-F]{64}(?![0-9a-fA-F])"
)
# Mnemonic: 12+ lowercase words that look like a BIP-39 phrase
RE_MNEMONIC = re.compile(
    r"\b(?:[a-z]{3,8}\s+){11,}[a-z]{3,8}\b"
)
# API key patterns — common formats
RE_API_KEY = re.compile(
    r"(?i)(?:api[_-]?key|api[_-]?secret|secret[_-]?key|access[_-]?token)"
    r"\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{20,}['\"]?"
)
# PEM private key blocks
RE_PEM_KEY = re.compile(
    r"-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----"
)
# Base64 strings > 100 chars (potential obfuscation)
RE_BASE64_LONG = re.compile(
    r"[A-Za-z0-9+/]{100,}={0,3}"
)

# Dangerous code patterns in scripts — note: these regex patterns detect
# dangerous function calls in scanned skill scripts, they are NOT used to
# execute any code themselves.
RE_DANGEROUS_EVAL = re.compile(r"\beval\s*\(")
RE_DANGEROUS_EXEC = re.compile(r"\bexec\s*\(")
RE_SUBPROCESS_SHELL = re.compile(r"subprocess\.\w+\(.*shell\s*=\s*True", re.DOTALL)
RE_FETCH_HTTP = re.compile(r"""(?:fetch|requests\.get|requests\.post|urllib\.request\.urlopen)\s*\(\s*['"]http://""")
RE_NON_HTTPS_URL = re.compile(r"""['"]http://[^'"\s]+['"]""")

# Placeholder text patterns
RE_PLACEHOLDER = re.compile(r"\b(?:TODO|TBD|FIXME|Lorem\s+ipsum)\b", re.IGNORECASE)

# Kebab-case validation
RE_KEBAB_CASE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Official naming pattern
RE_OFFICIAL_NAME = re.compile(r"^[a-z0-9]+-official-")

# Contract address (0x + 40 hex chars)
RE_CONTRACT_ADDR = re.compile(r"(?<![a-fA-F0-9])0x[0-9a-fA-F]{40}(?![0-9a-fA-F])")

# URL pattern
RE_URL = re.compile(r"https?://[^\s\"'<>]+")

# API URL
RE_API_URL = re.compile(r"https?://[^\s\"'<>]*(?:api|rpc|endpoint|graphql|subgraph)[^\s\"'<>]*", re.IGNORECASE)

# Chain names
CHAIN_NAMES = {
    "ethereum", "solana", "bitcoin", "polygon", "arbitrum", "optimism",
    "avalanche", "base", "bnb", "bsc", "fantom", "cosmos", "near",
    "sui", "aptos", "cardano", "polkadot", "tron", "starknet", "zksync",
    "scroll", "linea", "mantle", "blast", "mode", "gnosis", "celo",
}

# npm/pip install patterns
RE_NPM_INSTALL = re.compile(r"npm\s+install|yarn\s+add|npx\s+", re.IGNORECASE)
RE_PIP_INSTALL = re.compile(r"pip\s+install|pip3\s+install", re.IGNORECASE)

# Section heading patterns for SKILL.md analysis
RE_SECTION_HEADING = re.compile(r"^#{1,4}\s+(.+)", re.MULTILINE)

# Known placeholder private keys / mnemonics used in docs
PLACEHOLDER_KEYS = {
    "0x0000000000000000000000000000000000000000000000000000000000000000",
    "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80",  # hardhat #0
    "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d",  # hardhat #1
    "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
}

# Known example/placeholder mnemonics
PLACEHOLDER_MNEMONICS = {
    "test test test test test test test test test test test junk",
    "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def parse_frontmatter(path: Path) -> dict:
    """Parse YAML frontmatter from a SKILL.md file. Minimal parser, no deps."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}

    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}

    fm = {}
    current_list_key = None
    current_multiline_key = None
    multiline_lines = []

    for line in m.group(1).splitlines():
        if current_multiline_key:
            if re.match(r"^[a-zA-Z\w-]+:", line):
                fm[current_multiline_key] = " ".join(multiline_lines).strip()
                current_multiline_key = None
                multiline_lines = []
            elif line.strip():
                multiline_lines.append(line.strip())
                continue
            else:
                continue

        list_match = re.match(r"^\s+-\s+(.+)", line)
        if list_match and current_list_key:
            fm.setdefault(current_list_key, []).append(
                list_match.group(1).strip().strip("\"'")
            )
            continue

        kv = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if kv:
            key = kv.group(1)
            val = kv.group(2).strip().strip("\"'")
            if val in ("|", ">"):
                current_multiline_key = key
                multiline_lines = []
                current_list_key = None
            elif val:
                fm[key] = val
                current_list_key = None
            else:
                current_list_key = key
            continue

        current_list_key = None

    if current_multiline_key and multiline_lines:
        fm[current_multiline_key] = " ".join(multiline_lines).strip()

    return fm


def read_file_safe(path: Path) -> str:
    """Read a file safely, returning empty string on failure."""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def get_skill_body(path: Path) -> str:
    """Get the body content of a SKILL.md (everything after frontmatter)."""
    text = read_file_safe(path)
    m = re.match(r"^---\s*\n.*?\n---\s*\n?", text, re.DOTALL)
    if m:
        return text[m.end():]
    return text


def word_count(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def git_last_commit_ts(skill_dir: Path) -> int | None:
    """Get the Unix timestamp of the last commit touching skill_dir."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ct", "--", str(skill_dir)],
            capture_output=True, text=True, timeout=5,
            cwd=str(REPO_ROOT),
        )
        if result.returncode == 0 and result.stdout.strip():
            return int(result.stdout.strip())
    except (subprocess.TimeoutExpired, ValueError, OSError):
        pass
    return None


# Cache for git timestamps
_git_ts_cache: dict[str, int | None] = {}


def git_last_commit_ts_cached(skill_dir: Path) -> int | None:
    """Get git timestamp with caching."""
    key = str(skill_dir)
    if key not in _git_ts_cache:
        _git_ts_cache[key] = git_last_commit_ts(skill_dir)
    return _git_ts_cache[key]


def is_placeholder_key(key_str: str) -> bool:
    """Check if a detected private key is a known placeholder."""
    return key_str.lower() in PLACEHOLDER_KEYS


def is_placeholder_mnemonic(phrase: str) -> bool:
    """Check if a detected mnemonic is a known placeholder."""
    return phrase.strip().lower() in PLACEHOLDER_MNEMONICS


# ---------------------------------------------------------------------------
# Scoring: Static Score (0-40)
# ---------------------------------------------------------------------------


def score_documentation(skill_dir: Path) -> tuple[int, dict]:
    """Score documentation quality (0-10 points)."""
    skill_md = skill_dir / "SKILL.md"
    points = 0
    details = {}

    if not skill_md.exists():
        return 0, {"exists": False}

    details["exists"] = True
    points += 1  # SKILL.md exists

    fm = parse_frontmatter(skill_md)
    body = get_skill_body(skill_md)
    full_text = read_file_safe(skill_md)

    # Has valid YAML frontmatter with name and description
    if fm.get("name") and fm.get("description"):
        points += 1
        details["has_frontmatter"] = True
    else:
        details["has_frontmatter"] = bool(fm)

    # Description > 50 chars
    desc = fm.get("description", "")
    if len(desc) > 50:
        points += 1
        details["desc_length"] = len(desc)
    else:
        details["desc_length"] = len(desc)

    # Has "When to Use" or trigger section
    trigger_patterns = [
        r"when\s+to\s+use", r"trigger", r"use\s+case",
        r"use\s+when", r"why\s+this\s+skill",
    ]
    has_trigger = any(re.search(p, body, re.IGNORECASE) for p in trigger_patterns)
    if has_trigger:
        points += 1
    details["has_trigger_section"] = has_trigger

    # Has examples or usage section
    example_patterns = [
        r"##\s*(?:examples?|usage|quick\s*start|getting\s*started)",
        r"```",  # code block as proxy for examples
    ]
    has_examples = any(re.search(p, body, re.IGNORECASE) for p in example_patterns)
    if has_examples:
        points += 1
    details["has_examples"] = has_examples

    # Has references/ directory
    has_refs = (skill_dir / "references").is_dir()
    if has_refs:
        points += 1
    details["has_references"] = has_refs

    # Word count > 200
    wc = word_count(body)
    if wc > 200:
        points += 1
    details["word_count"] = wc

    # Has version in frontmatter
    fm_text_raw = read_file_safe(skill_md)
    fm_match = re.match(r"^---\s*\n(.*?)\n---", fm_text_raw, re.DOTALL)
    if fm_match and re.search(r"\bversion\b", fm_match.group(1), re.IGNORECASE):
        points += 1
        details["has_version"] = True
    else:
        details["has_version"] = False

    # Has metadata.openclaw section
    if fm_match and re.search(r"\bopenclaw\b", fm_match.group(1), re.IGNORECASE):
        points += 1
        details["has_openclaw"] = True
    else:
        details["has_openclaw"] = False

    # No placeholder text
    if not RE_PLACEHOLDER.search(body):
        points += 1
        details["no_placeholders"] = True
    else:
        details["no_placeholders"] = False

    return min(points, 10), details


def score_completeness(skill_dir: Path) -> tuple[int, dict]:
    """Score file completeness (0-8 points)."""
    points = 0
    details = {}

    # SKILL.md present (2 pts)
    has_skill = (skill_dir / "SKILL.md").exists()
    if has_skill:
        points += 2
    details["has_skill_md"] = has_skill

    # SOURCE.md present with all fields (2 pts)
    source_md = skill_dir / "SOURCE.md"
    if source_md.exists():
        source_text = read_file_safe(source_md)
        required_fields = ["Original Author", "Source", "Classification"]
        has_all = all(f.lower() in source_text.lower() for f in required_fields)
        if has_all:
            points += 2
            details["source_md"] = "complete"
        else:
            points += 1
            details["source_md"] = "partial"
    else:
        details["source_md"] = "missing"

    # references/ directory with at least 1 file (2 pts)
    refs_dir = skill_dir / "references"
    if refs_dir.is_dir():
        ref_files = [f for f in refs_dir.iterdir() if f.is_file()]
        if ref_files:
            points += 2
            details["references"] = len(ref_files)
        else:
            points += 1
            details["references"] = 0
    else:
        details["references"] = "missing"

    # scripts/ directory (1 pt)
    has_scripts = (skill_dir / "scripts").is_dir()
    if has_scripts:
        points += 1
    details["has_scripts"] = has_scripts

    # _meta.json present (1 pt)
    has_meta = (skill_dir / "_meta.json").exists()
    if has_meta:
        points += 1
    details["has_meta_json"] = has_meta

    return min(points, 8), details


def score_freshness(skill_dir: Path) -> tuple[int, dict]:
    """Score freshness based on git log (0-7 points)."""
    ts = git_last_commit_ts_cached(skill_dir)
    details = {}

    if ts is None:
        details["last_commit"] = None
        return 0, details

    now = time.time()
    age_days = (now - ts) / 86400
    details["last_commit_days_ago"] = round(age_days, 1)
    details["last_commit_date"] = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")

    if age_days <= 30:
        return 7, details
    elif age_days <= 90:
        return 5, details
    elif age_days <= 180:
        return 3, details
    elif age_days <= 365:
        return 1, details
    else:
        return 0, details


def score_provenance(skill_dir: Path) -> tuple[int, dict]:
    """Score provenance (0-8 points)."""
    points = 0
    details = {}

    source_md = skill_dir / "SOURCE.md"
    if not source_md.exists():
        return 0, {"source_md": "missing"}

    source_text = read_file_safe(source_md)

    # Classification = OFFICIAL (4 pts)
    if re.search(r"classification.*official", source_text, re.IGNORECASE):
        points += 4
        details["classification"] = "OFFICIAL"
    else:
        details["classification"] = "COMMUNITY"

    # GitHub org present (proxy: has github.com URL) — 2 pts
    # We can't check org repo count without API, so give 2 if github URL present
    github_match = re.search(r"github\.com/([^/\s]+)", source_text)
    if github_match:
        points += 2
        details["github_org"] = github_match.group(1)
    else:
        details["github_org"] = None

    # Source repo has stars — can't check without API, skip (1 pt possible)
    # We give 1 pt if classification is OFFICIAL as proxy for quality
    if details.get("classification") == "OFFICIAL":
        points += 1
        details["stars_proxy"] = True

    # License declared (1 pt)
    if re.search(r"license", source_text, re.IGNORECASE):
        points += 1
        details["has_license"] = True
    else:
        details["has_license"] = False

    return min(points, 8), details


def score_structure(skill_dir: Path) -> tuple[int, dict]:
    """Score structural conventions (0-7 points)."""
    points = 0
    details = {}
    slug = skill_dir.name
    category = skill_dir.parent.name

    # Directory name is kebab-case (1 pt)
    if RE_KEBAB_CASE.match(slug):
        points += 1
        details["kebab_case"] = True
    else:
        details["kebab_case"] = False

    # Official skills follow project-official-name pattern (2 pts)
    source_md = skill_dir / "SOURCE.md"
    is_official = False
    if source_md.exists():
        source_text = read_file_safe(source_md)
        is_official = bool(re.search(r"classification.*official", source_text, re.IGNORECASE))

    if is_official:
        if RE_OFFICIAL_NAME.match(slug):
            points += 2
            details["official_naming"] = True
        else:
            # Still give 1 pt if it's official but doesn't follow the naming
            points += 1
            details["official_naming"] = False
    else:
        # Non-official skills don't need official naming — give the 2 pts
        points += 2
        details["official_naming"] = "n/a"

    # Correct category placement (2 pts) — check skill is in a valid category
    valid_categories = {
        "exchanges", "chains", "defi", "wallets", "analytics", "dev-tools",
        "trading", "prediction-markets", "payments", "social", "ai-crypto",
        "identity", "mcp-servers",
    }
    if category in valid_categories:
        points += 2
        details["valid_category"] = True
    else:
        details["valid_category"] = False

    # No hardcoded secrets in SKILL.md (1 pt)
    skill_md = skill_dir / "SKILL.md"
    has_secrets = False
    if skill_md.exists():
        text = read_file_safe(skill_md)
        for match in RE_PRIVATE_KEY.finditer(text):
            if not is_placeholder_key(match.group()):
                has_secrets = True
                break
        if not has_secrets:
            for match in RE_API_KEY.finditer(text):
                # Skip if it looks like a documentation example (key = "YOUR_...")
                val = match.group()
                if not re.search(r"YOUR|EXAMPLE|REPLACE|xxx|placeholder", val, re.IGNORECASE):
                    has_secrets = True
                    break
    if not has_secrets:
        points += 1
        details["no_secrets"] = True
    else:
        details["no_secrets"] = False

    # Valid YAML frontmatter (1 pt)
    if skill_md.exists():
        fm = parse_frontmatter(skill_md)
        if fm:
            points += 1
            details["valid_frontmatter"] = True
        else:
            details["valid_frontmatter"] = False
    else:
        details["valid_frontmatter"] = False

    return min(points, 7), details


def compute_static_score(skill_dir: Path) -> tuple[int, dict]:
    """Compute full static score (0-40)."""
    doc_pts, doc_details = score_documentation(skill_dir)
    comp_pts, comp_details = score_completeness(skill_dir)
    fresh_pts, fresh_details = score_freshness(skill_dir)
    prov_pts, prov_details = score_provenance(skill_dir)
    struct_pts, struct_details = score_structure(skill_dir)

    total = doc_pts + comp_pts + fresh_pts + prov_pts + struct_pts

    dimensions = {
        "documentation": {"score": doc_pts, "max": 10},
        "completeness": {"score": comp_pts, "max": 8},
        "freshness": {"score": fresh_pts, "max": 7},
        "provenance": {"score": prov_pts, "max": 8},
        "structure": {"score": struct_pts, "max": 7},
    }

    return min(total, 40), dimensions


# ---------------------------------------------------------------------------
# Scoring: Security Score (0-20)
# ---------------------------------------------------------------------------


def scan_files_for_patterns(skill_dir: Path) -> dict:
    """Scan all files in skill_dir for security-relevant patterns."""
    findings = {
        "private_keys": [],
        "mnemonics": [],
        "api_keys": [],
        "pem_keys": [],
        "dangerous_eval_calls": [],
        "dangerous_exec_calls": [],
        "subprocess_shell": [],
        "non_https_fetch": [],
        "base64_long": [],
    }

    for root, dirs, files in os.walk(skill_dir):
        for fname in files:
            fpath = Path(root) / fname
            # Skip binary files
            if fpath.suffix in {".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff",
                                 ".woff2", ".ttf", ".eot", ".svg", ".pdf", ".zip",
                                 ".tar", ".gz", ".bin"}:
                continue

            text = read_file_safe(fpath)
            if not text:
                continue

            rel = str(fpath.relative_to(skill_dir))
            is_script = "scripts/" in rel or fpath.suffix in {".py", ".js", ".ts", ".sh"}

            # Private keys (skip placeholders)
            for match in RE_PRIVATE_KEY.finditer(text):
                if not is_placeholder_key(match.group()):
                    findings["private_keys"].append(rel)
                    break  # one per file is enough

            # Mnemonics (skip placeholders and short matches in docs)
            for match in RE_MNEMONIC.finditer(text):
                phrase = match.group()
                if not is_placeholder_mnemonic(phrase):
                    # Additional filter: skip if it's in a markdown table or
                    # code comment explaining the format
                    words = phrase.split()
                    if len(words) >= 12 and len(set(words)) >= 6:
                        findings["mnemonics"].append(rel)
                        break

            # API keys
            for match in RE_API_KEY.finditer(text):
                val = match.group()
                if not re.search(r"YOUR|EXAMPLE|REPLACE|xxx|placeholder|\.\.\.", val, re.IGNORECASE):
                    findings["api_keys"].append(rel)
                    break

            # PEM keys
            if RE_PEM_KEY.search(text):
                findings["pem_keys"].append(rel)

            # Code safety — only in scripts
            if is_script:
                if RE_DANGEROUS_EVAL.search(text):
                    findings["dangerous_eval_calls"].append(rel)
                if RE_DANGEROUS_EXEC.search(text):
                    findings["dangerous_exec_calls"].append(rel)
                if RE_SUBPROCESS_SHELL.search(text):
                    findings["subprocess_shell"].append(rel)
                if RE_FETCH_HTTP.search(text) or RE_NON_HTTPS_URL.search(text):
                    findings["non_https_fetch"].append(rel)

            # Base64 obfuscation (only in scripts)
            if is_script:
                for match in RE_BASE64_LONG.finditer(text):
                    findings["base64_long"].append(rel)
                    break

    return findings


def score_credential_safety(findings: dict) -> tuple[int, dict]:
    """Score credential safety (0-6 points). Start at 6, deduct per finding."""
    points = 6
    details = {}

    if findings["private_keys"]:
        points -= 3
        details["private_keys"] = findings["private_keys"]
    if findings["mnemonics"]:
        points -= 3
        details["mnemonics"] = findings["mnemonics"]
    if findings["api_keys"]:
        points -= 1
        details["api_keys"] = findings["api_keys"]
    if findings["pem_keys"]:
        points -= 1
        details["pem_keys"] = findings["pem_keys"]

    details["deductions"] = 6 - max(points, 0)
    return max(points, 0), details


def score_code_safety(findings: dict) -> tuple[int, dict]:
    """Score code safety (0-6 points). Start at 6, deduct per finding."""
    points = 6
    details = {}

    if findings["dangerous_eval_calls"]:
        points -= 2
        details["dangerous_eval"] = findings["dangerous_eval_calls"]
    if findings["dangerous_exec_calls"]:
        points -= 2
        details["dangerous_exec"] = findings["dangerous_exec_calls"]
    if findings["subprocess_shell"]:
        points -= 1
        details["subprocess_shell"] = findings["subprocess_shell"]
    if findings["non_https_fetch"]:
        points -= 1
        details["non_https_fetch"] = findings["non_https_fetch"]

    details["deductions"] = 6 - max(points, 0)
    return max(points, 0), details


def score_permission_scope(skill_dir: Path) -> tuple[int, dict]:
    """Score permission scope (0-4 points)."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return 2, {"allowed_tools": "unknown", "risk": "unknown"}

    text = read_file_safe(skill_md)
    fm_match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not fm_match:
        return 2, {"allowed_tools": "unknown", "risk": "unknown"}

    fm_text = fm_match.group(1)

    # Find allowed-tools line
    at_match = re.search(r"allowed-tools?:\s*(.*)", fm_text, re.IGNORECASE)
    if not at_match:
        # No allowed-tools specified — assume medium risk
        return 3, {"allowed_tools": "not_specified", "risk": "low"}

    tools_str = at_match.group(1).strip().strip("[]")
    tools_lower = tools_str.lower()

    details = {"allowed_tools": tools_str}

    # Classify risk
    if not tools_str:
        # Empty allowed-tools
        details["risk"] = "low"
        return 4, details

    has_bash = "bash" in tools_lower
    has_network = any(kw in tools_lower for kw in ["fetch", "http", "curl", "network", "web"])
    has_write = any(kw in tools_lower for kw in ["edit", "write"])

    if has_bash and has_network:
        details["risk"] = "critical"
        return 1, details
    elif has_bash:
        details["risk"] = "high"
        return 2, details
    elif has_write:
        details["risk"] = "medium"
        return 3, details
    else:
        details["risk"] = "low"
        return 4, details


def score_supply_chain(skill_dir: Path) -> tuple[int, dict]:
    """Score supply chain risk (0-4 points)."""
    points = 4
    details = {"external_urls": 0, "install_commands": 0}

    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.is_dir():
        return 4, details

    url_count = 0
    install_count = 0

    for fpath in scripts_dir.rglob("*"):
        if not fpath.is_file():
            continue
        text = read_file_safe(fpath)
        if not text:
            continue

        url_count += len(RE_URL.findall(text))
        install_count += len(RE_NPM_INSTALL.findall(text)) + len(RE_PIP_INSTALL.findall(text))

    details["external_urls"] = url_count
    details["install_commands"] = install_count

    # Deduct based on dependency count
    total_deps = url_count + install_count
    if total_deps > 10:
        points -= 2
    elif total_deps > 5:
        points -= 1

    if install_count > 3:
        points -= 1

    return max(points, 0), details


def check_security_gate(findings: dict) -> tuple[bool, list[str]]:
    """Check security gate. Returns (passed, reasons)."""
    reasons = []

    if findings["private_keys"]:
        reasons.append("Private key found in: " + ", ".join(findings["private_keys"][:3]))
    if findings["mnemonics"]:
        reasons.append("Mnemonic found in: " + ", ".join(findings["mnemonics"][:3]))
    if findings["dangerous_eval_calls"]:
        reasons.append("Dangerous eval() in: " + ", ".join(findings["dangerous_eval_calls"][:3]))
    if findings["base64_long"]:
        reasons.append("Long base64 string in: " + ", ".join(findings["base64_long"][:3]))

    return len(reasons) == 0, reasons


def compute_security_score(skill_dir: Path) -> tuple[int, dict, bool, list[str]]:
    """Compute full security score (0-20). Returns (score, dimensions, gate_passed, gate_reasons)."""
    findings = scan_files_for_patterns(skill_dir)

    cred_pts, cred_details = score_credential_safety(findings)
    code_pts, code_details = score_code_safety(findings)
    perm_pts, perm_details = score_permission_scope(skill_dir)
    chain_pts, chain_details = score_supply_chain(skill_dir)

    gate_passed, gate_reasons = check_security_gate(findings)

    total = cred_pts + code_pts + perm_pts + chain_pts

    dimensions = {
        "credential_safety": {"score": cred_pts, "max": 6},
        "code_safety": {"score": code_pts, "max": 6},
        "permission_scope": {"score": perm_pts, "max": 4},
        "supply_chain": {"score": chain_pts, "max": 4},
    }

    return min(total, 20), dimensions, gate_passed, gate_reasons


# ---------------------------------------------------------------------------
# Scoring: Depth Score (0-40) — Track B Heuristic for ALL skills (Phase 1)
# ---------------------------------------------------------------------------


def score_actionability(skill_dir: Path) -> tuple[int, dict]:
    """Score actionability (0-12 points)."""
    points = 0
    details = {}

    # Has scripts/ with files? (up to 5 pts)
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.is_dir():
        script_files = [f for f in scripts_dir.rglob("*") if f.is_file()]
        if script_files:
            points += min(len(script_files), 3) + 2  # 3-5 pts
            details["script_count"] = len(script_files)
        else:
            details["script_count"] = 0
    else:
        details["script_count"] = 0

    # Has CLI commands in SKILL.md? (up to 4 pts)
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        body = get_skill_body(skill_md)
        # Count code blocks
        code_blocks = re.findall(r"```[\s\S]*?```", body)
        cli_blocks = [b for b in code_blocks if re.search(
            r"(?:curl|npm|pip|python|node|docker|bash|sh|forge|cast|npx|yarn|git|solana|eth)",
            b, re.IGNORECASE
        )]
        if cli_blocks:
            points += min(len(cli_blocks), 4)
            details["cli_commands"] = len(cli_blocks)
        else:
            details["cli_commands"] = 0

        # Has API endpoints? (up to 3 pts)
        api_endpoints = RE_API_URL.findall(body)
        # Also check for endpoint patterns like GET /api/...
        rest_endpoints = re.findall(
            r"(?:GET|POST|PUT|DELETE|PATCH)\s+[/`][^\s`]*",
            body, re.IGNORECASE
        )
        endpoint_count = len(api_endpoints) + len(rest_endpoints)
        if endpoint_count:
            points += min(endpoint_count, 3)
            details["api_endpoints"] = endpoint_count
        else:
            details["api_endpoints"] = 0
    else:
        details["cli_commands"] = 0
        details["api_endpoints"] = 0

    return min(points, 12), details


def score_specificity(skill_dir: Path) -> tuple[int, dict]:
    """Score specificity (0-10 points)."""
    points = 0
    details = {}

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return 0, details

    body = get_skill_body(skill_md)

    # References contract addresses (0x + 40 hex) — up to 3 pts
    contracts = RE_CONTRACT_ADDR.findall(body)
    # Filter out zero address and common placeholders
    real_contracts = [c for c in contracts if c != "0x0000000000000000000000000000000000000000"]
    if real_contracts:
        points += min(len(real_contracts), 3)
    details["contract_addresses"] = len(real_contracts)

    # Specific API URLs — up to 3 pts
    api_urls = RE_API_URL.findall(body)
    if api_urls:
        points += min(len(api_urls), 3)
    details["api_urls"] = len(api_urls)

    # Chain names mentioned — up to 4 pts
    body_lower = body.lower()
    chains_mentioned = [c for c in CHAIN_NAMES if c in body_lower]
    if chains_mentioned:
        points += min(len(chains_mentioned), 4)
    details["chains_mentioned"] = chains_mentioned[:10]

    return min(points, 10), details


def score_examples(skill_dir: Path) -> tuple[int, dict]:
    """Score examples quality (0-8 points)."""
    points = 0
    details = {}

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return 0, details

    body = get_skill_body(skill_md)

    # Has example sections? (up to 3 pts)
    example_headings = re.findall(
        r"#{1,4}\s+(?:examples?|usage|quick\s*start|tutorial|walkthrough|demo)",
        body, re.IGNORECASE
    )
    if example_headings:
        points += min(len(example_headings), 3)
        details["example_sections"] = len(example_headings)
    else:
        details["example_sections"] = 0

    # Has code blocks with content (up to 3 pts)
    code_blocks = re.findall(r"```[\s\S]*?```", body)
    substantial_blocks = [b for b in code_blocks if len(b) > 50]
    if substantial_blocks:
        points += min(len(substantial_blocks), 3)
        details["code_blocks"] = len(substantial_blocks)
    else:
        details["code_blocks"] = 0

    # Has expected outputs? (up to 2 pts)
    output_patterns = [
        r"(?:output|response|result|returns?)\s*[::]",
        r"expected\s+(?:output|response|result)",
        r"```(?:json|xml|yaml|text|output|response)",
    ]
    output_matches = sum(1 for p in output_patterns if re.search(p, body, re.IGNORECASE))
    if output_matches:
        points += min(output_matches, 2)
        details["has_outputs"] = True
    else:
        details["has_outputs"] = False

    return min(points, 8), details


def score_error_handling(skill_dir: Path) -> tuple[int, dict]:
    """Score error handling documentation (0-6 points)."""
    points = 0
    details = {}

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return 0, details

    body = get_skill_body(skill_md)

    # Documents errors (up to 2 pts)
    error_patterns = [
        r"#{1,4}\s+(?:errors?|error\s+handling|troubleshooting|common\s+issues)",
        r"\berror\b.*\b(?:code|message|response)\b",
        r"(?:4\d{2}|5\d{2})\s+",  # HTTP error codes
    ]
    error_matches = sum(1 for p in error_patterns if re.search(p, body, re.IGNORECASE))
    if error_matches:
        points += min(error_matches, 2)
    details["error_docs"] = error_matches

    # Documents edge cases (up to 2 pts)
    edge_patterns = [
        r"edge\s+case",
        r"#{1,4}\s+(?:caveats?|limitations?|known\s+issues?|notes?|warnings?)",
        r"\b(?:caveat|limitation|caution|warning|note)\b.*[::]",
    ]
    edge_matches = sum(1 for p in edge_patterns if re.search(p, body, re.IGNORECASE))
    if edge_matches:
        points += min(edge_matches, 2)
    details["edge_cases"] = edge_matches

    # Documents rate limits, constraints (up to 2 pts)
    constraint_patterns = [
        r"rate\s+limit",
        r"max(?:imum)?\s+(?:request|call|query|limit)",
        r"(?:require|prerequisite|dependency|setup)",
    ]
    constraint_matches = sum(1 for p in constraint_patterns if re.search(p, body, re.IGNORECASE))
    if constraint_matches:
        points += min(constraint_matches, 2)
    details["constraints"] = constraint_matches

    return min(points, 6), details


def score_integration(skill_dir: Path) -> tuple[int, dict]:
    """Score integration references (0-4 points)."""
    points = 0
    details = {}

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return 0, details

    body = get_skill_body(skill_md)

    # References other skills (up to 2 pts)
    skill_refs = re.findall(r"(?:skill|plugin|extension|tool)s?/\w+", body, re.IGNORECASE)
    other_skill_refs = re.findall(r"\b\w+-(?:skill|plugin|agent|mcp)\b", body, re.IGNORECASE)
    ref_count = len(skill_refs) + len(other_skill_refs)
    if ref_count:
        points += min(ref_count, 2)
    details["skill_references"] = ref_count

    # References MCP servers or protocols (up to 2 pts)
    mcp_patterns = [
        r"\bMCP\b",
        r"model\s+context\s+protocol",
        r"\bSSE\b.*\bserver\b",
        r"\bwebsocket\b",
        r"compose|docker",
    ]
    mcp_matches = sum(1 for p in mcp_patterns if re.search(p, body, re.IGNORECASE))
    if mcp_matches:
        points += min(mcp_matches, 2)
    details["integration_refs"] = mcp_matches

    return min(points, 4), details


def compute_depth_score(skill_dir: Path) -> tuple[int, dict]:
    """Compute full depth score (0-40) using Track B heuristic."""
    act_pts, act_details = score_actionability(skill_dir)
    spec_pts, spec_details = score_specificity(skill_dir)
    ex_pts, ex_details = score_examples(skill_dir)
    err_pts, err_details = score_error_handling(skill_dir)
    intg_pts, intg_details = score_integration(skill_dir)

    total = act_pts + spec_pts + ex_pts + err_pts + intg_pts

    dimensions = {
        "actionability": {"score": act_pts, "max": 12},
        "specificity": {"score": spec_pts, "max": 10},
        "examples": {"score": ex_pts, "max": 8},
        "error_handling": {"score": err_pts, "max": 6},
        "integration": {"score": intg_pts, "max": 4},
    }

    return min(total, 40), dimensions


# ---------------------------------------------------------------------------
# Composite Score + Grade
# ---------------------------------------------------------------------------


def compute_grade(score: int) -> str:
    """Map score to letter grade."""
    if score >= 80:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 40:
        return "C"
    elif score >= 20:
        return "D"
    else:
        return "F"


def score_skill(skill_dir: Path) -> dict:
    """Compute all scores for a single skill."""
    static_total, static_dims = compute_static_score(skill_dir)
    security_total, security_dims, gate_passed, gate_reasons = compute_security_score(skill_dir)
    depth_total, depth_dims = compute_depth_score(skill_dir)

    composite = min(static_total + security_total + depth_total, 100)
    grade = compute_grade(composite)

    return {
        "total": composite,
        "grade": grade,
        "static": static_total,
        "security": security_total,
        "depth": depth_total,
        "risk_gate": "PASS" if gate_passed else "FAIL",
        "risk_gate_reasons": gate_reasons if not gate_passed else [],
        "dimensions": {
            "static": static_dims,
            "security": security_dims,
            "depth": depth_dims,
        },
        "scored_at": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def collect_skill_dirs(args_paths: list[str]) -> list[Path]:
    """Collect skill directories from CLI arguments or walk all."""
    if args_paths:
        dirs = []
        for pattern in args_paths:
            expanded = glob_mod.glob(pattern)
            for p in expanded:
                path = Path(p).resolve()
                if path.is_dir() and (path / "SKILL.md").exists():
                    dirs.append(path)
                elif path.is_dir():
                    # Maybe it's a category dir — walk children
                    for child in sorted(path.iterdir()):
                        if child.is_dir() and (child / "SKILL.md").exists():
                            dirs.append(child)
        return sorted(set(dirs))

    # Walk all
    dirs = []
    for cat_dir in sorted(SKILLS_DIR.iterdir()):
        if not cat_dir.is_dir():
            continue
        for skill_dir in sorted(cat_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            dirs.append(skill_dir)
    return dirs


def print_summary(results: dict[str, dict]):
    """Print a summary table to stdout."""
    if not results:
        print("No skills scored.")
        return

    # Sort by score descending
    sorted_skills = sorted(results.items(), key=lambda x: x[1]["total"], reverse=True)

    # Grade distribution
    grade_dist = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    gate_failures = []
    total_score = 0
    cat_scores: dict[str, list[int]] = {}

    for name, result in sorted_skills:
        grade_dist[result["grade"]] += 1
        total_score += result["total"]
        if result["risk_gate"] == "FAIL":
            gate_failures.append(name)

        # Extract category from path
        parts = name.split("/")
        if len(parts) >= 2:
            cat = parts[0]
        else:
            cat = "unknown"
        cat_scores.setdefault(cat, []).append(result["total"])

    avg_score = total_score / len(sorted_skills)

    print("\n" + "=" * 72)
    print("  CRYPTOSKILL EVALUATION REPORT")
    print("=" * 72)
    print("")
    print("  Total skills scored: {}".format(len(sorted_skills)))
    print("  Average score: {:.1f}/100".format(avg_score))
    print("  Security gate failures: {}".format(len(gate_failures)))

    # Grade distribution
    print("")
    print("  Grade Distribution:")
    for grade in ["A", "B", "C", "D", "F"]:
        count = grade_dist[grade]
        pct = count / len(sorted_skills) * 100
        bar = "#" * int(pct / 2)
        print("    {}: {:4d} ({:5.1f}%) {}".format(grade, count, pct, bar))

    # Category averages
    print("")
    print("  Category Averages:")
    print("  {:<22} {:>5}  {:>5}  {:>5}".format("Category", "Avg", "Count", "Grade"))
    print("  {} {}  {}  {}".format("-" * 22, "-" * 5, "-" * 5, "-" * 5))
    for cat in sorted(cat_scores.keys()):
        scores = cat_scores[cat]
        cat_avg = sum(scores) / len(scores)
        cat_grade = compute_grade(int(cat_avg))
        print("  {:<22} {:5.1f}  {:5d}  {:>5}".format(cat, cat_avg, len(scores), cat_grade))

    # Top 10
    print("")
    print("  Top 10 Skills:")
    print("  {:<45} {:>5}  {:>5}  {:>6}  {:>3}  {:>5}".format(
        "Skill", "Score", "Grade", "Static", "Sec", "Depth"))
    print("  {} {}  {}  {}  {}  {}".format(
        "-" * 45, "-" * 5, "-" * 5, "-" * 6, "-" * 3, "-" * 5))
    for name, result in sorted_skills[:10]:
        short_name = name.split("/")[-1][:44]
        print("  {:<45} {:5d}  {:>5}  {:6d}  {:3d}  {:5d}".format(
            short_name, result["total"], result["grade"],
            result["static"], result["security"], result["depth"]))

    # Bottom 10
    print("")
    print("  Bottom 10 Skills:")
    print("  {:<45} {:>5}  {:>5}  {:>6}  {:>3}  {:>5}".format(
        "Skill", "Score", "Grade", "Static", "Sec", "Depth"))
    print("  {} {}  {}  {}  {}  {}".format(
        "-" * 45, "-" * 5, "-" * 5, "-" * 6, "-" * 3, "-" * 5))
    for name, result in sorted_skills[-10:]:
        short_name = name.split("/")[-1][:44]
        print("  {:<45} {:5d}  {:>5}  {:6d}  {:3d}  {:5d}".format(
            short_name, result["total"], result["grade"],
            result["static"], result["security"], result["depth"]))

    # Security gate failures
    if gate_failures:
        print("")
        print("  Security Gate Failures ({}):".format(len(gate_failures)))
        for name in gate_failures[:20]:
            short_name = name.split("/")[-1]
            reasons = results[name].get("risk_gate_reasons", [])
            print("    - {}: {}".format(short_name, "; ".join(reasons[:2])))
        if len(gate_failures) > 20:
            print("    ... and {} more".format(len(gate_failures) - 20))

    print("")
    print("=" * 72)


def main():
    parser = argparse.ArgumentParser(
        description="CryptoSkill Evaluation Framework -- Phase 1 Scorer"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Specific skill directories or glob patterns (default: all skills)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print scores without writing to skills.json",
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Only output JSON, no summary table",
    )
    args = parser.parse_args()

    skill_dirs = collect_skill_dirs(args.paths)
    if not skill_dirs:
        print("No skill directories found.", file=sys.stderr)
        sys.exit(1)

    print("Scoring {} skills...".format(len(skill_dirs)), file=sys.stderr)
    start_time = time.time()

    # Score all skills
    results: dict[str, dict] = {}
    for i, skill_dir in enumerate(skill_dirs):
        # Use relative path as key for matching with skills.json
        try:
            rel = str(skill_dir.relative_to(SKILLS_DIR))
        except ValueError:
            rel = skill_dir.name
        slug = skill_dir.name

        result = score_skill(skill_dir)
        results[rel] = result

        if (i + 1) % 100 == 0:
            elapsed = time.time() - start_time
            print("  ... scored {}/{} ({:.1f}s)".format(i + 1, len(skill_dirs), elapsed),
                  file=sys.stderr)

    elapsed = time.time() - start_time
    print("Scored {} skills in {:.1f}s".format(len(results), elapsed), file=sys.stderr)

    # Print summary
    if not args.json_only:
        print_summary(results)

    # Update skills.json
    if args.dry_run:
        print("\n[DRY-RUN] Would update {} with scores for {} skills".format(
            SKILLS_JSON, len(results)), file=sys.stderr)
        return

    # Load existing skills.json
    if SKILLS_JSON.exists():
        try:
            with open(SKILLS_JSON, "r", encoding="utf-8") as fh:
                catalog = json.load(fh)
        except (json.JSONDecodeError, OSError) as e:
            print("Error reading {}: {}".format(SKILLS_JSON, e), file=sys.stderr)
            sys.exit(1)
    else:
        print("{} not found".format(SKILLS_JSON), file=sys.stderr)
        sys.exit(1)

    # Match scores to skill entries by name
    updated = 0
    for skill_entry in catalog.get("skills", []):
        slug = skill_entry["name"]
        category = skill_entry.get("category", "")

        # Try to find matching result
        key = "{}/{}".format(category, slug)
        if key in results:
            skill_entry["score"] = results[key]
            updated += 1
        else:
            # Try slug-only match
            for res_key, res_val in results.items():
                if res_key.endswith("/{}".format(slug)):
                    skill_entry["score"] = res_val
                    updated += 1
                    break

    # Write updated catalog
    with open(SKILLS_JSON, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print("\nUpdated {}/{} skill entries in {}".format(
        updated, len(catalog.get("skills", [])), SKILLS_JSON), file=sys.stderr)


if __name__ == "__main__":
    main()
