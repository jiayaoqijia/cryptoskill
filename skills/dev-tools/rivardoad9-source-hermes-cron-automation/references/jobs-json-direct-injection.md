# Injecting a one-day directive into a recurring cron prompt (jobs.json direct edit)

Verified 31 Aug 2026 (Threads 06:00 promo job, one-day "vibe coding budgeting app" hook).

## When to use

A recurring daily cron job's prompt needs a directive for ONE specific upcoming run
(e.g. "tomorrow's post uses hook X with product Y"), and the prompt is long — too long
to round-trip through the `cronjob` tool's update param, or you want to avoid touching
the whole prompt. Editing `~/.hermes/cron/jobs.json` directly works; the scheduler
picks the change up.

## Procedure

```python
import json, shutil
path = '/home/ubuntu/.hermes/cron/jobs.json'
shutil.copy(path, path + '.bak_<date>')           # ALWAYS back up first
data = json.load(open(path))
jobs = data['jobs'] if isinstance(data, dict) else data
job = next(j for j in jobs if (j.get('job_id') or j.get('id')) == '<job_id>')
# insert a DATE-BOUND block before the job's task section:
#   "🎯 ARAHAN KHUSUS POST <DATE> (HANYA berlaku untuk tanggal ini; kalau tanggal
#    sudah bukan <DATE>, ABAIKAN blok ini): ..."
job['prompt'] = job['prompt'].replace("TUGAS HARI INI:", arahan + "\n\nTUGAS HARI INI:", 1)
json.dump(data, open(path, 'w'), ensure_ascii=False, indent=2)
```

## File schema notes (jobs.json ≠ cronjob tool display)

- Jobs are keyed by **`id`** in the file (the tool surface calls it `job_id`).
- `schedule` is a dict `{"kind": "cron", "expr": "0 6 * * *", "display": "..."}`, not a string.
- `enabled` boolean, `next_run_at` ISO string — verify these survive the edit.

## Verification

- `search_files(pattern="ARAHAN KHUSUS", path="~/.hermes/cron/jobs.json")` — confirm the
  insert landed in the prompt field.
- `cronjob action=list` shows only `prompt_preview` (the HEAD of the prompt) — a
  mid-prompt insert will NOT show there; trust the file grep.
- Make the directive explicitly date-bound ("kalau tanggal sudah bukan <DATE>, ABAIKAN")
  so it self-expires and never leaks into later runs.
