"""
GenTech Agent Kit — Output Enforcer Plugin
===========================================
Validates tool outputs against pydantic schemas. On schema mismatch:
1. Logs the violation with tool name, schema, and actual output
2. Auto-retries once (for transient/API-dependent tools)
3. Returns a structured error if validation fails again

Hardened for production:
- Disk-backed violation storage (survives VPS reboot / process crash)
- Auto-recovery on startup
- Graceful degradation (disk full / corruption handled)
- Circuit breaker pattern (tools that keep failing get backoff)

Usage:
    from .schemas import QuoteResponse
    from .decorator import validated_output

    @mcp.tool()
    @validated_output(QuoteResponse)
    def get_quote(symbol: str) -> str:
        ...

Plugin auto-discovered by the Agent Kit plugin loader.
"""

from __future__ import annotations

import functools
import json
import logging
import os
import time
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

from . import schemas

_LOG = logging.getLogger("gentech-kit.plugins.output-enforcer")

# ── Persistence ──────────────────────────────────────────────────────────────
# Violations survive VPS reboots and process crashes via a JSON file.

_VOLATIONS_DIR = os.environ.get(
    "OUTPUT_ENFORCER_DATA_DIR",
    os.path.expanduser("~/.agent-kit/data/output-enforcer"),
)
_VIOLATIONS_FILE = os.path.join(_VOLATIONS_DIR, "violations.json")
_CIRCUIT_BREAKER_FILE = os.path.join(_VOLATIONS_DIR, "circuit-breaker.json")

# In-memory cache (loaded from disk on init, written on each mutation)
_violations: dict[str, list[dict[str, Any]]] = {}
_breaker_state: dict[str, dict[str, Any]] = {}

# ── Disk I/O ─────────────────────────────────────────────────────────────────


def _ensure_dir() -> None:
    """Create the data directory if it doesn't exist. Silently handles races."""
    try:
        os.makedirs(_VOLATIONS_DIR, mode=0o755, exist_ok=True)
    except OSError as exc:
        _LOG.warning("Output enforcer: cannot create data dir %s: %s", _VOLATIONS_DIR, exc)


def _load_violations() -> dict[str, list[dict[str, Any]]]:
    """Load violations from disk. Returns empty dict on any failure (doesn't crash)."""
    if not os.path.isfile(_VIOLATIONS_FILE):
        return {}
    try:
        with open(_VIOLATIONS_FILE, "r") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            _LOG.warning("Output enforcer: violations file corrupt (not a dict), resetting")
            return {}
        return data
    except (json.JSONDecodeError, OSError) as exc:
        _LOG.warning("Output enforcer: cannot load violations: %s, starting fresh", exc)
        return {}


def _save_violations() -> bool:
    """Write violations to disk. Returns True on success, False on failure."""
    _ensure_dir()
    try:
        # Atomic write: write to temp, then rename
        tmp = _VIOLATIONS_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(_violations, f, indent=2)
        os.replace(tmp, _VIOLATIONS_FILE)
        return True
    except (OSError, TypeError) as exc:
        _LOG.error("Output enforcer: cannot save violations: %s", exc)
        return False


def _load_breakers() -> dict[str, dict[str, Any]]:
    """Load circuit breaker state from disk."""
    if not os.path.isfile(_CIRCUIT_BREAKER_FILE):
        return {}
    try:
        with open(_CIRCUIT_BREAKER_FILE, "r") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _save_breakers() -> bool:
    """Write circuit breaker state to disk."""
    _ensure_dir()
    try:
        tmp = _CIRCUIT_BREAKER_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(_breaker_state, f, indent=2)
        os.replace(tmp, _CIRCUIT_BREAKER_FILE)
        return True
    except OSError as exc:
        _LOG.error("Output enforcer: cannot save breaker state: %s", exc)
        return False


# ── Init: load persisted state (survives VPS reboot) ─────────────────────────

_violations = _load_violations()
_breaker_state = _load_breakers()
_total_violations_loaded = sum(len(v) for v in _violations.values())
if _total_violations_loaded > 0:
    _LOG.info(
        "Output enforcer: loaded %d violation(s) from disk (%d tool(s))",
        _total_violations_loaded, len(_violations),
    )


# ── Violation API ────────────────────────────────────────────────────────────


def get_violations(tool_name: str | None = None, since: float = 0) -> list[dict[str, Any]]:
    """Get output validation violations. Optionally filter by tool and/or time window."""
    results = []
    for name, entries in _violations.items():
        if tool_name and name != tool_name:
            continue
        for entry in entries:
            if entry.get("timestamp", 0) >= since:
                results.append({"tool": name, **entry})
    return sorted(results, key=lambda x: x.get("timestamp", 0), reverse=True)


