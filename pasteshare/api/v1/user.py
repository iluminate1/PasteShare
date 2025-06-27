from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from pasteshare.api.dependencies import (
    UserRepo,
    get_current_active_user,
    get_current_superuser,
)
from pasteshare.core.models import User
from pasteshare.core.schemas.user import (
    PrivateUserOut,
    PublicUserOut,
    UserCreate,
    UserInDB,
    UserUpdate,
)
from pasteshare.core.security import get_password_hash

router = APIRouter()


@router.get("/me", response_model=PrivateUserOut)
async def get_auth_user(user: Annotated[User, Depends(get_current_active_user)]):
    return user


@router.get("/all", response_model=Sequence[PublicUserOut])
async def get_all_user(user_repo: UserRepo):
    return await user_repo.find()


@router.get("/{user_id}", response_model=PublicUserOut)
async def get_user(user_id: int, user_repo: UserRepo):
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id={user_id} not founded",
        )

    return user


@router.post("/", response_model=PrivateUserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_create: UserCreate,
    user_repo: UserRepo,
    _: Annotated[User, Depends(get_current_superuser)],
):
    user = await user_repo.get_user_by_email(email=user_create.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The user with this {user_create.email} already exists \
            in the system",
        )
    user_in = UserInDB(
        **user_create.model_dump(),
        hashed_password=get_password_hash(user_create.password),
    )
    return await user_repo.create(user_in)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    user_repo: UserRepo,
    current_user: Annotated[User, Depends(get_current_superuser)],
):
    user = await user_repo.get_one(User.id == user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found. Cannot delete.",
        )

    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot delete yourself",
        )
    try:
        await user_repo.remove(user)
    except Exception as e:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Couldn't delete user with id {user_id}. Error: {e!s}",
        ) from e

    return {"detail": f"User with id {user_id} deleted."}


@router.put("/{user_id}", response_model=PrivateUserOut, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    user_repo: UserRepo,
    _: Annotated[User, Depends(get_current_superuser)],
):
    user = await user_repo.get_one(User.id == user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found. Cannot update.",
        )
    try:
        user = await user_repo.update(user, user_update)
    except Exception as e:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Couldn't update user with id {user_id}. Error: {e!s}",
        ) from e
    return user
