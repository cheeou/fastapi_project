from src.app.config.db import get_async_session, create_db_and_tables, get_user_db
from src.app.dependencies import user_service
from src.app.schemas.register import RegisterDto, RegisterResponse
from src.app.routers import user

from typing import Annotated

from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
app = FastAPI()

app.include_router(user.router)


# 애플리케이션 시작 시 테이블 생성
@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

# 테스트 엔드포인트: DB 연결 확인
@app.get("/test-db")
async def test_db_connection(db: AsyncSession = Depends(get_async_session)):
    try:
        from sqlalchemy import text
        result = await db.execute(text("SELECT 1"))
        row = result.scalar()
        return {"db_status": "connected", "result": row}
    except Exception as e:
        return {"db_status": "error", "detail": str(e)}

# 사용자 관련 엔드포인트 예시
@app.get("/user-db-test")
async def test_user_db(user_db=Depends(get_user_db)):
    return {"user_db_type": str(type(user_db))}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return {"access_token": form_data.username, "token_type": "bearer"}


@app.get("/token/detail")
async def my_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

