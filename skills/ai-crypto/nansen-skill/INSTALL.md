# Install Nansen

This repository is a generated single-skill distribution of [https://github.com/Vo1ganin/crypto-claude-skills](https://github.com/Vo1ganin/crypto-claude-skills).

## Claude Code

```bash
tmp="$(mktemp -d)"
git clone --depth 1 https://github.com/Vo1ganin/nansen-skill.git "$tmp/repo"
rm -rf "$HOME/.claude/skills/nansen"
mkdir -p "$HOME/.claude/skills"
cp -R "$tmp/repo" "$HOME/.claude/skills/nansen"
rm -rf "$HOME/.claude/skills/nansen/.git" "$tmp"
```

Restart Claude Code after installation. Re-running the commands replaces the prior generated copy rather than nesting another directory.

## Other agents

Use `SKILL.md` as task-scoped instructions only where your agent supports that convention. Agent behavior differs; do not assume automatic discovery without checking that agent's documentation.

## API configuration

Copy `.env.example` to a private environment file outside Git, or export only the variables you need. Never paste credentials into prompts, screenshots, examples, or committed files.

## Update / uninstall

Update by repeating the installation steps. Uninstall with:

```bash
rm -rf "$HOME/.claude/skills/nansen"
```
