"""
Conversation state machine shared by both adapters.

State flow:
    greeting → awaiting_crop → awaiting_photo → (awaiting_consent on first contact) → idle

State is keyed by channel_id and stored in Redis (implementation deferred).
For now, an in-process dict is used so the structure is clear.
"""

from .models import ConversationState, Crop

# TODO: replace with Redis-backed store for multi-instance deployments
_store: dict[str, dict] = {}


def get_state(channel_id: str) -> ConversationState:
    return _store.get(channel_id, {}).get("state", ConversationState.greeting)


def set_state(channel_id: str, state: ConversationState) -> None:
    _store.setdefault(channel_id, {})["state"] = state


def get_crop(channel_id: str) -> Crop | None:
    return _store.get(channel_id, {}).get("crop")


def set_crop(channel_id: str, crop: Crop) -> None:
    _store.setdefault(channel_id, {})["crop"] = crop


def reset(channel_id: str) -> None:
    _store.pop(channel_id, None)
