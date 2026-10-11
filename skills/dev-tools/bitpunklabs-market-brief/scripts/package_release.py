"""Build and verify an installable Market Brief ZIP without runtime dependencies."""

import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

from check import ROOT, check, package_files


def build(output, tag=None):
    result = check()
    if tag is not None and tag != "v" + result["version"]:
        raise ValueError("Release tag does not match SKILL.md version")
    output = Path(output).resolve()
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError("Choose a new or empty output directory")
    output.mkdir(parents=True, exist_ok=True)

    archive = output / f'market-brief-{result["version"]}.zip'
    sources = {path.relative_to(ROOT).as_posix(): path.read_bytes() for path in package_files()}
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, content in sorted(sources.items()):
            entry = zipfile.ZipInfo("market-brief/" + name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            bundle.writestr(entry, content)

    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None:
            raise ValueError("ZIP integrity check failed")
        if set(bundle.namelist()) != {"market-brief/" + name for name in sources}:
            raise ValueError("ZIP file boundary check failed")
        for name, content in sources.items():
            if bundle.read("market-brief/" + name) != content:
                raise ValueError("ZIP source mismatch: " + name)

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / "SHA256SUMS").write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=False
    )
    status = subprocess.run(
        ["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, check=False
    )
    receipt = dict(
        result, archive=archive.name, sha256=digest,
        commit=commit.stdout.strip() if commit.returncode == 0 else None,
        dirty=bool(status.stdout.strip()) if status.returncode == 0 else None,
        files={name: hashlib.sha256(content).hexdigest() for name, content in sources.items()},
    )
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="A new or empty directory")
    parser.add_argument("--tag", help="Validate the GitHub release tag against the skill version")
    args = parser.parse_args()
    try:
        receipt = build(args.output, args.tag)
        print(json.dumps({key: value for key, value in receipt.items() if key != "files"}))
    except (ValueError, OSError) as exc:
        parser.exit(1, str(exc) + "\n")
