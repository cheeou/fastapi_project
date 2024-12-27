from src.app.config.db import create_db_and_tables
from src.app.routers import user

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(user.router)

# 애플리케이션 시작 시 테이블 생성
@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

# CORS 설정
origins = [
    "http://localhost:3000",  # Next.js 개발 서버
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
