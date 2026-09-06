# Extension POM anti-patterns

Agent checklist for Page Object Model defects under `test/e2e/`. These are
maintainability defects that cause flakes and expensive rewrites — treat them as
must-fix when creating or reviewing E2E code.

The same rules exist as **local** review rules in the Extension repo:

- `.cursor/BUGBOT.md` (sections 3.3–3.9)

## Checklist (flag and fix)

| Anti-pattern | Prefer |
| --- | --- |
| Locators (`data-testid`, `{ css }`, `{ text, tag }`, `*Button`/`*Input` constants) in `page-objects/flows/**` | Move locators into `page-objects/pages/**`; flow only calls page methods |
| Flow that instantiates exactly one page object and no other flow | Move the method onto that page object |
| UI helper in a `*.spec.ts` that clicks/fills/waits or builds page objects | Page object method, or a flow if multi-page |
| Spec calls `driver.clickElement` / `findElement` / `waitForSelector` / `fill` / … for UI | Call page object or flow; keep locators in pages |
| `driver.delay(` or bare `setTimeout` without a justifying comment | `waitForSelector`, `waitForElementNotPresent`, `driver.wait` |
| Page object imports/instantiates another page (`new OtherPage(this.driver)`) | Multi-page steps belong in a flow |
| `try`/`catch` in page objects or flows (except `driver.wait` poll returning `false`) | Let failures surface; use wait helpers and `check*` methods |

## Create / maintain process tie-in

- After writing E2E: run this checklist before submit.
- When fixing flakes: if the root cause is structural, fix here first, then apply
  [`flakiness.md`](flakiness.md) patterns.

## Where Bugbot fits (MMQA-2248 outcome)

Bugbot is used **locally only** — as a last-resort safety net, never as a merge
gate:

| Where | Behaviour |
| --- | --- |
| Local CODEBOT / `/review` / local Bugbot run | Reads `.cursor/BUGBOT.md` and applies sections 3.1–3.9 reliably. Run it before you push. |
| Bugbot on the PR | Often reports **no new issues** even with POM violations in the diff: team/learned rules and the Default effort level bias it toward high-confidence bugs, not style/POM gates. Not enforced, not relied on. |
| Cursor dashboard settings | Effort level, learned rules, and team rate limits are dashboard-only; a repo cannot change them. |
| Deterministic ESLint rules for POM | Possible future work; out of scope here. |

**Bottom line:** prevent bad E2E by following this skill while writing and
maintaining tests, then self-check with this checklist. Treat a local Bugbot
finding as a backstop for something you missed — not as the primary gate.
