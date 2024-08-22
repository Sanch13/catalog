import os
from io import BytesIO
from pathlib import Path

from PIL import Image
from bs4 import BeautifulSoup
from fpdf import FPDF, XPos, YPos

from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from django.conf import settings as config_settings

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


def get_jar_data_from_db(id_item):
    from catalog.models import Jar

    jar = Jar.objects.prefetch_related('jar_files').filter(id=id_item).first()

    if jar:
        params = {
            'name': jar.name,
            'volume': jar.volume,
            'surface': jar.surface,
            'status_decoration': jar.status_decoration,
            'description': BeautifulSoup(jar.description, "html.parser").get_text(),
            'files': [open(file, 'rb').read() for file in
                      [file.file.path for file in jar.jar_files.all()]]

        }

        return params


def convert_webp_to_jpeg_bytes(file):
    # Открываем WEBP-изображение из байтового потока
    with Image.open(BytesIO(file)) as img:
        # Преобразуем изображение в формат JPEG и сохраняем его в байтовый поток
        jpeg_io = BytesIO()
        img.convert('RGB').save(jpeg_io, format='JPEG')
        jpeg_io.seek(0)  # Возвращаемся к началу потока
        return jpeg_io


def create_pdf_from_data(params):
    image_bytes_list = params["files"]
    font_path = str(Path(__file__).resolve().parent) + "/" + "DejaVuSans.ttf"
    print("font_path", font_path)
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', font_path)
    page_width = pdf.w  # Ширина страницы (210 мм для A4)
    page_height = pdf.h  # Высота страницы (297 мм для A4)
    margin = 3
    images_per_row = 3

    available_width = (page_width - 2 * margin) / images_per_row  # 68 mm

    image_width = available_width
    image_height = image_width  # Если хотите, чтобы изображения были квадратными

    x_start = margin
    y_start = margin
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

    header_font_size = 24
    pdf.set_font("DejaVu", '', size=header_font_size)

    text_width = pdf.get_string_width(params["name"])
    x_position = (page_width - text_width) / 2  # Смещение для центрирования

    # Вставка текста по центру строки
    pdf.set_y(height_y_photo + 6)  # Установка вертикальной позиции после изображений
    pdf.set_x(x_position)          # Установка горизонтальной позиции для центрирования
    pdf.cell(text_width, 10, params["name"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_y(height_y_photo + 20)
    pdf.set_font("DejaVu", size=16)

    table_width = page_width - 2 * margin   # Ширина таблицы с учетом отступов
    col1_width = table_width * 0.3          # 30% ширины страницы для первой колонки
    col2_width = table_width * 0.7          # 70% ширины страницы для второй колонки

    text_items = [
        ("Объем мл.", params['volume']),
        ("Поверхность", params['surface']),
        ("Декорирование", params['status_decoration']),
    ]

    row_height = 10  # Настройка высоты строки таблицы

    # Создание строк таблицы
    for label, value in text_items:
        pdf.set_x(margin)  # Начало строки таблицы по оси X
        pdf.cell(col1_width, row_height, label, border=1, align='L')  # Первая колонка
        pdf.cell(col2_width, row_height, str(value), border=1, align='L')  # Вторая колонка
        pdf.ln(row_height)  # Переход на следующую строку

    pdf.ln(10)  # Добавляем небольшой отступ перед описанием
    description = params['description']
    pdf.multi_cell(0, 10, description)  # Добавление описания

    pdf.output(f"{config_settings.PDF_DIR}/{params['name']}.pdf")
    filename = f"{params['name']}.pdf"
    return Path(config_settings.PDF_DIR, filename)


def file_exists_in_directory(directory, filename):
    return Path(directory, filename).is_file()
