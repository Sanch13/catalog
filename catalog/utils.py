import os
from io import BytesIO
from pathlib import Path
from email.message import EmailMessage
import smtplib
import ssl

from PIL import Image
from bs4 import BeautifulSoup
from fpdf import FPDF, XPos, YPos

from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from django.conf import settings as config_settings
from django.db.models import Q
from django.template.loader import render_to_string

from pypdf import PdfWriter, PdfReader

from settings import settings


def get_objects_from_paginator(request, per_page=1, model_objects_list=None):
    if model_objects_list:
        paginator = Paginator(model_objects_list, per_page=per_page)
        page_number = request.GET.get('page', 1)
        return paginator.page(page_number)


def get_upload_path_category(instance, filename):
    return os.path.join('files', instance.name, filename)


def get_validate_list_values(data: list) -> list[tuple[int, int]]:
    filtered_data = []
    for el in data:
        if '-' in el:
            first, second = el.split('-')
            filtered_data.append((int(first), int(second)))
        else:
            filtered_data.append((int(el), int(el)))
    sorted_volumes = sorted(filtered_data)
    if sorted_volumes:
        return sorted_volumes


def get_query_for_request_to_db(list_volumes: list[tuple[int, int]]):
    query = Q()
    for start, end in list_volumes:
        query |= Q(volume__range=(start, end))
    return query


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


def get_list_params_jars_from_db(ids: list[int]) -> list:
    from catalog.models import Jar

    pdf_dir = config_settings.PDF_DIR
    params = []
    jars = Jar.objects.prefetch_related('jar_files').filter(id__in=ids)

    for jar in jars:
        filename = f"{jar.name}.pdf"
        item = {
            'name': jar.name,
            'volume': jar.volume,
            'surface': jar.surface,
            'status_decoration': jar.status_decoration,
            'feature': jar.feature,
            'description': BeautifulSoup(jar.description, "html.parser").get_text(),
            'files': [open(file, 'rb').read() for file in
                      [file.file.path for file in jar.jar_files.all()]],
            'filename': filename,
            'path_to_pdf': str(pdf_dir / filename)
        }
        params.append(item)

    return params


def get_list_params_caps_from_db(ids: list[int]) -> list:
    from catalog.models import Cap

    pdf_dir = config_settings.PDF_DIR
    params = []
    caps = Cap.objects.prefetch_related('cap_files').filter(id__in=ids)

    for cap in caps:
        filename = f"{cap.name}.pdf"
        item = {
            'name': cap.name,
            'throat_standard': cap.throat_standard,
            'type_of_closure': cap.type_of_closure,
            'surface': cap.surface,
            'description': BeautifulSoup(cap.description, "html.parser").get_text(),
            'files': [open(file, 'rb').read() for file in
                      [file.file.path for file in cap.cap_files.all()]],
            'filename': filename,
            'path_to_pdf': str(pdf_dir / filename)
        }
        params.append(item)

    return params


def get_list_params_bottles_from_db(ids: list[int], category) -> list:
    from catalog.models import Bottle

    pdf_dir = config_settings.PDF_DIR
    params = []
    if category == 'bottles':
        bottles = Bottle.objects.prefetch_related('bottle_files').filter(id__in=ids)
    else:
        bottles = Bottle.objects.filter(
            series_id__in=ids
        ).select_related(
            'series'
        ).prefetch_related(
            'bottle_files'
        )

    for bottle in bottles:
        filename = f"{bottle.name}.pdf"
        item = {
            'name': bottle.name,
            'volume': bottle.volume,
            'throat_standard': bottle.throat_standard,
            'shape': bottle.shape,
            'surface': bottle.surface,
            'status_decoration': bottle.status_decoration,
            'description': BeautifulSoup(bottle.description, "html.parser").get_text(),
            'files': [open(file, 'rb').read() for file in
                      [file.file.path for file in bottle.bottle_files.all()]],
            'filename': filename,
            'path_to_pdf': str(pdf_dir / filename)
        }
        params.append(item)

    return params


def convert_webp_to_jpeg_bytes(file):
    # Открываем WEBP-изображение из байтового потока
    with Image.open(BytesIO(file)) as img:
        # Преобразуем изображение в формат JPEG и сохраняем его в байтовый поток
        jpeg_io = BytesIO()
        img.convert('RGB').save(jpeg_io, format='JPEG')
        jpeg_io.seek(0)  # Возвращаемся к началу потока
        return jpeg_io


