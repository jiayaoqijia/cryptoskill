---
name: build-a-resettable-practice-sandbox
description: Use when learners need to practice against a realistic system without risking real data. Provides a containerised, seeded environment with a one-command reset, so mistakes are free and every session starts identical.
---

# Build a Resettable Practice Sandbox

Practice on production teaches fear; practice on a fake that drifts teaches wrong habits. A seeded container with a one-command reset makes every mistake cheap and every session reproducible.

## Procedure

1. Define the environment in `docker-compose.yml`: app, database, and any queue, all pinned to explicit image digests.
2. Seed deterministic data in `seed.sql` with fixed ids and timestamps, so learners can share expected answers.
3. Provide the reset as one target: `make reset`, which runs `docker compose down -v`, `up -d`, then loads `seed.sql`.
4. Print a readiness check the learner can trust: `psql -tAc 'select count(*) from users'` should print `100`.
5. Never mount real credentials or a production network; the compose file must declare its own network.
6. Add a "break it" task: drop a table, run `make reset`, confirm the learner is back to green.
7. Document the reset command at the top of the exercise `README.md`, not buried in the `Makefile`.
8. Pin the seed date so time-dependent queries return the same rows tomorrow.
9. Cap container memory and CPU so a runaway practice loop cannot freeze the laptop.
10. Ship a smoke test `make check` that fails if the seed count is wrong, so a broken sandbox is caught early.
11. Add a `.dockerignore` so builds are fast and no local secrets are copied in.
12. Name the database and volume explicitly so `down -v` targets the right one.
13. Print the reset instructions on a failed smoke test, so the fix is one command away.
14. Document the exact reset command in one line at the top of the README.
15. Keep the seed small enough to load in seconds.
16. Log the container start time so a stuck boot is obvious.

## Pitfalls

- Seeding with `now()` or random ids, so two learners get different answers.
- A reset that drops the volume but not the schema, leaving stale state behind.
- Pointing the sandbox at a shared staging database "just for convenience".
- Requiring a dozen manual steps to reset, so learners avoid experimenting.
- Leaving a real API key in the compose file for realism.
- Pin tags instead of digests, so a rebuild silently pulls a new image.
- Binding to a port already in use on the laptop, so startup fails confusingly.
- A seed script that depends on the wall clock.
- Assuming `docker` is installed without checking during bootstrap.
- Reset buried under three make targets so nobody finds it.
- A seed so large that resetting interrupts practice.
- A silent hang on startup that looks like a broken exercise.

## Verification

    make reset && psql -tAc 'select count(*) from users'
    # passes when the count is exactly 100 after reset, and drops again after a deliberate break

Report to the user: the reset command, the readiness check, and the pinned image digests.
