#!/usr/bin/env python3
import json
import argparse
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import re


# Valid severity levels
SEVERITY_LEVELS = {
    "critical": {"priority": 1, "color": "🔴", "sla_minutes": 15},
    "high": {"priority": 2, "color": "🟠", "sla_minutes": 60},
    "medium": {"priority": 3, "color": "🟡", "sla_minutes": 240},
    "low": {"priority": 4, "color": "🟢", "sla_minutes": 1440}
}

# Valid incident types
INCIDENT_TYPES = ["service_outage", "degradation", "security", "data_loss", "other"]


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details=None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def validate_severity(severity: str) -> bool:
    """Validate incident severity level."""
    return severity.lower() in SEVERITY_LEVELS


def validate_incident_type(incident_type: str) -> bool:
    """Validate incident type."""
    return incident_type.lower() in INCIDENT_TYPES


def calculate_duration(start_time: str, end_time: str) -> str:
    """Calculate duration between two timestamps."""
    try:
        # Try parsing ISO format
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
    except (ValueError, TypeError):
        return "Unknown"
    
    duration = end - start
    hours = duration.total_seconds() // 3600
    minutes = (duration.total_seconds() % 3600) // 60
    
    if hours > 0:
        return f"{int(hours)}h {int(minutes)}m"
    else:
        return f"{int(minutes)}m"


def generate_markdown_report(incident: Dict[str, Any]) -> str:
    """Generate incident report in Markdown format."""
    title = incident.get("title", "Incident Report")
    severity = incident.get("severity", "medium").lower()
    incident_type = incident.get("type", "other")
    impact = incident.get("impact", "")
    affected_systems = incident.get("affected_systems", [])
    timeline = incident.get("timeline", [])
    assigned_team = incident.get("assigned_team", [])
    root_cause = incident.get("root_cause", "")
    resolution_steps = incident.get("resolution_steps", [])
    action_items = incident.get("action_items", [])
    
    severity_info = SEVERITY_LEVELS.get(severity, SEVERITY_LEVELS["medium"])
    
    report = f"""# Incident Report

## {title}

**Severity:** {severity_info['color']} {severity.upper()}  
**Type:** {incident_type}  
**Date Created:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Incident ID:** INC-{datetime.now().strftime("%Y%m%d%H%M%S")}  

## Impact Summary

{impact}

"""
    
    if affected_systems:
        report += f"""## Affected Systems

"""
        for system in affected_systems:
            report += f"- {system}\n"
        report += "\n"
    
    if timeline:
        report += """## Timeline

"""
        for i, event in enumerate(timeline, 1):
            time = event.get("time", "")
            description = event.get("event", "")
            report += f"{i}. **{time}**: {description}\n"
        report += "\n"
    
    if assigned_team:
        report += """## Assigned Team

"""
        for member in assigned_team:
            role = member.get("role", "Team Member") if isinstance(member, dict) else "Team Member"
            name = member.get("name", member) if isinstance(member, dict) else member
            report += f"- {name} ({role})\n"
        report += "\n"
    
    report += """## Root Cause Analysis

"""
    if root_cause:
        report += f"{root_cause}\n\n"
    else:
        report += "[To be determined during investigation]\n\n"
    
    if resolution_steps:
        report += """## Resolution Steps

"""
        for i, step in enumerate(resolution_steps, 1):
            report += f"{i}. {step}\n"
        report += "\n"
    
    if action_items:
        report += """## Action Items

"""
        for item in action_items:
            status = item.get("status", "pending") if isinstance(item, dict) else "pending"
            task = item.get("task", item) if isinstance(item, dict) else item
            owner = item.get("owner", "") if isinstance(item, dict) else ""
            checkbox = "☑" if status == "completed" else "☐"
            owner_str = f" (@{owner})" if owner else ""
            report += f"{checkbox} {task}{owner_str}\n"
        report += "\n"
    
    report += """## Follow-up Notes

[Space for post-incident review and lessons learned]
"""
    
    return report


def generate_structured_report(incident: Dict[str, Any]) -> Dict[str, Any]:
    """Generate structured incident report for programmatic use."""
    severity = incident.get("severity", "medium").lower()
    timeline = incident.get("timeline", [])
    
    # Calculate SLA compliance if start and end times available
    sla_minutes = SEVERITY_LEVELS.get(severity, {}).get("sla_minutes", 240)
    start_time = timeline[0].get("time") if timeline else None
    end_time = timeline[-1].get("time") if timeline else None
    
    return {
        "id": f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "title": incident.get("title", ""),
        "severity": severity,
        "type": incident.get("type", "other"),
        "status": incident.get("status", "open"),
        "created_at": datetime.now().isoformat(),
        "impact": incident.get("impact", ""),
        "affected_systems": incident.get("affected_systems", []),
        "assigned_team": incident.get("assigned_team", []),
        "timeline_count": len(timeline),
        "has_root_cause": bool(incident.get("root_cause")),
        "resolution_steps": len(incident.get("resolution_steps", [])),
        "action_items_total": len(incident.get("action_items", [])),
        "action_items_completed": len([i for i in incident.get("action_items", []) if (i.get("status") if isinstance(i, dict) else False) == "completed"]),
        "sla_minutes": sla_minutes
    }