def get_params_category_for_table(params, category):
    items = []
    if category == 'jars':
        items = [
            ("Объем мл.", params['volume']),
            ("Поверхность", params['surface']),
            ("Декорирование", params['status_decoration']),
            ("Доп. характеристики", params['feature']),
        ]
    if category == 'caps':
        items = [
            ("Стандарт горла", params['throat_standard']),
            ("Тип колпачка", params['type_of_closure']),
            ("Поверхность", params['surface']),
        ]
    if category in ('bottles', 'series'):
        items = [
            ("Объем мл.", params['volume']),
            ("Стандарт горла", params['throat_standard']),
            ("Форма", params['shape']),
            ("Поверхность", params['surface']),
            ("Декорирование", params['status_decoration']),
        ]
    return items


def get_text_for_email_table(user_data):
    categories = {
        "new_products": "Новинки",
        "series": "Серии флаконов",
        "bottles": "Флаконы",
        "jars": "Баночки",
        "caps": "Колпачки",
        "no category": "",
    }
    places = {
        "catalog": "Из каталога продукции",
        "contact": "Из Свяжитесь со мной",
    }

    if user_data.get("category") in categories:
        user_data["category"] = categories[user_data.get("category")]
    if user_data.get("place") in places:
        user_data["place"] = places[user_data.get("place")]

    return user_data


