from typing import Annotated

from fastapi import APIRouter, Body, status

from src.core.dto import AccessRefreshTokensDto
from ..dependencies import AuthServiceDep, UserServiceDep, CurrentUserDep
from ...schemes import (
    LoginRequest,
    LoginResponse,
    MeResponse,
    ProtectedDataResponse,
    PublicDataResponse,
    RefreshRequest,
    RefreshResponse,
    RegisterRequest,
    RegisterResponse,
)

auth_router = APIRouter(
    prefix="/jwt_auth",
    tags=["jwt auth 🛡️🔄"],
)

_401_UNAUTHORIZED = {status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials or token"}}
_409_CONFLICT = {status.HTTP_409_CONFLICT: {"description": "Username already registered"}}


@auth_router.get(
    "/public",
    response_model=PublicDataResponse,
    status_code=status.HTTP_200_OK,
)
async def get_public_data() -> PublicDataResponse:
    return PublicDataResponse()


@auth_router.post(
    "/users",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    responses=_409_CONFLICT,
)
async def register(
    request: Annotated[RegisterRequest, Body()],
    user_service: UserServiceDep
) -> RegisterResponse:
    user = await user_service.register(username=request.username, password=request.password, bio=request.bio)
    return RegisterResponse(user_id=user.id)


@auth_router.post(
    "/tokens",
    response_model=LoginResponse,
    status_code=status.HTTP_201_CREATED,
    responses=_401_UNAUTHORIZED,
)
async def login(
    request: Annotated[LoginRequest, Body()],
    auth_service: AuthServiceDep
) -> LoginResponse:
    tokens: AccessRefreshTokensDto = await auth_service.login(request.username, request.password)
    return LoginResponse(access_token=tokens.access_token, refresh_token=tokens.refresh_token)


@auth_router.post(
    "/tokens/refresh",
    response_model=RefreshResponse,
    status_code=status.HTTP_201_CREATED,
    responses=_401_UNAUTHORIZED,
)
async def refresh(
    request: Annotated[RefreshRequest, Body()],
    _: CurrentUserDep,
    auth_service: AuthServiceDep
) -> RefreshResponse:
    tokens = await auth_service.refresh(request.refresh_token)
    return RefreshResponse(access_token=tokens.access_token, refresh_token=tokens.refresh_token)


@auth_router.get(
    "/protected",
    response_model=ProtectedDataResponse,
    status_code=status.HTTP_200_OK,
    responses=_401_UNAUTHORIZED,
)
async def get_protected_data(
    _: CurrentUserDep
) -> ProtectedDataResponse:
    return ProtectedDataResponse()


@auth_router.get(
    "/users/me",
    response_model=MeResponse,
    status_code=status.HTTP_200_OK,
    responses=_401_UNAUTHORIZED,
)
async def get_me(
    current_user: CurrentUserDep
) -> MeResponse:
    return MeResponse(
        user_id=current_user.id,
        username=current_user.username,
        bio=current_user.bio
    )

@auth_router.delete(
    "/sessions/me",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=_401_UNAUTHORIZED,
)
async def logout(
    request: Annotated[RefreshRequest, Body()],
    _: CurrentUserDep,
    auth_service: AuthServiceDep
) -> None:
    await auth_service.logout(request.refresh_token)


@auth_router.delete(
    "/users/me",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=_401_UNAUTHORIZED,
)
async def unregister(
    current_user: CurrentUserDep,
    user_service: UserServiceDep
) -> None:
    await user_service.unregister(current_user)
