from fastapi import APIRouter, Request, Response

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request) -> Response:
    """360dialog webhook. Signature verification + message routing goes here."""
    raise NotImplementedError


@router.post("/telegram")
async def telegram_webhook(request: Request) -> Response:
    """Telegram Bot API webhook. Token validation + message routing goes here."""
    raise NotImplementedError
