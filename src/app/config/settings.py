from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

class DataBaseConfig(BaseModel):
    db: Annotated[str, Field(serialization_alias="path")]
    host: Annotated[str, Field(serialization_alias="host")]
    port: Annotated[int, Field(serialization_alias="port")]
    user: Annotated[str, Field(default="", serialization_alias="username")]
    password: Annotated[str, Field(default="", serialization_alias="password")]

class JWTSettings(BaseModel): # BaseSettings will be applied soon
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))


class Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent.parent.parent.parent
    postgres: DataBaseConfig

    def postgres_dsn(self) -> str:
        print(f"postgres model dump>>>>>>>>{self.postgres.model_dump(by_alias=True)}")
        db_url = str(PostgresDsn.build(scheme="postgresql+asyncpg", **self.postgres.model_dump(by_alias=True)))
        return db_url


    print(base_dir)
    model_config = SettingsConfigDict(
        env_file=str(base_dir / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
        env_nested_delimiter="__",
    )



jwt_settings = JWTSettings()
settings = Settings()
