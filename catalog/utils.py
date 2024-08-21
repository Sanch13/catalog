from io import BytesIO

from PIL import Image

from django.core.paginator import Paginator
from django.core.files.base import ContentFile


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
