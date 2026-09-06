#!/usr/bin/env python3
"""Shared parser, validator, and renderer for finding adjudication reports."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Final

NAMESPACE: Final = "finding_adjudication"
REPORT_NAME: Final = "full-report.md"
BRIEF_NAME: Final = "brief.md"
INPUT_NAME: Final = "input.md"
MAX_CORE_WORDS: Final = 1_000

_MARKER_RE = re.compile(
    rf"^<!-- {NAMESPACE}:(?P<kind>begin|end)"
    r'(?P<attrs>(?:\s+[a-z][a-z0-9_-]*="[^"]*")*)\s*-->$'
)
_ATTRIBUTE_RE = re.compile(r'([a-z][a-z0-9_-]*)="([^"]*)"')
_RESULT_RE = re.compile(r"<!-- adjudication-result: (?P<json>\{.*\}) -->")
_WEIGHTS_RE = re.compile(r"<!-- rubric-weights: (?P<json>\{.*\}) -->")
_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_WORD_RE = re.compile(r"\b[\w'-]+\b", re.UNICODE)

DISPOSITIONS: Final = {"Confirmed", "Downgraded", "Question", "Closed"}
SEVERITIES: Final = {"Blocker", "Major", "Minor", "Question", "Nit", "None"}


@dataclass(frozen=True)
class SectionSpec:
    slug: str
    disclosure: str
    heading: str


SECTION_SPECS: Final[tuple[SectionSpec, ...]] = (
    SectionSpec("candidate-hypothesis", "core", "# Candidate hypothesis"),
    SectionSpec(
        "requirement-interpretations",
        "reference",
        "# Requirement interpretations",
    ),
    SectionSpec("investigation", "reference", "# Investigation"),
    SectionSpec(
        "evidence-for-and-against",
        "reference",
        "# Evidence for and against",
    ),
    SectionSpec("evidence-synthesis", "core", "# Evidence synthesis"),
    SectionSpec("disposition", "core", "# Disposition"),
    SectionSpec(
        "feasible-response-variants",
        "reference",
        "# Feasible response variants",
    ),
    SectionSpec("decision-rubric", "reference", "# Decision rubric"),
    SectionSpec("variant-evaluation", "reference", "# Variant evaluation"),
    SectionSpec(
        "sensitivity-analysis",
        "reference",
        "# Sensitivity analysis",
    ),
    SectionSpec("decision-boundary", "core", "# Decision boundary"),
    SectionSpec("recommendation", "core", "# Recommendation"),
    SectionSpec(
        "residual-uncertainty",
        "core",
        "# Residual uncertainty",
    ),
    SectionSpec("overlap", "core", "# Overlap with other candidates"),
)

_SPEC_BY_SLUG: Final = {spec.slug: spec for spec in SECTION_SPECS}


class ReportValidationError(ValueError):
    """Raised when a report violates the adjudication artifact contract."""

    def __init__(self, errors: list[str] | tuple[str, ...]):
        self.errors = tuple(errors)
        super().__init__("\n".join(f"- {error}" for error in self.errors))


@dataclass(frozen=True)
class ReportSection:
    slug: str
    disclosure: str
    content: str
    begin_line: int
    end_line: int


@dataclass(frozen=True)
class AdjudicationReport:
    path: Path
    raw_bytes: bytes
    sections: tuple[ReportSection, ...]
    result: dict[str, object]
    rubric_weights: dict[str, float]

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.raw_bytes).hexdigest()

    def section(self, slug: str) -> ReportSection:
        for section in self.sections:
            if section.slug == slug:
                return section
        raise KeyError(slug)


def _parse_attributes(raw: str, line_number: int) -> tuple[dict[str, str], list[str]]:
    attributes: dict[str, str] = {}
    errors: list[str] = []
    cursor = 0
    for match in _ATTRIBUTE_RE.finditer(raw):
        gap = raw[cursor : match.start()]
        if gap.strip():
            errors.append(f"line {line_number}: malformed tag attributes near {gap.strip()!r}")
        cursor = match.end()
        key, value = match.groups()
        if key in attributes:
            errors.append(f"line {line_number}: duplicate attribute {key!r}")
        attributes[key] = value
    if raw[cursor:].strip():
        errors.append(f"line {line_number}: malformed tag attributes near {raw[cursor:].strip()!r}")
    return attributes, errors


def _first_nonblank_line(content: str) -> str | None:
    for line in content.splitlines():
        if line.strip():
            return line.strip()
    return None


def _load_json_comment(
    *,
    content: str,
    regex: re.Pattern[str],
    label: str,
    slug: str,
    errors: list[str],
) -> dict[str, object] | None:
    matches = list(regex.finditer(content))
    if len(matches) != 1:
        errors.append(f"section {slug!r}: expected exactly one {label} JSON comment, found {len(matches)}")
        return None
    try:
        value = json.loads(matches[0].group("json"))
    except json.JSONDecodeError as exc:
        errors.append(f"section {slug!r}: invalid {label} JSON: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"section {slug!r}: {label} JSON must be an object")
        return None
    return value


def _validate_result(value: dict[str, object] | None, errors: list[str]) -> None:
    if value is None:
        return
    expected_keys = {"disposition", "confidence", "severity"}
    if set(value) != expected_keys:
        errors.append("adjudication-result: keys must be exactly 'disposition', 'confidence', and 'severity'")
    disposition = value.get("disposition")
    if disposition not in DISPOSITIONS:
        errors.append(f"adjudication-result: disposition must be one of {sorted(DISPOSITIONS)}, got {disposition!r}")
    severity = value.get("severity")
    if severity not in SEVERITIES:
        errors.append(f"adjudication-result: severity must be one of {sorted(SEVERITIES)}, got {severity!r}")
    confidence = value.get("confidence")
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        errors.append("adjudication-result: confidence must be a number from 0 through 1")
    if disposition == "Closed" and severity != "None":
        errors.append("adjudication-result: Closed disposition requires severity None")
    if disposition == "Question" and severity != "Question":
        errors.append("adjudication-result: Question disposition requires severity Question")


def _validate_weights(value: dict[str, object] | None, errors: list[str]) -> dict[str, float]:
    if value is None:
        return {}
    if not 2 <= len(value) <= 8:
        errors.append("rubric-weights: expected between 2 and 8 criteria")
    normalized: dict[str, float] = {}
    for key, weight in value.items():
        if not isinstance(key, str) or not _SLUG_RE.fullmatch(key):
            errors.append(f"rubric-weights: criterion key must be a kebab-case slug, got {key!r}")
            continue
        if isinstance(weight, bool) or not isinstance(weight, (int, float)) or weight <= 0:
            errors.append(f"rubric-weights: weight for {key!r} must be a positive number")
            continue
        normalized[key] = float(weight)
    if normalized and abs(sum(normalized.values()) - 100) > 1e-9:
        errors.append(f"rubric-weights: weights must total 100, got {sum(normalized.values()):g}")
    return normalized


def parse_and_validate_report(path: Path | str) -> AdjudicationReport:
    """Parse and validate one full adjudication report."""

    report_path = Path(path).resolve()
    errors: list[str] = []
    if report_path.name != REPORT_NAME:
        errors.append(f"report filename must be {REPORT_NAME!r}")
    if not report_path.is_file():
        raise ReportValidationError([f"report does not exist: {report_path}"])
    if report_path.is_symlink():
        errors.append("report must not be a symbolic link")

    raw_bytes = report_path.read_bytes()
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ReportValidationError([f"report is not valid UTF-8: {exc}"]) from exc

    sections: list[ReportSection] = []
    current_slug: str | None = None
    current_disclosure: str | None = None
    current_begin_line = 0
    current_lines: list[str] = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        marker = _MARKER_RE.fullmatch(line.strip())
        if marker is None:
            if NAMESPACE in line:
                errors.append(f"line {line_number}: malformed {NAMESPACE} marker")
            if current_slug is None:
                if line.strip():
                    errors.append(f"line {line_number}: nonblank content outside tagged sections")
            else:
                current_lines.append(line)
            continue

        attributes, attribute_errors = _parse_attributes(marker.group("attrs"), line_number)
        errors.extend(attribute_errors)
        kind = marker.group("kind")

        if kind == "begin":
            if set(attributes) != {"disclosure", "slug"}:
                errors.append(f"line {line_number}: begin marker attributes must be exactly 'disclosure' and 'slug'")
            if current_slug is not None:
                errors.append(f"line {line_number}: nested section inside {current_slug!r}")
                continue
            current_slug = attributes.get("slug", "")
            current_disclosure = attributes.get("disclosure", "")
            current_begin_line = line_number
            current_lines = []
            continue

        if set(attributes) != {"slug"}:
            errors.append(f"line {line_number}: end marker attribute must be exactly 'slug'")
        if current_slug is None:
            errors.append(f"line {line_number}: end marker without an open section")
            continue
        end_slug = attributes.get("slug", "")
        if end_slug != current_slug:
            errors.append(f"line {line_number}: end slug {end_slug!r} does not match open slug {current_slug!r}")
        sections.append(
            ReportSection(
                slug=current_slug,
                disclosure=current_disclosure or "",
                content="\n".join(current_lines).strip() + "\n",
                begin_line=current_begin_line,
                end_line=line_number,
            )
        )
        current_slug = None
        current_disclosure = None
        current_lines = []

    if current_slug is not None:
        errors.append(f"section {current_slug!r} opened on line {current_begin_line} is not closed")

    actual_slugs = [section.slug for section in sections]
    expected_slugs = [spec.slug for spec in SECTION_SPECS]
    if actual_slugs != expected_slugs:
        errors.append(f"section slugs/order mismatch: expected {expected_slugs!r}, got {actual_slugs!r}")
    if len(set(actual_slugs)) != len(actual_slugs):
        errors.append("section slugs must be unique")

    for section in sections:
        spec = _SPEC_BY_SLUG.get(section.slug)
        if spec is None:
            continue
        if section.disclosure != spec.disclosure:
            errors.append(
                f"section {section.slug!r}: disclosure must be {spec.disclosure!r}, got {section.disclosure!r}"
            )
        first_line = _first_nonblank_line(section.content)
        if first_line != spec.heading:
            errors.append(f"section {section.slug!r}: first nonblank line must be {spec.heading!r}, got {first_line!r}")
        if "REPLACE_ME" in section.content:
            errors.append(f"section {section.slug!r}: unresolved REPLACE_ME placeholder")

    section_map = {section.slug: section for section in sections}
    disposition_section = section_map.get("disposition")
    result_value = (
        _load_json_comment(
            content=disposition_section.content,
            regex=_RESULT_RE,
            label="adjudication-result",
            slug="disposition",
            errors=errors,
        )
        if disposition_section
        else None
    )
    _validate_result(result_value, errors)

    rubric_section = section_map.get("decision-rubric")
    weights_value = (
        _load_json_comment(
            content=rubric_section.content,
            regex=_WEIGHTS_RE,
            label="rubric-weights",
            slug="decision-rubric",
            errors=errors,
        )
        if rubric_section
        else None
    )
    normalized_weights = _validate_weights(weights_value, errors)

    core_word_count = sum(
        len(_WORD_RE.findall(section.content)) for section in sections if section.disclosure == "core"
    )
    if core_word_count > MAX_CORE_WORDS:
        errors.append(f"core sections contain {core_word_count} words; maximum is {MAX_CORE_WORDS}")

    if errors:
        raise ReportValidationError(errors)

    return AdjudicationReport(
        path=report_path,
        raw_bytes=raw_bytes,
        sections=tuple(sections),
        result=result_value or {},
        rubric_weights=normalized_weights,
    )


def render_brief(report: AdjudicationReport) -> str:
    """Render a deterministic brief from core sections in report order."""

    source_link = f"./{report.path.name}"
    blocks = [
        "<!-- generated by implementation-plan-review; do not edit -->",
        f"<!-- source-sha256: {report.sha256} -->",
        f"Source: [{report.path.name}]({source_link})",
    ]
    blocks.extend(section.content.rstrip() for section in report.sections if section.disclosure == "core")
    return "\n\n".join(blocks) + "\n"


def write_text_atomically(path: Path | str, content: str) -> None:
    """Write UTF-8 text atomically in the destination directory."""

    destination = Path(path).resolve()
    destination.parent.mkdir(parents=False, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.tmp-{os.getpid()}")
    try:
        temporary.write_text(content, encoding="utf-8")
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()


def expected_candidate_files() -> set[str]:
    """Return the exact allowed file set for a completed candidate directory."""

    return {INPUT_NAME, REPORT_NAME, BRIEF_NAME}
