import uuid

from sqlalchemy import TEXT, UUID, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pasteshare.core.models.base import Base
from pasteshare.core.models.category import Category
from pasteshare.core.models.comment import Comment
from pasteshare.core.models.language import Language
from pasteshare.core.models.mixins import TimeStampMixin
from pasteshare.core.models.users import User


class Paste(TimeStampMixin, Base):
    __tablename__ = "pastes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(TEXT, nullable=False)
    is_private: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    url: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    views: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped[User | None] = relationship(back_populates="pastes", lazy="selectin")

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True,
    )
    category: Mapped[Category | None] = relationship(
        back_populates="pastes",
        lazy="selectin",
    )

    language_id: Mapped[int | None] = mapped_column(
        ForeignKey("languages.id"),
        nullable=True,
    )
    language: Mapped[Language | None] = relationship(
        back_populates="pastes",
        lazy="selectin",
    )

    comments: Mapped[list[Comment]] = relationship(
        back_populates="paste",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self):
        return f"Paste[id={self.id}, title='{self.title}', uuid='{self.url}']"
