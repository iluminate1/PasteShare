from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pasteshare.core.models import Base
from pasteshare.core.models.mixins import TimeStampMixin

if TYPE_CHECKING:
    from pasteshare.core.models.paste import Paste


class Category(TimeStampMixin, Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str]

    pastes: Mapped[list["Paste"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"Category[id={self.id}, name={self.name}]"
