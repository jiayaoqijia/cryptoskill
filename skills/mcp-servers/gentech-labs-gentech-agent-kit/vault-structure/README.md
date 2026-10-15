# GenTech Agent Kit — Vault Structure

This is the standard vault structure for GenTech-compatible agents.

## Directory Layout

```
your-vault/
├── 00-HQ/                    # Main coordination
│   ├── INDEX.md              # Master index
│   └── decisions.md          # Key decisions log
│
├── 01-Agency/                # Agency operations
│   └── working/              # Active work
│
├── 06-Security/              # Security and audits
│   └── audits/               # Audit logs
│
├── 08-Daily/                 # Daily notes
│   └── YYYY-MM-DD.md         # Daily summaries
│
├── 09-Green Room/            # Ideas and brainstorming
│   ├── ideas.md              # Checkbox list of things to explore
│   └── designs/              # Design documents
│
├── 11-Mess Hall/             # Scratchpad and thinking
│   ├── considerations.md     # Decisions to make
│   ├── YYYY-MM-DD-handoff.md # Session handoff notes
│   └── archive/              # Old scratchpads
│
├── Cookbook/                  # User-specific content
│   ├── cookbook-dashboard-data.json
│   └── christel-journal.json
│
├── Labs/                     # Technical experiments
│   └── Design-Assets/        # Design resources
│
├── Strategies/               # Business strategies
│   └── DeFi-Monitor/         # DeFi monitoring
│
├── Archive/                  # Historical content
│   └── dashboard-concepts/   # Old concepts
│
└── INDEX.md                  # Master navigation
```

## File Naming Conventions

- **Daily notes:** `YYYY-MM-DD.md`
- **Handoff notes:** `YYYY-MM-DD-handoff.md`
- **Context snapshots:** `YYYY-MM-DD-context-snapshot.md`
- **Ideas:** `ideas.md` (single file, checkbox format)
- **Considerations:** `considerations.md` (single file, checkbox format)

## Key Files

### INDEX.md
Master navigation file. Should link to all major sections.

### ideas.md
Checkbox list of things to explore. Format:
```markdown
- [ ] Idea 1
- [ ] Idea 2
- [x] Completed idea
```

### considerations.md
Checkbox list of decisions to make. Format:
```markdown
- [ ] Decision 1
- [ ] Decision 2
- [x] Made decision
```

### Handoff Notes
Session handoff notes for context preservation. Format:
```markdown
# Session Handoff — YYYY-MM-DD

## Working On
- What we were doing

## Decisions Made
- Choices made

## Open Threads
- Things not finished

## Next Steps
- What to do next

## Files Modified
- List of changes
```

### Inter-Agent Handoff (full mesh)
Beyond session notes, agents hand work to each other via the vault's
`01-HANDOFFS/INBOX/<target>/` folders. **Any agent can initiate a handoff to any
peer** (Forge, Labs, Treasury, Entertainment, HQ) — not just respond to one. To
send work onward, write a dated `<YYYY-MM-DD>-<topic>.md` note into
`INBOX/<target>/` with `**From:** <you>`, `**To:** <target>`, `**Status:** open`,
and a `## What's needed` section, then commit + push. Never hand off to a peer
without writing the note to their INBOX folder — the watcher and the target's
wake trigger surface it from there. On completion, report back to the original
sender's return lane with three sections: `## ✅ What was done`,
`## 📌 What you should know`, `## ⏭️ What's next`.

## Rules

1. **Green Room** = ideas only, not active work
2. **Mess Hall** = thinking space, scratchpad, not final docs
3. **Archive** = old content, not current
4. **Daily** = daily summaries, not raw notes
5. **Handoffs** = context preservation, not task lists
