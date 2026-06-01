from pydantic_settings import BaseSettings, SettingsConfigDict

from ._env_file import ENV_FILE

class AuthSettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_TTL: int = 900
    REFRESH_TOKEN_TTL: int = 60 * 60 * 24 * 7

    model_config = SettingsConfigDict(env_file=ENV_FILE, env_prefix="AUTH_", extra="ignore")

auth_settings = AuthSettings()
