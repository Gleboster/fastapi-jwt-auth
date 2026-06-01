from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped


class Base(DeclarativeBase):

    _repr_cnt = 3
    _repr_inc = []

    def __repr__(self) -> str:
        attr_val = []
        for i, attr in enumerate(self.__table__.columns):
            if attr.name in self._repr_inc or i < self._repr_cnt:
                attr_val.append((attr.name, self.__getattribute__(attr.name)))
        return (
                f"{self.__class__.__name__}"
                f"("
                f"{', '.join(f"{attr}={val}" for (attr, val) in attr_val)}"
                f"...)"
        )

