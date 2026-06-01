from typing import Annotated

from fastapi import Depends

from src.services import AuthService, UserService
from .db import AuthDalDep, UserDalDep

def get_auth_service(
    auth_dal: AuthDalDep,
    user_dal: UserDalDep
) -> AuthService:
    return AuthService(auth_dal, user_dal)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

def get_user_service(
    auth_dal: AuthDalDep,
    user_dal: UserDalDep
) -> UserService:
    return UserService(auth_dal, user_dal)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]