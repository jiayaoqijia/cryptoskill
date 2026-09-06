"""
parse_ad_data.py — Multi-Format Ad Performance Data Parser

Parses advertising performance data from CSV, JSON, or plain text
and outputs a standardized JSON structure for report generation.

Usage:
    python parse_ad_data.py --input data.csv --format csv
    python parse_ad_data.py --input data.json --format json
    echo "Impressions: 50000, Clicks: 750, Spend: $500" | python parse_ad_data.py --format text
"""

import json
import csv
import sys
import re
import argparse
from typing import Any
from io import StringIO


# Metric definitions with aliases for flexible parsing
METRIC_ALIASES = {
    "impressions": ["impressions", "impr", "views", "shown"],
    "clicks": ["clicks", "click", "clk"],
    "ctr": ["ctr", "click_through_rate", "click-through-rate", "clickthrough"],
    "cpc": ["cpc", "cost_per_click", "cost-per-click"],
    "cpm": ["cpm", "cost_per_mille", "cost_per_thousand"],
    "roas": ["roas", "return_on_ad_spend", "return-on-ad-spend"],
    "conversion_rate": ["conversion_rate", "conv_rate", "cvr", "cr"],
    "conversions": ["conversions", "conv", "converts"],
    "frequency": ["frequency", "freq", "avg_frequency"],
    "spend": ["spend", "cost", "total_spend", "budget", "amount_spent"],
    "revenue": ["revenue", "sales", "total_revenue", "income"],
    "reach": ["reach", "unique_reach", "people_reached"],
    "engagement_rate": ["engagement_rate", "eng_rate", "er"],
}


def normalize_metric_name(raw_name: str) -> str | None:
    """Map a raw metric name to its standardized name."""
    cleaned = raw_name.strip().lower().replace(" ", "_").replace("-", "_")
    for standard_name, aliases in METRIC_ALIASES.items():
        if cleaned in aliases:
            return standard_name
    return None


def parse_numeric(value: str) -> float | None:
    """Parse a numeric value, handling currency symbols, commas, and percentages."""
    if not value:
        return None
    cleaned = value.strip().replace(",", "").replace("$", "").replace("%", "")
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_csv_data(content: str) -> list[dict[str, Any]]:
    """Parse CSV formatted ad data."""
    reader = csv.DictReader(StringIO(content))
    results = []

    for row in reader:
        parsed_row = {}
        for raw_key, raw_value in row.items():
            metric_name = normalize_metric_name(raw_key)
            if metric_name:
                numeric_val = parse_numeric(raw_value)
                if numeric_val is not None:
                    parsed_row[metric_name] = numeric_val
            else:
                # Keep non-metric fields as metadata
                parsed_row[raw_key.strip().lower().replace(" ", "_")] = raw_value.strip()

        if parsed_row:
            results.append(parsed_row)

    return results


def parse_json_data(content: str) -> list[dict[str, Any]]:
    """Parse JSON formatted ad data."""
    data = json.loads(content)

    # Handle both single object and array of objects
    if isinstance(data, dict):
        data = [data]

    results = []
    for item in data:
        parsed = {}
        for raw_key, raw_value in item.items():
            metric_name = normalize_metric_name(raw_key)
            if metric_name:
                if isinstance(raw_value, (int, float)):
                    parsed[metric_name] = float(raw_value)
                elif isinstance(raw_value, str):
                    numeric_val = parse_numeric(raw_value)
                    if numeric_val is not None:
                        parsed[metric_name] = numeric_val
            else:
                parsed[raw_key.strip().lower().replace(" ", "_")] = raw_value
        if parsed:
            results.append(parsed)

    return results


def parse_text_data(content: str) -> list[dict[str, Any]]:
    """Parse plain text ad data with flexible formatting."""
    parsed = {}

    # Pattern: "Metric: Value" or "Metric = Value"
    patterns = [
        r"([a-zA-Z\s_-]+)[:\s=]+\$?([\d,]+\.?\d*)\s*%?",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, content)
        for raw_name, raw_value in matches:
            metric_name = normalize_metric_name(raw_name)
            if metric_name:
                numeric_val = parse_numeric(raw_value)
                if numeric_val is not None:
                    parsed[metric_name] = numeric_val

    return [parsed] if parsed else []


def compute_derived_metrics(data: dict[str, Any]) -> dict[str, Any]:
    """Calculate missing metrics from available data."""
    result = dict(data)

    impressions = result.get("impressions")
    clicks = result.get("clicks")
    spend = result.get("spend")
    conversions = result.get("conversions")
    revenue = result.get("revenue")

    # CTR = Clicks / Impressions * 100
    if "ctr" not in result and clicks and impressions:
        result["ctr"] = round((clicks / impressions) * 100, 2)

    # CPC = Spend / Clicks
    if "cpc" not in result and spend and clicks:
        result["cpc"] = round(spend / clicks, 2)

    # CPM = Spend / Impressions * 1000
    if "cpm" not in result and spend and impressions:
        result["cpm"] = round((spend / impressions) * 1000, 2)

    # ROAS = Revenue / Spend
    if "roas" not in result and revenue and spend:
        result["roas"] = round(revenue / spend, 2)

    # Conversion Rate = Conversions / Clicks * 100
    if "conversion_rate" not in result and conversions and clicks:
        result["conversion_rate"] = round((conversions / clicks) * 100, 2)

    return result


def parse_ad_data(content: str, fmt: str) -> dict[str, Any]:
    """Main parsing function. Returns standardized data structure."""
    parsers = {
        "csv": parse_csv_data,
        "json": parse_json_data,
        "text": parse_text_data,
    }

    parser = parsers.get(fmt)
    if not parser:
        return {"error": f"Unsupported format: {fmt}. Use csv, json, or text."}

    try:
        rows = parser(content)
    except Exception as e:
        return {"error": f"Failed to parse {fmt} data: {str(e)}"}

    if not rows:
        return {"error": "No metrics could be parsed from the input."}

    # Compute derived metrics for each row
    enriched_rows = [compute_derived_metrics(row) for row in rows]

    # If single row, also provide flat summary
    if len(enriched_rows) == 1:
        return {
            "status": "success",
            "format": fmt,
            "metrics": enriched_rows[0],
            "derived_metrics_computed": True,
        }

    return {
        "status": "success",
        "format": fmt,
        "rows": enriched_rows,
        "row_count": len(enriched_rows),
        "derived_metrics_computed": True,
    }


def main():
    parser = argparse.ArgumentParser(description="Parse ad performance data")
    parser.add_argument("--input", "-i", type=str, help="Path to input file")
    parser.add_argument("--format", "-f", type=str, choices=["csv", "json", "text"], default="text",
                        help="Input data format")
    args = parser.parse_args()

    # Read input from file or stdin
    if args.input:
        with open(args.input, "r") as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    result = parse_ad_data(content, args.format)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
