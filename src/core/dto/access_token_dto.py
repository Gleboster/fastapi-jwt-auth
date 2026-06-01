from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class AccessTokenDto:
    user_id: UUID
    expired_datetime: datetime
    type: str
