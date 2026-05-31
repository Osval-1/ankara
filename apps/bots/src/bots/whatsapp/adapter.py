"""
WhatsApp adapter — 360dialog webhook → NormalizedMessage → API → formatted reply.

360dialog sends messages as:
  POST /webhooks/whatsapp
  {
    "messages": [{"from": "<phone>", "type": "text"|"image", "text": {"body": "..."}, ...}]
  }
"""

import httpx
from fastapi import APIRouter, Depends, Request, Response

from ..api_client import APIClient
from ..models import Channel, ConversationState, Crop, Language, NormalizedMessage
from ..reply_formatter import (
    consent_request,
    crop_menu,
    format_whatsapp,
    greeting,
    send_photo_prompt,
)
from ..state_machine import get_crop, get_state, reset, set_crop, set_state
from .sender import send_whatsapp_message
from .signature import verify_signature

router = APIRouter(prefix="/webhooks/whatsapp", tags=["whatsapp"])
_api = APIClient()

_CROP_MAP = {"1": Crop.cassava, "2": Crop.maize, "3": Crop.plantain, "4": Crop.tomato, "5": Crop.cocoa}


def _parse_language(phone: str) -> Language:
    # Default to French for Cameroon numbers; extend with region mapping later
    return Language.fr


@router.post("")
async def whatsapp_webhook(request: Request, body: bytes = Depends(verify_signature)) -> Response:
    import json
    payload = json.loads(body)
    messages = payload.get("messages", [])

    for msg in messages:
        channel_id = msg.get("from", "")
        language = _parse_language(channel_id)
        state = get_state(channel_id)
        msg_type = msg.get("type", "")

        if msg_type == "text":
            text = msg.get("text", {}).get("body", "").strip()
            await _handle_text(channel_id, text, language, state)

        elif msg_type == "image":
            image_url = msg.get("image", {}).get("link", "")
            await _handle_image(channel_id, image_url, language, state)

    return Response(status_code=200)


async def _handle_text(channel_id: str, text: str, language: Language, state: ConversationState) -> None:
    if text.upper() == "STOP":
        reset(channel_id)
        return

    if state == ConversationState.greeting or state == ConversationState.idle:
        await send_whatsapp_message(channel_id, greeting(language.value))
        await send_whatsapp_message(channel_id, crop_menu(language.value))
        set_state(channel_id, ConversationState.awaiting_crop)

    elif state == ConversationState.awaiting_crop:
        crop = _CROP_MAP.get(text)
        if crop:
            set_crop(channel_id, crop)
            await send_whatsapp_message(channel_id, send_photo_prompt(language.value))
            set_state(channel_id, ConversationState.awaiting_photo)
        else:
            await send_whatsapp_message(channel_id, crop_menu(language.value))

    elif state == ConversationState.awaiting_consent:
        if text.upper() in ("OUI", "YES"):
            pass  # ConsentService.record_consent — implemented when services are wired
        set_state(channel_id, ConversationState.idle)


async def _handle_image(channel_id: str, image_url: str, language: Language, state: ConversationState) -> None:
    if state != ConversationState.awaiting_photo:
        await send_whatsapp_message(channel_id, crop_menu(language.value))
        set_state(channel_id, ConversationState.awaiting_crop)
        return

    crop = get_crop(channel_id)
    if not crop:
        set_state(channel_id, ConversationState.awaiting_crop)
        return

    async with httpx.AsyncClient() as client:
        img_response = await client.get(image_url)
        image_bytes = img_response.content

    reply = await _api.diagnose(crop, image_bytes, Channel.whatsapp.value, language, channel_id)
    await send_whatsapp_message(channel_id, format_whatsapp(reply, language.value))
    await send_whatsapp_message(channel_id, consent_request(language.value))
    set_state(channel_id, ConversationState.awaiting_consent)
