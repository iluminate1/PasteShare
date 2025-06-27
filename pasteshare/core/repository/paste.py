from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from pasteshare.core.models import Paste
from pasteshare.core.models.comment import Comment
from pasteshare.core.repository.base import SQLAlchemyRepository


class PasteRepository(SQLAlchemyRepository[Paste]):
    model = Paste

    async def get_by_url(self, url: UUID) -> Paste | None:
        return await self.get_one(url=url)

    @classmethod
    async def add_comment(
        cls,
        session: AsyncSession,
        paste: Paste,
        comment: Comment,
    ) -> Comment:
        paste.comments.append(comment)
        session.add(paste)
        await session.commit()
        return comment
