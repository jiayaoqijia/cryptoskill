from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from datetime import date, datetime
from typing import Any, Dict, List


@dataclass
class ModuleResult:
    module: str
    target_date: str
    status: str
    data: Dict[str, Any]
    data_gaps: List[str]
    source_warnings: List[str]
    sources: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def build_result(
    module: str,
    target: date,
    data: Dict[str, Any],
    gaps: List[str],
    warnings: List[str],
    sources: Dict[str, str],
) -> ModuleResult:
    if gaps:
        status = "degraded"
    elif warnings:
        status = "partial"
    else:
        status = "complete"
    return ModuleResult(module, target.isoformat(), status, data, gaps, warnings, sources)


def fetch_recoverable(fetcher: Any, gaps: List[str], warnings: List[str], *args: Any, **kwargs: Any) -> Any:
    issues: List[str] = []
    value = fetcher(*args, issues, **kwargs)
    (warnings if value else gaps).extend(issues)
    return value


def json_default(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, set):
        return sorted(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")
