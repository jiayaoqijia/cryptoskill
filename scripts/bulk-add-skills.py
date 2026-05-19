#!/usr/bin/env python3
"""
Bulk-add candidate skills discovered by an autoresearch pass.

Each candidate is a tuple: (org, repo, category, slug, classification, branch).
For each one we:
  1. Fetch the canonical SKILL.md (or skill.md / SKILL.MD) from raw.githubusercontent
  2. Try a default branch if `branch` is None (master, main)
  3. Write skills/{category}/{slug}/SKILL.md
  4. Write SOURCE.md with classification, license guess, submitter
  5. Write _meta.json
  6. Append to a registration log so we can re-run idempotently

Run extract-capabilities.py + update-catalog.py + generate-pages.py
afterwards (this script does NOT regenerate; it only places files).

Usage:
  python3 scripts/bulk-add-skills.py
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
TODAY = "2026-05-08"

# (org, repo, category, slug, classification, branch_or_None,
#  skill_md_subpath_or_None, license_known)
CANDIDATES = [
    # ── 2026-05-08 community submissions ──
    ("coinpilot-labs", "skills", "ai-crypto",
     "coinpilot-hyperliquid-copy-trade", "COMMUNITY", "main",
     "coinpilot-hyperliquid-copy-trade/SKILL.md", "unspecified"),
    ("openocean-finance", "OpenOcean-skills", "defi",
     "openocean-official-multichain-token-swap", "OFFICIAL", "main",
     "SKILL.md", "unspecified"),
    # ── 2026-05-08 autoresearch pulse: high-confidence official adds ──
    ("smartcontractkit", "chainlink-agent-skills", "dev-tools",
     "chainlink-official-agent-skills", "OFFICIAL", "main",
     None, "MIT"),
    ("helius-labs", "core-ai", "dev-tools",
     "helius-official-core-ai", "OFFICIAL", "main",
     None, "MIT"),
    ("quiknode-labs", "blockchain-skills", "dev-tools",
     "quicknode-official-blockchain-skills", "OFFICIAL", "main",
     None, "MIT"),
    ("aptos-labs", "aptos-agent-skills", "chains",
     "aptos-official-agent-skills", "OFFICIAL", "main",
     None, "MIT"),
    ("sendaifun", "skills", "chains",
     "sendai-official-solana-skills", "OFFICIAL", "main",
     None, "Apache-2.0"),
    ("coinpaprika", "claude-marketplace", "analytics",
     "coinpaprika-official-claude-marketplace", "OFFICIAL", "main",
     None, "NOASSERTION"),
    ("crypto-com", "crypto-agent-trading", "exchanges",
     "cryptocom-official-agent-trading", "OFFICIAL", "main",
     None, "Apache-2.0"),
    ("blockscout", "agent-skills", "dev-tools",
     "blockscout-official-agent-skills", "OFFICIAL", "main",
     None, "MIT"),
    ("celo-org", "agent-skills", "chains",
     "celo-official-agent-skills", "OFFICIAL", "main",
     None, "Apache-2.0"),
    ("worldcoin", "agentkit", "identity",
     "worldcoin-official-agentkit", "OFFICIAL", "main",
     None, "MIT"),
    # ── Priority A: top brands + Anthropic-spotlighted ──
    ("trailofbits", "building-secure-contracts", "dev-tools",
     "trailofbits-official-building-secure-contracts", "OFFICIAL", "master",
     None, "AGPL-3.0"),
    ("trailofbits", "slither-mcp", "mcp-servers",
     "trailofbits-official-slither-mcp", "OFFICIAL", "main",
     None, "AGPL-3.0"),
    ("Polymarket", "agent-skills", "prediction-markets",
     "polymarket-official-agent-skills", "OFFICIAL", "main",
     None, "unspecified"),
    ("bybit-exchange", "skills", "exchanges",
     "bybit-official-skills", "OFFICIAL", "main",
     None, "MIT"),
    ("GMGNAI", "gmgn-skills", "trading",
     "gmgn-official-skills", "OFFICIAL", "main",
     None, "MIT"),
    ("bitget-wallet-ai-lab", "bitget-wallet-skill", "wallets",
     "bitget-wallet-official-skill", "OFFICIAL", "main",
     None, "MIT"),
    ("dfinity", "icskills", "chains",
     "icp-official-icskills", "OFFICIAL", "main",
     None, "Apache-2.0"),
    ("hashgraph", "hedera-agent-kit-js", "chains",
     "hedera-official-agent-kit-js", "OFFICIAL", "main",
     None, "Apache-2.0"),
    ("InjectiveLabs", "mcp-server", "mcp-servers",
     "injective-official-mcp-server", "OFFICIAL", "main",
     None, "unspecified"),
    ("celo-org", "celo-mcp", "mcp-servers",
     "celo-official-mcp", "OFFICIAL", "main",
     None, "NOASSERTION"),
    ("drpcorg", "drpc-agent-skills", "dev-tools",
     "drpc-official-agent-skills", "OFFICIAL", "main",
     None, "MIT"),
    ("chainstacklabs", "rpc-nodes-mcp", "mcp-servers",
     "chainstack-official-rpc-nodes-mcp", "OFFICIAL", "main",
     None, "Apache-2.0"),
    ("onflow", "flow-mcp", "mcp-servers",
     "flow-official-mcp", "OFFICIAL", "main",
     None, "MIT"),
    ("xmtp", "skills", "social",
     "xmtp-official-skills", "OFFICIAL", "main",
     None, "unspecified"),
    ("duneanalytics", "skills", "analytics",
     "dune-official-skills", "OFFICIAL", "main",
     "skills/dune/SKILL.md", "MIT"),

    # ── Priority B: high-quality community MCPs (kukapay, bankless, etc.) ──
    ("kukapay", "crypto-feargreed-mcp", "mcp-servers",
     "kukapay-crypto-feargreed-mcp", "COMMUNITY", "main",
     None, "MIT"),
    ("kukapay", "cryptopanic-mcp-server", "mcp-servers",
     "kukapay-cryptopanic-mcp", "COMMUNITY", "main",
     None, "MIT"),
    ("kukapay", "crypto-indicators-mcp", "mcp-servers",
     "kukapay-crypto-indicators-mcp", "COMMUNITY", "main",
     None, "MIT"),
    ("kukapay", "uniswap-trader-mcp", "mcp-servers",
     "kukapay-uniswap-trader-mcp", "COMMUNITY", "main",
     None, "MIT"),
    ("kukapay", "hyperliquid-info-mcp", "mcp-servers",
     "kukapay-hyperliquid-info-mcp", "COMMUNITY", "main",
     None, "MIT"),
    ("bankless", "onchain-mcp", "mcp-servers",
     "bankless-onchain-mcp", "COMMUNITY", "main",
     None, "MIT"),
    ("magnetai", "mcp-free-usdc-transfer", "payments",
     "magnetai-free-usdc-transfer-mcp", "COMMUNITY", "main",
     None, "MIT"),

    # ── Priority C: aelf ecosystem coordinated rollout ──
    ("AElfProject", "aelf-skills", "chains",
     "aelf-official-skills", "OFFICIAL", "main",
     None, "unspecified"),
    ("AelfScanProject", "aelfscan-skill", "analytics",
     "aelfscan-official-skill", "OFFICIAL", "main",
     None, "MIT"),
    ("Awaken-Finance", "awaken-agent-skills", "defi",
     "awaken-official-agent-skills", "OFFICIAL", "master",
     None, "MIT"),
    ("TomorrowDAOProject", "tomorrowDAO-skill", "defi",
     "tomorrowdao-official-skill", "OFFICIAL", "main",
     None, "MIT"),
    ("Portkey-Wallet", "ca-agent-skills", "wallets",
     "portkey-official-ca-agent-skills", "OFFICIAL", "main",
     None, "MIT"),

    # ── Priority D: more brands ──
    ("aibtcdev", "aibtc-mcp-server", "mcp-servers",
     "aibtc-official-mcp-server", "OFFICIAL", "main",
     None, "unspecified"),
    ("ChainGPT-org", "chaingpt-claude-skill", "ai-crypto",
     "chaingpt-official-claude-skill", "OFFICIAL", "main",
     None, "MIT"),
    ("XSpoonAi", "spoon-awesome-skill", "ai-crypto",
     "spoonos-official-awesome-skill", "OFFICIAL", "master",
     None, "unspecified"),
    ("aicoincom", "coinos-skills", "analytics",
     "aicoin-official-coinos-skills", "OFFICIAL", "main",
     None, "MIT"),
    ("reown-com", "skills", "wallets",
     "reown-official-skills", "OFFICIAL", "main",
     "skills/appkit/SKILL.md", "unspecified"),
    ("EmblemCompany", "Agent-skills", "ai-crypto",
     "emblem-official-agent-skills", "OFFICIAL", "main",
     None, "MIT"),
]


def fetch_skill_md(org, repo, branch, subpath, slug, fallback_desc=""):
    """Try to fetch SKILL.md / skill.md from the repo. subpath overrides.
    Falls back to README.md and wraps it with synthesized frontmatter so
    the existing extractor and update-catalog can ingest it."""
    skill_md_paths = []
    if subpath:
        skill_md_paths.append(subpath)
    skill_md_paths += [
        "SKILL.md", "skill.md", "Skill.md", "SKILL.MD",
        "openclaw-skill/SKILL.md", "claude-skills/SKILL.md",
        ".claude/skills/SKILL.md", "agents/SKILL.md",
        "skill/SKILL.md", "claude-skill/SKILL.md",
    ]
    readme_paths = ["README.md", "readme.md", "README.MD", "Readme.md"]
    branches = [branch] if branch else ["main", "master"]
    headers = {"User-Agent": "cryptoskill-autoresearch/1.0"}

    def _try(path, br):
        url = f"https://raw.githubusercontent.com/{org}/{repo}/{br}/{path}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as r:
                if r.status == 200:
                    return url, r.read().decode("utf-8", errors="replace")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            pass
        return None, None

    # First pass: real SKILL.md anywhere
    for br in branches:
        for path in skill_md_paths:
            url, body = _try(path, br)
            if body:
                return url, body, "skill_md"

    # Second pass: README.md, wrapped in synthesized frontmatter so the
    # parser sees a valid SKILL.md shape.
    for br in branches:
        for path in readme_paths:
            url, body = _try(path, br)
            if not body:
                continue
            # Pull a one-line description from the first non-blank prose line.
            desc = fallback_desc
            for line in body.splitlines():
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("!["):
                    continue
                if line.startswith("<") or line.startswith("```"):
                    continue
                desc = line[:300]
                break
            desc = desc.replace('"', "'").replace("\n", " ").replace("\r", " ").strip()
            # Guard against YAML block-scalar openers ("|", ">", "|-", ">-").
            # If the first prose line begins with one of these, the canonical
            # YAML parser interprets the description as a multiline block,
            # which breaks the frontmatter shape. Prefix a space so the
            # description stays a single-quoted scalar.
            if desc and desc[0] in ("|", ">"):
                desc = " " + desc
            if not desc:
                desc = f"Skill from {org}/{repo}; see linked README for details."
            wrapped = (
                "---\n"
                f"name: {slug}\n"
                f'description: "{desc}"\n'
                "---\n\n"
                f"# {slug}\n\n"
                f"_Source: [github.com/{org}/{repo}](https://github.com/{org}/{repo}). "
                "The body below is the upstream README.md captured at the time of registration._\n\n"
                "---\n\n"
                + body
            )
            return url, wrapped, "readme_wrapped"

    return None, None, None


def write_source_md(target_dir, org, repo, classification, license_known,
                    submitter, source_url):
    target_dir.mkdir(parents=True, exist_ok=True)
    body = f"""# Source Attribution

