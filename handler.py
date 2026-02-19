"""
PL202 – Serverless Event Processing (Local Lambda Simulation)
Day 1 (45 min) – Individual Task
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
import re


ALLOWED_TYPES = {"USER_SIGNUP", "PAYMENT", "FILE_UPLOAD"}
ALLOWED_PLANS = {"free", "pro", "edu"}
ALLOWED_CURRENCIES = {"BHD", "USD", "EUR"}


def _err(*msgs: str) -> Dict[str, Any]:
    """Create a standard error response."""
    return {
        "status": "error",
        "message": "Event rejected",
        "data": None,
        "errors": list(msgs),
    }


def _ok(message: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a standard ok response."""
    return {
        "status": "ok",
        "message": message,
        "data": data,
        "errors": [],
    }


def _is_email(value: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value))


def handler(event: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Main Lambda-style handler."""
    # TODO 1: Validate event is a dict and has 'type' field
    if not isinstance(event, dict):
        return _err("Event must be a JSON object (dict), not a list or other type")

    if "type" not in event:
        return _err("Missing required field: 'type'")

    # TODO 2: Ensure event['type'] is one of ALLOWED_TYPES
    event_type = event["type"]
    if event_type not in ALLOWED_TYPES:
        return _err(f"Unknown event type: '{event_type}'. Allowed: {', '.join(sorted(ALLOWED_TYPES))}")

    # TODO 3: Route to a per-type function
    if event_type == "USER_SIGNUP":
        return handle_user_signup(event)
    elif event_type == "PAYMENT":
        return handle_payment(event)
    elif event_type == "FILE_UPLOAD":
        return handle_file_upload(event)


def handle_user_signup(event: Dict[str, Any]) -> Dict[str, Any]:
    """Process USER_SIGNUP events."""
    errors = []

    # TODO 5: Validate required fields and types
    user_id = event.get("user_id")
    email = event.get("email")
    plan = event.get("plan")

    if user_id is None:
        errors.append("Missing required field: 'user_id'")
    elif not isinstance(user_id, int):
        errors.append("'user_id' must be an integer")

    if email is None:
        errors.append("Missing required field: 'email'")
    elif not isinstance(email, str):
        errors.append("'email' must be a string")
    else:
        # TODO 6: Validate email format
        if not _is_email(email):
            errors.append(f"Invalid email format: '{email}'")

    if plan is None:
        errors.append("Missing required field: 'plan'")
    elif not isinstance(plan, str):
        errors.append("'plan' must be a string")
    else:
        # TODO 7: Validate plan is allowed (normalize first)
        if plan.lower() not in ALLOWED_PLANS:
            errors.append(f"Invalid plan: '{plan}'. Allowed: {', '.join(sorted(ALLOWED_PLANS))}")

    if errors:
        return _err(*errors)

    # TODO 8: Build normalized output data
    normalized_email = email.lower()
    normalized_plan = plan.lower()

    return _ok("Signup processed", {
        "user_id": user_id,
        "email": normalized_email,
        "plan": normalized_plan,
        "welcome_email_subject": f"Welcome to the {normalized_plan} plan!",
    })


def handle_payment(event: Dict[str, Any]) -> Dict[str, Any]:
    """Process PAYMENT events."""
    errors = []

    # TODO 9: Validate required fields and types
    payment_id = event.get("payment_id")
    user_id = event.get("user_id")
    amount = event.get("amount")
    currency = event.get("currency")

    if payment_id is None:
        errors.append("Missing required field: 'payment_id'")
    elif not isinstance(payment_id, str):
        errors.append("'payment_id' must be a string")

    if user_id is None:
        errors.append("Missing required field: 'user_id'")
    elif not isinstance(user_id, int):
        errors.append("'user_id' must be an integer")

    if amount is None:
        errors.append("Missing required field: 'amount'")
    elif not isinstance(amount, (int, float)):
        errors.append("'amount' must be a number")
    else:
        # TODO 10: Validate amount > 0
        if amount <= 0:
            errors.append(f"'amount' must be greater than 0, got {amount}")

    if currency is None:
        errors.append("Missing required field: 'currency'")
    elif not isinstance(currency, str):
        errors.append("'currency' must be a string")
    else:
        # TODO 11: Validate currency allowed (normalize first)
        if currency.upper() not in ALLOWED_CURRENCIES:
            errors.append(f"Invalid currency: '{currency}'. Allowed: {', '.join(sorted(ALLOWED_CURRENCIES))}")

    if errors:
        return _err(*errors)

    # TODO 12: Compute fee and net_amount
    normalized_amount = round(float(amount), 3)
    normalized_currency = currency.upper()
    fee = round(0.02 * normalized_amount, 3)
    net_amount = round(normalized_amount - fee, 3)

    return _ok("Payment processed", {
        "payment_id": payment_id,
        "user_id": user_id,
        "amount": normalized_amount,
        "currency": normalized_currency,
        "fee": fee,
        "net_amount": net_amount,
    })


def handle_file_upload(event: Dict[str, Any]) -> Dict[str, Any]:
    """Process FILE_UPLOAD events."""
    errors = []

    # TODO 13: Validate required fields and types
    file_name = event.get("file_name")
    size_bytes = event.get("size_bytes")
    bucket = event.get("bucket")
    uploader = event.get("uploader")

    if file_name is None:
        errors.append("Missing required field: 'file_name'")
    elif not isinstance(file_name, str):
        errors.append("'file_name' must be a string")

    if size_bytes is None:
        errors.append("Missing required field: 'size_bytes'")
    elif not isinstance(size_bytes, int):
        errors.append("'size_bytes' must be an integer")
    elif size_bytes < 0:
        errors.append("'size_bytes' must be >= 0")

    if bucket is None:
        errors.append("Missing required field: 'bucket'")
    elif not isinstance(bucket, str):
        errors.append("'bucket' must be a string")

    if uploader is None:
        errors.append("Missing required field: 'uploader'")
    elif not isinstance(uploader, str):
        errors.append("'uploader' must be a string")
    else:
        # TODO 14: Validate uploader email
        if not _is_email(uploader):
            errors.append(f"Invalid uploader email: '{uploader}'")

    if errors:
        return _err(*errors)

    # Normalize
    normalized_file_name = file_name.strip()
    normalized_bucket = bucket.lower()
    normalized_uploader = uploader.lower()

    # TODO 15: Compute storage_class
    if size_bytes < 1_000_000:
        storage_class = "STANDARD"
    elif size_bytes < 50_000_000:
        storage_class = "STANDARD_IA"
    else:
        storage_class = "GLACIER"

    return _ok("Upload processed", {
        "file_name": normalized_file_name,
        "size_bytes": size_bytes,
        "bucket": normalized_bucket,
        "uploader": normalized_uploader,
        "storage_class": storage_class,
    })
