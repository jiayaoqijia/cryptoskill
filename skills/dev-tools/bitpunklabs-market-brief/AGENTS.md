# Repository guidance

Read [SKILL.md](SKILL.md) for the product workflow. This repository is one skill:
`market-brief`, backed by the complete prompts in `assets/prompts/`.

- Keep project documentation in English; reports follow the selected prompt or user language.
- Use Asset prompts directly. Ordinary report execution and prompt export leave the library unchanged.
- Make focused, evidence-backed prompt changes; preserve independently usable files.
- Run `python scripts/check.py` after changes and verify packaging for release changes.
- Local/static checks prove package integrity, not market-research accuracy.
- Keep private inputs and evaluation runs in ignored local directories.
- Avoid adding model clients, schedulers, databases, or generated prompt mirrors.
