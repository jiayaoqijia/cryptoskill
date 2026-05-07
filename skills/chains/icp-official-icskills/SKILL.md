---
name: icp-official-icskills
description: "> **Under active development** — Skill files are being reviewed and signed off by DFINITY engineers. Content may change. Feedback and PRs are welcome."
---

# icp-official-icskills

_Source: [github.com/dfinity/icskills](https://github.com/dfinity/icskills). The body below is the upstream README.md captured at the time of registration._

---

# Internet Computer (ICP) Skills

> **Under active development** — Skill files are being reviewed and signed off by DFINITY engineers. Content may change. Feedback and PRs are welcome.

**Agent-readable instructions for every IC need.**

Structured, agent-readable skill files for every Internet Computer capability. Your AI reads the skill. It builds correctly. No hallucinations.

---

## The Problem

AI agents building on the Internet Computer hallucinate canister IDs, use deprecated APIs, and miss critical pitfalls. Traditional documentation is written for humans to browse — not for agents to consume programmatically.

## The Solution

Each skill is a single markdown file containing everything an agent needs to build correctly:

```
skills/ckbtc/SKILL.md
skills/internet-identity/SKILL.md
skills/stable-memory/SKILL.md
...
```

Every skill typically includes:

| Section | Purpose |
|---------|---------|
| **What This Is** | One paragraph. What the technology does. |
| **Prerequisites** | Exact library versions. `ic-cdk >= 0.19`, `@icp-sdk/auth >= 4.0.1`. |
| **Common Pitfalls** | Numbered pitfalls that prevent hallucinations. |
| **Implementation** | Tested, copy-paste-correct code blocks. |
| **Deploy & Test** | Step-by-step commands for local and mainnet. |
| **Verify It Works** | Concrete commands to confirm it works. |

Skills can include additional sections (Canister IDs, How It Works, etc.) and use whatever headings best fit their domain. The pitfalls section is the highest-value part — every pitfall documented is a hallucination prevented.

## Skills

All skills live in [`skills/*/SKILL.md`](skills/). Each skill is a self-contained markdown file with YAML frontmatter.

## Usage

### Install via CLI

Works with any agent that supports skills (Claude Code, Cursor, Windsurf, Copilot, and more):

```bash
npx skills add dfinity/icskills
```

Browse available skills, pick your agent, and install. See [skills.sh](https://skills.sh) for details.

### Manual

Fetch a single skill and place it wherever your agent reads instructions from:

```bash
curl -sL https://skills.internetcomputer.org/.well-known/skills/ckbtc/SKILL.md
```

The files are plain markdown — paste into any system prompt, rules file, or context window.

## Programmatic Access

| Resource | URL | Description |
|----------|-----|-------------|
| Skills discovery | [`.well-known/skills/index.json`](https://skills.internetcomputer.org/.well-known/skills/index.json) | Machine-readable skill index ([Agent Skills Discovery RFC](https://github.com/cloudflare/agent-skills-discovery-rfc)) |
| Single skill | `/.well-known/skills/{name}/SKILL.md` | Raw markdown for one skill |
| Reference files | `/.well-known/skills/{name}/references/{file}.md` | Additional files listed in the discovery index |
| Download (zip) | `/.well-known/skills/{name}/SKILL.zip` | Zip bundle for multi-file skills (SKILL.md + references) |
| Skill index | [`llms.txt`](https://skills.internetcomputer.org/llms.txt) | All skills with descriptions and discovery links |
| Skill page | [`/skills/{name}/`](https://skills.internetcomputer.org/skills/ckbtc/) | Pre-rendered skill page for humans |

## Evaluations

Each skill can have an evaluation file at `evaluations/<skill-name>.json` that tests whether agents produce correct output with the skill loaded. Evals compare agent output with and without the skill, using an LLM judge to score expected behaviors.

```bash
node scripts/evaluate-skills.js <skill-name>                    # All evals
node scripts/evaluate-skills.js <skill-name> --eval 2            # Single eval
node scripts/evaluate-skills.js <skill-name> --no-baseline       # Skip without-skill baseline
node scripts/evaluate-skills.js <skill-name> --triggers-only     # Trigger evals only
```

Results are saved to `evaluations/results/` (gitignored). See [CONTRIBUTING.md](CONTRIBUTING.md#4-add-evaluation-cases) for how to write eval cases and prompts.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add or update skills.

**All PRs require repo admin approval.** One skill per PR. Code examples must be tested.

## Tech Stack

- **Site**: [Astro](https://astro.build/) — static site generator, zero JS by default. Interactive islands with [Preact](https://preactjs.com/) (~18kb gzipped total)
- **Hosting**: IC asset canister at [`skills.internetcomputer.org`](https://skills.internetcomputer.org)
- **Skills**: Plain markdown files in `skills/*/SKILL.md`
- **Validation**: [`skill-validator`](https://github.com/agent-ecosystem/skill-validator) for structure, links, content analysis, and contamination checks (`npm run validate`)
- **Evaluation**: Per-skill eval cases with LLM-as-judge scoring (`node scripts/evaluate-skills.js <skill>`)
- **Schema**: JSON Schema for frontmatter at `skills/skill.schema.json`
- **SEO**: Per-skill meta tags, JSON-LD (TechArticle), sitemap, canonical URLs
- **Skills Discovery**: `llms.txt`, `.well-known/skills/` ([Skills Discovery RFC](https://github.com/cloudflare/agent-skills-discovery-rfc))

## License

Apache-2.0
