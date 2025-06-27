from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pasteshare.core.models import Base
from pasteshare.core.models.mixins import TimeStampMixin

if TYPE_CHECKING:
    from pasteshare.core.models.comment import Comment
    from pasteshare.core.models.paste import Paste


class User(TimeStampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(25))
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_super_user: Mapped[bool] = mapped_column(default=False)

    pastes: Mapped[list["Paste"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User[id={self.id}, name={self.name!r}]"
