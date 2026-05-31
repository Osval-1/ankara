"""360dialog webhook signature verification."""

import hashlib
import hmac

from fastapi import HTTPException, Request

from ..config import settings


async def verify_signature(request: Request) -> bytes:
    """Raise 403 if the D360-Signature header doesn't match the payload HMAC."""
    body = await request.body()
    expected = hmac.new(
        settings.WHATSAPP_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256,
    ).hexdigest()
    received = request.headers.get("D360-Signature", "")
    if not hmac.compare_digest(expected, received):
        raise HTTPException(status_code=403, detail="Invalid webhook signature")
    return body
