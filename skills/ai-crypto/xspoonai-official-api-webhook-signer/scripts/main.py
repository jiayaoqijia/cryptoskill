#!/usr/bin/env python3
import json
import argparse
import hmac
import hashlib
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List


def format_success(data: Dict[str, Any]) -> str:
    """Format successful result as JSON."""
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error: str, details: Optional[Dict[str, Any]] = None) -> str:
    """Format error as JSON."""
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def sign_webhook(payload: Dict[str, Any], secret: str) -> str:
    """Generate HMAC-SHA256 signature for webhook payload.
    
    Args:
        payload: Webhook payload dictionary
        secret: Secret key for signing
        
    Returns:
        Hex-encoded HMAC signature
    """
    payload_str = json.dumps(payload, sort_keys=True)
    signature = hmac.new(
        secret.encode('utf-8'),
        payload_str.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return signature


def verify_webhook(payload: Dict[str, Any], secret: str, signature: str) -> bool:
    """Verify HMAC-SHA256 signature for webhook payload.
    
    Args:
        payload: Webhook payload dictionary
        secret: Secret key for verification
        signature: Signature to verify
        
    Returns:
        True if signature is valid, False otherwise
    """
    expected_signature = sign_webhook(payload, secret)
    return hmac.compare_digest(expected_signature, signature)


def calculate_retry_delays(max_attempts: int, base_delay: int, multiplier: float) -> List[Dict[str, Any]]:
    """Calculate retry delays using exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        base_delay: Base delay in seconds
        multiplier: Exponential backoff multiplier
        
    Returns:
        List of retry schedule entries
    """
    retry_queue = []
    for attempt in range(1, max_attempts + 1):
        delay = base_delay * (multiplier ** (attempt - 1))
        next_retry = datetime.now(datetime.UTC if hasattr(datetime, 'UTC') else None) + timedelta(seconds=delay)
        if next_retry.tzinfo is None:
            next_retry = next_retry.replace(tzinfo=None)
            retry_str = next_retry.isoformat() + "Z"
        else:
            retry_str = next_retry.isoformat()
        retry_queue.append({
            "attempt": attempt,
            "delay_seconds": delay,
            "next_retry": retry_str
        })
    return retry_queue


def execute_webhook_signer(params: Dict[str, Any]) -> Dict[str, Any]:
    """Execute webhook signer functionality.
    
    Args:
        params: Input parameters
        
    Returns:
        Result data dictionary
    """
    action = params.get("action", "sign")
    payload = params.get("payload", {})
    secret = params.get("secret", "")
    
    if not secret:
        raise ValueError("Secret key is required")
    
    if action == "sign":
        signature = sign_webhook(payload, secret)
        result = {
            "action": "sign",
            "signature": signature,
            "payload": payload
        }
        
        # Add retry queue if requested
        retry_config = params.get("retry_config")
        if retry_config:
            max_attempts = retry_config.get("max_attempts", 3)
            base_delay = retry_config.get("base_delay", 1)
            multiplier = retry_config.get("backoff_multiplier", 2)
            result["retry_queue"] = calculate_retry_delays(max_attempts, base_delay, multiplier)
        
        return result
    
    elif action == "verify":
        signature = params.get("signature", "")
        if not signature:
            raise ValueError("Signature is required for verification")
        
        is_valid = verify_webhook(payload, secret, signature)
        return {
            "action": "verify",
            "valid": is_valid,
            "payload": payload
        }
    
    else:
        raise ValueError(f"Unknown action: {action}. Use 'sign' or 'verify'")


def main():
    parser = argparse.ArgumentParser(
        description='Generate and verify signed webhooks with retry queue'
    )
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    parser.add_argument('--params', type=str, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        if args.demo:
            # Demo mode: sign a webhook and verify it
            demo_payload = {"event": "user.created", "user_id": 12345, "timestamp": "2026-02-06T10:00:00Z"}
            demo_secret = "demo_secret_key_12345"
            
            # Sign the webhook
            signature = sign_webhook(demo_payload, demo_secret)
            
            # Verify the signature
            is_valid = verify_webhook(demo_payload, demo_secret, signature)
            
            # Generate retry queue
            retry_queue = calculate_retry_delays(3, 1, 2)
            
            result = {
                "demo": True,
                "signed_webhook": {
                    "payload": demo_payload,
                    "signature": signature,
                    "secret": demo_secret
                },
                "verification": {
                    "valid": is_valid
                },
                "retry_queue": retry_queue
            }
            print(format_success(result))
        
        elif args.params:
            params = json.loads(args.params)
            result = execute_webhook_signer(params)
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
