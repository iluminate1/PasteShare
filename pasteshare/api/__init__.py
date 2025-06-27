from fastapi import APIRouter

__all__ = ("api_v1",)

from pasteshare.api.v1.auth import router as auth_router

api_v1 = APIRouter()
api_v1.include_router(auth_router, prefix="/auth", tags=["Auth"])
