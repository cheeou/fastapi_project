from src.app.config.db import get_async_session, create_db_and_tables, get_user_db
from src.app.dependencies import user_service
from src.app.schemas.login import LoginResponse, LoginDto
from src.app.schemas.register import RegisterDto, RegisterResponse

from fastapi import FastAPI, Depends, status, HTTPException, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.post(
    "/register",
    response_model=RegisterResponse,  # 반환할 데이터의 스키마
    status_code=status.HTTP_201_CREATED,
    responses={201: {"description": "User successfully registered"}},
)
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

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    responses={201: {"description": "User successfully logged in"}},
)
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