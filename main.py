from fastapi import FastAPI, Depends, HTTPException, status

from typing import Annotated

from database import async_session_factory
app = FastAPI()

AsyncSession  = async_session_factory()

async def get_db():
    async with AsyncSession:
        yield AsyncSession

@app.get("/test-db")
async def test_db_connection(db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        from sqlalchemy import text
        result = await db.execute(text("SELECT 1"))
        row = result.scalar()
        return {"db_status": "connected", "result": row}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection failed",
        )
