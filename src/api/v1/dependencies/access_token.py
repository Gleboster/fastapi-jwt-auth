from typing import Annotated

from fastapi import Header, Depends

from src.core.dto import UserDto
from .services import AuthServiceDep

AccessTokenHeader = Annotated[str, Header(alias="X-access-token")]

async def get_current_user(
    access_token: AccessTokenHeader,
    auth_service: AuthServiceDep
) -> UserDto:
    return await auth_service.authenticate(access_token)

CurrentUserDep = Annotated[UserDto, Depends(get_current_user)]
