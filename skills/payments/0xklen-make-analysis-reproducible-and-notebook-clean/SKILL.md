---
name: make-analysis-reproducible-and-notebook-clean
description: Use when delivering an analysis, notebook, or script. Pins the environment and seeds and keeps the notebook rerunnable from top to bottom.
---

# Make Analysis Reproducible and Notebooks Clean

An analysis is the code plus the environment plus the seed. If any of the three is unpinned nobody — including you tomorrow — can reproduce the number.

## Procedure

1. Freeze dependencies: `python3 -m pip freeze > requirements.txt` (or `uv lock`). Record the interpreter version: `python3 --version`.
2. Seed every RNG and set deterministic flags before the first draw:
   ```python
   import random, numpy as np
   random.seed(0); np.random.seed(0)
   ```
3. Make the run one command from a clean checkout: a `Makefile` target or `./run.sh` that fetches, processes, and writes outputs with no manual steps.
4. Delete hidden state. Restart the kernel and run all cells top-to-bottom; a notebook that only works if cell 7 ran before cell 3 is not reproducible. Fix execution order or promote the notebook to a script.
5. Clear outputs and instrument counters on commit: `jupyter nbconvert --clear-output --inplace analysis.ipynb`. A 40 MB CSV printed into a cell bloats the repo and hides nothing useful.
6. Write derived outputs to `out/` and treat them as disposable artifacts, never as inputs you edit by hand.
7. Record wall-clock runtime and row counts in the log so a silent empty-input run is visible.

```bash
jupyter nbconvert --execute --to notebook --inplace analysis.ipynb \
  --ExecutePreprocessor.timeout=300
```

## Pitfalls

- Cloning a mutable source (a URL, a `latest` tag, a live database) breaks reproducibility as soon as upstream changes — vendor a hash-pinned snapshot.
- Hardcoded absolute paths (`/Users/me/data`) fail on any other machine.
- A notebook that mutates a file in cell 2 and reads it in cell 9 depends on run order; make the dependency explicit.
- Leaving large stdout/plot outputs in the committed notebook hides the code that produced them.
- `np.random` and `random` are separate streams — seed both, plus any library RNG.

## Verification

    jupyter nbconvert --execute --to notebook --stdout analysis.ipynb > /dev/null && echo OK

Run-all from a fresh kernel completes with no errors and the committed output has an unchanged hash. Report: "Re-ran from clean checkout with pinned env; output hash matches <H> — reproducible."
