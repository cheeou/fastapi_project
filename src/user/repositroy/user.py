from sqlalchemy.ext.asyncio import AsyncSession
from src.user.model.user import User
from src.user.schema.register import RegisterDto

class UserRepository:
    async def create(self, session: AsyncSession, data: dict) -> User:
        user = User(**data)

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user
