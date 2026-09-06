# Maintain Extension E2E

Use this when fixing flaky E2E, cleaning POM bad practices, or auditing a PR for
anti-patterns. For greenfield specs, start at [`writing-tests.md`](writing-tests.md).

## Workflow

```
1. Reproduce locally (single spec, --leave-running if useful)
2. Classify: flake pattern vs structural POM smell vs both
3. Flake → open flakiness.md and apply the matching before/after fix
4. POM smell → open pom-antipatterns.md and refactor
5. Prefer waits / mocks / FixtureBuilderV2 over retries and delays
6. Re-run: yarn test:e2e:single <path> --browser=chrome
7. Self-check pom-antipatterns.md again before submitting
```

## Classification hints

| Symptom | Start here |
| --- | --- |
| Intermittent timeout, stale element, wrong window | [`flakiness.md`](flakiness.md) |
| Locators in flow/spec, try/catch in POM, `driver.delay`, PO→PO | [`pom-antipatterns.md`](pom-antipatterns.md) |
| Missing mocks / live network | [`flakiness.md`](flakiness.md) (mocks + allowlist sections) |
| Spec calls `driver.clickElement` directly | [`pom-antipatterns.md`](pom-antipatterns.md) |

## Hard rules while fixing

- Do not add `try/catch` in page objects or flows to “make it pass”.
- Do not paper over races with `driver.delay` unless a comment explains why a
  condition wait is impossible.
- Do not move locators into the spec or flow “temporarily”.
- Do not rely on Cursor Bugbot on the PR to catch regressions — self-check and
  run review locally; see [`pom-antipatterns.md`](pom-antipatterns.md).

## Related in-repo docs

- `test/e2e/AGENTS.md`
- `.cursor/BUGBOT.md` (local review rules, sections 3.1–3.9)
