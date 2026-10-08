---
name: detect-a-degraded-model-endpoint
description: Use when a model API is slow intermittently or quietly returning worse output while still answering 200. Detect degradation from metrics and output sampling, not by waiting for an error.
---

# Detect a degraded model endpoint

A provider can be "up" — 200 OK, fast-ish — while serving worse answers or a truncated model behind the scenes. Uptime is not quality. Watch both.

## Procedure

1. Track per-call signals: latency percentiles (p50/p95/p99), tokens-in/out ratio, `finish_reason` distribution, schema-fail rate, and refusal rate. A shift in any of these precedes user complaints.

2. Baseline the signals over a quiet week; alert on deviation, not on absolute values.

3. Watch for the tell-tales of degradation: a jump in `finish_reason: length` (output hitting a hidden cap), a sudden rise in truncated JSON, or a drop in response length for the same prompt.

4. Sample outputs continuously: run a small fixed probe set (10-20 known-answer cases) every few minutes and score it automatically. Quality regressions show up here before volume metrics notice.

```bash
while :; do curl -s "$API" -d @probe.json | jq -c '{fr:.choices[0].finish_reason, n:(.choices[0].message.content|length)}'; sleep 300; done
```

5. Distinguish the causes: your traffic changed (new inputs), the provider changed (version/aliasing), or the network is slow. Only the middle one is theirs.

6. On confirmed degradation, switch traffic to the fallback provider and raise it with the provider's status page, evidence attached.

7. Record the window and the signatures so the postmortem has data, not vibes.

## Pitfalls

- Alerting on p100 latency; one slow request fires constantly — use percentiles over a window.
- Watching only error rates; degradation returns 200s and hides from that metric entirely.
- Running the quality probe on prompts you tuned to pass, which stay green while real traffic degrades.
- Assuming a provider incident is the cause when your own prompt or traffic shifted — check both sides first.
- Treating a slow-but-correct endpoint as healthy or a fast-but-wrong one as degraded; measure both axes.
- Probing on a fixed schedule and missing a short degradation window between probes; shorten the interval if incidents are brief.
- Comparing against an absolute threshold instead of your own baseline, so a normally-slow provider alerts constantly.
- Sampling only successes; a degraded endpoint that also drops calls needs error rate beside the quality probe.

## Verification

    python3 probe_score.py --window 24h   # prints p95 latency, schema-fail %, probe accuracy vs a 7-day baseline

Report: "probe accuracy dropped from 96% to 71% and finish_reason=length rose 40x at 03:10 while latency held — degraded quality detected; traffic failed over to the secondary."
