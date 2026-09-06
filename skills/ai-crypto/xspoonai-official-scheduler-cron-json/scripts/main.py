#!/usr/bin/env python3
import json
import argparse
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# Try importing croniter for real cron parsing
try:
    from croniter import croniter
    HAS_CRONITER = True
except ImportError:
    HAS_CRONITER = False


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details: Optional[Dict[str, Any]] = None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def validate_cron_expression(cron_expr: str) -> bool:
    """Validate cron expression format using croniter if available."""
    if HAS_CRONITER:
        try:
            croniter(cron_expr)
            return True
        except:
            return False
    else:
        # Fallback validation
        parts = cron_expr.split()
        if len(parts) != 5:
            return False
        
        ranges = [(0, 59), (0, 23), (1, 31), (1, 12), (0, 6)]
        
        for part, (min_val, max_val) in zip(parts, ranges):
            if part == '*' or part == '?':
                continue
            try:
                if ',' in part or '-' in part or '/' in part:
                    continue
                val = int(part)
                if not (min_val <= val <= max_val):
                    return False
            except ValueError:
                pass
        
        return True


def calculate_next_runs(cron_expr: str, count: int = 5) -> List[str]:
    """Calculate next N execution times using croniter if available."""
    next_runs = []
    
    if HAS_CRONITER:
        try:
            cron = croniter(cron_expr, datetime.now())
            for _ in range(count):
                next_time = cron.get_next(datetime)
                next_runs.append(next_time.isoformat())
            return next_runs
        except:
            pass
    
    # Fallback: simplified calculation
    parts = cron_expr.split()
    if len(parts) >= 2:
        try:
            minute = int(parts[0]) if parts[0] != '*' else None
            hour = int(parts[1]) if parts[1] != '*' else None
            
            current = datetime.now()
            
            for i in range(count):
                if minute is not None and hour is not None:
                    next_time = current.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    if next_time <= current:
                        next_time += timedelta(days=1)
                    else:
                        next_time += timedelta(days=i)
                elif minute is not None:
                    next_time = current.replace(minute=minute, second=0, microsecond=0)
                    if next_time <= current:
                        next_time += timedelta(hours=1)
                    else:
                        next_time += timedelta(hours=i)
                elif hour is not None:
                    next_time = current.replace(hour=hour, minute=0, second=0, microsecond=0)
                    if next_time <= current:
                        next_time += timedelta(days=1)
                    else:
                        next_time += timedelta(days=i)
                else:
                    next_time = current + timedelta(minutes=i+1)
                
                next_runs.append(next_time.isoformat())
        except:
            pass
    
    return next_runs


def get_cron_description(cron_expr: str) -> str:
    """Generate human-readable description of cron expression."""
    parts = cron_expr.split()
    if len(parts) < 5:
        return "Invalid cron expression"
    
    minute, hour, day, month, weekday = parts
    
    descriptions = []
    
    # Weekday mapping
    weekdays = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 
                4: "Thursday", 5: "Friday", 6: "Saturday"}
    
    # Month mapping
    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
              7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    
    # Build description
    if minute == "*":
        minute_desc = "every minute"
    else:
        minute_desc = f"at {minute} minutes"
    
    if hour == "*":
        time_desc = minute_desc
    else:
        time_desc = f"at {hour}:{minute}" if minute != "*" else f"at {hour}:00"
    
    if weekday != "*" and weekday != "?":
        try:
            wd = int(weekday)
            time_desc += f" on {weekdays.get(wd, 'custom day')}"
        except:
            pass
    
    if day != "*" and day != "?":
        try:
            d = int(day)
            time_desc += f" on day {d}"
        except:
            pass
    
    return time_desc


def main():
    parser = argparse.ArgumentParser(description='JSON-based cron scheduler with croniter support')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            examples = [
                {"cron": "0 9 * * 1-5", "description": "Every weekday at 9 AM"},
                {"cron": "*/15 * * * *", "description": "Every 15 minutes"},
                {"cron": "0 0 1 * *", "description": "First day of month at midnight"},
                {"cron": "0 2 * * 0", "description": "Every Sunday at 2 AM"},
                {"cron": "30 */4 * * *", "description": "Every 4 hours at 30 minutes"}
            ]
            
            results = []
            for ex in examples:
                is_valid = validate_cron_expression(ex["cron"])
                next_runs = calculate_next_runs(ex["cron"], 3) if is_valid else []
                desc = get_cron_description(ex["cron"]) if is_valid else "Invalid"
                results.append({
                    "cron_expression": ex["cron"],
                    "description": desc,
                    "valid": is_valid,
                    "next_executions": next_runs
                })
            
            info = {
                "demo": True,
                "croniter_available": HAS_CRONITER,
                "examples": results
            }
            print(format_success(info))
        
        elif args.params:
            params = json.loads(args.params)
            cron_expr = params.get("cron_expression", "")
            next_runs_count = params.get("next_runs", 5)
            
            if not cron_expr:
                raise ValueError("cron_expression is required")
            
            is_valid = validate_cron_expression(cron_expr)
            
            if not is_valid:
                raise ValueError(f"Invalid cron expression: {cron_expr}")
            
            next_runs = calculate_next_runs(cron_expr, next_runs_count)
            description = get_cron_description(cron_expr)
            
            result = {
                "cron_expression": cron_expr,
                "description": description,
                "valid": True,
                "next_executions": next_runs,
                "using_croniter": HAS_CRONITER
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
        print(format_error(f"Unexpected error: {e}", {"error_type": "processing"}))
        sys.exit(1)


if __name__ == '__main__':
    main()
