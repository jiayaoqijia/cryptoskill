# Claim honesty on a non-programmer account (user correction, 10 Oct 2026)

Companion to `references/profile-polish-recipe.md`. Read this before writing any skill list,
bio, portfolio card, or CV line for an account whose owner **directs AI coding agents** rather
than writing code.

## The correction, verbatim

The first pass of the profile README, the bio, the Pages portfolio and the CV listed
`Python` `TypeScript / Node.js` `Next.js` `SQLite` as *his* skills (a "Software & Data" card on
the site, a "Tools I use daily" line on the profile). The user rejected it:

> "yg software data keknya terlalu di lebih2 kan deh, gw ga punya basic programming."

He operates the agents that write the code. He does not read or write it. The same day he also
rejected `English (professional working)` on the CV: *"yang bahasa inggris jujur gw ga begitu
jago, gw paham basic aja."* Both were my defaults, not his claims — that is the pattern to kill.

## What to write instead

Personal skill rows describe **activity**, never the stack:

```
AI coding agents & tooling
directs and operates AI coding agents (Hermes Agent, Claude Code) to build and test applications;
runs, tests and maintains the results; working familiarity with Git/GitHub, database structure and
API/webhook flows at user level
```

```
AI coding agents & tooling
mengarahkan dan mengoperasikan AI coding agent untuk membangun dan menguji aplikasi; menjalankan,
menguji, dan merawat sistem hasilnya; Git/GitHub, struktur basis data, dan alur API/webhook di
level pengguna
```

Notes that go under the projects heading (profile README, portfolio, CV):

- EN: *"Everything below was built with AI coding agents (Claude Code, Hermes Agent) under my
  direction: I set the requirements, test the behaviour, and operate the systems. I direct and test,
  rather than write code from scratch."*
- ID: *"Semua proyek di bawah ini dibangun bersama AI coding agent (Claude Code, Hermes Agent) atas
  arahan saya: saya menetapkan kebutuhan, menguji perilaku, dan menjalankannya, bukan menulis kode
  dari nol."*

Keep per-project stack columns/lines (`TypeScript`, `Next.js`, `Python`) — they describe the
artefact, which is true. Do NOT put a stack name on a line that describes the person.

Conservative wording when a self-rated claim is unverified:

| Claim | Do not write | Write |
|---|---|---|
| English | professional working / fluent | `English (basic: reads technical documents and terminology)` / `Inggris (dasar: bisa baca dokumen dan istilah teknis)` |
| Code | Python, TypeScript, SQLite | `directs and operates AI coding agents ...; runs, tests and maintains the results` |
| Seniority | engineer, developer | operator / automation builder (leave the title to the person's own choice) |

Reframe, never just delete: "baca dokumentasi teknis + paham istilah" is a real, passive-then-active
skill, and recruiters read it as trainable. Deleting a line entirely leaves a bare CV; editing it to
the truth keeps the value.

## The single claim set

The CV, the profile README, the bio, the portfolio site and any outreach blurb are **one claim
set**. When the user corrects one, fix all of them in the same pass — a corrected CV next to an
uncorrected profile is still a contradiction the user will get asked about. Cost is one PUT per
surface plus one Pages build wait.

## Tell the user what the correction changes (do not just comply)

Two lines that were worth saying and should be said again:

1. Overstating a stack is the expensive direction: it survives ATS and dies on the first technical
   question. "I direct and test AI-built systems" is defensible and is genuinely scarce in 2026.
2. Target the jobs that match the honest claim — automation/operations, finance ops, accounting-firm
   and tax-office process roles — not "junior developer". The accounting background plus agent
   operation is the rare combination; the coding gap is not the story.

## Verify, then deliver

`uv run --quiet --with pypdf python - <<'PY'` over the rebuilt PDFs: page count == 1, then assert
the corrected strings are present AND the removed stack names are absent:

```python
for kw in ("AI coding agent", "rather than write code", "Python", "TypeScript", "SQLite"):
    ...
```

If the CV grows past 1 page after the wording change, trim text before shrinking type: drop stack
names from one-line project bullets, shorten the note, then tighten `leading`/`spaceAfter`
(11.6 → 11.1) and margins (1.05/0.9 cm → 1.0/0.8 cm). Verified working: 2 pages → 1 page with all
keywords intact.
