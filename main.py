from fastapi import FastAPI, Depends, HTTPException, status

from typing import Annotated

from src.config.db import async_session_factory
from src.user.depandencies import get_user_service
from src.user.schema.register import RegisterDto, RegisterResponse
from src.user.service.user import UserService
app = FastAPI()


AsyncSession  = async_session_factory()

async def get_db() -> AsyncSession:
    async with async_session_factory() as session:
        yield session

@app.get("/test-db")
async def test_db_connection(db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        from sqlalchemy import text
        result = await db.execute(text("SELECT 1"))
        row = result.scalar()
        return {"db_status": "connected", "result": row}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection failed",
        )

@app.post("/register", response_model=RegisterResponse)
async def register(
    data: RegisterDto,
    session: AsyncSession = Depends(get_db),  # DB 세션 주입
    user_service: UserService = Depends(get_user_service),  # UserService 주입
):
    return await user_service.register_user(data, session)