from email.utils import encode_rfc2231
from io import BytesIO
from pathlib import Path
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from PIL import Image

from django.core.paginator import Paginator
from django.core.files.base import ContentFile

from settings import settings


def get_objects_from_paginator(request, per_page=1, model_objects_list=None):
    if model_objects_list:
        paginator = Paginator(model_objects_list, per_page=per_page)
        page_number = request.GET.get('page', 1)
        return paginator.page(page_number)


def get_min_max_volumes(data: list) -> tuple[int, int]:
    filtered_data = []
    for el in data:
        if '-' in el:
            first, second = el.split('-')
            filtered_data.append(int(first))
            filtered_data.append(int(second))
        else:
            filtered_data.append(int(el))

    sorted_volumes = sorted(filtered_data)
    if sorted_volumes:
        return sorted_volumes[0], sorted_volumes[-1]


def convert_img_to_webp(image):
    filename = image.name
    image = Image.open(image)
    target_size = (1200, 1200)
    image = image.resize(target_size, Image.Resampling.LANCZOS)

    image_io = BytesIO()
    image.save(image_io, format='WEBP', quality=90)
    image_content = ContentFile(image_io.getvalue(),
                                name=f'{filename.rsplit(".", 1)[0]}.webp')
    return image_content


def send_email():
    message = MIMEMultipart()
    message['Subject'] = settings.SUBJECT
    message['From'] = settings.FROM
    message['To'] = settings.TO

    message.attach(MIMEText(settings.BODY, 'plain', 'utf-8'))

    path_to_pdf_dir = Path(__file__).resolve().parent
    file_path = path_to_pdf_dir / "Баночка «Боди-150»_5.pdf"
    print(file_path)
    filename = str(file_path).rsplit("/", 1)[-1]
    print(filename)

    with open(file_path, "rb") as attachment:
        # Создаем MIMEBase объект
        file_data = MIMEBase("application", "octet-stream")
        file_data.set_payload(attachment.read())

    encoders.encode_base64(file_data)
    encoded_filename = encode_rfc2231(filename, charset='utf-8')
    print(encoded_filename)

    # Добавляем заголовки
    file_data.add_header(
        "Content-Disposition",
        f'attachment; filename*="{encoded_filename}"',
    )

    # Прикрепляем файл к сообщению
    message.attach(file_data)

    context = ssl.create_default_context()
    with smtplib.SMTP(settings.SMTP_SERVER, settings.PORT_TLS) as server:
        server.starttls(context=context)
        server.login(settings.FROM, settings.PASSWORD_EMAIL)
        server.sendmail(settings.FROM, settings.TO, message.as_string())
    print("sent email")
