from collections.abc import Sequence

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pasteshare.core.repository.interface import IRepository


class SQLAlchemyRepository[T](IRepository[T]):
    model: type[T]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        if not hasattr(self, "model"):
            msg = "The model should be defined"
            raise ValueError(msg)

    @property
    def session(self) -> AsyncSession:
        return self._session

    async def add(self, entity: T) -> None:
        self._session.add(entity)
        await self._session.commit()

    async def create(self, entity: BaseModel) -> T:
        entity_data = entity.model_dump(exclude_unset=True)
        db_entity = self.model(**entity_data)

        self._session.add(db_entity)
        await self._session.commit()
        await self._session.refresh(db_entity)

        return db_entity

    async def remove(self, entity: T) -> T:
        await self._session.delete(entity)
        await self._session.commit()

        return entity

    async def update(self, entity: T, new_entity: BaseModel) -> T:
        entity_update_data = new_entity.model_dump(
            exclude_none=True,
            exclude_unset=True,
        )

        for field, value in entity_update_data.items():
            setattr(entity, field, value)

        self._session.add(entity)
        await self._session.commit()
        await self._session.refresh(entity)

        return entity

    async def get_one(self, *args, **kwargs) -> T | None:
        stmt = select(self.model).filter(*args).filter_by(**kwargs)
        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_id(self, _id: int) -> T | None:
        stmt = select(self.model).filter_by(id=_id)
        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def find(self, *args, **kwargs) -> Sequence[T]:
        stmt = select(self.model).filter(*args).filter_by(**kwargs)
        result = await self._session.execute(stmt)

        return result.scalars().all()
