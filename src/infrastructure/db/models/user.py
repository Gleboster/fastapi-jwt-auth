from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    name: Mapped[str] = mapped_column(index=True, unique=True)
    bio: Mapped[str | None]

    password_hash: Mapped[str]