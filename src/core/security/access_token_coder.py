from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt

from ..configs.auth_config import auth_settings
from ..dto import AccessTokenDto
from ..mappers import access_token_dict2dto, access_token_dto2dict
from ..utils import datetime_now


class AccessTokenCoder:

    @classmethod
    def create_access_token(cls, user_id: UUID) -> str:
        expired = (
            datetime_now() +
            timedelta(seconds=auth_settings.ACCESS_TOKEN_TTL)
        )

        payload_dto = AccessTokenDto(user_id=user_id,
                                     expired_datetime=expired,
                                     type="access")

        return jwt.encode(
            payload=access_token_dto2dict(payload_dto),
            key=auth_settings.JWT_SECRET_KEY,
            algorithm=auth_settings.JWT_ALGORITHM
        )

    @classmethod
    def decode_token(cls, token: str) -> AccessTokenDto:
        payload = jwt.decode(
            jwt=token,
            key=auth_settings.JWT_SECRET_KEY,
            algorithms=[auth_settings.JWT_ALGORITHM]
        )

        return access_token_dict2dto(payload)