def clear_violations() -> int:
    """Clear all violation records (memory + disk). Returns count cleared."""
    global _violations
    count = sum(len(v) for v in _violations.values())
    _violations = {}
    _save_violations()
    return count


def _record_violation(tool_name: str, violation: dict[str, Any]) -> None:
    """Record a violation in memory and persist to disk."""
    _violations.setdefault(tool_name, []).append(violation)
    # Trim oldest entries if we have too many (cap at 1000 per tool)
    if len(_violations[tool_name]) > 1000:
        _violations[tool_name] = _violations[tool_name][-1000:]
    _save_violations()


# ── Circuit Breaker ──────────────────────────────────────────────────────────
# If a tool fails validation repeatedly, back off instead of burning retries.


def _breaker_check(tool_name: str) -> tuple[bool, str]:
    """Check if a tool is circuit-broken.
    
    Returns: (is_broken: bool, reason: str)
    """
    entry = _breaker_state.get(tool_name)
    if not entry:
        return False, ""
    
    failures = entry.get("consecutive_failures", 0)
    cooldown_until = entry.get("cooldown_until", 0)
    now = time.time()
    
    if failures >= 5 and now < cooldown_until:
        remaining = int(cooldown_until - now)
        return True, f"Circuit breaker active ({remaining}s remaining, {failures} consecutive failures)"
    
    # Cooldown expired — reset
    if failures >= 5 and now >= cooldown_until:
        _breaker_state.pop(tool_name, None)
        _save_breakers()
    
    return False, ""


def _breaker_record_failure(tool_name: str) -> None:
    """Record a validation failure and potentially trip the breaker."""
    entry = _breaker_state.setdefault(tool_name, {
        "consecutive_failures": 0,
        "cooldown_until": 0,
        "last_failure": 0,
    })
    entry["consecutive_failures"] = entry.get("consecutive_failures", 0) + 1
    entry["last_failure"] = time.time()
    
    # Trip after 5 consecutive failures: 60s cooldown, doubling each time
    cf = entry["consecutive_failures"]
    if cf >= 5:
        cooldown = min(60 * (2 ** (min(cf, 10) - 5)), 3600)  # 60s → 120s → ... → 1h max
        entry["cooldown_until"] = time.time() + cooldown
        _LOG.warning(
            "Output enforcer: circuit breaker tripped for %s after %d failures (cooldown: %ds)",
            tool_name, cf, cooldown,
        )
    
    _save_breakers()


def _breaker_record_success(tool_name: str) -> None:
    """Record a validation success — resets consecutive failures."""
    if tool_name in _breaker_state:
        _breaker_state[tool_name]["consecutive_failures"] = 0
        _breaker_state[tool_name]["cooldown_until"] = 0
        _save_breakers()


# ── Validated Output Decorator ────────────────────────────────────────────────

F = TypeVar("F", bound=callable)


