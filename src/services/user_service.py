from fastapi import HTTPException, status

from ..core.dto import UserDto
from ..core.mappers import user_orm2dto
from ..core.security import Hasher
from ..infrastructure.db.dals import AuthDal, UserDal

_CONFLICT_USERNAME_REGISTERED = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username already registered",
)


class UserService:
    def __init__(self, auth_dal: AuthDal, user_dal: UserDal) -> None:
        self.auth_dal = auth_dal
        self.user_dal = user_dal

    async def register(self, username: str, bio: str | None, password: str) -> UserDto:
        user_orm = await self.user_dal.get_user_by_name(username)
        if user_orm is not None:
            raise _CONFLICT_USERNAME_REGISTERED

        user_orm = await self.user_dal.create_user(
            name=username,
            bio=bio,
            password_hash=Hasher.hash_password(password),
        )
        return user_orm2dto(user_orm)

    async def unregister(self, user: UserDto) -> None:
        await self.auth_dal.delete_refresh_tokens_by_user(user.id)
        await self.user_dal.delete_user(user.id)
