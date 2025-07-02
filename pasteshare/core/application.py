import logging
import sys
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from pasteshare.core import constants
from pasteshare.core.broker import broker
from pasteshare.core.cache import cache
from pasteshare.core.config import settings
from pasteshare.core.database.manager import db_manager
from pasteshare.core.logger import InterceptHandler


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: ARG001
    await broker.startup()
    logger.info(f"Ping successful: {await cache.ping()}")
    yield
    await db_manager.dispose()
    await broker.shutdown()
    await cache.close()


def create_app() -> FastAPI:
    app = FastAPI(
        debug=settings.app.DEBUG,
        title=settings.app.PROJECT_NAME,
        redoc_url=None,
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
        swagger_ui_parameters={
            "docExpansion": "list",
            "deepLinking": True,
            "tagsSorter": "alpha",
            "operationsSorter": "alpha",
            "filter": True,
            "displayRequestDuration": True,
            "showCommonExtensions": True,
        },
    )

    register_logger(not settings.app.DEBUG)
    register_assets(app)
    register_middleware(app)
    register_exception_handlers(app)

    return app


def register_assets(app: FastAPI) -> None:
    """Ensure the static/media dirs exist and mount them on the app."""
    # Static files
    constants.STATIC_DIR.mkdir(parents=True, exist_ok=True)
    app.mount(
        constants.STATIC_URL,
        StaticFiles(directory=str(constants.STATIC_DIR)),
        name="static",
    )

    # Media files
    # constants.MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    # app.mount(
    #     constants.MEDIA_URL,
    #     StaticFiles(directory=str(constants.MEDIA_DIR)),
    #     name="media",
    # )


def register_middleware(app: FastAPI) -> None:
    """Include and configure global middleware."""
    # CORS (Cross-Origin Resource Sharing) settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.server.CORS_ORIGINS,
        allow_origin_regex=settings.server.CORS_ORIGINS_REGEX,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_logger(register: bool = False) -> None:
    if not register:
        return

    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel("DEBUG")

    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    logger.configure(
        handlers=[
            {"sink": sys.stdout, "serialize": False},
            {
                "sink": constants.LOG_DIR / "application.log",
                "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
                "rotation": "500 MB",
                "compression": "zip",
                "level": "TRACE" if settings.app.DEBUG else "INFO",
                "backtrace": settings.app.DEBUG,
                "diagnose": settings.app.DEBUG,
            },
        ],
    )


def register_exception_handlers(app: FastAPI) -> None: ...
