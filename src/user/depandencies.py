from fastapi import Depends
from src.user.repositroy.user import UserRepository
from src.user.service.user import UserService

def get_user_repository() -> UserRepository:
    """
    UserRepository 객체를 생성하여 반환.
    """
    return UserRepository()


def get_user_service(
    repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    """
    UserService 객체를 생성하여 반환.
    UserRepository를 주입받아 UserService를 초기화.
    """
    return UserService(repository=repository)