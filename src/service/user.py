from src.config import database
from src.schemas.register import RegisterDto
from src.schemas.user import UserResponse
from src.core.models.repository import UserRepository

from argon2 import PasswordHasher

session = database.async_session_factory

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.password_hasher = PasswordHasher()

    async def register_user(self, data: RegisterDto, _session: session):
        data = data.model_dump(by_alias=True) # JSON type
        data['password'] = self.password_hasher.hash(data['password'])

        user = await self.repository.create(session, **data)

        return UserResponse(
            id=user.id,
            email=user.email,
        )
