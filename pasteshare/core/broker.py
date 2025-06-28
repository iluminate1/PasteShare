__all__ = ("broker",)

from loguru import logger
from taskiq import TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker

from pasteshare.core.config import settings

broker = AioPikaBroker(
    url=settings.taskiq.URL,
)


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(_: TaskiqState) -> None:
    logger.debug("Broker start up")
