# generate-changelog

Generate a structured CHANGELOG.md from git history since the last tag.

## When to use
- User asks for a changelog, release notes, or commit summary since a version
- Preparing a GitHub Release body

## How to use
```bash
bash scripts/generate-changelog.sh
# or
python3 scripts/generate-changelog.py
```

## Output
Sections: Added / Fixed / Changed / Removed (conventional-commit mapping).
Writes `CHANGELOG.md` (or stdout with `--stdout`).
