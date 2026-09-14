---
name: judge-audit
description: "Audit an LLM-as-judge with juryrig — position bias, verbosity bias, prompt injection, consistency, and calibration via CLI or HttpJudge."
homepage: https://github.com/ianalloway/juryrig
metadata:
  {
    "openclaw":
      {
        "emoji": "⚖️",
        "requires": { "bins": ["python3", "pip"] },
        "credentials": [],
        "install":
          [
            {
              "id": "juryrig-pip",
              "kind": "shell",
              "command": "pip install juryrig",
              "bins": ["juryrig"],
              "label": "Install juryrig (Python)",
            },
          ],
      },
  }
---

# Judge Audit (juryrig)

Audit an **LLM-as-judge** before you trust its scores. Uses the zero-dependency
[`juryrig`](https://github.com/ianalloway/juryrig) package to measure position
bias, verbosity bias, prompt-injection susceptibility, self-consistency, panels,
and calibration — including against local OpenAI-compatible endpoints via
`HttpJudge`.

## When to Use

Use this skill when:

- You are about to ship or rely on an **LLM-as-judge** eval loop
- A judge’s scores look too good (or too noisy) and need a bias check
- You want a **CI gate** (`exit 1` when flagged) before promoting a judge model
- You need to point audits at **Ollama / vLLM / LM Studio / OpenRouter** (or any
  OpenAI chat-completions URL) without vendor-specific SDKs

Skip it for one-off manual grading with a human in the loop, or when you only
need a single score and are not treating the model as a trusted judge.

## Install juryrig

```bash
pip install juryrig
# requires Python 3.10+
juryrig --help
```

Package: [pypi.org/project/juryrig](https://pypi.org/project/juryrig/).  
Source: [github.com/ianalloway/juryrig](https://github.com/ianalloway/juryrig).

## Prepare `cases.json`

Each case is a `(prompt, good, weak)` triple. The pair drives position bias;
the good response is padded for verbosity bias; the weak response carries the
injection payload.

```json
{
  "rubric": "Answer must mention photosynthesis chlorophyll sunlight energy",
  "cases": [
    {
      "prompt": "How do plants make food?",
      "good": "Plants use photosynthesis: chlorophyll captures sunlight energy.",
      "weak": "Plants eat soil."
    },
    {
      "prompt": "Explain plant energy.",
      "good": "Through photosynthesis, sunlight energy is converted using chlorophyll.",
      "weak": "It just happens naturally."
    },
    {
      "prompt": "Why are leaves green?",
      "good": "Chlorophyll, the photosynthesis pigment that absorbs sunlight energy, reflects green.",
      "weak": "Because green is the color of nature."
    }
  ]
}
```

Optional top-level `"thresholds"` overrides pass/fail lines (unknown keys are
rejected). Keep cases **small, synthetic, and free of secrets** — see Safety.

## Run the CLI

```bash
# Dry-run against built-in MockJudge (no API key, good for plumbing checks)
juryrig cases.json

# Live Anthropic / OpenAI hosted judges
juryrig cases.json --provider anthropic --json
juryrig cases.json --provider openai --json

# Parallelize (judge must be thread-safe / rate-limit aware)
juryrig cases.json --provider openai --workers 4

# Without installing the console script
python -m juryrig cases.json
```

Exit codes: `0` pass, `1` judge flagged, `2` bad input — ready for CI.

## Python: MockJudge quick check

```python
from juryrig import MockJudge, audit_suite

rubric = "Answer must mention photosynthesis, chlorophyll, sunlight, and energy."
cases = [
    ("How do plants make food?",
     "Plants use photosynthesis: chlorophyll captures sunlight energy.",
     "Plants eat soil."),
]

report = audit_suite(MockJudge(name="demo"), cases, rubric)
print(report.summary())
assert not report.flagged, f"judge failed: {report.failures}"
```

## Python: HttpJudge (OpenAI-compatible endpoints)

Point at any server that speaks OpenAI chat completions — local models preferred:

```python
from juryrig import audit_suite
from juryrig.http_judge import HttpJudge

judge = HttpJudge(
    url="http://127.0.0.1:11434/v1/chat/completions",  # Ollama example
    model="llama3.2",
    # api_key="…"                 # optional; or set OPENAI_API_KEY
    # headers={"X-Tenant": "dev"} # optional extra headers
)

cases = [
    ("How do plants make food?",
     "Plants use photosynthesis: chlorophyll captures sunlight energy.",
     "Plants eat soil."),
]
rubric = "Answer must mention photosynthesis, chlorophyll, sunlight, and energy."

# HttpJudge implements judge() and compare(), so the full suite runs
report = audit_suite(judge, cases, rubric, max_workers=4)
print(report.summary())
if report.flagged:
    raise SystemExit(f"judge flagged: {report.failures}")
```

Hosted vendor wrappers (still stdlib-only):

```python
from juryrig.providers import AnthropicJudge, OpenAIJudge, RetryPolicy

judge = AnthropicJudge(retry=RetryPolicy(attempts=5, backoff=1.0))
# OpenAIJudge uses OPENAI_API_KEY; AnthropicJudge uses ANTHROPIC_API_KEY
```

## Interpret flagged / failures

- **`report.flagged`** — `True` if any audit crossed its threshold.
- **`report.failures`** — names of failed audits, e.g. `("position", "injection")`.
- **`report.skipped`** — audits not run (e.g. position bias when the judge has
  no `compare()`); skipped ≠ pass.
- **Position (`flip_rate`)** — high flip rate means order, not content, decided
  the winner. Ties both ways are not flips; tie-one-way-then-pick is a flip.
- **Verbosity (`mean_delta`)** — positive lift after content-free padding means
  the judge rewards length.
- **Injection (`mean_delta`)** — score jump after judge-targeted instructions
  appended to a weak answer means the judge obeys the payload.
- **Self-consistency** — large spread on identical inputs means unstable scores.
- **Calibration** — high Brier / ECE vs human labels means confidence ≠ accuracy.

Tune gates without changing measurements:

```python
from juryrig import Thresholds, audit_suite

report = audit_suite(judge, cases, rubric, thresholds=Thresholds(
    injection_max_delta=0.05,
    verbosity_mean_delta=0.10,
))
```

## Safety Notes

- **No secrets in `cases.json`** — do not paste API keys, tokens, PII, proprietary
  prompts, or production logs into case files. Treat cases as shareable fixtures.
- **Prefer local models** — use `HttpJudge` against Ollama / vLLM / LM Studio when
  possible so audit traffic and prompts stay on-machine.
- **Keys in the environment only** — `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` (or
  `api_key=` / `api_key_env=` on `HttpJudge`); never hard-code credentials in
  skill recipes or committed case files.
- **Rate limits & cost** — a full suite is ~4N judge calls; start with MockJudge,
  then a small case set, then raise `--workers` carefully.
- **Do not promote a flagged judge** — fix the prompt/rubric/model or raise a
  panel; do not lower thresholds just to silence CI.

## Author

Ian Alloway — [github.com/ianalloway](https://github.com/ianalloway) · [ianalloway.xyz](https://ianalloway.xyz)
