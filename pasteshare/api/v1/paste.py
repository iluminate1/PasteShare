from collections.abc import Sequence
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from pasteshare.api.dependencies import ActiveUser, PasteRepo
from pasteshare.core.exceptions import NotFound
from pasteshare.core.schemas import PasteSchemaCreate, PasteSchemaOut, PasteSchemaUpdate

router = APIRouter()


@router.get("/all", response_model=Sequence[PasteSchemaOut])
async def get_pastes(paste_repo: PasteRepo):
    return await paste_repo.find(is_private=False)


@router.get("/{paste_url}", response_model=PasteSchemaOut)
async def get_paste_by_url(paste_url: UUID, paste_repo: PasteRepo):
    paste = await paste_repo.get_by_url(paste_url)
    if paste is None:
        raise NotFound

    paste.views += 1
    paste_repo.session.add(paste)
    await paste_repo.session.commit()
    await paste_repo.session.refresh(paste)

    return paste


@router.post("/", response_model=PasteSchemaOut, status_code=status.HTTP_201_CREATED)
async def create_paste_private(
    paste_in: PasteSchemaCreate,
    paste_repo: PasteRepo,
    user: ActiveUser,
):
    paste = await paste_repo.create(paste_in)
    paste.user_id = user.id
    session = paste_repo.session
    session.add(paste)
    await session.commit()
    await session.refresh(paste)

    return paste


@router.post(
    "/guest",
    response_model=PasteSchemaOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_paste_public(
    paste_in: PasteSchemaCreate,
    paste_repo: PasteRepo,
):
    return await paste_repo.create(paste_in)


@router.put("/{paste_id}", response_model=PasteSchemaOut)
async def update_paste(
    paste_id: int,
    paste_in: PasteSchemaUpdate,
    paste_repo: PasteRepo,
    user: ActiveUser,
):
    paste = await paste_repo.get_by_id(paste_id)
    if paste is None:
        raise NotFound
    if paste.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this paste.",
        )
    return await paste_repo.update(paste, paste_in)


@router.delete("/{paste_id}", response_model=PasteSchemaOut)
async def delete_paste(
    paste_id: int,
    paste_repo: PasteRepo,
    user: ActiveUser,
):
    paste = await paste_repo.get_by_id(paste_id)
    if paste is None:
        raise NotFound
    if paste.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this paste.",
        )
    await paste_repo.remove(paste)
    return paste
