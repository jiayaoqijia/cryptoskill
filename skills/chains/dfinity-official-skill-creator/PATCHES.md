# Local Patches to skill-creator

This copy of skill-creator diverges from the upstream Anthropic release. Do NOT update via `npx skills add` — doing so will overwrite these fixes with no warning.

To update intentionally: re-run `npx skills add`, then manually re-apply each patch listed here.

Upstream repo: https://github.com/anthropics/skills/tree/main/skills/skill-creator
Upstream commit SHA: `b0cbd3df1533b396d281a6886d5132f623393a9c` (last changed upstream: 2026-03-06)
Vendored into this repo on: 2026-05-29

---

## Patch 1 — `eval-viewer/generate_review.py`: `</script>` breaks viewer

**Problem:** `json.dumps` does not escape `</script>`. Eval output containing HTML with script tags (e.g. a generated `index.html`) closes the `<script>` block in `viewer.html` prematurely — the entire viewer breaks.

**Fix:** Added `.replace("</script>", r"<\/script>")` after `json.dumps`.

**Confirmed in:** testrun on a full-stack hello-world skill that generated `index.html` with a `<script type="module">` tag.

---

## Patch 2 — `SKILL.md`: Missing `run-1/` level in output paths

**Problem:** SKILL.md instructed saving outputs to `eval-<ID>/with_skill/outputs/`. The `aggregate_benchmark.py` script globs for `run-*` inside config directories and silently skips any config dir without a `run-N/` subdirectory — all runs show 0% pass rate and the viewer shows "(No prompt found)".

**Fix:** Changed all output paths to `eval-<ID>/with_skill/run-1/outputs/` (and equivalents for baseline configs). Added note to copy `eval_metadata.json` into each config directory.

---

## Patch 3 — `SKILL.md`: Eval directory naming conflict

**Problem:** SKILL.md said to give evals "a descriptive name" and use it for the directory. `aggregate_benchmark.py` globs for `eval-*` and parses the numeric ID from `split("-")[1]` — a directory named `full-stack-hello-world/` silently disappears from benchmark results.

**Fix:** Changed instruction to require the `eval-0-descriptive-name/` format (numeric prefix required, descriptive suffix optional).

---

## Patch 4 — `SKILL.md`: `--static` flag wrong for Claude Code

**Problem:** SKILL.md said to use `--static` when `webbrowser.open()` is not available or "the environment has no display." In Claude Code (VS Code extension, desktop app), `webbrowser.open()` works correctly. `--static` generates a `file://` URL; browsers block certain JS APIs for `file://` pages, causing outputs not to render — same visible symptom as Patch 1 but a different root cause.

**Fix:** Clarified that Claude Code should always use server mode. `--static` is only for truly headless environments (Cowork — Anthropic's browser-based coding environment — CI, or a remote server with no graphical display).

---

## Patch 5 — `scripts/quick_validate.py`: PyYAML (third-party) replaced with stdlib parser

**Problem:** `quick_validate.py` imported `yaml` (PyYAML), a third-party library not declared as a dependency. In a clean Python environment, `package_skill.py` fails at import time before any packaging can occur (`from scripts.quick_validate import validate_skill`).

**Fix:** Replaced `yaml.safe_load` with a minimal stdlib-only YAML parser (`_parse_simple_yaml`) that handles the flat key-value + one-level-nesting structure used by all SKILL.md frontmatter. No external dependencies.
