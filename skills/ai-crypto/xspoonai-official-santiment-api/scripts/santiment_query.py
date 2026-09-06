#!/usr/bin/env python3
"""Execute a Santiment GraphQL query for any metric, asset, and time range.

Reads JSON from stdin, constructs a getMetric query, POSTs to the Santiment
GraphQL API, and writes JSON results to stdout.

Input JSON fields:
    metric (str, required): Metric name (e.g., "price_usd", "daily_active_addresses")
    slug (str): Single asset identifier (e.g., "bitcoin"). Mutually exclusive with slugs.
    slugs (list[str]): Multiple asset identifiers. Uses timeseriesDataPerSlugJson.
    from (str): Start of time range. ISO 8601 or relative (e.g., "utc_now-7d"). Default: "utc_now-30d"
    to (str): End of time range. Default: "utc_now"
    interval (str): Data granularity (e.g., "1d", "1h"). Default: "1d"
    sub_field (str): Query sub-field. Default: "timeseriesData"
        Options: timeseriesData, aggregatedTimeseriesData, timeseriesDataPerSlugJson
    aggregation (str): Override aggregation (AVG, SUM, LAST, FIRST, MEDIAN, MAX, MIN, ANY)
    transform (dict): Transform object, e.g. {"type": "moving_average", "movingAverageBase": 7}
    selector (dict): Advanced selector overriding slug/slugs. Used for holdersCount, owner, etc.

Environment:
    SANTIMENT_API_KEY (required): API key for authentication

Output JSON:
    On success: {"success": true, "data": <API response data>}
    On error:   {"success": false, "error": "<message>", "details": <optional>}
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

API_URL = "https://api.santiment.net/graphql"


def build_query(params: dict) -> tuple[str, dict]:
    """Build a GraphQL query string and variables dict from input parameters."""
    metric = params["metric"]
    slug = params.get("slug")
    slugs = params.get("slugs")
    selector = params.get("selector")
    from_dt = params.get("from", "utc_now-30d")
    to_dt = params.get("to", "utc_now")
    interval = params.get("interval", "1d")
    sub_field = params.get("sub_field", "timeseriesData")
    aggregation = params.get("aggregation")
    transform = params.get("transform")

    variables: dict = {"metric": metric, "from": from_dt, "to": to_dt}

    # Determine selector vs slug
    if selector:
        variables["selector"] = selector
    elif slugs:
        variables["selector"] = {"slugs": slugs}
    elif slug:
        variables["slug"] = slug
    else:
        variables["slug"] = "bitcoin"  # sensible default

    # Determine which optional params apply for this sub-field
    use_interval = bool(interval) and sub_field != "aggregatedTimeseriesData"
    use_transform = bool(transform) and sub_field == "timeseriesData"

    if use_interval:
        variables["interval"] = interval
    if aggregation:
        variables["aggregation"] = aggregation
    if use_transform:
        variables["transform"] = transform

    # Build variable declarations (only declare variables that are used)
    var_decls = ["$metric: String!", "$from: DateTime!", "$to: DateTime!"]
    use_selector = "selector" in variables
    if use_selector:
        var_decls.append("$selector: MetricTargetSelectorInputObject")
    else:
        var_decls.append("$slug: String")
    if use_interval:
        var_decls.append("$interval: interval")
    if aggregation:
        var_decls.append("$aggregation: Aggregation")
    if use_transform:
        var_decls.append("$transform: TimeseriesMetricTransformInputObject")

    # Build sub-field arguments
    target_arg = "selector: $selector" if use_selector else "slug: $slug"
    args = [target_arg, "from: $from", "to: $to"]
    if use_interval:
        args.append("interval: $interval")
    if aggregation:
        args.append("aggregation: $aggregation")
    if use_transform:
        args.append("transform: $transform")

    args_str = ", ".join(args)

    # Build return fields
    if sub_field == "timeseriesData":
        return_fields = " { datetime value }"
    elif sub_field == "aggregatedTimeseriesData":
        return_fields = ""
    elif sub_field == "timeseriesDataPerSlugJson":
        return_fields = ""
    else:
        return_fields = ""

    query = (
        f"query({', '.join(var_decls)}) {{ "
        f"getMetric(metric: $metric) {{ "
        f"{sub_field}({args_str}){return_fields}"
        f" }} }}"
    )

    return query, variables


def execute_query(query: str, variables: dict, api_key: str) -> dict:
    """Send a GraphQL request to the Santiment API and return the parsed response."""
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")

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
        body = e.read().decode("utf-8", errors="replace")
        if e.code == 429:
            return {"error": "rate_limited", "message": "API rate limit exceeded. Back off and retry.", "status": 429}
        return {"error": "http_error", "message": f"HTTP {e.code}: {body}", "status": e.code}
    except urllib.error.URLError as e:
        return {"error": "connection_error", "message": str(e.reason)}
    except TimeoutError:
        return {"error": "timeout", "message": "Request timed out after 25 seconds"}


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

    if "metric" not in params:
        json.dump({"success": False, "error": "Missing required field: metric"}, sys.stdout)
        sys.exit(1)

    query, variables = build_query(params)
    result = execute_query(query, variables, api_key)

    # Check for connection/rate-limit errors
    if "error" in result and "data" not in result:
        json.dump({"success": False, "error": result["message"], "error_type": result["error"]}, sys.stdout)
        sys.exit(1)

    # Check for GraphQL errors
    if result.get("errors"):
        messages = [e.get("message", "Unknown error") for e in result["errors"]]
        json.dump({"success": False, "error": "; ".join(messages), "errors": result["errors"]}, sys.stdout)
        sys.exit(1)

    json.dump({"success": True, "data": result.get("data")}, sys.stdout)


if __name__ == "__main__":
    main()
