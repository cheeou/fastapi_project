from src.app.models.user import User
from src.app.repository.user import UserRepository
from src.app.repository.b_token import TokenBlacklistRepository
from src.app.service.user import UserService


token_blacklist_repository = TokenBlacklistRepository()
user_repository = UserRepository(User)
user_service = UserService(user_repository, token_blacklist_repository)
