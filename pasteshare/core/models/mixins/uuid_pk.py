import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import declarative_mixin, mapped_column


@declarative_mixin
class UUIDPrimaryKeyMixin:
    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        # server_default=text("uuid_generate_v4()"),
        unique=True,
        nullable=False,
    )
