from __future__ import annotations

import os
from typing import Any

import httpx

from crypto_skill.constants import (
    APIFY_BASE_URL,
    AUTH_ERROR_CODES,
    DEFAULT_TIMEOUT,
    RATE_LIMIT_ERROR_CODE,
    TIMEOUT_ERROR_CODE,
)
from crypto_skill.exceptions import (
    ActorDataError,
    ApifyActorError,
    ApifyAuthError,
    ApifyTimeoutError,
)


async def run_actor_sync(actor_id: str, run_input: dict[str, Any]) -> list[dict[str, Any]]:
    """Run an Apify actor synchronously and return dataset items."""
    token = os.environ.get("APIFY_API_TOKEN")
    if not token:
        raise ApifyAuthError("APIFY_API_TOKEN environment variable is not set")

    url = f"{APIFY_BASE_URL}/acts/{actor_id}/run-sync-get-dataset-items"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.post(url, json=run_input, headers=headers)
    except httpx.TimeoutException as exc:
        raise ApifyTimeoutError(f"Request timed out: {exc}") from exc
    except httpx.RequestError as exc:
        raise ApifyActorError(f"Request failed: {exc}") from exc

    status = response.status_code

    if status in AUTH_ERROR_CODES:
        raise ApifyAuthError(f"Authentication failed (HTTP {status})")
    if status == TIMEOUT_ERROR_CODE:
        raise ApifyTimeoutError(f"Actor run timed out (HTTP {status})")
    if status == RATE_LIMIT_ERROR_CODE:
        raise ApifyActorError(f"Apify API rate limited (HTTP {status})")
    if status >= 400:
        raise ApifyActorError(f"Actor run failed (HTTP {status})")

    try:
        data = response.json()
    except ValueError as exc:
        raise ActorDataError(f"Invalid JSON response: {exc}") from exc

    if not isinstance(data, list):
        raise ActorDataError(f"Expected list, got {type(data).__name__}")

    return data
