#!/usr/bin/env python3
import json
import argparse
import sys
import re
from typing import Dict, Any, List, Optional


def format_success(data: Dict[str, Any]) -> str:
    """Format successful result as JSON."""
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details: Optional[Dict[str, Any]] = None) -> str:
    """Format error as JSON."""
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def parse_logfile(log_content: str, pattern: str, threshold: int = 0) -> Dict[str, Any]:
    """Parse log file and find pattern matches.
    
    Args:
        log_content: Log file content
        pattern: Regex pattern to match
        threshold: Alert threshold (trigger if matches >= threshold)
        
    Returns:
        Dictionary with matches and alert status
    """
    try:
        regex = re.compile(pattern)
    except re.error as e:
        raise ValueError(f"Invalid regex pattern: {e}")
    
    matches = []
    lines = log_content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        if regex.search(line):
            matches.append({
                "line_number": line_num,
                "content": line.strip()
            })
    
    match_count = len(matches)
    alert_triggered = match_count >= threshold if threshold > 0 else False
    
    return {
        "matches": matches,
        "match_count": match_count,
        "alert_triggered": alert_triggered,
        "threshold": threshold
    }


def main():
    parser = argparse.ArgumentParser(
        description='Parse log files and trigger alerts on patterns'
    )
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            # Demo log content
            demo_log = """2026-02-06 10:00:01 INFO Server started successfully
2026-02-06 10:00:15 INFO User login: alice@example.com
2026-02-06 10:01:23 WARNING High memory usage detected: 85%
2026-02-06 10:02:45 ERROR Database connection failed: timeout
2026-02-06 10:03:12 INFO User login: bob@example.com
2026-02-06 10:04:33 ERROR Failed to process payment: insufficient funds
2026-02-06 10:05:21 CRITICAL System overload - rejecting requests
2026-02-06 10:06:45 ERROR API rate limit exceeded
2026-02-06 10:07:12 INFO User logout: alice@example.com
2026-02-06 10:08:33 WARNING Disk space low: 15% remaining"""
            
            # Test different patterns
            results = {}
            
            # Pattern 1: All ERROR messages
            results["errors"] = parse_logfile(demo_log, r"ERROR", threshold=2)
            
            # Pattern 2: WARNING or CRITICAL
            results["warnings_critical"] = parse_logfile(demo_log, r"WARNING|CRITICAL", threshold=3)
            
            # Pattern 3: Failed operations
            results["failures"] = parse_logfile(demo_log, r"[Ff]ailed", threshold=1)
            
            result = {
                "demo": True,
                "log_lines": len(demo_log.split('\n')),
                "patterns_tested": results
            }
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            
            log_file = params.get("log_file", "")
            log_content = params.get("log_content", "")
            pattern = params.get("pattern", "")
            threshold = params.get("threshold", 0)
            
            if not pattern:
                raise ValueError("Pattern is required")
            
            # Read log file if provided
            if log_file and not log_content:
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        log_content = f.read()
                except FileNotFoundError:
                    raise ValueError(f"Log file not found: {log_file}")
                except Exception as e:
                    raise ValueError(f"Error reading log file: {e}")
            
            if not log_content:
                raise ValueError("Either log_file or log_content is required")
            
            result = parse_logfile(log_content, pattern, threshold)
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
        print(format_error(f"Unexpected error: {e}", {"error_type": "processing"}))
        sys.exit(1)


if __name__ == '__main__':
    main()
