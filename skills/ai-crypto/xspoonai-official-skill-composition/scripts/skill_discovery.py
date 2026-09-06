#!/usr/bin/env python3
"""
Skill Discovery Engine

Parses SKILL.md metadata files across the repository, builds a searchable
skill catalog, and semantically matches user intent to relevant skills.

Architecture:
    Three-layer matching: Keyword Filter → Tag Scoring → LLM Semantic Match
    Inspired by search engine ranking — fast filters first, expensive LLM last.

SpoonOS Integration:
    - MCP Tool Discovery: Scan available skills from marketplace
    - Skill Marketplace: Query skill registry for composable capabilities
    - StateGraph: Discovery node in the composition pipeline
"""

import asyncio
import json
import math
import os
import re
import sys
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

from _llm_client import extract_json, llm_chat, load_env

load_env()


# ---------------------------------------------------------------------------
# Domain Types
# ---------------------------------------------------------------------------


class MatchTier(str, Enum):
    """Matching confidence tiers."""
    EXACT = "exact"
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"


@dataclass(frozen=True)
class SkillParameter:
    """Immutable parameter definition from SKILL.md frontmatter."""
    name: str
    param_type: str
    required: bool
    default: Optional[str] = None
    description: str = ""


@dataclass(frozen=True)
class SkillMetadata:
    """Immutable skill metadata parsed from SKILL.md frontmatter."""
    name: str
    description: str
    version: str
    author: str
    tags: tuple[str, ...]
    parameters: tuple[SkillParameter, ...]
    keywords: tuple[str, ...]
    composable: bool
    file_path: str
    scripts: tuple[str, ...] = ()


@dataclass(frozen=True)
class SkillMatch:
    """Immutable result of matching a skill to user intent."""
    skill: SkillMetadata
    score: float
    tier: MatchTier
    matched_keywords: tuple[str, ...]
    matched_tags: tuple[str, ...]
    semantic_reasoning: str = ""


# ---------------------------------------------------------------------------
# YAML Frontmatter Parser (stdlib only — no PyYAML dependency)
# ---------------------------------------------------------------------------

def _parse_yaml_value(value: str) -> str | int | float | bool | list[str]:
    """Parse a single YAML value into a Python type."""
    value = value.strip()
    if value.lower() in ("true", "yes"):
        return True
    if value.lower() in ("false", "no"):
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        items = value[1:-1].split(",")
        return [item.strip().strip("'\"") for item in items if item.strip()]
    return value


