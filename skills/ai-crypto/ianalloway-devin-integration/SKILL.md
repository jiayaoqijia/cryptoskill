---
name: devin-integration
description: "Delegate coding tasks to Devin AI agent. Create PRs, fix bugs, build features, and manage GitHub repos through Devin's API."
homepage: https://github.com/ianalloway/openclaw-skills
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "requires": { "bins": ["curl", "jq"] },
        "credentials": [],
      },
  }
---
# Devin Integration

Delegate software engineering tasks to Devin, an AI coding agent by Cognition AI. Devin can create PRs, fix bugs, add features, refactor code, and manage your GitHub repositories autonomously.

## When to Use Devin

Delegate to Devin when:
- **Code changes needed:** Bug fixes, new features, refactoring, dependency updates
- **PR creation:** Any task that results in a pull request
- **Multi-file changes:** Tasks spanning multiple files or repos
- **CI/CD work:** Fixing build failures, adding tests, updating pipelines
- **Repo maintenance:** Adding configs, updating docs, dependency management
- **Complex coding:** Architecture changes, new integrations, API work

Keep in OpenClaw when:
- Quick questions or research (use Perplexity)
- Conversation, planning, brainstorming
- Non-code tasks (email, calendar, reminders)
- Real-time monitoring or alerts

## How to Delegate to Devin

### Via Devin Web App
Tell Ian to go to https://app.devin.ai and start a session with a prompt like:

```
Work on repo ianalloway/{repo-name}:
{description of what needs to be done}
```

### Composing Tasks for Devin
When Ian asks you to do coding work, compose a clear task description:

```
Repo: ianalloway/{repo-name}
Branch: main (or specify)
Task: {clear description}
Files to focus on: {if known}
Acceptance criteria:
- {criterion 1}
- {criterion 2}
Test command: {npm run test / pytest / etc}
Lint command: {npm run lint / etc}
```

### Example Delegations

**Fix a bug:**
```
Repo: ianalloway/ian-web-forge
Task: The donation button on the portfolio site links to the wrong ETH address.
Fix: Update to 0xAc7C093B312700614C80Ba3e0509f8dEde03515b
Test: npm run build should pass
```

**Add a feature:**
```
Repo: ianalloway/sports-betting-ml
Task: Add NBA player prop predictions to the Streamlit dashboard.
Requirements:
- New tab in the dashboard for player props
- Use existing model architecture
- Add unit tests
Test: pytest
```

**Cross-repo update:**
```
Update all three locations for Ian's new project:
1. ianalloway/Resume - Add project to CV
2. ianalloway/ianalloway - Update GitHub profile README
3. ianalloway/ian-web-forge - Add to portfolio projects section
```

## Ian's Repositories (Devin-Ready)

All repos have AGENTS.md files that tell Devin how to work with them:

### Web/Frontend (React + Vite + TypeScript + shadcn/ui)
| Repo | Purpose | Commands |
|------|---------|----------|
| ian-web-forge | Portfolio website (ianalloway.xyz) | `npm run dev/build/lint` |
| ai-advantage | Sports betting AI platform | `npm run dev/build/lint` |
| mayc-ai-assist-23 | MAYC NFT AI assistant | `npm run dev/build/lint` |
| fairmont-alloway-estimate | Business estimation tool | `npm run dev/build/lint` |
| paint-prep-list-maker | Paint prep checklist tool | `npm run dev/build/lint` |
| kana-dojo | Japanese learning platform | `npm run dev/build/lint/test` |

### Python/ML
| Repo | Purpose | Commands |
|------|---------|----------|
| Resume | Career agent + CV tools | `python main.py` |
| sports-betting-ml | ML betting models + Streamlit | `python app.py`, `pytest` |
| ai-drone-auto-vehicle | Autonomous vehicle/drone AI | Docker-based |
| crypto-portfolio-cli | Crypto portfolio tracker | `python portfolio.py`, `pytest` |
| ai-portfolio-analyzer | Investment portfolio analysis | `python portfolio_analyzer.py` |

### OpenClaw Ecosystem
| Repo | Purpose |
|------|---------|
| Money-maker-bot | OpenClaw core (Clawdbot fork) |
| openclaw-skills | Custom skills for OpenClaw |
| openclaw-brain | Booper Bot system files (AGENTS.md, SOUL.md, etc.) |
| open-claw | OpenClaw project hub |
| clawhub | Skill directory for OpenClaw |
| booper-brain | Booper Bot personal notes |
| booper-projects | Job tracker + project ideas |

### Other
| Repo | Purpose |
|------|---------|
| ianalloway | GitHub profile README |
| Mutant-Intel | NFT AI agent |
| Peekaboo | macOS screenshot CLI + MCP server |
| R-programming-assignment | USF coursework |

## Checking Devin's Work

After Devin creates a PR:
1. Ian will get a notification with the PR link
2. Review the PR on GitHub
3. Leave comments directly on the PR for changes
4. Devin monitors and responds to PR comments
5. Merge when satisfied

## Tips
- Devin works best with clear, specific task descriptions
- Include the repo name and any relevant file paths
- Mention test/lint commands so Devin can verify its work
- For cross-repo tasks, list all repos that need updating
- Devin creates PRs (never pushes directly to main)