def main():
    parser = argparse.ArgumentParser(description='Generate structured incident reports with timeline, analysis, and action tracking')
    parser.add_argument('--demo', action='store_true', help='Run with demo incident')
    parser.add_argument('--params', type=str, help='JSON incident parameters')
    parser.add_argument('--format', type=str, choices=['markdown', 'json', 'both'], default='markdown', help='Output format')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            # Demo incident: Service degradation
            demo_incident = {
                "title": "Database Connection Pool Exhaustion",
                "severity": "high",
                "type": "degradation",
                "status": "resolved",
                "impact": "API response times increased to 5+ seconds, affecting user experience. 15% of requests failing with timeouts. Estimated 5000+ users impacted.",
                "affected_systems": [
                    "User API Service",
                    "Order Processing Service",
                    "Payment Gateway Integration",
                    "Database (PostgreSQL Primary)"
                ],
                "assigned_team": [
                    {"name": "Alice Johnson", "role": "Incident Commander"},
                    {"name": "Bob Chen", "role": "Database Engineer"},
                    {"name": "Carol Williams", "role": "Backend Lead"}
                ],
                "timeline": [
                    {"time": "2026-02-07T14:32:00", "event": "Monitoring alert triggered - API response time > 3s"},
                    {"time": "2026-02-07T14:33:15", "event": "Incident escalated to on-call team"},
                    {"time": "2026-02-07T14:35:22", "event": "Database team identified connection pool saturation"},
                    {"time": "2026-02-07T14:38:45", "event": "Increased connection pool size from 100 to 200"},
                    {"time": "2026-02-07T14:42:30", "event": "Response times returned to normal (<500ms)"},
                    {"time": "2026-02-07T14:45:00", "event": "Incident marked as resolved"}
                ],
                "root_cause": "A third-party service integration experienced intermittent failures, causing database connections to remain open longer than expected and exhaust the connection pool. Legacy retry logic was not releasing connections properly.",
                "resolution_steps": [
                    "Identified resource leak in third-party service retry handler",
                    "Increased connection pool size as immediate mitigation",
                    "Implemented connection timeout and cleanup",
                    "Deployed fix to graceful connection closure"
                ],
                "action_items": [
                    {"task": "Review and refactor third-party service integration", "owner": "Bob Chen", "status": "pending"},
                    {"task": "Implement connection pool monitoring and alerts", "owner": "Carol Williams", "status": "pending"},
                    {"task": "Update runbook with troubleshooting steps", "owner": "Alice Johnson", "status": "completed"},
                    {"task": "Schedule postmortem review meeting", "owner": "Alice Johnson", "status": "pending"}
                ]
            }
            
            output = {}
            
            if args.format in ['markdown', 'both']:
                markdown_report = generate_markdown_report(demo_incident)
                output['markdown'] = markdown_report
            
            if args.format in ['json', 'both']:
                structured = generate_structured_report(demo_incident)
                output['structured'] = structured
            
            result = {"demo": True, "incident_id": f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}", **output}
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            
            # Validate required fields
            title = params.get("title", "")
            if not title:
                raise ValueError("'title' is required")
            
            severity = params.get("severity", "medium").lower()
            if not validate_severity(severity):
                raise ValueError(f"Invalid severity. Must be one of: {', '.join(SEVERITY_LEVELS.keys())}")
            
            incident_type = params.get("type", "other").lower()
            if not validate_incident_type(incident_type):
                raise ValueError(f"Invalid incident type. Must be one of: {', '.join(INCIDENT_TYPES)}")
            
            # Build incident object
            incident = {
                "title": title,
                "severity": severity,
                "type": incident_type,
                "status": params.get("status", "open"),
                "impact": params.get("impact", ""),
                "affected_systems": params.get("affected_systems", []),
                "assigned_team": params.get("assigned_team", []),
                "timeline": params.get("timeline", []),
                "root_cause": params.get("root_cause", ""),
                "resolution_steps": params.get("resolution_steps", []),
                "action_items": params.get("action_items", [])
            }
            
            output = {}
            
            if args.format in ['markdown', 'both']:
                markdown_report = generate_markdown_report(incident)
                output['markdown'] = markdown_report
            
            if args.format in ['json', 'both']:
                structured = generate_structured_report(incident)
                output['structured'] = structured
            
            result = {"incident_id": f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}", **output}
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
