from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.app.config.settings import settings


DATABASE_URL = settings.postgres_dsn()

# Base 클래스 정의
class Base(DeclarativeBase):
    pass

# SQLAlchemy 비동기 엔진 및 세션 팩토리 생성
engine = create_async_engine(DATABASE_URL, pool_size=5, max_overflow=10, pool_timeout=30, pool_recycle=3600, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# 테이블 생성 함수
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully.")

# 비동기 세션 생성 함수
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
