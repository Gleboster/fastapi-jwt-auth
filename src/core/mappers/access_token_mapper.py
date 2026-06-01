from datetime import datetime, timezone, timedelta

from ..dto import AccessTokenDto
from ..utils import datetime_fromtimestamp

def access_token_dict2dto(token: dict):
    return AccessTokenDto(
        user_id=token["sub"],
        expired_datetime=datetime_fromtimestamp(token["exp"]),
        type=token["type"]
    )

def access_token_dto2dict(token_dto: AccessTokenDto):
    sub = str(token_dto.user_id)
    expire = int(token_dto.expired_datetime.timestamp())
    type = token_dto.type

    return {
        "sub" : sub,
        "exp" : expire,
        "type": type
    }