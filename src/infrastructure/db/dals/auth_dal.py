from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import RefreshTokenOrm


class AuthDal:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_refresh_token(self, user_id: UUID, expire_at: datetime) -> RefreshTokenOrm:
        token = RefreshTokenOrm(user_id=user_id, expire_at=expire_at)
        self.session.add(token)
        await self.session.flush()
        return token

    async def get_refresh_token_by_token(self, token: UUID) -> RefreshTokenOrm | None:
        return await self.session.get(RefreshTokenOrm, token)

    async def delete_refresh_token_by_token(self, token: UUID) -> None:
        await self.session.execute(
            delete(RefreshTokenOrm).where(RefreshTokenOrm.token == token)
        )

    async def delete_refresh_tokens_by_user(self, user_id: UUID) -> None:
        await self.session.execute(
            delete(RefreshTokenOrm).where(RefreshTokenOrm.user_id == user_id)
        )
