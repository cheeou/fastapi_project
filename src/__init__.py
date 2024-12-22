from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from src.app.config.db import Base


class User(Base):
    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    email : Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    password : Mapped[str] = mapped_column(String(320), nullable=False)