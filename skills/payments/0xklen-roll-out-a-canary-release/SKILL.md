---
name: roll-out-a-canary-release
description: Use when a change is too risky for an all-at-once deploy — routes a small traffic slice to the new version, gates promotion on SLO comparison against stable, and reverts on regression.
---

# Roll out a canary release

Ship to 1% of traffic first. Compare the canary's error rate and latency against the stable version on the same traffic mix, and promote only if the canary is not worse. This catches the regressions that pass every pre-production test.

## Procedure

1. Route by a stable key (user-id hash, header, or mesh weight) so a user's experience is consistent within the canary, not round-robin per request:
       # Istio VirtualService
       http: [{ route: [ {destination: {host: app, subset: stable},  weight: 99},
                          {destination: {host: app, subset: canary}, weight: 1 } ] }]

2. Size the canary so the sample is meaningful: at least 1000 requests and 30 minutes before judging. At 1% of 100 rps that is about 17 minutes of traffic.

3. Compare against stable measured *at the same time*, never against yesterday — the traffic mix shifts daily:
       canary_err = rate(err{version="canary"}[5m]) / rate(req{version="canary"}[5m])
       stable_err = rate(err{version="stable"}[5m]) / rate(req{version="stable"}[5m])

4. Promotion gates, all must hold: canary error ratio ≤ stable + 0.2 pp, canary p99 ≤ stable × 1.1, no error code new to the canary, canary saturation < 0.8.

5. Step the weight 1 → 5 → 25 → 50 → 100, holding each step at least 15 minutes and re-checking the gates. On any breach, set the canary weight to 0 immediately and keep the pods for logs.

6. Automate the gate with Argo Rollouts `AnalysisTemplate` or Flagger so promotion is not a human watching a dashboard at 2 a.m.

7. Run the canary long enough to catch slow leaks — memory, file descriptors, goroutines — which all pass a 15-minute latency check.

## Pitfalls

- Judging on too little traffic: 20 requests give a meaningless ratio and the gate flaps.
- Comparing the canary with yesterday's stable, so a global regression looks like a canary-only win.
- A canary that differs from stable in more than the code (different config or replica count) — you are then measuring the wrong variable.
- A new error path affecting only a specific customer segment, hidden by the aggregate ratio; break down by `code` and by `route`.

## Verification

    kubectl argo rollouts get rollout app --watch
    # steps advance only while analysis passes; setWeight 0 on failure
    curl -s 'localhost:9090/api/v1/query?query=sum(rate(err{version="canary"}[5m]))/sum(rate(req{version="canary"}[5m]))' | jq

Report: the weight schedule, the gate thresholds, the canary-vs-stable error and p99 deltas at each step, and either promotion or the timestamped revert.
