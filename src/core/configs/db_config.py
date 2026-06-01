from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from ._env_file import ENV_FILE


class DbSettings(BaseSettings):
    USER: str
    PASS: str
    HOST: str
    PORT: str
    NAME: str

    def get_async_url(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"

    def get_url(self):
        return f"postgresql+psycopg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"

    model_config = SettingsConfigDict(env_file=ENV_FILE, env_prefix="DB_", extra="ignore")


db_settings = DbSettings()