from pydantic import EmailStr

from pasteshare.core.schemas.base import ORMSchema, Schema


class UserCreate(Schema):
    name: str
    email: EmailStr
    password: str
    is_super_user: bool = False
    is_active: bool = True


class PublicUserOut(ORMSchema):
    id: int
    name: str
    is_active: bool


class PrivateUserOut(ORMSchema):
    id: int
    name: str
    email: EmailStr
    is_active: bool


class UserInDB(Schema):
    name: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_super_user: bool = False


class UserUpdate(Schema):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool = True
    is_superuser: bool = False
