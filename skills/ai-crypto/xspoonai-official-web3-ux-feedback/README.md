# web3-ux-feedback

> An AI agent skill that evaluates web3 project landing pages across UX design
> and marketing messaging, then generates copy-ready landing page redesign concepts.

## What This Skill Does

This skill enables an AI agent to act as a senior UX + marketing strategist for
web3 projects. It combines two disciplines in a single analysis pass:

**1. Frontend/UX Evaluation**
Visual design, layout, user flow, trust signals, and web3-specific UI patterns —
wallet connection UX, gas fee transparency, chain identification, jargon
accessibility, security badges.

**2. Messaging Analysis**
Value proposition clarity, ICP targeting, competitive positioning, and narrative
flow using the **5-part SaaS Messaging Framework** adapted for web3.

The output is a structured feedback report plus **2–3 complete landing page
redesign concepts** with specific, copy-ready content — not vague suggestions.

---

## Why Frontend Only?

An AI agent cannot safely execute wallet connections, real transactions, or
smart contract interactions. The frontend is the right scope because:

- Users decide within 5 seconds whether to stay or leave
- Landing page improvements require no backend changes
- Most web3 projects lose users at the landing page, not inside the app

---

## The Messaging Framework

The skill applies the **5-Part SaaS Messaging Framework** adapted for web3:

| Part | Key Question |
|------|-------------|
| 1. Market | What's changing that makes this project relevant now? |
| 2. ICP | Who *specifically* is this for? |
| 3. Competitive Alternatives | What would users do without this? |
| 4. Product | What can users *do* now they couldn't before? (capabilities, not features) |
| 5. Value Proposition | What's the measurable outcome + proof? |

The key insight driving the framework: **messaging ≠ copy**. Messaging is WHAT
you say. Copy is HOW you say it. A beautifully written headline about the wrong
thing is still wrong.

---

## Output

Every analysis produces:

1. **Executive Summary** — biggest opportunity + most critical fix in 2–3 sentences
2. **UX/Frontend Evaluation** — strengths, critical issues (with fixes), quick wins
3. **Messaging Analysis** — gap analysis across all 5 framework parts
4. **Landing Page Redesign Concepts** — 2–3 complete alternatives with:
   - Full hero section (H1, H2, primary CTA, secondary CTA, trust line, visual direction)
   - Problem section with 3 pain points
   - Capabilities section (feature → capability → benefit)
   - Social proof recommendations
   - CTA strategy across the full page
5. **Prioritized Action Plan** — ranked by impact/effort
6. **Competitive Inspiration** — examples from successful web3 projects

---

## Usage

### With Claude Code

```bash
cp -r web3-ux-feedback/ ~/.claude/skills/
```

Then in your project:
```
Review this web3 project's landing page: [URL or description]
```

### With SpoonOS

```bash
cp -r web3-ux-feedback/ ~/.agent/skills/
python your_agent.py
```

### Trigger Phrases

The skill activates on prompts like:
- "Review this web3 landing page"
- "Give me feedback on this DeFi project's homepage"
- "What's wrong with my NFT marketplace messaging?"
- "Create landing page alternatives for this DAO tool"
- "Why isn't my web3 project converting visitors?"

---

## Scripts

### `scripts/main_tool.py`

Prepares a web3 landing page URL for analysis — fetches metadata, extracts
visible text content, and structures it for the agent's evaluation pass.

```bash
python scripts/main_tool.py --url https://yourproject.xyz
```

### `scripts/helper.py`

Scoring utilities — calculates UX and messaging scores, generates the
prioritized action plan table, and formats the output report structure.

---

## References

### `references/messaging-framework.md`

Full 5-part SaaS Messaging Framework with web3-specific examples, the
feature → capability → benefit ladder explained, and common messaging
anti-patterns for DeFi, NFT, DAO, and L2 projects.

### `references/web3-ux-patterns.md`

Web3 UI/UX best practices and anti-patterns organized by project type
(DeFi, NFT marketplace, DAO tooling, Layer 2, GameFi). Includes a curated
list of successful web3 landing pages and what they do well.

---

## Project Types Supported

| Type | Key Evaluation Focus |
|------|---------------------|
| DeFi / DEX | TVL display, audit badges, fee transparency, chain support |
| NFT Marketplace | Creator vs. collector ICP, royalty stance, visual NFT display |
| DAO Tooling | Governance clarity, target DAO type, proposal flow |
| Layer 2 | Speed/cost comparison, ecosystem apps, bridge UX |
| GameFi | Lead with fun not tokens, onboarding simplicity, ownership clarity |

---

## Track

`ai-productivity` — This skill automates intelligent UX and marketing analysis
work. The agent does not execute on-chain transactions.

---

## License

MIT