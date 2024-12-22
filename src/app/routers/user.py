from src.app.config.db import get_async_session
from src.app.dependencies import user_service
from src.app.schemas.login import LoginDto
from src.app.schemas.register import RegisterDto

from fastapi import Depends, status, HTTPException, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED,)
async def register(
    data: RegisterDto,  # 입력 데이터 (DTO)
    db: AsyncSession = Depends(get_async_session),  # 비동기 세션  # UserService 주입
):
    try:
        return await user_service.register_user(data, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
        data: LoginDto,
        db: AsyncSession = Depends(get_async_session),
):
    try:
        return await user_service.login_user(data, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )




