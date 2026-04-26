#!/usr/bin/env python3
"""
Emit the corpus-level attestation predicate body (TRUST.md §"Corpus-level
attestation"): a signed-once-per-bot-run record binding the full
discovered/processed/skipped set with per-skill manifest digests.

This prevents omission attacks where a malicious or buggy bot silently
drops a high-risk skill from the registry; verifiers compare the corpus
attestation's `manifest_digests` map to the per-skill attestations they
trust and detect missing entries.

Output: an in-toto Statement v0.1 to stdout. Sign with cosign:
  cosign attest --predicate <(this script) --type \\
    https://cryptoskill.org/attestations/skill-corpus/v1 ...
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import rfc8785

from canonicalize import to_canonical_json_bytes

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
CAPABILITIES_JSON = ROOT / "docs" / "capabilities.json"

PREDICATE_TYPE = "https://cryptoskill.org/attestations/skill-corpus/v1"


def manifest_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(
        to_canonical_json_bytes(path.read_text(encoding="utf-8"))
    ).hexdigest()


def gather_manifests():
    discovered, processed = [], {}
    skipped = []
    for cat in sorted(SKILLS_DIR.iterdir()):
        if not cat.is_dir():
            continue
        for skill in sorted(cat.iterdir()):
            if not skill.is_dir():
                continue
            rel = str(skill.relative_to(SKILLS_DIR))
            discovered.append(rel)
            auto = skill / "TRUST.auto.yaml"
            if auto.exists():
                processed[rel] = manifest_digest(auto)
            else:
                reason = "missing_skill_md" if not (skill / "SKILL.md").exists() else "missing_trust_auto"
                skipped.append({"skill": rel, "reason": reason})
    return discovered, processed, skipped


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default=None, help="write to file instead of stdout")
    args = p.parse_args()

    if not CAPABILITIES_JSON.exists():
        print("capabilities.json not found; run extract-capabilities.py first", file=sys.stderr)
        sys.exit(1)
    summary = json.loads(CAPABILITIES_JSON.read_text(encoding="utf-8"))

    discovered, processed, skipped = gather_manifests()
    predicate = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "extractor_version": summary.get("extractor_version"),
        "taxonomy_version": summary.get("taxonomy_version"),
        "hostlist_version": summary.get("hostlist_version"),
        "discovered": len(discovered),
        "processed": len(processed),
        "skipped": skipped,
        "manifest_digests": processed,
    }
    if predicate["discovered"] != predicate["processed"] + len(predicate["skipped"]):
        print(
            f"corpus accounting drift: discovered={predicate['discovered']} "
            f"processed={predicate['processed']} skipped={len(predicate['skipped'])}",
            file=sys.stderr,
        )
        sys.exit(2)

    # subject.digest must be reproducible: canonicalize the predicate dict
    # directly via RFC 8785 JCS (no intermediate json.dumps round-trip,
    # which would re-parse and re-emit through canonicalize.py only to
    # produce the same bytes — but with extra brittleness if a future
    # field type changes serialization).
    canonical_predicate_bytes = rfc8785.dumps(predicate)
    subject_digest = hashlib.sha256(canonical_predicate_bytes).hexdigest()

    statement = {
        "_type": "https://in-toto.io/Statement/v0.1",
        "subject": [
            {
                "name": "cryptoskill-corpus",
                "digest": {"sha256": subject_digest},
            }
        ],
        "predicateType": PREDICATE_TYPE,
        "predicate": predicate,
    }
    out = json.dumps(statement, indent=2)
    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
    else:
        print(out)


if __name__ == "__main__":
    main()
