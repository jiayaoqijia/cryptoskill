# Publishing your own skill library to git

Triggered by: *"import semua skill lu ke github gw"*, *"gw mau pakai skill lu di agent lain"*. This is the
reverse of adoption: the deliverable is a public/private repo another agent can clone, with every folder
holding a `SKILL.md`, and **no credentials, sessions, or personal identifiers**.

## 1. Inventory before copying

```bash
find ~/.hermes/skills -name SKILL.md -not -path "*/.hub/*" -not -path "*/.curator_backups/*" | wc -l
du -sh ~/.hermes/skills
```

Three populations exist and only one ships: active skills, archived ones (`.archive/`), and runtime
caches (`.hub/`, `.curator_backups/`, `__pycache__`, `*.pyc`). Skip archives and caches, and say in the
report that archived skills were left out rather than silently dropping them.

Skills live at two depths: `skills/<category>/<name>/SKILL.md` and `skills/<name>/SKILL.md` for the
root-level ones. A walker that assumes the first shape either misses the roots or nests them
(`<name>/<name>/SKILL.md`). Handle both and assert the exported count equals total minus archived.

## 2. Copy only real skill payload

Include every file inside a directory that contains `SKILL.md` (`references/`, `scripts/`, `templates/`,
`assets/`) and exclude by name: `.env*`, `*.pem`, `*.key`, runtime session/state files (for this tree,
`.termix-a2a-session*`, `.termix-watch-state*`), logs, `node_modules`, and anything over ~3 MB. Copying
support files matters: a `SKILL.md` that references `scripts/foo.py` is broken without it.

Emit a `skills-manifest.json` next to the tree: `path`, `name`, `description`, file count, and a short
`SKILL.md` hash. It is what lets a later session diff two exports instead of guessing which copy is newer.

## 3. Sanitize personal identifiers, not just secrets

A skill written for one user carries that user's life in it: emails, chat IDs, bot handles, repo names,
absolute home paths. Replace them with placeholders before publishing:

| Pattern | Replacement |
|---|---|
| personal email / campus email | `your-email@example.com` |
| Telegram numeric ID | `<telegram-user-id>` |
| `@some_personal_bot` | `@your_gateway_bot` |

Then scan the **copy**, not the source:

```python
PATTERNS = {
  "openai": r"\bsk-[A-Za-z0-9_-]{20,}",
  "github": r"\b(ghp_|gho_|github_pat_)[A-Za-z0-9_]{20,}",
  "telegram": r"\b\d{8,10}:AA[A-Za-z0-9_-]{25,}",
  "aws": r"\bAKIA[0-9A-Z]{16}\b",
  "gcp": r"\bAIza[0-9A-Za-z_-]{30,}",
  "privkey": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
  "assign": r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][A-Za-z0-9_\-/+]{24,}['\"]",
}
```

**Read every hit before deleting it.** Most are placeholders (`sk-xxx`, `ghp_xx...xxxx`, `user@example.com`)
or compliance prose quoting a key format; a few are real. Redact the real ones and the instructional
mentions of key material (an example line showing a `PRIVATE KEY` block header still trips a reviewer's
grep), and leave placeholders alone — over-redaction makes the docs unusable.

## 4. Personas are skills too

Ship voices as `personas/<name>/SKILL.md` with the same frontmatter (`name`, `description`) so other agents
can load them like any skill. Write one persona per job (daily chat, builder, market analyst), keep the
rules imperative, and keep the user's PII out — a persona that names a private email or ID is not portable.

## 5. Publish into the existing repo

Check `gh repo list` first; a repo from a previous export usually exists. Update it instead of creating a
near-duplicate: clone shallow, `rsync -a --delete --exclude .git` the build over it, commit, push to `main`.
Keep the LICENSE that is already there. Set the description with the real counts (`183 SKILL.md — 180
skills + 3 personas`) so the repo explains itself.

## 6. Verify from a fresh clone

Local success proves nothing about what landed. Clone the remote into a scratch dir and assert:

- `find . -name SKILL.md | wc -l` equals skills + personas
- zero `*.env*`, `*.pem`, `*.key`
- zero hits for personal identifiers and the secret patterns above
- every skill dir has `SKILL.md` at its root (not in a subfolder) with `name` and `description` in frontmatter

The last check is what makes the repo usable by Claude Code, Cue, or a custom agent: they all expect
`SKILL.md` at the folder root.

## Boundaries

- Never publish `.env`, token caches, session state, or logs, even inside a skill folder that "needs" them.
- Never publish a private vault path, chat ID, or customer data; skills are reusable, incidents are not.
- Skills that call wallets, exchanges, or paid APIs stay in the pack, but the report should tell the user to
  start the receiving agent with the low-risk categories and add credentialed ones after its permission gate
  is configured.

## 5. Weekly sync (proven setup)

Source of truth is `~/.hermes/skills`; the public mirror is `rivardoad9-source/agentZ-Skill`.
`~/.hermes/scripts/sync_skills_to_github.py` does the whole cycle: export (skip `.hub`,
`.curator_backups`, `.archive`, `__pycache__`, `.env`/`.pem`/`.key`, `.termix-*` runtime state,
files >3 MB) → sanitize personal identifiers → scan → rsync → commit/push.

Rules that make it safe to run unattended:

- Scan failure must **abort before push** (exit 1, print `label: path: value`). Never "push then fix".
- Placeholders (`sk-xxx`, `ghp_xx...xxxx`, `your-`, `example`, `<redacted`) are allowlisted; real-looking
  values are not.
- Instructional prose that quotes a key header trips the scanner. Reword it at the source
  ("a PRIVATE KEY block header"), don't weaken the regex.
- Silent stdout when nothing changed — cron runs with `no_agent` and only speaks on change or failure.
- Verify from a **fresh clone**, not the working copy: count `SKILL.md`, check zero `.env`, zero secret
  patterns, zero personal IDs.

Registered as weekly cron `1a311fb42c64`, Monday 09:00 WIB, `deliver=origin`.