def parse_yaml_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from SKILL.md content.

    Handles nested structures (parameters, triggers, scripts) with
    indentation-based parsing. Supports both list ('- ' prefix) and
    mapping ('key: value') sub-structures.
    """
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}

    yaml_text = parts[1].strip()
    result: dict = {}
    current_key: Optional[str] = None
    current_list: Optional[list] = None
    current_dict: Optional[dict] = None
    # Track whether the top-level value is a mapping (dict) vs list
    current_is_mapping: bool = False
    # Track the top-level mapping dict separately from list-item dicts
    top_mapping: Optional[dict] = None

    for line in yaml_text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())

        # Top-level key: value
        if indent == 0 and ":" in stripped:
            current_list = None
            current_dict = None
            current_is_mapping = False
            top_mapping = None
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip()
            if val:
                result[key] = _parse_yaml_value(val)
            else:
                # Defer type decision — will be resolved on first nested line
                result[key] = None
                current_key = key
            continue

        # We have a nested line under current_key — decide list vs mapping
        if current_key and result.get(current_key) is None:
            if stripped.startswith("- "):
                result[current_key] = []
                current_list = result[current_key]
                current_is_mapping = False
            else:
                result[current_key] = {}
                top_mapping = result[current_key]
                current_dict = top_mapping
                current_is_mapping = True

        # Nested key: value inside a list-item dict (highest priority)
        if (
            ":" in stripped
            and not stripped.startswith("- ")
            and current_dict is not None
            and current_dict is not top_mapping
            and isinstance(current_dict, dict)
        ):
            k, _, v = stripped.partition(":")
            k = k.strip()
            v = v.strip()
            current_dict[k] = _parse_yaml_value(v) if v else []
            continue

        # Mapping value under a top-level mapping key
        if (
            current_is_mapping
            and current_key
            and ":" in stripped
            and not stripped.startswith("- ")
            and top_mapping is not None
        ):
            k, _, v = stripped.partition(":")
            k = k.strip()
            v = v.strip()
            top_mapping[k] = _parse_yaml_value(v) if v else []
            # If value is a list placeholder, prepare for list items
            if not v:
                current_list = top_mapping[k] if isinstance(top_mapping[k], list) else None
            continue

        # List item
        if stripped.startswith("- "):
            item_content = stripped[2:].strip()
            if ":" in item_content and not item_content.startswith('"'):
                k, _, v = item_content.partition(":")
                new_dict = {k.strip(): _parse_yaml_value(v.strip()) if v.strip() else ""}
                if current_list is not None:
                    current_list.append(new_dict)
                    current_dict = new_dict
            else:
                if current_list is not None:
                    current_list.append(_parse_yaml_value(item_content))
                    current_dict = None
            continue

        # Sub-structure of top-level list item (fallback)
        if ":" in stripped and indent > 0 and current_key:
            k, _, v = stripped.partition(":")
            k = k.strip()
            v = v.strip()
            if isinstance(result.get(current_key), list) and result[current_key]:
                last = result[current_key][-1]
                if isinstance(last, dict):
                    last[k] = _parse_yaml_value(v) if v else []

    return result


# ---------------------------------------------------------------------------
# Skill Catalog Builder
# ---------------------------------------------------------------------------

def extract_keywords_from_triggers(triggers: list[dict]) -> tuple[str, ...]:
    """Extract all keywords from trigger definitions."""
    keywords: list[str] = []
    for trigger in triggers:
        if isinstance(trigger, dict):
            kws = trigger.get("keywords", [])
            if isinstance(kws, list):
                keywords.extend(str(k) for k in kws)
    return tuple(keywords)


def extract_script_names(scripts_data: dict | list) -> tuple[str, ...]:
    """Extract script names from scripts definition.

    Handles both dict format (scripts.definitions) and flat list format.
    """
    if isinstance(scripts_data, dict):
        defs = scripts_data.get("definitions", [])
        if isinstance(defs, list):
            return tuple(
                d.get("name", "") for d in defs
                if isinstance(d, dict) and d.get("name")
            )
    # Fallback: flat list of dicts with 'name' key
    if isinstance(scripts_data, list):
        return tuple(
            d.get("name", "") for d in scripts_data
            if isinstance(d, dict) and d.get("name")
        )
    return ()


def parse_skill_file(file_path: Path) -> Optional[SkillMetadata]:
    """Parse a single SKILL.md file into SkillMetadata."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    meta = parse_yaml_frontmatter(content)
    if not meta.get("name"):
        return None

    params_raw = meta.get("parameters", [])
    parameters: list[SkillParameter] = []
    if isinstance(params_raw, list):
        for p in params_raw:
            if isinstance(p, dict):
                parameters.append(SkillParameter(
                    name=str(p.get("name", "")),
                    param_type=str(p.get("type", "string")),
                    required=bool(p.get("required", False)),
                    default=str(p.get("default", "")) if p.get("default") is not None else None,
                    description=str(p.get("description", "")),
                ))

    triggers = meta.get("triggers", [])
    keywords = extract_keywords_from_triggers(
        triggers if isinstance(triggers, list) else []
    )

    tags_raw = meta.get("tags", [])
    tags = tuple(str(t) for t in tags_raw) if isinstance(tags_raw, list) else ()

    scripts_raw = meta.get("scripts", {})
    scripts = extract_script_names(scripts_raw) if isinstance(scripts_raw, (dict, list)) else ()

    return SkillMetadata(
        name=str(meta.get("name", "")),
        description=str(meta.get("description", "")),
        version=str(meta.get("version", "0.0.0")),
        author=str(meta.get("author", "unknown")),
        tags=tags,
        parameters=tuple(parameters),
        keywords=keywords,
        composable=bool(meta.get("composable", False)),
        file_path=str(file_path),
        scripts=scripts,
    )


def scan_skill_registry(root_path: str) -> list[SkillMetadata]:
    """Recursively scan directory for SKILL.md files and build catalog."""
    root = Path(root_path).resolve()
    skills: list[SkillMetadata] = []
    for skill_file in root.rglob("SKILL.md"):
        skill = parse_skill_file(skill_file)
        if skill is not None:
            skills.append(skill)
    return skills


# ---------------------------------------------------------------------------
# Layer 1: Keyword Matching (Fast Filter)
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> set[str]:
    """Tokenize text into lowercase word set."""
    return set(re.findall(r"[a-z0-9\u4e00-\u9fff]+", text.lower()))


