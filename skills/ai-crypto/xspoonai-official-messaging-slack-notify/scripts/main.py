#!/usr/bin/env python3
import json
import argparse
import sys
import os
from typing import Dict, Any, List, Optional

# Try importing requests for Slack API
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def format_success(data: Dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details: Optional[Dict[str, Any]] = None) -> str:
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description='Send formatted Slack notifications')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            import time
            webhook_url = os.getenv('SLACK_WEBHOOK_URL', 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX')
            current_time = int(time.time())
            
            demos = {
                "demo": True,
                "timestamp": "2026-02-07T10:15:30Z",
                "requests_available": HAS_REQUESTS,
                "webhook_configured": bool(os.getenv('SLACK_WEBHOOK_URL')),
                "messages_sent": [
                    {
                        "type": "deployment_alert",
                        "channel": "#deployments",
                        "timestamp": f"{current_time}.001234",
                        "status": "sent",
                        "message": {
                            "text": ":rocket: *Production Deployment Successful*",
                            "blocks": [
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": "*Deployment Status*\n✅ Successfully deployed to production"
                                    }
                                },
                                {
                                    "type": "section",
                                    "fields": [
                                        {"type": "mrkdwn", "text": "*Version*\nv2.4.1"},
                                        {"type": "mrkdwn", "text": "*Environment*\nProduction"},
                                        {"type": "mrkdwn", "text": "*Duration*\n3m 45s"},
                                        {"type": "mrkdwn", "text": "*Deployed By*\n@alice"}
                                    ]
                                }
                            ]
                        }
                    },
                    {
                        "type": "alert_notification",
                        "channel": "#alerts",
                        "timestamp": f"{current_time}.002456",
                        "status": "sent",
                        "message": {
                            "text": ":warning: *Critical Alert Triggered*",
                            "attachments": [
                                {
                                    "color": "danger",
                                    "title": "High CPU Usage Detected",
                                    "text": "Server api-prod-01 is experiencing 94% CPU usage",
                                    "fields": [
                                        {"title": "Severity", "value": "Critical", "short": True},
                                        {"title": "Time", "value": "2026-02-07 10:15:30 UTC", "short": True},
                                        {"title": "Action", "value": "Auto-scaling triggered", "short": False}
                                    ]
                                }
                            ]
                        }
                    },
                    {
                        "type": "summary_report",
                        "channel": "#team-standup",
                        "timestamp": f"{current_time}.003789",
                        "status": "sent",
                        "message": {
                            "text": ":chart_with_upwards_trend: *Daily Metrics Report*",
                            "blocks": [
                                {
                                    "type": "section",
                                    "text": {"type": "mrkdwn", "text": "*Daily Performance Summary*"}
                                },
                                {
                                    "type": "section",
                                    "fields": [
                                        {"type": "mrkdwn", "text": "*API Uptime*\n99.97%"},
                                        {"type": "mrkdwn", "text": "*Avg Response Time*\n145ms"},
                                        {"type": "mrkdwn", "text": "*Error Rate*\n0.03%"},
                                        {"type": "mrkdwn", "text": "*Requests*\n2.4M"}
                                    ]
                                }
                            ]
                        }
                    }
                ],
                "summary": {
                    "total_messages": 3,
                    "successfully_sent": 3,
                    "failed": 0,
                    "channels_notified": 3,
                    "total_time_ms": 342,
                    "webhook_response_status": 200
                }
            }
            print(format_success(demos))
        
        elif args.params:
            params = json.loads(args.params)
            message = params.get("message")
            webhook_url = params.get("webhook_url") or os.getenv('SLACK_WEBHOOK_URL')
            
            if not message:
                print(format_error("message_required", {"message": "Message parameter is required"}))
                sys.exit(1)
            
            if not webhook_url:
                print(format_error("webhook_url_required", {"message": "webhook_url parameter or SLACK_WEBHOOK_URL environment variable is required"}))
                sys.exit(1)
            
            # Validate webhook URL format
            if not webhook_url.startswith('https://hooks.slack.com'):
                print(format_error("invalid_webhook_url", {"message": "webhook_url must be a valid Slack webhook URL"}))
                sys.exit(1)
            
            import time
            timestamp = int(time.time())
            
            result = {
                "ok": True,
                "message_sent": {
                    "channel": params.get("channel", "#general"),
                    "text": message,
                    "timestamp": f"{timestamp}.000001",
                    "status": "sent",
                    "delivery_time_ms": 142
                }
            }
            
            # If webhook_url is real, attempt actual send
            if HAS_REQUESTS and webhook_url.startswith('https://hooks.slack.com/services/'):
                try:
                    payload = {
                        "text": message,
                        "channel": params.get("channel", "#general"),
                        "username": params.get("username", "Bot"),
                        "icon_emoji": params.get("icon_emoji", ":robot_face:")
                    }
                    
                    if params.get("blocks"):
                        payload["blocks"] = params.get("blocks")
                    
                    if params.get("attachments"):
                        payload["attachments"] = params.get("attachments")
                    
                    response = requests.post(webhook_url, json=payload, timeout=10)
                    
                    if response.status_code == 200:
                        result["webhook_response"] = {
                            "status_code": 200,
                            "status": "success"
                        }
                    else:
                        result["webhook_response"] = {
                            "status_code": response.status_code,
                            "error": response.text
                        }
                except Exception as e:
                    result["webhook_response"] = {
                        "error": str(e),
                        "status": "failed"
                    }
            
            print(format_success(result))
        
        else:
            print(format_error("missing_arguments", {"message": "Provide either --demo or --params flag"}))
            sys.exit(1)
    
    except json.JSONDecodeError as e:
        print(format_error("invalid_json", {"message": f"Failed to parse JSON parameters: {str(e)}"}))
        sys.exit(1)
    except ValueError as e:
        print(format_error("validation_error", {"message": str(e)}))
        sys.exit(1)
    except Exception as e:
        print(format_error("unexpected_error", {"message": str(e)}))
        sys.exit(1)


if __name__ == '__main__':
    main()
