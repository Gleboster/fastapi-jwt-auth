from datetime import datetime, timezone, timedelta
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .user import UserOrm

class RefreshTokenOrm(Base):
    __tablename__ = "refresh_tokens"

    token: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    expire_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )

    user: Mapped[UserOrm] = relationship(viewonly=True, lazy="selectin")
