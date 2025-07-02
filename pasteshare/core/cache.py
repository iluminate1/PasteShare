from redis.asyncio import Redis

from pasteshare.core.config import settings

cache = Redis(
    host=settings.redis.HOST,
    port=settings.redis.PORT,
    # username=settings.redis.USER,
    # password=settings.redis.PASSWORD,
    db=settings.redis.DB,
)
