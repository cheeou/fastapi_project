from src.app.config.db import get_async_session
from src.app.dependencies import user_service
from src.app.schemas.login import LoginDto
from src.app.schemas.register import RegisterDto

from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return {"access_token": form_data.username, "token_type": "bearer"}
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
        data: LoginDto,
        db: AsyncSession = Depends(get_async_session),
):
    try:
        user =  await user_service.login_user(data, db)
        token_data = {"sub": user.email}
        access_token = user_service.create_access_token(token_data)
        refresh_token = user_service.create_refresh_token(token_data)

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(
    refresh_token: str,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        user = await user_service.refresh_token(refresh_token, session)
        token_data = {"sub": user.email}
        access_token = user_service.create_access_token(token_data)
        refresh_token = user_service.create_refresh_token(token_data)

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
@router.get("/profile", status_code=status.HTTP_200_OK)
async def get_profile(
    current_user: dict = Depends(user_service.get_current_user),
):
    return {"email": current_user["email"]}

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session),
):
    await user_service.logout_user(token, session)
    return {"message": "Logged out successfully"}