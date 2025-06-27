from pasteshare.core.models import Category
from pasteshare.core.repository.base import SQLAlchemyRepository


class CategoryRepository(SQLAlchemyRepository[Category]):
    model = Category

    async def get_by_name(self, name: str) -> Category | None:
        return await self.get_one(self.model.name == name)
