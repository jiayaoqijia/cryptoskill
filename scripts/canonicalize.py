#!/usr/bin/env python3
"""
Canonical serialization for trust-manifest digests (TRUST.md §"Canonical
serialization"): YAML parse -> JSON tree -> RFC 8785 JCS bytes -> sha256.

Per the spec, YAML inputs MUST NOT use any non-JSON YAML feature (anchors,
aliases, merge keys, custom tags, duplicate keys, multi-document, non-string
keys, non-finite numbers, YAML-typed timestamps). The bot rejects (does
not silently re-canonicalize) inputs that violate the constraints, so
the digest is reproducible across signers.

Implementation note: ruamel's safe loader silently resolves anchors and
aliases to the same Python object before any tree walk can detect them.
We therefore intercept at the **token stream** level (before composition)
to flag every banned token, AND walk the tree afterward for the
schema-level checks (non-string keys, non-finite numbers, etc.).

Usage:
  python3 scripts/canonicalize.py <path>            # print canonical JCS bytes
  python3 scripts/canonicalize.py --digest <path>   # print sha256:HEX
"""

import argparse
import hashlib
import json
import sys
import unicodedata
from io import StringIO
from pathlib import Path

import rfc8785
from ruamel.yaml import YAML
from ruamel.yaml.constructor import DuplicateKeyError
from ruamel.yaml.scanner import Scanner
from ruamel.yaml import tokens as yaml_tokens
from ruamel.yaml.parser import Parser
from ruamel.yaml.events import (
    AliasEvent,
    MappingStartEvent,
    SequenceStartEvent,
    ScalarEvent,
)


def _detect_multidoc(text: str) -> None:
    """Reject multi-document streams. A leading '---' is allowed once.
    A real multidoc has '---' at the start of a line *after* content, so we
    look for a second occurrence."""
    sep_count = sum(1 for ln in text.splitlines() if ln.rstrip() == "---")
    if sep_count > 1:
        raise ValueError("multi-document YAML stream is not allowed")


def _scan_for_banned_features(text: str) -> None:
    """Run the ruamel SCANNER and PARSER over the text and reject tokens/
    events that have no canonical JSON projection: anchors, aliases, custom
    tags. (Merge keys appear as `<<` scalars and are caught by the schema
    walk below; they are also flagged here so the error message points to
    YAML-feature use.)"""
    yaml = YAML(typ="safe", pure=True)
    yaml.allow_duplicate_keys = False
    parser = yaml.parser
    # Use a fresh loader-internal pipeline to consume parse events.
    yaml.loader = yaml.Reader
    # ruamel exposes parse_events via load_all(); a simpler hand-rolled
    # check uses the constructor on the composed graph, but to catch
    # anchors/aliases we walk the parser events directly.
    yaml_local = YAML(typ="safe", pure=True)
    yaml_local.allow_duplicate_keys = False
    try:
        events = list(yaml_local.parse(text))
    except Exception as exc:
        raise ValueError(f"YAML parse failed: {exc}") from exc

    for ev in events:
        if isinstance(ev, AliasEvent):
            raise ValueError(f"YAML aliases (`*name`) are not allowed (at {ev.start_mark})")
        # Detect anchors: every event has an .anchor attribute that is None when absent.
        anchor = getattr(ev, "anchor", None)
        if anchor:
            raise ValueError(f"YAML anchors (`&name`) are not allowed (at {ev.start_mark})")
        tag = getattr(ev, "tag", None)
        # Allow only the implicit YAML core schema tags. The safe loader emits
        # tag strings like "tag:yaml.org,2002:str"; anything else (custom !tags,
        # YAML 1.1 type tags) we refuse at the parser-event layer before
        # composition can resolve them.
        if tag is not None and tag != "":
            if not isinstance(tag, str) or not tag.startswith("tag:yaml.org,2002:"):
                raise ValueError(f"non-core YAML tag not allowed: {tag!r}")
            local = tag.removeprefix("tag:yaml.org,2002:")
            allowed_local = {"str", "int", "float", "bool", "null", "seq", "map"}
            if local not in allowed_local:
                raise ValueError(f"YAML core tag {tag!r} is outside the JSON-projectable subset")
        # Merge keys appear as ScalarEvents with value '<<'; reject them.
        if isinstance(ev, ScalarEvent) and ev.value == "<<":
            raise ValueError("YAML merge keys (`<<`) are not allowed")


def _check_no_yaml_only_features(node, path="$"):
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
        raise ValueError(f"non-JSON value type at {path}: {type(node).__name__}")


def parse_canonical_yaml(text: str):
    """Parse YAML under the safe loader with all banned-feature checks."""
    _detect_multidoc(text)
    _scan_for_banned_features(text)
    yaml = YAML(typ="safe", pure=True)
    yaml.allow_duplicate_keys = False
    try:
        node = yaml.load(text)
    except DuplicateKeyError as exc:
        raise ValueError(f"duplicate keys are not allowed: {exc}") from exc
    _check_no_yaml_only_features(node)
    return node


def _no_dup_object_pairs(pairs):
    seen = {}
    for k, v in pairs:
        if k in seen:
            raise ValueError(f"duplicate JSON object key: {k!r}")
        seen[k] = v
    return seen


def _parse_canonical_json(text: str):
    """Parse JSON rejecting duplicate keys (default last-wins is unsafe for
    canonicalization)."""
    try:
        node = json.loads(text, object_pairs_hook=_no_dup_object_pairs)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON parse failed: {exc}") from exc
    _check_no_yaml_only_features(node)
    return node


def to_canonical_json_bytes(text: str) -> bytes:
    """Return RFC 8785 JCS bytes for YAML or JSON input. NFC-normalize all
    string values so visually identical inputs hash identically.

    NFC-collision check: two source keys can be byte-distinct (e.g.
    'é' as U+00E9 vs 'e' + U+0301) but NFC-collapse to the same string.
    A naive comprehension `{nfc(k): nfc(v) ...}` would silently last-wins
    and produce a digest that depends on dict iteration order. We
    therefore reject NFC-colliding keys explicitly.
    """
    if text.lstrip().startswith("{") or text.lstrip().startswith("["):
        node = _parse_canonical_json(text)
    else:
        node = parse_canonical_yaml(text)

    def _nfc(value, path="$"):
        if isinstance(value, str):
            return unicodedata.normalize("NFC", value)
        if isinstance(value, dict):
            normalized = {}
            for k, v in value.items():
                if not isinstance(k, str):
                    raise ValueError(f"non-string key at {path}")
                nk = unicodedata.normalize("NFC", k)
                if nk in normalized:
                    raise ValueError(
                        f"NFC-colliding map keys at {path}: distinct source "
                        f"strings collapse to {nk!r} after Unicode normalization"
                    )
                normalized[nk] = _nfc(v, f"{path}.{nk}")
            return normalized
        if isinstance(value, list):
            return [_nfc(v, f"{path}[{i}]") for i, v in enumerate(value)]
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
