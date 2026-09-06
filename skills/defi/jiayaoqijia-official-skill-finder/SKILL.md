---
name: skill-finder
description: "Automatically find, install, and activate skills when the user's request needs capabilities not currently available. Use when: (1) user asks to do something that requires tools/APIs/integrations not present in current skills, (2) user explicitly asks to find or install a skill, (3) user mentions a service/API/tool name that suggests a registry skill exists (e.g. 'binance', 'notion', 'jira', 'stripe'). Acts as the bootstrap skill that makes the agent self-extending."
---

# Skill Finder — Self-Extending Agent Bootstrap

Proactively search, install, and use skills from registries so the agent can handle requests beyond its current capabilities.

## When to Trigger

- User asks for something no current tool or skill can do
- User mentions a specific service/API/tool name (e.g. "binance", "notion", "slack", "stripe")
- User explicitly asks to find, search, or install a skill

## Workflow

### 1. Identify the Gap

Determine what capability is missing. Map the user's request to a search query:

- "Check my Binance balance" → query: `binance`
- "Create a Jira ticket" → query: `jira`
- "Send a Stripe invoice" → query: `stripe`
- "Translate this to Japanese" → query: `translation`

### 2. Search

Use the `find_skills` tool:

```
find_skills(query="<search term>", limit=5)
```

Tips:
- Use the service/tool name first: `find_skills(query="binance")`
- Try broader terms if specific ones return nothing: `find_skills(query="project management")` instead of `find_skills(query="jira")`

### 3. Evaluate Results

Pick the best match based on:
- **Relevance score** (higher = better match)
- **Summary** (does it solve the user's need?)

### 4. Install

Use the `install_skill` tool with the slug and registry from the search results:

```
install_skill(slug="<slug>", registry="<registry-name>")
```

The skill installs to `workspace/skills/<slug>/` and is auto-discovered within seconds.

### 5. Use the Skill

After installation, read the new skill's SKILL.md with `read_file`:

```
read_file(path="workspace/skills/<slug>/SKILL.md")
```

Then follow its instructions to fulfill the user's original request.

## Important

- **Don't over-install**: Only install when there's a clear need. Don't speculatively install skills.
- **Check first**: Review what skills are already available before searching.
- **Warn about credentials**: If a skill needs API keys or secrets, tell the user what's needed before proceeding.
- **Fallback**: If no suitable skill exists, inform the user and suggest alternatives.
