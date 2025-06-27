from typing import Annotated

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError

from pasteshare.core.config import settings
from pasteshare.core.database import ASession
from pasteshare.core.exceptions import get_credential_exception
from pasteshare.core.models import User
from pasteshare.core.repository import (
    CategoryRepository,
    CommentRepository,
    LanguageRepository,
    PasteRepository,
    UserRepository,
)
from pasteshare.core.repository.base import SQLAlchemyRepository
from pasteshare.core.schemas import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class RepoFactory[T: type[SQLAlchemyRepository]]:
    def __init__(self, repository: T) -> None:
        self.__repository = repository

    def __call__(self, session: ASession) -> T:
        return self.__repository(session=session)


UserRepo = Annotated[UserRepository, Depends(RepoFactory(UserRepository))]
CategoryRepo = Annotated[CategoryRepository, Depends(RepoFactory(CategoryRepository))]
LanguageRepo = Annotated[LanguageRepository, Depends(RepoFactory(LanguageRepository))]
CommentRepo = Annotated[CommentRepository, Depends(RepoFactory(CommentRepository))]
PasteRepo = Annotated[PasteRepository, Depends(RepoFactory(PasteRepository))]


def get_token(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    """Retrieve the token payload from the provided JWT token.

    Parameters
    ----------
        token (str | None): The JWT token. Defaults to the value returned by the `oauth2_scheme` dependency.

    Returns
    -------
        TokenPayload: The decoded token payload.

    Raises
    ------
        HTTPException: If there is an error decoding the token or validating the payload.

    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt.SECRET_KEY,
            algorithms=[settings.jwt.ALGORITHM],
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError) as e:
        raise get_credential_exception(status_code=status.HTTP_403_FORBIDDEN) from e
    return token_data


async def get_current_user(
    user_repo: UserRepo,
    token: Annotated[TokenPayload, Depends(get_token)],
) -> User:
    """Retrieve the current user based on the provided database session and authentication token.

    Parameters
    ----------
        user_repo: The user repository to use for querying the user information.
        token (TokenPayload): The authentication token containing the user's identification.

    Returns
    -------
        User: The user object representing the current authenticated user.

    Raises
    ------
        HTTPException: If the user is not found in the database.

    """
    user = await user_repo.get_one(User.id == token.sub)
    if user is None:
        raise get_credential_exception(
            status_code=status.HTTP_404_NOT_FOUND,
            details="User not found",
        )
    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Return the current active user.

    Parameters
    ----------
        current_user (User | None): The current user.

    Returns
    -------
        User: The current active user.

    Raises
    ------
        HTTPException: If the user is not active

    """
    if not UserRepository.is_active_user(current_user):
        raise get_credential_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            details="Inactive user",
        )
    return current_user


def get_current_superuser(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Return the current superuser.

    Parameters
    ----------
        current_user (User | None): The current user.

    Returns
    -------
        User: The current superuser.

    Raises
    ------
        HTTPException: If the current user is not a super user.

    """
    if not UserRepository.is_super_user(current_user):
        raise get_credential_exception(
            status_code=status.HTTP_403_FORBIDDEN,
            details="The user does not have enough privileges",
        )
    return current_user


ActiveUser = Annotated[User, Depends(get_current_active_user)]
SuperUser = Annotated[User, Depends(get_current_superuser)]
