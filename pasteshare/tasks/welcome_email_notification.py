from loguru import logger

from pasteshare.core.broker import broker
from pasteshare.mainling.send_welcome_email import send_welcome_email as send


@broker.task
async def send_welcome_email(user_id: int) -> None:
    logger.info("Sending welcome email to user {}", user_id)
    await send(user_id=user_id)
