---
name: domain-map
domain: skill-authoring/domain-map
trigger: After the research gate passes — decompose the target skill's domain into atomic leaf scopes.
anti_trigger: The domain map already exists and passed the uniqueness check for this skill.
scope: Producing a closed subdomain map where every scope is claimed by exactly one leaf.
status: seedling
---

# Domain Map (pipeline step 2)

Decompose the skill's **own** domain into a closed set of atomic, independently-
triggerable scopes — the blueprint for the tree. Method follows the taxonomy
decomposition in the subskills-architecture findings (D0).

## Standard

The map is closed and unique (Rule 4): every section of the source material maps to
exactly one leaf; no orphan content; no scope claimed twice. The domain chain root is set
now: `<skill-domain>`; every leaf's `domain:` is a strict prefix-extension of it.

## Decision rules

1. **Stay in-domain** — decompose by *its own* domain's knowledge, never cross-field.
2. **Atomic scopes** — each leaf is one thing a user can want independently. If two scopes
   share a trigger, they are one leaf. If one scope has two unrelated triggers, split it.
3. **Keep Level 2 in SKILL.md** — overview, when-to-use/when-not, the precedence rule,
   the index, and See Also stay in the body. Only instructional content becomes leaves.
4. **Out of scope, never dropped** — subdomains that are not task-triggerable (foundations,
   theory) are each declared out of scope with a one-line reason; never dropped silently.

## Procedure

1. Enumerate every distinct, independently-triggerable want in the domain → one candidate
   leaf each.
2. Write the uniqueness check down — for any pair that looks adjacent, state in one line
   why they are distinct.
3. **Self-contained, never delegated:** before you claim scopes, list the installed
   skills (list the skills directory two levels deep, e.g. `ls -d <skills-dir>/*/ <skills-dir>/*/*/`). Use the names only to find
   coverage gaps and collisions, never to copy. If another skill covers a subdomain,
   re-research that subdomain from primary sources (standards, official docs, the
   research dossier) and write it in this skill's own words. Never open or read another
   skill's files while authoring: that risks a derivative copy and a licence breach
   (self-contained rebuild intake, rules R1–R2). The new skill depends on no other skill.
4. Record the leaf **count** — it drives flat-or-nest.

## Anti-patterns

- Claiming a scope another skill already covers without re-researching it yourself.
- Silently dropping a non-triggerable subdomain instead of declaring it out of scope.

## Done checklist

Output the table: leaf file | domain segment | one-line scope | source section it absorbs |
also-covered-by (collision watch). The last cell holds `-`, or installed-skill names that
cover the same ground — test targets for the entrance eval, never handlers: this skill
still owns the scope in full. Out-of-scope subdomains get their own rows with `-` as the
leaf file and the reason in the scope cell. Plus the uniqueness-check paragraph. This
table is the input to flat-or-nest and emit-tree.

## Sources

- House standard for skills-with-subskills (unpublished).
- <https://martinfowler.com>
- <https://github.com/>
