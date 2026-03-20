from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .contracts import AdapterType, BaseAdapter
from .registry import AdapterRegistry


@dataclass(frozen=True)
class AdapterAttempt:
    adapter_name: str
    success: bool
    error: str | None = None


@dataclass(frozen=True)
class AdapterCallOutcome:
    adapter_name: str
    payload: Any
    attempts: list[AdapterAttempt]


class AdapterCallError(RuntimeError):
    def __init__(self, message: str, attempts: list[AdapterAttempt]) -> None:
        super().__init__(message)
        self.attempts = attempts


def _candidate_names(
    registry: AdapterRegistry,
    adapter_type: AdapterType,
    preferred_name: str,
    fallback_names: list[str] | None = None,
) -> list[str]:
    names: list[str] = []
    if preferred_name:
        names.append(preferred_name)
    for name in fallback_names or []:
        if name not in names:
            names.append(name)
    for name in registry.list_names(adapter_type):
        if name not in names:
            names.append(name)
    return names


def call_with_healing(
    registry: AdapterRegistry,
    adapter_type: AdapterType,
    preferred_name: str,
    call_fn: Callable[[BaseAdapter], Any],
    fallback_names: list[str] | None = None,
    retries_per_adapter: int = 1,
) -> AdapterCallOutcome:
    attempts: list[AdapterAttempt] = []
    candidates = _candidate_names(registry, adapter_type, preferred_name, fallback_names)
    if not candidates:
        raise AdapterCallError("no_adapters_registered", attempts)

    last_error = "unknown_error"
    for adapter_name in candidates:
        try:
            adapter = registry.get(adapter_type, adapter_name)
        except Exception as exc:
            attempts.append(
                AdapterAttempt(
                    adapter_name=adapter_name,
                    success=False,
                    error=f"{type(exc).__name__}: {exc}",
                )
            )
            continue
        max_tries = max(1, retries_per_adapter)
        for _ in range(max_tries):
            try:
                payload = call_fn(adapter)
                attempts.append(AdapterAttempt(adapter_name=adapter_name, success=True))
                return AdapterCallOutcome(
                    adapter_name=adapter_name,
                    payload=payload,
                    attempts=attempts,
                )
            except Exception as exc:  # defensive boundary around third-party adapters
                last_error = f"{type(exc).__name__}: {exc}"
                attempts.append(
                    AdapterAttempt(
                        adapter_name=adapter_name,
                        success=False,
                        error=last_error,
                    )
                )

    raise AdapterCallError(f"all_adapter_attempts_failed: {last_error}", attempts)
