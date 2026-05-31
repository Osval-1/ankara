from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base
from .enums import Crop


class ModelVersion(Base):
    __tablename__ = "model_version"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, init=False)

    crop: Mapped[Crop] = mapped_column(PgEnum(Crop, name="crop_enum"), nullable=False, index=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    dataset_version: Mapped[str] = mapped_column(String(50), nullable=False)
    code_commit: Mapped[str] = mapped_column(String(40), nullable=False)
    accuracy: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)
    ece: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)
    artifact_path: Mapped[str] = mapped_column(String(512), nullable=False)
    deployed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
