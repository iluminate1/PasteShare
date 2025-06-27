from collections.abc import Sequence

from fastapi import APIRouter, HTTPException, status

from pasteshare.api.dependencies import CategoryRepo, SuperUser
from pasteshare.core.exceptions import Conflict, NotFound
from pasteshare.core.schemas.category import (
    CategorySchemaCreate,
    CategorySchemaDB,
    CategorySchemaOut,
    CategorySchemaUpdate,
)

router = APIRouter()


@router.get("/all", response_model=Sequence[CategorySchemaOut])
async def get_categories(category_repo: CategoryRepo):
    return await category_repo.find()


@router.get("/{category_id}", response_model=CategorySchemaOut)
async def get_category_by_id(category_id: int, category_repo: CategoryRepo):
    category = await category_repo.get_by_id(category_id)
    if category is None:
        raise NotFound

    return category


@router.post("/", response_model=CategorySchemaOut)
async def category_create(
    new_category: CategorySchemaCreate,
    category_repo: CategoryRepo,
    _: SuperUser,
):
    category = await category_repo.get_by_name(new_category.name)
    if category is not None:
        raise Conflict

    entity = CategorySchemaDB(**new_category.model_dump())
    return await category_repo.create(entity)


@router.patch("/{category_id}", response_model=CategorySchemaOut)
async def update_category(
    category_id: int,
    category_data: CategorySchemaUpdate,
    category_repo: CategoryRepo,
):
    category = await category_repo.get_by_id(category_id)
    if category is None:
        raise NotFound

    try:
        updated_category = await category_repo.update(
            category,
            category_data,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Couldn't update category with id {category_id}. Error: {e!s}",
        ) from e

    return updated_category


@router.delete("/{category_id}", response_model=CategorySchemaOut)
async def delete_category(
    category_id: int,
    category_repo: CategoryRepo,
    _: SuperUser,
):
    category = await category_repo.get_by_id(category_id)
    if category is None:
        raise NotFound

    await category_repo.remove(category)

    return category
