from email.message import EmailMessage
from pathlib import Path
import smtplib
import ssl

from django.template.loader import get_template
from django.conf import settings as config_settings

from celery import shared_task

from catalog.utils import file_exists_in_directory, create_pdf_from_data
from settings import settings


@shared_task()
def send_email(params, email, text_body=None):
    list_emails = ['']
    if email:
        list_emails.append(email)

    message = EmailMessage()
    message['Subject'] = settings.SUBJECT
    message['From'] = settings.FROM
    message['To'] = ', '.join(list_emails)

    # Поле Cc используется для отправки копии письма другим получателям,
    # и они будут видны всем, кто получил письмо.
    # message['Cc'] = ''
    # Поле Bcc используется для скрытой копии, и адреса в этом поле не видны остальным получателям.
    # message['Bcc'] = ''

    # для обычного текста
    text_body = settings.BODY if text_body is None else text_body
    message.set_content(text_body)

    # Добавление HTML части
    template = get_template('sign.html')
    html_sign = template.render()
    html = f"""
    <div>
        <h1>{text_body}</h1>
    </div>
        <br><br>
        {html_sign}
    """
    message.add_alternative(html, subtype='html')

    filename = f'{params["name"]}.pdf'
    if not file_exists_in_directory(directory=config_settings.PDF_DIR, filename=filename):
        file_path = create_pdf_from_data(params=params)
    else:
        file_path = Path(config_settings.PDF_DIR, filename)

    with open(file_path, "rb") as attachment:
        message.add_attachment(attachment.read(),
                               maintype='application',
                               subtype="octet-stream",
                               filename=("utf-8", "", f"{filename}"))

    context = ssl.create_default_context()
    with smtplib.SMTP(settings.SMTP_SERVER, settings.PORT_TLS) as server:
        server.starttls(context=context)
        server.login(settings.FROM, settings.PASSWORD_EMAIL)
        server.send_message(message)
    print("sent email")
