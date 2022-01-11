import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app import schemas
from app.core import mail_settings


conf = ConnectionConfig(
    MAIL_USERNAME=mail_settings.MAIL_USERNAME,
    MAIL_PASSWORD=mail_settings.MAIL_PASSWORD,
    MAIL_FROM=mail_settings.MAIL_FROM,
    MAIL_PORT=mail_settings.MAIL_PORT,
    MAIL_SERVER=mail_settings.MAIL_SERVER,
    MAIL_FROM_NAME=mail_settings.MAIL_FROM_NAME,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=os.path.abspath('assets/emails')
)


async def send_email_verification(email: schemas.Email):
    message = MessageSchema(
        subject='Incedo Account Verification Code',
        recipients=email.dict().get('email'),
        template_body=email.dict().get('body')
    )

    fm = FastMail(conf)

    await fm.send_message(message, template_name='verify_email.html')
