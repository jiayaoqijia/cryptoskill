#!/usr/bin/env python3
"""Verify a release manifest and copy into an explicitly selected, new skill directory."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path, PurePosixPath


REQUIRED_MEMBERS = ("SKILL.md", "scripts/research.py", "references/models.md", "VERSION", "LICENSE")
FORBIDDEN_FLAGS = ("--dangerously-bypass-approvals-and-sandbox",)


def verify(root: Path) -> list[str]:
    manifest = root / "SHA256SUMS"
    names = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        checksum, name = line.split("  ", 1)
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts or name in names:
            raise ValueError("Unsafe or duplicate manifest path")
        actual = root / name
        if actual.is_symlink() or not actual.is_file() or root.resolve() not in actual.resolve().parents:
            raise ValueError("Manifest member is not a regular internal file")
        if hashlib.sha256(actual.read_bytes()).hexdigest() != checksum:
            raise ValueError(f"Checksum mismatch: {name}")
        names.append(name)
    models = root / "references/models.md"
    if models.is_file() and any(flag in models.read_text(encoding="utf-8") for flag in FORBIDDEN_FLAGS):
        raise ValueError("references/models.md must not contain an approval/sandbox bypass flag")
    if not names or any(required not in names for required in REQUIRED_MEMBERS):
        raise ValueError("Incomplete package manifest")
    return names


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--target", help="Explicit native skill directory; discover it from host instructions first")
    args = parser.parse_args()
    source = Path(args.source).resolve()
    names = verify(source)
    if not args.target:
        print(json.dumps({"status": "verified", "files": len(names), "source": str(source)}))
        return
    target = Path(args.target).expanduser().resolve()
    if target == source or source in target.parents:
        raise ValueError("Target must be separate from release source")
    if target.exists() and any(target.iterdir()):
        existing = verify(target)
        if existing == names and (target / "SHA256SUMS").read_bytes() == (source / "SHA256SUMS").read_bytes():
            print(json.dumps({"status": "already_installed", "target": str(target)}))
            return
        raise ValueError("Target contains a different skill; preserve it and choose a new target")
    target.mkdir(parents=True, exist_ok=True)
    for name in names + ["SHA256SUMS"]:
        destination = target / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as handle:
            handle.write((source / name).read_bytes())
    verify(target)
    print(json.dumps({"status": "installed_files", "target": str(target), "files": len(names),
                      "next": "Register SKILL.md with the host native skill update mechanism; copying files alone does not prove discovery."}))


if __name__ == "__main__":
    main()
