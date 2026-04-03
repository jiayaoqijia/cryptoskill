# CryptoSkill Evaluation Framework

## Design Philosophy

Evaluation should be **cheap by default, deep when it matters**. Most of the 800+ skills can be scored with static analysis (zero LLM cost). Only fund-moving skills (exchanges, DeFi, wallets, trading) need expensive LLM-as-judge evaluation. The framework produces a single **0-100 Quality Score** per skill, decomposed into transparent dimensions.

Inspired by: npm quality scores, Minara crypto-skill-benchmark, ClawHub repository context scoring, SkillsMP maintenance tiers, GoPlus/AgentGuard security scanning, and Chrome Web Store ratings.

---

## Score Architecture

```
Quality Score (0-100) = Static Score (40%) + Security Score (20%) + Depth Score (40%)
```

| Component | Cost | Runs | Coverage |
|-----------|------|------|----------|
| **Static Score** | Free | Every bot cycle (6h) | All 800+ skills |
| **Security Score** | Free | Every bot cycle (6h) | All 800+ skills |
| **Depth Score** | ~$0.10/skill | On change or weekly | Fund-moving skills get LLM judge; others get heuristic |

---

## Layer 1: Static Score (40 points max)

Computed purely from file analysis. No LLM, no API calls. Runs on every skill every 6 hours.

### Dimensions

| Dimension | Points | How Computed |
|-----------|--------|--------------|
| **Documentation** | 10 | SKILL.md quality (see checklist below) |
| **Completeness** | 8 | Required files present (SKILL.md, SOURCE.md, references/) |
| **Freshness** | 7 | Last update recency (from git log or SOURCE.md) |
| **Provenance** | 8 | Official classification, GitHub org verification |
| **Structure** | 7 | Follows naming conventions, proper frontmatter |

### Documentation Checklist (10 points)

| Check | Points | Method |
|-------|--------|--------|
| SKILL.md exists | 1 | File check |
| Has valid YAML frontmatter (name, description) | 1 | YAML parse |
| Description > 50 chars | 1 | Length check |
| Has "When to Use" or trigger section | 1 | Text search |
| Has examples or usage section | 1 | Text search |
| Has references/ directory | 1 | Directory check |
| Word count > 200 (meaningful content) | 1 | Word count |
| Has version in frontmatter | 1 | YAML check |
| Has metadata.openclaw section | 1 | YAML check |
| No placeholder text ("TODO", "TBD", "Lorem") | 1 | Text search |

### Completeness (8 points)

| Check | Points |
|-------|--------|
| SKILL.md present | 2 |
| SOURCE.md present with all fields | 2 |
| references/ directory with at least 1 file | 2 |
| scripts/ directory (if skill is executable) | 1 |
| _meta.json present | 1 |

### Freshness (7 points)

Based on the source repo last commit date:

| Recency | Points |
|---------|--------|
| Within 1 month | 7 |
| Within 3 months | 5 |
| Within 6 months | 3 |
| Within 1 year | 1 |
| Older than 1 year | 0 |

### Provenance (8 points)

| Check | Points |
|-------|--------|
| Classification = OFFICIAL | 4 |
| Source GitHub org has 10+ public repos | 2 |
| Source repo has 5+ stars | 1 |
| License declared | 1 |

### Structure (7 points)

| Check | Points |
|-------|--------|
| Directory name is kebab-case | 1 |
| Official skills follow project-official-name pattern | 2 |
| Correct category placement | 2 |
| No hardcoded API keys or secrets in SKILL.md | 1 |
| Valid YAML frontmatter (parses without error) | 1 |

---

## Layer 2: Security Score (20 points max)

Static security analysis. No LLM needed. Flags critical issues.

### Dimensions

| Dimension | Points | How Computed |
|-----------|--------|--------------|
| **Credential Safety** | 6 | Regex scan for API keys, private keys, mnemonics |
| **Code Safety** | 6 | Scan scripts/ for dangerous patterns |
| **Permission Scope** | 4 | Analysis of allowed-tools in frontmatter |
| **Supply Chain** | 4 | External dependency count, URL destination checks |

### Security Gate (Binary)

Independent of score. A **FAIL** flag if any of:
- Private key or mnemonic pattern found in any file
- Dynamic code execution with user input in scripts
- Fetches to non-HTTPS URLs
- Obfuscated code detected (base64 encoded strings > 100 chars)

### Permission Risk Tiers

| Allowed Tools | Risk | Deduction |
|---------------|------|-----------|
| Read, Glob, Grep only | Low | 0 |
| + Edit, Write | Medium | -1 |
| + Bash | High | -2 |
| + Bash with network access | Critical | -3 |

---

## Layer 3: Depth Score (40 points max)

Two tracks depending on skill category:

