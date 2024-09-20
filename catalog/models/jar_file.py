import os

from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from .jar import Jar
from catalog.utils import convert_img_to_webp


def get_file_upload_path_jar(instance, filename):
    category = instance.jar.category.name
    jar_name = instance.jar.name
    return os.path.join('files', category, jar_name, filename)


class JarFile(models.Model):
    class FileTypeChoices(models.TextChoices):
        IMAGE = 'image', 'image'
        VIDEO = 'video', 'video'

    jar = models.ForeignKey(Jar,
                            on_delete=models.CASCADE,
                            related_name="jar_files",
                            verbose_name='Файл колпачка')
    file_type = models.CharField(max_length=5,
                                 choices=FileTypeChoices.choices,
                                 default=FileTypeChoices.IMAGE,
                                 verbose_name='Тип файла')
    file = models.FileField(upload_to=get_file_upload_path_jar,
                            verbose_name='Файл',
                            blank=True,
                            null=True,
                            )
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
