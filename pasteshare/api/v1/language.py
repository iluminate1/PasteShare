from collections.abc import Sequence

from fastapi import APIRouter, HTTPException, status

from pasteshare.api.dependencies import LanguageRepo, SuperUser
from pasteshare.core.exceptions import Conflict, NotFound
from pasteshare.core.schemas.language import (
    LanguageSchemaCreate,
    LanguageSchemaDB,
    LanguageSchemaOut,
    LanguageSchemaUpdate,
)

router = APIRouter()


@router.get("/all", response_model=Sequence[LanguageSchemaOut])
async def get_languages(language_repo: LanguageRepo):
    return await language_repo.find()


@router.get("/{language_id}", response_model=LanguageSchemaOut)
async def get_language_by_id(language_id: int, language_repo: LanguageRepo):
    language = await language_repo.get_by_id(language_id)
    if language is None:
        raise NotFound

    return language


@router.post("/", response_model=LanguageSchemaOut)
async def language_create(
    new_language: LanguageSchemaCreate,
    language_repo: LanguageRepo,
    _: SuperUser,
):
    language = await language_repo.get_by_name(new_language.name)
    if language is not None:
        raise Conflict

    entity = LanguageSchemaDB(**new_language.model_dump())
    return await language_repo.create(entity)


@router.patch("/{language_id}", response_model=LanguageSchemaOut)
async def update_language(
    language_id: int,
    language_data: LanguageSchemaUpdate,
    language_repo: LanguageRepo,
):
    language = await language_repo.get_by_id(language_id)
    if language is None:
        raise NotFound

    try:
        updated_language = await language_repo.update(
            language,
            language_data,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Couldn't update language with id {language_id}. Error: {e!s}",
        ) from e

    return updated_language


@router.delete("/{language_id}", response_model=LanguageSchemaOut)
async def delete_language(
    language_id: int,
    language_repo: LanguageRepo,
    _: SuperUser,
):
    language = await language_repo.get_by_id(language_id)
    if language is None:
        raise NotFound

    await language_repo.remove(language)

    return language
