from typing import Any, TypeVar, Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.models.user import User

T = TypeVar("T", bound=DeclarativeBase) # DeclarativeBase 상속 클래스 T

class BaseRepository[T]:
    def __init__(self, model: Type[T]):
        self.model = model # 사용할 sqla 모델 지정

    async def create(self, session: AsyncSession, **kwargs: Any) -> T:
        entity = self.model(**kwargs)
        session.add(entity)
        await session.commit()
        await session.refresh(entity)
        return entity

class UserCreateRepository(BaseRepository[User]):

    pass


class UserRepository(UserCreateRepository):
    pass