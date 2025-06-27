from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pasteshare.core.models import Base
from pasteshare.core.models.mixins import TimeStampMixin

if TYPE_CHECKING:
    from pasteshare.core.models.paste import Paste


class Language(TimeStampMixin, Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    file_extension: Mapped[str] = mapped_column(String(10))

    pastes:Mapped[list["Paste"]] = relationship("Paste", back_populates="language")

    def __repr__(self):
        return f"Language[id={self.id}, name='{self.name}', code='{self.code}']"
