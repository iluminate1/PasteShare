from fastapi import APIRouter

__all__ = ("api_v1",)

api_v1 = APIRouter()


@api_v1.get("/")
async def health_check():
    return {"status": "healthy"}

