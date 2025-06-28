from email.mime.text import MIMEText

import aiosmtplib


async def send_email(
    recipient: str,
    subject: str,
    body: str,
):
    admin_email = "admin@site.com"

    # message = EmailMessage()
    message = MIMEText(body, "html")
    message["From"] = admin_email
    message["To"] = recipient
    message["Subject"] = subject

    await aiosmtplib.send(
        message,
        sender=admin_email,
        recipients=[recipient],
        hostname="localhost",
        port=1025,
    )
