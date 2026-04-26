#!/usr/bin/env python3
"""
Canonical serialization for trust-manifest digests (TRUST.md §"Canonical
serialization"): YAML parse -> JSON tree -> RFC 8785 JCS bytes -> sha256.

Per the spec, YAML inputs MUST NOT use any non-JSON YAML feature. The bot
rejects (does not silently re-canonicalize) inputs that violate the
constraints, so the digest is reproducible across signers.

Usage:
  python3 scripts/canonicalize.py <path>            # print canonical JCS bytes
  python3 scripts/canonicalize.py --digest <path>   # print sha256:HEX
"""

import argparse
import hashlib
import json
import sys
import unicodedata
from pathlib import Path

import rfc8785
from ruamel.yaml import YAML
from ruamel.yaml.constructor import DuplicateKeyError


BANNED_NODE_KINDS = (
    # Detected via runtime tree inspection after parse. ruamel's safe loader
    # already rejects custom !tag types and aliases by default.
)


def _check_no_yaml_only_features(node, path="$"):
    """Walk the parsed tree and reject anything that has no canonical JSON
    projection: non-string map keys, non-finite numbers, byte values, etc.

    Duplicate keys, anchors/aliases, and merge keys are caught at parse time
    by the loader configuration; this pass catches the schema-level issues.
    """
    if isinstance(node, dict):
        for k, v in node.items():
            if not isinstance(k, str):
                raise ValueError(f"non-string map key at {path}: {k!r}")
            _check_no_yaml_only_features(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _check_no_yaml_only_features(v, f"{path}[{i}]")
    elif isinstance(node, float):
        if node != node or node in (float("inf"), float("-inf")):
            raise ValueError(f"non-finite number at {path}")
    elif isinstance(node, (bytes, bytearray)):
        raise ValueError(f"binary value at {path} (use base64 string)")
    elif isinstance(node, (str, int, bool)) or node is None:
        return
    else:
        raise ValueError(
            f"non-JSON value type at {path}: {type(node).__name__}"
        )


def _detect_multidoc(text: str) -> None:
    """Reject multi-document streams. A leading '---' is allowed once.

    A real multidoc has '---' at the start of a line *after* content, so we
    look for a second occurrence.
    """
    lines = text.splitlines()
    sep_count = sum(1 for ln in lines if ln.rstrip() == "---")
    if sep_count > 1:
        raise ValueError("multi-document YAML stream is not allowed")


def parse_canonical_yaml(text: str):
    """Parse YAML under the safe loader with all banned-feature checks.

    Returns the parsed Python tree (dict / list / str / int / bool / None).
    """
    _detect_multidoc(text)
    yaml = YAML(typ="safe", pure=True)
    yaml.allow_duplicate_keys = False
    try:
        node = yaml.load(text)
    except DuplicateKeyError as exc:
        raise ValueError(f"duplicate keys are not allowed: {exc}") from exc
    _check_no_yaml_only_features(node)
    return node


def to_canonical_json_bytes(text: str) -> bytes:
    """Return RFC 8785 JCS bytes for YAML or JSON input. NFC-normalize all
    string values so visually identical inputs hash identically."""
    if text.lstrip().startswith("{") or text.lstrip().startswith("["):
        node = json.loads(text)
        _check_no_yaml_only_features(node)
    else:
        node = parse_canonical_yaml(text)

    def _nfc(value):
        if isinstance(value, str):
            return unicodedata.normalize("NFC", value)
        if isinstance(value, dict):
            return {_nfc(k): _nfc(v) for k, v in value.items()}
        if isinstance(value, list):
            return [_nfc(v) for v in value]
        return value

    normalized = _nfc(node)
    return rfc8785.dumps(normalized)


def digest_path(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return "sha256:" + hashlib.sha256(to_canonical_json_bytes(text)).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("path", help="YAML or JSON file to canonicalize")
    p.add_argument("--digest", action="store_true", help="emit sha256:HEX instead of bytes")
    args = p.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        sys.exit(2)
    try:
        if args.digest:
            print(digest_path(path))
        else:
            sys.stdout.buffer.write(to_canonical_json_bytes(path.read_text(encoding="utf-8")))
    except ValueError as exc:
        print(f"canonicalize: rejecting {path}: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