- **Original Author**: {org}
- **Source**: https://github.com/{org}/{repo}
- **Source URL**: {source_url}
- **License**: {license_known}
- **Classification**: {classification}
- **Discovered**: {TODAY} (autoresearch pass)
"""
    if submitter:
        body += f"- **Submitter**: {submitter}\n"
    (target_dir / "SOURCE.md").write_text(body, encoding="utf-8")


def write_meta_json(target_dir, slug, org, repo, branch):
    body = {
        "name": slug,
        "owner": org,
        "version": "1.0.0",
        "added_at": TODAY,
        "source_repo": f"{org}/{repo}",
        "source_url": f"https://github.com/{org}/{repo}",
        "source_branch": branch or "main",
        "tags": [],
        "history": [{
            "version": "1.0.0",
            "added_at": TODAY,
            "note": "Initial bulk-add via autoresearch pass."
        }],
    }
    (target_dir / "_meta.json").write_text(
        json.dumps(body, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    added, skipped, failed = 0, 0, 0
    log = []
    for tup in CANDIDATES:
        org, repo, cat, slug, cls, branch, subpath, lic = tup
        target = SKILLS_DIR / cat / slug
        if (target / "SKILL.md").exists():
            skipped += 1
            log.append(f"SKIP    {slug}  (already present)")
            continue
        url, content, kind = fetch_skill_md(org, repo, branch, subpath, slug)
        if not url:
            failed += 1
            log.append(f"FAIL    {slug}  (no SKILL.md or README.md at {org}/{repo})")
            continue
        target.mkdir(parents=True, exist_ok=True)
        (target / "SKILL.md").write_text(content, encoding="utf-8")
        write_source_md(target, org, repo, cls, lic,
                        f"autoresearch ({kind})",
                        url)
        write_meta_json(target, slug, org, repo, branch)
        added += 1
        tag = "ADD" if kind == "skill_md" else "ADD-rd"
        log.append(f"{tag:8s}{slug}  ←  {url[len('https://raw.githubusercontent.com/'):][:60]}")
    print("\n".join(log))
    print()
    print(f"Result: {added} added, {skipped} skipped (already present), {failed} failed.")


if __name__ == "__main__":
    main()
