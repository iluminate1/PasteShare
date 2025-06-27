from pydantic import Field

from pasteshare.core.schemas.base import Schema


class Token(Schema):
    """Bearer Access Token."""

    access_token: str
    token_type: str


class TokenPayload(Schema):
    """Payload for Bearer Access Token."""

    sub: int | None = None


class UserRegister(Schema):
    name: str = Field(..., examples=["John"])
    email: str = Field(..., examples=["john@gmail.com"])
    password: str = Field(..., examples=["password"])
