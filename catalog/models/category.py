import os

from django.db import models
from django.utils.text import slugify

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


def get_upload_path_category(instance, filename):
    return os.path.join('files', instance.name, filename)


class Category(models.Model):
    class Categories(models.TextChoices):
        BOTTLES = 'Флаконы', 'Флаконы'
        JARS = 'Баночки', 'Баночки'
        CAPS = 'Колпачки', 'Колпачки'
        NEWS = 'Новинки', 'Новинки'

    name = models.CharField(max_length=50,
                            unique=True,
                            choices=Categories.choices,
                            default=Categories.BOTTLES,
                            verbose_name='Название')
    slug = models.SlugField(max_length=50,
                            unique=True)
    rating = models.PositiveSmallIntegerField(blank=True,
                                              null=True,
                                              default=1,
                                              verbose_name='Рейтинг Категории')
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name='Описание')
    category_image = models.ImageField(upload_to=get_upload_path_category,
                                       blank=True,
                                       null=True,
                                       verbose_name='Изображение категории')
    thumbnail = ImageSpecField(source='category_image',
                               processors=[ResizeToFill(150, 150)],
                               format='JPEG',
                               options={'quality': 60})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = [
            "-rating",
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse(viewname="catalog:category", args=[self.slug])
