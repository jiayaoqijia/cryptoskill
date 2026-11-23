# Publishing an artifact pack (skills, templates, configs) to a public repo

When the ask is "share my skills / templates so people can fork them", the work is curation plus a scrub,
not a `git push`. The repo is public forever and search-indexable.

## 1. Decide the boundary before copying anything

Walk the source tree by category and sort into include / exclude. Keep the generic procedure, drop anything
that encodes the owner's money or clients:

- include: design, docs, media, software-development, research-of-public-data, devops patterns
- exclude: live trading strategies, wallet/portfolio lanes, capital sizes, client work, product-specific
  ops runbooks, anything with a business model inside it

Rule of thumb: if the file would tell a competitor how the owner makes money, it is out. If it teaches a
technique anyone could re-derive in ten minutes, it is in. Say in the README that private material is
deliberately absent, so a reader does not think the collection is incomplete by accident.

## 2. Scrub identifiers, then prove the scrub

```bash
find . -type f \( -name '*.md' -o -name '*.sh' -o -name '*.py' -o -name '*.json' -o -name '*.html' \) -print0 |
  xargs -0 sed -i \
    -e 's/owner\.real@email/you@example.com/g' \
    -e 's/<telegram_chat_id>/1234567890/g' \
    -e 's/0x<real_wallet_address>/0xYOURWALLET/g' \
    -e 's|/home/<user>|$HOME|g'

grep -rIlE 'owner\.real@email|<chat_id>|0x<wallet>' . || echo clean
```

Scan for hard secrets first (tokens, private keys, `*.env`, `*.db`); a skill library usually has none, but
references often quote placeholder tokens that look real. Check the frontmatter of third-party skills —
keep `author:` and `license:` intact and carry their LICENSE files along; the README should name them.

## 3. Shape the repo

- `README.md`: what the pack is, a table of contents with counts, the install one-liner, the ZIP link, and
  what is deliberately excluded.
- `LICENSE`: MIT for the owner's own material, with a line that third-party files stay under their own.
- Keep the original directory layout so `cp -r pack/*/ ~/.hermes/skills/` works unchanged.

## 4. Create, then verify from outside

```bash
gh repo create <name> --public --source=. --remote=origin --push --description "..."
gh repo edit OWNER/<name> --add-topic ai-agents --add-topic agent-skills
```

Verification is a fresh clone somewhere else, not `git status` in the source dir:

```bash
git clone -q https://github.com/OWNER/<name>.git /tmp/verify && find /tmp/verify -name SKILL.md | wc -l
grep -rIlE '<the scrubbed identifiers>' /tmp/verify || echo clean
curl -sL -o /tmp/pack.zip -w '%{http_code} %{size_download}\n' https://github.com/OWNER/<name>/archive/refs/heads/main.zip
```

The archive ZIP is much smaller than the clone (no `.git`) — that is not a broken archive. Report the file
count, not the byte size, as the proof the pack is complete.

## 5. Rename while it is still young

A pack that starts as one topic and grows past its name (github-only → whole library) should be renamed
right away: `gh repo rename <new-name> --repo OWNER/old --yes`. GitHub keeps a 301 from the old path, so an
already-shared link keeps working — verify with
`curl -s -o /dev/null -w '%{http_code} %{redirect_url}' https://github.com/OWNER/old` and expect `301`.
Renaming after someone forks leaves the fork pointing at the old name; do it before advertising the link.
