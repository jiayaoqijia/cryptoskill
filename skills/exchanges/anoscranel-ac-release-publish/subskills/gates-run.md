---
name: gates-run
domain: skill-authoring/gates-run
trigger: "Running local checks before a release commit; a tree that must be clean enough to audit; a scan that failed on a build artifact"
anti_trigger: "Building the claim inventory; briefing an independent auditor; judging whether a repair introduced a defect"
scope: "Running structure, security, YAML, link, and private-data gates on the exact bytes that will ship, leaving no artifacts in the tree"
status: "seedling"
---

# Gates Run

## Standard

- **YAML 1.2.2**: a parser accepts a document or reports an error; "it looks fine" is not a parse. <https://yaml.org/spec/1.2.2/>
- **Python `-B`**: the flag stops the interpreter writing bytecode, so a check leaves the tree as it found it. <https://docs.python.org/3/using/cmdline.html#cmdoption-B>
- **Reproducible builds**: the tested artifact and the shipped artifact must be the same bytes. <https://reproducible-builds.org/>
- ⚠️ House convention: warnings are read and either closed or recorded. A pass carrying unread warnings is not a pass.

## Decision rules

1. Gates run after the final content edit. A run before an edit is void.
2. Run every gate from the root of the tree that will be committed.
3. Use `python3 -B` throughout. `python3 -m py_compile` writes `__pycache__` into the tree, and the security scan then fails on a build artifact.
4. The structural linter must report a full pass, and the security scan must be clean. A warning or suppression is a recorded decision.
5. Every frontmatter block parses strictly and contains `name`.
6. Every relative link resolves from the file that holds it.

## Procedure

1. Starting state: `git status --porcelain` lists only the intended files.
2. Structural lint from the tree root: `python3 -B <linter> .` If the pack ships no linter, check by hand: unique names, required fields, every indexed file on disk, no symlinks, no non-markdown files. Read all output; fix and rerun.
3. Security scan: `python3 -B <scanner> .` Fix a finding at the source; never narrow the scanner to pass.
4. Strict YAML on every markdown file:

   ```
   python3 -B - <<'PY'
   import pathlib, sys, yaml
   bad = 0
   for p in sorted(pathlib.Path(".").rglob("*.md")):
       t = p.read_text(encoding="utf-8")
       if not t.startswith("---\n"):
           print("no fence:", p); bad += 1; continue
       try:
           d = yaml.safe_load(t.split("\n---", 1)[0][4:])
       except Exception as e:
           print("yaml:", p, e); bad += 1; continue
       if not isinstance(d, dict) or not d.get("name"):
           print("name:", p); bad += 1
   sys.exit(1 if bad else 0)
   PY
   ```

5. Links: resolve each relative link from its own file's directory; fail on a missing target or one outside the tree.
6. Private data: search for home paths, usernames, host names, and token shapes; record the patterns.
7. Check whitespace after a multiline regex edit: `grep -rnE '^[[:space:]]+$' .` A whitespace-only line usually means a replacement swallowed a newline.
8. Build artifacts: `find . \( -name '__pycache__' -o -name '*.pyc' \) -print` Empty output passes.
9. Rerun from step 2 after any fix; the last run must be on the bytes you commit.

## Anti-patterns

- **Compile check that pollutes the tree.** `py_compile` leaves `__pycache__`, and the next scan fails. Fix: `python3 -B`, or compile in a scratch copy.
- **Gates before the last edit.** The fix lands, the old result stays. Fix: rerun everything after the final edit.
- **Scanner narrowed to pass.** Fix: change the file, not the pattern.

## Done checklist

- [ ] Every gate ran on the final tree, after the last edit.
- [ ] `python3 -B` used throughout; no `__pycache__` in the tree.
- [ ] Structural lint: full pass, warnings closed or recorded.
- [ ] Security scan clean, or each suppression has a reason.
- [ ] Every frontmatter parses strictly and carries `name`.
- [ ] Every link resolves; no private paths, handles, tokens, or whitespace-only lines.

## Sources

- YAML 1.2.2: <https://yaml.org/spec/1.2.2/>
- Python `-B`: <https://docs.python.org/3/using/cmdline.html#cmdoption-B>
- Reproducible builds: <https://reproducible-builds.org/>
- GNU grep: <https://www.gnu.org/software/grep/manual/grep.html>
