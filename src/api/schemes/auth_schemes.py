from uuid import UUID

from pydantic import BaseModel


# --- Requests ---


class RegisterRequest(BaseModel):
    username: str
    bio: str | None = None
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


# --- Responses ---


class RegisterResponse(BaseModel):
    user_id: UUID


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class PublicDataResponse(BaseModel):
    message: str = "This is public data. No authentication required."


class ProtectedDataResponse(BaseModel):
    message: str = "This is protected data. You are authenticated."


class MeResponse(BaseModel):
    user_id: UUID
    username: str
    bio: str | None = None
