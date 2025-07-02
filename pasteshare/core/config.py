from functools import cached_property

from pydantic import BaseModel
from pydantic.networks import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    PROJECT_NAME: str = "PasteShare"
    API_VERSION: str = "v1"
    DEBUG: bool = True


class JWTSettings(BaseModel):
    SECRET_KEY: str = "ca6f2f0aa75c75b07d43b7b8f954b424f4165c775b7de030d76c87d3fb7da268"  # noqa: S105
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class ServerSettings(BaseModel):
    SERVER_HOST: str = "0.0.0.0"  # noqa: S104
    SERVER_PORT: int = 8000

    CORS_ORIGINS: list[str] = ["*"]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] = ["*"]


class TaskiqSettings(BaseModel):
    URL: str = "amqp://guest:guest@localhost:5672//"


class RedisSettings(BaseModel):
    HOST: str = "localhost"
    PORT: int = 6379
    DB: int = 0
    USER: str = "user"
    PASSWORD: str = "password"  # noqa: S105


class DatabaseSettings(BaseModel):
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"  # noqa: S105
    POSTGRES_DB: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_HOST: str = "database"
    NAMING_CONVENTION: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @cached_property
    def URL(self) -> str:  # noqa: N802
        return PostgresDsn(
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}",
        ).encoded_string()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.dev", ".env"),
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    app: AppSettings = AppSettings()
    jwt: JWTSettings = JWTSettings()
    server: ServerSettings = ServerSettings()
    taskiq: TaskiqSettings = TaskiqSettings()
    redis: RedisSettings = RedisSettings()
    database: DatabaseSettings = DatabaseSettings()


settings: Settings = Settings()
