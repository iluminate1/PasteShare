from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from pasteshare.core.models import Base
from pasteshare.core.models.mixins import TimeStampMixin


class Category(TimeStampMixin, Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str]

    def __repr__(self) -> str:
        return f"Category[id={self.id}, name={self.name}]"
