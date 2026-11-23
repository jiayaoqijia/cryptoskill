---
name: user-profile-export
description: Use when exporting user memory as text for another AI.
version: 1.0.0
author: Hermes Agent
license: MIT
triggers:
  - import memory tentang gw
  - kirim profil ke AI lain
  - export memory
  - context untuk agent lain
metadata:
  hermes:
    tags: [memory, privacy, profile, handoff]
    related_skills: [hyatlas-memory-ops, session-librarian]
---

# Privacy-filtered profile export

Turning what the assistant knows about Do into a text document another AI (folk.com, another agent, a
future profile) can ingest — with the private and the merely transient stripped out.

## When to Use

Do asks to "import memory tentang gw dalam bentuk teks", wants to hand context to a different AI, or wants a
profile the other side can use to answer in his voice. Not for recalling a past session (`session_search`) and
not for writing new memories (`memory` / `hyatlas_add`).

## Step 1 — Inventory, then synthesize

Sources, in order: `memories/USER.md` (identity, preferences), `memories/MEMORY.md` (standing operational
facts), then `hyatlas_search` for anything durable they miss.

What comes back from the vector store is mostly `l2_raw` **task transcripts** — a market deep-dive, a cron
cleanup, an options analysis. Do not paste them. Mine them for a trait, a preference, or a principle, and write
that in one line. A profile is a description of a person, not an archive of what they asked for.

## Step 2 — Apply the include / exclude line

Include: name and nickname, brand, education and semester, work or internship field, the goal he is actually
chasing and why, career posture (inside a system vs solo), how he works, how he learns, how he wants to be
corrected, communication style, interests and decision principles at the level of *how*, current projects by
purpose (not by client or account), what he wants from an AI.

Exclude, always: wallet and bank addresses, balances and portfolio values, exchange and broker names, API keys
and tokens, email, phone, chat and account IDs, transaction history, employer/client names, and any third
party's identity. The target is another company's model; treat the whole document as publishable.

State the exclusion in the document itself (a short closing note) so a later edit does not quietly reintroduce
a number that happens to be in context.

## Step 3 — Write it so it survives being read by a stranger

- Sections with plain headings; neutral third person ("Rivardo, dipanggil Do") so it reads as a profile, not
  as a chat log quoting him.
- Keep the friction, not just the flattery: the self-imposed pressure, the learning behaviour that makes him
  stop halfway, the correction style that shuts him down. Those are the parts that make another AI useful to him.
- One concrete goal number is fine (his target), because it is motivation. Any number that is *state* (balance,
  position size, P&L) goes out.
- No internal tool names, file paths, job IDs, bot usernames, or server details.

## Step 4 — Verify redaction mechanically, not by re-reading

Run the scan before delivering:

```bash
python3 scripts/redaction_scan.py <file.md>
```

It flags wallet addresses, emails, URLs, long digit runs, filesystem paths, credential words, broker names and
chat IDs. Every hit must be a deliberate keep or removed — never ship an unexplained hit.

## Step 5 — Deliver the file plus the text, and offer the blank template

Write to `~/.hermes/exports/` and send the document as a file, with the full text inline so he can copy it
without opening anything. `templates/profile-export.md` is the blank skeleton; hand it over when he wants to
fill one in himself or produce a second version.

## Pitfalls

- **A bare "kirimin template" is a referent question.** It can mean the blank skeleton, the document just
  written, or the template for whatever message he is replying to. Resolve it against the message he replied to
  or the last artifact discussed before sending anything; if two readings are equally live, send both in one
  message rather than guessing once and being corrected.
- **Never quote a task log as a trait.** "Prefers concentration over diversification" is a profile line;
  the whole correlation table that produced it is not.
- **State numbers age.** A balance or position size is wrong the next day, and it is also the most sensitive
  thing in the file. Both reasons point the same way.
- **Do not let the exclusion list itself leak details.** Write "exchange names", not the names of his exchanges.
