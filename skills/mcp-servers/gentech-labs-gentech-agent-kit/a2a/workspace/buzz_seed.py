#!/usr/bin/env python3
"""a2a-workspace — seed a Hermes profile as a native managed agent in Buzz.

Pre-seeds Buzz Desktop's managed-agents.json with the target Hermes profile
and pins it to a self-hosted relay, so a headless or fresh Desktop install
picks it up on first launch without the GUI first-run flow.

Stdlib only. Fail-closed. Idempotent.

Usage:
    python3 buzz_seed.py                       # seed agent + relay env
    python3 buzz_seed.py --dry-run             # print what would be written
    python3 buzz_seed.py --relay wss://buzz.example.com:3003
    python3 buzz_seed.py --profile work --name "Work Agent"

Configuration (env vars):
    A2A_BUZZ_PROFILE   Hermes profile to register (default: gentech)
    A2A_BUZZ_RELAY     Default relay URL (default: wss://buzz.gentechlabs.net:3003)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

BUZZ_TAURI_IDENTIFIER = "xyz.block.buzz.app"
MANAGED_AGENTS_FILE = "managed-agents.json"
DEFAULT_PROFILE = os.environ.get("A2A_BUZZ_PROFILE", "gentech")
DEFAULT_RELAY = os.environ.get("A2A_BUZZ_RELAY", "wss://buzz.gentechlabs.net:3003")


def platform_name() -> str:
    return {"darwin": "macOS", "linux": "Linux", "win32": "Windows"}.get(
        sys.platform, sys.platform
    )


def buzz_data_dir() -> Path:
    home = Path.home()
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA")
        if not base:
            raise RuntimeError("LOCALAPPDATA is not set")
        return Path(base) / BUZZ_TAURI_IDENTIFIER
    if sys.platform == "darwin":
        return home / "Library" / "Application Support" / BUZZ_TAURI_IDENTIFIER
    xdg = os.environ.get("XDG_DATA_HOME")
    if xdg:
        return Path(xdg) / BUZZ_TAURI_IDENTIFIER
    return home / ".local" / "share" / BUZZ_TAURI_IDENTIFIER


def resolve_hermes() -> str:
    candidate = "/usr/local/lib/hermes-agent/venv/bin/hermes"
    if Path(candidate).is_file():
        return candidate
    from shutil import which

    w = which("hermes")
    if w:
        return w
    raise RuntimeError("hermes executable not found on PATH or at default venv path")


def profile_home(profile: str) -> Path:
    home = Path.home()
    cand = home / ".hermes" / "profiles" / profile
    if cand.is_dir():
        return cand
    raise RuntimeError(f"Hermes profile '{profile}' not found at {cand}")


def read_soul_prompt(profile_home: Path) -> str | None:
    soul = profile_home / "SOUL.md"
    if not soul.is_file():
        return None
    try:
        text = soul.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError):
        return None
    if len(text) > 4000:
        text = text[:3997] + "..."
    return text or None


def build_entry(profile: str, hermes_path: str, relay_url: str, system_prompt: str, name: str) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    slug = f"hermes:{profile}"
    return {
        "pubkey": "",
        "name": name,
        "persona_id": None,
        "auth_tag": None,
        "relay_url": relay_url,
        "acp_command": "buzz-acp",
        "agent_command": hermes_path,
        "agent_command_override": None,
        "agent_args": ["-p", profile, "acp"],
        "mcp_command": "",
        "turn_timeout_seconds": 320,
        "idle_timeout_seconds": None,
        "max_turn_duration_seconds": None,
        "parallelism": 10,
        "system_prompt": system_prompt,
        "model": None,
        "provider": None,
        "persona_source_version": None,
        "start_on_app_launch": False,
        "auto_restart_on_config_change": True,
        "runtime_pid": None,
        "backend": {"type": "local"},
        "backend_agent_id": None,
        "provider_binary_path": None,
        "created_at": now,
        "updated_at": now,
        "last_started_at": None,
        "last_stopped_at": None,
        "last_exit_code": None,
        "last_error": None,
        "last_error_code": None,
        "respond_to": "owner-only",
        "respond_to_allowlist": [],
        "slug": slug,
        "is_builtin": False,
        "is_active": True,
    }


def load_agents(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"managed-agents.json not valid JSON: {exc}") from exc
    if not isinstance(data, list):
        raise RuntimeError("managed-agents.json must be a JSON array")
    return data


def save_agents(path: Path, agents: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    import tempfile

    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.tmp-")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(json.dumps(agents, indent=2) + "\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def write_relay_env(data_dir: Path, relay_url: str) -> Path:
    env_path = data_dir / "gentech-relay.env"
    lines = [
        "# Source this before launching Buzz Desktop, or pass these to the process.",
        f"RELAY_URL={relay_url}",
        "# Relay process (if run locally) also reads RELAY_URL.",
        "",
    ]
    env_path.write_text("\n".join(lines), encoding="utf-8")
    return env_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--relay", default=DEFAULT_RELAY, help="Relay ws:// or wss:// URL")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--profile", default=DEFAULT_PROFILE, help="Hermes profile to register")
    ap.add_argument("--name", default=None, help="Display name in Buzz agents panel")
    args = ap.parse_args()

    relay_url = args.relay
    if not (relay_url.startswith("ws://") or relay_url.startswith("wss://")):
        print(f"ERROR: relay must be ws:// or wss:// (got {relay_url})", file=sys.stderr)
        return 1

    profile = args.profile
    hermes_path = resolve_hermes()
    ph = profile_home(profile)
    prompt = read_soul_prompt(ph) or (
        f"You are the Hermes agent '{profile}' running inside Buzz. Coordinate "
        f"agent workflows and operate the agent economy stack."
    )
    display_name = args.name or profile.capitalize()
    entry = build_entry(profile, hermes_path, relay_url, prompt, display_name)
    slug = f"hermes:{profile}"

    data_dir = buzz_data_dir()
    agents_file = data_dir / "agents" / MANAGED_AGENTS_FILE

    existing = load_agents(agents_file)
    replaced = False
    for i, ag in enumerate(existing):
        if ag.get("slug") == slug or (
            ag.get("agent_command", "").endswith("hermes")
            and ag.get("agent_args") == ["-p", profile, "acp"]
        ):
            existing[i] = entry
            replaced = True
            break
    if not replaced:
        existing.append(entry)

    env_path = data_dir / "gentech-relay.env"

    if args.dry_run:
        print(f"[dry-run] buzz_data_dir : {data_dir}")
        print(f"[dry-run] agents_file   : {agents_file}")
        print(f"[dry-run] relay_url     : {relay_url}")
        print(f"[dry-run] hermes_path   : {hermes_path}")
        print(f"[dry-run] profile       : {profile}")
        print(f"[dry-run] would write {len(existing)} agent(s); {profile} present: {replaced or not replaced}")
        print(json.dumps(entry, indent=2))
        return 0

    save_agents(agents_file, existing)
    ep = write_relay_env(data_dir, relay_url)
    print(f"OK: seeded {display_name} agent ({'updated' if replaced else 'added'})")
    print(f"    agents_file : {agents_file}")
    print(f"    relay_url   : {relay_url}")
    print(f"    launch env  : {ep}")
    print(f"    next        : launch Buzz Desktop with RELAY_URL set (source {ep})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
