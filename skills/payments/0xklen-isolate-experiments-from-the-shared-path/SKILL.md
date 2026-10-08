---
name: isolate-experiments-from-the-shared-path
description: Use when new code, flags or experiments run on the live request path and must not be able to take down the shared path — wraps each in an error boundary, samples it, and keeps a kill switch wired to it.
---

# Isolate experiments from the shared path

An experiment that raises on a null field, mutates shared state, or adds latency is indistinguishable from a product outage once it is on the live path. Isolation means the experiment can fail, be slow or be wrong without affecting the users who are not in it. A `try/catch` around the variant is the whole mechanism.

## Procedure

1. Put every experiment behind an error boundary so its failure returns the *control* behaviour, never a 5xx. Catch, log, and fall through:
       try { variant = experiment.render(user) } catch (e) { log("exp.error", e); variant = control }

2. Allocate the experiment its own budget, not the request's: its own timeout (e.g. 50ms), its own concurrency cap, and no unbounded work. An experiment that can block the request thread is a request-path change, not an experiment.

3. Never let an experiment write to shared state without going through the same validation and idempotency as production code. An experiment that writes half a record under a flag is corruption with a side of "it was only a test".

4. Sample by a stable hash of user id, not random-per-request, so a user sees a consistent variant:
       bucket = crc32(user_id) % 100; variant = bucket < 10 ? "B" : "control"
   Random-per-request flips users between variants mid-session and corrupts the measurement.

5. Size the sample to the decision: a 1% slice gets a usable answer for a big effect in days, not for a 2% lift. Compute the required sample beforehand; an underpowered experiment is a waste of production risk.

6. Wire a kill switch the experiment checks *first*: a flag value that returns control for 100% of traffic, verifiable in staging. The switch must not depend on the experiment code path itself.

7. Exclude the experiment from anything safety-critical: no experiment on the payment path, the auth decision, or the data-deletion path. Run those as a behind-the-scenes shadow/tap, not as a live variant.

## Pitfalls

- An experiment that throws and takes the whole page down for the treatment group; the error boundary is what makes the experiment safe, and it is the first thing skipped.
- A/B by random-per-request, so the "variant" a user sees changes mid-flow and neither arm is measured cleanly.
- Exposing an unauthenticated experiment endpoint an attacker can force to evaluate (a debug flag), effectively an injection surface.
- No kill switch, so the only way to stop a harmful experiment is a full deploy reversal, which is far slower than the experiment's own rollout.

## Verification

    # force the experiment to throw and confirm the page still renders (control)
    curl -s localhost:8080/exp/_force_error && curl -s -o /dev/null -w '%{http_code}\n' localhost:8080/home
    # expect 200, control rendering, exp.error logged
    # kill switch returns everyone to control
    curl -s -X POST localhost:9090/flags/exp_new_recs -d '{"value":0}'
    curl -s localhost:8080/home | grep -c 'variant-B'   # 0
    grep -n 'exp.error' /var/log/app.log

Report: the error boundary, the experiment's own budget, the sampling method and required sample size, and a forced-failure run where the shared path stayed at 200 while the experiment logged its error.
