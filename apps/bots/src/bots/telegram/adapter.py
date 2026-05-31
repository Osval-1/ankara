"""
Telegram adapter — Bot API webhook → NormalizedMessage → API → formatted reply.

Telegram sends updates as:
  POST /webhooks/telegram
  {"update_id": ..., "message": {"chat": {"id": ...}, "text": "...", "photo": [...]}}
"""

import httpx
from fastapi import APIRouter, Header, HTTPException, Request, Response

from ..api_client import APIClient
from ..config import settings
from ..models import Channel, ConversationState, Crop, Language, NormalizedMessage
from ..reply_formatter import (
    consent_request,
    crop_menu,
    format_telegram,
    greeting,
    send_photo_prompt,
)
from ..state_machine import get_crop, get_state, reset, set_crop, set_state
from .sender import send_telegram_message

router = APIRouter(prefix="/webhooks/telegram", tags=["telegram"])
_api = APIClient()

_CROP_MAP = {"1": Crop.cassava, "2": Crop.maize, "3": Crop.plantain, "4": Crop.tomato, "5": Crop.cocoa}


@router.post("")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(None),
) -> Response:
    if x_telegram_bot_api_secret_token != settings.TELEGRAM_WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid Telegram webhook token")

    payload = await request.json()
    message = payload.get("message", {})
    if not message:
        return Response(status_code=200)

    chat_id = str(message.get("chat", {}).get("id", ""))
    language = Language.fr
    state = get_state(chat_id)

    if "text" in message:
        text = message["text"].strip()
        await _handle_text(chat_id, text, language, state)

    elif "photo" in message:
        photos = message["photo"]
        file_id = photos[-1]["file_id"]  # largest size
        await _handle_photo(chat_id, file_id, language, state)

    return Response(status_code=200)


async def _handle_text(chat_id: str, text: str, language: Language, state: ConversationState) -> None:
    if text.upper() in ("/STOP", "STOP"):
        reset(chat_id)
        return

    if text.startswith("/start") or state in (ConversationState.greeting, ConversationState.idle):
        await send_telegram_message(chat_id, greeting(language.value))
        await send_telegram_message(chat_id, crop_menu(language.value))
        set_state(chat_id, ConversationState.awaiting_crop)

    elif state == ConversationState.awaiting_crop:
        crop = _CROP_MAP.get(text)
        if crop:
            set_crop(chat_id, crop)
            await send_telegram_message(chat_id, send_photo_prompt(language.value))
            set_state(chat_id, ConversationState.awaiting_photo)
        else:
            await send_telegram_message(chat_id, crop_menu(language.value))

    elif state == ConversationState.awaiting_consent:
        if text.upper() in ("OUI", "YES"):
            pass  # ConsentService.record_consent — wired when services are implemented
        set_state(chat_id, ConversationState.idle)


async def _handle_photo(chat_id: str, file_id: str, language: Language, state: ConversationState) -> None:
    if state != ConversationState.awaiting_photo:
        await send_telegram_message(chat_id, crop_menu(language.value))
        set_state(chat_id, ConversationState.awaiting_crop)
        return

    crop = get_crop(chat_id)
    if not crop:
        set_state(chat_id, ConversationState.awaiting_crop)
        return

    # Fetch the photo bytes via Telegram getFile API
    async with httpx.AsyncClient() as client:
        file_info = await client.get(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getFile",
            params={"file_id": file_id},
        )
        file_path = file_info.json()["result"]["file_path"]
        img_response = await client.get(
            f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{file_path}"
        )
        image_bytes = img_response.content

    reply = await _api.diagnose(crop, image_bytes, Channel.telegram.value, language, chat_id)
    await send_telegram_message(chat_id, format_telegram(reply, language.value))
    await send_telegram_message(chat_id, consent_request(language.value))
    set_state(chat_id, ConversationState.awaiting_consent)