def keyword_match_score(query: str, skill: SkillMetadata) -> tuple[float, list[str]]:
    """Score skill by keyword overlap with query.

    Returns (score, matched_keywords) where score is 0.0-1.0.
    """
    query_tokens = _tokenize(query)
    if not query_tokens:
        return 0.0, []

    # Build skill token pool from all text fields
    skill_text = " ".join([
        skill.name,
        skill.description,
        " ".join(skill.tags),
        " ".join(skill.keywords),
    ])
    skill_tokens = _tokenize(skill_text)

    matched = query_tokens & skill_tokens
    if not matched:
        return 0.0, []

    # Jaccard-inspired score with query coverage emphasis
    query_coverage = len(matched) / len(query_tokens)
    skill_coverage = len(matched) / max(len(skill_tokens), 1)
    score = 0.7 * query_coverage + 0.3 * skill_coverage

    return min(1.0, score), sorted(matched)


# ---------------------------------------------------------------------------
# Layer 2: Tag & Metadata Scoring
# ---------------------------------------------------------------------------

def tag_match_score(query: str, skill: SkillMetadata) -> tuple[float, list[str]]:
    """Score skill by tag relevance to query.

    Tags are curated metadata — higher signal than raw text matching.
    """
    query_tokens = _tokenize(query)
    if not query_tokens or not skill.tags:
        return 0.0, []

    matched_tags: list[str] = []
    for tag in skill.tags:
        tag_tokens = _tokenize(tag)
        if tag_tokens & query_tokens:
            matched_tags.append(tag)

    if not matched_tags:
        return 0.0, []

    score = len(matched_tags) / len(skill.tags)
    return min(1.0, score), matched_tags


# ---------------------------------------------------------------------------
# Layer 3: LLM Semantic Matching (via shared _llm_client)
# ---------------------------------------------------------------------------


async def llm_semantic_match(
    query: str,
    candidates: list[SkillMetadata],
    provider: str = "openai",
) -> list[dict]:
    """Use LLM to semantically match query to candidate skills.

    This is the expensive but most accurate matching layer.
    Only called for candidates that passed keyword/tag filters.

    Delegates to SpoonOS LLMManager when available, falls back to HTTP.
    """
    if not candidates:
        return []

    fallback = [
        {"skill_name": c.name, "relevance": 0.5, "reasoning": "LLM unavailable"}
        for c in candidates
    ]

    skill_summaries = "\n".join(
        f"- **{c.name}**: {c.description[:200]} (tags: {', '.join(c.tags[:5])})"
        for c in candidates
    )

    system_prompt = (
        "You are a skill routing expert. Given a user query and a list of available skills, "
        "rate each skill's relevance to the query on a scale of 0.0 to 1.0. "
        "Also explain briefly why each skill is or isn't relevant. "
        "Consider semantic meaning, not just keyword overlap."
    )

    user_prompt = f"""User Query: "{query}"

Available Skills:
{skill_summaries}

Rate each skill's relevance. Respond in this exact JSON format:
```json
[
  {{"skill_name": "name", "relevance": 0.0-1.0, "reasoning": "why relevant/not", "sub_task": "what sub-task this skill handles"}}
]
```"""

    response = await llm_chat(
        messages=[{"role": "user", "content": user_prompt}],
        provider=provider,
        system=system_prompt,
        temperature=0.1,
        max_tokens=1024,
    )

    if not response:
        return fallback

    parsed = extract_json(response)
    if isinstance(parsed, list):
        return parsed

    return fallback


# ---------------------------------------------------------------------------
# Composite Scoring & Ranking
# ---------------------------------------------------------------------------

def classify_tier(score: float) -> MatchTier:
    """Classify match score into confidence tier."""
    if score >= 0.8:
        return MatchTier.EXACT
    if score >= 0.6:
        return MatchTier.STRONG
    if score >= 0.35:
        return MatchTier.MODERATE
    return MatchTier.WEAK


