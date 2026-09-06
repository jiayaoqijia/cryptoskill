#!/usr/bin/env python3
import json
import argparse
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime
import math


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details=None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


# Default metric thresholds and units
METRIC_CONFIG = {
    "load_time_ms": {
        "unit": "milliseconds",
        "threshold": 3000,
        "description": "Page load time",
        "type": "time",
        "lower_is_better": True
    },
    "bundle_size_kb": {
        "unit": "kilobytes",
        "threshold": 500,
        "description": "JavaScript bundle size",
        "type": "size",
        "lower_is_better": True
    },
    "requests": {
        "unit": "count",
        "threshold": 50,
        "description": "Number of HTTP requests",
        "type": "count",
        "lower_is_better": True
    },
    "first_contentful_paint_ms": {
        "unit": "milliseconds",
        "threshold": 2500,
        "description": "Time to First Contentful Paint",
        "type": "time",
        "lower_is_better": True
    },
    "memory_mb": {
        "unit": "megabytes",
        "threshold": 100,
        "description": "Memory usage",
        "type": "size",
        "lower_is_better": True
    },
    "error_rate": {
        "unit": "percentage",
        "threshold": 0.1,
        "description": "Error rate",
        "type": "percentage",
        "lower_is_better": True
    }
}


def calculate_overage(value: float, budget: float) -> float:
    """Calculate percentage overage."""
    if budget == 0:
        return 0
    return ((value - budget) / budget) * 100


def calculate_margin(value: float, budget: float) -> float:
    """Calculate percentage margin remaining."""
    if budget == 0:
        return 0
    return ((budget - value) / budget) * 100


def determine_severity(metric: str, value: float, budget: float) -> str:
    """Determine severity level based on overage."""
    if value <= budget:
        return "pass"
    
    overage = calculate_overage(value, budget)
    
    if overage <= 5:
        return "warning"
    elif overage <= 15:
        return "caution"
    else:
        return "critical"


