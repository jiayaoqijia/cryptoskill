#!/usr/bin/env python3
"""Discover available metrics and asset slugs from the Santiment API.

Reads JSON from stdin, queries the Santiment GraphQL API for discovery data,
and writes JSON results to stdout.

Input JSON fields:
    action (str, required): One of "metrics", "slugs", or "metadata"
    search (str): Filter keyword for metrics/slugs actions (case-insensitive substring match)
    metric (str): Metric name for the "metadata" action

Actions:
    metrics  - List available metrics, optionally filtered by search keyword
    slugs    - List project slugs (assets), optionally filtered by search keyword
    metadata - Fetch metadata for a specific metric (available slugs, aggregations, intervals, etc.)

Environment:
    SANTIMENT_API_KEY (required): API key for authentication

Output JSON:
    On success: {"success": true, "data": <results>, "count": <int>}
    On error:   {"success": false, "error": "<message>"}
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

API_URL = "https://api.santiment.net/graphql"


def graphql_request(query: str, api_key: str, variables: dict | None = None) -> dict:
    """Send a GraphQL request and return parsed JSON response."""
    body: dict = {"query": query}
    if variables:
        body["variables"] = variables

    payload = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Apikey {api_key}",
            "User-Agent": "santiment-api-skill/1.1.5",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        if e.code == 429:
            return {"error": "rate_limited", "message": "API rate limit exceeded. Back off and retry."}
        return {"error": "http_error", "message": f"HTTP {e.code}: {body_text}"}
    except urllib.error.URLError as e:
        return {"error": "connection_error", "message": str(e.reason)}
    except TimeoutError:
        return {"error": "timeout", "message": "Request timed out after 25 seconds"}


def fetch_metrics(api_key: str, search: str | None = None) -> dict:
    """Fetch available metrics, optionally filtered by keyword."""
    result = graphql_request("{ getAvailableMetrics }", api_key)

    if "error" in result and "data" not in result:
        return {"success": False, "error": result["message"]}

    if result.get("errors"):
        messages = [e.get("message", "Unknown error") for e in result["errors"]]
        return {"success": False, "error": "; ".join(messages)}

    metrics: list[str] = result.get("data", {}).get("getAvailableMetrics", [])

    if search:
        keyword = search.lower()
        metrics = [m for m in metrics if keyword in m.lower()]

    return {"success": True, "data": metrics, "count": len(metrics)}


def fetch_slugs(api_key: str, search: str | None = None) -> dict:
    """Fetch project slugs, optionally filtered by keyword."""
    query = "{ allProjects(page: 1, pageSize: 5000) { slug name ticker } }"
    result = graphql_request(query, api_key)

    if "error" in result and "data" not in result:
        return {"success": False, "error": result["message"]}

    if result.get("errors"):
        messages = [e.get("message", "Unknown error") for e in result["errors"]]
        return {"success": False, "error": "; ".join(messages)}

    projects: list[dict] = result.get("data", {}).get("allProjects", [])

    if search:
        keyword = search.lower()
        projects = [
            p for p in projects
            if keyword in p.get("slug", "").lower()
            or keyword in p.get("name", "").lower()
            or keyword in p.get("ticker", "").lower()
        ]

    return {"success": True, "data": projects, "count": len(projects)}


def fetch_metadata(api_key: str, metric: str) -> dict:
    """Fetch metadata for a specific metric."""
    query = """
    query($metric: String!) {
      getMetric(metric: $metric) {
        metadata {
          availableSlugs
          availableAggregations
          availableSelectors
          dataType
          defaultAggregation
          minInterval
        }
        availableSince(slug: "bitcoin")
        lastDatetimeComputedAt(slug: "bitcoin")
      }
    }
    """
    result = graphql_request(query, api_key, variables={"metric": metric})

    if "error" in result and "data" not in result:
        return {"success": False, "error": result["message"]}

    if result.get("errors"):
        messages = [e.get("message", "Unknown error") for e in result["errors"]]
        return {"success": False, "error": "; ".join(messages)}

    metric_data = result.get("data", {}).get("getMetric", {})
    return {"success": True, "data": metric_data}


def main() -> None:
    api_key = os.environ.get("SANTIMENT_API_KEY", "").strip()
    if not api_key:
        json.dump(
            {"success": False, "error": "SANTIMENT_API_KEY environment variable is not set"},
            sys.stdout,
        )
        sys.exit(1)

    try:
        params = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        json.dump({"success": False, "error": f"Invalid JSON input: {e}"}, sys.stdout)
        sys.exit(1)

    action = params.get("action")
    if action not in ("metrics", "slugs", "metadata"):
        json.dump(
            {"success": False, "error": f"Invalid action: {action!r}. Must be 'metrics', 'slugs', or 'metadata'"},
            sys.stdout,
        )
        sys.exit(1)

    search = params.get("search")

    if action == "metrics":
        output = fetch_metrics(api_key, search)
    elif action == "slugs":
        output = fetch_slugs(api_key, search)
    elif action == "metadata":
        metric = params.get("metric")
        if not metric:
            json.dump({"success": False, "error": "Missing required field 'metric' for metadata action"}, sys.stdout)
            sys.exit(1)
        output = fetch_metadata(api_key, metric)

    json.dump(output, sys.stdout)
    if not output.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