async def discover_skills(
    query: str,
    registry_path: str,
    max_results: int = 5,
    provider: str = "openai",
    use_llm: bool = True,
) -> list[SkillMatch]:
    """Main discovery pipeline: scan → filter → score → rank.

    Three-layer matching:
        1. Keyword matching (fast, broad filter)
        2. Tag scoring (structured metadata)
        3. LLM semantic matching (deep understanding, expensive)
    """
    # Step 1: Scan registry
    all_skills = scan_skill_registry(registry_path)
    if not all_skills:
        return []

    # Step 2: Layer 1 + Layer 2 scoring
    scored: list[tuple[SkillMetadata, float, list[str], list[str]]] = []
    for skill in all_skills:
        kw_score, kw_matched = keyword_match_score(query, skill)
        tag_score, tag_matched = tag_match_score(query, skill)

        # Weighted combination: keywords 40%, tags 60% (tags are higher signal)
        combined = 0.4 * kw_score + 0.6 * tag_score

        # Bonus for composable skills
        if skill.composable:
            combined = min(1.0, combined + 0.05)

        if combined > 0.05:  # Minimum threshold to proceed
            scored.append((skill, combined, kw_matched, tag_matched))

    # Sort by score descending
    scored.sort(key=lambda x: x[1], reverse=True)

    # Take top candidates for LLM matching
    candidates = scored[:max(max_results * 2, 10)]

    # Step 3: Layer 3 — LLM semantic matching (optional)
    llm_scores: dict[str, dict] = {}
    if use_llm and candidates:
        candidate_skills = [c[0] for c in candidates]
        llm_results = await llm_semantic_match(query, candidate_skills, provider)
        for result in llm_results:
            if isinstance(result, dict):
                llm_scores[result.get("skill_name", "")] = result

    # Combine all scores
    final_matches: list[SkillMatch] = []
    for skill, base_score, kw_matched, tag_matched in candidates:
        llm_data = llm_scores.get(skill.name, {})
        llm_relevance = float(llm_data.get("relevance", 0.5))
        reasoning = str(llm_data.get("reasoning", ""))

        # Final score: base 40% + LLM 60% (LLM is most accurate)
        if use_llm and llm_scores:
            final_score = 0.4 * base_score + 0.6 * llm_relevance
        else:
            final_score = base_score

        tier = classify_tier(final_score)

        final_matches.append(SkillMatch(
            skill=skill,
            score=round(final_score, 3),
            tier=tier,
            matched_keywords=tuple(kw_matched),
            matched_tags=tuple(tag_matched),
            semantic_reasoning=reasoning,
        ))

    # Sort by final score, take top N
    final_matches.sort(key=lambda m: m.score, reverse=True)
    return final_matches[:max_results]


# ---------------------------------------------------------------------------
# Output Serialization
# ---------------------------------------------------------------------------

def match_to_dict(match: SkillMatch) -> dict:
    """Serialize a SkillMatch to JSON-compatible dict."""
    return {
        "skill_name": match.skill.name,
        "score": match.score,
        "tier": match.tier.value,
        "matched_keywords": list(match.matched_keywords),
        "matched_tags": list(match.matched_tags),
        "semantic_reasoning": match.semantic_reasoning,
        "metadata": {
            "description": match.skill.description,
            "version": match.skill.version,
            "author": match.skill.author,
            "tags": list(match.skill.tags),
            "composable": match.skill.composable,
            "file_path": match.skill.file_path,
            "scripts": list(match.skill.scripts),
            "parameters": [
                {
                    "name": p.name,
                    "type": p.param_type,
                    "required": p.required,
                    "default": p.default,
                    "description": p.description,
                }
                for p in match.skill.parameters
            ],
        },
    }


async def run_skill_discovery(input_data: dict) -> dict:
    """Main entry point: discover and rank skills for a user query.

    StateGraph node mapping:
        graph.add_node("discover", run_skill_discovery)
        graph.add_edge("entry", "discover")
        graph.add_edge("discover", "compose")
    """
    query = input_data.get("query", "")
    if not query:
        return {"error": "Missing required parameter: query"}

    registry_path = input_data.get("skill_registry_path", ".")
    max_results = min(10, max(1, input_data.get("max_skills", 5)))
    provider = input_data.get("provider", "openai")
    use_llm = input_data.get("use_llm", True)

    start_ms = int(time.time() * 1000)

    # Scan and discover
    all_skills = scan_skill_registry(registry_path)
    matches = await discover_skills(
        query=query,
        registry_path=registry_path,
        max_results=max_results,
        provider=provider,
        use_llm=use_llm,
    )

    elapsed_ms = int(time.time() * 1000) - start_ms

    return {
        "success": True,
        "query": query,
        "registry_path": str(Path(registry_path).resolve()),
        "total_skills_scanned": len(all_skills),
        "matches_found": len(matches),
        "elapsed_ms": elapsed_ms,
        "provider": provider,
        "use_llm": use_llm,
        "matches": [match_to_dict(m) for m in matches],
    }


# ---------------------------------------------------------------------------
# Main Entry Point (stdin/stdout JSON protocol)
# ---------------------------------------------------------------------------

def main() -> None:
    """Read JSON from stdin, run skill discovery, output JSON to stdout."""
    try:
        input_data = json.loads(sys.stdin.read())
        result = asyncio.run(run_skill_discovery(input_data))
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Skill discovery failed: {e}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
