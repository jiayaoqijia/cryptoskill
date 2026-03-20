#!/usr/bin/env python3
"""Regenerate docs/skills.json from the skills/ directory tree.

Walks skills/{category}/{skill-name}/ directories, reads SKILL.md
front-matter and _meta.json, then writes a fresh docs/skills.json.

Usage:
    python scripts/update-catalog.py            # rebuild catalog
    python scripts/update-catalog.py --dry-run   # preview without writing
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
DOCS_DIR = REPO_ROOT / "docs"
SKILLS_JSON = DOCS_DIR / "skills.json"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("update-catalog")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def parse_skill_md_frontmatter(path: Path) -> dict:
    """Return the YAML front-matter from a SKILL.md as a dict.

    Uses a minimal parser so we don't need a PyYAML dependency.
    """
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}

    fm: dict = {}
    current_list_key: str | None = None
    current_multiline_key: str | None = None
    multiline_lines: list = []

    for line in m.group(1).splitlines():
        # If we're collecting multiline text (YAML | or >)
        if current_multiline_key:
            if re.match(r"^[a-zA-Z\w-]+:", line):
                # New key starts — save collected multiline
                fm[current_multiline_key] = " ".join(multiline_lines).strip()
                current_multiline_key = None
                multiline_lines = []
                # Fall through to parse this line as a key
            elif line.strip():
                multiline_lines.append(line.strip())
                continue
            else:
                continue

        # List item (e.g.  "  - some-tag")
        list_match = re.match(r"^\s+-\s+(.+)", line)
        if list_match and current_list_key:
            fm.setdefault(current_list_key, []).append(
                list_match.group(1).strip().strip('"').strip("'")
            )
            continue

        # Key-value pair
        kv = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if kv:
            key = kv.group(1)
            val = kv.group(2).strip().strip('"').strip("'")
            if val == "|" or val == ">":
                # YAML multiline block scalar
                current_multiline_key = key
                multiline_lines = []
                current_list_key = None
            elif val:
                fm[key] = val
                current_list_key = None
            else:
                # Next lines will be list items for this key
                current_list_key = key
            continue

        current_list_key = None

    # Flush any remaining multiline
    if current_multiline_key and multiline_lines:
        fm[current_multiline_key] = " ".join(multiline_lines).strip()

    return fm


def read_json_safe(path: Path) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        log.warning("Could not read %s: %s", path, exc)
        return {}


def make_display_name(slug: str) -> str:
    """Convert 'binance-spot-api' -> 'Binance Spot Api'."""
    return " ".join(w.capitalize() for w in slug.split("-"))


def classify_source(source_md_path: Path) -> str:
    """Return 'official' or 'community' based on SOURCE.md contents."""
    if not source_md_path.exists():
        return "community"
    text = source_md_path.read_text(encoding="utf-8").lower()
    if "official" in text:
        return "official"
    return "community"


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------


def build_catalog() -> dict:
    """Walk skills/*/* and build the catalog dict."""
    skills_list: list[dict] = []

    for cat_dir in sorted(SKILLS_DIR.iterdir()):
        if not cat_dir.is_dir():
            continue
        category = cat_dir.name

        for skill_dir in sorted(cat_dir.iterdir()):
            if not skill_dir.is_dir():
                continue

            slug = skill_dir.name
            skill_md = skill_dir / "SKILL.md"
            meta_json = skill_dir / "_meta.json"
            source_md = skill_dir / "SOURCE.md"

            # Parse available metadata sources
            fm = parse_skill_md_frontmatter(skill_md) if skill_md.exists() else {}
            meta = read_json_safe(meta_json) if meta_json.exists() else {}

            # Determine author
            author = meta.get("owner", fm.get("author", "unknown"))

            # Determine version
            version = meta.get("latest", {}).get("version", fm.get("version", "1.0.0"))

            # Determine display name
            display_name = meta.get("displayName", make_display_name(slug))

            # Determine description
            description = fm.get("description", display_name)

            # Tags
            tags = fm.get("tags", [])
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",")]
            if not tags:
                tags = [category]

            # Classification
            classification = classify_source(source_md)

            entry: dict = {
                "name": slug,
                "displayName": display_name,
                "description": description,
                "category": category,
                "tags": tags,
                "author": author,
                "version": version,
            }

            skills_list.append(entry)

    # Preserve existing categories and merge with existing skill data
    catalog = {"skills": skills_list, "categories": {}}
    if SKILLS_JSON.exists():
        try:
            existing = read_json_safe(SKILLS_JSON)
            # Keep curated categories
            catalog["categories"] = existing.get("categories", {})
            # Merge author/tags from existing entries where our parse found "unknown"
            existing_by_name = {s["name"]: s for s in existing.get("skills", [])}
            for entry in catalog["skills"]:
                old = existing_by_name.get(entry["name"])
                if old:
                    if entry["author"] == "unknown" and old.get("author", "unknown") != "unknown":
                        entry["author"] = old["author"]
                    if entry["tags"] == [entry["category"]] and old.get("tags"):
                        entry["tags"] = old["tags"]
                    if entry["description"] == entry["displayName"] and old.get("description"):
                        entry["description"] = old["description"]
                    if entry["displayName"] == make_display_name(entry["name"]) and old.get("displayName"):
                        entry["displayName"] = old["displayName"]
        except Exception:
            pass

    return catalog


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regenerate docs/skills.json from the skills/ directory."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print summary without writing skills.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=SKILLS_JSON,
        help=f"Output path (default: {SKILLS_JSON})",
    )
    args = parser.parse_args()

    catalog = build_catalog()
    total = len(catalog["skills"])

    # Category breakdown
    cat_counts: dict[str, int] = {}
    for s in catalog["skills"]:
        cat_counts[s["category"]] = cat_counts.get(s["category"], 0) + 1

    log.info("Catalog summary: %d skills in %d categories", total, len(cat_counts))
    for cat, count in sorted(cat_counts.items()):
        log.info("  %-22s %d", cat, count)

    if args.dry_run:
        log.info("[DRY-RUN] Would write %d skills to %s", total, args.output)
        return

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    log.info("Wrote %s (%d skills)", args.output, total)


if __name__ == "__main__":
    main()
