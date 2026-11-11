# ctf-router real-world coverage eval

A free, deterministic complement to the upstream `ctf-skills-src/evals/` promptfoo
suite (which needs a model API key and costs money). This one checks the *text*
of the router and skills against a corpus of real, published CTF challenges.

## Run

```bash
ctf-solver/.venv/bin/python .agents/skills/ctf-router/evals/check_routing.py
```

Exit status 1 on any failure. Prints per-case router/skill pass status and the
specific unmatched regex group.

## Corpus

`corpus.json` holds 33 cases (web, pwn, crypto, forensics, stego, jail, misc,
osint, ai-ml, cloud, hardware, reverse) taken from published writeups, each with
the challenge name, event, year, source URL, expected skill, and two sets of regex
groups:

- `router_groups`: regexes that must match somewhere in `ctf-router/SKILL.md`
  (artifact-class coverage of the routing table).
- `skill_groups`: regexes that must match somewhere in the expected skill's
  `*.md` files (technique coverage).

Groups are lists of alternatives (OR within a group, AND across groups).

## When it fails

A failure means either a routing-table row or a technique note is missing for
that challenge class. Fix the router (`ctf-router/SKILL.md`) or the relevant
skill file, then re-run. Keep `.agents/skills` and `ctf-skills-src` in sync for
shared skills.