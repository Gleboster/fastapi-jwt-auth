from datetime import datetime, timezone, timedelta
from uuid import UUID

from fastapi import HTTPException, status

from ..core.configs import auth_settings
from ..core.dto import UserDto, AccessRefreshTokensDto
from ..core.mappers import user_orm2dto
from ..core.security import Hasher, AccessTokenCoder
from ..core.utils import datetime_now
from ..infrastructure.db.dals import AuthDal, UserDal

_INVALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
)

_INVALID_TOKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired token",
)

_INVALID_USER_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User does not exist or unregistered",
)

class AuthService:
    def __init__(self, auth_dal: AuthDal, user_dal: UserDal) -> None:
        self.auth_dal = auth_dal
        self.user_dal = user_dal

    async def _create_access_refresh_tokens(self, user_id: UUID) -> AccessRefreshTokensDto:
        refresh_token_orm = await self.auth_dal.create_refresh_token(
            user_id,
            datetime_now() + timedelta(seconds=auth_settings.REFRESH_TOKEN_TTL)
        )

        access_token = AccessTokenCoder.create_access_token(user_id)
        refresh_token = str(refresh_token_orm.token)

        return AccessRefreshTokensDto(access_token, refresh_token)

    async def login(self, username: str, password: str) -> AccessRefreshTokensDto:
        user_orm = await self.user_dal.get_user_by_name(username)
        if user_orm is None:
            raise _INVALID_CREDENTIALS_EXCEPTION

        if not Hasher.verify_password(password, user_orm.password_hash):
            raise _INVALID_CREDENTIALS_EXCEPTION

        return await self._create_access_refresh_tokens(user_id=user_orm.id)


    async def refresh(self, refresh_token: str) -> AccessRefreshTokensDto:
        old_refresh_token = await self.auth_dal.get_refresh_token_by_token(UUID(refresh_token))

        if old_refresh_token is None or datetime_now() > old_refresh_token.expire_at:
            raise _INVALID_TOKEN_EXCEPTION

        user_id = old_refresh_token.user_id
        await self.auth_dal.delete_refresh_token_by_token(UUID(refresh_token))

        return await self._create_access_refresh_tokens(user_id=user_id)


    async def logout(self, refresh_token: str) -> None:
        await self.auth_dal.delete_refresh_token_by_token(UUID(refresh_token))


    async def authenticate(self, access_token: str) -> UserDto:
        try:
            token_payload = AccessTokenCoder.decode_token(access_token)
        except:
            raise _INVALID_TOKEN_EXCEPTION

        if datetime_now() > token_payload.expired_datetime:
            raise _INVALID_TOKEN_EXCEPTION

        user_id = token_payload.user_id

        user_orm = await self.user_dal.get_user_by_id(user_id)
        if user_orm is None:
            raise _INVALID_USER_EXCEPTION

        return user_orm2dto(user_orm)