### Track A: LLM-as-Judge (Fund-Moving Skills)

For categories: **exchanges, defi, trading, wallets, payments**

Uses the crypto-skill-benchmark methodology: send scenarios to an LLM simulating the skill, then judge responses.

| Dimension | Points | What it measures |
|-----------|--------|-----------------|
| **Safety** | 12 | Confirmation before fund moves, amount precision |
| **Coverage** | 10 | Breadth of operations and chains |
| **Robustness** | 8 | Adversarial input handling, scam detection |
| **Routing** | 6 | Intent-to-action mapping accuracy |
| **UX** | 4 | Output completeness |

**Scenario tiers:**
- **Basic** (5 scenarios): swap, send, balance, price, deposit ($0.05/skill)
- **Standard** (20 scenarios): + perps, limit orders, scam tokens ($0.15/skill)
- **Full** (76 scenarios): All core + adversarial ($3/skill)

### Track B: Heuristic Depth (Non-Fund-Moving Skills)

For categories: **chains, analytics, identity, prediction-markets, social, ai-crypto, dev-tools, mcp-servers**

No LLM needed. Scored by content analysis:

| Dimension | Points | How Computed |
|-----------|--------|--------------|
| **Actionability** | 12 | Has scripts/ or CLI commands? Has API endpoints documented? |
| **Specificity** | 10 | References specific contracts, addresses, or API URLs? |
| **Examples** | 8 | Has concrete usage examples with expected outputs? |
| **Error Handling** | 6 | Documents error cases, edge cases, limitations? |
| **Integration** | 4 | References other skills, MCP servers, or tools? |

### Category-Specific Bonus Dimensions

Certain categories get bonus checks (up to +5, capped at 40 total):

| Category | Bonus Check | Points |
|----------|-------------|--------|
| **MCP Servers** | Has install command (npm/docker/SSE URL) | +2 |
| **MCP Servers** | Has tool schema or endpoint documentation | +3 |
| **Analytics** | Cites data sources (APIs, contracts, subgraphs) | +3 |
| **Analytics** | Documents rate limits and freshness | +2 |
| **Identity** | References specific ERC standards | +2 |
| **Identity** | Documents privacy considerations | +3 |
| **Dev Tools** | Has build/test commands | +3 |
| **Dev Tools** | Documents supported chains/frameworks | +2 |

---

## Composite Score Formula

```
quality_score = static_score + security_score + depth_score
# Clamped to 0-100
```

### Grade Tiers

| Grade | Score | Badge | Meaning |
|-------|-------|-------|---------|
| **A** | 80-100 | Green | Production-ready, well-documented, secure |
| **B** | 60-79 | Blue | Good quality, minor gaps |
| **C** | 40-59 | Yellow | Usable but significant gaps |
| **D** | 20-39 | Orange | Minimal quality, use with caution |
| **F** | 0-19 | Red | Not recommended |

---

## Implementation Plan

### Phase 1: Static + Security Scoring (Week 1)
- Add `scripts/score-skills.py` to compute static + security scores
- Store scores in `docs/skills.json` per skill
- Run in bot cycle after catalog regeneration

### Phase 2: Website Display (Week 2)
- Score badge on skill cards (A/B/C/D/F with color)
- Safety gate indicator
- Sort/filter by score
- Tooltip with dimension breakdown

### Phase 3: LLM Depth Scoring (Week 3-4)
- Integrate crypto-skill-benchmark scenario runner
- Run basic tier for all fund-moving skills
- Update weekly

### Phase 4: Regression Tracking (Week 5+)
- JSONL history per skill
- Alert on score drops >10 points
- Score trend sparkline on website

---

## Cost Estimate

| Phase | Skills | Cost/Run | Frequency | Monthly |
|-------|--------|----------|-----------|---------|
| Static + Security | 800 | $0 | Every 6h | **$0** |
| Heuristic Depth | 500 | $0 | Every 6h | **$0** |
| LLM Basic (5 scenarios) | 300 | $0.05/skill | Weekly | **~$60** |
| LLM Standard (20 scenarios) | 50 | $0.15/skill | Monthly | **~$8** |

**Total monthly: ~$70**

---

## References

- [Minara crypto-skill-benchmark](https://github.com/Minara-AI/crypto-skill-benchmark) -- 76 scenarios, 5 dimensions, LLM-as-judge
- [ClawHub Repository Context Score](https://arxiv.org/html/2603.16572) -- Codebase (70%) + Metadata (30%)
- [SkillsMP Maintenance Tiers](https://skillsmp.com) -- Freshness-based trust indicators
- [GoPlus AgentGuard](https://agentguard.gopluslabs.io) -- Security scanning for AI agent skills
- [npm quality scores](https://docs.npmjs.com/about-package-search-ranking) -- Quality, maintenance, popularity
