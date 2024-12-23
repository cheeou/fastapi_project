
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from src.app.models.b_token import TokenBlacklist


class TokenBlacklistRepository:
    async def add_token_to_blacklist(self, token: str, session: AsyncSession):
        existing_token = await session.execute(
            select(TokenBlacklist).where(TokenBlacklist.token == token)
        )
        if existing_token.scalars().first():
            return {"message": "Token already blacklisted"}


        new_blacklist_entry = TokenBlacklist(
            token=token,
            created_at=datetime.utcnow(),
            is_valid=False
        )
        session.add(new_blacklist_entry)
        await session.commit()
        return {"message": "Token blacklisted successfully"}

    async def is_blacklisted(self, token: str, session: AsyncSession) -> bool:
        result = await session.execute(
            select(TokenBlacklist).where(TokenBlacklist.token == token)
        )
        blacklist_entry = result.scalars().first()
        return blacklist_entry is not None