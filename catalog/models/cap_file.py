import os

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from django.db import models

from .cap import Cap
from catalog.utils import convert_img_to_webp


def get_file_upload_path_cap(instance, filename):
    category = instance.cap.category.name
    cap_name = instance.cap.name
    return os.path.join('files', category, cap_name, filename)


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
    rating = models.PositiveSmallIntegerField(blank=True,
                                              null=True,
                                              default=100,
                                              verbose_name='Порядок')
    thumbnail = ImageSpecField(source='file',
                               processors=[ResizeToFill(150, 150)],
                               format='JPEG',
                               options={'quality': 60})
    uploaded_at = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата загрузки')

    def save(self, *args, **kwargs):
        if not self.pk:
            image_content = convert_img_to_webp(image=self.file)
            self.file.save(image_content.name, image_content, save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return '| --->'.join(f"{self.file}".rsplit('/', 2)[-2:])

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = [
            "rating",
        ]
