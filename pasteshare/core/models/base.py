from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

# from sqlalchemy.orm import declared_attr
from pasteshare.core.config import settings

# from pasteshare.utils import camel_case_to_snake_case


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__: bool = True

    metadata = MetaData(naming_convention=settings.database.NAMING_CONVENTION)

    # @declared_attr.directive
    # @classmethod
    # def __tablename__(cls) -> str:
    #     return f"{camel_case_to_snake_case(cls.__name__)}s"

