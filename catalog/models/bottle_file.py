import os

from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from .bottle import Bottle
from catalog.utils import convert_img_to_webp


def get_file_upload_path_bottle(instance, filename):
    category = instance.bottle.category.name
    series = instance.bottle.series.name
    bottle_name = instance.bottle.name
    return os.path.join('files', category, series, bottle_name, filename)


class BottleFile(models.Model):
    class FileTypeChoices(models.TextChoices):
        IMAGE = 'image', 'image'
        VIDEO = 'video', 'video'

    bottle = models.ForeignKey(Bottle,
                               on_delete=models.CASCADE,
                               related_name="bottle_files",
                               verbose_name='Файл флакона')
    file_type = models.CharField(max_length=5,
                                 choices=FileTypeChoices.choices,
                                 default=FileTypeChoices.IMAGE,
                                 verbose_name='Тип файла')
    file = models.FileField(upload_to=get_file_upload_path_bottle,
                            verbose_name='Файл')
    thumbnail = ImageSpecField(source='file',
                               processors=[ResizeToFill(150, 150)],
                               format='JPEG',
                               options={'quality': 60})
    uploaded_at = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата загрузки')

    def save(self, *args, **kwargs):
        image_content = convert_img_to_webp(image=self.file)
        self.file.save(image_content.name, image_content, save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return '| --->'.join(f"{self.file}".rsplit('/', 2)[-2:])

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
