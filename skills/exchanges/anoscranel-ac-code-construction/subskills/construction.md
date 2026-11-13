---
name: construction
domain: software-engineering/construction
trigger: "\"Implement this\", \"write the function\", \"how should I name this\", \"how should this handle errors\", \"set up the linter and formatter\", \"add type checking\"."
anti_trigger: "Order and size of steps (subskills/incremental-delivery.md); cleaning up working code; test design."
scope: "Writing new code: naming, error handling, lint and static-analysis gates"
status: "seedling"
---

# Construction

## Standard

- **SWEBOK v4** Software Construction KA (https://www.computer.org/education/bodies-of-knowledge/software-engineering/topics).
- **Names** reveal intent and use domain terms (Martin, *Clean Code*, 2008; Evans, *DDD*, 2003 ubiquitous language).
- **Comments** explain why, not what (Ousterhout 2018).
- **Formatter as law**: gofmt, Black, Prettier, rustfmt; EditorConfig for the rest.
- **Linters and types**: ESLint v9 flat config, Ruff, Clippy, Semgrep; `tsc --noEmit`, mypy/pyright, `cargo check`.
- **Error handling**: OWASP Top 10:2025 adds A10 "Mishandling of Exceptional Conditions" (https://owasp.org/Top10).
- **Local gates** at commit via pre-commit (https://pre-commit.com).

## Decision rules

1. Name for the reader and for grep. Domain words over generic ones (`invoice`, not `data`). Booleans read as questions (`isExpired`).
2. A function does one thing at one level of abstraction. Long is fine if it reads top to bottom; nesting over three levels is not.
3. Errors:
 - Validate input at the boundary. Inside, trust typed values.
 - Fail fast on programmer errors. Return or raise typed errors for expected failures.
 - Never swallow an exception. Catch only what you can handle; add context and re-raise.
 - Release resources on every path (`with`, `defer`, `try/finally`, RAII).
 - Retries only for transient errors, bounded, with backoff and jitter.
4. No magic numbers. Name the constant and its unit (`TIMEOUT_MS = 5000`).
5. Make illegal states unrepresentable: enums or sealed types over string flags.
6. Pure logic separate from I/O, so tests need no mocks.
7. New modules get strict type checking. Legacy may stay relaxed, with a budget for ignores.
8. Every lint suppression carries a reason on the same line.
9. Do not adopt a numeric complexity threshold as a hard gate; the evidence is weak (Shepperd 2008). Track it as a trend.

## Procedure

1. Read the task's done condition and the module's existing style.
2. Write the signature and types first. Name inputs, outputs and errors.
3. Write the happy path. Then each failure path from rule 3.
4. Run the gates locally:
   ```yaml
   # .pre-commit-config.yaml (example)
   repos:
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: <pinned-tag>
       hooks: [{id: ruff}, {id: ruff-format}]
     - repo: https://github.com/gitleaks/gitleaks
       rev: <pinned-tag>
       hooks: [{id: gitleaks}]
   ```
 Then `pre-commit run --all-files` and the type checker.
5. Fix every new warning. Suppress only with a reason.
6. Add a why-comment where a choice is not obvious from the code.
7. Self-read the diff once as a stranger. Rename anything you had to think about.

## Anti-patterns

- `catch (e) {}` or `except: pass`.
- Error codes mixed with exceptions in one module.
- Comments that restate the code.
- Abbreviations only the author knows.
- Formatter config debates; pick the tool default.
- Gates that run only in a distant CI.

## Done checklist

- [ ] Formatter, linter, type checker and secret scan pass.
- [ ] Every failure path handled or explicitly propagated.
- [ ] No unexplained suppression.
- [ ] Names read clearly to a stranger.
- [ ] Why-comments where needed.

## Sources

- <https://go.dev/blog>
- <https://www.iso.org/standard/78176.html>
- https://pre-commit.com · https://owasp.org/Top10
