---
name: ctf-misc
description: Use when a challenge is misc-category: a python jail or sandbox escape (pyjail, filtered eval/exec, stripped builtins), a restricted shell or rbash to break out of, character-filtered command injection, OSINT (person, image, location, infrastructure, company tracing), esoteric languages (brainfuck, whitespace, JSFuck, Piet, LOLCODE, Shakespeare), quiz/logic/sequence puzzles, QR repair, code systems (morse, semaphore, tap code, maritime flags), or identifier/format puzzles (UUID timeline, ISBN, GPS formats, tar/zip polyglots, SDR/HDL traces).
---

# CTF misc — jails, esolangs, OSINT, grab-bag

Workspace rules, remote gate, flag logging: sibling skill `ctf`.

## Triage — classify the constraint first (5 minutes)

The whole category is "a rule blocks you". Identify WHICH rule before touching
payloads. One row per look:

| What the challenge shows | Constraint class | Read |
|---|---|---|
| `eval(input())`, stripped/filtered builtins, "safe calculator" | python jail | `references/pyjail.md` |
| `ssh user@host` drops into rbash, `PATH` broken, allowed-commands menu | restricted shell | `references/bashjail.md` |
| input re-run through bash, `ca""t`-style wargames, char filters on commands | command filter | `references/bashjail.md` |
| `++++[>` / space-tab-LF-only / `[](!+[])` / colored Piet image / `HAI` | esoteric language | `references/esoteric.md` |
| find the person/photo/place/company/infrastructure from artifacts | OSINT | `references/osint.md` |
| QR image, PDF, plist, morse/flags/stick figures, UUID/ISBN/GPS, polyglot file, SDR/HDL | grab-bag | `references/misc-grab-bag.md` |
| riddles, logic grid, number sequences | quiz/logic | `references/esoteric.md` (bottom) |

Then, in `notes.md`, write the constraint as a sentence: "jail evaluates my
expression with `{"__builtins__": {}}` and rejects `__`" — that sentence picks
the payload family, nothing else should.

## Playbook — jail workflow (the core loop)

1. **Replicate the jail locally, exactly** — same interpreter version, same
   filter code. Never develop payloads against the remote.

```bash
cp jail.py dist/ ; cd solve
../../skills/ctf-misc/scripts/pyjail-lab.sh 3.11 ../dist/jail.py   # podman, offline
../../skills/ctf-misc/scripts/pyjail-lab.sh --system ../dist/jail.py
bash -r    # rbash replica for shell jails (see bashjail.md harness)
```

2. **Enumerate primitives**: which builtins/classes/characters survive?
   Probes in `references/pyjail.md` step 1 — every error message is an oracle.
3. **Iterate payloads mechanically**: keep `payloads.txt`, one candidate per
   line; run each, record result + exact error. Never hand-type payloads twice.
4. Escalate families in order: builtin recovery → subclass walk → frames →
   format-string leak → unicode/charset bypass.
5. On escape: flag hunt per `ctf` skill; remote runs stay behind its gate.

## Playbook — other tracks (one-liners, details in references)

- **Esolang**: identify by look (table in `references/esoteric.md`); decode
  rather than execute when possible; run via `scripts/bf.py` (brainfuck) or the
  verified whitespace interpreter; untrusted JS (JSFuck) only inside
  `podman run --rm -i docker.io/library/node:24-alpine node -`.
- **OSINT**: enumerate → verify (two sources) → pivot; passive-only ethics and
  query recipes in `references/osint.md`.
- **Grab-bag**: match the artifact to the table in
  `references/misc-grab-bag.md` (QR ladder, PDF objects, code-system tables,
  identifier math, polyglots).

## References

- `references/pyjail.md` — jail taxonomy, payload families (subclass walk,
  builtins recovery, frames, compile route, format-string walk, charset/unicode
  bypasses), version warnings, lab loop.
- `references/bashjail.md` — rbash vs soft-jail decision table, escapes
  (interpreters, BASH_CMDS, ssh ProxyCommand, pagers), char-filter recipes,
  local harness.
- `references/esoteric.md` — identify-by-look table, bf.py usage, verified
  whitespace interpreter, JSFuck primitives + sandboxed execution, Piet,
  substitution langs, quiz/logic approach.
- `references/osint.md` — workflow, per-goal technique table, query recipes
  (dorks, crt.sh, archives, Shodan/Censys/FOFA), ethics rules.
- `references/misc-grab-bag.md` — QR repair ladder, PDF/plist, morse/tap/
  semaphore/maritime tables, UUID v1 timeline+MAC leak, ISBN/GPS math,
  tar/zip polyglots, SDR/logic/HDL notes.

## Toolbox

| Tool | Install | Purpose |
|---|---|---|
| `scripts/bf.py` | included (stdlib) | brainfuck interpreter, bounded tape/step limit |
| `scripts/pyjail-lab.sh` | included | run a jail replica under the exact python via podman |
| `podman` | preinstalled | jail replicas (python:3.x-slim), sandboxed esolang execution |
| `bash -r` | included | rbash replica harness |
| `zbarimg` | preinstalled (zbar 0.23) | QR/barcode decode attempts |
| `pdftotext` | preinstalled (poppler) | PDF text layers |
| `qpdf` | `sudo pacman -S qpdf` | PDF object/xref inspection |
| `exiftool` | `sudo pacman -S perl-image-exiftool` | image/document metadata (OSINT) |
| `dig` | preinstalled | DNS records for OSINT pivots |
| `node` (container) | local image `docker.io/library/node:24-alpine` | run untrusted JSFuck/JS payloads isolated |
| `gdb`, `ssh`, `vim`, `base64` | preinstalled | rbash escape targets / ssh ProxyCommand |
| `qrcode`, `pillow` | `uv pip install --python .venv/bin/python qrcode pillow` | QR rebuild, image repair (`.venv` via `scripts/setup.sh`) |
| `iverilog` | `sudo pacman -S iverilog` | verilog HDL puzzles |
| `sigrok` | `sudo pacman -S sigrok` | logic-trace protocol decode |
| `rtl_433` | build from upstream (needs rtl-sdr) | ISM-band capture decoding |
| `npiet` | upstream sourceforge binary | Piet programs |
