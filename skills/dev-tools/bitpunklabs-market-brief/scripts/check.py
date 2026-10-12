"""Check the prompt package offline using only the Python standard library."""

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = (
    "SKILL.md", "README.md", "LICENSE", "CHANGELOG.md",
    "CONTRIBUTING.md", "SECURITY.md", "AGENTS.md",
)
LINK = re.compile(r"\[[^\]\n]+\]\(([^)\n]+)\)")


def package_files(root=ROOT):
    """Use an explicit boundary; local runs and GitHub configuration stay out."""
    paths = [root / name for name in DOCUMENTS]
    paths += [root / "agents/openai.yaml"]
    paths += sorted((root / "assets/prompts").glob("*.md"))
    paths += [root / "scripts/check.py", root / "scripts/package_release.py"]
    demo = root / "media/market-brief-demo.gif"
    if demo.exists():
        paths.append(demo)
    return sorted(paths)


def version(root=ROOT):
    text = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r'^  version: "(\d+\.\d+\.\d+)"$', text, re.MULTILINE)
    if not match:
        raise ValueError("SKILL.md needs metadata.version as a quoted semantic version")
    return match.group(1)


def check(root=ROOT):
    errors = []
    files = package_files(root)
    for path in files:
        if not path.is_file() or path.is_symlink():
            errors.append(f"Missing file or unsupported symlink: {path.relative_to(root)}")
    if errors:
        raise ValueError("\n".join(errors))

    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
    if not match:
        errors.append("SKILL.md needs YAML frontmatter")
    else:
        fields = dict(re.findall(r"^([a-z-]+): (.+)$", match.group(1), re.MULTILINE))
        if fields.get("name") != "market-brief":
            errors.append("Skill name must be market-brief")
        if not 1 <= len(fields.get("description", "")) <= 1024:
            errors.append("Skill description must be 1–1024 characters")
        if fields.get("license") != "MIT":
            errors.append("Skill license must match the repository license")

    current_version = version(root)
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"\n## {current_version}\n" not in changelog:
        errors.append("Changelog must contain the current skill version")

    prompts = sorted((root / "assets/prompts").glob("*.md"))
    if len(prompts) != 11:
        errors.append(f"Expected the 11 supported prompts, found {len(prompts)}")
    routes = [target for target in LINK.findall(skill) if target.startswith("assets/prompts/")]
    expected = {path.relative_to(root).as_posix() for path in prompts}
    if len(routes) != len(expected) or set(routes) != expected:
        errors.append("Skill routing must reference every prompt exactly once")
    readme = (root / "README.md").read_text(encoding="utf-8")
    if not expected.issubset(set(LINK.findall(readme))):
        errors.append("README must link every supported prompt")

    for path in files:
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            errors.append(f"Empty Markdown file: {path.relative_to(root)}")
        for target in LINK.findall(text):
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme or not parsed.path:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(root.resolve()) or not destination.exists():
                errors.append(f"Broken local link in {path.relative_to(root)}: {target}")

    ui = (root / "agents/openai.yaml").read_text(encoding="utf-8")
    description = re.search(r'^  short_description: "(.+)"$', ui, re.MULTILINE)
    if not description or not 25 <= len(description.group(1)) <= 64:
        errors.append("UI short_description must be 25–64 characters")
    if "$market-brief" not in ui:
        errors.append("UI default prompt must invoke $market-brief")

    for source in re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', readme):
        if not urlsplit(source).scheme and not (root / source).is_file():
            errors.append(f"Missing README image: {source}")

    if errors:
        raise ValueError("\n".join(errors))
    return {"version": current_version, "prompts": len(prompts), "package_files": len(files)}


if __name__ == "__main__":
    import json
    import sys

    try:
        print(json.dumps(check()))
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
