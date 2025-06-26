from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from pasteshare.core.database.manager import db_manager

ASession = Annotated[AsyncSession, Depends(db_manager.session_getter)]