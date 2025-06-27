from collections.abc import Sequence
from uuid import UUID

from fastapi import APIRouter

from pasteshare.api.dependencies import ActiveUser, CommentRepo, PasteRepo
from pasteshare.core.exceptions import NotFound
from pasteshare.core.schemas.comment import (
    CommentSchemaCreate,
    CommentSchemaDB,
    CommentSchemaOut,
)

router = APIRouter()


@router.get("/{paste_url}", response_model=Sequence[CommentSchemaOut])
async def get_comments(paste_url: UUID, paste_repo: PasteRepo):
    paste = await paste_repo.get_by_url(paste_url)
    if paste is None:
        raise NotFound

    return paste.comments


@router.post("/{paste_url}", response_model=CommentSchemaOut)
async def create_comment(
    paste_url: UUID,
    comment_in: CommentSchemaCreate,
    user: ActiveUser,
    paste_repo: PasteRepo,
    comment_repo: CommentRepo,
):
    paste = await paste_repo.get_by_url(paste_url)
    if paste is None:
        raise NotFound

    comment = await comment_repo.create(
        CommentSchemaDB(paste_id=paste.id, user_id=user.id, text=comment_in.text),
    )

    return await paste_repo.add_comment(paste_repo.session, paste, comment)
