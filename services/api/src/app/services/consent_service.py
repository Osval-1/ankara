from sqlalchemy.ext.asyncio import AsyncSession

from ..models.enums import Channel


class ConsentService:
    """Handles first-contact consent flow and STOP command processing."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def has_consented(self, channel_id: str, channel: Channel) -> bool:
        raise NotImplementedError

    async def record_consent(self, channel_id: str, channel: Channel, retain_photos: bool = False) -> None:
        raise NotImplementedError

    async def revoke_consent(self, channel_id: str, channel: Channel) -> None:
        """Handles STOP command — deletes farmer record and schedules photo deletion."""
        raise NotImplementedError
