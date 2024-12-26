from os import access
from typing import cast

from fastapi import HTTPException, status

from src.app.models.user import User
from src.app.repository.b_token import TokenBlacklistRepository
from src.app.repository.user import UserRepository
from src.app.schemas.login import LoginDto
from src.app.schemas.register import RegisterDto, RegisterResponse
from src.app.config.settings import jwt_settings

from sqlalchemy.ext.asyncio import AsyncSession

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from datetime import datetime, timedelta
from jose import jwt


class UserService:
    def __init__(self, repository: UserRepository, blacklist_repository: TokenBlacklistRepository):
        self.repository = repository
        self.blacklist_repository = blacklist_repository
        self.password_hasher = PasswordHasher()

    async def _is_token_valid(self, token: str, session: AsyncSession) -> bool:
        return not await self.blacklist_repository.is_blacklisted(token, session)

    async def _is_login_valid(self, data: LoginDto, session: AsyncSession) -> User:
        user = await self.repository.get_user_by_email(session, cast(str, data.email))

        if not user:
            raise HTTPException(status_code=404, detail="Please check your email")
        try:
            self.password_hasher.verify(user.password, data.password)
            print("Login successful!")
        except VerifyMismatchError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Please check your account again",
            )
        return user

    async def register_user(self, data: RegisterDto, session: AsyncSession) -> RegisterResponse:

        data = data.model_dump(by_alias=True)
        data["password"] = self.password_hasher.hash(data["password"])
        data.pop("password2", None) # 리팩토링 필요
        user = await self.repository.create(session, data)

        return RegisterResponse(
                email=user.email,
                message="User successfully registered"
        )

    async def login_user(self, data: LoginDto, session: AsyncSession) -> User:
        user = await self._is_login_valid(data=data, session=session)
        print(user.email)

        return user

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expires_delta = datetime.utcnow() + timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expires_delta})
        encoded_jwt = jwt.encode(
            to_encode,
            jwt_settings.SECRET_KEY,
            algorithm=jwt_settings.ALGORITHM
        )
        return encoded_jwt

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expires_delta = datetime.utcnow() + timedelta(days=jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expires_delta})
        encoded_jwt = jwt.encode(
            to_encode,
            jwt_settings.SECRET_KEY,
            algorithm=jwt_settings.ALGORITHM
        )
        return encoded_jwt

    async def refresh_token(self, refresh_token: str, session: AsyncSession) -> str:
        try:
            payload = jwt.decode(refresh_token, jwt_settings.SECRET_KEY, algorithms=[jwt_settings.ALGORITHM])
            email = payload.get("sub")
            if not email:
                raise HTTPException(status_code=401, detail="Invalid refresh token")

            user = await self.repository.get_user_by_email(session, email)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    async def get_current_user(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, jwt_settings.SECRET_KEY, algorithms=[jwt_settings.ALGORITHM])
            user_email = payload.get("sub")
            if user_email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                )
            return {"email": user_email}
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

    async def logout_user(self, token: str, session: AsyncSession):
        await self.blacklist_repository.add_token_to_blacklist(token, session)

