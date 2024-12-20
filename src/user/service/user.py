from argon2 import PasswordHasher

from src.user.repositroy.user import UserRepository
from src.user.schema.register import RegisterDto, RegisterResponse

from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.password_hasher = PasswordHasher()

    async def register_user(self, data: RegisterDto, session: AsyncSession):

        data = data.model_dump(by_alias=True)
        data["password"] = self.password_hasher.hash(data["password"])
        user = await self.repository.create(session, data)

        return RegisterResponse(
            email=user.email,
            message="User successfully registered"
        )

