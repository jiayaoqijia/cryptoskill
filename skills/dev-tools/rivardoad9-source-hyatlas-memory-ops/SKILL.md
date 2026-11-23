---
name: hyatlas-memory-ops
description: Use when installing or debugging HyAtlas memory on Hermes.
---

# HyAtlas v4 memory ops (Hermes)

## When to Use

- The user asks to install, enable, or switch HyAtlas v4 as the Hermes memory provider.
- The flat `MEMORY.md` is at its character cap and durable facts need a retrieval backend.
- `hyatlas-go` / the `hyatlas` plugin misbehaves: server down, wrong mode, provider not active, stale counters.
- Post-install questions like "what changed?" after wiring a memory provider.

Local 7-layer memory backend (`hyatlas-go` + Hermes plugin `hyatlas`). It replaces nothing: the flat
`memories/MEMORY.md` + `memories/USER.md` stay loaded (the built-in store is independent); the provider
ADDS per-turn recall and turn storage. Install order matters: Hermes version first.

## Order
1. `hermes update --yes --backup` (plugin needs >= 0.21.4; approval-ledger >= 0.21.5).
2. `hermes plugins install approval-ledger --enable` (optional, cheap; records approvals).
3. `hermes plugins install tuancookiez-hub/HyAtlas-Memory/plugins/hyatlas`
4. Server install (no Go toolchain needed, binary release ~172 MB):
```bash
HYATLAS_MODE=lite HYATLAS_VERSION=v4.5.0 curl -fsSL \
  https://raw.githubusercontent.com/tuancookiez-hub/HyAtlas-Memory/main/scripts/install.sh -o /tmp/hyatlas_install.sh
bash /tmp/hyatlas_install.sh   # binary -> ~/.local/bin/hyatlas-go, model -> ~/.hyatlas/models
```
5. `hermes plugins enable hyatlas` then `hermes config set memory.provider hyatlas`
   (never hand-edit config.yaml; `hermes config set` handles it).

## Run it as a durable service
`write_file` REFUSES `/etc/**` paths: write the unit to `/tmp`, then copy with sudo.
- env file `~/.hermes/hyatlas.env` (chmod 600): `HYATLAS_EMBED_BASE=bge`,
  `HYATLAS_MODEL_DIR=/home/ubuntu/.hyatlas/models`, `HYATLAS_MODE=lite`,
  `HYATLAS_GO_HOST=127.0.0.1`, `HYATLAS_GO_PORT=19528`, `HYATLAS_GO_DATA=<data dir>`.
- systemd unit (system scope, `Restart=always`, `EnvironmentFile=`) then
  `sudo -n cp /tmp/x.service /etc/systemd/system/ && sudo -n systemctl daemon-reload && sudo -n systemctl enable --now hyatlas-go`.

## Verify (this order)
- `curl -s 127.0.0.1:19528/healthz` -> `{"status":"ok"}`
- `/api/v1/status` -> `"mode":"lite"` (if it says `ultra` your env never reached the process), `embed:"ok"`, `vdb:"ok"`
- round trip: `hermes hyatlas add "<fact>"` then `hermes hyatlas search "<words>"`; the hit comes back with a score
- counters (`writes` / `searches` / `vdb_points`) increment

## Pitfalls
1. `hyatlas-go --version` and `--help` DO NOT exit: they ignore the flag and START a server (mode ultra).
   Never probe the binary with flags; start it and curl. Kill strays by PID, never `pkill -f hyatlas-go`
   (the pattern matches your own shell command and kills it).
2. Restarting the gateway FROM INSIDE the gateway is blocked (the guard also scans referenced scripts):
   ask the user to send `/restart` (gateway slash command, drains active runs) or run
   `hermes gateway restart` from a shell outside. Do not promise a self-scheduled restart.
3. Do NOT assume a gateway restart is needed after `hermes plugins enable hyatlas` + `hermes config set
   memory.provider hyatlas`: the enable step prints `Gateway reloaded plugins`, and the provider can be live in the
   SAME session (a recall block shows up in the prompt, `writes`/`searches` climb, MainPID unchanged). Poll
   `/api/v1/status` across two turns before mentioning a restart at all; only offer `/restart` when the counters
   really stay flat.
4. `lite` = no LLM call, nothing leaves the machine, no extraction (L1/L3 stay empty). `pro`/`ultra` need
   `HYATLAS_LLM_BASE` / `HYATLAS_LLM_MODEL` / `HYATLAS_LLM_KEY` (any OpenAI-compatible API, e.g. DeepSeek).
5. RAM: ~490 MB RSS. On a 1.9 GB box check `free -h` right after start and tell the user plainly.
6. Backup before switching: `config.yaml`, `memories/MEMORY.md`, `memories/USER.md`.
7. The plugin does NOT read a `memory.providers` block; host/port go under `plugins.entries.hyatlas.settings`.
