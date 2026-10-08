---
name: budget-concurrency-against-provider-rate-limits
description: Use when sending many model calls in parallel. Size concurrency to the tier's RPM/TPM limit, back off on 429, and bound the queue so a batch does not stall or overrun cost.
---

# Budget concurrency against provider rate limits

Provider limits are per-minute tokens and requests, not per-second guesses. Size your worker pool to the tier and let backoff absorb the rest, or your batch spends its life in 429s.

## Procedure

1. Find the real limits: requests per minute (RPM) and tokens per minute (TPM) for your tier. TPM usually binds first for large prompts.

2. Size concurrency from tokens, not requests: `workers = (TPM * 0.8) / avg_tokens_per_call / (60 / avg_latency_s)`. Target ~80% of the limit; the margin absorbs bursts.

3. Pace the queue: put a token-bucket or leaky-bucket in front of the API, not a bare `ThreadPoolExecutor(max_workers=64)`.

```python
# refill TPM/60 tokens per second; block until a permit is available
bucket = TokenBucket(rate=tpm/60, capacity=tpm*0.1)
with bucket.permit(est_tokens(prompt)):
    call_api(prompt)
```

4. On 429, back off with jitter and honour `Retry-After`; respect a `remaining`/`reset` header if the provider sends one.

5. Bound the in-flight queue and the retry count so a stall fails fast instead of buffering the whole batch in memory.

6. Sample actual TPM during the run and log headroom; a batch that runs near 100% will trip limits on any input variance.

7. Run large batches off-peak or on a provisioned tier if the limit is the bottleneck — raising concurrency will not beat a hard cap.

## Pitfalls

- Treating RPM as the only limit; a few huge prompts blow the TPM budget while request count looks fine.
- Concurrency set once and never revisited as prompts grew, so the same pool now overruns TPM.
- Retrying a 429 immediately, turning throttling into a self-inflicted denial of service.
- No jitter in backoff, so all workers retry in lockstep and re-trigger the limit together.
- An unbounded queue: memory grows with the batch when the API stalls instead of jobs failing.

## Verification

    python3 run_batch.py --log usage.jsonl && jq -s 'map(.tpm)|max' usage.jsonl   # observed peak TPM must stay under the tier limit

Report: "pitched 12 workers at the 400k TPM tier (~78% util); batch of 50k calls hit 0 hard 429s, 3 soft throttles absorbed by backoff; peak observed 372k TPM."
