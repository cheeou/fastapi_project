from fastapi import FastAPI, Depends, HTTPException, status

from typing import Annotated

from src.config.database import async_session_factory
from src.schemas.register import RegisterDto
from src.schemas.user import UserResponse
from src.service.user import UserService



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


@app.post("/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    responses={
        201: {"description": "User created"},
    },
)
async def register(
        data: RegisterDto,
        user_service: Annotated[UserService, Depends(UserService)],
        session: AsyncSession = Depends(get_db),
):
    try:
        return user_service.register_user(session, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))