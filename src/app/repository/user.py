from http.client import HTTPException
from typing import Type, Optional

from fastapi import HTTPException, status

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.user import User

class UserRepository:
    def __init__(self, model: Type[User]):
        self.model = model

    async def get_user_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first() # mappings() : return 'dict' , scalars().first() : return SQLAlchemy ORM instance
        if user:
            print(f"Loaded user email: {user.email}")  # 속성 접근 확인
        return user
    async def create(self, session: AsyncSession, data: dict) -> User:

        existing_user = await self.get_user_by_email(session, data['email'])
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered"
            )

        user = User(**data)

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user