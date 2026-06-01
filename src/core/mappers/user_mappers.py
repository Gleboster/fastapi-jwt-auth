from ..dto import UserDto
from src.infrastructure.db import UserOrm


def user_orm2dto(orm: UserOrm) -> UserDto:
    return UserDto(
        id=orm.id,
        username=orm.name,
        bio=orm.bio,
    )
