from typing import cast

from fastapi import HTTPException, status

from src.app.repository.user import UserRepository
from src.app.schemas.login import LoginDto, LoginResponse
from src.app.schemas.register import RegisterDto, RegisterResponse

from sqlalchemy.ext.asyncio import AsyncSession

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from datetime import datetime, timedelta
from jose import jwt

from dotenv import load_dotenv

import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.password_hasher = PasswordHasher()

    def issue_token(self, data: dict):
        to_encode = data.copy()
        expire_data = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire_data})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    async def _is_login_valid(self, data: LoginDto, session: AsyncSession):
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

    async def login_user(self, data: LoginDto, session: AsyncSession) -> LoginResponse:

        user = await self._is_login_valid(data=data, session=session)

        return LoginResponse(
            email=user.email,
            message="User successfully logged in"
        )