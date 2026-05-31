from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base
from .enums import Channel, ConfidenceLevel, Crop, CropClass


class Interaction(Base):
    __tablename__ = "interaction"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, init=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))

    channel: Mapped[Channel] = mapped_column(PgEnum(Channel, name="channel_enum"), nullable=False)
    crop: Mapped[Crop] = mapped_column(PgEnum(Crop, name="crop_enum"), nullable=False)
    predicted_class: Mapped[CropClass] = mapped_column(PgEnum(CropClass, name="cropclass_enum"), nullable=False)
    confidence_raw: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_level: Mapped[ConfidenceLevel] = mapped_column(
        PgEnum(ConfidenceLevel, name="confidencelevel_enum"), nullable=False
    )
    advice_template_version: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    image_ref: Mapped[str | None] = mapped_column(String(512), nullable=True, default=None)
    farmer_id: Mapped[int | None] = mapped_column(ForeignKey("farmer.id"), nullable=True, default=None, init=False)
    region: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None)
    escalated: Mapped[bool] = mapped_column(Boolean, default=False)
    model_version_id: Mapped[int | None] = mapped_column(
        ForeignKey("model_version.id"), nullable=True, default=None, init=False
    )
