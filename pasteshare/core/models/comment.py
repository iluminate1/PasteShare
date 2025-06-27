from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pasteshare.core.models.base import Base
from pasteshare.core.models.mixins import TimeStampMixin

if TYPE_CHECKING:
    from pasteshare.core.models.paste import Paste
    from pasteshare.core.models.users import User


class Comment(TimeStampMixin, Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text)

    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User | None"] = relationship(
        back_populates="comments",
        lazy="selectin",
    )

    paste_id: Mapped[int] = mapped_column(ForeignKey("pastes.id"))
    paste: Mapped["Paste"] = relationship(
        back_populates="comments",
        lazy="selectin",
    )

    def __repr__(self):
        return (
            f"Comment[id={self.id}, paste_id={self.paste_id}, user_id={self.user_id}]"
        )
