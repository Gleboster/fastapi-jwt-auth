from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db import async_session_factory, AuthDal, UserDal


async def get_async_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session
        await session.commit()


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]

def get_auth_dal(session: AsyncSessionDep) -> AuthDal:
    return AuthDal(session)

AuthDalDep = Annotated[AuthDal, Depends(get_auth_dal)]
def get_user_dal(session: AsyncSessionDep) -> UserDal:
    return UserDal(session)

UserDalDep = Annotated[UserDal, Depends(get_user_dal)]
