from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from pasteshare.api.dependencies import UserRepo
from pasteshare.core.config import settings
from pasteshare.core.schemas import Token, UserInDB, UserRegister
from pasteshare.core.security import create_access_token, get_password_hash
from pasteshare.tasks import send_welcome_email

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_access_token(
    user_repo: UserRepo,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> dict[str, str]:
    user = await user_repo.authenticate_user(
        email=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    if not user_repo.is_active_user(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    access_token_expires = timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id,
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_repo: UserRepo,
    user_register: UserRegister,
):
    user = await user_repo.get_user_by_email(email=user_register.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The user with this {user_register.email} already exists in the system",
        )

    user_in = UserInDB(
        **user_register.model_dump(exclude_unset=True, exclude_defaults=True),
        hashed_password=get_password_hash(user_register.password),
    )

    user = await user_repo.create(user_in)
    await send_welcome_email.kiq(user_id=user.id)
    return {"message": "User created successfully"}
