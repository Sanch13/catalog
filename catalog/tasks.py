from pathlib import Path
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from catalog.utils import file_exists_in_directory, create_pdf_from_data
from settings import settings

from django.conf import settings as config_settings

from celery import shared_task


@shared_task()
def send_email(params, email, text_body=None):
    message = MIMEMultipart()
    message['Subject'] = settings.SUBJECT
    message['From'] = settings.FROM
    message['To'] = email if email else settings.TO
    text_body = settings.BODY if text_body is None else text_body

    message.attach(MIMEText(text_body, 'plain', 'utf-8'))

    filename = f'{params["name"]}.pdf'
    if not file_exists_in_directory(directory=config_settings.PDF_DIR, filename=filename):
        file_path = create_pdf_from_data(params=params)
    else:
        file_path = Path(config_settings.PDF_DIR) / f"{params['name']}.pdf"

    with open(file_path, "rb") as attachment:
        # Создаем MIMEBase объект
        file_data = MIMEBase("application", "octet-stream")
        file_data.set_payload(attachment.read())

    encoders.encode_base64(file_data)

    file_data.add_header(
        "Content-Disposition",
        'attachment',
        filename=("utf-8", "", f"{filename}")
    )

    message.attach(file_data)

    context = ssl.create_default_context()
    with smtplib.SMTP(settings.SMTP_SERVER, settings.PORT_TLS) as server:
        server.starttls(context=context)
        server.login(settings.FROM, settings.PASSWORD_EMAIL)
        server.sendmail(settings.FROM, message['To'], message.as_string())
    print("sent email")
