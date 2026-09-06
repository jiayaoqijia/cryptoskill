---
name: give-feedback
description: >-
  Send feedback about cardano-dev-skills itself to its maintainers as a GitHub
  issue: a bundled skill or doc that was wrong, stale, confusing, or missing
  something, a prompt that should have triggered a skill but didn't, or a
  skill that saved real time. Drafts the issue from the current context,
  scrubs secrets, asks once, then files it with gh. Trigger phrases: "give
  feedback", "send feedback", "report this skill", "this doc is wrong", "that
  skill is stale", "feedback to cardano-dev-skills", "/give-feedback".
allowed-tools: Read Grep Glob
disallowed-tools: WebFetch WebSearch Edit Write
---

# Give Feedback

Send what you just learned about a cardano-dev-skills skill or bundled doc to the
people who maintain it: a GitHub issue on `cardano-foundation/cardano-dev-skills`,
under the user's own GitHub account, after one approval. Maintainers read every issue.
The small gaps and the quiet wins are what make the skills better for the next agent.

## When to use

- A bundled skill or doc was wrong, stale, misleading, or confusingly worded.
- It lacked the one sentence, example, or warning that would have saved time.
- A prompt should have matched a skill and didn't.
- A skill or doc saved a real mistake or explained something unusually well. Praise is
  data: it tells maintainers what not to break.
- The user asks: "send feedback", "report this skill", `/give-feedback`.

Bias toward sending. A rough issue with a path and one sentence beats a perfect one
never filed; weak signals are cheap to close, missing ones cannot be recovered.

## When NOT to use

- General Cardano questions, or bugs in the user's own project.
- Problems with an upstream project's software rather than with how it is documented
  here. Report those upstream.
- Proposing a new documentation source. That form asks the human to attest the vetting
  bar; give them
  `https://github.com/cardano-foundation/cardano-dev-skills/issues/new?template=suggest-source.yml`.
- Mid-task. Finish, then offer once at a natural pause. If the user declines, drop it
  for the rest of the session.

## Key principles

1. **Scrub before showing.** Remove mnemonics, signing keys, API keys and project ids,
   mainnet addresses, names, emails, home-directory paths, and private repo names.
   Replace them with `<redacted>`.
2. **Show the draft and ask once, in the same message.** After a yes, send. Do not
   re-confirm. If the user edits ("drop that line", "wrong skill"), apply and send.
3. **The user's identity, the user's words.** The issue goes out under their `gh`
   login. Quote what actually happened; never invent evidence.
4. **Send once.** One finding per issue; never retry after a success.

## Format

Title: `[docs]`, `[topic]`, or `[feedback]` plus a short summary, with the label
`documentation`, `enhancement`, or `feedback`. `[docs]` for anything wrong or stale,
`[topic]` for something missing, `[feedback]` for praise, a prompt that missed, or
general experience. One body shape for all three:

```markdown
### Where
skills/<name>/SKILL.md (section "<heading>") or docs/sources/<source>/<file>

### What happened
<what it said, what was expected, what actually happened; evidence if any>

### What would have helped
<the missing sentence, example, or warning; or "keep doing this">

Agent: <Claude Code | Codex | Cursor | other>
```

## Workflow

### Step 1: Gather

From the conversation, not from a round of questions: the exact path (Glob or Grep under
`${CLAUDE_SKILL_DIR}/../..` to confirm it — the repo root, so that both `skills/` and
`docs/sources/` are reachable), what was asked, what the skill or doc said, what
happened, and what would have helped.

### Step 2: Scrub

Apply principle 1 to the title and the body.

### Step 3: Draft and ask once

In one message: the title, the label, and the body in a fenced block, then "Ready to
file this as a **public** issue on cardano-foundation/cardano-dev-skills, under your
GitHub account. OK, or want to tweak it?"

Say public every time. The repository is public, the draft is built from a working
session that may not be, and visibility — not authorship — is what makes an accidental
disclosure irreversible.

### Step 4: Send

The body goes through stdin in a quoted heredoc, so it needs no shell quoting. The title
is substituted into a double-quoted string, so it is one line of plain text with `` ` ``,
`$`, `"` and `\` removed before substitution:

```bash
gh issue create -R cardano-foundation/cardano-dev-skills \
  --title "[docs] skills/<name>/SKILL.md: <short summary>" \
  --label documentation \
  --body-file - <<'ISSUE_BODY'
### Where
...
ISSUE_BODY
```

If the host asks permission for the command, that prompt shows exactly what is being
sent; proceed once it is approved, without re-asking in chat. If the command fails for
any reason (no `gh`, not logged in, label rejected), say so in one line and give
`https://github.com/cardano-foundation/cardano-dev-skills/issues/new/choose`; the draft
above is what to paste.

### Step 5: Report

One line: the issue URL, or "Not sent; draft and link above."
