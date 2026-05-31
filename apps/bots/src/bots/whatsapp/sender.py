"""Send outbound messages via 360dialog REST API."""

import httpx

from ..config import settings


async def send_whatsapp_message(to: str, text: str) -> None:
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{settings.WHATSAPP_API_URL}/messages",
            headers={"D360-API-KEY": settings.WHATSAPP_API_KEY},
            json={"recipient_type": "individual", "to": to, "type": "text", "text": {"body": text}},
        )
