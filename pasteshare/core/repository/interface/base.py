from abc import ABC, abstractmethod
from collections.abc import Sequence

from pydantic import BaseModel


class IRepository[T](ABC):
    """Abstract base class for all repositories."""

    @abstractmethod
    async def add(self, entity: T) -> None: ...

    @abstractmethod
    async def create(self, entity: BaseModel) -> T: ...

    @abstractmethod
    async def remove(self, entity: T) -> T: ...

    @abstractmethod
    async def update(self, entity: T, new_entity: BaseModel) -> T: ...

    @abstractmethod
    async def get_one(self, *args, **kwargs) -> T | None: ...

    @abstractmethod
    async def get_by_id(self, _id: int) -> T | None: ...

    @abstractmethod
    async def find(self, *args, **kwargs) -> Sequence[T]: ...
