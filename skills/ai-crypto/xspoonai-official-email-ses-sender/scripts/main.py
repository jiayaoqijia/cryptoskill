#!/usr/bin/env python3
import json
import argparse
import sys
import re
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional

# Try importing boto3 for AWS SES
try:
    import boto3
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False


def format_success(data: Dict[str, Any]) -> str:
    """Format successful result as JSON."""
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details: Optional[Dict[str, Any]] = None) -> str:
    """Format error as JSON."""
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def render_template(template: str, variables: Dict[str, Any]) -> str:
    """Render template with variable substitution."""
    result = template
    for key, value in variables.items():
        placeholder = f"{{{{{key}}}}}"
        result = result.replace(placeholder, str(value))
    return result


def validate_email(email: str) -> bool:
    """Validate email format."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None


def send_email_smtp(to: str, subject: str, body: str, format_type: str = "text",
                   smtp_server: str = None, smtp_port: int = 587, 
                   from_address: str = None, username: str = None, password: str = None) -> Dict[str, Any]:
    """Send email via SMTP server."""
    
    if not from_address:
        from_address = os.environ.get("EMAIL_FROM", "noreply@example.com")
    
    if not smtp_server:
        smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    
    if not username:
        username = os.environ.get("SMTP_USERNAME")
    
    if not password:
        password = os.environ.get("SMTP_PASSWORD")
    
    if not username or not password:
        return {
            "success": False,
            "error": "missing_credentials",
            "message": "SMTP_USERNAME and SMTP_PASSWORD environment variables required"
        }
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = to
        
        # Attach body
        if format_type == "html":
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))
        
        # Send via SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
        
        return {
            "success": True,
            "method": "SMTP",
            "recipient": to,
            "subject": subject,
            "from_address": from_address,
            "smtp_server": smtp_server,
            "status": "sent"
        }
    
    except smtplib.SMTPAuthenticationError:
        return {"success": False, "error": "authentication_failed", "message": "SMTP authentication failed"}
    except Exception as e:
        return {"success": False, "error": "smtp_error", "message": str(e)}


def send_email_ses(to: str, subject: str, body: str, format_type: str = "text",
                  from_address: str = None, charset: str = "UTF-8") -> Dict[str, Any]:
    """Send email via AWS SES."""
    
    if not HAS_BOTO3:
        return {
            "success": False,
            "error": "boto3_not_installed",
            "message": "Run: pip install boto3"
        }
    
    if not from_address:
        from_address = os.environ.get("EMAIL_FROM", "noreply@example.com")
    
    try:
        # Create SES client
        client = boto3.client('ses')
        
        # Send email
        response = client.send_email(
            Source=from_address,
            Destination={'ToAddresses': [to]},
            Message={
                'Subject': {'Data': subject, 'Charset': charset},
                'Body': {
                    'Html' if format_type == 'html' else 'Text': {
                        'Data': body,
                        'Charset': charset
                    }
                }
            }
        )
        
        return {
            "success": True,
            "method": "AWS_SES",
            "recipient": to,
            "subject": subject,
            "message_id": response.get('MessageId', ''),
            "status": "sent"
        }
    
    except Exception as e:
        return {"success": False, "error": "ses_error", "message": str(e)}


def format_email_preview(to: str, subject: str, body: str, format_type: str = "text",
                        template: Optional[str] = None, template_vars: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Format and preview email without sending."""
    
    if template and template_vars:
        body = render_template(body, template_vars)
        subject = render_template(subject, template_vars)
    
    if format_type == "html":
        formatted_body = f"<html><body>{body}</body></html>"
    else:
        formatted_body = body
    
    return {
        "to": to,
        "from": os.environ.get("EMAIL_FROM", "noreply@example.com"),
        "subject": subject,
        "body": formatted_body,
        "format": format_type
    }


def main():
    parser = argparse.ArgumentParser(
        description='Send emails via SMTP or AWS SES with template support'
    )
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            # Demo mode: preview emails (no sending)
            demo_emails = []
            
            # Plain text email
            plain_email = format_email_preview(
                to="user@example.com",
                subject="Welcome to Our Service",
                body="Hello! Thank you for signing up.",
                format_type="text"
            )
            demo_emails.append({"type": "plain_text", "email": plain_email})
            
            # HTML email
            html_email = format_email_preview(
                to="user@example.com",
                subject="Your Order Confirmation",
                body="<h1>Order Confirmed</h1><p>Your order #12345 has been confirmed.</p>",
                format_type="html"
            )
            demo_emails.append({"type": "html", "email": html_email})
            
            # Template email
            template_email = format_email_preview(
                to="john@example.com",
                subject="Hello {{name}}!",
                body="Dear {{name}}, your account balance is ${{balance}}.",
                format_type="text",
                template_vars={"name": "John Doe", "balance": "1,234.56"}
            )
            demo_emails.append({"type": "template", "email": template_email})
            
            result = {
                "demo": True,
                "emails": demo_emails,
                "available_methods": {
                    "SMTP": "Available (requires SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD)",
                    "AWS_SES": "Available" if HAS_BOTO3 else "Requires: pip install boto3"
                }
            }
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            
            to = params.get("to", "")
            subject = params.get("subject", "")
            body = params.get("body", "")
            format_type = params.get("format", "text")
            method = params.get("method", "smtp").upper()
            template_vars = params.get("template_vars", {})
            action = params.get("action", "send")
            
            if not to or not subject or not body:
                raise ValueError("Missing required: to, subject, body")
            
            if not validate_email(to):
                raise ValueError(f"Invalid email: {to}")
            
            # Render template if variables provided
            if template_vars:
                body = render_template(body, template_vars)
                subject = render_template(subject, template_vars)
            
            # Preview action (no sending)
            if action == "preview":
                result = format_email_preview(to, subject, body, format_type, None, template_vars)
                print(format_success(result))
            
            # Send action
            elif action == "send":
                if method == "SES":
                    result = send_email_ses(to, subject, body, format_type)
                else:
                    result = send_email_smtp(to, subject, body, format_type)
                
                if result.get("success"):
                    print(format_success(result))
                else:
                    print(format_error(result.get("error", "unknown_error"), {"message": result.get("message")}))
            
            else:
                raise ValueError(f"Unknown action: {action}")
        
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
