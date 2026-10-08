---
name: cut-over-with-blue-green-deployment
description: Use when a deploy must not cause partial-version downtime — runs two full environments, verifies green in isolation, flips one selector, and keeps blue warm for instant rollback.
---

# Cut over with blue-green deployment

A rolling deploy mixes two versions behind one router; blue-green keeps exactly one version live and flips a single pointer. The cost is double infrastructure during the cutover; the payoff is an atomic switch and a one-command rollback.

## Procedure

1. Stand up green beside blue with the new image but no traffic:
       kubectl apply -f green-deploy.yaml
       kubectl rollout status deploy/app-green
   The service selector still points at blue while green becomes ready.

2. Verify green in isolation before the flip — a green that fails readiness must never receive the flip:
       kubectl port-forward svc/app-green 8081:80 &
       curl -sf localhost:8081/healthz && ./smoke.sh http://localhost:8081

3. Confirm the two versions can share data. Migrations must be backward-compatible (expand/contract). If blue still writes rows green cannot read, stop — a flip would corrupt data.

4. Flip by patching one selector, never by editing replicas:
       kubectl patch svc app -p '{"spec":{"selector":{"version":"green"}}}'
   The switch is one API call, so there is no partial state.

5. Watch the SLOs for 10 minutes — error ratio, p99, saturation. On any breach, flip back with the same one-line patch; blue pods still run the old image and are warm.

6. Keep blue alive for the rollback window (at least the observation period, e.g. 30 min), then scale it to zero:
       kubectl scale deploy/app-blue --replicas=0

7. Drain the old side gracefully: set `terminationGracePeriodSeconds: 30` and a `preStop` hook so in-flight requests finish instead of resetting.

## Pitfalls

- One shared database with a non-backward-compatible migration: the flip creates errors either way (blue sees green's columns, or the reverse). Always expand-then-contract.
- Flipping before green is warm; the first requests hit cold caches and JIT, spiking p99 exactly at cutover.
- Session state pinned to a local pod, so the flip logs every user out. Externalise sessions before blue-green.
- Leaving blue running forever "just in case", doubling cost with no documented rollback runbook.

## Verification

    kubectl get svc app -o jsonpath='{.spec.selector}'   # version: green
    kubectl get endpoints app                            # only green pod IPs
    # rollback drill: patch selector back to blue, confirm endpoints switch in < 5s

Report: green verified before flip, the single API call that performed the switch, endpoints showing only the new version, and a timed rollback drill completing under 5 s.
