import datetime
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from pasteshare.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: str | Any,
    expires_delta: datetime.timedelta | None = None,
) -> str:
    """Create an access token.

    Parameters
    ----------
        subject (Union[str, Any]): The subject for which the access token is created.
        expires_delta (timedelta, optional): The expiration time for the access token. Defaults to None.

    Returns
    -------
        str: The encoded access token.

    """
    if expires_delta:
        expire = datetime.datetime.now(tz=datetime.UTC) + expires_delta
    else:
        expire = datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(
            minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(
        to_encode,
        settings.jwt.SECRET_KEY,
        algorithm=settings.jwt.ALGORITHM,
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if a plain password matches a hashed password.

    Parameters
    ----------
        plain_password (str): The plain password to be verified.
        hashed_password (str): The hashed password to compare with.

    Returns
    -------
        bool: True if the plain password matches the hashed password, False otherwise.

    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate the hash value of a password.

    Parameters
    ----------
        password (str): The password to be hashed.

    Returns
    -------
        str: The hash value of the password.

    """
    return pwd_context.hash(password)
