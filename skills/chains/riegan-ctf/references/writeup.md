# Writeup template

Write per challenge after solving (or at event end). Goal: teammate can re-solve from
the writeup alone. Save as `work/<event>/<chal>/writeup.md`.

```markdown
# <category>/<challenge-name> — <points> pts, <N> solves

## TL;DR
<one-liner: bug class + key primitive + how the flag falls out>

## artifacts
- dist/... : <what it is, sha256>
- remote: nc <host> <port> / https://... (dead after event)

## recon
<what triage revealed: mitigations, language/framework, red herrings>

## solution
1. <step + command/exploit snippet>
2. ...
<full final exploit script in solve/, referenced not inlined if >60 lines>

## mistakes made (keep — this is the valuable part)
- <dead end, why it looked right, what ruled it out>

## flag
flag{...}
```

## Event summary (work/<event>/summary.md, after event)

| challenge | category | points | solves | solved | bug class | time spent |
|---|---|---|---|---|---|---|

Then three lists: **fastest next time** (what to automate), **knowledge gaps**
(attack classes that stalled us), **tooling gaps** (what to pre-install before the
next event). These feed back into the skill suite — propose edits as a team.