def check_performance_budget(metrics: Dict[str, float], budget: Dict[str, float], 
                            baseline: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Comprehensive performance budget check with trend analysis."""
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "checks": [],
        "summary": {
            "total_metrics": len(metrics),
            "passed": 0,
            "warnings": 0,
            "cautions": 0,
            "critical": 0
        },
        "overall_status": "pass",
        "details": {}
    }
    
    for metric_name, value in metrics.items():
        budget_value = budget.get(metric_name, float('inf'))
        config = METRIC_CONFIG.get(metric_name, {})
        
        # Determine check status
        severity = determine_severity(metric_name, value, budget_value)
        
        # Update summary
        if severity == "pass":
            results["summary"]["passed"] += 1
        elif severity == "warning":
            results["summary"]["warnings"] += 1
            results["overall_status"] = "warning"
        elif severity == "caution":
            results["summary"]["cautions"] += 1
            if results["overall_status"] == "pass":
                results["overall_status"] = "caution"
        elif severity == "critical":
            results["summary"]["critical"] += 1
            results["overall_status"] = "critical"
        
        # Calculate metrics
        overage = calculate_overage(value, budget_value) if value > budget_value else 0
        margin = calculate_margin(value, budget_value) if value <= budget_value else 0
        
        # Trend analysis
        trend = None
        trend_direction = None
        if baseline and metric_name in baseline:
            baseline_value = baseline[metric_name]
            change = value - baseline_value
            change_pct = (change / baseline_value * 100) if baseline_value != 0 else 0
            
            if abs(change_pct) < 1:
                trend = "stable"
            elif change_pct > 0:
                trend = "degraded"
                trend_direction = f"+{change_pct:.1f}%"
            else:
                trend = "improved"
                trend_direction = f"{change_pct:.1f}%"
        
        check = {
            "metric": metric_name,
            "value": value,
            "budget": budget_value,
            "unit": config.get("unit", "unknown"),
            "status": severity,
            "passed": severity == "pass",
            "description": config.get("description", ""),
            "overage_pct": round(overage, 1) if overage > 0 else 0,
            "margin_pct": round(margin, 1) if margin > 0 else 0,
            "recommendation": generate_recommendation(metric_name, severity, value, budget_value)
        }
        
        if trend:
            check["trend"] = trend
            if trend_direction:
                check["trend_change"] = trend_direction
        
        results["checks"].append(check)
        results["details"][metric_name] = {
            "current": value,
            "budget": budget_value,
            "overage": overage,
            "margin": margin,
            "status": severity
        }
    
    return results


def generate_recommendation(metric: str, severity: str, value: float, budget: float) -> str:
    """Generate actionable recommendation based on metric violation."""
    
    if severity == "pass":
        return "Within budget"
    
    if severity == "warning":
        return f"Nearly at budget ({value:.0f}/{budget:.0f}). Monitor closely."
    
    overage = calculate_overage(value, budget)
    
    recommendations = {
        "load_time_ms": f"Reduce by {overage:.1f}%. Consider code splitting, lazy loading, or compression.",
        "bundle_size_kb": f"Reduce by {overage:.1f}%. Remove unused dependencies or minify code.",
        "requests": f"Reduce by {overage:.1f}%. Combine requests or use HTTP/2 multiplexing.",
        "first_contentful_paint_ms": f"Reduce by {overage:.1f}%. Optimize critical rendering path.",
        "memory_mb": f"Reduce by {overage:.1f}%. Profile memory usage and fix leaks.",
        "error_rate": f"Reduce by {overage:.1f}%. Improve error handling and monitoring."
    }
    
    return recommendations.get(metric, f"Reduce by {overage:.1f}%. Optimize this metric.")


def main():
    parser = argparse.ArgumentParser(
        description='Validate application performance metrics against budgets'
    )
    parser.add_argument('--demo', action='store_true', help='Run with realistic demo metrics')
    parser.add_argument('--params', type=str, help='JSON with metrics, budgets, and optional baseline')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            # Realistic demo scenario: Web application performance metrics
            metrics = {
                "load_time_ms": 2800,           # Within budget
                "bundle_size_kb": 520,          # 4% over budget
                "requests": 48,                 # Within budget
                "first_contentful_paint_ms": 2200,  # Well within budget
                "memory_mb": 95,                # Within budget
                "error_rate": 0.08              # Within budget
            }
            
            budget = {
                "load_time_ms": 3000,
                "bundle_size_kb": 500,
                "requests": 50,
                "first_contentful_paint_ms": 2500,
                "memory_mb": 100,
                "error_rate": 0.1
            }
            
            # Historical baseline for trend analysis
            baseline = {
                "load_time_ms": 2600,
                "bundle_size_kb": 480,
                "requests": 45,
                "first_contentful_paint_ms": 2100,
                "memory_mb": 92,
                "error_rate": 0.06
            }
            
            check = check_performance_budget(metrics, budget, baseline)
            result = {
                "demo": True,
                "application": "web-frontend",
                "environment": "production",
                "check": check
            }
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            metrics = params.get("metrics", {})
            budget = params.get("budget", {})
            baseline = params.get("baseline")
            
            if not metrics:
                raise ValueError("'metrics' object is required")
            if not budget:
                raise ValueError("'budget' object is required")
            
            # Validate that metrics are numeric
            for key, value in metrics.items():
                if not isinstance(value, (int, float)):
                    raise ValueError(f"Metric '{key}' must be numeric, got {type(value).__name__}")
            
            for key, value in budget.items():
                if not isinstance(value, (int, float)):
                    raise ValueError(f"Budget '{key}' must be numeric, got {type(value).__name__}")
            
            check = check_performance_budget(metrics, budget, baseline)
            result = {
                "application": params.get("application", "unnamed"),
                "environment": params.get("environment", "unknown"),
                "check": check
            }
            print(format_success(result))
        
        else:
            print(format_error("Either --demo or --params must be provided"))
            sys.exit(1)
    
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except ValueError as e:
        print(format_error(str(e)))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == '__main__':
    main()
