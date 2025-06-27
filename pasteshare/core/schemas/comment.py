from pydantic import Field

from pasteshare.core.schemas import ORMSchema, Schema
from pasteshare.core.schemas.user import PublicUserOut


class CommentSchemaCreate(Schema):
    text: str = Field(..., min_length=1, max_length=2000)


class CommentSchemaUpdate(Schema):
    text: str | None = Field(..., min_length=1, max_length=2000)


class CommentSchemaOut(ORMSchema):
    id: int
    text: str
    user: PublicUserOut | None = None


class CommentSchemaDB(Schema):
    paste_id: int
    user_id: int
    text: str = Field(..., min_length=1, max_length=2000)
