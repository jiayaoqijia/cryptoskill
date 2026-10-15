"""
GenTech Agent Kit — Pika Creative Suite Plugin
Integrates Pika MCP (video generation, brand assets, creative skills)
into the Agent Kit's plugin system.

register_gentech_plugin(mcp) is auto-discovered by the Agent Kit plugin system.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

import httpx

_LOG = logging.getLogger("gentech-kit.plugins.pika")

# ── Config ──────────────────────────────────────────────────────────────────

PIKA_MCP_URL = "https://experiment-mcp.pika.art/api/mcp"
PIKA_TOKEN = os.environ.get("PIKA_TOKEN", "")

# ── HTTP Client ──────────────────────────────────────────────────────────────

_client: httpx.Client | None = None


def _http() -> httpx.Client:
    global _client
    if _client is None:
        _client = httpx.Client(timeout=60.0)
    return _client


def _mcp_headers() -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if PIKA_TOKEN:
        headers["Authorization"] = f"Bearer {PIKA_TOKEN}"
    return headers


def _pika_call(method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    """Call the Pika MCP server with a tool request."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": method, "arguments": params or {}},
    }
    resp = _http().post(PIKA_MCP_URL, json=payload, headers=_mcp_headers())
    if resp.status_code == 402:
        return {"error": "Pika requires payment. Set PIKA_TOKEN env var."}
    resp.raise_for_status()
    return resp.json()


def _pika_list_tools() -> list[dict[str, Any]]:
    """List available Pika MCP tools."""
    payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    try:
        resp = _http().post(PIKA_MCP_URL, json=payload, headers=_mcp_headers())
        resp.raise_for_status()
        return resp.json().get("result", {}).get("tools", [])
    except Exception as exc:
        _LOG.warning("Failed to list Pika tools: %s", exc)
        return []


# ── Plugin Registration ─────────────────────────────────────────────────────


def register_gentech_plugin(mcp: object) -> None:
    """Register Pika creative tools with the Agent Kit MCP server."""

    @mcp.tool()  # type: ignore[misc]
    def pika_skills() -> str:
        """List available Pika creative skills — 4K VFX, App Sizzle, Build-a-Brand, Explainer, Founder Video, Podcast, UGC Ads, and more."""
        tools = _pika_list_tools()
        return json.dumps({
            "provider": "Pika",
            "mcp_url": PIKA_MCP_URL,
            "available_skills": [t.get("name") for t in tools],
            "count": len(tools),
        }, indent=2)

    @mcp.tool()  # type: ignore[misc]
    def pika_generate(skill: str, params: str = "{}") -> str:
        """Generate content using a Pika creative skill. Skills: 4k-vfx, app-sizzle, app-store-screens, build-a-brand, founder-product-video, explainer, podcast, ugc-ads, voxel-it, anime-soccer, gameday, kiss-cam, baseball-trend, viral-hook, content-director, fix-my-look, persona-builder, language-swap, stagefight, vfx. Pass params as JSON string."""
        try:
            parsed = json.loads(params) if isinstance(params, str) else params
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON params"})
        result = _pika_call(skill, parsed)
        content = result.get("result", {}).get("content", [])
        return json.dumps({"skill": skill, "result": content}, indent=2)

    @mcp.tool()  # type: ignore[misc]
    def pika_build_brand(brief: str) -> str:
        """Generate a complete brand identity from a product brief. Creates brand strategy, tone of voice, logo direction, color palette, typography, and brand.md."""
        return pika_generate("build-a-brand", json.dumps({"brief": brief}))

    @mcp.tool()  # type: ignore[misc]
    def pika_app_sizzle(url: str) -> str:
        """Create a 15-second launch video from an app store link, product screens, or GitHub repo URL."""
        return pika_generate("app-sizzle", json.dumps({"url": url}))

    @mcp.tool()  # type: ignore[misc]
    def pika_explainer(url: str) -> str:
        """Turn a URL, GitHub repo, or written brief into a polished explainer video."""
        return pika_generate("explainer", json.dumps({"url": url}))

    _LOG.info("Registered Pika Creative Suite plugin: %s", PIKA_MCP_URL)


__plugin_manifest__ = {
    "name": "Pika Creative Suite",
    "version": "0.1.0",
    "description": "Pika MCP integration — AI video, brand, and creative skills for agents",
}