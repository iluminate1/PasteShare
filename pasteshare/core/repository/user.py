from sqlalchemy.ext.asyncio import AsyncSession

from pasteshare.core.models.users import User
from pasteshare.core.repository.base import SQLAlchemyRepository
from pasteshare.core.security import verify_password


class UserRepository(SQLAlchemyRepository[User]):
    model = User

    async def get_user_by_email(self, email: str) -> User | None:
        """Get a user by email.

        Parameters
        ----------
            email (str): The email of the user.

        Returns
        -------
            Optional[User]: The user found by email, or None if not found.

        """
        return await self.get_one(self.model.email == email)

    @staticmethod
    def is_super_user(user: User) -> bool:
        """Check if the given user is a super user.

        Parameters
        ----------
            user (User): The user to check.

        Returns
        -------
            bool: True if the user is a super user, False otherwise.

        """
        return user.is_super_user

    @staticmethod
    def is_active_user(user: User) -> bool:
        """Check if a user is active.

        Parameters
        ----------
            user (User): The user object to check.

        Returns
        -------
            bool: True if the user is active, False otherwise.

        """
        return user.is_active

    @staticmethod
    async def deactivate_user(session: AsyncSession, user: User) -> User:
        """Deactivates a user by setting their `is_active` flag to `False`.

        Parameters
        ----------
            session (Session): The database session object.
            user (User): The user to deactivate.

        Returns
        -------
            User: The deactivated user object.

        """
        user.is_active = False
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> User | None:
        """Authenticate a user with the given email and password.

        Parameters
        ----------
            db (Session): The database session object.
            email (str): The email of the user.
            password (str): The password of the user.

        Returns
        -------
            Optional[User]: The authenticated user if successful, None otherwise.

        """
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
