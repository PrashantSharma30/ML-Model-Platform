from fastapi_mail import FastMail, MessageSchema, MessageType

from app.core.mail import mail_config


async def send_welcome_email(
    recipient_email: str,
    username: str,
):
    html = f"""
    <h2>Welcome to ML Model Platform!</h2>

    <p>Hello {username},</p>

    <p>Your account has been created successfully.</p>

    <p>You can now:</p>

    <ul>
        <li>Upload models</li>
        <li>Train models</li>
        <li>Deploy models</li>
        <li>Make predictions</li>
    </ul>

    <p>Happy building!</p>

    <p><strong>ML Model Platform Team</strong></p>
    """

    message = MessageSchema(
        subject="Welcome to ML Model Platform",
        recipients=[recipient_email],
        body=html,
        subtype=MessageType.html,
    )

    fm = FastMail(mail_config)

    await fm.send_message(message)