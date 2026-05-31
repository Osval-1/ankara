from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base
from .enums import Channel, Language


class Farmer(Base):
    __tablename__ = "farmer"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, init=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))

    channel_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    channel: Mapped[Channel] = mapped_column(PgEnum(Channel, name="channel_enum"), nullable=False)
    region: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None)
    language: Mapped[Language] = mapped_column(PgEnum(Language, name="language_enum"), default=Language.fr)
    consent_given_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    retain_photos: Mapped[bool] = mapped_column(Boolean, default=False)
