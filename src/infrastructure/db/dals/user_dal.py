from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import UserOrm


class UserDal:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(
        self,
        name: str,
        bio: str | None,
        password_hash: str,
    ) -> UserOrm:
        user = UserOrm(name=name, bio=bio, password_hash=password_hash)
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_user_by_name(self, name: str) -> UserOrm | None:
        stmt = select(UserOrm).where(UserOrm.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> UserOrm | None:
        return await self.session.get(UserOrm, user_id)

    async def delete_user(self, user_id: UUID) -> None:
        await self.session.execute(
            delete(UserOrm)
            .where(UserOrm.id == user_id)
        )
