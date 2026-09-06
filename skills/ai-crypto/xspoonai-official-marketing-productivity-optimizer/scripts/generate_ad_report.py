"""
generate_ad_report.py — Marketing Performance Report Generator

Generates a formatted marketing performance report with benchmark
comparisons, insights, and actionable recommendations.

Usage:
    python generate_ad_report.py --input parsed_data.json
    echo '{"metrics": {"impressions": 50000, "clicks": 750}}' | python generate_ad_report.py
"""

import json
import sys
import argparse
from typing import Any
from datetime import datetime


# Industry benchmarks for social media advertising (Instagram + Facebook average)
BENCHMARKS = {
    "ctr": {"low": 0.5, "good": 0.9, "excellent": 1.5, "unit": "%"},
    "cpc": {"low": 3.0, "good": 2.0, "excellent": 0.5, "unit": "$", "lower_is_better": True},
    "cpm": {"low": 20.0, "good": 15.0, "excellent": 5.0, "unit": "$", "lower_is_better": True},
    "roas": {"low": 1.0, "good": 3.0, "excellent": 5.0, "unit": "x"},
    "conversion_rate": {"low": 1.0, "good": 2.0, "excellent": 5.0, "unit": "%"},
    "frequency": {"low": 4.0, "good": 3.0, "excellent": 1.5, "unit": "", "lower_is_better": True},
}


def evaluate_metric(metric_name: str, value: float) -> dict[str, str]:
    """Evaluate a metric against benchmarks."""
    benchmark = BENCHMARKS.get(metric_name)
    if not benchmark:
        return {"status": "-", "benchmark": "-"}

    lower_is_better = benchmark.get("lower_is_better", False)
    unit = benchmark["unit"]

    if lower_is_better:
        if value <= benchmark["excellent"]:
            status = "Excellent"
        elif value <= benchmark["good"]:
            status = "Good"
        elif value <= benchmark["low"]:
            status = "Below Average"
        else:
            status = "Poor"
        benchmark_range = f"{benchmark['excellent']}{unit} - {benchmark['low']}{unit}"
    else:
        if value >= benchmark["excellent"]:
            status = "Excellent"
        elif value >= benchmark["good"]:
            status = "Good"
        elif value >= benchmark["low"]:
            status = "Below Average"
        else:
            status = "Poor"
        benchmark_range = f"{benchmark['low']}{unit} - {benchmark['excellent']}{unit}"

    return {"status": status, "benchmark": benchmark_range}


def format_metric_value(metric_name: str, value: float) -> str:
    """Format a metric value with appropriate unit and precision."""
    if metric_name in ("cpc", "cpm", "spend", "revenue"):
        return f"${value:,.2f}"
    elif metric_name in ("ctr", "conversion_rate", "engagement_rate"):
        return f"{value:.2f}%"
    elif metric_name == "roas":
        return f"{value:.2f}x"
    elif metric_name == "frequency":
        return f"{value:.1f}"
    elif metric_name in ("impressions", "clicks", "conversions", "reach"):
        return f"{value:,.0f}"
    else:
        return f"{value:,.2f}"


def generate_insights(metrics: dict[str, Any]) -> list[str]:
    """Generate actionable insights from the metrics."""
    insights = []

    ctr = metrics.get("ctr")
    cpc = metrics.get("cpc")
    cpm = metrics.get("cpm")
    roas = metrics.get("roas")
    conv_rate = metrics.get("conversion_rate")
    frequency = metrics.get("frequency")

    # CTR insights
    if ctr is not None:
        if ctr < 0.5:
            insights.append(
                "CTR is significantly below average. The ad creative or targeting may not resonate with the audience. "
                "Consider A/B testing new headlines, images, or refining audience segments."
            )
        elif ctr >= 1.5:
            insights.append(
                "CTR is excellent, indicating strong creative-audience alignment. "
                "Scale this campaign by increasing budget or expanding to similar audiences."
            )

    # CPC insights
    if cpc is not None:
        if cpc > 3.0:
            insights.append(
                "CPC is high. This may indicate competitive bidding or poor relevance score. "
                "Improve ad relevance, test different placements, or narrow targeting."
            )
        elif cpc < 0.5:
            insights.append(
                "CPC is very efficient. The ad is well-optimized for click acquisition."
            )

    # ROAS insights
    if roas is not None:
        if roas < 1.0:
            insights.append(
                "ROAS is below breakeven (< 1x). The campaign is losing money. "
                "Urgently review targeting, creatives, and landing page conversion rate."
            )
        elif roas >= 5.0:
            insights.append(
                "ROAS is excellent at 5x+. This is a highly profitable campaign. "
                "Consider increasing budget to maximize returns."
            )

    # Conversion rate insights
    if conv_rate is not None:
        if conv_rate < 1.0:
            insights.append(
                "Conversion rate is low. The landing page or post-click experience may need optimization. "
                "Review page load speed, CTA clarity, and offer relevance."
            )

    # Frequency insights
    if frequency is not None:
        if frequency > 4.0:
            insights.append(
                "Ad frequency is too high. Audience fatigue is likely reducing performance. "
                "Refresh creatives or expand the audience pool."
            )
        elif frequency < 1.2:
            insights.append(
                "Frequency is very low. The campaign may benefit from a longer run time or smaller audience "
                "to ensure sufficient exposure."
            )

    # Cross-metric insights
    if ctr and ctr > 1.0 and conv_rate and conv_rate < 1.0:
        insights.append(
            "High CTR but low conversion rate suggests a disconnect between ad promise and landing page. "
            "Ensure the landing page delivers on the ad's message."
        )

    if not insights:
        insights.append("Metrics are within normal ranges. Continue monitoring and consider incremental optimizations.")

    return insights


