from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from pasteshare.core.models import Base
from pasteshare.core.models.mixins import TimeStampMixin


class User(TimeStampMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(25))
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_super_user: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        return f"User[id={self.id}, name={self.name!r}]"
