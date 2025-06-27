from fastapi import APIRouter

__all__ = ("api_v1",)

from pasteshare.api.v1.auth import router as auth_router
from pasteshare.api.v1.category import router as category_router
from pasteshare.api.v1.language import router as language_router
from pasteshare.api.v1.user import router as user_router

api_v1 = APIRouter()
api_v1.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_v1.include_router(user_router, prefix="/users", tags=["Users"])
api_v1.include_router(category_router, prefix="/category", tags=["Category"])
api_v1.include_router(language_router, prefix="/language", tags=["Language"])
