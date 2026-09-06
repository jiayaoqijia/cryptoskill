# Sui Dev Skills

A collection of Claude skills for Sui development. Each skill is modular and can be used independently or composed together for full-stack Sui projects.

## Skills

| Skill | Description | Status |
|-------|-------------|--------|
| [`move/`](./move/) | Idiomatic Move on Sui — object model, modern syntax, testing | ✅ Ready |
| [`sui-ts-sdk/`](./sui-ts-sdk/) | TypeScript SDK v2 — PTB construction, client setup, transaction execution, on-chain queries | ✅ Ready |
| [`sui-frontend/`](./sui-frontend/) | Frontend integration — dApp Kit, wallet connection, React hooks, on-chain queries from the browser | ✅ Ready |

## Installation

### Global install (recommended — works across all your projects)

```bash
git clone https://github.com/MystenLabs/sui-dev-skills ~/.claude/skills/sui-dev-skills
```

Claude Code auto-discovers skills in `~/.claude/skills/` and activates them automatically based on context.

### Project-local install (commit to your repo)

```bash
git clone https://github.com/MystenLabs/sui-dev-skills .claude/skills/sui-dev-skills
```

Commit it to share the skill with your whole team — anyone who opens the project in Claude Code gets it automatically.

### Composing skills

For full-stack Sui dapps, install all skills and Claude will activate whichever are relevant. You can also pin specific skills in your `CLAUDE.md`:

```markdown
# My Sui Dapp

@~/sui-dev-skills/move/SKILL.md
@~/sui-dev-skills/sui-ts-sdk/SKILL.md
@~/sui-dev-skills/sui-frontend/SKILL.md
```

Claude reads all referenced skills before starting work, so it will apply conventions from all of them.

## Running evals

Requires [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview).

Each skill has its own `evals/evals.json`. To evaluate a skill, run Claude Code from this repo's parent directory:

```bash
cd ~/  # parent of sui-dev-skills/
claude
```

Then tell Claude:
> "Use the skill-creator to run evals on the skill at `./sui-dev-skills/move/`"
>
> Or for the TypeScript SDK skill:
> "Use the skill-creator to run evals on the skill at `./sui-dev-skills/sui-ts-sdk/`"
>
> Or for the frontend skill:
> "Use the skill-creator to run evals on the skill at `./sui-dev-skills/sui-frontend/`"

Eval workspace outputs are written to a sibling directory (e.g. `move-workspace/`) and are gitignored.

## Contributing

PRs welcome for:
- New skills (SDK, frontend, indexer, zkLogin, etc.)
- Improvements to existing skills
- Additional evals and benchmark prompts
- Verified real-world examples