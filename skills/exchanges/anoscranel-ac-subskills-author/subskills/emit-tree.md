---
name: emit-tree
domain: skill-authoring/emit-tree
trigger: After flat-or-nest — write the SKILL.md and subskills/ files into a staging dir (e.g. `~/.local/share/skill-staging/<skill>/`), never into any skill-discovery root.
anti_trigger: The tree is already written and unchanged since the last emit.
scope: Writing the skill's files with valid routing headers and the index; hard-codes the subskills/ name.
status: seedling
---

# Emit Tree (pipeline step 4)

Write the files. Naming is **`subskills/`** — the operator's binding constraint #1, hard-coded.

## Standard

Every leaf file carries the mandatory routing header:

```markdown
---
name: <slug>
domain: <parent-chain>/<this-segment>   # strict prefix-extension of the parent
trigger: <when to use — one line, pushy>
anti_trigger: <when NOT to use — one line>
scope: <the single thing this file governs, uniquely claimed>
status: seedling | growing | verified | stale | deprecated
---
```

`trigger` / `anti_trigger` / `scope` are the genuine upgrade over a bare `references/`
folder — they close the intra-skill discovery and over-loading gaps. `domain:` enforces
the in-domain constraint mechanically (Rule 3 / linter).

SKILL.md body (Level 2): frontmatter `name` + `description`, then overview, when-to-use /
when-not, the precedence rule, the **subskill index** (a multi-column table mapping task
→ trigger → leaf file), and See Also. Keep the body well under 500 lines; move
instructional content into leaves.

The precedence rule (Rule 4) — write this sentence into every SKILL.md:

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:`
> string is claimed by exactly one file in this tree; no leaf may widen a prohibition
> declared by an ancestor — leaves narrow, never override upward.

## Decision rules

The description (the only Level-1 routing signal — the loader sees only it at startup):

1. It is third person: "Writes…", "Reviews…", never "I" or "you".
2. It names concrete trigger phrases a user would actually say.
3. It says when NOT to use the skill, as tasks that are out of scope. It never names
   another skill as the handler.
4. It stays at or under 1024 characters.

routing-eval.md (step 5b) measures whether the description works. Write it to pass that test.

If nested (>60 leaves only): each `subskills/<group>/INDEX.md` is pure TOC — frontmatter +
heading + routing table, **zero imperative sentences.** A content-bearing intermediate is forbidden.

No `00-rsi` in new skills (yet): SPEC-rsi-skills §7 adds `00-rsi` only at Stage 3, after
Stage 2 succeeds. Stage 1 covers only ac-subskills-author and ac-security-engineer.

## Procedure

Every leaf holds the whole job for its scope, in this order:

1. **Standard** — the professional standard, cited inline (a primary URL).
2. **Decision rules** — when to choose which option.
3. **Procedure** — numbered steps an agent can follow without any other file.
4. **Anti-patterns** — the common mistakes, one line each.
5. **Done checklist** — the checks that prove the step is finished.

A leaf that would pass 600 words splits into two leaves, each with its own scope. Never
end a leaf by handing work to another skill, and never tell the agent to load one (domain-map
rule 5). The SKILL.md "when NOT to use" lines name out-of-scope tasks, never a handler.
`lint_tree.py` and `skill_scan.py` both FAIL a hand-off line.

## Anti-patterns

- A leaf that defers its procedure to another file or skill.
- An intermediate INDEX.md with imperative content.
- A SKILL.md body over 500 lines because leaf content stayed at Level 2.

## Done checklist

- List every file written (paths). The next step lints them — do not hand to the human
  until lint-tree and security-vet pass.

## Sources

- House standard for skills-with-subskills (unpublished); the schema standard it emits against: <https://json-schema.org>.
- SPEC-rsi-skills §7: https://github.com/anoscranel/rsi-skills