def validated_output(schema_class: type[BaseModel], max_retries: int = 1) -> callable:
    """Decorator that validates a tool's JSON string output against a pydantic schema.
    
    Hardened features:
    - Disk-backed violation storage (survives reboot)
    - Circuit breaker (5 consecutive failures → 60s-1h cooldown)
    - Graceful degradation (storage failures don't crash the tool)
    - Auto-retry on transient validation failures
    
    Args:
        schema_class: A pydantic BaseModel subclass defining the expected output shape.
        max_retries: Number of retries on validation failure (default 1).
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> str:
            tool_name = func.__name__
            last_error: Exception | None = None

            # Check circuit breaker
            is_broken, reason = _breaker_check(tool_name)
            if is_broken:
                _LOG.warning("Output enforcer: %s blocked by circuit breaker", tool_name)
                return json.dumps({
                    "error": "Tool temporarily unavailable",
                    "tool": tool_name,
                    "detail": reason,
                })

            for attempt in range(max_retries + 1):
                try:
                    raw_output = func(*args, **kwargs)

                    # Parse the JSON string output
                    try:
                        parsed = json.loads(raw_output) if isinstance(raw_output, str) else raw_output
                    except json.JSONDecodeError:
                        # Non-JSON tool — skip validation, pass through
                        return raw_output

                    # Validate against schema
                    validated = schema_class(**parsed)
                    
                    # Success — reset breaker, return
                    _breaker_record_success(tool_name)
                    _LOG.debug("Output enforcer: %s passed schema %s (attempt %d)", 
                               tool_name, schema_class.__name__, attempt + 1)
                    return validated.model_dump_json(indent=2)

                except ValidationError as exc:
                    last_error = exc
                    violation = {
                        "timestamp": time.time(),
                        "schema": schema_class.__name__,
                        "attempt": attempt + 1,
                        "error": str(exc),
                        "args": str(args),
                        "kwargs": str(kwargs),
                    }
                    _record_violation(tool_name, violation)
                    _breaker_record_failure(tool_name)
                    
                    _LOG.warning(
                        "Output enforcer: %s failed schema %s (attempt %d/%d): %s",
                        tool_name, schema_class.__name__, attempt + 1, max_retries + 1, exc
                    )
                    
                    if attempt < max_retries:
                        _LOG.info("Output enforcer: retrying %s (attempt %d)", tool_name, attempt + 2)
                    else:
                        _LOG.error(
                            "Output enforcer: %s failed after %d attempts. Schema: %s",
                            tool_name, max_retries + 1, schema_class.__name__
                        )

                except Exception as exc:
                    # Non-validation error — tool execution failed
                    _LOG.error("Output enforcer: %s crashed: %s", tool_name, exc)
                    return json.dumps({"error": f"Tool execution failed: {exc}"})

            # All retries exhausted
            return json.dumps({
                "error": f"Output validation failed after {max_retries + 1} attempt(s)",
                "schema": schema_class.__name__,
                "tool": tool_name,
                "detail": str(last_error) if last_error else "Unknown",
            })

        return wrapper  # type: ignore
    return decorator


# ── Plugin Registration ──────────────────────────────────────────────────────


__plugin_manifest__ = {
    "name": "Output Enforcer",
    "version": "0.2.0",
    "description": "Validates tool outputs against pydantic schemas with auto-retry, disk-backed violations, and circuit breaker",
    "type": "middleware",
}


def register_gentech_plugin(mcp: Any) -> None:
    """Register Output Enforcer tools with the Agent Kit MCP server."""
    
    @mcp.tool()
    def output_enforcer_status() -> str:
        """Get Output Enforcer status — violations, circuit breakers, storage health."""
        total = sum(len(v) for v in _violations.values())
        tools_with_violations = list(_violations.keys())
        broken_tools = {
            k: v for k, v in _breaker_state.items()
            if v.get("consecutive_failures", 0) >= 5 and time.time() < v.get("cooldown_until", 0)
        }
        
        # Verify disk storage is operational
        disk_ok = _save_violations() if _violations else True
        
        return json.dumps({
            "plugin": "Output Enforcer",
            "version": "0.2.0",
            "status": "active",
            "storage": "disk-backed" if disk_ok else "memory-only (disk write failed)",
            "violations_path": _VIOLATIONS_FILE,
            "total_violations": total,
            "tools_with_violations": tools_with_violations,
            "broken_tools": len(broken_tools),
            "broken_tools_detail": list(broken_tools.keys()),
            "registered_schemas": list(schemas.__all__) if hasattr(schemas, "__all__") else [],
            "data_dir": _VOLATIONS_DIR,
        }, indent=2)

    @mcp.tool()
    def output_enforcer_violations(tool_name: str = "", hours: int = 24) -> str:
        """Get recent validation violations. Filter by tool name (optional) and time window.
        
        Args:
            tool_name: Optional tool name to filter by. Empty string returns all.
            hours: How many hours back to look (default 24).
        """
        since = time.time() - (hours * 3600)
        violations = get_violations(tool_name if tool_name else None, since)
        return json.dumps({
            "count": len(violations),
            "window_hours": hours,
            "storage": _VIOLATIONS_FILE,
            "violations": violations[:100],  # cap at 100
        }, indent=2)

    @mcp.tool()
    def output_enforcer_clear() -> str:
        """Clear all violation records (memory + disk). Returns count cleared."""
        count = clear_violations()
        return json.dumps({"cleared": count, "status": "ok", "persisted": True})

    @mcp.tool()
    def output_enforcer_breakers() -> str:
        """Get circuit breaker status for all tools."""
        now = time.time()
        active = {}
        for tool_name, state in _breaker_state.items():
            cf = state.get("consecutive_failures", 0)
            cooldown = state.get("cooldown_until", 0)
            active[tool_name] = {
                "consecutive_failures": cf,
                "broken": cf >= 5 and now < cooldown,
                "cooldown_remaining_s": max(0, int(cooldown - now)) if cf >= 5 else 0,
                "last_failure": state.get("last_failure", 0),
            }
        return json.dumps({
            "count": len(active),
            "tools": active,
        }, indent=2)

    _LOG.info("Registered Output Enforcer plugin v0.2.0 (disk-backed)")
