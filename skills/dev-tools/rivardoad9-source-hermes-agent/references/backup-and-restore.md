# Backing up and restoring a Hermes install

Use when the user asks whether a backup exists ("hermes backup tuh ada ga"), before an upgrade or a
risky migration, or when they believe a scheduled "backup" job is protecting them.

## The three commands

| Need | Command | Lands as |
|---|---|---|
| Full archive (config, skills, plugins, sessions, data, `.env`) | `hermes backup [-o PATH] [-k N]` | zip, default `~/hermes-backup-<ts>.zip` |
| Fast snapshot of critical state only | `hermes backup --quick -l <label>` | DIR `$HERMES_HOME/state-snapshots/<stamp>-<label>/` |
| Restore | `hermes import <zip> [--force]` / slash `/snapshot restore <name>` | over the Hermes home |

- `-k N` (default 3) prunes older `hermes-backup-*.zip` in the output dir after a FULL backup; `0` keeps
  everything. The full archive excludes the `hermes-agent/` codebase — reinstall the code, restore the data.
- The quick snapshot is a plain directory with `manifest.json` (`file_count`, `total_size`, per-file
  sizes). Restoring it is a slash command, not `hermes import`.

**`--quick` ignores `-o`.** Pass `-o /path/foo.zip` and you still get a snapshot DIRECTORY under
`state-snapshots/`, then go looking for a zip that was never written and report the backup as failed.
Verified: `--quick` finishes in ~6s and prints its own path — read that line instead of the path you asked for.

## What each one actually contains

Quick (the 12 files that matter for a live install): `state.db`, `config.yaml`, `.env`, `auth.json`,
`cron/jobs.json`, `cron/executions.db`, `gateway_state.json`, `kanban.db`, `projects.db`,
`verification_evidence.db`, `channel_directory.json`, `processes.json`.

NOT in quick: `skills/`, `plugins/`, `data/`, `sessions/` transcripts, `profiles/*/memories/`,
`SOUL.md` files. A profile-based bot fleet lives in `profiles/<name>/` — quick does not cover it, so
pair it with a full archive (or a plain tar of `profiles/`) before any risky change.

## Size and headroom

- `state.db` dominates everything (500MB+ on a real install), so the quick snapshot ≈ the size of
  `state.db`. Check `df -h /` first: on a disk at 91% used, one snapshot alone cut free space from
  4.1GB to 3.6GB, and a full archive needs ~600MB more on top of that.
- A full archive of an ~11GB home measured ~530MB (7.5k entries, ~1.5GB uncompressed): the compression
  is real, but it is still the same disk. Never run a full backup with under ~1GB free, and never
  delete the only offsite copy to make room.
- Say the number out loud before running one. "Backup" that fills the disk is how the install goes down.
- Need room first? See `disk-space-and-cleanup.md` (safe /tmp + cache + journal reclaim, and the
  lifecycle-guard pitfall when a cleanup script names a file over 1MiB).

## Two traps that make users think they are covered

1. **A job named "backup" may not back anything up.** Read the script, not the job name: a "daily
   config backup" that runs `git add config.yaml cron/jobs.json && git commit` is a config HISTORY
   inside `$HERMES_HOME`, and it protects nothing else. Check with
   `python3 -c "import json;j=json.load(open('$HERMES_HOME/cron/jobs.json'));print([(x['id'],x['name'],x['script']) for x in (j if isinstance(j,list) else j['jobs']) if 'backup' in (x.get('name') or '').lower()])"`,
   then read the script it names.
2. **A backup on the same disk is not a backup.** Archive + originals die together when the VPS does.
   Offer the offsite leg (Google Drive via the `google-workspace` skill, or any external host) and
   keep the frequent local one cheap: quick snapshot weekly + full archive only around changes.

## Verify a backup exists and is real

```python
import json, zipfile
print(zipfile.ZipFile('/home/ubuntu/.hermes/backups/<file>.zip').namelist()[:10])   # full archive
print(json.load(open('/home/ubuntu/.hermes/state-snapshots/<name>/manifest.json')))  # snapshot
```

Confirm `state.db` and `.env` are present in the listing — a backup missing the secrets or the session
store will be discovered at restore time otherwise. Keep every archive mode 600 and out of any
synced/public directory: it holds `.env`, `auth.json`, and every cron/token path. Never print archive
contents to the user; report sizes and entry counts instead.

## The implemented shape (working install)

Two `--no-agent` cron jobs, both silent on success (empty stdout = no message):

- weekly Sun 03:30 → `~/.hermes/scripts/backup_weekly.sh`: full archive
  `-o ~/.hermes/backups/hermes-backup-<ts>.zip -k 2`, verify the zip, upload it to the Drive folder
  `Hermes Backups`, keep the 2 newest there. `--skip-zip` reuses the newest local zip (fast test).
- weekly Sun 04:00 → `~/.hermes/scripts/disk_maintenance.sh`. Order matters: archive first, prune second,
  otherwise the cleanup deletes the archive's input.

state.db maintenance CANNOT be a cron job: it needs the gateway stopped, and a job living inside the
stopped gateway dies with it. Use the systemd timer pattern in `disk-space-and-cleanup.md`.

Recipes that cost time to rediscover:

- The Drive CLI needs `googleapiclient`, which the system python lacks. Pick an interpreter first:
  `for p in ~/.hermes/hermes-agent/venv/bin/python ~/.hermes/installs/*/environments/*/venv/bin/python; do "$p" -c 'import googleapiclient' 2>/dev/null && { echo "$p"; break; }; done`.
- Never judge an upload by grepping its stdout. Piping it through `tail -3` cut the `"status": "uploaded"` /
  `"id"` lines and turned a SUCCESSFUL 460MB upload into a "BACKUP GAGAL" alert (and skipped the prune step).
  Make the script search the destination folder for the uploaded name and require a hit:
  `drive search --raw-query "'<folderId>' in parents and name = '<file>' and trashed = false" | len()`
  — read-back verification, same as any other external write.
- A 460MB upload takes ~5 minutes on this box; budget `timeout 3000` and do not expect the cron message in seconds.
- Never name a shell variable `UID` — it is readonly in bash, keeps its old value, and a "delete" then
  runs against an empty/previous id.
- Verify the NEW archive before deleting the old one: `unzip -t` (exit 0 prints "No errors detected"),
  `unzip -l | tail -1` for the entry count, and grep the listing for `state.db|config.yaml|jobs.json|memories/`.
  Then delete the stale copies and report the GB that came back.

## Reporting shape

Give the commands, then one measured run as proof (name, path, size, file count), then the honest gap:
what is NOT covered today and what that costs them. Close with a concrete choice — e.g. "weekly local
with 3 kept, or weekly pushed to Drive" — rather than a generic "want me to set up backups?".
