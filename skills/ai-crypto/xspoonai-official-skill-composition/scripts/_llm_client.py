#!/usr/bin/env python3
"""Shared LLM Client — SpoonOS LLMManager with stdlib HTTP fallback.

Strategy Pattern (three-level degradation):
    1. PREFERRED: spoon_ai.llm.LLMManager (native SpoonOS, fallback chain + caching)
    2. FALLBACK:  stdlib HTTP calls (when SpoonOS is not installed)
    3. BASELINE:  No LLM, return empty string (when no API keys available)

This module is the single source of truth for LLM interactions across
the Skill Composition Engine scripts (skill_discovery.py, workflow_composer.py).

Usage:
    from _llm_client import llm_chat, extract_json, load_env

    response = await llm_chat(
        messages=[{"role": "user", "content": "Hello"}],
        provider="openai",
        system="You are an expert.",
    )
    parsed = extract_json(response)
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import ssl
import sys
import urllib.request
from pathlib import Path
from typing import Any, Optional, Sequence


# ---------------------------------------------------------------------------
# Environment bootstrap
# ---------------------------------------------------------------------------

def load_env() -> None:
    """Load .env file from script or parent directory (best-effort)."""
    for candidate in (Path(__file__).parent, Path(__file__).parent.parent):
        env_file = candidate / ".env"
        if env_file.is_file():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip().strip("\"'"))
            break


# ---------------------------------------------------------------------------
# SpoonOS LLMManager detection
# ---------------------------------------------------------------------------

_USE_SPOONOS: bool = False
_llm_manager: Any = None

try:
    from spoon_ai.llm import LLMManager, ConfigurationManager  # type: ignore[import-untyped]

    _config_manager = ConfigurationManager()
    _llm_manager = LLMManager(_config_manager)
    _USE_SPOONOS = True
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Stdlib HTTP fallback (used when SpoonOS is not available)
# ---------------------------------------------------------------------------

_SSL_CTX = ssl.create_default_context()

_PROVIDER_CONFIG: dict[str, dict[str, str]] = {
    "openai": {
        "url": "https://api.openai.com/v1/chat/completions",
        "key_env": "OPENAI_API_KEY",
        "model": "gpt-4o-mini",
    },
    "anthropic": {
        "url": "https://api.anthropic.com/v1/messages",
        "key_env": "ANTHROPIC_API_KEY",
        "model": "claude-sonnet-4-20250514",
    },
    "deepseek": {
        "url": "https://api.deepseek.com/v1/chat/completions",
        "key_env": "DEEPSEEK_API_KEY",
        "model": "deepseek-chat",
    },
    "qwen": {
        "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        "key_env": "DASHSCOPE_API_KEY",
        "model": "qwen-plus",
    },
}


async def _http_llm_chat(
    messages: Sequence[dict[str, str]],
    provider: str,
    system: str,
    temperature: float,
    max_tokens: int,
) -> str:
    """Stdlib HTTP fallback for LLM chat when SpoonOS is unavailable."""
    cfg = _PROVIDER_CONFIG.get(provider, _PROVIDER_CONFIG["openai"])
    api_key = os.environ.get(cfg["key_env"], "")
    if not api_key:
        return ""

    if provider == "anthropic":
        payload = json.dumps({
            "model": cfg["model"],
            "max_tokens": max_tokens,
            "system": system,
            "messages": list(messages),
        }).encode()
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        }
    else:
        full_messages = []
        if system:
            full_messages.append({"role": "system", "content": system})
        full_messages.extend(messages)
        payload = json.dumps({
            "model": cfg["model"],
            "messages": full_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }).encode()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    req = urllib.request.Request(cfg["url"], data=payload, headers=headers)

    def _do_request() -> str:
        try:
            with urllib.request.urlopen(req, context=_SSL_CTX, timeout=30) as resp:
                data = json.loads(resp.read().decode())
            if provider == "anthropic":
                return "".join(
                    block.get("text", "")
                    for block in data.get("content", [])
                    if block.get("type") == "text"
                )
            return (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8") if e.fp else ""
            print(f"LLM HTTP error {e.code}: {body}", file=sys.stderr)
            return ""
        except Exception as e:
            print(f"LLM request failed: {e}", file=sys.stderr)
            return ""

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _do_request)


# ---------------------------------------------------------------------------
# Unified public API
# ---------------------------------------------------------------------------

async def llm_chat(
    messages: Sequence[dict[str, str]],
    *,
    provider: str = "openai",
    system: str = "",
    temperature: float = 0.1,
    max_tokens: int = 1024,
) -> str:
    """Send a chat request to the LLM, using SpoonOS or HTTP fallback.

    Args:
        messages: List of {"role": "user"|"assistant", "content": "..."} dicts.
        provider: LLM provider name (openai, anthropic, deepseek, qwen).
        system: System prompt (prepended or passed as system param).
        temperature: Sampling temperature.
        max_tokens: Maximum response tokens.

    Returns:
        The LLM response text, or empty string on failure.
    """
    if _USE_SPOONOS and _llm_manager is not None:
        try:
            full_messages: list[dict[str, str]] = []
            if system:
                full_messages.append({"role": "system", "content": system})
            full_messages.extend(messages)
            response = await _llm_manager.chat(
                full_messages,
                provider=provider,
            )
            if isinstance(response, str):
                return response
            # Handle structured response objects
            if hasattr(response, "content"):
                return str(response.content)
            return str(response)
        except Exception as e:
            print(
                f"SpoonOS LLMManager failed, falling back to HTTP: {e}",
                file=sys.stderr,
            )

    return await _http_llm_chat(
        messages, provider, system, temperature, max_tokens,
    )


def get_backend() -> str:
    """Return the active LLM backend name for diagnostics."""
    return "spoonos" if _USE_SPOONOS else "http"


# ---------------------------------------------------------------------------
# JSON extraction utility
# ---------------------------------------------------------------------------

def extract_json(text: str) -> Any:
    """Extract JSON from LLM response, handling markdown fences.

    Tries in order:
        1. ```json ... ``` fenced block
        2. Raw JSON starting with [ or {
        3. Returns None on failure
    """
    if not text:
        return None

    cleaned = text.strip()

    # Try fenced JSON block
    if "```json" in cleaned:
        try:
            json_str = cleaned.split("```json")[1].split("```")[0].strip()
            return json.loads(json_str)
        except (json.JSONDecodeError, IndexError):
            pass

    # Try any fenced block
    if "```" in cleaned:
        try:
            json_str = cleaned.split("```")[1].split("```")[0].strip()
            # Skip language identifier line if present
            if json_str and not json_str[0] in "[{":
                json_str = json_str.split("\n", 1)[1] if "\n" in json_str else json_str
            return json.loads(json_str)
        except (json.JSONDecodeError, IndexError):
            pass

    # Try raw JSON
    if cleaned.startswith(("[", "{")):
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

    return None
