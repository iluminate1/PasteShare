import uvicorn

from pasteshare.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "pasteshare.main:app",
        host=settings.server.SERVER_HOST,
        port=settings.server.SERVER_PORT,
        reload=settings.app.DEBUG,
    )
