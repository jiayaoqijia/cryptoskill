#!/usr/bin/env python3
"""Solodit API client for audit-intelligence skill.

This module centralizes HTTP communication and response normalization so that
all tools share the same API/auth/retry behavior.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import aiohttp


class SoloditAPIError(RuntimeError):
    """Raised when Solodit API returns a non-success response."""


@dataclass
class SoloditConfig:
    """Runtime configuration loaded from environment variables."""

    base_url: str = os.getenv("SOLODIT_API_BASE", "https://api.solodit.xyz/v1")
    api_key: Optional[str] = os.getenv("SOLODIT_API_KEY")
    timeout_seconds: float = float(os.getenv("SOLODIT_TIMEOUT_SECONDS", "20"))


class SoloditClient:
    """Async Solodit API client with lightweight normalization helpers."""

    def __init__(self, config: Optional[SoloditConfig] = None):
        self.config = config or SoloditConfig()

    def _headers(self) -> Dict[str, str]:
        headers = {"Accept": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    async def _request(self, method: str, path: str, **kwargs: Any) -> Dict[str, Any]:
        if not self.config.api_key:
            raise SoloditAPIError("Missing SOLODIT_API_KEY environment variable")

        timeout = aiohttp.ClientTimeout(total=self.config.timeout_seconds)
        url = f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"

        async with aiohttp.ClientSession(timeout=timeout, headers=self._headers()) as session:
            async with session.request(method, url, **kwargs) as response:
                text = await response.text()
                if response.status >= 400:
                    raise SoloditAPIError(
                        f"Solodit API error {response.status} for {path}: {text[:300]}"
                    )
                try:
                    return await response.json()
                except Exception as exc:  # noqa: BLE001
                    raise SoloditAPIError(f"Invalid JSON from Solodit API: {text[:300]}") from exc

    async def search_findings(
        self,
        query: str,
        severities: Optional[List[str]] = None,
        limit: int = 10,
        sort_by: str = "recency",
    ) -> List[Dict[str, Any]]:
        """Search audit findings by keyword and optional filters."""
        params: Dict[str, Any] = {
            "q": query,
            "limit": max(1, min(limit, 50)),
            "sort": sort_by,
        }
        if severities:
            params["severity"] = ",".join(severities)

        payload = await self._request("GET", "/findings/search", params=params)
        findings = payload.get("data") or payload.get("findings") or []
        return [self._normalize_finding(item) for item in findings]

    async def get_project_findings(self, project: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get findings associated with a project identifier or contract address."""
        params = {"project": project, "limit": max(1, min(limit, 100))}
        payload = await self._request("GET", "/findings/project", params=params)
        findings = payload.get("data") or payload.get("findings") or []
        return [self._normalize_finding(item) for item in findings]

    async def similar_findings(self, text: str, limit: int = 8) -> List[Dict[str, Any]]:
        """Find semantically similar findings from a code snippet or summary text."""
        body = {"text": text, "limit": max(1, min(limit, 20))}
        payload = await self._request("POST", "/findings/similar", json=body)
        findings = payload.get("data") or payload.get("findings") or []
        return [self._normalize_finding(item) for item in findings]

    @staticmethod
    def _normalize_finding(raw: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize Solodit responses into a stable schema used by tools."""
        return {
            "id": raw.get("id") or raw.get("finding_id") or "unknown",
            "title": raw.get("title") or raw.get("name") or "Untitled finding",
            "severity": (raw.get("severity") or "UNKNOWN").upper(),
            "category": raw.get("category") or raw.get("vulnerability") or "uncategorized",
            "project": raw.get("project") or raw.get("protocol") or "unknown",
            "chain": raw.get("chain") or "unknown",
            "summary": raw.get("summary") or raw.get("description") or "No summary available",
            "recommendation": raw.get("recommendation") or raw.get("fix") or "No recommendation provided",
            "source_url": raw.get("url") or raw.get("source") or "",
            "published_at": raw.get("published_at") or raw.get("date") or "unknown",
            "score": raw.get("score"),
        }
