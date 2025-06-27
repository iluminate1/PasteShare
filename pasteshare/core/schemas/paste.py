from datetime import datetime
from uuid import UUID

from pydantic import Field

from pasteshare.core.schemas import ORMSchema, Schema
from pasteshare.core.schemas.category import CategorySchemaOut
from pasteshare.core.schemas.comment import CommentSchemaOut
from pasteshare.core.schemas.language import LanguageSchemaOut
from pasteshare.core.schemas.user import PublicUserOut


class PasteSchemaCreate(Schema):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    language_id: int | None = None
    category_id: int | None = None
    is_private: bool | None = True


class PasteSchemaUpdate(Schema):
    title: str | None = Field(None, max_length=100)
    content: str | None = Field(None, min_length=1)
    language_id: int | None = None
    category_id: int | None = None
    is_private: bool | None = None


class PasteSchemaOut(ORMSchema):
    id: int
    title: str | None = None
    url: UUID
    content: str
    views: int
    is_private: bool = True
    created_at: datetime
    user: PublicUserOut | None = None
    language: LanguageSchemaOut | None = None
    category: CategorySchemaOut | None = None
    comments: list[CommentSchemaOut] = Field([])


class PasteSchemaDB(Schema):
    title: str | None = None
    url: UUID
    content: str
    views: int
    is_private: bool = True
    created_at: datetime
    user: PublicUserOut | None = None
    language: LanguageSchemaOut | None = None
    category: CategorySchemaOut | None = None
    comments: list[CommentSchemaOut] = Field([])
