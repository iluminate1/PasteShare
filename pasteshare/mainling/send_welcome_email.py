from pasteshare.core.config import settings
from pasteshare.core.database import db_manager
from pasteshare.core.repository import UserRepository
from pasteshare.core.templates import env
from pasteshare.mainling.send_message import send_email


async def send_welcome_email(user_id: int) -> None:
    async with db_manager.session_factory() as session:
        user = await UserRepository(session=session).get_by_id(user_id)

        if user is None:
            msg = "Invalid user"
            raise Exception(msg)  # noqa: TRY002

    t = env.get_template("mail/welcome_message.html")
    body = await t.render_async(
        service_name=settings.app.PROJECT_NAME,
        username=user.name,
    )

    await send_email(
        recipient=user.email,
        subject="Welcome to our site!",
        body=body,
    )
