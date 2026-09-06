---
name: self-evolve
description: "After completing a task that required improvisation (multi-step workflows, one-off scripts, API calls, complex shell commands), proactively package the successful approach into a reusable skill for next time. Also triggers when: (1) a task took many steps that could be simplified, (2) the same type of request has come up before, (3) an installed skill didn't work well and needs improvement."
---

# Self-Evolve

After completing a non-trivial task, check if the approach should become a reusable skill.

## When to Trigger

Ask yourself after each completed task:
- Did I write a multi-step workflow from scratch?
- Did I write a script that could be reused?
- Did I figure out an API or tool pattern that wasn't obvious?
- Has the user asked for something similar before?

If yes to any, offer to save it as a skill.

## Create a Skill

1. **Ask the user**: "I can save this as a reusable skill for next time. Want me to?"
2. If yes, create `workspace/skills/<name>/SKILL.md` with:

```markdown
---
name: <short-name>
description: "<what it does and when to use it>"
---

# <Title>

<Concise instructions the agent needs to reproduce this workflow>
```

3. If scripts were involved, save them to `workspace/skills/<name>/scripts/`

Keep skills minimal — only include what the agent can't figure out on its own.

## Improve an Existing Skill

If a skill was used but had issues (wrong commands, missing steps, outdated API):

1. Read the skill: `read_file(path="workspace/skills/<name>/SKILL.md")`
2. Fix the specific issue
3. Write the updated file

Don't rewrite working skills. Patch only what's broken.

## Rules

- **Ask first** — never auto-create skills without user consent
- **One skill per workflow** — don't create overlapping skills
- **No junk** — skip trivial one-liners the agent already knows
- **Check existing** — read `workspace/skills/` before creating duplicates
