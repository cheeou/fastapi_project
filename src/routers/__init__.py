from fastapi import APIRouter
from .user import user_router

# 메인 라우터
api_router = APIRouter()

# 각 라우터를 등록
api_router.include_router(user_router, prefix="/users", tags=["users"])
