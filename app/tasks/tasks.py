from pydantic import EmailStr
from app.tasks.celery import celery
from PIL import Image
from pathlib import Path
from app.config import settings
from app.tasks.email_templates import create_booking_confirmation_template
import smtplib


# @celery.task
def process_pic(
    path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_200_100 = im.resize((200, 100))
    im_resized_1000_500.save(
        f"app/static/images/resized_1000_500_{im_path.name}")
    im_resized_200_100.save(
        f"app/static/images/resized_200_100_{im_path.name}")


# @celery.task  # Раскомментировать, если нужен celery вместо BackgroundTasks
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr,
):
    # Удалите строчку ниже для отправки сообщения на свой email, а на пользовательский
    email_to = settings.SMTP_USER
    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
