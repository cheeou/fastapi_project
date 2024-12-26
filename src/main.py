from src.app.config.db import get_async_session, create_db_and_tables
from src.app.routers import user
from typing import Annotated

from fastapi import FastAPI, Depends

from sqlalchemy.ext.asyncio import AsyncSession
app = FastAPI()
app.include_router(user.router)

# 애플리케이션 시작 시 테이블 생성
@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
