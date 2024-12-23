from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from src.app.config.db import Base

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    token : Mapped[str] = mapped_column(String, primary_key=True, index=True)
    created_at : Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    is_valid : Mapped[bool] = mapped_column(Boolean, default=False)