from src.app.models.user import User
from src.app.repository.user import UserRepository
from src.app.service.user import UserService

from dotenv import load_dotenv

user_repository = UserRepository(User)
user_service = UserService(user_repository)

