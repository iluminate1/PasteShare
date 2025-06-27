from pasteshare.core.models import Language
from pasteshare.core.repository.base import SQLAlchemyRepository


class LanguageRepository(SQLAlchemyRepository[Language]):
    model = Language

    async def get_by_name(self, name: str) -> Language | None:
        return await self.get_one(self.model.name == name)
