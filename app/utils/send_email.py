from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.core import mail_settings
from app.schemas import _assets, _user


conf = ConnectionConfig(
    MAIL_USERNAME=mail_settings.MAIL_USERNAME,
    MAIL_PASSWORD=mail_settings.MAIL_PASSWORD,
    MAIL_FROM=mail_settings.MAIL_FROM,
    MAIL_PORT=mail_settings.MAIL_PORT,
    MAIL_SERVER=mail_settings.MAIL_SERVER,
    MAIL_FROM_NAME=mail_settings.MAIL_FROM_NAME,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)


async def send_email_verification(email: _assets.Email, user: _user.UserInDB):
    theme = _assets.Theme(**email.body['theme'])
    code = email.body['code']

    message = MessageSchema(
        subject='Incedo Account Verification',
        recipients=email.dict().get('email'),
        html=f"""
        <html>
            <body style="background-color: {theme.bg}; width: 100%; font-size: 1.25rem; padding: 2rem 0;">
                <table style="background-color: rgba(0,0,0,0.1); border-radius: 4px; height: 75%; padding: 1rem 2rem; max-width: 320px; margin-left: auto; margin-right: auto;">
                    <tr style="height: 100px;">
                        <td style="width: 100%; padding: 0 1rem; border-radius: 4px; background-color: {theme.bg};">
                            <p style="color: {theme.sub}; text-align: center; width: 100%; font-size: 2.5rem;"><i><b>Incedo</b></i></p>
                        </td>
                    </tr>
                    <tr style="height: 160px;">
                        <td style="width: 100%; height: 140px; margin: auto; padding: 0 1rem; border-radius: 4px; background-color: {theme.bg};">
                            <p style="color: {theme.text}; text-align: center; width: 100%;">Thanks for signing up,</p>
                            <p style="color: {theme.sub}; font-size: 1.5rem; width: 100%; text-align: center;"><i><b>{user.username}</b></i></p>
                        </td>
                    </tr>
                    <tr style="height: 180px;">
                        <td style="width: 100%; height: 160px; margin: auto; border-radius: 4px; background-color: {theme.bg};">
                            <p style="color: {theme.text}; text-align: center; width: 100%;">Here's your code:</p>
                            <p style="color: {theme.main}; text-align: center; width: fit-content; margin: auto; padding: 1.25rem 3rem; font-size: 2rem; background-color: rgba(0,0,0,0.1); border-radius: 4px;">{code}</p>
                        </td>
                    </tr>
                </table>
            </body>
        </html>
        """
    )

    fm = FastMail(conf)

    await fm.send_message(message)


def send_password_reset(email: _assets.Email, user: _user.UserInDB, bg: BackgroundTasks):
    theme = _assets.Theme(**email.body['theme'])
    url = email.body['url']

    message = MessageSchema(
        subject='Incedo Account Password Reset',
        recipients=email.dict().get('email'),
        html=f"""
        <html>
            <body style="background-color: {theme.bg}; width: 100%; font-size: 1.25rem; padding: 2rem 0;">
                <table style="background-color: rgba(0,0,0,0.1); border-radius: 4px; height: 75%; padding: 1rem 2rem; max-width: 320px; margin-left: auto; margin-right: auto;">
                    <tr style="height: 100px;">
                        <td style="width: 100%; padding: 0 1rem; border-radius: 4px; background-color: {theme.bg};">
                            <p style="color: {theme.sub}; text-align: center; width: 100%; font-size: 2.5rem;"><i><b>Incedo</b></i></p>
                        </td>
                    </tr>
                    <tr style="height: 160px;">
                        <td style="width: 100%; height: 140px; margin: auto; padding: 0 1rem; border-radius: 4px; background-color: {theme.bg};">
                            <p style="color: {theme.text}; text-align: center; width: 100%;">Reset your password, </p>
                            <p style="color: {theme.sub}; font-size: 1.5rem; width: 100%; text-align: center;"><i><b>{user.username}</b></i></p>
                        </td>
                    </tr>
                    <tr style="height: 180px;">
                        <td style="width: 100%; height: 160px; margin: auto; border-radius: 4px; background-color: {theme.bg};">
                            <p style="color: {theme.text}; text-align: center; width: 100%;">Enter this url:</button>
                            <p style="text-align: center; width: 100%;"><a href="{url}" style="color: {theme.main}; text-align: center; width: 100%; margin: auto; padding: 1.25rem 2rem; font-size: 1rem; border-radius: 4px;">Reset Password</a></p>
                        </td>
                    </tr>
                </table>
            </body>
        </html>
        """
    )

    fm = FastMail(conf)

    bg.add_task(fm.send_message, message=message)
