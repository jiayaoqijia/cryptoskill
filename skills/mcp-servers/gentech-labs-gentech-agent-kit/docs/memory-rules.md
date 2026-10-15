# Memory Rules — GenTech Agent Kit

## When to Save to Memory

### Always Save
- User preferences and corrections
- Environment details (OS, tools, quirks)
- Stable conventions and patterns
- Important discoveries

### Never Save
- Task progress or session outcomes
- Temporary TODO state
- Stale data (will be outdated in a week)
- Procedural knowledge (save as skill instead)

## Memory vs Skills

| Type | Use For | Example |
|------|---------|---------|
| **Memory** | Facts about the user or environment | "User prefers concise responses" |
| **Skills** | Behavioral patterns and workflows | "How to deploy to GitHub Pages" |

### Rule of Thumb
If you'll do it again, save it as a **skill**. If it's a fact about the user, save it to **memory**.

## Memory Bar Rules

- **Below 80%:** Don't show the memory bar
- **80-100%:** Show `[🧠 XX%]` in responses
- **Above 95%:** Consolidate memory entries immediately

## Session Start Protocol

1. Read latest Mess Hall file for context
2. Check `09-Green Room/ideas.md` and `11-Mess Hall/considerations.md`
3. Search sessions if user references something from before
4. Don't ask the user to repeat themselves — find it in the vault first

## Session End Protocol

1. Write handoff note to `11-Mess Hall/YYYY-MM-DD-handoff.md`
2. Log any ideas or insights to Mess Hall
3. Update memory with new facts or preferences
4. Save any discovered workflows as skills

## Cleanup Rules

- **Weekly:** Consolidate duplicate memory entries
- **Monthly:** Remove stale entries (outdated in 30+ days)
- **Always:** Keep memory under 90% capacity
