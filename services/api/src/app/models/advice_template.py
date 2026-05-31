from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, ENUM as PgEnum
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base
from .enums import Crop, CropClass, Language


class AdviceTemplate(Base):
    __tablename__ = "advice_template"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, init=False)

    crop: Mapped[Crop] = mapped_column(PgEnum(Crop, name="crop_enum"), nullable=False)
    crop_class: Mapped[CropClass] = mapped_column(PgEnum(CropClass, name="cropclass_enum"), nullable=False)
    language: Mapped[Language] = mapped_column(PgEnum(Language, name="language_enum"), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    opening: Mapped[str] = mapped_column(Text, nullable=False)
    steps: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)
    consult_message: Mapped[str] = mapped_column(Text, nullable=False)
    reviewed_by: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
