"""Send outbound messages via Telegram Bot API."""

import httpx

from ..config import settings


async def send_telegram_message(chat_id: str, text: str) -> None:
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "MarkdownV2"},
        )
