from dataclasses import dataclass


@dataclass
class AccessRefreshTokensDto:
    access_token: str
    refresh_token: str