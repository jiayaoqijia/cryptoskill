---
name: poll-an-async-job-to-completion
description: Use when an API returns 202 and a job id instead of the result. Poll the status endpoint with backoff until a terminal state, under a deadline, and surface the job id.
---

# Poll an async job to completion

A 202 means "accepted, not done". Treating the first poll as the answer, or polling in a tight
loop, are the two ways this goes wrong.

## Procedure

1. Capture the job handle from the 202: the `Location` header or a `{"job_id": "..."}` body.
2. Poll on a jittered, growing interval capped at ~30 s, with a deadline:
   ```python
   import time, random
   deadline = time.time() + 600
   n = 0
   while time.time() < deadline:
       s = get(f"/v1/jobs/{job_id}").json()
       if s["status"] in ("succeeded", "failed", "cancelled", "expired"):
           break
       time.sleep(min(30, 1.5**n) * (0.5 + random.random())); n += 1
   ```
3. Treat `succeeded`, `failed`, `cancelled`, `expired` as terminal; everything else loops.
4. On `failed`, read the error object and surface it; never re-poll a dead job.
5. On deadline expiry, give up with "timed out, job <id> still <status>" — jobs can run for hours.
6. Prefer a completion webhook or SSE over polling when the API offers one.
7. Record the job id in your own logs so a stuck job can be chased later.

## Pitfalls

- Polling every 100 ms hammers the API and often gets you rate limited before the job finishes.
- Assuming a short job means done after one poll; long tails exist.
- No deadline means a loop that never ends when a job hangs in `running`.
- A job can be `succeeded` with a partial-result field; check the payload, not just the status.
- Polling a job owned by another credential returns 404, not your result — check ownership.

## Verification

    python jobs/wait.py --id "$JOB" --deadline 600; echo "exit=$?"    # 0 with a terminal state

Report: "Job ab12... reached succeeded in 47s after 6 polls."