def generate_recommendations(metrics: dict[str, Any]) -> list[dict[str, str]]:
    """Generate specific recommendations based on metrics."""
    recommendations = []

    ctr = metrics.get("ctr")
    cpc = metrics.get("cpc")
    roas = metrics.get("roas")
    conv_rate = metrics.get("conversion_rate")
    frequency = metrics.get("frequency")

    if ctr is not None and ctr < 0.9:
        recommendations.append({
            "area": "Creative",
            "action": "Test 3 new ad creative variations with different hooks (problem/solution, benefit-first, social proof). "
                      "Aim for CTR above 0.9%.",
        })

    if cpc is not None and cpc > 2.0:
        recommendations.append({
            "area": "Bidding & Targeting",
            "action": "Switch to automatic bidding or narrow audience targeting to reduce CPC. "
                      "Test lookalike audiences based on existing converters.",
        })

    if roas is not None and roas < 3.0:
        recommendations.append({
            "area": "Conversion Funnel",
            "action": "Optimize the conversion funnel — review landing page UX, simplify the checkout process, "
                      "and add social proof elements to improve ROAS.",
        })

    if conv_rate is not None and conv_rate < 2.0:
        recommendations.append({
            "area": "Landing Page",
            "action": "A/B test landing page elements: headline, CTA button color/text, form length. "
                      "Ensure message match between ad and landing page.",
        })

    if frequency is not None and frequency > 3.0:
        recommendations.append({
            "area": "Audience & Frequency",
            "action": "Refresh ad creatives to combat fatigue, or expand target audience by 20-30% "
                      "to reduce frequency while maintaining reach.",
        })

    if not recommendations:
        recommendations.append({
            "area": "Scaling",
            "action": "Campaign metrics are healthy. Consider increasing daily budget by 20% and monitoring "
                      "performance for 3-5 days before further scaling.",
        })

    return recommendations


def generate_report(data: dict[str, Any]) -> str:
    """Generate a formatted marketing performance report."""
    metrics = data.get("metrics", data)
    report_date = datetime.now().strftime("%Y-%m-%d")

    lines = []
    lines.append(f"## Marketing Performance Report")
    lines.append(f"**Generated**: {report_date}")
    lines.append("")

    # Campaign Overview Table
    lines.append("### Campaign Overview")
    lines.append("| Metric | Value | Benchmark | Status |")
    lines.append("|--------|-------|-----------|--------|")

    metric_display_order = [
        "impressions", "reach", "clicks", "ctr", "cpc", "cpm",
        "spend", "conversions", "conversion_rate", "revenue", "roas", "frequency",
    ]

    for metric_name in metric_display_order:
        value = metrics.get(metric_name)
        if value is not None:
            formatted = format_metric_value(metric_name, value)
            evaluation = evaluate_metric(metric_name, value)
            display_name = metric_name.upper().replace("_", " ")
            lines.append(f"| {display_name} | {formatted} | {evaluation['benchmark']} | {evaluation['status']} |")

    lines.append("")

    # Key Findings
    insights = generate_insights(metrics)
    lines.append("### Key Findings")
    for i, insight in enumerate(insights, 1):
        lines.append(f"{i}. {insight}")
    lines.append("")

    # Optimization Recommendations
    recommendations = generate_recommendations(metrics)
    lines.append("### Optimization Recommendations")
    for i, rec in enumerate(recommendations, 1):
        lines.append(f"{i}. **{rec['area']}**: {rec['action']}")
    lines.append("")

    # Next Steps
    lines.append("### Next Steps")
    lines.append("- [ ] Implement top-priority recommendation")
    lines.append("- [ ] Set up A/B test for underperforming metrics")
    lines.append("- [ ] Schedule next performance review in 7 days")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate marketing performance report")
    parser.add_argument("--input", "-i", type=str, help="Path to parsed data JSON file")
    parser.add_argument("--output-format", "-o", type=str, choices=["markdown", "json"], default="markdown",
                        help="Output format")
    args = parser.parse_args()

    # Read input
    if args.input:
        with open(args.input, "r") as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    if args.output_format == "json":
        metrics = data.get("metrics", data)
        result = {
            "metrics": metrics,
            "evaluations": {k: evaluate_metric(k, v) for k, v in metrics.items() if isinstance(v, (int, float))},
            "insights": generate_insights(metrics),
            "recommendations": generate_recommendations(metrics),
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        report = generate_report(data)
        print(report)


if __name__ == "__main__":
    main()
