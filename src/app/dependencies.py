from src.app.models.user import User
from src.app.repository.user import UserRepository
from src.app.service.user import UserService
from src.app.service.token import TokenService

from dotenv import load_dotenv

token_service = TokenService()
user_repository = UserRepository(User)
user_service = UserService(user_repository, token_service)

