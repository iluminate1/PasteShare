from pasteshare.core.models import Comment
from pasteshare.core.repository.base import SQLAlchemyRepository


class CommentRepository(SQLAlchemyRepository[Comment]):
    model = Comment
