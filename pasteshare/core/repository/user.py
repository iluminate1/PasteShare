from pasteshare.core.models.users import User
from pasteshare.core.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[User]):
    model = User
    