def create_pdf_from_data(params, category):
    print("Create PDF file from category ", category)
    image_bytes_list = params["files"]
    font_path = Path(config_settings.FONT_DIR, "DejaVuSans.ttf")

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', str(font_path))
    pdf.set_font("DejaVu", '', size=24)

    page_width = pdf.w  # Ширина страницы (210 мм для A4)
    page_height = pdf.h  # Высота страницы (297 мм для A4)
    margin = 15
    padding_bottom = 5

    # HEADER
    header = 33
    pdf.set_y(0)
    pdf.set_x(5)
    pdf.image(name=Path(config_settings.BASE_DIR, 'static', 'img', 'header.jpg'),
              w=190,  # w=200
              h=35)

    # TITLE
    text_title = pdf.get_string_width(params["name"])
    x_position = (page_width - text_title) / 2  # Смещение для центрирования
    pdf.set_y(header + padding_bottom)
    pdf.set_x(x_position)
    pdf.cell(text_title, 10, params["name"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(padding_bottom)

    # IMAGES
    current_position_y = pdf.get_y()
    images_per_row = 3
    available_width = (page_width - 2 * margin) / images_per_row  # 68 mm
    image_height = image_width = available_width

    x_start = margin
    y_start = pdf.get_y()
    x = x_start
    y = y_start
    current_image_in_row = 0

    for image_bytes in image_bytes_list[:6]:
        if y + image_height > page_height - margin:  # Если не помещается на страницу
            pdf.add_page()  # Добавляем новую страницу
            x = x_start
            y = y_start
            current_image_in_row = 0  # Сброс текущей позиции в ряду

        # Преобразуем изображение и сохраняем его в PDF
        jpeg_io = convert_webp_to_jpeg_bytes(image_bytes)
        pdf.image(jpeg_io, x=x, y=y, w=image_width, h=image_height)

        current_image_in_row += 1
        if current_image_in_row < images_per_row:
            # Сдвиг по горизонтали для следующего изображения
            x += image_width
        else:
            # Переход на следующую линию
            x = x_start
            y += image_height
            current_image_in_row = 0

    height_y_photo = image_height if len(image_bytes_list) <= 3 else image_height * 2
    current_position_y = (current_position_y + height_y_photo)

    # TABLE
    pdf.set_y(current_position_y + padding_bottom)
    pdf.set_font("DejaVu", size=14)
    table_width = page_width - 2 * margin  # Ширина таблицы с учетом отступов
    col1_width = table_width * 0.4  # 30% ширины страницы для первой колонки
    col2_width = table_width * 0.6  # 70% ширины страницы для второй колонки
    row_height = 10  # Настройка высоты строки таблицы
    border_color = (127, 154, 20)
    text_items = get_params_category_for_table(params, category)
    for label, value in text_items:
        pdf.set_draw_color(*border_color)
        pdf.set_x(margin)  # Начало строки таблицы по оси X
        pdf.cell(col1_width, row_height, label, border='B', align='L')  # Первая колонка
        pdf.cell(col2_width, row_height, str(value), border='B', align='L')  # Вторая колонка
        pdf.ln(row_height)  # Переход на следующую строку

    # DESCRIPTION
    pdf.ln(padding_bottom)
    available_width_description = page_width - margin * 2
    description = params['description']
    pdf.set_x(margin)
    pdf.multi_cell(w=available_width_description, h=10, max_line_height=8,
                   text=description)  # Добавление описания

    filename = params["filename"]
    path_pdf_file = Path(config_settings.PDF_DIR, filename)
    pdf.output(str(path_pdf_file))
    return path_pdf_file


def file_exists_in_directory(file_path):
    return Path(file_path).is_file()


def get_formatted_file_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} байт"
    elif size_bytes < 1024 ** 2:
        size_kb = size_bytes / 1024
        return f"{size_kb:.2f} КБайт"
    elif size_bytes < 1024 ** 3:
        size_mb = size_bytes / (1024 ** 2)
        return f"{size_mb:.2f} МБайт"
    else:
        size_gb = size_bytes / (1024 ** 3)
        return f"{size_gb:.2f} ГБайт"


def convert_to_numbers(strings: list[str]) -> list:
    numbers = []
    for s in strings:
        try:
            num = int(s)
            numbers.append(num)
        except ValueError:
            continue
    return numbers


def merge_pdfs_to_stream(pdf_paths: list[str]):
    writer = PdfWriter()
    output_stream = BytesIO()

    for pdf in pdf_paths:
        reader = PdfReader(pdf)
        for page in reader.pages:
            writer.add_page(page)

    writer.write(output_stream)
    output_stream.seek(0)
    return output_stream


def send_admin_email(text_body):
    message = EmailMessage()
    message['Subject'] = 'Error'
    message['From'] = settings.FROM_APP
    message['To'] = ['a.zubchyk@miran-bel.com']
    message.set_content(text_body)
    context = ssl.create_default_context()
    with smtplib.SMTP(settings.SMTP_SERVER, settings.PORT_TLS) as server:
        server.starttls(context=context)
        server.login(settings.FROM_APP, settings.PASSWORD_APP)
        server.send_message(message)
    print("sent email to admin")


def get_text_subject_for_email_to_department(department) -> str:
    subject = {
        'production_email': "Предложение оборудования с выставки InterCharm",
        'buying_email': "Коммерческое предложение на материалы с выставки InterCharm",
        'marketing_email': "Предложение для маркетинга с выставки InterCharm",
        'miran_email': "Предложение о сотрудничестве с выставки InterCharm",
    }

    return subject.get(department, '')


def send_email_to_department(user_data):
    message = EmailMessage()
    message['Subject'] = get_text_subject_for_email_to_department(user_data.get('department', ''))
    message['From'] = settings.FROM_APP
    message['To'] = settings.DEPARTMENT[user_data['department']]

    template = 'template_for_emails/department.html'
    render_template_and_send_email(message, template, user_data)
    print("sent email to DEPARTMENT")


def send_data_to_client(list_params, data, file_stream):
    message = EmailMessage()
    message['Subject'] = settings.SUBJECT
    message['From'] = settings.SALE_EMAIL
    message['To'] = data["email"]

    # Поле Cc используется для отправки копии письма другим получателям,
    # и они будут видны всем, кто получил письмо.
    # message['Cc'] = ''
    # Поле Bcc используется для скрытой копии, и адреса в этом поле не видны остальным получателям.
    # message['Bcc'] = ''

    # # для обычного текста
    # text_body = settings.BODY
    # message.set_content(text_body)

    # Добавление HTML части
    html = render_to_string('template_for_emails/sign.html')
    message.add_alternative(html, subtype='html')

    filename = list_params[0]["filename"] if len(list_params) == 1 else f"Список продукции ЗАО «МИРАН».pdf"
    message.add_attachment(file_stream.read(),
                           maintype='application',
                           subtype="octet-stream",
                           filename=("utf-8", "", f"{filename}"))

    context = ssl.create_default_context()
    with smtplib.SMTP(settings.SMTP_SERVER, settings.PORT_TLS) as server:
        server.starttls(context=context)
        server.login(settings.SALE_EMAIL, settings.SALE_PASSWORD_EMAIL)
        server.send_message(message)
    print("sent email to client")


def get_subject_for_email(user_data):
    subject = {
        'catalog': "Информация о загрузке информации из каталога клиентом на InterCharm",
        'price': "Запрос цены на выбранную продукцию с InterCharm",
        'contact': "Запрос обратной связи с InterCharm",
    }
    if user_data.get("form") == "price" and user_data.get("place") == "catalog":
        user_data['subject'] = subject["price"]

    if user_data.get("form") == "catalog" and user_data.get("place") == "catalog":
        user_data['subject'] = subject["catalog"]

    if user_data.get("form") == "catalog" and user_data.get("place") == "contact":
        user_data['subject'] = subject["contact"]

    return user_data


def send_data_to_sale(user_data):
    message = EmailMessage()
    message['Subject'] = user_data.get('subject', "")
    # message['Subject'] = "Запрос цены на выбранную продукцию с InterCharm" if user_data.get("form") == "price" else "Информация о загрузке информации из каталога клиентом на InterCharm"
    message['From'] = settings.FROM_APP  # send app
    message['To'] = ['a.zubchyk@miran-bel.com']  # sent email settings.SALE_EMAIL to sale@miran-bel.com

    # text_body = "Информация о потенциальном покупателе"
    # message.set_content(text_body)
    template = "template_for_emails/template_email.html"
    render_template_and_send_email(message, template, user_data)
    print("sent email to sale")


def render_template_and_send_email(message, template, user_data):
    html = render_email_template(user_data=user_data, template_name=template)
    message.add_alternative(html, subtype='html')
    context = ssl.create_default_context()
    with smtplib.SMTP(settings.SMTP_SERVER, settings.PORT_TLS) as server:
        server.starttls(context=context)
        server.login(settings.FROM_APP, settings.PASSWORD_APP)
        server.send_message(message)


def render_email_template(user_data, template_name):
    context = {
        'name': user_data["name"],
        'company': user_data["company"],
        'phone_number': user_data.get("phone_number", ''),
        'email': user_data["email"],
        'category': user_data.get("category", ''),
        'products': user_data.get("products", ""),
        'comment': user_data["comment"],
        'place': user_data.get("place", ''),
        'status': user_data.get("status", ''),
    }
    return render_to_string(template_name=template_name,
                            context=context)


def get_size_category(list_params, category):
    all_size = 0
    for params in list_params:
        pdf_file_path = params['path_to_pdf']
        if not file_exists_in_directory(pdf_file_path):
            pdf_file_path = create_pdf_from_data(params=params, category=category)

        size = Path(pdf_file_path).stat().st_size
        all_size += size
    return all_size


def save_data_to_db_with_status(user_data, lead_qualification):
    from catalog.models import EmailLog

    EmailLog.objects.create(
        name=user_data["name"],
        company=user_data["company"],
        phone_number=user_data.get("phone_number", ''),
        email=user_data["email"],
        comment=user_data["comment"],
        category=user_data.get("category", ''),
        place=user_data.get("place", ''),
        status=user_data.get("status", ''),
        products=user_data.get("products", ''),
        lead_qualification=lead_qualification
    )


def get_params_from_category(user_data):
    category = user_data["category"]
    list_params = []
    if category == 'jars':
        list_params = get_list_params_jars_from_db(user_data["ids"])
    if category == 'caps':
        list_params = get_list_params_caps_from_db(user_data["ids"])
    if category in ('bottles', 'series'):
        list_params = get_list_params_bottles_from_db(user_data["ids"], category)
    if category == 'new_products':
        bottles = convert_to_numbers(user_data["new_products"].get('bottles', []))
        list_params += get_list_params_bottles_from_db(bottles, category="bottles")
        jars = convert_to_numbers(user_data["new_products"].get('jars', []))
        list_params += get_list_params_jars_from_db(jars)
        caps = convert_to_numbers(user_data["new_products"].get('caps', []))
        list_params += get_list_params_caps_from_db(caps)

    return list_params
