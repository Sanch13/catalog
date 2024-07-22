import os

from django.db import models

from .cap import Cap

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


def get_file_upload_path_cap(instance, filename):
    return os.path.join('files', instance.cap.category.name, instance.cap.name, filename)


class CapFile(models.Model):
    class FileTypeChoices(models.TextChoices):
        IMAGE = 'image', 'image'
        VIDEO = 'video', 'video'

    cap = models.ForeignKey(Cap,
                            on_delete=models.CASCADE,
                            related_name="cap_files",
                            verbose_name='Файл колпачка')
    file_type = models.CharField(max_length=5,
                                 choices=FileTypeChoices.choices,
                                 default=FileTypeChoices.IMAGE,
                                 verbose_name='Тип файла')
    file = models.FileField(upload_to=get_file_upload_path_cap,
                            verbose_name='Файл')
    thumbnail = ImageSpecField(source='file',
                               processors=[ResizeToFill(150, 150)],
                               format='JPEG',
                               options={'quality': 60})
    uploaded_at = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата загрузки')

    def __str__(self):
        return '| --->'.join(f"{self.file}".rsplit('/', 2)[-2:])

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
